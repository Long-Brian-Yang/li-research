#!/usr/bin/env bash
# MACE-MP-0b3-medium ML-IAP/Kokkos GPU smoke benchmark.
#SBATCH --comment=TSUBAME qsub script; submit with qsub -g tgj-26ICP
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N mace0b3_mliap_bench
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS="$ROOT/lammps-mliap-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mp-0b3-medium.model-mliap_lammps.pt"
DATA="$ROOT/Li3YCl6_ordered_03_2x2x2.data"
OUT="$ROOT/mace_mp0b3_mliap_benchmark"
mkdir -p "$OUT"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3
export LD_LIBRARY_PATH="$ROOT/lammps-mliap-gpu-install/lib64:$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$ROOT/lammps-mace/python:$ROOT/venv/lib64/python3.9/site-packages:${PYTHONPATH:-}"

cat > "$OUT/in.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton on
atom_modify map yes
read_data $DATA
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style mliap unified $MODEL 0
pair_coeff * * Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep 0.001
thermo 100
thermo_style custom step temp pe ke etotal press
thermo_modify flush yes
velocity all create 400.0 84731 mom yes rot no dist gaussian
fix nvt all nvt temp 400.0 400.0 0.1
run 1000
EOF

time "$LAMMPS" -k on g 1 -sf kk -pk kokkos newton on neigh half \
  -in "$OUT/in.lmp" -log "$OUT/lammps.log" > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
