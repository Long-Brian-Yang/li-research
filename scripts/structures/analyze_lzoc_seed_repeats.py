"""All seeded repeats, common 20–80 ps fit; never select on agreement with AIMD."""
import json
import hashlib
import numpy as np
from ase.io import read, iread
from analyze_lzoc_production import unwrap, window_msd, fit_msd
from analyze_followup300 import ROOT, BASE

OUT=BASE/'seed_repeats'

def main():
    OUT.mkdir(exist_ok=True)
    rows=[];hashes={}
    for T in [340,360]:
        for rep in [1,2]:
            base=BASE/f'source/LZOC_repeats/seed300_{T}K_R{rep}_8677221'
            p=base/'production';a=read(p/'model.xyz');frames=list(iread(p/'dump.xyz'))
            assert (base/'completed.txt').exists() and len(a)==192 and len(frames)==3000
            s=np.array(a.get_chemical_symbols())
            assert all(np.array_equal(s,f.get_chemical_symbols()) and np.allclose(a.cell,f.cell) for f in frames)
            np.testing.assert_allclose([f.info['Time']/1000 for f in frames],np.arange(1,3001)*.1)
            x=unwrap(np.array([a.positions]+[f.positions for f in frames]),a.cell.array)
            assert np.isfinite(x).all()
            x-=np.average(x,axis=1,weights=a.get_masses())[:,None,:]
            t=np.arange(3001)*.1
            curves=[window_msd(x[:,s==el]) for el in ['Li','Zr','Cl','O']]
            for lag in [100,400,800]:
                direct=np.mean(np.sum((x[lag:,s=='Li']-x[:-lag,s=='Li'])**2,2))
                np.testing.assert_allclose(curves[0][lag],direct,atol=1e-8)
            np.savetxt(OUT/f'LZOC_{T}K_R{rep}_MSD.csv',np.c_[t,*curves],delimiter=',',
                       header='lag_ps,Li_A2,Zr_A2,Cl_A2,O_A2',comments='')
            fit=fit_msd(t,curves[0],20,80)
            near=[fit_msd(t,curves[0],lo,hi)['D_cm2_s'] for lo,hi in [(20,60),(30,90)]]
            th=np.loadtxt(p/'thermo.out');assert th.shape==(6000,18) and np.isfinite(th).all()
            rows.append(dict(T_K=T,repeat=rep,job=f'8677221.{rep+(0 if T==340 else 2)}',**fit,
                neighbor_change=max(abs(d/fit['D_cm2_s']-1) for d in near),
                T_mean=float(th[:,0].mean()),PE_drift_meV_atom=float((th[-1000:,2].mean()-th[:1000,2].mean())/192*1000)))
            for name in ['model.xyz','dump.xyz','thermo.out']:
                f=p/name;hashes[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
            print(rows[-1],flush=True)
    summary=[]
    for T in [340,360]:
        ds=np.array([r['D_cm2_s'] for r in rows if r['T_K']==T])
        summary.append(dict(T_K=T,n=2,D_mean=float(ds.mean()),D_sample_sd=float(ds.std(ddof=1)),
                            D_min=float(ds.min()),D_max=float(ds.max())))
    result=dict(records=rows,summary=summary,source_hashes=hashes,
        method='All-origin COM-corrected MSD; full 300 ps shown, common 20–80 ps fit. Two velocity repeats per temperature, same glass; sample SD is not a confidence interval. Original runs have different equilibration history and are not pooled. No new three-temperature Ea without matching 380 K repeats.')
    (OUT/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
