#!/usr/bin/env bash
# Source this file on TSUBAME; no conda/Python environment is needed for GPUMD.
module load gcc/14.2.0 cuda/12.8.0 || return 1
export GPUMD_BIN=/gs/fs/tgj-26ICP/uf03782/yang/li-research/engines/gpumd/source/src/gpumd
export NEP89_MODEL=/gs/fs/tgj-26ICP/uf03782/yang/li-research/models/nep89/nep/nep89_20250409/nep89_20250409.txt
test -x "$GPUMD_BIN" && test -r "$NEP89_MODEL" || return 1
