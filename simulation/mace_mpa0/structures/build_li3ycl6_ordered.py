#!/usr/bin/env python3
"""Generate occupancy-resolved Li3YCl6 ordered models and 2x2x2 supercells.

The screenshot CIF is an average P-3m1 refinement.  This script resolves it
into integer Li9Y3Cl18 cells: zero-occupancy Y sites are excluded, one of the
two reported M1-M2/M1-M3 Y orderings is selected, and Li sites are selected to
match the refined Li1/Li2 populations.  No overlap deletion is used.
"""

from __future__ import annotations

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

import numpy as np
from ase.io import read, write


def min_distance(atoms) -> float:
    d = atoms.get_all_distances(mic=True)
    return float(d[np.triu_indices(len(atoms), 1)].min())


def clear_refinement_metadata(atoms) -> None:
    atoms.info.pop("occupancy", None)
    atoms.info.pop("spacegroup", None)
    atoms.info.pop("unit_cell", None)
    atoms.arrays.pop("spacegroup_kinds", None)
    atoms.arrays["occupancy"] = np.ones(len(atoms), dtype=float)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--models", type=int, default=3)
    args = parser.parse_args()

    source = read(args.source)
    symbols = source.get_chemical_symbols()
    kinds = source.arrays["spacegroup_kinds"]
    # ASE stores the CIF site occupancies keyed by the original site kind.
    occupancies = source.info.get("occupancy", {})

    li_candidates = [i for i, s in enumerate(symbols) if s == "Li"]
    y_candidates = [
        i for i, s in enumerate(symbols)
        if s == "Y" and occupancies.get(str(int(kinds[i])), {}).get("Y", 0.0) > 0.0
    ]
    cl_candidates = [i for i, s in enumerate(symbols) if s == "Cl"]
    if (len(li_candidates), len(y_candidates), len(cl_candidates)) != (12, 6, 18):
        raise ValueError(
            "Unexpected candidate-site count; inspect the original CIF before ordering: "
            f"Li={len(li_candidates)}, Y={len(y_candidates)}, Cl={len(cl_candidates)}"
        )

    li_by_kind = {}
    for i in li_candidates:
        li_by_kind.setdefault(int(kinds[i]), []).append(i)
    y_by_kind = {}
    for i in y_candidates:
        y_by_kind.setdefault(int(kinds[i]), []).append(i)
    # The two physically motivated ordered motifs are M1-M2 and M1-M3.
    y_motifs = [(2, 3), (2, 5)]
    y_selections = []
    for motif in y_motifs:
        chosen = [i for kind in motif for i in y_by_kind[kind]]
        if len(chosen) == 3:
            y_selections.append(chosen)
    if not y_selections:
        raise ValueError("Could not identify M1-M2/M1-M3 Y ordering motifs")

    # Refined Li populations are approximately 5/6 on Li1 and 4/6 on Li2.
    li0, li1 = li_by_kind[0], li_by_kind[1]
    li_selections = list(itertools.islice(
        itertools.product(itertools.combinations(li0, 5), itertools.combinations(li1, 4)),
        max(args.models, 1),
    ))

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for model_index in range(args.models):
        ysel = y_selections[model_index % len(y_selections)]
        li_pair = li_selections[model_index % len(li_selections)]
        lsel = list(li_pair[0] + li_pair[1])
        ids = lsel + ysel + cl_candidates
        base = source[ids]
        clear_refinement_metadata(base)
        supercell = base.repeat((2, 2, 2))
        clear_refinement_metadata(supercell)
        dmin_base = min_distance(base)
        dmin_super = min_distance(supercell)
        if dmin_base < 1.5 or dmin_super < 1.5:
            raise ValueError(f"Model {model_index + 1} has an unphysical distance")

        model_dir = args.output_dir / f"model_{model_index + 1:02d}"
        model_dir.mkdir(parents=True, exist_ok=True)
        base_cif = model_dir / f"Li3YCl6_ordered_{model_index + 1:02d}.cif"
        super_cif = model_dir / f"Li3YCl6_ordered_{model_index + 1:02d}_2x2x2.cif"
        super_data = model_dir / f"Li3YCl6_ordered_{model_index + 1:02d}_2x2x2.data"
        report_path = model_dir / f"Li3YCl6_ordered_{model_index + 1:02d}_validation.json"
        write(base_cif, base, format="cif")
        write(super_cif, supercell, format="cif")
        write(super_data, supercell, format="lammps-data", atom_style="atomic", specorder=["Li", "Y", "Cl"])
        report = {
            "source": str(args.source),
            "model_index": model_index + 1,
            "ordering": "M1-M2" if ysel == y_selections[0] else "M1-M3",
            "base_formula_counts": dict(Counter(base.get_chemical_symbols())),
            "supercell": [2, 2, 2],
            "supercell_atom_count": len(supercell),
            "supercell_formula_counts": dict(Counter(supercell.get_chemical_symbols())),
            "minimum_distance_angstrom_base": dmin_base,
            "minimum_distance_angstrom_supercell": dmin_super,
            "status": "ordered_candidate; MACE/DFT relaxation required",
        }
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
