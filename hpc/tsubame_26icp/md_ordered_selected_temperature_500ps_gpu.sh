#!/usr/bin/env bash
# One selected Li3YCl6 model: 50 ps equilibration + 500 ps production.
# Submit with: MD_TEMP=400 qsub -g tgj-26ICP md_ordered_selected_temperature_500ps_gpu.sh
# Required temperatures for the matched rerun: 400, 500, 600, 700, 800, 1000.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=24:00:00
#$ -N md_selected_mace_gpu
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
TEMP="${MD_TEMP:?set MD_TEMP to 400, 500, 600, 700, 800 or 1000}"
LAMMPS_BIN="$ROOT/lammps-mace-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mpa-0-medium.model-lammps.pt"
TEMPLATE="$ROOT/in.md_ordered_500K_50ps_500ps"
SOURCE_RUN="${SOURCE_RUN:-$ROOT/relax_cell_runs/20260818_193647}"
DATA="$SOURCE_RUN/Li3YCl6_03/Li3YCl6_03_mace_cell_relaxed.data"
RUNROOT="$ROOT/md_runs/selected_${TEMP}K_50ps_eq_500ps_$(date +%Y%m%d_%H%M%S)"
OUTDIR="$RUNROOT/Li3YCl6_03"
INPUT="$OUTDIR/in.${TEMP}K"

case "$TEMP" in 400|500|600|700|800|1000) ;; *) echo "ERROR: unsupported MD_TEMP=$TEMP" >&2; exit 2 ;; esac
module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3
[[ -x "$LAMMPS_BIN" ]] || { echo "ERROR: missing LAMMPS executable" >&2; exit 2; }
[[ -s "$MODEL" ]] || { echo "ERROR: missing MACE model" >&2; exit 2; }
[[ -s "$DATA" ]] || { echo "ERROR: missing relaxed data: $DATA" >&2; exit 2; }
mkdir -p "$OUTDIR"
export LD_LIBRARY_PATH="$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
sed "s/variable T equal 500.0/variable T equal ${TEMP}.0/" "$TEMPLATE" > "$INPUT"
"$LAMMPS_BIN" -echo screen \
  -var data "$DATA" -var model "$MODEL" -var elements "Li Y Cl" \
  -var seed "${TEMP}03" -var out_data "$OUTDIR/Li3YCl6_03_${TEMP}K_final.data" \
  -var out_dump "$OUTDIR/Li3YCl6_03_${TEMP}K_prod.lammpstrj" \
  -var msd_out "$OUTDIR/Li3YCl6_03_${TEMP}K_msd.dat" \
  -in "$INPUT" -log "$OUTDIR/lammps.log"
[[ -s "$OUTDIR/Li3YCl6_03_${TEMP}K_final.data" && -s "$OUTDIR/Li3YCl6_03_${TEMP}K_prod.lammpstrj" && -s "$OUTDIR/Li3YCl6_03_${TEMP}K_msd.dat" ]] || { echo "ERROR: incomplete output" >&2; exit 3; }
echo "PASS: selected Li3YCl6 ${TEMP} K 500 ps run completed: $OUTDIR"
