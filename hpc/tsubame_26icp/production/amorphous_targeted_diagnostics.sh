#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N amorph_diag
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
case "${SGE_TASK_ID:?}" in
 1)
 INPUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_anneal_8674277/hold/restart.xyz"
 HASH=c3c17a4d4b62d5b2decfe314946abb1668290784806e08371a85d514f3795795
 N=272; T=400; STEPS=40000
 ENSEMBLE='ensemble npt_mttk temp 400 400 iso 0.0001 0.0001 tperiod 200 pperiod 2000'
 OUT="$ROOT/runs/amorphous/LSZC/nep89/packed272_npt400_${JOB_ID:?}"
 ;;
 2)
 INPUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/transport_380K_8674278/equil/restart.xyz"
 HASH=2006cc9502d9ae18133c81d8b27fd02890484b5f20f799c0f102eb14d0df5dd9
 N=192; T=380; STEPS=160000
 ENSEMBLE='ensemble nvt_nhc 380 380 200'
 OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/nhc_dt05_380K_${JOB_ID:?}"
 ;;
 *) exit 2;;
esac
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$INPUT")" = "$N"
module purge
module load gcc/14.2.0 cuda/12.8.0
mkdir "$OUT"
cp "$INPUT" "$OUT/model.xyz"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
{
 printf '# Targeted diagnostic; not an exact literature reproduction or validated repair.\n'
 printf '# Preserve restart positions, cell and velocities. No density fitting.\n'
 printf 'potential %s\ntime_step 0.5\n%s\n' "$MODEL" "$ENSEMBLE"
 printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun %s\n' "$STEPS"
} > "$OUT/run.in"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
grep -q 'Finished running GPUMD' stdout.txt
test "$(head -1 restart.xyz)" = "$N"
awk -v expected="$((STEPS/100))" -v target="$T" '
 NF!=18 {bad=1}
 {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1;
 if($1<=0 || $1>5*target) bad=1; sum+=$1}
 END {if(bad || NR!=expected || sum/NR<0.5*target || sum/NR>1.5*target) exit 1}' thermo.out
printf 'Run finished; finite-output checks passed. Scientific analysis remains required.\n' > completed.txt
