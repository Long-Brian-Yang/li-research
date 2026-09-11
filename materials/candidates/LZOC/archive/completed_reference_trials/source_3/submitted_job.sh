#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=1:30:00
#$ -N lzoc_reference
#$ -t 1-2
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
case "${SGE_TASK_ID:?}" in
  1) SOURCE="$ROOT/materials/candidates/LZOC/kim2025_derived_seed" ;;
  2) SOURCE="$ROOT/materials/candidates/LZOC/kim2025_data19_seed" ;;
  3) SOURCE="$ROOT/materials/candidates/LZOC/kim2025_data18_seed" ;;
  *) exit 2 ;;
esac
PARENT="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/reference_${JOB_ID:?}"
mkdir -p "$PARENT"
OUT="$PARENT/source_${SGE_TASK_ID:?}"
MODEL="$MODELS_ROOT/mace/mace-mpa-0-medium.model-mliap_lammps.pt"
test -s "$SOURCE/target_unrelaxed.data"
test -s "$MODEL"
mkdir "$OUT"
cd "$OUT"
cp "$SOURCE/target_unrelaxed.data" input.data
cp "$SOURCE/comparison.json" initial_structure_metadata.json
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_reference.lmp" in.lmp
cp "$ROOT/hpc/tsubame_26icp/production/amorphous_lzoc_reference.sh" submitted_job.sh
printf 'source=%s\nmodel=%s\njob=%s\nstage=exploratory_candidate_not_validated\ninitial_density=derived_from_literature_cell_after_LiCl_removal\n' "$SOURCE" "$MODEL" "$JOB_ID" > provenance.txt
sha256sum input.data in.lmp submitted_job.sh "$MODEL" > input_sha256.txt
"$MACE_LMP_MLIAP" -k on g 1 -sf kk -pk kokkos newton on neigh half -var model "$MODEL" -in in.lmp -log candidate.log > stdout.txt 2> stderr.txt
test -s candidate_final.data
