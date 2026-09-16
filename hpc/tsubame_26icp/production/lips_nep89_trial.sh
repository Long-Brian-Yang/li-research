#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N lips_nep89_trial
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
BASE="$ROOT/materials/candidates/Li3PS4_glass"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
OUT="$ROOT/runs/amorphous/Li3PS4/nep89/preparation_${JOB_ID:?}"
module purge
module load gcc/14.2.0 cuda/12.8.0
test -x "$GPUMD"
test -s "$MODEL"
mkdir -p "$(dirname "$OUT")"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
cp "$BASE/README.md" "$BASE/validation.json" "$OUT/"
sha256sum "$GPUMD" "$MODEL" "$BASE/input/model.xyz" > "$OUT/provenance.sha256"
cd "$OUT"
PREVIOUS="$BASE/input/model.xyz"
for STAGE in smoke heating melt quench relaxation; do
  mkdir "$STAGE"
  cp "$PREVIOUS" "$STAGE/model.xyz"
  case "$STAGE" in
    smoke) STEPS=2000; ENSEMBLE='nvt_mttk temp 300 300 tperiod 200' ;;
    heating) STEPS=20000; ENSEMBLE='npt_mttk temp 300 1500 iso 0.0001 0.0001 tperiod 200 pperiod 2000' ;;
    melt) STEPS=200000; ENSEMBLE='npt_mttk temp 1500 1500 iso 0.0001 0.0001 tperiod 200 pperiod 2000' ;;
    quench) STEPS=960000; ENSEMBLE='npt_mttk temp 1500 300 iso 0.0001 0.0001 tperiod 200 pperiod 2000' ;;
    relaxation) STEPS=40000; ENSEMBLE='npt_mttk temp 300 300 iso 0.0001 0.0001 tperiod 200 pperiod 2000' ;;
  esac
  {
    printf 'potential %s\ntime_step 0.5\n' "$MODEL"
    if [[ "$STAGE" == smoke ]]; then
      printf 'minimize fire 0.01 10000\nvelocity 300 seed 20260914\n'
    fi
    printf 'ensemble %s\ndump_thermo 100\ndump_exyz 2000 1 1 1\ndump_restart 2000\nrun %s\n' "$ENSEMBLE" "$STEPS"
  } > "$STAGE/run.in"
  (cd "$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
  test -s "$STAGE/restart.xyz"
  if [[ "$STAGE" == smoke ]]; then
    awk '/f_max =/ {f=$(NF-1); found=1} END {if(!found || f>=0.01) exit 1}' "$STAGE/stdout.txt"
  fi
  # Numerical guardrails, not proof of equilibration or potential accuracy.
  awk -v expected="$((STEPS / 100))" 'NF<18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0 || $1>5000) bad=1; v=$10*$14*$18; if(v<5161 || v>20646) bad=1} END {if(bad || NR!=expected) exit 1}' "$STAGE/thermo.out"
  printf '%s completed\n' "$STAGE" >> stages_completed.txt
  PREVIOUS="$OUT/$STAGE/restart.xyz"
done
cp relaxation/restart.xyz prepared_candidate.xyz
printf 'Preparation completed; glass character and equilibration require analysis before production.\n' > preparation_status.txt
