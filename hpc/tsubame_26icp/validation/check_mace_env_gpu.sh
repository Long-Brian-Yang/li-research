#!/usr/bin/env bash
# GPU preflight for the existing Python 3.10 MACE environment.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:10:00
#$ -N mace_env_gpu_check
set -euo pipefail
module load cuda/12.8.0
YANG_PATHS_FILE="${YANG_PATHS_FILE:-${TSUBAME_TEST_ROOT:-/gs/fs/tgj-26ICP/uf03782/yang/li-research}/hpc/tsubame_26icp/config/yang_paths.sh}"
source "$YANG_PATHS_FILE"
PY="$MACE_ENV/bin/python"
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
"$PY" - <<'PY'
import torch, mace, cuequivariance, cuequivariance_torch, cuequivariance_ops_torch, cupy
print("torch", torch.__version__, "cuda", torch.version.cuda)
print("cuda_available", torch.cuda.is_available())
print("mace", mace.__version__)
print("cuequivariance", cuequivariance.__version__)
print("cueq_torch", cuequivariance_torch.__file__)
print("cueq_ops", cuequivariance_ops_torch.__file__)
print("cupy", cupy.__version__)
if not torch.cuda.is_available():
    raise SystemExit("CUDA is not available")
print("device", torch.cuda.get_device_name(0))
PY
