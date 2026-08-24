#!/usr/bin/env bash
# Official MACE ML-IAP/Kokkos CUDA build using the existing Python 3.10 mace_env.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N build_mace_maceenv
set -euo pipefail

YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
PY="$MACE_ENV/bin/python"
SRC="$ENGINES_ROOT/lammps/mace/source"
BUILD="$SRC/build-mliap-gpu-maceenv-canonical"
INSTALL="$ENGINES_ROOT/lammps/mace/install_mliap_gpu"

module purge
module load gcc/14.2.0
module load cuda/12.8.0
module load openmpi/5.0.7-gcc
export CUDA_VISIBLE_DEVICES=0

TORCH_PREFIX="$($PY -c 'import torch; print(torch.utils.cmake_prefix_path)')"
NVCC_WRAPPER="$SRC/lib/kokkos/bin/nvcc_wrapper"
CUDA_PY_LIBS="$(find "$MACE_ENV/lib/python3.10/site-packages/nvidia" -type d -name lib -printf '%p:')"
export LD_LIBRARY_PATH="$CUDA_PY_LIBS$MACE_ENV/lib/python3.10/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"

nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
"$PY" -c 'import torch, mace, cuequivariance_torch, cuequivariance_ops_torch, cupy; print(torch.__version__, torch.version.cuda); print(mace.__version__); print(cuequivariance_torch.__file__); print(cuequivariance_ops_torch.__file__); print(cupy.__version__)'

if [[ ! -f "$BUILD/CMakeCache.txt" ]]; then
  cmake -S "$SRC/cmake" -B "$BUILD" \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX="$INSTALL" \
    -D BUILD_MPI=ON -D BUILD_SHARED_LIBS=ON \
    -D PKG_KOKKOS=ON -D PKG_ML-IAP=ON -D PKG_ML-SNAP=ON \
    -D PKG_PYTHON=ON -D MLIAP_ENABLE_PYTHON=ON \
    -D Kokkos_ENABLE_CUDA=ON -D Kokkos_ENABLE_SERIAL=ON \
    -D Kokkos_ARCH_HOPPER90=ON \
    -D CMAKE_CXX_COMPILER="$NVCC_WRAPPER" \
    -D CMAKE_CUDA_ARCHITECTURES=90 \
    -D CMAKE_PREFIX_PATH="$TORCH_PREFIX" \
    -D Python_EXECUTABLE="$PY" \
    -D Python3_EXECUTABLE="$PY" \
    -D CMAKE_INSTALL_RPATH="$MACE_ENV/lib:$MACE_ENV/lib/python3.10/site-packages/torch/lib" \
    -D CMAKE_BUILD_RPATH="$MACE_ENV/lib:$MACE_ENV/lib/python3.10/site-packages/torch/lib"
  cmake --build "$BUILD" --parallel 16
  cmake --install "$BUILD"
fi

# Install the LAMMPS Python wheel used by the embedded ML-IAP bridge.  Without
# this package, mliap_unified_couple_kokkos cannot import ``lammps`` at runtime.
PY_BINDING="$BUILD/buildwheel/lib/python3.10/site-packages"
if [[ ! -d "$PY_BINDING/lammps" ]]; then
  cmake --build "$BUILD" --target install-python -- -j 8
fi
export PYTHONPATH="$PY_BINDING:${PYTHONPATH:-}"

# The installed executable is linked against liblammps.so.0.  Include the
# installation library directory for the smoke test and downstream jobs.
export LD_LIBRARY_PATH="$INSTALL/lib64:$INSTALL/lib:$MACE_ENV/lib:${LD_LIBRARY_PATH}"

"$PY" -m mace.cli.create_lammps_model "$MODELS_ROOT/mace/mace-mp-0b3-medium.model" --format=mliap
[[ -s "$MODELS_ROOT/mace/mace-mp-0b3-medium.model-mliap_lammps.pt" ]]
"$INSTALL/bin/lmp" -k on g 1 -echo screen -log none -in /dev/null
echo "Official MACE ML-IAP/Kokkos build completed: $INSTALL/bin/lmp"
