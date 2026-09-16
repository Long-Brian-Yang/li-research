#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N lzoc_rebuild
#$ -t 1-3
#$ -tc 1
set -euo pipefail
ROOT=/gs/fs/tgj-26ICP/uf03782/yang/li-research
source "$ROOT/hpc/tsubame_26icp/config/yang_paths.sh"
module purge
module load gcc/14.2.0 cuda/12.8.0 openmpi/5.0.7-gcc
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export PYTHONHOME="$MACE_ENV"
PY="$MACE_ENV/bin/python"
TORCH_LIB="$($PY -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__),"lib"))')"
export LD_LIBRARY_PATH="$ENGINES_ROOT/lammps/mace/install_mliap_gpu/lib64:$ENGINES_ROOT/lammps/mace/install_mliap_gpu/lib:$MACE_ENV/lib:$TORCH_LIB:${LD_LIBRARY_PATH:-}"
SEED=$((20260910 + ${SGE_TASK_ID:?}))
OUT="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/rebuild_${JOB_ID}/replica_${SGE_TASK_ID}"
mkdir -p "$OUT"
cd "$OUT"
"$PY" "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_pilot.py" --seed "$SEED"
MODEL="$MODELS_ROOT/mace/mace-mpa-0-medium.model-mliap_lammps.pt"
# Generate the input using Python to preserve an explicit saved input per run.
"$PY" -c 'import pathlib,sys; pathlib.Path("in.lmp").write_text("""units metal
atom_style atomic
boundary p p p
atom_modify map yes
read_data input.data
pair_style mliap unified MODEL 0
pair_coeff * * Li Zr O Cl
neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
thermo 100
thermo_style custom step time temp pe ke etotal press vol fmax
thermo_modify flush yes
min_style cg/kk
minimize 0 0.01 10000 30000
write_data minimized.data
reset_timestep 0
timestep 0.0005
velocity all create 300 SEED mom yes rot no dist gaussian
fix heat all nvt temp 300 1500 0.1
dump traj all custom 100 pilot.lammpstrj id type element x y z xu yu zu
dump_modify traj element Li Zr O Cl sort id
run 2000
unfix heat
write_data pilot_final.data
""".replace("MODEL",sys.argv[1]).replace("SEED",sys.argv[2]))' "$MODEL" "$SEED"
"$MACE_LMP_MLIAP" -k on g 1 -sf kk -pk kokkos newton on neigh half -in in.lmp -log pilot.log > stdout.txt 2> stderr.txt
test -s pilot_final.data
