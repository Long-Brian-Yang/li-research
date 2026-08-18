#!/usr/bin/env bash
# Isotropic variable-volume relaxation starting from the fixed-cell outputs.
# Submit: qsub -g tgj-26ICP relax_cell_ordered_gpu.sh
# Optional: RELAX_CASE=Li3YCl6_01
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N relax_cell_mace_gpu
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS_BIN="$ROOT/lammps-mace-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mpa-0-medium.model-lammps.pt"
TEMPLATE="$ROOT/in.relax_cell_ordered"
TEMPLATE_LINBO="$ROOT/in.relax_cell_ordered.LiNbOCl4"
SOURCE_RUN="${SOURCE_RUN:-$ROOT/relax_runs/20260818_191100}"
RUNROOT="$ROOT/relax_cell_runs/$(date +%Y%m%d_%H%M%S)"
CASE_FILTER="${RELAX_CASE:-all}"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3

[[ -x "$LAMMPS_BIN" ]] || { echo "ERROR: missing LAMMPS executable: $LAMMPS_BIN" >&2; exit 2; }
[[ -s "$MODEL" ]] || { echo "ERROR: missing MACE model: $MODEL" >&2; exit 2; }
[[ -s "$TEMPLATE" && -s "$TEMPLATE_LINBO" ]] || { echo "ERROR: missing input template" >&2; exit 2; }
nvidia-smi -L
mkdir -p "$RUNROOT"
export LD_LIBRARY_PATH="$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"

run_case() {
  local name="$1" elements="$2"
  if [[ "$CASE_FILTER" != all && "$CASE_FILTER" != "$name" ]]; then return 0; fi
  local input="$TEMPLATE"
  [[ "$name" == LiNbOCl4 ]] && input="$TEMPLATE_LINBO"
  local data="$SOURCE_RUN/$name/${name}_mace_ion_relaxed.data"
  [[ -s "$data" ]] || { echo "ERROR: missing ionic-relaxed data: $data" >&2; exit 2; }
  local outdir="$RUNROOT/$name"
  mkdir -p "$outdir"
  local out_data="$outdir/${name}_mace_cell_relaxed.data"
  local out_dump="$outdir/${name}_mace_cell_relaxed.dump"
  echo "=== $name ==="
  "$LAMMPS_BIN" -echo screen \
    -var data "$data" -var model "$MODEL" -var elements "$elements" \
    -var out_data "$out_data" -var out_dump "$out_dump" \
    -in "$input" -log "$outdir/lammps.log"
  [[ -s "$out_data" && -s "$out_dump" ]] || { echo "ERROR: missing output for $name" >&2; exit 3; }
}

run_case Li3YCl6_01 "Li Y Cl"
run_case Li3YCl6_02 "Li Y Cl"
run_case Li3YCl6_03 "Li Y Cl"
run_case LiNbOCl4 "Li Nb O Cl"
echo "All requested isotropic cell relaxations completed: $RUNROOT"
