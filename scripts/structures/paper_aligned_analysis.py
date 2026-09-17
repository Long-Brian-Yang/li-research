"""Paper-facing LSZC transport and origin-conditioned mobility, no trajectory edits."""
from pathlib import Path
from collections import Counter
import numpy as np
import json,hashlib
from ase.io import read,iread
from analyze_lzoc_production import unwrap,window_msd,fit_msd
from finish_amorphous_analysis import frame_metrics,block_slopes
from complete_amorphous_comparisons import sigma_mscm
from li_diffusion_style import apply_style

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'paper_alignment'

def conditioned_mobility(x,cn,lag,stride):
    """Rows: origin CN, observations, mean future displacement², sample SD."""
    ids=np.arange(0,len(x)-lag,stride)
    d2=((x[ids+lag]-x[ids])**2).sum(2).ravel()
    labels=cn[ids].ravel();rows=[]
    for c in np.unique(labels):
        v=d2[labels==c]
        rows.append([c,len(v),v.mean(),v.std(ddof=1) if len(v)>1 else np.nan])
    return np.array(rows)

def save(fig,name):
    import matplotlib.pyplot as plt
    apply_style(fig)
    for ext in ['png','pdf','svg']:fig.savefig(OUT/f'{name}.{ext}',dpi=220)
    p=OUT/f'{name}.svg';p.write_text('\n'.join(v.rstrip() for v in p.read_text().splitlines())+'\n')
    plt.close(fig)

def lszc():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42})
    OUT.mkdir(parents=True,exist_ok=True)
    p=BASE/'source/LSZC_transport/transport400_8676040'
    assert (p/'completed.txt').exists()
    a=read(p/'model.xyz');s=np.array(a.get_chemical_symbols())
    assert Counter(s)==Counter(Li=32,Zr=32,Cl=128,S=16,O=64)
    frames=list(iread(p/'dump.xyz'));assert len(frames)==2000
    np.testing.assert_allclose([f.info['Time']/1000 for f in frames],np.arange(1,2001)*.1)
    assert all(np.array_equal(s,f.get_chemical_symbols()) and np.allclose(a.cell,f.cell) for f in frames)
    x=np.array([a.positions]+[f.positions for f in frames]);assert np.isfinite(x).all()
    xu=unwrap(x,a.cell.array);xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
    t=np.arange(2001)*.1;els=['Li','Zr','Cl','S','O']
    msd={el:window_msd(xu[:,s==el]) for el in els}
    for lag in [10,200,800]:
        brute=np.mean(np.sum((xu[lag:,s=='Li']-xu[:-lag,s=='Li'])**2,2))
        np.testing.assert_allclose(brute,msd['Li'][lag],atol=1e-8)
    fits=[fit_msd(t,msd['Li'],*w) for w in [(5,20),(10,40),(20,80),(40,100)]]
    blocks=block_slopes(xu[:,s=='Li'],.1,4,(5,20))
    np.savetxt(OUT/'LSZC400_MSD.csv',np.column_stack([t, *[msd[e] for e in els]]),delimiter=',',header='lag_ps,'+','.join(e+'_A2' for e in els),comments='')
    np.savetxt(OUT/'LSZC400_fit_windows.csv',[[f[k] for k in ['lo_ps','hi_ps','D_cm2_s','R2','alpha','intercept_A2']] for f in fits],delimiter=',',header='lo_ps,hi_ps,D_cm2_s,R2,alpha,intercept_A2',comments='')
    np.savetxt(OUT/'LSZC400_blocks.csv',np.c_[[25,75,125,175],blocks],delimiter=',',header='block_centre_ps,D_5to20_cm2_s',comments='')
    f,ax=plt.subplots(1,2,layout='constrained');fit=fits[2]
    ax[0].plot(t[:1001],msd['Li'][:1001],label='Li, 400 K',color='#31688e')
    tt=np.array([20,80]);ax[0].plot(tt,fit['intercept_A2']+tt*fit['D_cm2_s']*6e4,'k--',label='20–80 ps fit')
    ax[0].set(title='LSZC: lithium transport',xlabel='Lag time (ps)',ylabel='MSD (Å²)');ax[0].legend()
    for el,ls in zip(els[:],['-','--',':','-.','--']):ax[1].plot(t[:1001],msd[el][:1001],label=el,ls=ls)
    ax[1].set(title='Li and framework motion',xlabel='Lag time (ps)',ylabel='MSD (Å²)');ax[1].legend();save(f,'LSZC400_transport')
    # CN at each 1 ps time origin; displacements follow for 1/5/10 ps.
    coarse=[a]+frames[9::10];xc=xu[::10,s=='Li'];cn=[]
    for aa in coarse:
        d=aa.get_all_distances(mic=True);cn.append((d[np.ix_(s=='Li',s=='O')]<2.7).sum(1))
    cn=np.array(cn);f,ax=plt.subplots(1,2,layout='constrained');mob=[]
    for lag,color in [(1,'#5e3c99'),(5,'#31688e'),(10,'#d73027')]:
        z=conditioned_mobility(xc,cn,lag,1)
        ax[0].plot(z[:,0],z[:,2],'o-',color=color,label=f'{lag} ps')
        mob.extend([[lag,*row] for row in z])
    cc,n=np.unique(cn[:-10],return_counts=True)
    ax[1].bar(cc,n/n.sum(),color='#31688e')
    ax[0].set(title='Mobility by starting Li–O CN',xlabel='Li–O neighbours (<2.7 Å)',ylabel='Mean subsequent |Δr|² (Å²)');ax[0].legend()
    ax[1].set(title='10 ps origin population',xlabel='Li–O neighbours (<2.7 Å)',ylabel='Fraction of Li–origin samples')
    save(f,'LSZC400_coordination_mobility')
    np.savetxt(OUT/'LSZC400_conditioned_mobility.csv',mob,delimiter=',',header='lag_ps,origin_LiO_CN,observations,mean_d2_A2,SD_d2_A2',comments='')
    # Common early/late structural definitions, 10 snapshots each.
    pairs=[('Li','O',2.7),('Li','Cl',3.2),('Zr','O',2.6),('Zr','Cl',3.2),('S','O',2.)]
    edges=np.arange(0,5.0001,.05);r=(edges[1:]+edges[:-1])/2
    f,ax=plt.subplots(2,2,layout='constrained');structure={}
    for label,ids,color,ls in [('early',range(0,500,50),'#777777','--'),('late',range(1500,2000,50),'#31688e','-')]:
        gs=[];cs=[];so=[]
        for idx in ids:
            g,c,_=frame_metrics(frames[idx],pairs,edges);gs.append(g);cs.append(c)
            d=frames[idx].get_all_distances(mic=True);so.append(float(((d[np.ix_(s=='S',s=='O')]<2).sum(1)==4).mean()))
        g=np.mean(gs,0);structure[label]={'CN':np.mean(cs,0).tolist(),'SO4_fraction':float(np.mean(so))}
        np.savetxt(OUT/f'LSZC400_{label}_RDF.csv',np.c_[r,g.T],delimiter=',',header='r_A,'+','.join(u+'_'+v for u,v,_ in pairs),comments='')
        for j in range(4):ax.flat[j].plot(r,g[j],color=color,ls=ls,label=label)
    for j,(u,v,_) in enumerate(pairs[:4]):ax.flat[j].set(title=f'{u}–{v}',xlabel='r (Å)',ylabel='g(r)');ax.flat[j].legend()
    save(f,'LSZC400_RDF')
    th=np.loadtxt(p/'thermo.out');assert th.shape==(2000,18) and np.isfinite(th).all()
    rho=a.get_masses().sum()*1.6605390666/a.get_volume()
    vals=np.c_[th[:,0],th[:,2]/272,th[:,3:6].mean(1)]
    np.savetxt(OUT/'LSZC400_thermo.csv',np.c_[t[1:],vals],delimiter=',',header='time_ps,T_K,PE_eV_atom,P_GPa',comments='')
    f,ax=plt.subplots(1,3,layout='constrained')
    for j,ylabel in enumerate(['Temperature (K)','Potential energy (eV/atom)','Pressure (GPa)']):
        ax[j].plot(t[1:],vals[:,j],lw=.8,alpha=.4,color='#31688e');ax[j].plot(np.arange(40)*5+2.5,vals[:,j].reshape(40,50).mean(1),color='#222222')
        ax[j].set(title='400 K production',xlabel='Time (ps)',ylabel=ylabel)
    save(f,'LSZC400_thermodynamics')
    res={'T_K':400,'atoms':272,'N_Li':32,'volume_A3':a.get_volume(),'rho_g_cm3':rho,'fits':fits,'block_D_5to20_cm2_s':blocks.tolist(),'sigma_NE_app_mS_cm':sigma_mscm(fit['D_cm2_s'],32,a.get_volume(),400),'mean_T_K':float(vals[:,0].mean()),'mean_P_GPa':float(vals[:,2].mean()),'PE_last50_minus_first50_eV_atom':float(vals[-500:,1].mean()-vals[:500,1].mean()),'MSD80_A2':{el:float(msd[el][800]) for el in els},'structure':structure,'mobility_cutoff_A':2.7,'source_hashes':{q.name:hashlib.sha256(q.read_bytes()).hexdigest() for q in p.iterdir() if q.is_file()}}
    (OUT/'LSZC400_summary.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2),flush=True)

if __name__=='__main__':lszc()
