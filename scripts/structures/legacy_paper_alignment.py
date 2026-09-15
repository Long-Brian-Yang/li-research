"""Postprocess archived high-T LZOC; these are model controls, not new MD."""
import json,hashlib
from pathlib import Path
import numpy as np
from ase import Atoms
from ase.io import read
from analyze_lzoc_production import read_dump,read_gpumd,unwrap,window_msd,fit_msd
from finish_amorphous_analysis import frame_metrics
from paper_aligned_analysis import save,OUT,ROOT

def run():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42})
 rows=[];hashes={};structure={};pairs=[('Li','Cl',3.2),('Li','O',2.7),('Zr','Cl',3.2),('Zr','O',2.6)]
 edges=np.arange(0,5.0001,.05);r=(edges[1:]+edges[:-1])/2
 fm,am=plt.subplots(1,3,layout='constrained');ff,af=plt.subplots(1,3,layout='constrained');fr,ar=plt.subplots(3,4,layout='constrained')
 for j,T in enumerate([700,800,900]):
  for model,color,ls in [('MACE','#31688e','-'),('NEP89','#d73027','--')]:
   base=ROOT/'results/LZOC'
   if model=='MACE':
    p=base/f'analysis_20260912/source/mace/{T}K_R1/production/trajectory.lammpstrj';t,x,c,s=read_dump(p)
   else:
    p=base/f'legacy_comparison_20260915/source_{T}K/production/dump.xyz';t,x,c,s=read_gpumd(p)
    a=read(p.parent/'model.xyz');x=np.concatenate([a.positions[None],x]);t=np.r_[0,t];x=unwrap(x,c[0])
   assert len(t)==2001 and np.allclose(np.diff(t),.1) and np.allclose(c,c[0]) and np.isfinite(x).all()
   a=Atoms(s,positions=x[0],cell=c[0],pbc=True)
   xc=x-np.average(x,axis=1,weights=a.get_masses())[:,None,:]
   els=['Li','Zr','O','Cl'];y={e:window_msd(xc[:,s==e]) for e in els};fit=fit_msd(t,y['Li'],20,80)
   np.savetxt(OUT/f'legacy_{model}_{T}K_MSD.csv',np.c_[t,*[y[e] for e in els]],delimiter=',',header='lag_ps,'+','.join(e+'_A2' for e in els),comments='')
   am[j].plot(t[:1001],y['Li'][:1001],color=color,ls=ls,label=model)
   for e in ['Zr','O','Cl']:af[j].plot(t[:1001],y[e][:1001],ls=ls,label=f'{model}: {e}')
   gs=[];cs=[]
   for k in range(1500,2001,25):
    aa=Atoms(s,positions=x[k],cell=c[0],pbc=True);g,cn,_=frame_metrics(aa,pairs,edges);gs.append(g);cs.append(cn)
   gm=np.mean(gs,0);cm=np.mean(cs,0)
   np.savetxt(OUT/f'legacy_{model}_{T}K_RDF.csv',np.c_[r,gm.T],delimiter=',',header='r_A,'+','.join(u+'_'+v for u,v,_ in pairs),comments='')
   for k,(u,v,_) in enumerate(pairs):ar[j,k].plot(r,gm[k],color=color,ls=ls,label=model);ar[j,k].set(title=f'{T} K: {u}–{v}',xlabel='r (Å)',ylabel='g(r)');ar[j,k].legend()
   rows.append([model,T,fit['D_cm2_s'],fit['R2'],fit['alpha'],*cm,*[y[e][800] for e in els]])
   structure[f'{model}_{T}K']={'CN':cm.tolist(),'fit':fit}
   hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
  for ax,title in [(am[j],'Li MSD'),(af[j],'Framework MSD')]:ax.set(title=f'{T} K: {title}',xlabel='Lag time (ps)',ylabel='MSD (Å²)');ax.legend()
 for f,name in [(fm,'legacy_highT_Li_MSD'),(ff,'legacy_highT_framework'),(fr,'legacy_highT_RDF')]:save(f,name)
 import csv
 with (OUT/'legacy_highT_summary.csv').open('w') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['model','T_K','D_20to80_cm2_s','R2','alpha','CN_LiCl','CN_LiO','CN_ZrCl','CN_ZrO','Li_MSD80_A2','Zr_MSD80_A2','O_MSD80_A2','Cl_MSD80_A2']);w.writerows(rows)
 (OUT/'legacy_highT_provenance.json').write_text(json.dumps({'hashes':hashes,'source':'archived 200 ps production; not NPT extension','structure':structure},indent=2)+'\n')
 print(rows,flush=True)

if __name__=='__main__':run()
