#!/usr/bin/env bash
# Direct ASE/MACE GPU benchmark for MACE-MP-0b3-medium.
# Fallback validation path when the legacy LAMMPS bridge is ABI-incompatible.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:15:00
#$ -N mace0b3_ase_bench
set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
export TSUBAME_TEST_ROOT="$ROOT"
OUT="$ROOT/mace_mp0b3_ase_benchmark"
mkdir -p "$OUT"
module load gcc/14.2.0 openmpi/5.0.10-gcc python/3.14.3
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD=1
cat > "$OUT/run.py" <<'PY'
import os, time
import torch
from ase import units
from ase.io import read
from ase.md.verlet import VelocityVerlet
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary, ZeroRotation
from mace.calculators import MACECalculator

root = os.environ["TSUBAME_TEST_ROOT"]
atoms = read(os.path.join(root, "Li3YCl6_ordered_03_2x2x2.data"), format="lammps-data", style="atomic")
atoms.set_pbc(True)
atoms.calc = MACECalculator(model_paths=os.path.join(root, "mace-mp-0b3-medium.model"), device="cuda", default_dtype="float64")
MaxwellBoltzmannDistribution(atoms, temperature_K=400.0)
Stationary(atoms)
ZeroRotation(atoms)
dyn = VelocityVerlet(atoms, timestep=1.0 * units.fs)
torch.cuda.synchronize()
t0 = time.perf_counter()
dyn.run(1000)
torch.cuda.synchronize()
elapsed = time.perf_counter() - t0
print(f"atoms={len(atoms)} steps=1000 elapsed_s={elapsed:.6f} steps_per_s={1000/elapsed:.6f}")
PY
"$ROOT/venv/bin/python" "$OUT/run.py" > "$OUT/stdout.txt" 2> "$OUT/stderr.txt"
