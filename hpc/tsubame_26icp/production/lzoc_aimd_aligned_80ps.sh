#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lzoc_nhc80
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
 1) T=340; HASH=1a1e9e9f05c44a8de784a90313979d369352739dfe088e29c19403a26d36eaf2;;
 2) T=360; HASH=e8c89863a4a78443132caab5efe19f56ab3578ed92ed7035c017c57db1e39e99;;
 3) T=380; HASH=2006cc9502d9ae18133c81d8b27fd02890484b5f20f799c0f102eb14d0df5dd9;;
 *) exit 2;;
esac
INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/transport_${T}K_8674278/equil/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 192
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/aimd_aligned_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
for STAGE in smoke production; do
 if [[ "$STAGE" == smoke ]]; then STEPS=1000; else STEPS=40000; fi
 DIR="$OUT/$STAGE"; mkdir "$DIR"
 # Restart both runs from identical old production-start state; smoke is not appended.
 cp "$INPUT" "$DIR/model.xyz"
 {
  printf '# NEP control, not exact AIMD reproduction. Prior preparation retained.\n'
  printf '# 100 fs coupling is a project choice, not a verified paper parameter.\n'
  printf 'potential %s\ntime_step 2\n' "$MODEL"
  printf 'ensemble nvt_nhc %s %s 50\n' "$T" "$T"
  printf 'dump_thermo 25\ndump_exyz 50 1 1 1\ndump_restart 500\nrun %s\n' "$STEPS"
 } > "$DIR/run.in"
 cd "$DIR"
 "$GPUMD" > stdout.txt 2> stderr.txt
 grep -q 'Finished running GPUMD' stdout.txt
 test -s restart.xyz
 test "$(head -1 restart.xyz)" = 192
 awk -v expected="$((STEPS/25))" -v target="$T" '
 NF!=18 {bad=1}
 {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1;
  if($1<=0 || $1>5*target) bad=1; sum+=$1}
 END {if(bad || NR!=expected || sum/NR<0.5*target || sum/NR>1.5*target) exit 1}' thermo.out
done
printf '80 ps finished; finite-output checks passed. Structural and transport validation pending.\n' > "$OUT/completed.txt"
