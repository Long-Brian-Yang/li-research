#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lzoc192_cool
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/heating_8673813/2000K/restart.xyz"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
printf '%s  %s\n' dfd3caef8a3c32e12d72ae0c803495d9634d88d7377bd98b85110702d59be18a "$INPUT" | sha256sum -c -
test "$(head -1 "$INPUT")" = 192
test -s "$MODEL"
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/cooling_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
PREVIOUS="$INPUT"
for SPEC in 1500:4000 1000:4000 500:4000 100:4000 300:40000; do
  TEMP=${SPEC%:*}; STEPS=${SPEC#*:}
  STAGE="$OUT/${TEMP}K"
  mkdir "$STAGE"
  cp "$PREVIOUS" "$STAGE/model.xyz"
  {
    printf '# Fixed-cell NEP adaptation, NOT the author DFT volume relaxation.\n'
    printf 'potential %s\n' "$MODEL"
    if [[ "$TEMP" == 1500 ]]; then
      printf 'minimize fire 0.01 10000\nvelocity 1500 seed 20260915\n'
    fi
    printf 'time_step 0.5\nensemble nvt_mttk temp %s %s tperiod 200\n' "$TEMP" "$TEMP"
    printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
  } > "$STAGE/run.in"
  cd "$STAGE"
  "$GPUMD" > stdout.txt 2> stderr.txt
  test -s restart.xyz
  grep -q 'Finished running GPUMD' stdout.txt
  awk -v expected="$((STEPS/100))" 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0 || $1>10000) bad=1} END {if(bad || NR!=expected) exit 1}' thermo.out
  PREVIOUS="$STAGE/restart.xyz"
done
printf '28 ps cooling/hold completed. Check minimization convergence, residual pressure, coordination and disorder; NOT validated glass or ambient equilibrium.\n' > "$OUT/completed.txt"
