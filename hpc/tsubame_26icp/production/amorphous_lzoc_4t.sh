#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=6:00:00
#$ -N lzoc_mace_4T
#$ -t 1-4
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
TEMPERATURES=(600 700 800 900)
TASK=${SGE_TASK_ID:?}
[[ "$TASK" =~ ^[1-4]$ ]] || exit 2
TEMP=${TEMPERATURES[$((TASK-1))]}
SEED=$((20260911 + TASK * 100))
SOURCE="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/equilibrate_8634186/equilibrated_300K.data"
MODEL="$MODELS_ROOT/mace/mace-mpa-0-medium.model-mliap_lammps.pt"
test -s "$SOURCE"
test -s "$MODEL"
EXPECTED=7450a1a366025fa4094eba6ce414698b2bcc67a6c86cc53c6c9dd2046ce4c584
[[ "$(sha256sum "$SOURCE" | awk '{print $1}')" == "$EXPECTED" ]] || exit 3
PARENT="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/production_4T_${JOB_ID:?}"
mkdir -p "$PARENT"
OUT="$PARENT/${TEMP}K_R1"
mkdir "$OUT"
cd "$OUT"
mkdir heating equilibration production
cp "$SOURCE" input.data
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_4t.lmp" in.lmp
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_4t.sh" submitted_job.sh
printf 'source=%s\nmodel=%s\njob=%s\ntask=%s\ntemperature_K=%s\nseed=%s\nprotocol=10ps_NVT_ramp_50ps_NPT_200ps_NVT\nproduction_cell=terminal_NPT_cell\nstatus=exploratory_not_prevalidated\n' "$SOURCE" "$MODEL" "$JOB_ID" "$TASK" "$TEMP" "$SEED" > provenance.txt
sha256sum input.data in.lmp submitted_job.sh "$MODEL" > input_sha256.txt
"$MACE_LMP_MLIAP" -k on g 1 -sf kk -pk kokkos newton on neigh half -var model "$MODEL" -var temperature "$TEMP" -var seed "$SEED" -in in.lmp -log setup.log > stdout.txt 2> stderr.txt
test -s production/final.data
test -s production/final.restart
