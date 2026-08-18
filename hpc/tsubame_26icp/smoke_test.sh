#!/usr/bin/env bash
# Minimal TSUBAME 26ICP environment smoke test.
# Submit with: qsub -g tgj-26ICP smoke_test.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N mace_lammps_smoke
set -euo pipefail

echo "=== TSUBAME MACE/LAMMPS smoke test ==="
echo "project_group=tgj-26ICP"
echo "host=$(hostname)"
echo "date=$(date -Is)"

module load lammps/22Jul2025_u3
echo "cuda=$(command -v nvidia-smi || true)"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader || true
echo "lammps=$(command -v lmp)"

# Empty input checks that the batch-node executable starts and exits cleanly.
# A real MACE test additionally needs an ordered CIF, a converted model, and
# a GPU allocation; those are intentionally not fabricated here.
timeout 30s lmp -echo screen -log none -in /dev/null
echo "lammps_empty_input=PASS"
