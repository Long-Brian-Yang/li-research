"""Finish existing-data comparisons. Fixed windows, no trajectory modifications."""
from pathlib import Path
from collections import Counter
import json, hashlib
import numpy as np
from ase.io import read, iread
from scipy.stats import linregress
from analyze_lzoc_production import unwrap, window_msd, fit_msd
from complete_amorphous_comparisons import sigma_mscm
from finish_amorphous_analysis import frame_metrics, block_slopes

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'completed_transport'
WINDOWS=[(5,20),(10,40),(20,80),(40,100)]

def summarize_curve(t,y,n,volume,T):
    v=fit_msd(t,y,20,80)
    v['sigma_mS_cm']=sigma_mscm(v['D_cm2_s'],n,volume,T) if v['D_cm2_s']>0 else None
    return v

def arrhenius(T,values):
    T=np.asarray(T,float);values=np.asarray(values,float)
    if not np.isfinite(values).all() or np.any(values<=0):return None
    fit=linregress(1000/T,np.log(values))
    return {'Ea_eV':float(-fit.slope*1000*8.617333262145e-5),'R2':float(fit.rvalue**2),
            'slope':float(fit.slope),'intercept':float(fit.intercept),
            'value_303_15':float(np.exp(fit.intercept+fit.slope*1000/303.15))}

def run():
    OUT.mkdir(exist_ok=True)
    records=[];hashes={};fitrows=[]
    for T in (320,330,340,350):
        p=BASE/f'source/LSZC_4T/paper_{T}K_8676216'
        assert (p/'completed.txt').exists()
        a=read(p/'production/model.xyz');s=np.array(a.get_chemical_symbols())
        assert Counter(s)==Counter(Li=32,Zr=32,Cl=128,S=16,O=64)
        frames=list(iread(p/'production/dump.xyz'));assert len(frames)==3000
        np.testing.assert_allclose([f.info['Time']/1000 for f in frames],np.arange(1,3001)*.1)
        assert all(np.array_equal(s,f.get_chemical_symbols()) and np.allclose(a.cell,f.cell,atol=1e-7,rtol=0) for f in frames)
        x=np.array([a.positions]+[f.positions for f in frames]);assert np.isfinite(x).all()
        xu=unwrap(x,a.cell.array);xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
        t=np.arange(3001)*.1;els=['Li','Zr','Cl','S','O']
        msd={el:window_msd(xu[:,s==el]) for el in els}
        for lag in [10,200,800]:
            brute=np.mean(np.sum((xu[lag:,s=='Li']-xu[:-lag,s=='Li'])**2,2))
            np.testing.assert_allclose(brute,msd['Li'][lag],atol=1e-8)
        np.savetxt(OUT/f'LSZC_{T}K_MSD.csv',np.c_[t,*[msd[e] for e in els]],delimiter=',',header='lag_ps,'+','.join(e+'_A2' for e in els),comments='')
        fits=[fit_msd(t,msd['Li'],*w) for w in WINDOWS]
        for f in fits:fitrows.append([T,*[f[k] for k in ['lo_ps','hi_ps','D_cm2_s','R2','alpha']]])
        summary=summarize_curve(t,msd['Li'],32,a.get_volume(),T)
        summary.update(T_K=T,volume_A3=a.get_volume(),rho_g_cm3=a.get_masses().sum()*1.6605390666/a.get_volume(),fits=fits,
                       block_D_5to20=block_slopes(xu[:,s=='Li'],.1,6,(5,20)).tolist(),MSD80={el:float(msd[el][800]) for el in els})
        stages={}
        for stage,count in [('ramp',200),('equil',1000),('production',6000)]:
            th=np.loadtxt(p/stage/'thermo.out');assert th.shape==(count,18) and np.isfinite(th).all()
            vol=np.linalg.det(th[:,9:].reshape(-1,3,3));assert np.all(vol>0)
            rho=a.get_masses().sum()*1.6605390666/vol
            pe=th[:,2]/272;pressure=th[:,3:6].mean(1)
            stages[stage]={'T_mean':float(th[:,0].mean()),'P_mean_GPa':float(pressure.mean()),'rho_mean':float(rho.mean()),
                           'PE_last_quarter_minus_first':float(pe[-count//4:].mean()-pe[:count//4].mean())}
        summary['stages']=stages
        # Late structural samples, same CN definitions as 400 K.
        cn=[];fractions=[]
        for f in frames[2500::50]:
            _,c,_=frame_metrics(f,[('Li','O',2.7),('Zr','O',2.6),('Zr','Cl',3.2),('S','O',2.)],np.arange(0,5.001,.05))
            cn.append(c);d=f.get_all_distances(mic=True)
            fractions.append(float(((d[np.ix_(s=='S',s=='O')]<2).sum(1)==4).mean()))
        summary['late_CN_LiO_ZrO_ZrCl_SO']=np.mean(cn,0).tolist();summary['SO4_fraction']=float(np.mean(fractions))
        records.append(summary)
        for q in p.rglob('*'):
            if q.is_file():hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
        print(T,summary['D_cm2_s'],summary['sigma_mS_cm'],summary['alpha'],flush=True)
    np.savetxt(OUT/'LSZC_4T_fit_windows.csv',fitrows,delimiter=',',header='T_K,lo_ps,hi_ps,D_cm2_s,R2,alpha',comments='')
    keys=['T_K','D_cm2_s','sigma_mS_cm','R2','alpha','rho_g_cm3','volume_A3']
    np.savetxt(OUT/'LSZC_4T_summary.csv',[[r[k] for k in keys] for r in records],delimiter=',',header=','.join(keys),comments='')
    T=np.array([r['T_K'] for r in records]);D=np.array([r['D_cm2_s'] for r in records]);sigma=np.array([r['sigma_mS_cm'] or np.nan for r in records])
    res={'records':records,'D_arrhenius_diagnostic':arrhenius(T,D),'sigmaT_arrhenius_diagnostic':arrhenius(T,sigma/1000*T),
         'method':'COM-corrected all-time-origin MSD, 20–80 ps primary fixed before analysing. One glass; no replica confidence interval.',
         'source_hashes':hashes}
    ref=np.loadtxt(OUT/'Tang_Fig3g.csv',delimiter=',',skiprows=1)
    exp=np.loadtxt(OUT/'Tang_S3_experiment.csv',delimiter=',',skiprows=1)
    res['reference_MACE_sigmaT_refit']=arrhenius(ref[:4,1],np.exp(ref[:4,2]))
    res['reference_experiment_sigmaT_refit']=arrhenius(exp[:,1],np.exp(exp[:,2]))
    res['NEP_over_reference_sigma']=(sigma/ref[:4,4]).tolist()
    res['arrhenius_status']='Nonmonotonic NEP series; diagnostic regression is not a physical activation energy or validated extrapolation.'
    (OUT/'LSZC_4T_analysis.json').write_text(json.dumps(res,indent=2)+'\n')
    print('fits',res['D_arrhenius_diagnostic'],res['sigmaT_arrhenius_diagnostic'],flush=True)

def legacy():
    OUT.mkdir(exist_ok=True);records=[];hashes={}
    for p in sorted((BASE/'source/legacy_NPT').iterdir()):
        T=int(p.name.split('K')[0]);assert (p/'completed.txt').exists()
        a=read(p/'model.xyz');th=np.loadtxt(p/'thermo.out');assert th.shape==(1000,18) and np.isfinite(th).all()
        rho=a.get_masses().sum()*1.6605390666/np.linalg.det(th[:,9:].reshape(-1,3,3))
        P=th[:,3:6].mean(1);pe=th[:,2]/len(a);v0=a.get_volume();b=read(p/'restart.xyz')
        rec={'T_K':T,'rho_start':a.get_masses().sum()*1.6605390666/v0,'rho_end':b.get_masses().sum()*1.6605390666/b.get_volume(),
             'rho_first10':float(rho[:200].mean()),'rho_last10':float(rho[-200:].mean()),'volume_change_pct':(b.get_volume()/v0-1)*100,
             'T_mean':float(th[:,0].mean()),'P_mean_GPa':float(P.mean()),'P_last10_GPa':float(P[-200:].mean()),'PE_last10_minus_first10':float(pe[-200:].mean()-pe[:200].mean())}
        records.append(rec)
        np.savetxt(OUT/f'legacy_NPT_{T}K.csv',np.c_[np.arange(1,1001)*.05,th[:,0],P,pe,rho],delimiter=',',header='time_ps,T_K,P_GPa,PE_eV_atom,rho_g_cm3',comments='')
        for q in p.iterdir():
            if q.is_file():hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
    (OUT/'legacy_NPT_analysis.json').write_text(json.dumps({'records':records,'source_hashes':hashes},indent=2)+'\n')
    print('legacy',records,flush=True)

if __name__=='__main__':
    run();legacy()
