"""Fixed-window nested-duration analysis; raw coordinates remain unchanged."""
from pathlib import Path
import json, hashlib
import numpy as np
from ase.io import read, iread
from analyze_lzoc_production import unwrap, window_msd, fit_msd
from finish_materials_transport import arrhenius

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'followup300'

def main():
    OUT.mkdir(exist_ok=True)
    records=[]; hashes={}; checks=[]
    for T in [340,360,380]:
        p=BASE/f'source/LZOC300/nhc300_{T}K_8676684'
        assert (p/'completed.txt').exists()
        a=read(p/'model.xyz');frames=list(iread(p/'dump.xyz'))
        assert len(a)==192 and len(frames)==3000
        s=np.array(a.get_chemical_symbols())
        assert all(np.array_equal(s,f.get_chemical_symbols()) and np.allclose(a.cell,f.cell) for f in frames)
        np.testing.assert_allclose([f.info['Time']/1000 for f in frames],np.arange(1,3001)*.1)
        xu=unwrap(np.array([a.positions]+[f.positions for f in frames]),a.cell.array)
        xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
        for duration in [80,150,300]:
            n=int(duration*10)+1;t=np.arange(n)*.1
            curves=[window_msd(xu[:n,s==el]) for el in ['Li','Zr','Cl','O']]
            for lag in [100,400]:
                direct=np.mean(np.sum((xu[lag:n,s=='Li']-xu[:n-lag,s=='Li'])**2,2))
                np.testing.assert_allclose(curves[0][lag],direct,atol=1e-8)
            np.savetxt(OUT/f'LZOC_{T}K_{duration}ps_MSD.csv',np.c_[t,*curves],delimiter=',',header='lag_ps,Li_A2,Zr_A2,Cl_A2,O_A2',comments='')
            fit=fit_msd(t,curves[0],10,40)
            records.append(dict(T_K=T,duration_ps=duration,**fit))
        blocks=[]
        for start in range(0,3000,500):
            y=window_msd(xu[start:start+501,s=='Li'])
            blocks.append(fit_msd(np.arange(len(y))*.1,y,10,40)['D_cm2_s'])
        th=np.loadtxt(p/'thermo.out');assert th.shape==(6000,18) and np.isfinite(th).all()
        checks.append(dict(T_K=T,block_D_50ps=blocks,T_mean=float(th[:,0].mean()),P_mean_GPa=float(th[:,3:6].mean()),PE_last50_minus_first50_eV_atom=float((th[-1000:,2].mean()-th[:1000,2].mean())/192)))
        for name in ['model.xyz','dump.xyz','thermo.out','run.in']:
            f=p/name;hashes[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
    fits={str(d):arrhenius([340,360,380],[r['D_cm2_s'] for r in records if r['duration_ps']==d]) for d in [80,150,300]}
    npt=[]
    for T in [320,350]:
        p=BASE/f'source/LSZC150/endpoint_npt150_{T}K_8676678/equil150'
        a=read(p/'model.xyz');th=np.loadtxt(p/'thermo.out');assert th.shape==(3000,18) and np.isfinite(th).all()
        vol=np.linalg.det(th[:,9:].reshape(-1,3,3));rho=a.get_masses().sum()*1.6605390666/vol
        x=np.c_[np.arange(1,3001)*.05,th[:,0],th[:,3:6].mean(1),th[:,2]/272,rho,vol]
        np.savetxt(OUT/f'LSZC_{T}K_NPT150.csv',x,delimiter=',',header='time_ps,T_K,P_GPa,PE_eV_atom,rho_g_cm3,volume_A3',comments='')
        blocks=x.reshape(6,500,6).mean(1)
        npt.append(dict(T_K=T,blocks25ps=blocks.tolist(),last50_density_change_pct=float((blocks[-1,4]/blocks[-2,4]-1)*100),last50_PE_change_meV_atom=float((blocks[-1,3]-blocks[-2,3])*1000)))
        for name in ['model.xyz','thermo.out','run.in']:
            f=p/name;hashes[str(f.relative_to(ROOT))]=hashlib.sha256(f.read_bytes()).hexdigest()
    result=dict(records=records,arrhenius_diagnostic=fits,checks=checks,LSZC_NPT=npt,source_hashes=hashes,method='COM-corrected all-origin MSD, fixed 10–40 ps fit. Nested durations and blocks are not independent replicas.')
    (OUT/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))

def select_window():
    result=json.loads((OUT/'analysis.json').read_text())
    windows=[(10,40),(20,60),(20,80),(30,90),(40,100),(50,110),(60,120),(75,150)]
    rows=[];primary=[]
    for T in [340,360,380]:
        a=np.loadtxt(OUT/f'LZOC_{T}K_300ps_MSD.csv',delimiter=',',skiprows=1)
        fits={w:fit_msd(a[:,0],a[:,1],*w) for w in windows}
        for (lo,hi),f in fits.items():rows.append([T,lo,hi,f['D_cm2_s'],f['R2'],f['alpha']])
        f=fits[(20,80)]
        delta=max(abs(fits[w]['D_cm2_s']/f['D_cm2_s']-1) for w in [(20,60),(30,90)])
        primary.append(dict(T_K=T,**f,neighbor_relative_change_max=delta))
    result['primary_20_80']=primary
    result['primary_arrhenius']=arrhenius([340,360,380],[f['D_cm2_s'] for f in primary])
    result['selection_note']='Post-analysis common 20–80 ps window; nearby 20–60 and 30–90 slopes differ by <4%. Exploratory local stability, not a unique optimum or demonstrated long-time convergence. Ea was not the selection criterion. Original 10–40 diagnostics retained.'
    np.savetxt(OUT/'LZOC_window_sensitivity.csv',rows,delimiter=',',header='T_K,lo_ps,hi_ps,D_cm2_s,R2,alpha',comments='')
    (OUT/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')

if __name__=='__main__':
    import sys
    if '--select-only' not in sys.argv:main()
    select_window()
