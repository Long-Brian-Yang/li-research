#!/usr/bin/env bash
# Build native MatGL/M3GNet LAMMPS with Kokkos CUDA on TSUBAME.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=2:00:00
#$ -N build_matgl_m3gnet

set -euo pipefail
YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
SRC="$ENGINES_ROOT/lammps/matgl/develop"
BUILD="$SRC/build-matgl-gpu"
INSTALL="$ENGINES_ROOT/lammps/matgl/install"
ENV="$MATGL_ENV"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
# Use the canonical MatGL environment below; do not load a second system
# Python module because it can shadow the environment's Torch libraries.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
export TORCH_CUDA_ARCH_LIST=9.0
TORCH_PREFIX="$($ENV/bin/python -c 'import torch; print(torch.utils.cmake_prefix_path)')"
NVCC_WRAPPER="$SRC/lib/kokkos/bin/nvcc_wrapper"

test -x "$NVCC_WRAPPER"
test -f "$SRC/src/ML-MATGL/pair_matgl.cpp"
# The Kokkos variant uses a full neighbor list and manages local/ghost force
# ownership itself; LAMMPS Kokkos therefore requires newton off. Keep the
# native CPU style's newton-on guard, but disable that guard for the shared
# implementation used by pair_matgl/kk.
sed -i 's/if (force->newton_pair == 0)/if (false \&\& force->newton_pair == 0)/' "$SRC/src/ML-MATGL/pair_matgl.cpp"
# Declare the external package in LAMMPS' package list so `PKG_ML-MATGL=ON`
# also enables its runtime style registry (not only compilation of the source).
if ! grep -q '^  ML-MATGL$' "$SRC/cmake/CMakeLists.txt"; then
  sed -i '/^  ML-HDNNP$/a\  ML-MATGL' "$SRC/cmake/CMakeLists.txt"
fi
# Keep the Kokkos header focused on the Kokkos styles; the native style is
# registered below with the ML-MATGL package label.
sed -i '/#include "\.\.\/ML-MATGL\/pair_matgl\.h"/d' "$SRC/src/KOKKOS/pair_matgl_kokkos.h"
cmake -S "$SRC/cmake" -B "$BUILD" \
  -C "$SRC/cmake/presets/kokkos-packages.cmake" \
  -D CMAKE_BUILD_TYPE=Release \
  -D CMAKE_INSTALL_PREFIX="$INSTALL" \
  -D BUILD_MPI=ON \
  -D BUILD_SHARED_LIBS=ON \
  -D PKG_KOKKOS=ON \
  -D PKG_MOLECULE=ON \
  -D PKG_CLASS2=ON \
  -D PKG_MOFFF=ON \
  -D PKG_EXTRA-MOLECULE=ON \
  -D PKG_YAFF=ON \
  -D PKG_DIPOLE=ON \
  -D PKG_CG-SPICA=ON \
  -D PKG_DPD-REACT=ON \
  -D PKG_EXTRA-COMPUTE=ON \
  -D PKG_SPIN=ON \
  -D PKG_ML-IAP=ON \
  -D PKG_ML-MATGL=ON \
  -D Kokkos_ENABLE_CUDA=ON \
  -D Kokkos_ENABLE_SERIAL=ON \
  -D Kokkos_ARCH_HOPPER90=ON \
  -D CMAKE_CXX_COMPILER="$NVCC_WRAPPER" \
  -D CMAKE_CXX_FLAGS="-arch=sm_90" \
  -D CMAKE_CUDA_ARCHITECTURES=90 \
  -D ML_MATGL_DIR="$SRC/src/ML-MATGL" \
  -D ML_MATGL_KOKKOS_DIR="$SRC/src/KOKKOS" \
  -D MKL_INCLUDE_DIR=/tmp \
  -D CMAKE_PREFIX_PATH="$TORCH_PREFIX" \
  -D CMAKE_INSTALL_RPATH="$ENV/lib/python3.12/site-packages/torch/lib"
# ML-MATGL is an external package, so CMake's generated registry only sees
# its Kokkos header.  Register the native pair style explicitly under its own
# package name (the Kokkos style remains registered by packages_pair.h).
PAIR_REG="$BUILD/styles/packages_pair.h"
if ! grep -q 'ML-MATGL/pair_matgl.h' "$PAIR_REG"; then
  sed -i '/#include "KOKKOS\/pair_matgl_kokkos.h"/a\\#undef PACKAGE\n#define PACKAGE "ML-MATGL"\n#include "ML-MATGL/pair_matgl.h"\n#undef PACKAGE\n#define PACKAGE "KOKKOS"' "$PAIR_REG"
fi
cmake --build "$BUILD" --parallel 16
cmake --install "$BUILD"
"$INSTALL/bin/lmp" -h 2>&1 | grep -E 'ML-MATGL|KOKKOS' || true
test -x "$INSTALL/bin/lmp"
echo "MatGL/M3GNet LAMMPS GPU build completed: $INSTALL/bin/lmp"
