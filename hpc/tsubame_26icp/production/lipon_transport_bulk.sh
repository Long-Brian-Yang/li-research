#!/usr/bin/env bash
# Bulk amorphous LiPON transport from structurally screened Preparation B.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N lipon_bulk_D
set -euo pipefail

ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
  1) T=600 ;;
  2) T=900 ;;
  3) T=1200 ;;
  4) T=1500 ;;
  *) exit 2 ;;
esac

INPUT="$ROOT/runs/amorphous/LiPON/nep89/prep_repeat_R1_8678859/prepared_candidate.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' cd35fbe7ea20123b6dc8f7e2894bed9c061d623919d07dcf5c271ef8883f6ba5 "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test -x "$GPUMD"
test "$(head -1 "$INPUT")" = 124

module purge
module load gcc/14.2.0 cuda/12.8.0

OUT="$ROOT/runs/amorphous/LiPON/nep89/bulk_transport_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
printf 'material=LiPON\npreparation=B\ntemperature_K=%s\ntimestep_fs=0.5\n' "$T" > "$OUT/settings.txt"

PREVIOUS="$INPUT"
for STAGE in ramp equil production; do
  case "$STAGE" in
    ramp)
      STEPS=20000
      ENS="npt_mttk temp 250 $T iso 0.0001 0.0001 tperiod 200 pperiod 2000"
      ;;
    equil)
      STEPS=100000
      ENS="npt_mttk temp $T $T iso 0.0001 0.0001 tperiod 200 pperiod 2000"
      ;;
    production)
      STEPS=600000
      ENS="nvt_mttk temp $T $T tperiod 200"
      ;;
  esac
  DIR="$OUT/$STAGE"
  mkdir "$DIR"
  cp "$PREVIOUS" "$DIR/model.xyz"
  {
    printf '# Bulk LiPON transport; temperatures follow Seth et al. 2025 bulk comparison.\n'
    printf '# NEP89, equilibration length and production length are project settings.\n'
    printf 'potential %s\ntime_step 0.5\nensemble %s\n' "$MODEL" "$ENS"
    printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
  } > "$DIR/run.in"
  (cd "$DIR"; "$GPUMD" > stdout.txt 2> stderr.txt)
  grep -q 'Finished running GPUMD' "$DIR/stdout.txt"
  test "$(head -1 "$DIR/restart.xyz")" = 124
  awk -v n="$((STEPS/100))" -v target="$T" '
    NF != 18 {bad=1}
    {
      for(i=1;i<=NF;i++) if(tolower($i) ~ /nan|inf/) bad=1
      if($1<=0 || $1>5*target) bad=1
      if($10<=0 || $14<=0 || $18<=0) bad=1
    }
    END {if(bad || NR!=n) exit 1}
  ' "$DIR/thermo.out"
  printf '%s complete; numerical checks only\n' "$STAGE" >> "$OUT/stages_completed.txt"
  PREVIOUS="$DIR/restart.xyz"
done

printf '300 ps bulk transport complete; diffusion and structural analysis required.\n' > "$OUT/completed.txt"
