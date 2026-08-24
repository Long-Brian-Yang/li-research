#!/usr/bin/env python3
"""Convert an ordered LAMMPS data structure into a periodic extended-XYZ file."""

from __future__ import annotations

import argparse
from pathlib import Path

from ase.io import read, write
from ase.data import atomic_numbers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="LAMMPS atomic data file")
    parser.add_argument("output", type=Path, help="periodic extended-XYZ output")
    parser.add_argument(
        "--specorder", nargs="+", required=True,
        help="atom-type order in the LAMMPS data file, e.g. Li Y Cl",
    )
    args = parser.parse_args()
    z_of_type = {index: atomic_numbers[symbol] for index, symbol in enumerate(args.specorder, start=1)}
    atoms = read(args.source, format="lammps-data", style="atomic", Z_of_type=z_of_type)
    if not all(atoms.pbc):
        raise ValueError("source structure is not periodic")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    write(args.output, atoms, format="extxyz")
    print(f"wrote {len(atoms)} atoms: {args.output}")


if __name__ == "__main__":
    main()
