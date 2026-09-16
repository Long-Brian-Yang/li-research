"""Independent, seeded LiPON construction following Seth 2025 composition."""
from pathlib import Path
from collections import Counter
from itertools import product
import random
import json
import math
import hashlib

def main():
    base=Path(__file__).resolve().parents[2]/'materials/candidates/LiPON'
    source=base/'source/Li3PO4_CONTCAR'
    lines=source.read_text().splitlines()
    scale=float(lines[1]); assert scale>0
    box=[[float(v)*scale for v in line.split()] for line in lines[2:5]]
    assert all(abs(box[i][j])<1e-8 for i in range(3) for j in range(3) if i!=j)
    names=lines[5].split(); counts=list(map(int,lines[6].split()))
    assert dict(zip(names,counts))=={'Li':6,'P':2,'O':8}
    assert lines[7].lower().startswith('d')
    symbols=[s for s,n in zip(names,counts) for _ in range(n)]
    frac=[list(map(float,line.split()[:3])) for line in lines[8:24]]
    cell=[2*box[k][k] for k in range(3)]
    atoms=[]
    for shift in product(range(2),repeat=3):
        for s,p in zip(symbols,frac):
            atoms.append([s,[(p[k]%1+shift[k])/2 for k in range(3)]])
    rng=random.Random(20260914)
    oxygen=[i for i,(s,_) in enumerate(atoms) if s=='O']
    nitrogen=sorted(rng.sample(oxygen,5))
    removed_o=sorted(rng.sample([i for i in oxygen if i not in nitrogen],3))
    removed_li=rng.choice([i for i,(s,_) in enumerate(atoms) if s=='Li'])
    for i in nitrogen: atoms[i][0]='N'
    atoms=[a for i,a in enumerate(atoms) if i not in removed_o+[removed_li]]
    count=dict(Counter(s for s,_ in atoms))
    charge=count['Li']+5*count['P']-2*count['O']-3*count['N']
    assert charge==0 and len(atoms)==124
    minimum=min(math.sqrt(sum(((a[k]-b[k])-round(a[k]-b[k]))**2*cell[k]**2 for k in range(3))) for i,(_,a) in enumerate(atoms) for _,b in atoms[i+1:])
    assert minimum>1.0
    out=base/'input'; out.mkdir(exist_ok=True)
    lat=' '.join(str(cell[i]) if i==j else '0' for i in range(3) for j in range(3))
    xyz=['124',f'Lattice="{lat}" Properties=species:S:1:pos:R:3 pbc="T T T"']
    xyz += [s+' '+' '.join(f'{p[k]*cell[k]:.12f}' for k in range(3)) for s,p in atoms]
    (out/'model.xyz').write_text('\n'.join(xyz)+'\n')
    cif=['data_LiPON_independent_seed',*[f'_cell_length_{a} {v}' for a,v in zip('abc',cell)],'_cell_angle_alpha 90','_cell_angle_beta 90','_cell_angle_gamma 90',"_symmetry_space_group_name_H-M 'P 1'",'loop_','_atom_site_label','_atom_site_type_symbol','_atom_site_fract_x','_atom_site_fract_y','_atom_site_fract_z']
    cif += [f'{s}{i+1} {s} '+' '.join(f'{v:.12f}' for v in p) for i,(s,p) in enumerate(atoms)]
    (out/'initial.cif').write_text('\n'.join(cif)+'\n')
    mass=sum(count[s]*m for s,m in dict(Li=6.94,P=30.973761998,O=15.999,N=14.007).items())
    result=dict(counts=count,formal_charge=charge,minimum_distance_A=minimum,cell_A=cell,density_g_cm3=mass*1.66053906660/math.prod(cell),seed=20260914,nitrogen_parent_indices=nitrogen,removed_oxygen_parent_indices=removed_o,removed_lithium_parent_index=removed_li,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    (base/'validation.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
if __name__=='__main__': main()
