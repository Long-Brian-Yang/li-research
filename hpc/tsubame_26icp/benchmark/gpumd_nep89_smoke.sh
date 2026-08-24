#!/usr/bin/env bash
# Short NEP89/GPUMD validation for the four relaxed direction-2 structures.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N gpumd_nep89_smoke
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"

module load gcc/14.2.0
module load cuda/13.1.1

GPUMD="$GPUMD_ENGINE"
POTENTIAL="$NEP89_MODEL"
RUNROOT="$RESULTS_ROOT/benchmark/gpumd_nep89/runs_$(date +%Y%m%d_%H%M%S)"

[[ -x "$GPUMD" ]] || { echo "ERROR: missing GPUMD executable" >&2; exit 2; }
[[ -s "$POTENTIAL" ]] || { echo "ERROR: missing NEP89 potential" >&2; exit 2; }
mkdir -p "$RUNROOT"

declare -A STRUCTURES=(
  [Li3YCl6_01]="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_01/Li3YCl6_ordered_01_2x2x2.xyz"
  [Li3YCl6_02]="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_02/Li3YCl6_ordered_02_2x2x2.xyz"
  [Li3YCl6_03]="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.xyz"
  [LiNbOCl4]="$STRUCTURES_ROOT/ordered/LiNbOCl4/2x2x2/LiNbOCl4_ordered_2x2x2.xyz"
)

for name in Li3YCl6_01 Li3YCl6_02 Li3YCl6_03 LiNbOCl4; do
  out="$RUNROOT/$name"
  mkdir -p "$out"
  [[ -s "${STRUCTURES[$name]}" ]] || { echo "ERROR: missing structure: ${STRUCTURES[$name]}" >&2; exit 2; }
  cp "${STRUCTURES[$name]}" "$out/model.xyz"
  cat > "$out/run.in" <<EOF
potential $POTENTIAL
velocity 400 seed 41004
ensemble nvt_lan 400 400 100
time_step 1
dump_thermo 100
dump_exyz 100 1 1 1
run 1000
EOF
  (cd "$out" && "$GPUMD" > gpumd.out 2>&1)
  test -s "$out/gpumd.out"
done
echo "NEP89 GPUMD smoke tests completed: $RUNROOT"
