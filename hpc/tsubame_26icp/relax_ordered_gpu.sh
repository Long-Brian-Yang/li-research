#!/usr/bin/env bash
# Run fixed-cell ionic relaxation for explicit ordered Direction-2 models.
# Submit on TSUBAME with: qsub -g tgj-26ICP relax_ordered_gpu.sh
# Optional: RELAX_CASE=Li3YCl6_01 to run one case only.
# Cell relaxation is intentionally a separate follow-up after this force check.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N relax_mace_gpu
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS_BIN="$ROOT/lammps-mace-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mpa-0-medium.model-lammps.pt"
TEMPLATE="$ROOT/in.relax_ordered"
TEMPLATE_LINBO="$ROOT/in.relax_ordered.LiNbOCl4"
RUNROOT="$ROOT/relax_runs/$(date +%Y%m%d_%H%M%S)"
CASE_FILTER="${RELAX_CASE:-all}"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3

[[ -x "$LAMMPS_BIN" ]] || { echo "ERROR: missing LAMMPS executable: $LAMMPS_BIN" >&2; exit 2; }
[[ -s "$MODEL" ]] || { echo "ERROR: missing MACE model: $MODEL" >&2; exit 2; }
[[ -s "$TEMPLATE" ]] || { echo "ERROR: missing input template: $TEMPLATE" >&2; exit 2; }
[[ -s "$TEMPLATE_LINBO" ]] || { echo "ERROR: missing input template: $TEMPLATE_LINBO" >&2; exit 2; }
nvidia-smi -L

mkdir -p "$RUNROOT"
export LD_LIBRARY_PATH="$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"

run_case() {
  local name="$1" data="$2" elements="$3"
  if [[ "$CASE_FILTER" != all && "$CASE_FILTER" != "$name" ]]; then
    return 0
  fi
  [[ -s "$data" ]] || { echo "ERROR: missing ordered data: $data" >&2; exit 2; }
  local outdir="$RUNROOT/$name"
  mkdir -p "$outdir"
  local out_data="$outdir/${name}_mace_ion_relaxed.data"
  local out_dump="$outdir/${name}_mace_ion_relaxed.dump"
  echo "=== $name ==="
  echo "data=$data"
  echo "elements=$elements"
  # The legacy MACE pair style manages Torch/CUDA itself.  Do not pass
  # -k on here: that switches the whole atom system to Kokkos atom styles,
  # which is incompatible with this `atom_style atomic` MACE input.
  local input="$TEMPLATE"
  [[ "$name" == LiNbOCl4 ]] && input="$TEMPLATE_LINBO"
  "$LAMMPS_BIN" -echo screen \
    -var data "$data" -var model "$MODEL" -var elements "$elements" \
    -var out_data "$out_data" -var out_dump "$out_dump" \
    -in "$input" -log "$outdir/lammps.log"
  [[ -s "$out_data" && -s "$out_dump" ]] || { echo "ERROR: missing relaxation output for $name" >&2; exit 3; }
  echo "output=$out_data"
}

run_case Li3YCl6_01 \
  "$ROOT/structures/ordered/Li3YCl6/2x2x2/model_01/Li3YCl6_ordered_01_2x2x2.data" \
  "Li Y Cl"
run_case Li3YCl6_02 \
  "$ROOT/structures/ordered/Li3YCl6/2x2x2/model_02/Li3YCl6_ordered_02_2x2x2.data" \
  "Li Y Cl"
run_case Li3YCl6_03 \
  "$ROOT/structures/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.data" \
  "Li Y Cl"
run_case LiNbOCl4 \
  "$ROOT/structures/ordered/LiNbOCl4/2x2x2/LiNbOCl4_ordered_2x2x2.data" \
  "Li Nb O Cl"

echo "All requested ionic relaxations completed: $RUNROOT"
