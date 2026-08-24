#!/usr/bin/env bash
# Short SevenNet-Nano 5.5 serial e3gnn benchmark on Li3YCl6 2x2x2.
# Submit with: qsub -g tgj-26ICP sevennet_nano_serial_benchmark.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:20:00
#$ -N sevennano_bench
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
LMP="$SEVENNET_LMP"
DATA="$STRUCTURES_ROOT/Li3YCl6_ordered_03_2x2x2.data"
MODEL="$MODELS_ROOT/sevennet/sevennet_nano_55.pt"
TORCH_LIB="$($SEVENNET_ENV/bin/python -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))')"
export LD_LIBRARY_PATH="$ENGINES_ROOT/lammps/sevennet/install/lib64:$TORCH_LIB:${LD_LIBRARY_PATH:-}"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1

OUT="$BENCHMARKS_ROOT/lammps/sevennet_nano"
mkdir -p "$OUT"
cat > "$OUT/in.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton on
read_data $DATA
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style e3gnn
pair_coeff * * $MODEL Li Y Cl
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

timeout 900 "$LMP" -log "$OUT/lammps.log" -in "$OUT/in.lmp"
grep -E "Performance:|Loop time|PairE3GNN" "$OUT/lammps.log" || true
