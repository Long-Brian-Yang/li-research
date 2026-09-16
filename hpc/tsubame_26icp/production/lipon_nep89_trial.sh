#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lipon_nep89_trial
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
BASE="$ROOT/materials/candidates/LiPON"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
OUT="$ROOT/runs/amorphous/LiPON/nep89/preparation_${JOB_ID:?}"
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
    smoke) STEPS=2000; T0=300; T1=300 ;;
    heating) STEPS=10000; T0=300; T1=2000 ;;
    melt) STEPS=20000; T0=2000; T1=2000 ;;
    quench) STEPS=14000; T0=2000; T1=250 ;;
    relaxation) STEPS=40000; T0=250; T1=250 ;;
  esac
  {
    printf 'potential %s\ntime_step 0.5\n' "$MODEL"
    if [[ "$STAGE" == smoke ]]; then
      printf 'minimize fire 0.01 10000\nvelocity 300 seed 20260914\n'
    fi
    printf 'ensemble nvt_mttk temp %s %s tperiod 200\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$T0" "$T1" "$STEPS"
  } > "$STAGE/run.in"
  (cd "$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
  test -s "$STAGE/restart.xyz"
  if [[ "$STAGE" == smoke ]]; then
    awk '/f_max =/ {f=$(NF-1); found=1} END {if(!found || f>=0.01) exit 1}' "$STAGE/stdout.txt"
  fi
  awk -v expected="$((STEPS / 100))" 'NF<18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0 || $1>6000) bad=1} END {if(bad || NR!=expected) exit 1}' "$STAGE/thermo.out"
  printf '%s completed\n' "$STAGE" >> stages_completed.txt
  PREVIOUS="$OUT/$STAGE/restart.xyz"
done
cp relaxation/restart.xyz prepared_candidate.xyz
printf 'Preparation completed; physical validation required before production.\n' > preparation_status.txt
