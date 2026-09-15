"""Reproducible postprocessing of job 8675392; no trajectory modification."""
from pathlib import Path
import hashlib
import json
import numpy as np
from ase.io import read
from analyze_lzoc_production import read_gpumd, unwrap, window_msd, fit_msd

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'targeted_diagnostics'

def run():
    OUT.mkdir(parents=True,exist_ok=True)
    result={}; hashes={}
    p=BASE/'source/LSZC_npt400'
    assert (p/'completed.txt').exists()
    frames=read(p/'dump.xyz',index=':');th=np.loadtxt(p/'thermo.out')
    assert len(frames)==200 and th.shape==(400,18) and np.isfinite(th).all()
    density=np.array([a.get_masses().sum()/a.get_volume()*1.6605390666 for a in frames])
    cn=[]
    for a in frames:
        s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True)
        assert len(a)==272
        cn.append([(d[np.ix_(s=='Zr',s=='O')]<2.6).sum(1).mean(),
                   (d[np.ix_(s=='Zr',s=='Cl')]<3.2).sum(1).mean(),
                   ((d[np.ix_(s=='S',s=='O')]<2.).sum(1)==4).mean()])
    np.savetxt(OUT/'LSZC_structure.csv',np.c_[np.arange(1,201)*.1,density,cn],
               delimiter=',',header='time_ps,density_g_cm3,CN_ZrO_2.6A,CN_ZrCl_3.2A,fraction_S_fourO_2A',comments='')
    blocks=np.c_[th[:,0],th[:,2]/272,th[:,3:6].mean(1)].reshape(4,100,3).mean(1)
    result['LSZC']={'last10ps_density_g_cm3':float(density[-100:].mean()),
                    'last10ps_CN_ZrO_ZrCl_fraction_S4O':np.mean(cn[-100:],axis=0).tolist(),
                    '5ps_blocks_T_PE_atom_P':blocks.tolist()}
    paths=[p];initial=None
    for tag,p in [('NHC_0.5fs',BASE/'source/LZOC_NHC05_380'),
                  ('NHC_2fs',BASE/'source/LZOC_NHC80/aimd_aligned_380K_8675022/production')]:
        paths.append(p)
        ts,x,c,s=read_gpumd(p/'dump.xyz');a=read(p/'model.xyz')
        assert len(ts)==800 and np.allclose(np.diff(ts),.1) and np.allclose(c,c[0])
        if initial is None: initial=a
        else:
            np.testing.assert_allclose(initial.positions,a.positions,atol=1e-9)
            np.testing.assert_allclose(initial.cell,a.cell,atol=1e-9)
            np.testing.assert_allclose(initial.arrays['vel'],a.arrays['vel'])
        x=unwrap(np.concatenate([a.positions[None],x]),c[0])
        x-=np.average(x,axis=1,weights=a.get_masses())[:,None,:]
        y=window_msd(x[:,s=='Li']);t=np.arange(801)*.1
        np.savetxt(OUT/(tag+'_MSD.csv'),np.c_[t,y],delimiter=',',header='lag_ps,Li_MSD_A2',comments='')
        th=np.loadtxt(p/'thermo.out');assert th.shape==(1600,18) and np.isfinite(th).all()
        result[tag]={'fits':{f'{lo}-{hi}ps':fit_msd(t,y,lo,hi) for lo,hi in [(5,20),(10,30),(10,40)]},
                     '20ps_blocks_T_PE_atom_P':np.c_[th[:,0],th[:,2]/192,th[:,3:6].mean(1)].reshape(4,400,3).mean(1).tolist()}
    for p in paths:
        for name in ['dump.xyz','model.xyz','thermo.out','run.in']:
            q=p/name;hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
    result['source_hashes']=hashes
    (OUT/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='source_hashes'},indent=2))

if __name__=='__main__':run()
