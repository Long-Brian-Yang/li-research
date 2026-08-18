"""Relax an explicit-occupancy CIF with MACE-MPA-0.

This intentionally refuses CIFs with partial occupancies because they must be
converted to explicit ordered models before a deterministic atomistic run.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from ase.constraints import UnitCellFilter
from ase.io import read, write
from ase.optimize import FIRE
from mace.calculators import mace_mp


def assert_explicit_occupancy(path: Path) -> None:
    for line in path.read_text().splitlines():
        if re.match(r"^\s*[A-Za-z][A-Za-z0-9_]*\s+(?:Li|Y|Nb|Cl|O)\s+", line):
            fields = line.split()
            if len(fields) >= 3:
                occupancy = float(fields[2])
                if occupancy < 0.999999:
                    raise ValueError(
                        f"{path} contains partial occupancy {occupancy}; "
                        "create an explicit ordered model first."
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_cif", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fmax", type=float, default=0.03)
    parser.add_argument("--steps", type=int, default=1000)
    parser.add_argument("--device", default="cpu")
    args = parser.parse_args()

    assert_explicit_occupancy(args.input_cif)
    atoms = read(args.input_cif)
    atoms.calc = mace_mp(model="medium-mpa-0", device=args.device)
    relaxed = UnitCellFilter(atoms)
    FIRE(relaxed, logfile="-").run(fmax=args.fmax, steps=args.steps)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write(args.output, atoms)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()

