#!/usr/bin/env bash
# Stage-gated follow-up: production must not start before post-run review.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lszc_npt150
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in 1) T=320;; 2) T=350;; *) exit 2;; esac
INPUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_npt400_8675392/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' 120b631b7d9cd3d34f8a7c015a20275a814166b029db9adf0144b6ef27ab1742 "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 272
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LSZC/nep89/endpoint_npt150_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
PREVIOUS="$INPUT"
for STAGE in ramp equil150; do
 if [ "$STAGE" = ramp ]; then STEPS=20000; START=400; else STEPS=300000; START=$T; fi
 DIR="$OUT/$STAGE"
 mkdir "$DIR"
 cp "$PREVIOUS" "$DIR/model.xyz"
 {
  printf '# Project follow-up, not an exact literature reproduction.\n'
  printf 'potential %s\ntime_step 0.5\n' "$MODEL"
  printf 'ensemble npt_mttk temp %s %s iso 0.0001 0.0001 tperiod 200 pperiod 2000\n' "$START" "$T"
  printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
 } > "$DIR/run.in"
 (cd "$DIR"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$DIR/stdout.txt"
 test "$(head -1 "$DIR/restart.xyz")" = 272
 awk -v n="$((STEPS/100))" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1}END{if(bad||NR!=n)exit 1}' "$DIR/thermo.out"
 printf '%s complete\n' "$STAGE" >> "$OUT/stages_completed.txt"
 PREVIOUS="$DIR/restart.xyz"
done
printf '150 ps NPT complete. STOP for density/energy block review before mean-volume NVT equilibration and 300 ps production.\n' > "$OUT/review_required.txt"
