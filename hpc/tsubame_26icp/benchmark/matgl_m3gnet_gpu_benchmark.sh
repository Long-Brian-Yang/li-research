#!/usr/bin/env bash
# MatGL native LAMMPS/M3GNet GPU preflight and short benchmark.
# Submit: qsub -g tgj-26ICP matgl_m3gnet_gpu_benchmark.sh
# Required in TSUBAME_TEST_ROOT: lammps-matgl-install/bin/lmp,
# m3gnet_matgl.pt, and Li3YCl6_ordered_03_2x2x2.data.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:20:00
#$ -N matgl_m3gnet_bench

set -euo pipefail
module load gcc/14.2.0
module load cuda/13.1.1
module load intel/2025.0.0
YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
ROOT="$ENGINES_ROOT/lammps/matgl"
MODEL_ROOT="$MODELS_ROOT/m3gnet"
DATA_ROOT="$STRUCTURES_ROOT"
export MATGL_PYTHON_ENV="$MATGL_ENV"
LMP="$MATGL_LMP"
MODEL="${MATGL_MODEL:-$MODEL_ROOT/m3gnet_matgl_gpu_fixed.pt}"
DATA="${MATGL_DATA:-$DATA_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.data}"
# The installed LAMMPS executable links to its shared library in the same
# prefix; make that library visible on TSUBAME compute nodes.
export LD_LIBRARY_PATH="$MATGL_RUNTIME_LIBS:$MATGL_LAMMPS_BUILD_ROOT:$ROOT/install/lib64:$MATGL_ENV/lib/python3.12/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$MATGL_SOURCE_ROOT/src:$MATGL_ENV/lib/python3.12/site-packages:${PYTHONPATH:-}"
GCC_LIBDIR="$(dirname "$(g++ -print-file-name=libstdc++.so.6)")"
export LD_LIBRARY_PATH="$GCC_LIBDIR:$LD_LIBRARY_PATH"
OUT="$ROOT/matgl_m3gnet_benchmark"
LOG="$OUT/lammps.log"
STEPS="${MATGL_STEPS:-1000}"
mkdir -p "$OUT"
{
  echo "=== MatGL/M3GNet native LAMMPS GPU preflight ==="
  echo "host=$(hostname)"; echo "date=$(date -Is)"; echo "root=$ROOT"
  command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi --query-gpu=name,driver_version --format=csv,noheader || true
  echo "lammps=$LMP"; echo "model=$MODEL"; echo "data=$DATA"
} | tee "$OUT/preflight.txt"
if [[ ! -x "$LMP" ]]; then
  echo "BLOCKED: missing MatGL-enabled LAMMPS executable: $LMP" | tee -a "$OUT/preflight.txt"; exit 3
fi
if [[ ! -s "$MODEL" ]]; then
  echo "BLOCKED: missing exported M3GNet TorchScript model: $MODEL" | tee -a "$OUT/preflight.txt"; exit 3
fi
if [[ ! -s "$DATA" ]]; then
  echo "BLOCKED: missing LAMMPS data file: $DATA" | tee -a "$OUT/preflight.txt"; exit 3
fi
cat > "$OUT/in.lmp" <<EOF
clear
units metal
atom_style atomic
atom_modify map yes
boundary p p p
newton off
read_data $DATA
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style matgl/kk
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
run $STEPS
EOF
"$LMP" -k on g 1 -sf kk -log "$LOG" -in "$OUT/in.lmp"
grep -E "Performance:|Loop time|MatGL|MATGL|KOKKOS|Total wall time" "$LOG" || true
echo "PASS: MatGL/M3GNet short benchmark completed"
