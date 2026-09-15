#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lzoc192_hold300
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/cooling_8674094/300K/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' af388d2b6a5aa90a2e4bc802656f30efd8bbab296f03b08c8e64ac10ec8f2a7f "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 192
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/hold300_${JOB_ID:?}"
mkdir "$OUT"
cp "$INPUT" "$OUT/model.xyz"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
{
 printf '# Project diagnostic: fixed volume, retained velocities, reinitialized thermostat.\n'
 printf 'potential %s\n' "$MODEL"
 printf 'time_step 0.5\nensemble nvt_mttk temp 300 300 tperiod 200\n'
 printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun 100000\n'
} > "$OUT/run.in"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
grep -q 'Finished running GPUMD' stdout.txt
awk 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=1000) exit 1}' thermo.out
printf '50 ps fixed-cell hold finished. Not a proof of equilibrium; no automatic production.\n' > completed.txt
