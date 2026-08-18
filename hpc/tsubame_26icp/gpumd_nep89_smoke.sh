#!/usr/bin/env bash
# Short NEP89/GPUMD validation for the four relaxed direction-2 structures.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N gpumd_nep89_smoke
set -euo pipefail

module load gcc/14.2.0
module load cuda/13.1.1

ROOT="${TSUBAME_TEST_ROOT:?set TSUBAME_TEST_ROOT}"
GPUMD="$ROOT/GPUMD/src/gpumd"
POTENTIAL="$ROOT/GPUMD/potentials/nep/nep89_20250409/nep89_20250409.txt"
SMOKE="$ROOT/gpumd_nep89_smoke"
RUNROOT="$SMOKE/runs_$(date +%Y%m%d_%H%M%S)"

[[ -x "$GPUMD" ]] || { echo "ERROR: missing GPUMD executable" >&2; exit 2; }
[[ -s "$POTENTIAL" ]] || { echo "ERROR: missing NEP89 potential" >&2; exit 2; }
mkdir -p "$RUNROOT"

for name in Li3YCl6_01 Li3YCl6_02 Li3YCl6_03 LiNbOCl4; do
  out="$RUNROOT/$name"
  mkdir -p "$out"
  cp "$SMOKE/$name.xyz" "$out/model.xyz"
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
