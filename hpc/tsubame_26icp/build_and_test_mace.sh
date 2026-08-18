#!/usr/bin/env bash
# Build the ACEsuit legacy ML-MACE LAMMPS fork with CUDA/Kokkos and run an
# ordered-structure GPU test.
# Submit from the group-disk workspace with:
#   qsub -g tgj-26ICP build_and_test_mace.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=1:00:00
#$ -N build_mace_lammps_gpu
set -euo pipefail

ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
VENV="$ROOT/venv"
SRC="$ROOT/lammps-mace"
BUILD="$SRC/build-mace-gpu"
INSTALL="$ROOT/lammps-mace-gpu-install"
LAMMPS_BIN="$INSTALL/bin/lmp"

module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3

nvidia-smi -L
"$VENV/bin/python" - <<'PY'
import sys
import torch
if not torch.cuda.is_available():
    print("ERROR: PyTorch cannot see the allocated CUDA device", file=sys.stderr)
    raise SystemExit(3)
print(f"PyTorch {torch.__version__}; CUDA {torch.version.cuda}; device={torch.cuda.get_device_name(0)}")
PY

TORCH_PREFIX="$($VENV/bin/python -c 'import torch; print(torch.utils.cmake_prefix_path)')"
NVCC_WRAPPER="$SRC/lib/kokkos/bin/nvcc_wrapper"

if [[ ! -x "$LAMMPS_BIN" ]]; then
  cmake -S "$SRC/cmake" -B "$BUILD" \
    -D CMAKE_BUILD_TYPE=Release \
    -D CMAKE_INSTALL_PREFIX="$INSTALL" \
    -D BUILD_MPI=ON \
    -D BUILD_OMP=ON \
    -D PKG_KOKKOS=ON \
    -D PKG_ML-MACE=ON \
    -D PKG_MANYBODY=ON \
    -D Kokkos_ENABLE_CUDA=ON \
    -D Kokkos_ENABLE_SERIAL=ON \
    -D Kokkos_ARCH_HOPPER90=ON \
    -D CMAKE_CXX_COMPILER="$NVCC_WRAPPER" \
    -D CMAKE_CUDA_ARCHITECTURES=90 \
    -D CMAKE_PREFIX_PATH="$TORCH_PREFIX" \
    -D MKL_INCLUDE_DIR=/usr/include \
    -D Python_EXECUTABLE="$VENV/bin/python" \
    -D Python3_EXECUTABLE="$VENV/bin/python" \
    -D CMAKE_INSTALL_RPATH="$VENV/lib64/python3.9/site-packages/torch/lib"
  cmake --build "$BUILD" --parallel 16
  cmake --install "$BUILD"
fi

export LD_LIBRARY_PATH="$VENV/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
if [[ "${BUILD_ONLY:-0}" == "1" ]]; then
  "$LAMMPS_BIN" -k on g 1 -echo screen -log none -in /dev/null
  echo "GPU LAMMPS build smoke test passed."
  exit 0
fi

for data in Li3YCl6_ordered.data LiNbOCl4_ordered.data; do
  if [[ ! -s "$ROOT/$data" ]]; then
    echo "ERROR: missing ordered input $ROOT/$data" >&2
    echo "Refusing to run on provisional/partial-occupancy structures." >&2
    exit 2
  fi
done

for system in Li3YCl6 LiNbOCl4; do
  "$LAMMPS_BIN" -k on g 1 -var root "$ROOT" -var model "$ROOT/mace-mpa-0-medium.model-lammps.pt" \
    -in "$ROOT/in.test.$system"
done
