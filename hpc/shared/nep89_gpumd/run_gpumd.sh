#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N team3_nep89
set -euo pipefail
source /gs/fs/tgj-26ICP/team3/nep89_gpumd/paths.sh
WORK=${SGE_O_WORKDIR:?Submit this script using qsub from your input directory}
test -s "$WORK/model.xyz"
test -s "$WORK/run.in"
umask 002
OUT="$WORK/results/${USER:?}_${JOB_ID:?}"
mkdir -p "$WORK/results"
mkdir "$OUT"
cp "$WORK/model.xyz" "$WORK/run.in" "$OUT/"
cp "$0" "$OUT/submitted_job.sh"
cd "$OUT"
sha256sum "$GPUMD_BIN" "$NEP89_MODEL" model.xyz run.in > provenance.sha256
"$GPUMD_BIN" > stdout.txt 2> stderr.txt
test -s thermo.out
awk 'NF<9 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i) ~ /nan|inf/) bad=1} END {if(bad || NR==0) exit 1}' thermo.out
printf 'GPUMD exited successfully; inspect equilibration and physical validity.\n' > completed.txt
