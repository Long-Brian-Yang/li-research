#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N lszc272_npt12
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
BASE="$ROOT/materials/candidates/LSZC/seed_272"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
OUT="$ROOT/runs/amorphous/LSZC/nep89/seed272_npt_${JOB_ID:?}"
test "$(head -1 "$BASE/model.xyz")" = 272
test -x "$GPUMD"
test -s "$MODEL"
module purge
module load gcc/14.2.0 cuda/12.8.0
mkdir "$OUT"
cp "$BASE/model.xyz" "$BASE/run.in" "$BASE/validation.json" "$OUT/"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$GPUMD" "$MODEL" "$BASE/model.xyz" "$BASE/run.in" > "$OUT/provenance.sha256"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
grep -q 'Finished running GPUMD' stdout.txt
awk 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=240) exit 1}' thermo.out
printf '12 ps NPT finished; amorphous character and stationarity NOT yet validated. No automatic continuation.\n' > completed.txt
