#!/usr/bin/env bash
# NEP89 + GPUMD: 400 K, 1 fs, 10 ps equilibration + 100 ps production.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N gpumd_nep89_400K
set -euo pipefail

module load gcc/14.2.0
module load cuda/13.1.1

ROOT="${TSUBAME_TEST_ROOT:?set TSUBAME_TEST_ROOT}"
GPUMD="$ROOT/GPUMD/src/gpumd"
POTENTIAL="$ROOT/GPUMD/potentials/nep/nep89_20250409/nep89_20250409.txt"
SMOKE="$ROOT/gpumd_nep89_smoke"
RUNROOT="$SMOKE/runs_400K_10ps_eq_100ps_prod_$(date +%Y%m%d_%H%M%S)"

[[ -x "$GPUMD" ]] || { echo "ERROR: missing GPUMD executable" >&2; exit 2; }
[[ -s "$POTENTIAL" ]] || { echo "ERROR: missing NEP89 potential" >&2; exit 2; }
mkdir -p "$RUNROOT"

declare -A SEEDS=(
  [Li3YCl6_01]=41001
  [Li3YCl6_02]=41002
  [Li3YCl6_03]=41003
  [LiNbOCl4]=41004
)

for name in Li3YCl6_01 Li3YCl6_02 Li3YCl6_03 LiNbOCl4; do
  out="$RUNROOT/$name"
  mkdir -p "$out"
  cp "$SMOKE/$name.xyz" "$out/model.xyz"
  cat > "$out/run.in" <<EOF
potential $POTENTIAL
velocity 400 seed ${SEEDS[$name]}
ensemble nvt_lan 400 400 100
time_step 1
dump_thermo 1000
run 10000
dump_exyz 1000 1 1 1
run 100000
EOF
  echo "=== Running $name: 10 ps equilibration + 100 ps production ==="
  (cd "$out" && "$GPUMD" > gpumd.out 2>&1)
  grep -q "Finished running GPUMD" "$out/gpumd.out"
  [[ -s "$out/dump.xyz" && -s "$out/thermo.out" ]] || {
    echo "ERROR: missing output for $name" >&2
    exit 3
  }
done
echo "NEP89 400 K production runs completed: $RUNROOT"
