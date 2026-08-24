#!/usr/bin/env python3
"""Build and validate Li3YCl6 2x2x4 supercells from the ordered 2x2x2 cells."""

from pathlib import Path
import json

from ase import Atoms
from ase.io import read, write


ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "structures" / "ordered" / "Li3YCl6" / "2x2x2"
DST = ROOT / "structures" / "ordered" / "Li3YCl6" / "2x2x4"


def validate(atoms: Atoms) -> dict:
    symbols = atoms.get_chemical_symbols()
    counts = {el: symbols.count(el) for el in ("Li", "Y", "Cl")}
    distances = atoms.get_all_distances(mic=True)
    distances[distances == 0] = float("inf")
    return {
        "atom_count": len(atoms),
        "formula_counts": counts,
        "cell_lengths_angstrom": atoms.cell.lengths().tolist(),
        "cell_angles_degrees": atoms.cell.angles().tolist(),
        "minimum_distance_angstrom": float(distances.min()),
        "finite_coordinates": bool(__import__("numpy").isfinite(atoms.positions).all()),
        "status": "validated_ordered_candidate",
    }


for model in ("model_01", "model_02", "model_03"):
    source = SRC / model / f"Li3YCl6_ordered_{model[-2:]}_2x2x2.cif"
    atoms = read(source)
    expanded = atoms.repeat((1, 1, 2))
    out_dir = DST / model
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"Li3YCl6_ordered_{model[-2:]}_2x2x4"
    write(out_dir / f"{stem}.cif", expanded)
    write(out_dir / f"{stem}.data", expanded, format="lammps-data", atom_style="atomic")
    (out_dir / f"{stem}_validation.json").write_text(
        json.dumps(
            {
                "source": str(source.relative_to(ROOT)),
                "repeat_from_2x2x2": [1, 1, 2],
                "supercell": [2, 2, 4],
                **validate(expanded),
            },
            indent=2,
        )
        + "\n"
    )
    print(model, validate(expanded))
