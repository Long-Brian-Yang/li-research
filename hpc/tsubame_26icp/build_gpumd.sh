#!/usr/bin/env bash
# Build GPUMD 5.0 and NEP executables on a TSUBAME GPU node.
# Submit from the GPUMD source directory with: qsub -g tgj-26ICP build_gpumd.sh
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N build_gpumd_nep89
set -euo pipefail

module load gcc/14.2.0
module load cuda/13.1.1
cd "${GPUMD_ROOT:?set GPUMD_ROOT to the GPUMD source directory}/src"
# TSUBAME 4 GPU nodes are NVIDIA H100 (compute capability 9.0).
sed -i 's/-arch=sm_60/-arch=sm_90/g' makefile
sed -i 's/-std=c++14/-std=c++17/g' makefile
make clean
make -j8
test -x gpumd
test -x nep
echo "GPUMD and NEP build completed: $(pwd)"
