#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N amorph_compare
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
case "${ROUTE:?}" in
 LSZC)
  INPUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_nvt_8674265/restart.xyz"
  HASH=34875ab725603aefdefbeb6f640453d825e525ae7e84cb864b8e7380d43eff55
  N=272;TAG=packed272_anneal;SPECS='ramp:300:400:200000 hold:400:400:40000'
  ;;
 LZOC)
  case "${SGE_TASK_ID:?}" in 1) T=340;;2) T=360;;3) T=380;;*) exit 2;;esac
  INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/hold300_8674222/restart.xyz"
  HASH=877262a3a6dc080a3e3af0df5586b7913256898dc5a8d0808c6a89a2ffe1b162
  N=192;TAG="transport_${T}K";SPECS="ramp:300:$T:20000 equil:$T:$T:100000 production:$T:$T:400000"
  ;;
 *) exit 2;;
esac
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = "$N"
module purge
module load gcc/14.2.0 cuda/12.8.0
MATERIAL=$ROUTE
[[ "$ROUTE" == LZOC ]] && MATERIAL=LZOC_Hussain2024
OUT="$ROOT/runs/amorphous/$MATERIAL/nep89/${TAG}_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
for SPEC in $SPECS; do
 IFS=: read -r STAGE T0 T1 STEPS <<< "$SPEC"
 DIR="$OUT/$STAGE";mkdir "$DIR";cp "$INPUT" "$DIR/model.xyz"
 {
  printf '# Literature-informed NEP comparison, not exact AIMD reproduction.\n'
  printf 'potential %s\ntime_step 0.5\n' "$MODEL"
  printf 'ensemble nvt_mttk temp %s %s tperiod 200\n' "$T0" "$T1"
  printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
 } > "$DIR/run.in"
 cd "$DIR";"$GPUMD" > stdout.txt 2> stderr.txt
 grep -q 'Finished running GPUMD' stdout.txt
 test -s restart.xyz
 awk -v expected="$((STEPS/100))" 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=expected) exit 1}' thermo.out
 INPUT="$DIR/restart.xyz"
done
printf 'Scheduled stages completed; analyse structure and transport with limitations.\n' > "$OUT/completed.txt"
