#!/usr/bin/env bash
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:03:00
#$ -N setup_mace_py314
set -euo pipefail
ROOT="/gs/fs/tgj-26ICP/uf03782/li-research-smoke"
PY=/apps/t4/rhel9/free/python/3.14.3/bin/python3
module load cuda/13.1.1
module load python/3.14.3
if [[ ! -x "$ROOT/venv314/bin/python" ]]; then
  "$PY" -m venv "$ROOT/venv314"
fi
if [[ ! -x "$ROOT/venv314/bin/pip" ]]; then
  "$ROOT/venv314/bin/python" -m ensurepip --upgrade
fi
"$ROOT/venv314/bin/python" -m pip install --upgrade pip
# Install the large PyTorch wheel first; keeping this separate makes a partial
# download resumable instead of losing the whole environment on a timeout.
# Avoid pip resolving the very large CUDA 13 dependency bundle on TSUBAME's
# three-minute trial queue.  The node already provides CUDA 13 libraries.
"$ROOT/venv314/bin/pip" install --no-input --timeout 1200 --no-deps torch
"$ROOT/venv314/bin/pip" install --no-input --timeout 1200 --no-deps mace-torch
"$ROOT/venv314/bin/python" -c 'import torch, cuequivariance_ops_torch; print(torch.__version__, torch.cuda.is_available()); print("cuEquivariance CUDA import OK")'
