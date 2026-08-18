#!/usr/bin/env python3
"""Repeat the previously relaxed 2x2x2 Li3YCl6 cells along c."""

from pathlib import Path
import json

import numpy as np
from ase.io import read, write


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = Path("/tmp/li_research_relaxed")
DST = ROOT / "structures" / "ordered" / "Li3YCl6" / "2x2x4"

for i in (1, 2, 3):
    source = SOURCE_DIR / f"Li3YCl6_0{i}.xyz"
    atoms = read(source, index=0, format="extxyz")
    expanded = atoms.repeat((1, 1, 2))
    symbols = expanded.get_chemical_symbols()
    counts = {element: symbols.count(element) for element in ("Li", "Y", "Cl")}
    d = expanded.get_all_distances(mic=True)
    d[d == 0] = np.inf
    model = f"model_0{i}"
    out_dir = DST / model
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"Li3YCl6_ordered_0{i}_2x2x4"
    write(out_dir / f"{stem}.cif", expanded, format="cif")
    write(out_dir / f"{stem}.data", expanded, format="lammps-data", atom_style="atomic")
    write(out_dir / f"{stem}.xyz", expanded, format="extxyz")
    validation = {
        "source_relaxed_2x2x2": str(source),
        "repeat_from_relaxed_2x2x2": [1, 1, 2],
        "supercell": [2, 2, 4],
        "atom_count": len(expanded),
        "formula_counts": counts,
        "cell_lengths_angstrom": expanded.cell.lengths().tolist(),
        "cell_angles_degrees": expanded.cell.angles().tolist(),
        "minimum_distance_angstrom": float(d.min()),
        "finite_coordinates": bool(np.isfinite(expanded.positions).all()),
        "status": "validated_repeated_relaxed_candidate; 2x2x4 relaxation still recommended",
    }
    (out_dir / f"{stem}_validation.json").write_text(json.dumps(validation, indent=2) + "\n")
    print(json.dumps({"model": model, **validation}, indent=2))
