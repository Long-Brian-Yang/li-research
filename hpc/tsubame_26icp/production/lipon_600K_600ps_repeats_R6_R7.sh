#!/usr/bin/env bash
# Two additional independent-velocity 600 K LiPON repeats.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N lipon600_r67
set -euo pipefail

ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
  1) REP=6; SEED=60009156 ;;
  2) REP=7; SEED=60009157 ;;
  *) exit 2 ;;
esac

T=600
INPUT="$ROOT/runs/amorphous/LiPON/nep89/prep_repeat_R1_8678859/prepared_candidate.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' cd35fbe7ea20123b6dc8f7e2894bed9c061d623919d07dcf5c271ef8883f6ba5 "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test -x "$GPUMD"
test "$(head -1 "$INPUT")" = 124

OUT="$ROOT/runs/amorphous/LiPON/nep89/bulk_transport_600K_R${REP}_600ps_${JOB_ID:?}"
mkdir "$OUT" "$OUT/ramp" "$OUT/equil" "$OUT/production"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
printf 'material=LiPON\npreparation=B\ntemperature_K=600\nreplica=%s\nvelocity_seed=%s\ntimestep_fs=0.5\nproduction_ps=600\n' \
  "$REP" "$SEED" > "$OUT/settings.txt"

awk 'NR==1{print;next} NR==2{sub(/:vel:R:3/,"");print;next} {if(NF!=8)exit 1;print $1,$2,$3,$4,$5}' \
  "$INPUT" > "$OUT/ramp/model.xyz"

module purge
module load gcc/14.2.0 cuda/12.8.0

for STAGE in ramp equil production; do
  case "$STAGE" in
    ramp)
      STEPS=20000
      ENS="npt_mttk temp 250 600 iso 0.0001 0.0001 tperiod 200 pperiod 2000"
      ;;
    equil)
      STEPS=100000
      ENS="npt_mttk temp 600 600 iso 0.0001 0.0001 tperiod 200 pperiod 2000"
      cp "$OUT/ramp/restart.xyz" "$OUT/equil/model.xyz"
      ;;
    production)
      STEPS=1200000
      ENS="nvt_mttk temp 600 600 tperiod 200"
      cp "$OUT/equil/restart.xyz" "$OUT/production/model.xyz"
      ;;
  esac
  {
    printf 'potential %s\ntime_step 0.5\n' "$MODEL"
    if [ "$STAGE" = ramp ]; then printf 'velocity 250 seed %s\n' "$SEED"; fi
    printf 'ensemble %s\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$ENS" "$STEPS"
  } > "$OUT/$STAGE/run.in"
  (cd "$OUT/$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
  grep -q 'Finished running GPUMD' "$OUT/$STAGE/stdout.txt"
  test "$(head -1 "$OUT/$STAGE/restart.xyz")" = 124
  awk -v n="$((STEPS/100))" '
    NF != 18 {bad=1}
    {
      for(i=1;i<=NF;i++) if(tolower($i) ~ /nan|inf/) bad=1
      if($1<=0 || $1>3000) bad=1
      if($10<=0 || $14<=0 || $18<=0) bad=1
    }
    END {if(bad || NR!=n) exit 1}
  ' "$OUT/$STAGE/thermo.out"
done

printf '600 K, 600 ps production complete; diffusion analysis required.\n' > "$OUT/completed.txt"
