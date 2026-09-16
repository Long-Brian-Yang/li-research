#!/usr/bin/env bash
# Remote-only post-processing: raw trajectories stay on TSUBAME.
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lps_r1_analysis
set -euo pipefail

ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
SOURCE="$ROOT/runs/amorphous/Li3PS4/nep89"
OUTPUT="$ROOT/analysis/amorphous/Li3PS4_R1_8679199"
SCRIPT="$ROOT/scripts/structures/analyze_lips_r1_remote.py"

module purge
module load gcc/14.2.0 cuda/12.8.0
mkdir -p "$OUTPUT"
python3 "$SCRIPT" --root "$SOURCE" --output "$OUTPUT" > "$OUTPUT/stdout.txt" 2> "$OUTPUT/stderr.txt"
test -s "$OUTPUT/summary.json"
test -s "$OUTPUT/fit_windows.csv"
printf 'Remote Li3PS4 R1 analysis completed.\n' > "$OUTPUT/completed.txt"
