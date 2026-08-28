#!/usr/bin/env bash
# MatGL/M3GNet native LAMMPS CPU benchmark.
# Submit after the MatGL build, preferably with -hold_jid <build-job-id>.
#$ -cwd
#$ -V
#$ -l h_rt=0:20:00
#$ -N matgl_m3gnet_cpu

set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LMP="${MATGL_LAMMPS_BIN:-$ROOT/lammps-matgl-install/bin/lmp}"
MODEL="${MATGL_MODEL:-$ROOT/m3gnet_matgl.pt}"
DATA="${MATGL_DATA:-$ROOT/Li3YCl6_ordered_03_2x2x2.data}"
OUT="$ROOT/matgl_m3gnet_cpu_benchmark"
LOG="$OUT/lammps.log"
mkdir -p "$OUT"
printf 'host=%s\ndate=%s\n' "$(hostname)" "$(date -Is)" | tee "$OUT/preflight.txt"
test -x "$LMP" || { echo "BLOCKED: missing $LMP" | tee -a "$OUT/preflight.txt"; exit 3; }
test -s "$MODEL" || { echo "BLOCKED: missing $MODEL" | tee -a "$OUT/preflight.txt"; exit 3; }
test -s "$DATA" || { echo "BLOCKED: missing $DATA" | tee -a "$OUT/preflight.txt"; exit 3; }
cat > "$OUT/in.lmp" <<EOF
clear
units metal
atom_style atomic
atom_modify map yes
boundary p p p
newton on
read_data $DATA
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style matgl
pair_coeff * * $MODEL Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep 0.001
velocity all create 400.0 84731 mom yes rot no dist gaussian
thermo 100
thermo_style custom step temp pe ke etotal press
thermo_modify flush yes
fix nvt all nvt temp 400.0 400.0 0.1
run 1000
EOF
"$LMP" -log "$LOG" -in "$OUT/in.lmp"
grep -E "Performance:|Loop time|MatGL|Total wall time" "$LOG" || true
echo "PASS: MatGL/M3GNet CPU benchmark completed"
