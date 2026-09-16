#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lzoc_hussain192
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
BASE="$ROOT/materials/candidates/LZOC_Hussain2024/seed_192"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
test "$(head -1 "$BASE/model.xyz")" = 192
test -x "$GPUMD"
test -s "$MODEL"
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/trial_${JOB_ID:?}"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
cp "$BASE/model.xyz" "$BASE/run.in" "$BASE/validation.json" "$OUT/"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$GPUMD" "$MODEL" "$BASE/model.xyz" "$BASE/run.in" > "$OUT/provenance.sha256"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
grep -q 'Finished running GPUMD' stdout.txt
awk 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=640) exit 1}' thermo.out
printf '32 ps initial heating trial finished. Not amorphous validation. No automatic continuation.\n' > completed.txt
