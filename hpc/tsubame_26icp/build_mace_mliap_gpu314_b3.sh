#!/usr/bin/env bash
# Build a CUDA ML-IAP/Kokkos LAMMPS and convert MACE-MP-0b3-medium in the
# Python 3.14 environment that contains the cuEquivariance CUDA operators.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N build_mace_b3_gpu314
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
VENV="$ROOT/venv314"
SRC="$ROOT/lammps-mace"
BUILD="$SRC/build-mliap-gpu314-b3"
INSTALL="$ROOT/lammps-mliap-gpu314-b3-install"
MODEL="$ROOT/mace-mp-0b3-medium.model"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load cuda/12.8.0
module load python/3.14.3
export CUDA_VISIBLE_DEVICES=0

TORCH_PREFIX="$($VENV/bin/python -c 'import torch; print(torch.utils.cmake_prefix_path)')"
NVCC_WRAPPER="$SRC/lib/kokkos/bin/nvcc_wrapper"

if [[ ! -x "$INSTALL/bin/lmp" ]]; then
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
    -D Python_EXECUTABLE="$VENV/bin/python" \
    -D Python3_EXECUTABLE="$VENV/bin/python" \
    -D CMAKE_INSTALL_RPATH="$VENV/lib/python3.14/site-packages/torch/lib"
  cmake --build "$BUILD" --parallel 16
  cmake --install "$BUILD"
fi

CUDA_PY_LIBS="$(find "$VENV/lib/python3.14/site-packages/nvidia" -type d -name lib -printf '%p:')"
export LD_LIBRARY_PATH="$CUDA_PY_LIBS$VENV/lib/python3.14/site-packages/torch/lib:$INSTALL/lib64:${LD_LIBRARY_PATH:-}"

[[ -s "$MODEL" ]]
"$VENV/bin/python" -m mace.cli.create_lammps_model "$MODEL" --format=mliap
[[ -s "$ROOT/mace-mp-0b3-medium.model-mliap_lammps.pt" ]]
"$INSTALL/bin/lmp" -k on g 1 -echo screen -log none -in /dev/null
echo "MACE-MP-0b3 ML-IAP GPU Python3.14 build and conversion completed."
