#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N lszc_nep89_preflight
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
BASE="$ROOT/materials/candidates/LSZC"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
OUT="$ROOT/runs/amorphous/LSZC/nep89/preflight_${JOB_ID:?}"
module purge
module load gcc/14.2.0 cuda/12.8.0
test -x "$GPUMD"
test -s "$MODEL"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
cp "$BASE/input/model.xyz" "$BASE/input/run.in" "$BASE/README.md" "$BASE/validation.json" "$OUT/"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$GPUMD" "$MODEL" "$BASE/input/model.xyz" "$BASE/input/run.in" > "$OUT/provenance.sha256"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
awk 'NF<18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0 || $1>2000) bad=1} END {if(bad || NR!=200) exit 1}' thermo.out
printf '10 ps diagnostic completed. Not equilibrated/validated transport production.\n' > status.txt
