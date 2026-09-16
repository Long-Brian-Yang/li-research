"""Convert the author's optimized amorphous Data 2 without changing its cell."""
from collections import Counter
from pathlib import Path
import hashlib
import json

import numpy as np
from ase.io import read, write

ROOT = Path(__file__).resolve().parents[2]


def main():
    base = ROOT / 'materials/candidates/LSZC'
    source = base / 'source/Supplementary Data 2.txt'
    a = read(source, format='cif')
    expected = {'Li': 128, 'Zr': 128, 'Cl': 512, 'S': 64, 'O': 256}
    assert dict(Counter(a.get_chemical_symbols())) == expected
    assert a.pbc.all() and np.isfinite(a.positions).all() and a.get_volume() > 0
    d = a.get_all_distances(mic=True)
    np.fill_diagonal(d, np.inf)
    assert d.min() > 1.0
    out = base / 'input'
    out.mkdir(exist_ok=True)
    a.calc = None
    write(out / 'model.xyz', a, format='extxyz')
    write(out / 'author_amorphous.cif', a, format='cif')
    info = dict(doi='10.1038/s41467-026-69737-x', source_data=2,
                counts=expected, atoms=len(a), cell_A=a.cell.array.tolist(),
                volume_A3=a.get_volume(), density_gcm3=float(a.get_masses().sum()*1.66053906660/a.get_volume()),
                minimum_distance_A=float(d.min()),
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                transformation='Format conversion only; no repeat, relaxation or atom substitution.')
    (base / 'validation.json').write_text(json.dumps(info, indent=2)+'\n')
    print(json.dumps(info, indent=2))


if __name__ == '__main__':
    main()
