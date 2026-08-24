#!/usr/bin/env python3
"""Build the LiNbOCl4 2x2x3 ordered-cell candidate."""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import read, write

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "structures/reference/photo_reconstructed/LiNbOCl4_photo_reconstructed.cif"
OUT = ROOT / "structures/ordered/LiNbOCl4/2x2x3"


def main() -> None:
    source = read(SOURCE)
    model = source.repeat((2, 2, 3))
    model.arrays["occupancy"] = np.ones(len(model), dtype=float)
    model.info.pop("occupancy", None)
    model.info.pop("spacegroup", None)
    model.info.pop("unit_cell", None)
    model.arrays.pop("spacegroup_kinds", None)
    counts = dict(sorted(Counter(model.get_chemical_symbols()).items()))
    distances = model.get_all_distances(mic=True)
    dmin = float(distances[np.triu_indices(len(model), 1)].min())
    if dmin < 1.0:
        raise ValueError(f"unphysical minimum distance: {dmin:.4f} Angstrom")
    OUT.mkdir(parents=True, exist_ok=True)
    stem = OUT / "LiNbOCl4_ordered_2x2x3"
    write(stem.with_suffix(".cif"), model, format="cif")
    write(stem.with_suffix(".data"), model, format="lammps-data", atom_style="atomic",
          specorder=["Li", "Nb", "O", "Cl"])
    report = {
        "source": str(SOURCE), "supercell": [2, 2, 3], "atom_count": len(model),
        "formula_counts": counts, "minimum_distance_angstrom": dmin,
        "status": "ordered_candidate; validate and relax before production MD",
        "note": "The screenshot-reconstructed conventional cell contains 28 atoms; direct 2x2x3 repeat contains 336 atoms. The 168-atom literature cell uses a different crystallographic setting.",
    }
    stem.with_suffix(".validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
