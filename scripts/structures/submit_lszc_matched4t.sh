#!/usr/bin/env bash
# Controlled isochoric series; not four independently equilibrated densities.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lszc_matched4t
set -euo pipefail
TASK=${SGE_TASK_ID:-}
if [[ ${1:-} == --plan ]]; then TASK=${2:-}; fi
case "$TASK" in 1) T=320;; 2) T=330;; 3) T=340;; 4) T=350;; *) exit 2;; esac
REPEAT=${LSZC_REPEAT:-1}
case "$REPEAT" in 1|2) ;; *) echo 'LSZC_REPEAT must be 1 or 2' >&2; exit 2;; esac
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
INPUT="$ROOT/materials/candidates/LSZC/production300_inputs/320K.xyz"
HASH=d4b29f986d8a6d548f9e6e320ea7b78df263a0bd0849adc78c60a6309c316b03
SEED=$((9155000+1000*REPEAT+T))
if [[ ${1:-} == --plan ]]; then
 printf 'T=%s repeat=%s seed=%s time_step=0.5\nsource=%s\nequil50|100000\nproduction|600000\n' "$T" "$REPEAT" "$SEED" "$HASH"
 exit 0
fi
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 272
grep -q 'Properties=species:S:1:pos:R:3:mass:R:1:vel:R:3' "$INPUT"
test -x "$GPUMD"
OUT="$ROOT/runs/amorphous/LSZC/nep89/matched4t_R${REPEAT}_${T}K_${JOB_ID:?}"
mkdir "$OUT"
mkdir "$OUT/equil50" "$OUT/production"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
printf 'temperature_K=%s\nrepeat=%s\nseed=%s\ncommon_cell_source=320K.xyz\nensemble=NVT MTTK\ntimestep_fs=0.5\nthermal_coupling_fs=100\n' "$T" "$REPEAT" "$SEED" > "$OUT/settings.txt"
# Preserve positions/cell/masses; remove old velocities before reinitialization.
awk 'NR==1{print;next}NR==2{sub(/:vel:R:3/,"");print;next}{if(NF!=8)exit 1;print $1,$2,$3,$4,$5}' "$INPUT" > "$OUT/equil50/model.xyz"
module purge
module load gcc/14.2.0 cuda/12.8.0
for STAGE in equil50 production; do
 if [[ $STAGE == equil50 ]]; then STEPS=100000; else
   STEPS=600000
   cp "$OUT/equil50/restart.xyz" "$OUT/production/model.xyz"
 fi
 {
   printf 'potential %s\ntime_step 0.5\n' "$MODEL"
   if [[ $STAGE == equil50 ]]; then printf 'velocity %s seed %s\n' "$T" "$SEED"; fi
   printf 'ensemble nvt_mttk temp %s %s tperiod 200\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$T" "$T" "$STEPS"
 } > "$OUT/$STAGE/run.in"
 (cd "$OUT/$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$OUT/$STAGE/stdout.txt"
 test "$(head -1 "$OUT/$STAGE/restart.xyz")" = 272
 awk -v rows="$((STEPS/100))" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0 || $1>3000)bad=1;if($10<=0 || $14<=0 || $18<=0)bad=1}END{if(bad||NR!=rows)exit 1}' "$OUT/$STAGE/thermo.out"
 printf '%s complete\n' "$STAGE" >> "$OUT/stages_completed.txt"
done
printf 'Execution finished; isochoric transport and structure analysis pending. Completion does not establish valid Ea.\n' > "$OUT/completed.txt"
