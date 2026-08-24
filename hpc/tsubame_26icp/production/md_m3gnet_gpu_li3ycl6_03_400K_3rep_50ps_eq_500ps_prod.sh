#!/usr/bin/env bash
# MatGL/M3GNet GPU: Li3YCl6 2x2x2, 400 K, three replicas.
# Each task performs cell relaxation, 50 ps equilibration and 500 ps production.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=24:00:00
#$ -t 1-3
#$ -tc 3
#$ -N m3gnet_400K_3R
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
MODEL_NAME="m3gnet_matgl_gpu"
STRUCTURE_NAME="Li3YCl6_03_2x2x2"
TEMPERATURE_K=400
TIMESTEP_PS=0.001
EQ_STEPS=50000
PROD_STEPS=500000
TASK_ID="${SGE_TASK_ID:?SGE_TASK_ID is required}"
REPLICA="$TASK_ID"
SEED=$((866200 + REPLICA))
LMP="$MATGL_LMP"
MODEL="${MATGL_MODEL:-$MODELS_ROOT/m3gnet/m3gnet_matgl_gpu_fixed.pt}"
INPUT="$STRUCTURES_ROOT/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.data"
RUN_ID="${JOB_ID:-manual}.${TASK_ID}_$(date +%Y%m%d_%H%M%S)"
OUT="$RUNS_ROOT/md/$MODEL_NAME/$STRUCTURE_NAME/${TEMPERATURE_K}K/replica_${REPLICA}/$RUN_ID"

module purge
module load gcc/14.2.0
module load cuda/13.1.1
module load intel/2025.0.0
export LD_LIBRARY_PATH="$MATGL_RUNTIME_LIBS:$MATGL_LAMMPS_BUILD_ROOT:$ENGINES_ROOT/lammps/matgl/install/lib64:$MATGL_ENV/lib/python3.12/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$MATGL_SOURCE_ROOT/src:$MATGL_ENV/lib/python3.12/site-packages:${PYTHONPATH:-}"
GCC_LIBDIR="$(dirname "$(g++ -print-file-name=libstdc++.so.6)")"
export LD_LIBRARY_PATH="$GCC_LIBDIR:$LD_LIBRARY_PATH"
[[ -x "$LMP" && -s "$MODEL" && -s "$INPUT" ]] || { echo "ERROR: missing LAMMPS, model, or input" >&2; exit 2; }
mkdir -p "$OUT"
cp "$INPUT" "$OUT/input.data"
printf 'model=%s\ninput=%s\ntemperature_K=%s\ntimestep_ps=%s\neq_steps=%s\nprod_steps=%s\nseed=%s\nreplica=%s\n' \
  "$MODEL" "$INPUT" "$TEMPERATURE_K" "$TIMESTEP_PS" "$EQ_STEPS" "$PROD_STEPS" "$SEED" "$REPLICA" > "$OUT/run_metadata.txt"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader > "$OUT/gpu.txt" || true

cat > "$OUT/in.relax.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton off
atom_modify map yes
read_data $OUT/input.data
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style matgl/kk
pair_coeff * * $MODEL Li Y Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
thermo 100
thermo_style custom step pe etotal press vol lx ly lz fnorm
thermo_modify flush yes
min_style cg/kk
fix cell all box/relax iso 0.0 vmax 0.001
minimize 0.0 1.0e-3 500 3000
minimize 0.0 1.0e-6 10000 30000
unfix cell
write_data $OUT/relaxed.data
write_dump all custom $OUT/relaxed.dump id type x y z
EOF
"$LMP" -k on g 1 -sf kk -pk kokkos newton off neigh half -log "$OUT/relax.log" -in "$OUT/in.relax.lmp" > "$OUT/relax.stdout" 2> "$OUT/relax.stderr"
[[ -s "$OUT/relaxed.data" ]] || { echo "ERROR: relaxation did not write relaxed.data" >&2; exit 3; }

cat > "$OUT/in.md.lmp" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton off
atom_modify map yes
read_data $OUT/relaxed.data
mass 1 6.94
mass 2 88.90584
mass 3 35.45
pair_style matgl/kk
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
"$LMP" -k on g 1 -sf kk -pk kokkos newton off neigh half -log "$OUT/md.log" -in "$OUT/in.md.lmp" > "$OUT/md.stdout" 2> "$OUT/md.stderr"
grep -q 'Performance:' "$OUT/md.log"
[[ -s "$OUT/msd_li.dat" && -s "$OUT/trajectory.lammpstrj" && -s "$OUT/final.data" ]] || { echo "ERROR: incomplete MD outputs" >&2; exit 4; }
grep -E 'Loop time|Performance:|Total wall' "$OUT/md.log" > "$OUT/performance.txt"
echo "COMPLETE: $OUT"
