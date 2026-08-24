#!/usr/bin/env bash
# Independent SevenNet-nano relaxation and multi-temperature MD.
# Li3YCl6 model 03, 2x2x2 (240 atoms): five temperatures, three replicas each.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=24:00:00
#$ -t 1-15
#$ -tc 3
#$ -N sevennano_5T3R
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"

MODEL_NAME="sevennet_nano_55"
STRUCTURE_NAME="Li3YCl6_03_2x2x2"
TIMESTEP_PS=0.001
EQ_STEPS=50000
PROD_STEPS=500000
TEMPERATURES=(400 500 600 700 800)
if [[ -n "${TEMPERATURES_OVERRIDE:-}" ]]; then
  IFS=',' read -r -a TEMPERATURES <<< "$TEMPERATURES_OVERRIDE"
fi
TASK_ID="${SGE_TASK_ID:?SGE_TASK_ID is required}"
TASK_INDEX=$((TASK_ID - 1))
TEMPERATURE_INDEX=$((TASK_INDEX / 3))
REPLICA=$((TASK_INDEX % 3 + 1))
(( TEMPERATURE_INDEX < ${#TEMPERATURES[@]} )) || { echo "ERROR: invalid task id $TASK_ID" >&2; exit 2; }
TEMPERATURE_K="${TEMPERATURES[$TEMPERATURE_INDEX]}"
SEED=$((865200 + TEMPERATURE_INDEX * 100 + REPLICA))

LMP="$SEVENNET_LMP"
MODEL="$MODELS_ROOT/sevennet/sevennet_nano_55.pt"
INPUT="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.data"
RUN_ID="${JOB_ID:-manual}.${TASK_ID}_$(date +%Y%m%d_%H%M%S)"
OUT="$RUNS_ROOT/md/$MODEL_NAME/$STRUCTURE_NAME/${TEMPERATURE_K}K/replica_${REPLICA}/$RUN_ID"

module purge
module load gcc/14.2.0
module load openmpi/5.0.10-gcc
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
TORCH_LIB="$($SEVENNET_ENV/bin/python -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))')"
export LD_LIBRARY_PATH="$ENGINES_ROOT/lammps/sevennet/install/lib64:$TORCH_LIB:${LD_LIBRARY_PATH:-}"

[[ -x "$LMP" && -s "$MODEL" && -s "$INPUT" ]] || { echo "ERROR: missing LAMMPS, model, or input" >&2; exit 2; }
mkdir -p "$OUT"
cp "$INPUT" "$OUT/input.data"
printf 'model=%s\ninput=%s\ntemperature_K=%s\ntimestep_ps=%s\neq_steps=%s\nprod_steps=%s\nseed=%s\n' \
  "$MODEL" "$INPUT" "$TEMPERATURE_K" "$TIMESTEP_PS" "$EQ_STEPS" "$PROD_STEPS" "$SEED" > "$OUT/run_metadata.txt"
printf 'replica=%s\narray_task_id=%s\n' "$REPLICA" "$TASK_ID" >> "$OUT/run_metadata.txt"
"$SEVENNET_ENV/bin/python" -c 'import sevenn,torch; print("sevennet", getattr(sevenn, "__version__", "import-ok")); print("torch", torch.__version__, torch.version.cuda, torch.cuda.is_available())' > "$OUT/environment.txt"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader >> "$OUT/environment.txt" || true

cat > "$OUT/in.relax.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton on
atom_modify map yes
read_data $OUT/input.data
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style e3gnn
pair_coeff * * $MODEL Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
thermo 100
thermo_style custom step pe etotal press vol lx ly lz fnorm
thermo_modify flush yes
min_style sd
fix cell all box/relax iso 0.0 vmax 0.001
minimize 0.0 1.0e-3 500 3000
min_style cg
min_modify line quadratic
minimize 0.0 1.0e-6 10000 30000
unfix cell
write_data $OUT/relaxed.data
write_dump all custom $OUT/relaxed.dump id type x y z
EOF

"$LMP" -log "$OUT/relax.log" -in "$OUT/in.relax.lmp" > "$OUT/relax.stdout" 2> "$OUT/relax.stderr"
[[ -s "$OUT/relaxed.data" ]] || { echo "ERROR: relaxation did not write relaxed.data" >&2; exit 3; }

cat > "$OUT/in.md.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton on
atom_modify map yes
read_data $OUT/relaxed.data
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style e3gnn
pair_coeff * * $MODEL Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep $TIMESTEP_PS
thermo 1000
thermo_style custom step temp pe ke etotal press vol lx ly lz
thermo_modify flush yes
velocity all create $TEMPERATURE_K $SEED mom yes rot no dist gaussian
fix nvt all nvt temp $TEMPERATURE_K $TEMPERATURE_K 0.1
run $EQ_STEPS
reset_timestep 0
group li type 1
compute msd_li li msd com no
fix msd_out li ave/time 1000 1 1000 c_msd_li[1] c_msd_li[2] c_msd_li[3] c_msd_li[4] file $OUT/msd_li.dat
dump traj all custom 1000 $OUT/trajectory.lammpstrj id type xu yu zu ix iy iz
run $PROD_STEPS
unfix msd_out
undump traj
write_data $OUT/final.data
EOF

"$LMP" -log "$OUT/md.log" -in "$OUT/in.md.lmp" > "$OUT/md.stdout" 2> "$OUT/md.stderr"
grep -q 'Performance:' "$OUT/md.log"
[[ -s "$OUT/msd_li.dat" && -s "$OUT/trajectory.lammpstrj" && -s "$OUT/final.data" ]] || { echo "ERROR: incomplete MD outputs" >&2; exit 4; }
grep -E 'Loop time|Performance:|Total wall' "$OUT/md.log" > "$OUT/performance.txt"
echo "COMPLETE: $OUT"
