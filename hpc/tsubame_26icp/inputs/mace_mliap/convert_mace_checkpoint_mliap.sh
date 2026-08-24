#!/usr/bin/env bash
set -euo pipefail

MODEL="${1:-mace-mpa-0-medium.model}"
if [[ ! -f "$MODEL" ]]; then
  echo "Model not found: $MODEL" >&2
  echo "Usage: $0 /path/to/mace-mpa-0-medium.model" >&2
  exit 2
fi

python -m mace.cli.create_lammps_model "$MODEL" --format=mliap
echo "Converted model should be beside the checkpoint with suffix -mliap_lammps.pt"
