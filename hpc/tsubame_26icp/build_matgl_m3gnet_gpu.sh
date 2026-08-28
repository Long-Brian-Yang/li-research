#!/usr/bin/env bash
# Build native MatGL/M3GNet LAMMPS with Kokkos CUDA on TSUBAME.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=2:00:00
#$ -N build_matgl_m3gnet

set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
SRC="$ROOT/lammps-develop"
BUILD="$SRC/build-matgl-gpu"
INSTALL="$ROOT/lammps-matgl-install"
ENV="${MATGL_PYTHON_ENV:-/gs/fs/tga-ishikawalab/yang/proton-nnp-benchmark/src/simulation/05_torch_sim_md/.conda/envs/ts312_mace}"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3 || true
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TORCH_CUDA_ARCH_LIST=9.0
TORCH_PREFIX="$($ENV/bin/python -c 'import torch; print(torch.utils.cmake_prefix_path)')"
NVCC_WRAPPER="$SRC/lib/kokkos/bin/nvcc_wrapper"

test -x "$NVCC_WRAPPER"
test -f "$SRC/src/ML-MATGL/pair_matgl.cpp"
cmake -S "$SRC/cmake" -B "$BUILD" \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX="$INSTALL" \
  -D BUILD_MPI=ON \
  -D BUILD_SHARED_LIBS=ON \
  -D PKG_KOKKOS=ON \
  -D PKG_ML-MATGL=ON \
  -D Kokkos_ENABLE_CUDA=ON \
  -D Kokkos_ENABLE_SERIAL=ON \
  -D Kokkos_ARCH_HOPPER90=ON \
  -D CMAKE_CXX_COMPILER="$NVCC_WRAPPER" \
  -D CMAKE_CXX_FLAGS="-arch=sm_90" \
  -D CMAKE_CUDA_ARCHITECTURES=90 \
  -D MKL_INCLUDE_DIR=/tmp \
  -D CMAKE_PREFIX_PATH="$TORCH_PREFIX" \
  -D CMAKE_INSTALL_RPATH="$ENV/lib/python3.12/site-packages/torch/lib"
cmake --build "$BUILD" --parallel 16
cmake --install "$BUILD"
"$INSTALL/bin/lmp" -h 2>&1 | grep -E 'ML-MATGL|KOKKOS' || true
test -x "$INSTALL/bin/lmp"
echo "MatGL/M3GNet LAMMPS GPU build completed: $INSTALL/bin/lmp"
