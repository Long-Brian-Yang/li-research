#!/usr/bin/env bash
# TSUBAME job body for project/group 26ICP.
# Submit this script with the queue/resource options required by your TSUBAME
# installation; keep the group/account as 26ICP, not the Ishikawa project.
set -euo pipefail

LAMMPS_BIN="${LAMMPS_BIN:-lmp}"
INPUT="${1:?usage: job_tsubame_26icp.sh in.md or in.md.LiNbOCl4}"

echo "project_group=26ICP"
echo "host=$(hostname)"
echo "date=$(date -Is)"
echo "lammps=$LAMMPS_BIN"
echo "input=$INPUT"
command -v "$LAMMPS_BIN"

"$LAMMPS_BIN" -k on g 1 -sf kk -pk kokkos newton on neigh half -in "$INPUT"
