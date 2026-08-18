#!/usr/bin/env bash
# Experimental end-to-end MACE-LAMMPS test for provisional screenshot CIFs.
# Submit from the group-disk working directory with:
#   qsub -g tgj-26ICP run_mace_provisional_test.sh
# This is not a production materials calculation.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N mace_provisional_test
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
VENV="$ROOT/venv"
MODEL="$ROOT/mace-mpa-0-medium.model"
LAMMPS_BIN="${LAMMPS_BIN:-lmp}"

module load python/3.14.3
module load lammps/22Jul2025_u3

if [[ ! -x "$VENV/bin/python" ]]; then
  python -m venv "$VENV"
fi
"$VENV/bin/python" -m pip install --no-cache-dir --upgrade pip
# The MPA-0 checkpoint used here predates the latest converter.  Pin the
# converter version used by the original foundation-model workflow.
"$VENV/bin/python" -m pip install --no-cache-dir --force-reinstall --no-deps mace-torch==0.3.13

"$VENV/bin/python" -m mace.cli.create_lammps_model "$MODEL" --format=libtorch
LAMMPS_MODEL="${MODEL%.model}-lammps.pt"

for system in Li3YCl6 LiNbOCl4; do
  # The site module currently reports no KOKKOS package, so this smoke test
  # intentionally exercises the legacy CPU MACE pair style.
  "$LAMMPS_BIN" -var root "$ROOT" -var model "$LAMMPS_MODEL" \
    -in "$ROOT/in.test.$system"
done
