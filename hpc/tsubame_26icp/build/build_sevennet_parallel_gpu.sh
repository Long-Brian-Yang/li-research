#!/usr/bin/env bash
# Build the SevenNet patched LAMMPS e3gnn/parallel backend on TSUBAME.
# SevenNet parallel currently uses e3gnn/parallel, not ML-IAP.
#$ -cwd
#$ -V
# Compilation only needs one GPU; the resulting executable can run on node_f.
#$ -l gpu_1=1
#$ -l h_rt=2:00:00
#$ -N build_sevennet_gpu
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
SRC="$ENGINES_ROOT/lammps/sevennet/source"
BUILD="$ENGINES_ROOT/lammps/sevennet/build_cuda128_ompi507"
INSTALL="$ENGINES_ROOT/lammps/sevennet/install"
PY="$SEVENNET_ENV/bin/python"

module purge
module load gcc/14.2.0
module load cuda/12.8.0
module load openmpi/5.0.7-gcc
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# The relocated environment's interpreter supplies SevenNet and Torch; do not
# inject a pre-migration Python 3.9 site-packages path.

# The migrated virtual environment contains entry-point wrappers whose old
# shebang still points to the pre-migration path.  Invoke SevenNet through the
# active interpreter and repair the wrappers for subsequent interactive use.
for cli in sevenn sevenn_patch_lammps sevenn_get_model sevenn_graph_build sevenn_inference; do
  if [[ -f "$SEVENNET_ENV/bin/$cli" ]]; then
    sed -i "1s|^#!.*|#!$PY|" "$SEVENNET_ENV/bin/$cli"
  fi
done

if [[ ! -d "$SRC/.git" ]]; then
  mkdir -p "$(dirname "$SRC")"
  git clone --branch stable_2Aug2023_update3 --depth=1 https://github.com/lammps/lammps.git "$SRC"
fi
if [[ ! -f "$SRC/src/pair_e3gnn_parallel.cpp" ]]; then
  "$PY" -m sevenn.main.sevenn patch_lammps "$SRC"
fi

TORCH_PREFIX="$($PY -c 'import torch; print(torch.utils.cmake_prefix_path)')"
TORCH_LIB="$($PY -c 'import os,torch; print(os.path.join(os.path.dirname(torch.__file__), "lib"))')"
MPI_CXX="$(command -v mpicxx)"
cmake -S "$SRC/cmake" -B "$BUILD" \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX="$INSTALL" \
  -D BUILD_MPI=ON \
  -D BUILD_SHARED_LIBS=ON \
  -D CMAKE_PREFIX_PATH="$TORCH_PREFIX" \
  -D CMAKE_CUDA_COMPILER="$CUDA_PATH/bin/nvcc" \
  -D CMAKE_CXX_COMPILER="$MPI_CXX" \
  -D MKL_INCLUDE_DIR=/tmp \
  -D Python_EXECUTABLE="$PY" \
  -D CMAKE_BUILD_RPATH="$TORCH_LIB" \
  -D CMAKE_INSTALL_RPATH="$TORCH_LIB"
cmake --build "$BUILD" --parallel 16
cmake --install "$BUILD"
[[ -x "$INSTALL/bin/lmp" ]]

echo "SevenNet Python: $($PY -c 'import sevenn,torch; print(sevenn.__version__ if hasattr(sevenn,"__version__") else "import-ok", torch.__version__)')"
echo "CUDA-aware MPI:"
ompi_info --parsable --all | grep 'mpi_built_with_cuda_support:value' || true
echo "SevenNet patched LAMMPS build completed: $INSTALL/bin/lmp"
