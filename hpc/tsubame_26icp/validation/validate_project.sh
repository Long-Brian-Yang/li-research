#!/usr/bin/env bash
# Non-submitting project/environment validation for TSUBAME.
# Run on a login or compute node after the environment modules are available.
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"

fail=0
check_path() { if [[ -e "$1" ]]; then printf 'OK   %s\n' "$1"; else printf 'FAIL %s\n' "$1"; fail=1; fi; }

printf '%s\n' '=== Direction 2 project validation ==='
printf 'YANG_ROOT=%s\nPROJECT_ROOT=%s\n' "$YANG_ROOT" "$PROJECT_ROOT"

for p in "$ENV_ROOT" "$STRUCTURES_ROOT" "$MODELS_ROOT" "$ENGINES_ROOT" \
         "$BENCHMARKS_ROOT" "$RESULTS_ROOT"; do
  check_path "$p"
done

for p in "$MACE_ENV/bin/python" "$SEVENNET_ENV/bin/python" "$MATGL_ENV/bin/python" \
         "$MACE_LMP_MLIAP" "$SEVENNET_LMP" "$MATGL_LMP" \
         "$MATGL_SOURCE_ROOT/src/matgl" "$GPUMD_ENGINE"; do
  check_path "$p"
done

for f in "$MODELS_ROOT/mace/mace-mpa-0-medium.model" \
         "$MODELS_ROOT/mace/mace-mp-0b3-medium.model" \
         "$MODELS_ROOT/sevennet/sevennet_nano_55.pt" \
         "$MODELS_ROOT/m3gnet/m3gnet_matgl_gpu_fixed.pt" "$NEP89_MODEL"; do
  check_path "$f"
done

for f in "$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_01/Li3YCl6_ordered_01_2x2x2.xyz" \
         "$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_02/Li3YCl6_ordered_02_2x2x2.xyz" \
         "$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.xyz" \
         "$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x4/model_03/Li3YCl6_ordered_03_2x2x4.xyz" \
         "$STRUCTURES_ROOT/ordered/LiNbOCl4/2x2x2/LiNbOCl4_ordered_2x2x2.xyz"; do
  check_path "$f"
done

while IFS= read -r -d '' f; do
  bash -n "$f" || { printf 'FAIL shell syntax: %s\n' "$f"; fail=1; }
done < <(find "$HPC_ROOT" -type f -name '*.sh' -print0)

if find "$HPC_ROOT" -type f \( -name '*.sh' -o -name '*.py' \) \
    ! -name 'yang_paths.sh' ! -name 'validate_project.sh' -print0 \
    | xargs -0 grep -nE '/home/2|tga-ishikawalab|/gs/fs/tgj-26ICP/uf03782/li-research' \
    >/tmp/yang_legacy_paths.$$ 2>/dev/null; then
  cat /tmp/yang_legacy_paths.$$
  fail=1
fi
rm -f /tmp/yang_legacy_paths.$$

OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "$MACE_ENV/bin/python" -c 'import mace, torch; print("MACE", mace.__version__, torch.__version__)'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 "$SEVENNET_ENV/bin/python" -c 'import sevenn, torch; print("SevenNet", torch.__version__)'
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONPATH="$MATGL_SOURCE_ROOT/src${PYTHONPATH:+:$PYTHONPATH}" "$MATGL_ENV/bin/python" -c 'import matgl, torch; print("MatGL", torch.__version__, matgl.__file__)'

if (( fail )); then echo 'VALIDATION=FAIL'; exit 1; fi
echo 'VALIDATION=PASS'
