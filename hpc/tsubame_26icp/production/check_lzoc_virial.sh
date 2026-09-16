#!/usr/bin/env bash
#$ -cwd
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N lzoc_virial
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
OUT="$RUNS_ROOT/amorphous/LZOC/mace_mpa0/virial_check_${JOB_ID:?}"
mkdir "$OUT"
cd "$OUT"
cp "$ROOT/hpc/tsubame_26icp/production/check_lzoc_virial.py" diagnostic.py
cp "$ROOT/hpc/tsubame_26icp/production/check_lzoc_virial.sh" submitted_job.sh
"$PY" diagnostic.py > summary.json 2> diagnostic_stderr.txt
test -s pressure_check.csv
