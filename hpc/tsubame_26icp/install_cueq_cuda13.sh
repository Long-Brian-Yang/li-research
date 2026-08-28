#!/usr/bin/env bash
set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
module load cuda/13.1.1
module load python/3.14.3
"$ROOT/venv/bin/pip" install --no-input cuequivariance-ops-torch-cu13
