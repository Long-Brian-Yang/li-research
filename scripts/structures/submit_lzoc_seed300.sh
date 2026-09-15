#!/usr/bin/env bash
# Two velocity-seed repeats per temperature; not independent glass structures.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lzoc_seed300
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
 1) T=340; REP=1; SEED=34009151;;
 2) T=340; REP=2; SEED=34009152;;
 3) T=360; REP=1; SEED=36009151;;
 4) T=360; REP=2; SEED=36009152;;
 *) exit 2;;
esac
case "$T" in
 340) HASH=1a1e9e9f05c44a8de784a90313979d369352739dfe088e29c19403a26d36eaf2;;
 360) HASH=e8c89863a4a78443132caab5efe19f56ab3578ed92ed7035c017c57db1e39e99;;
esac
INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/aimd_aligned_${T}K_8675022/production/model.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
grep -q 'Properties=species:S:1:pos:R:3:mass:R:1:vel:R:3$' "$INPUT"
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/seed300_${T}K_R${REP}_${JOB_ID:?}"
mkdir "$OUT"
mkdir "$OUT/equil50" "$OUT/production"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
printf 'temperature_K=%s\nrepeat=%s\nvelocity_seed=%s\nequilibration_ps=50\nproduction_ps=300\ntime_step_fs=2\n' "$T" "$REP" "$SEED" > "$OUT/settings.txt"
# Remove existing velocities so GPUMD actually initializes the requested seed.
awk 'NR==1{print;next}NR==2{sub(/:vel:R:3/,"");print;next}{if(NF!=8)exit 1;print $1,$2,$3,$4,$5}' "$INPUT" > "$OUT/equil50/model.xyz"
module purge
module load gcc/14.2.0 cuda/12.8.0
for STAGE in equil50 production; do
 if [ "$STAGE" = equil50 ]; then STEPS=25000; ROWS=1000; else
   STEPS=150000; ROWS=6000
   cp "$OUT/equil50/restart.xyz" "$OUT/production/model.xyz"
 fi
 {
   printf 'potential %s\n' "$MODEL"
   if [ "$STAGE" = equil50 ]; then printf 'velocity %s seed %s\n' "$T" "$SEED"; fi
   printf 'time_step 2\nensemble nvt_nhc %s %s 50\ndump_thermo 25\ndump_exyz 50 1 1 1\ndump_restart 500\nrun %s\n' "$T" "$T" "$STEPS"
 } > "$OUT/$STAGE/run.in"
 (cd "$OUT/$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$OUT/$STAGE/stdout.txt"
 test "$(head -1 "$OUT/$STAGE/restart.xyz")" = 192
 awk -v rows="$ROWS" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1}END{if(bad||NR!=rows)exit 1}' "$OUT/$STAGE/thermo.out"
done
printf 'Execution completed; physical stability and repeat analysis pending.\n' > "$OUT/completed.txt"
