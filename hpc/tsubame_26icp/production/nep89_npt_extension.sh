#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N nep89_npt50
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${TARGET_TEMP:-}" in
  700) ORIGINAL=700K_R1_8653328 ;;
  800) ORIGINAL=800K_R1_8653329 ;;
  900) ORIGINAL=900K_R1_8653330 ;;
  *) echo 'TARGET_TEMP must be 700, 800 or 900' >&2; exit 2 ;;
esac
INPUT="$ROOT/runs/amorphous/LZOC/nep89/$ORIGINAL/equilibration/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
render_input() {
  printf '# Continued from %s; positions/cell/velocities retained, extended ensemble state reinitialized.\n' "$INPUT"
  printf 'potential %s\ntime_step 0.5\n' "$MODEL"
  printf 'ensemble npt_mttk temp %s %s iso 0.0001 0.0001 tperiod 200 pperiod 2000\n' "$TARGET_TEMP" "$TARGET_TEMP"
  printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun 100000\n'
}
if [[ "${1:-}" == --print-input ]]; then render_input; exit 0; fi
test -s "$INPUT"
test -x "$GPUMD"
test "$(head -1 "$INPUT")" = 192
grep -q 'vel:R:3' "$INPUT"
printf '%s  %s\n' "${SOURCE_SHA:?must pin source restart at submission}" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
printf '%s  %s\n' c6fc625521b12a53f6ae25363c67a9a31c54d1f3dc8d29c3610b6ddae77b4773 "$GPUMD" | sha256sum -c -
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC/nep89/${TARGET_TEMP}K_npt_extension_${JOB_ID:?}"
# Deliberately fail if output already exists: no overwrite or automatic production.
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
cp "$INPUT" "$OUT/model.xyz"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
render_input > "$OUT/run.in"
cd "$OUT"
printf 'source=%s\nsource_job=%s\nadditional_ps=50\noriginal_npt_offset_ps=50\nensemble_state=reinitialized\n' "$INPUT" "$ORIGINAL" > parameters.txt
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
grep -q 'Finished running GPUMD' stdout.txt
awk 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i) ~ /nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=1000) exit 1}' thermo.out
printf '50 ps NPT completed; scientific stationarity not yet assessed. No production submitted.\n' > completed.txt
