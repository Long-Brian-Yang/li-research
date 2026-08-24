#!/usr/bin/env bash
# NEP89 + GPUMD: 300 K production for Li3YCl6 2x2x4 and LiNbOCl4 2x2x2.
# Set SHORT_STEPS=1000, EQ_STEPS=0, PRODUCTION_STEPS=1000 for a smoke check.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=4:00:00
#$ -N gpumd_nep89_300K
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"

module load gcc/14.2.0
module load cuda/13.1.1

GPUMD="$GPUMD_ENGINE"
POTENTIAL="$NEP89_MODEL"
STRUCT="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x4"
RUNROOT="$RESULTS_ROOT/md/gpumd_nep89/300K_2x2x4_$(date +%Y%m%d_%H%M%S)"
EQ_STEPS="${EQ_STEPS:-100000}"
PRODUCTION_STEPS="${PRODUCTION_STEPS:-1000000}"
FRAME_INTERVAL="${FRAME_INTERVAL:-1000}"

[[ -x "$GPUMD" ]] || { echo "ERROR: missing GPUMD executable" >&2; exit 2; }
[[ -s "$POTENTIAL" ]] || { echo "ERROR: missing NEP89 potential" >&2; exit 2; }
mkdir -p "$RUNROOT"

declare -A FILES=(
  [Li3YCl6_01]="$STRUCT/model_01/Li3YCl6_ordered_01_2x2x4.xyz"
  [Li3YCl6_02]="$STRUCT/model_02/Li3YCl6_ordered_02_2x2x4.xyz"
  [Li3YCl6_03]="$STRUCT/model_03/Li3YCl6_ordered_03_2x2x4.xyz"
  [LiNbOCl4]="$STRUCTURES_ROOT/ordered/LiNbOCl4/2x2x2/LiNbOCl4_ordered_2x2x2.xyz"
)
declare -A SEEDS=([Li3YCl6_01]=31001 [Li3YCl6_02]=31002 [Li3YCl6_03]=31003 [LiNbOCl4]=31004)

for name in Li3YCl6_01 Li3YCl6_02 Li3YCl6_03 LiNbOCl4; do
  out="$RUNROOT/$name"
  mkdir -p "$out"
  [[ -s "${FILES[$name]}" ]] || { echo "ERROR: missing structure: ${FILES[$name]}" >&2; exit 2; }
  cp "${FILES[$name]}" "$out/model.xyz"
  cat > "$out/run.in" <<EOF
potential $POTENTIAL
velocity 300 seed ${SEEDS[$name]}
ensemble nvt_lan 300 300 100
time_step 1
dump_thermo 1000
run $EQ_STEPS
dump_exyz $FRAME_INTERVAL 1 1 1
run $PRODUCTION_STEPS
EOF
  echo "=== Running $name: $EQ_STEPS equilibration steps + $PRODUCTION_STEPS production steps ==="
  (cd "$out" && "$GPUMD" > gpumd.out 2>&1)
  grep -q "Finished running GPUMD" "$out/gpumd.out"
  # A short smoke run may end before the first thermo dump; production runs
  # use 1000-step thermo output and will contain thermo.out data.
  [[ -s "$out/dump.xyz" ]] || { echo "ERROR: missing trajectory for $name" >&2; exit 3; }
done
echo "NEP89 300 K runs completed: $RUNROOT"
