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
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LMP="${MATGL_LAMMPS_BIN:-$ROOT/lammps-matgl-install/bin/lmp}"
MODEL="${MATGL_MODEL:-$ROOT/m3gnet_matgl.pt}"
DATA="${MATGL_DATA:-$ROOT/Li3YCl6_ordered_03_2x2x2.data}"
OUT="$ROOT/matgl_m3gnet_benchmark"
LOG="$OUT/lammps.log"
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
newton on
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
run 1000
EOF
"$LMP" -k on g 1 -sf kk -log "$LOG" -in "$OUT/in.lmp"
grep -E "Performance:|Loop time|MatGL|MATGL|KOKKOS|Total wall time" "$LOG" || true
echo "PASS: MatGL/M3GNet short benchmark completed"
