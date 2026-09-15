"""Extract finite geometric components, not uniquely defined chemical molecules."""
from pathlib import Path
import hashlib,json
from collections import Counter
import numpy as np
from ase import Atoms
from ase.io import read,write
from ase.geometry import find_mic
from scipy.sparse.csgraph import connected_components

def extract(a):
    s=np.array(a.get_chemical_symbols());n=len(a)
    raw=a.positions[None,:,:]-a.positions[:,None,:]
    v,d=find_mic(raw.reshape(-1,3),a.cell,pbc=True);v=v.reshape(n,n,3);d=d.reshape(n,n)
    adj=np.zeros((n,n),bool)
    for x,y,c in [('S','O',1.9),('Zr','O',2.6),('Zr','Cl',3.)]:
        adj|=(s[:,None]==x)&(s[None,:]==y)&(d<c);adj|=adj.T
    count,labels=connected_components(adj,directed=False);result=[]
    for k in range(count):
        ids=np.where(labels==k)[0]
        if np.all(s[ids]=='Li'):continue
        xyz={int(ids[0]):np.zeros(3)};queue=[int(ids[0])]
        for i in queue:
            for j in np.where(adj[i])[0]:
                pos=xyz[i]+v[i,j]
                if int(j) in xyz:
                    if np.linalg.norm(xyz[int(j)]-pos)>1e-6:raise ValueError('Periodic spanning component cannot be cut')
                else:xyz[int(j)]=pos;queue.append(int(j))
        cluster=Atoms(symbols=s[ids].tolist(),positions=[xyz[int(i)] for i in ids],pbc=False)
        result.append((ids,cluster))
    return result

if __name__=='__main__':
    root=Path(__file__).resolve().parents[2]
    src=root/'materials/candidates/LSZC/source/Supplementary Data 1.txt'
    out=root/'materials/candidates/LSZC/cluster_library_272';out.mkdir(exist_ok=True)
    a=read(src,format='cif');info=[]
    for i,(ids,c) in enumerate(extract(a),1):
        filename=f'cluster_{i}.xyz';write(out/filename,c,format='extxyz')
        info.append({'file':filename,'source_indices_zero_based':ids.tolist(),'composition':dict(Counter(c.get_chemical_symbols())),'copies_for_272':2})
    data={'source':str(src.relative_to(root)),'sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'cutoffs_A':{'S-O':1.9,'Zr-O':2.6,'Zr-Cl':3.0},'clusters':info,'free_Li_for_272':32,'target_composition':{'Li':32,'Zr':32,'Cl':128,'S':16,'O':64},'status':'Finite components extracted; NOT packed, minimized, or validated glass. Geometric definitions are project choices.'}
    (out/'manifest.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
