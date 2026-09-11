"""Build one unrelaxed, literature-derived LZOC seed; never submit MD.

Requires ASE and NumPy. Parent: Kim et al. 2025 Supplementary Data 4.
LiCl pair removal is a reproducible construction heuristic, NOT an energy search.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import numpy as np
from ase.io import read, write


def build_target(parent, seed=20260911):
    if Counter(parent.get_chemical_symbols()) != Counter(Li=15,Zr=6,Cl=33,O=3):
        raise ValueError('Expected Supplementary Data 4: Li15 Zr6 Cl33 O3')
    atoms = parent.repeat((2, 2, 1))
    symbols = np.array(atoms.get_chemical_symbols())
    distances = atoms.get_all_distances(mic=True)
    rng = np.random.default_rng(seed)
    chlorine = rng.choice(np.where(symbols == 'Cl')[0], size=18, replace=False)
    lithium = set(np.where(symbols == 'Li')[0].tolist())
    removed = []
    for cl in chlorine:
        li = min(lithium, key=lambda i: (distances[int(cl), i], i))
        lithium.remove(li)
        removed.extend([int(cl), int(li)])
    keep = [i for i in range(len(atoms)) if i not in set(removed)]
    return atoms[keep], sorted(removed)


def metrics(atoms):
    symbols = np.array(atoms.get_chemical_symbols())
    distances = atoms.get_all_distances(mic=True)
    np.fill_diagonal(distances, np.inf)
    result = dict(counts=dict(Counter(symbols.tolist())), atoms=len(atoms),
                  volume_A3=float(atoms.get_volume()),
                  density_g_cm3=float(sum(atoms.get_masses())*1.66053906660/atoms.get_volume()),
                  minimum_pair_distance_A=float(distances.min()),
                  cell_lengths_A=atoms.cell.lengths().tolist(),
                  cell_angles_deg=atoms.cell.angles().tolist())
    result['pairs'] = {}
    for a,b,cutoff in [('Zr','O',2.6),('Zr','Cl',3.0),('Li','O',2.7),('Li','Cl',3.2),('O','O',1.9)]:
        block = distances[np.ix_(symbols==a, symbols==b)]
        if block.size:
            result['pairs'][a+'-'+b] = dict(minimum_A=float(block.min()),
                nearest_neighbor_median_A=float(np.median(block.min(axis=1))),
                diagnostic_cutoff_A=cutoff, mean_neighbors_within_cutoff=float((block<cutoff).sum(axis=1).mean()))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--compare', action='append', default=[], type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    parent = read(args.parent)
    target, removed = build_target(parent)
    write(args.output/'target_unrelaxed.cif', target)
    write(args.output/'target_unrelaxed.data', target, format='lammps-data',
          atom_style='atomic', specorder=['Li','Zr','O','Cl'], masses=True)
    comparisons = {str(args.parent): metrics(parent), 'target_unrelaxed':metrics(target)}
    for path in args.compare:
        if path.suffix == '.data':
            atoms = read(path, format='lammps-data', atom_style='atomic', Z_of_type={1:3,2:40,3:8,4:17})
        else:
            atoms = read(path)
        comparisons[str(path)] = metrics(atoms)
    report = dict(doi='10.1038/s41467-025-65702-2', source_file=str(args.parent),
        source_sha256=hashlib.sha256(args.parent.read_bytes()).hexdigest(),
        license='CC BY 4.0', seed=20260911, repeat=[2,2,1],
        removed_zero_based_parent_supercell_indices=removed,
        method='Choose 18 Cl with fixed seed; remove each with its nearest still-available Li under PBC. Keep all Zr/O and unchanged cell.',
        status='unrelaxed composition-adjusted crystalline seed; NOT validated amorphous',
        coordination_warning='Fixed diagnostic cutoffs, not RDF-derived first minima; different temperatures/compositions are not equivalent.',
        comparisons=comparisons)
    (args.output/'comparison.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
