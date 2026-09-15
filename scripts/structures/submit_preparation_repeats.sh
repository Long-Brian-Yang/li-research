#!/usr/bin/env bash
# Two stochastic preparations per material from one documented precursor.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N glass_prep_repeat
set -euo pipefail
TASK=${SGE_TASK_ID:-}
if [[ ${1:-} == --plan ]]; then TASK=${2:-}; fi
case "$TASK" in
  1) MATERIAL=Li3PS4; INPUT_NAME=Li3PS4_glass; REP=1; SEED=9153101; N=512; HASH=8976c5ee5a0d89ea15e817c95afef9c4cda4c4dbd5a8980febe1e50831054e48 ;;
  2) MATERIAL=Li3PS4; INPUT_NAME=Li3PS4_glass; REP=2; SEED=9153102; N=512; HASH=8976c5ee5a0d89ea15e817c95afef9c4cda4c4dbd5a8980febe1e50831054e48 ;;
  3) MATERIAL=LiPON; INPUT_NAME=LiPON; REP=1; SEED=9154101; N=124; HASH=059d2d5793fd4bfe9dfcc77905b0c8735e3e050737abc6cde0d890d3ac3dd8e7 ;;
  4) MATERIAL=LiPON; INPUT_NAME=LiPON; REP=2; SEED=9154102; N=124; HASH=059d2d5793fd4bfe9dfcc77905b0c8735e3e050737abc6cde0d890d3ac3dd8e7 ;;
  *) echo 'Expected task 1 through 4' >&2; exit 2 ;;
esac
schedule() {
  printf '%s\n' 'smoke|2000|nvt_mttk temp 300 300 tperiod 200'
  if [[ $MATERIAL == Li3PS4 ]]; then
    printf '%s\n' \
      'heating|20000|npt_mttk temp 300 1500 iso 0.0001 0.0001 tperiod 200 pperiod 2000' \
      'melt|200000|npt_mttk temp 1500 1500 iso 0.0001 0.0001 tperiod 200 pperiod 2000' \
      'quench|960000|npt_mttk temp 1500 300 iso 0.0001 0.0001 tperiod 200 pperiod 2000' \
      'relaxation|40000|npt_mttk temp 300 300 iso 0.0001 0.0001 tperiod 200 pperiod 2000'
  else
    printf '%s\n' \
      'heating|10000|nvt_mttk temp 300 2000 tperiod 200' \
      'melt|20000|nvt_mttk temp 2000 2000 tperiod 200' \
      'quench|14000|nvt_mttk temp 2000 250 tperiod 200' \
      'relaxation|40000|nvt_mttk temp 250 250 tperiod 200' \
      'release|40000|npt_mttk temp 250 250 iso 0.0001 0.0001 tperiod 200 pperiod 2000'
  fi
}
if [[ ${1:-} == --plan ]]; then
  printf '%s R%s seed=%s timestep_fs=0.5\n' "$MATERIAL" "$REP" "$SEED"
  schedule
  exit 0
fi
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
POTENTIAL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
INPUT="$ROOT/materials/candidates/$INPUT_NAME/input/model.xyz"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$POTENTIAL" | sha256sum -c -
test -x "$GPUMD"
test "$(head -1 "$INPUT")" = "$N"
# Source has no velocities: different velocity seeds must actually take effect.
if head -2 "$INPUT" | grep -q ':vel:'; then exit 3; fi
OUT="$ROOT/runs/amorphous/$MATERIAL/nep89/prep_repeat_R${REP}_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$GPUMD" "$POTENTIAL" "$INPUT" > "$OUT/provenance.sha256"
schedule > "$OUT/schedule.txt"
printf 'seed=%s\nmaterial=%s\nreplica=%s\n' "$SEED" "$MATERIAL" "$REP" > "$OUT/settings.txt"
module purge
module load gcc/14.2.0 cuda/12.8.0
PREVIOUS="$INPUT"
while IFS='|' read -r STAGE STEPS ENSEMBLE; do
  mkdir "$OUT/$STAGE"
  cp "$PREVIOUS" "$OUT/$STAGE/model.xyz"
  {
    printf 'potential %s\ntime_step 0.5\n' "$POTENTIAL"
    if [[ $STAGE == smoke ]]; then
      printf 'minimize fire 0.01 10000\nvelocity 300 seed %s\n' "$SEED"
    fi
    printf 'ensemble %s\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$ENSEMBLE" "$STEPS"
  } > "$OUT/$STAGE/run.in"
  (cd "$OUT/$STAGE"; "$GPUMD" > stdout.txt 2> stderr.txt)
  grep -q 'Finished running GPUMD' "$OUT/$STAGE/stdout.txt"
  test "$(head -1 "$OUT/$STAGE/restart.xyz")" = "$N"
  if [[ $STAGE == smoke ]]; then
    awk '/f_max =/ {f=$(NF-1); found=1} END {if(!found || f>=0.01) exit 1}' "$OUT/$STAGE/stdout.txt"
  fi
  # Numerical checks only: not acceptance of glass chemistry or convergence.
  awk -v rows="$((STEPS/100))" 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0 || $1>6000)bad=1;if($10<=0 || $14<=0 || $18<=0)bad=1}END{if(bad || NR!=rows)exit 1}' "$OUT/$STAGE/thermo.out"
  printf '%s completed\n' "$STAGE" >> "$OUT/stages_completed.txt"
  PREVIOUS="$OUT/$STAGE/restart.xyz"
done < "$OUT/schedule.txt"
cp "$PREVIOUS" "$OUT/prepared_candidate.xyz"
printf 'Preparation finished; structural review required. No transport production submitted automatically.\n' > "$OUT/completed.txt"
