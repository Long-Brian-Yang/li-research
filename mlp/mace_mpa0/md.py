"""Run exploratory NVT MD with MACE-MPA-0 on an explicit ordered model."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from ase import units
from ase.io import read
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution, Stationary
from mace.calculators import mace_mp


def assert_explicit_occupancy(path: Path) -> None:
    for line in path.read_text().splitlines():
        if re.match(r"^\s*[A-Za-z][A-Za-z0-9_]*\s+(?:Li|Y|Nb|Cl|O)\s+", line):
            fields = line.split()
            if len(fields) >= 3 and float(fields[2]) < 0.999999:
                raise ValueError(
                    f"{path} contains partial occupancy; ordered CIF required before MD."
                )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_cif", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--supercell", nargs=3, type=int, default=[2, 2, 2])
    parser.add_argument("--temperature", type=float, default=500.0)
    parser.add_argument("--steps", type=int, default=25000)
    parser.add_argument("--timestep-fs", type=float, default=1.0)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    assert_explicit_occupancy(args.input_cif)
    atoms = read(args.input_cif).repeat(tuple(args.supercell))
    atoms.calc = mace_mp(model="medium-mpa-0", device=args.device)
    MaxwellBoltzmannDistribution(atoms, temperature_K=args.temperature)
    Stationary(atoms)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    trajectory = args.output_dir / "md.traj"
    logfile = args.output_dir / "md.log"
    dyn = Langevin(
        atoms,
        timestep=args.timestep_fs * units.fs,
        temperature_K=args.temperature,
        friction=0.001 / units.fs,
        trajectory=trajectory,
        logfile=logfile,
        loginterval=100,
    )
    dyn.run(args.steps)
    print(f"Wrote {trajectory} and {logfile}")


if __name__ == "__main__":
    main()

