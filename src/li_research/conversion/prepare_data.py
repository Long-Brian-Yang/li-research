#!/usr/bin/env python3
"""Convert an ordered CIF into a simple LAMMPS atomic data file."""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from ase.io import read, write


def source_has_partial_occupancy(path: Path, tolerance: float) -> bool:
    """Detect disorder in the source CIF before ASE expands symmetry."""
    text = path.read_text(encoding="utf-8", errors="replace")
    if "_atom_site_occupancy" not in text:
        return False
    chemical_symbols = {
        "H", "Li", "B", "C", "N", "O", "F", "Na", "Mg", "Al", "Si",
        "P", "S", "Cl", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe",
        "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Rb",
        "Sr", "Y", "Zr", "Nb", "Mo", "Ru", "Rh", "Pd", "Ag", "Cd", "In",
        "Sn", "Sb", "Te", "I", "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Sm",
        "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Hf", "Ta",
        "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi",
    }
    for line in text.splitlines():
        fields = line.split()
        if len(fields) >= 3 and fields[1] in chemical_symbols:
            try:
                occupancy = float(re.sub(r"\([^)]*\)$", "", fields[2]))
            except ValueError:
                continue
            if occupancy < 1.0 - tolerance:
                return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cif", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--elements", nargs="+", required=True,
        help="LAMMPS atom-type order, e.g. Li Y Cl",
    )
    parser.add_argument(
        "--occupancy-tolerance", type=float, default=1e-6,
        help="Reject CIFs with any site occupancy below 1-tolerance.",
    )
    parser.add_argument(
        "--allow-partial", action="store_true",
        help="Allow a provisional conversion for format smoke tests only.",
    )
    args = parser.parse_args()

    has_partial = source_has_partial_occupancy(args.cif, args.occupancy_tolerance)
    if has_partial and not args.allow_partial:
        raise ValueError("Partial occupancy detected in source CIF; create an ordered model first.")
    if has_partial:
        print("WARNING: writing provisional data from a partial-occupancy CIF; do not use for production MD.")

    atoms = read(args.cif)
    if atoms.pbc is None or not all(atoms.pbc):
        raise ValueError("Input structure must be fully periodic.")
    if len(atoms) == 0:
        raise ValueError("Input structure contains no atoms.")

    # ASE represents a fully ordered CIF as one chemical symbol per atom.  A
    # CIF with disorder normally arrives with an occupancy array; reject it.
    occupancies = atoms.arrays.get("occupancy")
    if occupancies is not None and any(float(x) < 1.0 - args.occupancy_tolerance for x in occupancies):
        raise ValueError("Partial occupancy detected; create an ordered model first.")

    symbols = set(atoms.get_chemical_symbols())
    expected = set(args.elements)
    unknown = symbols - expected
    if unknown:
        raise ValueError(f"Elements not listed in --elements: {sorted(unknown)}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    write(args.output, atoms, format="lammps-data", atom_style="atomic", specorder=args.elements)
    print(f"Wrote {args.output} ({len(atoms)} atoms; type order: {' '.join(args.elements)})")


if __name__ == "__main__":
    main()
