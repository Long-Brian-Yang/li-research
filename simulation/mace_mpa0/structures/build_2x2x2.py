#!/usr/bin/env python3
"""Build a first-pass 2x2x2 ordered model from a screenshot CIF.

This utility is intentionally conservative: it only writes a model when the
fully occupied ASE expansion has the requested nominal formula.  It never
deletes atoms to repair overlaps and never silently changes composition.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import read, write


def formula_counts(atoms) -> dict[str, int]:
    return dict(sorted(Counter(atoms.get_chemical_symbols()).items()))


def min_distance(atoms) -> float:
    distances = atoms.get_all_distances(mic=True)
    values = distances[np.triu_indices(len(atoms), 1)]
    return float(values.min())


def reduced_counts(counts: dict[str, int]) -> dict[str, int]:
    from math import gcd
    divisor = 0
    for value in counts.values():
        divisor = gcd(divisor, int(value))
    return {key: int(value) // divisor for key, value in sorted(counts.items())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--formula", required=True, help="Expected reduced formula, e.g. Li Nb O Cl4")
    parser.add_argument("--name", required=True)
    parser.add_argument("--elements", nargs="+", required=True, help="LAMMPS/CIF atom-type order")
    args = parser.parse_args()

    source = read(args.source)
    source_counts = formula_counts(source)
    expected_tokens = args.formula.replace(" ", "")
    # The caller supplies a compact expected formula such as LiNbOCl4.
    from ase.formula import Formula

    expected = reduced_counts(dict(Formula(expected_tokens).count().items()))
    source_reduced = reduced_counts(source_counts)
    expected_reduced = reduced_counts(expected)
    if source_reduced != expected_reduced:
        raise ValueError(
            f"Fully occupied source expands to {source_counts} ({source_reduced}), "
            f"not nominal {expected} ({expected_reduced}); resolve partial/disordered sites "
            "before fabricating an ordered model."
        )

    if not all(source.pbc):
        raise ValueError("Source structure is not fully periodic")

    supercell = source.repeat((2, 2, 2))
    # The generated model is explicitly ordered under the stated assumption;
    # do not carry the source refinement occupancies into the output CIF.
    supercell.arrays["occupancy"] = np.ones(len(supercell), dtype=float)
    supercell.info.pop("occupancy", None)
    supercell.info.pop("spacegroup", None)
    supercell.info.pop("unit_cell", None)
    supercell.arrays.pop("spacegroup_kinds", None)
    counts = formula_counts(supercell)
    dmin = min_distance(supercell)
    if dmin < 1.0:
        raise ValueError(f"Supercell has an unphysical minimum distance of {dmin:.4f} Å")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    cif_path = args.output_dir / f"{args.name}_ordered_2x2x2.cif"
    data_path = args.output_dir / f"{args.name}_ordered_2x2x2.data"
    report_path = args.output_dir / f"{args.name}_ordered_2x2x2.validation.json"

    # ASE writes explicit full occupancies for this ordered Atoms object.
    write(cif_path, supercell, format="cif")
    write(data_path, supercell, format="lammps-data", atom_style="atomic", specorder=args.elements)
    report = {
        "source": str(args.source),
        "model": str(cif_path),
        "ordering_assumption": "all visible screenshot-CIF sites are treated as fully occupied",
        "supercell": [2, 2, 2],
        "atom_count": len(supercell),
        "formula_counts": counts,
        "minimum_distance_angstrom": dmin,
        "nominal_formula_counts": expected_reduced,
        "atom_type_order": args.elements,
        "status": "pipeline_candidate_only; validate against original deposited CIF before production MD",
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
