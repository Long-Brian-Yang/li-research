#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=4:00:00
#$ -N lzoc_nep89_600
set -euo pipefail
TARGET_TEMP=${TARGET_TEMP:-600}
case "$TARGET_TEMP" in 600|700|800|900) ;; *) echo 'Unsupported TARGET_TEMP' >&2; exit 2 ;; esac
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
module purge
module load gcc/14.2.0 cuda/12.8.0
SRC="$ROOT/engines/gpumd/source"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
INPUT="$ROOT/materials/candidates/LZOC/archive/nep89_input/model.xyz"
OUT="$ROOT/runs/amorphous/LZOC/nep89/${TARGET_TEMP}K_R1_${JOB_ID:?}"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
test -x "$SRC/src/gpumd"
cd "$OUT"
sha256sum "$MODEL" "$INPUT" "$SRC/src/gpumd" > provenance.sha256
printf 'TARGET_TEMP=%s\nvelocity_seed=20260912\n' "$TARGET_TEMP" > parameters.txt
for STAGE in smoke heating equilibration production; do
  mkdir "$STAGE"
  case "$STAGE" in
    smoke) cp "$INPUT" "$STAGE/model.xyz"; STEPS=2000; ENSEMBLE='nvt_mttk temp 300 300 tperiod 200' ;;
    heating) cp smoke/restart.xyz "$STAGE/model.xyz"; STEPS=20000; ENSEMBLE="nvt_mttk temp 300 ${TARGET_TEMP} tperiod 200" ;;
    equilibration) cp heating/restart.xyz "$STAGE/model.xyz"; STEPS=100000; ENSEMBLE="npt_mttk temp ${TARGET_TEMP} ${TARGET_TEMP} iso 0.0001 0.0001 tperiod 200 pperiod 2000" ;;
    production) cp equilibration/restart.xyz "$STAGE/model.xyz"; STEPS=400000; ENSEMBLE="nvt_mttk temp ${TARGET_TEMP} ${TARGET_TEMP} tperiod 200" ;;
  esac
  # Generate run.in from this archived, versioned job specification.
  {
    printf 'potential %s\ntime_step 0.5\n' "$MODEL"
    if [[ "$STAGE" == smoke ]]; then
      printf 'minimize fire 0.01 10000\nvelocity 300 seed 20260912\n'
    fi
    printf 'ensemble %s\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$ENSEMBLE" "$STEPS"
  } > "$STAGE/run.in"
  (cd "$STAGE"; "$SRC/src/gpumd" > stdout.txt 2> stderr.txt)
  test -s "$STAGE/restart.xyz"
  if [[ "$STAGE" == smoke ]]; then
    awk '/f_max =/ {f=$(NF-1); found=1} END {if(!found || f>=0.01) exit 1}' "$STAGE/stdout.txt"
  fi
  # Reject incomplete/non-finite results before advancing to the next stage.
  awk -v expected="$((STEPS / 100))" 'NF < 9 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i) ~ /nan|inf/) bad=1; if($1<=0 || $1>3000) bad=1} END {if(bad || NR!=expected) exit 1}' "$STAGE/thermo.out"
  printf '%s completed\n' "$STAGE" >> stages_completed.txt
done
