#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lips_transport
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in 1) T=300;;2) T=500;;3) T=700;;4) T=900;;*) exit 2;;esac
INPUT="$ROOT/runs/amorphous/Li3PS4/nep89/preparation_8670632/relaxation/restart.xyz"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' a92cb37de5d8aaf4fd110edcb8aa85ebc6a1b9798b8588d2c1dbae08f25c45df "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = 512
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/Li3PS4/nep89/transport_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
PREVIOUS="$INPUT"
for STAGE in ramp equil production; do
 case "$STAGE" in
 ramp) STEPS=20000; ENS="npt_mttk temp 300 $T iso 0.0001 0.0001 tperiod 200 pperiod 2000";;
 equil) STEPS=100000; ENS="npt_mttk temp $T $T iso 0.0001 0.0001 tperiod 200 pperiod 2000";;
 production) STEPS=400000; ENS="nvt_mttk temp $T $T tperiod 200";;
 esac
 DIR="$OUT/$STAGE";mkdir "$DIR";cp "$PREVIOUS" "$DIR/model.xyz"
 {
 printf '# NEP transport control, not exact Chen2025 replication.\n'
 printf '# 10 ps ramp, 50 ps NPT, 200 ps NVT are declared project choices.\n'
 printf 'potential %s\ntime_step 0.5\nensemble %s\n' "$MODEL" "$ENS"
 printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
 } > "$DIR/run.in"
 (cd "$DIR"; "$GPUMD" > stdout.txt 2> stderr.txt)
 grep -q 'Finished running GPUMD' "$DIR/stdout.txt"
 test "$(head -1 "$DIR/restart.xyz")" = 512
 awk -v n="$((STEPS/100))" -v target="$T" '
 NF!=18 {bad=1}
 {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1;
 if($1<=0 || $1>5*target) bad=1; v=$10*$14*$18;
 if(v<5000 || v>22000) bad=1; sum+=$1}
 END {if(bad || NR!=n) exit 1}' "$DIR/thermo.out"
 printf '%s complete; numerical checks only\n' "$STAGE" >> "$OUT/stages_completed.txt"
 PREVIOUS="$DIR/restart.xyz"
done
printf '200 ps transport complete; structural and diffusion validation still required.\n' > "$OUT/completed.txt"
