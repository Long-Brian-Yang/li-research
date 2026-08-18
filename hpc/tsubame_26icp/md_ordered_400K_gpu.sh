#!/usr/bin/env bash
# Run 400 K NVT MD: 10 ps equilibration + 100 ps production.
# Submit: qsub -g tgj-26ICP md_ordered_400K_gpu.sh
# Optional: MD_CASE=Li3YCl6_01
#$ -cwd
#$ -V
#$ -l gpu_1=1
# Full 110 ps runs need about 13.5 h at the measured MACE speed (~2.3 steps/s).
# Keep a small margin for initialization and file I/O.
#$ -l h_rt=14:00:00
#$ -N md_400K_mace_gpu
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS_BIN="$ROOT/lammps-mace-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mpa-0-medium.model-lammps.pt"
TEMPLATE="$ROOT/in.md_ordered_400K"
TEMPLATE_LINBO="$ROOT/in.md_ordered_400K.LiNbOCl4"
SOURCE_RUN="${SOURCE_RUN:-$ROOT/relax_cell_runs/20260818_193647}"
RUNROOT="$ROOT/md_runs/400K_10ps_eq_100ps_prod_$(date +%Y%m%d_%H%M%S)"
CASE_FILTER="${MD_CASE:-all}"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3
[[ -x "$LAMMPS_BIN" ]] || { echo "ERROR: missing LAMMPS executable" >&2; exit 2; }
[[ -s "$MODEL" ]] || { echo "ERROR: missing MACE model" >&2; exit 2; }
mkdir -p "$RUNROOT"
export LD_LIBRARY_PATH="$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"

run_case() {
  local name="$1" elements="$2" seed="$3"
  if [[ "$CASE_FILTER" != all && "$CASE_FILTER" != "$name" ]]; then return 0; fi
  local input="$TEMPLATE"
  [[ "$name" == LiNbOCl4 ]] && input="$TEMPLATE_LINBO"
  local data="$SOURCE_RUN/$name/${name}_mace_cell_relaxed.data"
  [[ -s "$data" ]] || { echo "ERROR: missing cell-relaxed data: $data" >&2; exit 2; }
  local outdir="$RUNROOT/$name"
  mkdir -p "$outdir"
  echo "=== $name at 400 K ==="
  "$LAMMPS_BIN" -echo screen \
    -var data "$data" -var model "$MODEL" -var elements "$elements" \
    -var seed "$seed" -var out_data "$outdir/${name}_400K_final.data" \
    -var out_dump "$outdir/${name}_400K_prod.lammpstrj" \
    -in "$input" -log "$outdir/lammps.log"
  [[ -s "$outdir/${name}_400K_final.data" && -s "$outdir/${name}_400K_prod.lammpstrj" ]] || {
    echo "ERROR: missing MD output for $name" >&2; exit 3;
  }
}

run_case Li3YCl6_01 "Li Y Cl" 41001
run_case Li3YCl6_02 "Li Y Cl" 41002
run_case Li3YCl6_03 "Li Y Cl" 41003
run_case LiNbOCl4 "Li Nb O Cl" 41004
echo "All requested 400 K MD runs completed: $RUNROOT"
