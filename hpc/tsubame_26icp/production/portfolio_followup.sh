#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:20:00
#$ -N portfolio_check
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
case "${SGE_TASK_ID:?}" in
 1|2)
 INPUT="$ROOT/results/amorphous_review_20260915/portfolio_supplement/LiPON_precontact_input.xyz"
 HASH=66c4b08c1056a0a14d2d73825f5849497b2b2f3a6c0a9b8b0d11a72d9b9a4123
 N=124;T=2000
 if [ "$SGE_TASK_ID" = 1 ]; then DT=0.5;STEPS=4000;PERIOD=200;DUMP=20;TAG=dt05;else DT=0.25;STEPS=8000;PERIOD=400;DUMP=40;TAG=dt025;fi
 OUT="$ROOT/runs/amorphous/LiPON/nep89/precontact_${TAG}_${JOB_ID:?}"
 ;;
 3)
 INPUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_npt400_8675392/restart.xyz"
 HASH=120b631b7d9cd3d34f8a7c015a20275a814166b029db9adf0144b6ef27ab1742
 N=272;T=400;DT=0.5;STEPS=400000;PERIOD=200;DUMP=200
 OUT="$ROOT/runs/amorphous/LSZC/nep89/transport400_${JOB_ID:?}"
 ;;
 *) exit 2;;
esac
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = "$N"
module purge
module load gcc/14.2.0 cuda/12.8.0
mkdir "$OUT"
cp "$INPUT" "$OUT/model.xyz"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
{
 printf '# Exploratory control, not exact paper reproduction. Preserve source coordinates and velocities.\n'
 printf '# LiPON: thermostat state reinitialized for both branches; physical coupling100 fs.\n'
 printf 'potential %s\ntime_step %s\nensemble nvt_mttk temp %s %s tperiod %s\n' "$MODEL" "$DT" "$T" "$T" "$PERIOD"
 printf 'dump_thermo %s\ndump_exyz %s 1 1 1\ndump_restart %s\nrun %s\n' "$DUMP" "$DUMP" "$DUMP" "$STEPS"
} > "$OUT/run.in"
(cd "$OUT"; "$GPUMD" > stdout.txt 2> stderr.txt)
grep -q 'Finished running GPUMD' "$OUT/stdout.txt"
test "$(head -1 "$OUT/restart.xyz")" = "$N"
awk -v n="$((STEPS/DUMP))" 'NF!=18 {bad=1} {for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1} END{if(bad||NR!=n)exit 1}' "$OUT/thermo.out"
printf 'Completed numerical checks; scientific analysis required.\n' > "$OUT/completed.txt"
