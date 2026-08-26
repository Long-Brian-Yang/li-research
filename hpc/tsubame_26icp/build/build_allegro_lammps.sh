#!/usr/bin/env bash
# Build/install the official NequIP-Allegro LAMMPS interface on TSUBAME.
set -euo pipefail
source "${YANG_PATHS_FILE:-/gs/fs/tgj-26ICP/uf03782/yang/li-research/hpc/tsubame_26icp/config/yang_paths.sh}"
module purge
module load gcc/14.2.0
module load cmake
module load openmpi/5.0.10-gcc
PYTHON_BIN="${PYTHON_BIN:-python3}"
ENV="$ENV_ROOT/allegro_env"
mkdir -p "$ENV_ROOT" "$ENGINES_ROOT/lammps/allegro" "$MODELS_ROOT/allegro"
if [[ ! -x "$ENV/bin/python" ]]; then "$PYTHON_BIN" -m venv "$ENV"; fi
"$ENV/bin/python" -m pip install --upgrade pip setuptools wheel
"$ENV/bin/python" -m pip install 'nequip-allegro>=0.7' 'allegro>=0.7'
echo "Environment ready: $ENV"
echo "Next: compile a checkpoint with nequip-compile and build LAMMPS pair_allegro."
