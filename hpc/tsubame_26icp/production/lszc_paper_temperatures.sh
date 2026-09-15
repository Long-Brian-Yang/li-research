#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lszc_paper
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in 1) T=320;;2) T=330;;3) T=340;;4) T=350;;*) exit 2;;esac
# Independent branches from the same pre-production 400 K endpoint.
INPUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_npt400_8675392/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' 120b631b7d9cd3d34f8a7c015a20275a814166b029db9adf0144b6ef27ab1742 "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 272
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LSZC/nep89/paper_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
PREVIOUS="$INPUT"
for STAGE in ramp equil production; do
 case "$STAGE" in
 ramp) STEPS=20000; ENS="npt_mttk temp 400 $T iso 0.0001 0.0001 tperiod 200 pperiod 2000";;
 equil) STEPS=100000; ENS="npt_mttk temp $T $T iso 0.0001 0.0001 tperiod 200 pperiod 2000";;
 production) STEPS=600000; ENS="nvt_mttk temp $T $T tperiod 200";;
 esac
 DIR="$OUT/$STAGE";mkdir "$DIR";cp "$PREVIOUS" "$DIR/model.xyz"
 {
 printf '# Tang2026 SI Fig24 temperatures and 300 ps production; NEP comparison, not exact reproduction.\n'
 printf '# 272 atoms, 0.5 fs, 10 ps ramp and 50 ps NPT are project choices; paper uses tuned MACE, 1088 atoms, 3 fs.\n'
 printf 'potential %s\ntime_step 0.5\nensemble %s\n' "$MODEL" "$ENS"
 printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
 } > "$DIR/run.in"
 (cd "$DIR"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$DIR/stdout.txt"
 test "$(head -1 "$DIR/restart.xyz")" = 272
 awk -v n="$((STEPS/100))" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1}END{if(bad||NR!=n)exit 1}' "$DIR/thermo.out"
 printf '%s complete\n' "$STAGE" >> "$OUT/stages_completed.txt"
 PREVIOUS="$DIR/restart.xyz"
done
printf '300 ps complete; analyse transport and compare with paper.\n' > "$OUT/completed.txt"
