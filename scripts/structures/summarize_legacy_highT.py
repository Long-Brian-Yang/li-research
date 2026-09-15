"""Audit existing 700–900 K thermodynamics; not a diffusion analysis."""
from pathlib import Path
import csv,json,hashlib
import numpy as np
from ase.io import read

R=Path(__file__).resolve().parents[2]
OUT=R/'results/LZOC/legacy_comparison_20260915'
rows=[];hashes={}
for temp in [700,800,900]:
    for model in ['MACE','NEP89']:
        if model=='MACE':
            p=R/f'results/LZOC/analysis_20260912/MACE_{temp}K_production_thermo.csv'
            x=np.loadtxt(p,delimiter=',',skiprows=1)
            t,T,pe,P,rho=x[:,0],x[:,1],x[:,2]/192,x[:,4],x[:,6]
        else:
            p=OUT/f'source_{temp}K/production/thermo.out'
            x=np.loadtxt(p);assert x.shape==(4000,18)
            cell=x[:,9:].reshape(-1,3,3);v=np.linalg.det(cell)
            a=read(p.parent/'restart.xyz');assert len(a)==192
            t=np.arange(1,len(x)+1)*.05;T=x[:,0];pe=x[:,2]/192;P=x[:,3:6].mean(1)
            rho=a.get_masses().sum()*1.6605390666/v
        assert np.isfinite(x).all() and 199.9<=t[-1]<=200.1
        drift=float(pe[t>150].mean()-pe[t<=50].mean())
        rows.append([model,temp,len(t),float(T.mean()),float(P.mean()),float(rho.mean()),drift])
        hashes[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
with (OUT/'highT_thermo_summary.csv').open('w') as f:
    w=csv.writer(f,lineterminator='\n');w.writerow(['model','target_K','records','mean_T_K','mean_P_GPa','mean_density_g_cm3','PE_last50_minus_first50_eV_atom']);w.writerows(rows)
(OUT/'highT_source_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
for row in rows:print(row)
