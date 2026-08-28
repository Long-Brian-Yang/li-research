#!/usr/bin/env bash
# CPU ML-IAP compatibility check for MACE-MP-0b3-medium (one step).
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:05:00
#$ -N mace0b3_mliap_cpu
set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS="$ROOT/lammps-mliap-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mp-0b3-medium.model-mliap_lammps.pt"
DATA="$ROOT/Li3YCl6_ordered_03_2x2x2.data"
OUT="$ROOT/mace_mp0b3_mliap_cpu_smoke"
mkdir -p "$OUT"
module load gcc/14.2.0 openmpi/5.0.10-gcc python/3.14.3
export LD_LIBRARY_PATH="$ROOT/lammps-mliap-gpu-install/lib64:$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$ROOT/lammps-mace/python:$ROOT/venv/lib64/python3.9/site-packages:${PYTHONPATH:-}"
export MACE_ALLOW_CPU=true
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
pair_style mliap unified $MODEL 0
pair_coeff * * Li Y Cl
timestep 0.001
thermo 1
thermo_style custom step temp pe ke etotal press
velocity all create 400.0 84731 mom yes rot no dist gaussian
fix nve all nve
run 1
EOF
"$LAMMPS" -in "$OUT/in.lmp" -log "$OUT/lammps.log" > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
