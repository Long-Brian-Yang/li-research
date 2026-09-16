#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:30:00
#$ -N lzoc_candidate
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
SOURCE="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/rebuild_8628860/replica_1"
OUT="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/candidate_${JOB_ID:?}"
MODEL="$MODELS_ROOT/mace/mace-mpa-0-medium.model-mliap_lammps.pt"
test -s "$SOURCE/pilot_final.data"
test -s "$MODEL"
mkdir "$OUT"
cd "$OUT"
cp "$SOURCE/pilot_final.data" input.data
cp "$SOURCE/metadata.json" initial_structure_metadata.json
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_candidate.lmp" in.lmp
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_candidate.sh" submitted_job.sh
printf 'source=%s\nmodel=%s\njob=%s\nstage=exploratory_candidate_not_validated\ninitial_density=construction_assumption\n' "$SOURCE" "$MODEL" "$JOB_ID" > provenance.txt
sha256sum input.data in.lmp submitted_job.sh "$MODEL" > input_sha256.txt
"$MACE_LMP_MLIAP" -k on g 1 -sf kk -pk kokkos newton on neigh half -var model "$MODEL" -in in.lmp -log candidate.log > stdout.txt 2> stderr.txt
test -s candidate_final.data
