#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lszc_prod300
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
 1) T=320; HASH=d4b29f986d8a6d548f9e6e320ea7b78df263a0bd0849adc78c60a6309c316b03; STAGES=production;;
 2) T=350; HASH=f18397b2b92a0863b7b3743f874268c4c0fb0969d26d7e0d160b4c056a9ab69f; STAGES='equil50 production';;
 *) exit 2;;
esac
INPUT="$ROOT/materials/candidates/LSZC/production300_inputs/${T}K.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
OUT="$ROOT/runs/amorphous/LSZC/nep89/production300_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
module purge
module load gcc/14.2.0 cuda/12.8.0
for STAGE in $STAGES; do
 mkdir "$OUT/$STAGE"
 cp "$INPUT" "$OUT/$STAGE/model.xyz"
 if [ "$STAGE" = equil50 ]; then STEPS=100000; ROWS=1000; else STEPS=600000; ROWS=6000; fi
 printf 'potential %s\ntime_step 0.5\nensemble nvt_mttk temp %s %s tperiod 200\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$MODEL" "$T" "$T" "$STEPS" > "$OUT/$STAGE/run.in"
 (cd "$OUT/$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$OUT/$STAGE/stdout.txt"
 test "$(head -1 "$OUT/$STAGE/restart.xyz")" = 272
 awk -v rows="$ROWS" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1}END{if(bad||NR!=rows)exit 1}' "$OUT/$STAGE/thermo.out"
 INPUT="$OUT/$STAGE/restart.xyz"
done
printf 'Execution completed; 350 K fixed-volume results exploratory, NPT density drift unresolved. Physical analysis pending.\n' > "$OUT/completed.txt"
