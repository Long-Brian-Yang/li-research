#!/usr/bin/env bash
# One-step CUDA/ML-IAP diagnostic for MACE-MP-0b3-medium.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:05:00
#$ -N mace0b3_gpu_diag
set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
export TSUBAME_TEST_ROOT="$ROOT"
OUT="$ROOT/mace_mp0b3_gpu_diagnostic"
mkdir -p "$OUT"
module load gcc/14.2.0 openmpi/5.0.10-gcc python/3.14.3
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
export MACE_TIME=true
export LD_LIBRARY_PATH="$ROOT/lammps-mliap-gpu-install/lib64:$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$ROOT/lammps-mace/python:$ROOT/venv/lib64/python3.9/site-packages:${PYTHONPATH:-}"
"$ROOT/venv/bin/python" -c 'import torch; print("torch_cuda",torch.cuda.is_available()); print("torch_device",torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")' > "$OUT/preflight.txt"
sed 's/^run 1000/run 1/' "$ROOT/mace_mp0b3_mliap_benchmark/in.lmp" > "$OUT/in.lmp"
"$ROOT/lammps-mliap-gpu-install/bin/lmp" -k on g 1 -sf kk -pk kokkos newton on neigh half -in "$OUT/in.lmp" -log "$OUT/lammps.log" > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
