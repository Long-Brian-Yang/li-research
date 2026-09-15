#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N lszc272_release
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
INPUT="$ROOT/runs/amorphous/LSZC/nep89/seed272_npt_8671205/restart.xyz"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
printf '%s  %s\n' 88ad0a3173ee5fc1a597603a025036741809aa137d259cb9726c9a68bbc04b4d "$INPUT" | sha256sum -c -
test "$(head -1 "$INPUT")" = 272
test -s "$MODEL"
module purge
module load gcc/14.2.0 cuda/12.8.0
OUT="$ROOT/runs/amorphous/LSZC/nep89/seed272_release_${JOB_ID:?}"
mkdir "$OUT"
cp "$INPUT" "$OUT/model.xyz"
cp "$0" "$OUT/submitted_job.sh"
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
{
 printf '# Ambient-pressure diagnostic, NOT author protocol or density fitting.\n'
 printf 'potential %s\ntime_step 0.5\n' "$MODEL"
 printf 'ensemble npt_mttk temp 300 300 iso 0.0001 0.0001 tperiod 200 pperiod 2000\n'
 printf 'dump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun 40000\n'
} > "$OUT/run.in"
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
test -s restart.xyz
grep -q 'Finished running GPUMD' stdout.txt
awk 'NF!=18 {bad=1} {for(i=1;i<=NF;i++) if(tolower($i)~/nan|inf/) bad=1; if($1<=0) bad=1} END {if(bad || NR!=400) exit 1}' thermo.out
printf '20 ps pressure release completed; density and disorder require analysis. No automatic heating or production.\n' > completed.txt
