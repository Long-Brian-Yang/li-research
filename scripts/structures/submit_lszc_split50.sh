#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N lszc_split50
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
case "${SGE_TASK_ID:?}" in
 1) T=320; MODE=nvt; INPUT="$ROOT/materials/candidates/LSZC/followup_mean_volume_320K/model.xyz"; HASH=702019f708d4cbef45e4e66578b68b3b35a226753d631059c2ee0e82a200ef13; ENS='nvt_mttk temp 320 320 tperiod 200';;
 2) T=350; MODE=npt; INPUT="$ROOT/runs/amorphous/LSZC/nep89/endpoint_npt150_350K_8676678/equil150/restart.xyz"; HASH=f8606ab9a01e884e35142619cedcbe480dc985dcf8be0bd208296847bed5b76e; ENS='npt_mttk temp 350 350 iso 0.0001 0.0001 tperiod 200 pperiod 2000';;
 *) exit 2;;
esac
MODEL="$ROOT/models/nep89/nep/nep89_20250409/nep89_20250409.txt"
GPUMD="$ROOT/engines/gpumd/source/src/gpumd"
printf '%s  %s\n' "$HASH" "$INPUT" | sha256sum -c -
printf '%s  %s\n' 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1 "$MODEL" | sha256sum -c -
OUT="$ROOT/runs/amorphous/LSZC/nep89/split50_${T}K_${MODE}_${JOB_ID:?}"
mkdir "$OUT"
cp "$0" "$OUT/submitted_job.sh"
cp "$INPUT" "$OUT/model.xyz"
test "$(head -1 "$INPUT")" = 272
sha256sum "$INPUT" "$MODEL" "$GPUMD" > "$OUT/provenance.sha256"
printf 'potential %s\ntime_step 0.5\nensemble %s\ndump_thermo 100\ndump_exyz 200 1 1 1\ndump_restart 2000\nrun 100000\n' "$MODEL" "$ENS" > "$OUT/run.in"
module purge
module load gcc/14.2.0 cuda/12.8.0
cd "$OUT"
"$GPUMD" > stdout.txt 2> stderr.txt
grep -q 'Finished running GPUMD' stdout.txt
test "$(head -1 restart.xyz)" = 272
awk 'NF!=18{bad=1}{for(i=1;i<=NF;i++)if(tolower($i)~/nan|inf/)bad=1}END{if(bad||NR!=1000)exit 1}' thermo.out
printf '50 ps complete; review before any production submission.\n' > review_required.txt
