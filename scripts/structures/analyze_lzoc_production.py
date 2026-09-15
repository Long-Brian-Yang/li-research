"""Reproducible first-pass production analysis; source files are never modified.
FFT windowed MSD definition matches the Einstein time-origin average.
ASE handles triclinic minimum-image distances. Fits are exploratory.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import numpy as np
from scipy.stats import linregress
from ase import Atoms
from ase.geometry import find_mic
from ase.io import read

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/LZOC/analysis_20260912'
MASS={'Li':6.94,'Zr':91.224,'O':15.999,'Cl':35.45}

def window_msd(x):
    x=np.asarray(x,dtype=float);x=x-x[0]
    n=len(x);f=np.fft.rfft(x,n=2*n,axis=0)
    corr=np.fft.irfft(f*f.conjugate(),n=2*n,axis=0)[:n].sum(axis=(1,2))
    s=np.r_[0,np.cumsum((x*x).sum(axis=(1,2)))]
    k=np.arange(n)
    y=(s[n-k]+s[n]-s[k]-2*corr)/((n-k)*x.shape[1])
    y[0]=0
    return y

def fit_msd(t,y,lo,hi):
    mask=(t>=lo)&(t<=hi);r=linregress(t[mask],y[mask])
    positive=mask&(t>0)&(y>0)
    alpha=linregress(np.log(t[positive]),np.log(y[positive])).slope
    return dict(D_cm2_s=float(r.slope/6*1e-4),R2=float(r.rvalue**2),
                intercept_A2=float(r.intercept),alpha=float(alpha),lo_ps=lo,hi_ps=hi)

def unwrap(x,cell):
    frac=x@np.linalg.inv(cell);delta=np.diff(frac,axis=0)
    delta-=np.round(delta)
    return np.concatenate([x[:1],x[:1]+np.cumsum(delta@cell,axis=0)])

def read_dump(p):
    times=[];positions=[];cells=[];symbols=None
    with open(p) as f:
        while True:
            line=f.readline()
            if not line:break
            assert line.strip()=='ITEM: TIMESTEP'
            step=int(f.readline());assert f.readline().strip()=='ITEM: NUMBER OF ATOMS'
            n=int(f.readline());assert n==192
            assert 'xy xz yz' in f.readline()
            b=np.array([list(map(float,f.readline().split())) for _ in range(3)])
            xy,xz,yz=b[:,2]
            lx=b[0,1]-b[0,0]-max(0,xy,xz,xy+xz)+min(0,xy,xz,xy+xz)
            ly=b[1,1]-b[1,0]-max(0,yz)+min(0,yz)
            cell=np.array([[lx,0,0],[xy,ly,0],[xz,yz,b[2,1]-b[2,0]]])
            columns=f.readline().split()[2:]
            rows=[f.readline().split() for _ in range(n)];rows.sort(key=lambda r:int(r[0]))
            assert [int(r[0]) for r in rows]==list(range(1,193))
            sy=[r[columns.index('element')] for r in rows]
            if symbols is None:symbols=sy
            assert sy==symbols
            positions.append([[float(r[columns.index(c)]) for c in ('xu','yu','zu')] for r in rows])
            cells.append(cell);times.append(step*.0005)
    return np.array(times),np.array(positions),np.array(cells),np.array(symbols)

def read_gpumd(p):
    times=[];positions=[];cells=[];symbols=None
    with open(p) as f:
        while True:
            line=f.readline()
            if not line:break
            n=int(line);assert n==192
            header=f.readline();t=float(re.search(r'Time=([\d.eE+-]+)',header).group(1))/1000
            cell=np.array(list(map(float,re.search(r'Lattice="([^"]+)"',header).group(1).split()))).reshape(3,3)
            rows=[f.readline().split() for _ in range(n)];sy=[r[0] for r in rows]
            if symbols is None:symbols=sy
            assert sy==symbols
            positions.append([[float(v) for v in r[1:4]] for r in rows]);times.append(t);cells.append(cell)
    return np.array(times),np.array(positions),np.array(cells),np.array(symbols)

def thermo(p,nep=False):
    if nep:
        a=np.loadtxt(p);assert a.shape[1]==18
        volume=np.linalg.det(a[:,9:].reshape(-1,3,3))
        mass=42*MASS['Li']+24*MASS['Zr']+12*MASS['O']+114*MASS['Cl']
        return np.column_stack([np.arange(1,len(a)+1)*.05,a[:,0],a[:,2],a[:,1]+a[:,2],a[:,3:6].mean(1),volume,mass*1.6605390666/volume])
    rows={}
    for line in p.read_text().splitlines():
        try:a=list(map(float,line.split()))
        except ValueError:continue
        if len(a)==14 and a[2]==192:rows[a[0]]=a
    a=np.array([rows[k] for k in sorted(rows)])
    return a[:,[1,3,4,6,7,8,9]]*np.array([1,1,1,1,1e-4,1,1])

def stats(a):
    result={}
    for i,k in enumerate(['T_K','PE_eV','Etot_eV','P_GPa','V_A3','rho_g_cm3'],1):
        result[k]={'mean':float(a[:,i].mean()),'sd':float(a[:,i].std(ddof=1)),
                   'slope_per_ps':float(linregress(a[:,0],a[:,i]).slope)}
    return result

def main():
    OUT.mkdir(exist_ok=True,parents=True)
    result={};hashes={}
    runs=[('MACE',t,OUT/'source/mace'/f'{t}K_R1') for t in (600,700,800,900)]+[('NEP89',600,OUT/'source/nep89')]
    for model,temp,p in runs:
        key=f'{model}_{temp}K';nep=model=='NEP89';print('Analyzing',key,flush=True)
        trajectory=p/'production'/('dump.xyz' if nep else 'trajectory.lammpstrj')
        for file in p.rglob('*'):
            if file.is_file() and file.suffix not in ('.restart',):hashes[str(file.relative_to(OUT))]=hashlib.sha256(file.read_bytes()).hexdigest()
        t,x,cells,sy=(read_gpumd if nep else read_dump)(trajectory)
        assert Counter(sy)==Counter(Li=42,Zr=24,O=12,Cl=114)
        assert np.isfinite(x).all() and np.allclose(cells,cells[0])
        assert len(t)==(2000 if nep else 2001) and np.allclose(np.diff(t),.1) and abs(t[-1]-200)<1e-8
        if nep:
            a=read(p/'production/model.xyz');assert np.allclose(a.cell,cells[0])
            x=np.concatenate([a.positions[None],x]);t=np.r_[0,t];cells=np.concatenate([cells[:1],cells])
            x=unwrap(x,cells[0])
        # Remove total-system mass-weighted COM motion, not Li-only motion.
        mass=np.array([MASS[s] for s in sy]);com=np.average(x,axis=1,weights=mass)
        corrected=x-com[:,None,:];li=corrected[:,sy=='Li']
        msd=window_msd(li)
        windows={f'{lo}-{hi}':fit_msd(t,msd,lo,hi) for lo,hi in [(5,40),(10,50),(20,80),(20,100),(40,100),(20,180)]}
        blocks=[]
        for lo in (0,50,100,150):
            part=li[(t>=lo)&(t<lo+50)]
            blocks.append(fit_msd(np.arange(len(part))*.1,window_msd(part),5,20)['D_cm2_s'])
        species={s:dict(MSD_200ps_A2=float(np.mean(np.sum((corrected[-1,sy==s]-corrected[0,sy==s])**2,axis=1))),
                        fit=fit_msd(t,window_msd(corrected[:,sy==s]),20,80)) for s in ('Li','Zr','O','Cl')}
        li_com=x[:,sy=='Li']-x[:,sy=='Li'].mean(axis=1)[:,None,:]
        legacy=None
        if not nep:
            raw=np.loadtxt(p/'production/msd_li.dat');single=np.mean(np.sum((li_com-li_com[0])**2,axis=2),axis=1)
            sampled=np.interp(t[1:],raw[:,0]*.0005,raw[:,-1])
            legacy=dict(max_abs_reconstruction_error_A2=float(np.max(np.abs(single[1:]-sampled))),
                        D_single_origin_20_80_ps=fit_msd(raw[:,0]*.0005,raw[:,-1],20,80))
        stages={stage:thermo(p/stage/('thermo.out' if nep else 'log.lammps'),nep) for stage in ['heating','equilibration','production']}
        for stage,values in stages.items():
            assert np.isfinite(values).all()
            np.savetxt(OUT/f'{key}_{stage}_thermo.csv',values,delimiter=',',header='time_ps,T_K,PE_eV,Etot_eV,P_GPa,volume_A3,density_g_cm3',comments='')
        prod=stages['production'];eq=stages['equilibration']
        # Fixed diagnostic cutoffs, identical across runs. Early/late RDF blocks.
        pairs=[('Li','Cl',3.2),('Li','O',2.7),('Zr','Cl',3.),('Zr','O',2.6),('Cl','Cl',4.)]
        edges=np.arange(0,4.5001,.05);r=(edges[1:]+edges[:-1])/2;shell=4*np.pi/3*np.diff(edges**3)
        rdf={};cn={};mins=[]
        for label,indices in [('early',range(0,501,25)),('late',range(1500,2001,25))]:
            accum={f'{a}-{b}':[] for a,b,_ in pairs};counts={k:[] for k in accum}
            for idx in indices:
                atoms=Atoms(sy,positions=x[idx],cell=cells[idx],pbc=True)
                assert min(1/np.linalg.norm(atoms.cell.reciprocal(),axis=1))>9
                d=atoms.get_all_distances(mic=True);np.fill_diagonal(d,np.inf);mins.append(float(d.min()))
                for a,b,cutoff in pairs:
                    distances=d[np.ix_(sy==a,sy==b)];na=(sy==a).sum();nb=(sy==b).sum();name=f'{a}-{b}'
                    accum[name].append(np.histogram(distances,edges)[0]*atoms.get_volume()/(na*(nb-(a==b))*shell))
                    counts[name].append(float((distances<cutoff).sum()/na))
            rdf[label]={k:np.mean(v,axis=0) for k,v in accum.items()}
            cn[label]={k:dict(mean=float(np.mean(v)),frame_sd=float(np.std(v,ddof=1))) for k,v in counts.items()}
        np.savetxt(OUT/f'{key}_rdf.csv',np.column_stack([r]+[v for data in rdf.values() for v in data.values()]),delimiter=',',header=','.join(['r_A']+[f'{label}_{k}' for label,data in rdf.items() for k in data]),comments='')
        np.savetxt(OUT/f'{key}_msd.csv',np.column_stack([t,msd,window_msd(li_com),np.mean(np.sum((li-li[0])**2,axis=2),axis=1)]),delimiter=',',header='lag_ps,Li_MSD_A2,Li_COM_removed_window_MSD_A2,single_origin_system_COM_removed_A2',comments='')
        step=np.diff(x,axis=0);frac=step@np.linalg.inv(cells[0])
        result[key]=dict(model=model,T_target=temp,n_frames=len(t),composition=dict(Counter(sy)),
          cell_A=cells[0].tolist(),max_frame_step_A=float(np.linalg.norm(step,axis=2).max()),
          max_fractional_frame_step=float(np.abs(frac).max()),COM_displacement_A=float(np.linalg.norm(com[-1]-com[0])),
          thermo=stats(prod),thermo_first50=stats(prod[prod[:,0]<50]),thermo_last50=stats(prod[prod[:,0]>=150]),
          density_NPT_first10=stats(eq[eq[:,0]<10])['rho_g_cm3'],density_NPT_last10=stats(eq[eq[:,0]>=40])['rho_g_cm3'],
          fit_windows=windows,block_D_cm2_s=blocks,block_mean=float(np.mean(blocks)),block_sd=float(np.std(blocks,ddof=1)),
          species=species,legacy_check=legacy,CN=cn,sampled_min_pair_A=min(mins),
          rms_RDF_change={k:float(np.sqrt(np.mean((rdf['late'][k]-rdf['early'][k])**2))) for k in rdf['early']})
        (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
        print(key,windows['20-80'],result[key]['thermo']['rho_g_cm3'],flush=True)
    arr={}
    for win in result['MACE_600K']['fit_windows']:
        temps=np.array([600,700,800,900]);ds=np.array([result[f'MACE_{t}K']['fit_windows'][win]['D_cm2_s'] for t in temps])
        if np.all(ds>0):
            f=linregress(1/temps,np.log(ds));arr[win]=dict(Ea_eV=float(-f.slope*8.617333262145e-5),R2=float(f.rvalue**2),D0_cm2_s=float(np.exp(f.intercept)))
    (OUT/'arrhenius.json').write_text(json.dumps(arr,indent=2)+'\n')
    (OUT/'source_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print('Arrhenius',arr,flush=True)

if __name__=='__main__':main()
