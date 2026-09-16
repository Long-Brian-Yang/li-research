"""Convert pinned author's first Li24P8S32 training frame; not a glass claim."""
from pathlib import Path
from collections import Counter
from itertools import product
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'materials/candidates/Li3PS4_glass'
SRC = BASE/'source'

def main():
    names = (SRC/'type_map.raw').read_text().split()
    types = [int(v) for v in (SRC/'type.raw').read_text().split()]
    symbols = [names[v] for v in types]
    assert Counter(symbols) == {'Li':24, 'P':8, 'S':32}
    with (SRC/'box.raw').open() as f:
        box = list(map(float, next(f).split()))
    with (SRC/'coord.raw').open() as f:
        xyz = list(map(float, next(f).split()))
    assert len(box)==9 and len(xyz)==192
    assert all(math.isfinite(v) for v in box+xyz)
    assert all(abs(box[i])<1e-9 for i in (1,2,3,5,6,7))
    cell = [box[i] for i in (0,4,8)]
    assert min(cell)>0
    points = [xyz[i:i+3] for i in range(0,len(xyz),3)]
    atoms=[]
    for shift in product(range(2),repeat=3):
        for sym,pos in zip(symbols,points):
            atoms.append((sym,[(pos[k]%cell[k])+shift[k]*cell[k] for k in range(3)]))
    lengths=[2*v for v in cell]
    minimum=float('inf')
    for i,(_,a) in enumerate(atoms):
        for _,b in atoms[i+1:]:
            d=[(a[k]-b[k])-round((a[k]-b[k])/lengths[k])*lengths[k] for k in range(3)]
            minimum=min(minimum,math.sqrt(sum(v*v for v in d)))
    assert minimum>1.0, f'Overlapping source input: {minimum}'
    out=BASE/'input'
    out.mkdir(exist_ok=True)
    lattice=f'{lengths[0]:.12f} 0 0 0 {lengths[1]:.12f} 0 0 0 {lengths[2]:.12f}'
    lines=['512',f'Lattice="{lattice}" Properties=species:S:1:pos:R:3 pbc="T T T"']
    lines += [s+' '+' '.join(f'{v:.12f}' for v in p) for s,p in atoms]
    (out/'model.xyz').write_text('\n'.join(lines)+'\n')
    cif=['data_Li3PS4_training_seed',*[f'_cell_length_{a} {v:.12f}' for a,v in zip('abc',lengths)],
         '_cell_angle_alpha 90','_cell_angle_beta 90','_cell_angle_gamma 90',
         "_symmetry_space_group_name_H-M 'P 1'",'loop_','_atom_site_label','_atom_site_type_symbol',
         '_atom_site_fract_x','_atom_site_fract_y','_atom_site_fract_z']
    cif += [f'{s}{i+1} {s} '+' '.join(f'{p[k]/lengths[k]:.12f}' for k in range(3)) for i,(s,p) in enumerate(atoms)]
    (out/'initial.cif').write_text('\n'.join(cif)+'\n')
    counts=dict(Counter(s for s,_ in atoms))
    mass=sum(counts[s]*v for s,v in {'Li':6.94,'P':30.973761998,'S':32.06}.items())
    record={'counts':counts,'source_frame_zero_based':0,'repeat':[2,2,2],
            'cell_A':lengths,'minimum_distance_A':minimum,
            'density_g_cm3':mass*1.66053906660/math.prod(lengths),
            'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.raw')}}
    (BASE/'validation.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record))

if __name__=='__main__':
    main()
