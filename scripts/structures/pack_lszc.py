"""Independent rigid-cluster packing; not the author's configuration."""
from pathlib import Path
import json,hashlib
from collections import Counter
import numpy as np
from scipy.spatial.transform import Rotation
from ase import Atoms
from ase.io import read,write

def clearance(x,y,L):
 if not len(y):return float('inf')
 d=x[:,None,:]-y[None,:,:];d-=L*np.round(d/L)
 return float(np.sqrt((d*d).sum(axis=2).min()))

if __name__=='__main__':
 root=Path(__file__).resolve().parents[2];lib=root/'materials/candidates/LSZC/cluster_library_272'
 out=root/'materials/candidates/LSZC/packed_272';out.mkdir(exist_ok=True)
 seed=20260915;rng=np.random.default_rng(seed)
 units=[read(lib/f'cluster_{i}.xyz') for i in range(1,6) for _ in range(2)]
 units.sort(key=len,reverse=True)
 mass=sum(u.get_masses().sum() for u in units)+32*Atoms('Li').get_masses()[0]
 rho=1.8637638368982403 # Data1 starting density, not an experimental target.
 L=(mass*1.66053906660/rho)**(1/3)
 success=False
 for attempt in range(30):
  pos=np.empty((0,3));symbols=[];groups=[];mapping=[]
  for idx,u in enumerate(units+[Atoms('Li') for _ in range(32)]):
   centered=u.positions-u.positions.mean(axis=0);cut=1.8 if len(u)>1 else 1.7
   for trial in range(20000):
    x=centered@Rotation.random(random_state=rng).as_matrix().T+rng.uniform(0,L,3)
    if clearance(x,pos,L)>=cut:break
   else:break
   mapping.append({'start_zero_based':len(pos),'size':len(u),'attempts':trial+1})
   pos=np.vstack((pos,x%L));symbols.extend(u.get_chemical_symbols());groups.extend([idx]*len(u))
  if len(pos)==272:success=True;break
  print('Retry',attempt,'placed',len(pos),flush=True)
 if not success:raise RuntimeError('No acceptable packing; no structure exported')
 a=Atoms(symbols,positions=pos,cell=[L]*3,pbc=True)
 assert dict(Counter(symbols))=={'Li':32,'Zr':32,'Cl':128,'S':16,'O':64}
 d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf);g=np.array(groups);cross=g[:,None]!=g[None,:]
 # Ensure no cluster internally overlaps its own periodic image.
 for info,u in zip(mapping,units+[Atoms('Li') for _ in range(32)]):
  start=info['start_zero_based'];n=len(u)
  expected=u.get_all_distances();actual=a[start:start+n].get_all_distances(mic=True)
  local=expected<3.2
  if not np.allclose(expected[local],actual[local],atol=1e-6):raise RuntimeError('Local intracluster geometry changed')
  # Long intracluster pairs may have a shorter minimum image without a clash.
  if np.any((expected>3.2)&(actual<1.8)):raise RuntimeError('Intracluster periodic-image clash')
 a.set_array('cluster_id',g);write(out/'packed.xyz',a,format='extxyz');write(out/'packed.cif',a)
 report={'seed':seed,'packing_attempt':attempt,'n_atoms':272,'composition':dict(Counter(symbols)),'density_g_cm3':rho,'cubic_length_A':L,'minimum_all_A':float(d.min()),'minimum_intercluster_A':float(d[cross].min()),'placement':mapping,'cluster_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in lib.glob('cluster_*.xyz')},'status':'Packed precursor only; not relaxed or validated glass','settings_basis':'Independent geometric packing at Data1 density; cross-fragment cutoff1.8A, incomingLi1.7A, not paper parameters'}
 (out/'packing.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['placement','cluster_hashes']},indent=2))
