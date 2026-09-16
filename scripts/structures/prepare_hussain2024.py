"""New integer-occupancy realization of SI Table 2; not author coordinates."""
from pathlib import Path
from collections import Counter
import json
import numpy as np
from ase import Atoms
from ase.cell import Cell
from ase.spacegroup import Spacegroup
from ase.io import write
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

BASE=Path(__file__).resolve().parents[2]/'materials/candidates/LZOC_Hussain2024/seed_192'

def main():
    # Integer quotas for eight average cells; rounded occupancies resolved to exact stoichiometry.
    specs=[('Li',(0.311,0,0),16),('Li',(0.337,0,0.5),26),
           ('Cl',(0.1061,-0.1061,0.7514),40),('Cl',(0.2283,-0.2283,0.2811),26),
           ('Cl',(0.4419,-0.4419,0.7676),48),
           ('O',(0.1061,-0.1061,0.7514),4),('O',(0.2283,-0.2283,0.2811),8),
           ('Zr',(0,0,0),4),('Zr',(1/3,2/3,0.52),8),
           ('Zr',(0,0,0.5),4),('Zr',(1/3,2/3,0.9609),8)]
    cell=Cell.fromcellpar([21.874,21.874,12.044,90,90,120])
    frac=[]; symbols=[]; groups=[]
    sg=Spacegroup(164)
    for g,(sym,pos,count) in enumerate(specs):
        sites,_=sg.equivalent_sites([pos])
        for shift in np.ndindex(2,2,2):
            for p in sites:
                frac.append((p+np.array(shift))/2)
                symbols.append(sym); groups.append(g)
    pool=Atoms(symbols,scaled_positions=frac,cell=cell,pbc=True)
    d=pool.get_all_distances(mic=True)
    pairs=[]
    for i in range(len(pool)):
        for j in range(i):
            threshold=3.0 if symbols[i]==symbols[j]=='Zr' else (2.0 if {symbols[i],symbols[j]}=={'Li','Zr'} else 1.65)
            if d[i,j]<threshold: pairs.append((i,j))
    mat=lil_matrix((len(specs)+len(pairs),len(pool)))
    lo=np.zeros(mat.shape[0]); hi=np.ones(mat.shape[0])
    for g,(_,_,count) in enumerate(specs):
        mat[g,np.where(np.array(groups)==g)[0]]=1
        lo[g]=hi[g]=count
    for k,(i,j) in enumerate(pairs,len(specs)):
        mat[k,i]=mat[k,j]=1
    result=milp(np.random.default_rng(20260914).random(len(pool)),
                integrality=np.ones(len(pool)),bounds=Bounds(0,1),
                constraints=LinearConstraint(mat.tocsr(),lo,hi),options={'time_limit':60})
    if result.x is None: raise RuntimeError('No non-overlapping occupancy realization found')
    chosen=np.rint(result.x)
    assert np.all(mat@chosen>=lo-1e-8) and np.all(mat@chosen<=hi+1e-8)
    a=pool[np.where(chosen>0.5)[0]]
    dist=a.get_all_distances(mic=True); np.fill_diagonal(dist,np.inf)
    assert Counter(a.get_chemical_symbols())==dict(Li=42,Zr=24,Cl=114,O=12)
    BASE.mkdir(parents=True,exist_ok=True)
    write(BASE/'model.xyz',a,format='extxyz')
    write(BASE/'initial_structure.cif',a)
    info=dict(atoms=len(a),counts=dict(Counter(a.get_chemical_symbols())),
              minimum_distance_A=float(dist.min()),cell_A=a.cell.tolist(),
              density_gcm3=float(a.get_masses().sum()*1.6605390666/a.get_volume()),
              seed=20260914,repeat=[2,2,2],source='SI Table 2, DOI 10.1038/s41524-024-01346-y',
              method='Integer occupancy constraints and geometric exclusion; random objective, NOT energy optimization',
              author_configuration=False,validated_amorphous=False)
    (BASE/'validation.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps(info,indent=2))

if __name__=='__main__': main()
