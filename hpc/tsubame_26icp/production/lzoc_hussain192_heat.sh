#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lzoc192_heat
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/trial_8671250/restart.xyz"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
printf '%s  %s\n' 85592b2364660ccd18a902970cd84508ef5f7df3e64d4895d9a03d15e2abad4d "$INPUT" | sha256sum -c -
test "$(head -1 "$INPUT")" = 192
grep -q 'vel:R:3' "$INPUT"
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/heating_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
PREVIOUS="$INPUT"
for SPEC in 1000:100000 1500:60000 2000:40000; do
  TEMP=${SPEC%:*}
  STEPS=${SPEC#*:}
  STAGE="$OUT/${TEMP}K"
  mkdir "$STAGE"
  cp "$PREVIOUS" "$STAGE/model.xyz"
  {
    printf '# NEP89 adaptation; retained velocities, reinitialized thermostat.\n'
    printf 'potential %s\ntime_step 0.5\n' "$MODEL"
    printf 'ensemble nvt_mttk temp %s %s tperiod 200\n' "$TEMP" "$TEMP"
    printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
  } > "$STAGE/run.in"
  cd "$STAGE"
  "$GPUMD" > stdout.txt 2> stderr.txt
  test -s restart.xyz
  grep -q 'Finished running GPUMD' stdout.txt
  awk -v expected="$((STEPS/100))" 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0 || $1>10000) bad=1} END {if(bad || NR!=expected) exit 1}' thermo.out
  PREVIOUS="$STAGE/restart.xyz"
done
printf '100 ps heating completed. Melting NOT yet demonstrated. No relaxation, cooling or transport automatically submitted.\n' > "$OUT/completed.txt"
