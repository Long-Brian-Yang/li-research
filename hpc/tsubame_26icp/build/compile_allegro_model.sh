#!/usr/bin/env bash
# Compile an Allegro checkpoint for LAMMPS AOTInductor execution.
set -euo pipefail
source "${YANG_PATHS_FILE:-/gs/fs/tgj-26ICP/uf03782/yang/li-research/hpc/tsubame_26icp/config/yang_paths.sh}"
ENV="${ALLEGRO_ENV:-$ENV_ROOT/allegro_env}"
INPUT_CHECKPOINT="${1:?Usage: $0 CHECKPOINT OUTPUT_PT2 [cuda|cpu]}"
OUTPUT_MODEL="${2:?Usage: $0 CHECKPOINT OUTPUT_PT2 [cuda|cpu]}"
DEVICE="${3:-cuda}"
"$ENV/bin/nequip-compile" "$INPUT_CHECKPOINT" "$OUTPUT_MODEL" \
  --device "$DEVICE" --mode aotinductor --target pair_allegro
echo "Compiled Allegro model: $OUTPUT_MODEL"
