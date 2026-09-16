"""Expand author's AIMD seed along its shortest axis; not a validated glass."""
from collections import Counter
from pathlib import Path
import hashlib
import json

import numpy as np
from ase.io import read, write

ROOT = Path(__file__).resolve().parents[2]


def main():
    base = ROOT / 'materials/candidates/LSZC'
    source = base / 'source/Supplementary Data 1.txt'
    parent = read(source, format='cif')
    assert len(parent) == 136
    assert int(np.argmin(parent.cell.lengths())) == 1
    a = parent.repeat((1, 2, 1))
    counts = dict(Counter(a.get_chemical_symbols()))
    assert counts == {'Li':32, 'Zr':32, 'Cl':128, 'S':16, 'O':64}
    assert np.isfinite(a.positions).all() and a.pbc.all()
    distances = a.get_all_distances(mic=True)
    np.fill_diagonal(distances, np.inf)
    assert distances.min() > 1.0
    out = base / 'seed_272'
    out.mkdir(exist_ok=True)
    write(out / 'model.xyz', a, format='extxyz')
    write(out / 'initial_structure.cif', a, format='cif')
    info = dict(atoms=len(a), counts=counts, repeat=[1,2,1],
                source_data=1, doi='10.1038/s41467-026-69737-x',
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                cell_A=a.cell.array.tolist(), volume_A3=a.get_volume(),
                density_gcm3=float(a.get_masses().sum()*1.66053906660/a.get_volume()),
                minimum_distance_A=float(distances.min()), validated_amorphous=False,
                status='Periodic replicated AIMD seed; reconstruction and validation required before transport MD.')
    (out / 'validation.json').write_text(json.dumps(info, indent=2)+'\n')
    print(json.dumps(info, indent=2))


if __name__ == '__main__':
    main()
