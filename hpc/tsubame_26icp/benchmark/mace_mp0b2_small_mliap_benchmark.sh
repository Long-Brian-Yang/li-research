#!/usr/bin/env bash
# MACE-MP-0b2-small + ML-IAP/Kokkos CUDA benchmark.
# This is the official small MP model available from the MACE foundation set.
# Submit with: qsub -g tgj-26ICP mace_mp0b2_small_mliap_benchmark.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N mace0b2_small
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
PY="$MACE_ENV/bin/python"
LMP="$ENGINES_ROOT/lammps/mace/install_mliap_gpu/bin/lmp"
MODEL="$MODELS_ROOT/mace/mace-mp-0b2-small.model-mliap_lammps.pt"
SOURCE_MODEL="$MODELS_ROOT/mace/mace-mp-0b2-small.model"
DATA="$STRUCTURES_ROOT/Li3YCl6_ordered_03_2x2x2.data"
OUT="$BENCHMARKS_ROOT/lammps/mace_mliap_gpu/mace_mp0b2_small"

module purge
module load gcc/14.2.0
module load cuda/12.8.0
module load openmpi/5.0.7-gcc
export CUDA_VISIBLE_DEVICES=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONHOME="$MACE_ENV"

TORCH_LIB="$($PY -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))')"
CUDA_PY_LIBS="$(find "$MACE_ENV" -type d -path '*/site-packages/nvidia/*/lib' -printf '%p:')"
export LD_LIBRARY_PATH="$ENGINES_ROOT/lammps/mace/install_mliap_gpu/lib64:$ENGINES_ROOT/lammps/mace/install_mliap_gpu/lib:$MACE_ENV/lib:$TORCH_LIB:$CUDA_PY_LIBS${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export PYTHONPATH="$ENGINES_ROOT/lammps/mace/source/build-mliap-gpu-maceenv-canonical/buildwheel/lib/python3.10/site-packages${PYTHONPATH:+:$PYTHONPATH}"

mkdir -p "$OUT"
{
  echo "model=MACE-MP-0b2-small"
  echo "source_model=$SOURCE_MODEL"
  echo "python=$($PY -V 2>&1)"
  "$PY" -c 'import torch,mace; print("mace", mace.__version__); print("torch", torch.__version__, "cuda", torch.version.cuda, "available", torch.cuda.is_available())'
  ompi_info --parsable --all | grep 'mpi_built_with_cuda_support:value' || true
  nvidia-smi --query-gpu=name,driver_version --format=csv,noheader || true
} > "$OUT/preflight.txt" 2>&1

if [[ ! -s "$MODEL" ]]; then
  "$PY" -m mace.cli.create_lammps_model "$SOURCE_MODEL" --format=mliap
fi
[[ -s "$MODEL" ]]
[[ -x "$LMP" ]]

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
pair_style mliap unified $MODEL 0
pair_coeff * * Li Y Cl
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
timeout 1800 "$LMP" -k on g 1 -sf kk -pk kokkos newton on neigh half \
  -log "$OUT/lammps.log" -in "$OUT/in.lmp" > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
grep -E "Performance:|Loop time|ERROR|Segmentation|Total wall|MACE" "$OUT/lammps.log" | tee "$OUT/summary.txt"
grep -q "Performance:" "$OUT/lammps.log"
