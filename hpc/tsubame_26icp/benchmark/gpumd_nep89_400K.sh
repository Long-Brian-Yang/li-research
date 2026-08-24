#!/usr/bin/env bash
# NEP89 + GPUMD: unified short benchmark, 400 K, 1 fs, 100 + 1000 steps.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N gpumd_nep89_400K
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"

module load gcc/14.2.0
module load cuda/13.1.1

GPUMD="$GPUMD_ENGINE"
POTENTIAL="$NEP89_MODEL"
STRUCTURE="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.xyz"
RUNROOT="$RESULTS_ROOT/md/gpumd_nep89/400K_10ps_eq_100ps_prod_$(date +%Y%m%d_%H%M%S)"

[[ -x "$GPUMD" ]] || { echo "ERROR: missing GPUMD executable" >&2; exit 2; }
[[ -s "$POTENTIAL" ]] || { echo "ERROR: missing NEP89 potential" >&2; exit 2; }
mkdir -p "$RUNROOT"
[[ -s "$STRUCTURE" ]] || { echo "ERROR: missing structure: $STRUCTURE" >&2; exit 2; }

declare -A SEEDS=([Li3YCl6_relaxed]=41003)

for name in Li3YCl6_relaxed; do
  out="$RUNROOT/$name"
  mkdir -p "$out"
  cp "$STRUCTURE" "$out/model.xyz"
  cat > "$out/run.in" <<EOF
potential $POTENTIAL
velocity 400 seed ${SEEDS[$name]}
ensemble nvt_lan 400 400 100
time_step 1
dump_thermo 1000
run 100
run 1000
EOF
  echo "=== Running $name: 10 ps equilibration + 100 ps production ==="
  (cd "$out" && "$GPUMD" > gpumd.out 2>&1)
  grep -q "Finished running GPUMD" "$out/gpumd.out"
  [[ -s "$out/thermo.out" ]] || {
    echo "ERROR: missing output for $name" >&2
    exit 3
  }
done
echo "NEP89 400 K production runs completed: $RUNROOT"
