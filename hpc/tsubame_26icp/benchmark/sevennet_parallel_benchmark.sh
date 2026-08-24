#!/usr/bin/env bash
# SevenNet e3gnn/parallel benchmark on Li3YCl6.
# One MPI rank is used per GPU, as required by the official SevenNet backend.
# Submit with: qsub -g tgj-26ICP sevennet_parallel_benchmark.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:20:00
#$ -N sevennet_bench
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
LMP="$ENGINES_ROOT/lammps/sevennet/install/bin/lmp"
DATA="$STRUCTURES_ROOT/Li3YCl6_ordered_03_2x2x2.data"
SEVENNET_TORCH_LIB="$($SEVENNET_ENV/bin/python -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))')"
export LD_LIBRARY_PATH="$ENGINES_ROOT/lammps/sevennet/install/lib64:$SEVENNET_TORCH_LIB:${LD_LIBRARY_PATH:-}"

module purge
module load gcc/14.2.0
module load cuda/12.8.0
module load openmpi/5.0.7-gcc
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1

NP="${SEVENNET_NGPU:-1}"
if ! [[ "$NP" =~ ^[1-9][0-9]*$ ]]; then
  echo "SEVENNET_NGPU must be a positive integer" >&2
  exit 2
fi
if [[ ! -x "$LMP" ]]; then
  echo "Missing SevenNet LAMMPS executable: $LMP" >&2
  exit 3
fi
if ! command -v mpirun >/dev/null 2>&1; then
  echo "mpirun is required for e3gnn/parallel" >&2
  exit 4
fi

OUT="$BENCHMARKS_ROOT/lammps/sevennet_parallel/np${NP}"
mkdir -p "$OUT"
MODEL_DIR="$MODELS_ROOT/sevennet/sevennet_omni_mpa"
for i in 0 1 2 3 4; do
  [[ -f "$MODEL_DIR/deployed_parallel_${i}.pt" ]] || { echo "Missing deployed model $i" >&2; exit 5; }
done
cat > "$OUT/in.lmp" <<EOF
clear
units metal
atom_style atomic
atom_modify map yes
boundary p p p
newton on
read_data $DATA
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style e3gnn/parallel
pair_coeff * * 5 $MODEL_DIR/deployed_parallel_0.pt $MODEL_DIR/deployed_parallel_1.pt $MODEL_DIR/deployed_parallel_2.pt $MODEL_DIR/deployed_parallel_3.pt $MODEL_DIR/deployed_parallel_4.pt Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep 0.001
velocity all create 400.0 84731 mom yes rot no dist gaussian
thermo 100
thermo_style custom step temp pe ke etotal press
thermo_modify flush yes
fix nvt all nvt temp 400.0 400.0 0.1
run 100
reset_timestep 0
run 1000
EOF

cd "$OUT"
ompi_info --parsable --all | grep 'mpi_built_with_cuda_support:value' > "$OUT/mpi_cuda_support.txt" || true
printf 'NP=%s\n' "$NP" > "$OUT/run_metadata.txt"
printf 'LMP=%s\n' "$LMP" >> "$OUT/run_metadata.txt"
timeout 900 mpirun --bind-to none -np "$NP" "$LMP" -log "$OUT/lammps.log" -in "$OUT/in.lmp"
grep -E "Performance:|MPI task|PairE3GNNParallel|Loop time" "$OUT/lammps.log" | tee "$OUT/summary.txt"
grep -q "PairE3GNNParallel using device : CUDA" "$OUT/lammps.log"
grep -q "PairE3GNNParallel cuda-aware mpi : True" "$OUT/lammps.log"
