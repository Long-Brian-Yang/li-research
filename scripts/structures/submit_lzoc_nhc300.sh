#!/usr/bin/env bash
# Fresh 300 ps runs from original 80 ps inputs, not independent glass replicas.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lzoc_nhc300
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
 1) T=340; HASH=1a1e9e9f05c44a8de784a90313979d369352739dfe088e29c19403a26d36eaf2;;
 2) T=360; HASH=e8c89863a4a78443132caab5efe19f56ab3578ed92ed7035c017c57db1e39e99;;
 3) T=380; HASH=2006cc9502d9ae18133c81d8b27fd02890484b5f20f799c0f102eb14d0df5dd9;;
 *) exit 2;;
esac
PREVIOUS="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/aimd_aligned_${T}K_8675022/production"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
printf '%s  %s\n' "$HASH" "$PREVIOUS/model.xyz" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
test "$(head -1 "$PREVIOUS/model.xyz")" = 192
grep -qx 'time_step 2' "$PREVIOUS/run.in"
grep -qx "ensemble nvt_nhc $T $T 50" "$PREVIOUS/run.in"
test "$(grep -c '^run ' "$PREVIOUS/run.in")" = 1
grep -qx 'run 40000' "$PREVIOUS/run.in"
OUT="$ROOT/runs/amorphous/LZOC_Hussain2024/nep89/nhc300_${T}K_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
cp "$PREVIOUS/model.xyz" "$OUT/model.xyz"
sed 's/^run 40000$/run 150000/' "$PREVIOUS/run.in" > "$OUT/run.in"
sha256sum "$PREVIOUS/model.xyz" "$PREVIOUS/run.in" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
module purge
module load gcc/14.2.0 cuda/12.8.0
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
grep -q 'Finished running GPUMD' stdout.txt
test "$(head -1 restart.xyz)" = 192
awk 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1;if($1<=0)bad=1}END{if(bad||NR!=6000)exit 1}' thermo.out
printf 'Fresh 300 ps complete; compare nested 80/150/300 ps estimates, not independent replicas.\n' > completed.txt
