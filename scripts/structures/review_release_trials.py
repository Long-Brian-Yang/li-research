"""Reproducible screening of existing diagnostics; no equilibrium certification."""
from pathlib import Path
import json
import hashlib
import numpy as np
from ase.io import read, write
from validate_amorphous_trials import pair

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/amorphous_review_20260915'

def contacts(a,x,y,cut):
    s=np.array(a.get_chemical_symbols())
    d=a.get_all_distances(mic=True)
    np.fill_diagonal(d,np.inf)
    z=d[np.ix_(s==x,s==y)]
    return float(z.min()),(z<cut).sum(axis=1)

def thermo_values(t,a):
    if t.shape!=(400,18) or not np.isfinite(t).all():
        raise ValueError('Expected 400 finite GPUMD 18-column records')
    volume=np.linalg.det(t[:,9:].reshape(-1,3,3))
    if np.any(volume<=0):raise ValueError('Nonpositive cell volume')
    return np.column_stack((t[:,0],t[:,2]/len(a),t[:,3:6].mean(axis=1),sum(a.get_masses())*1.66053906660/volume))

if __name__=='__main__':
    result={}
    for name,sub,pairs in [('LZOC','300K',[('Zr','Cl',3.2),('Zr','O',2.6)]),('LSZC','',[('S','O',1.9),('Zr','Cl',3.2)]),('LiPON','',[('N','N',1.6),('P','O',2.1),('P','N',2.1)])]:
        src=OUT/'source'/name/sub
        a=read(src/'model.xyz'); frames=read(src/'dump.xyz',index=':')
        assert len(frames)==200 and all(np.array_equal(f.numbers,a.numbers) for f in frames)
        v=thermo_values(np.loadtxt(src/'thermo.out'),a)
        b=v.reshape(4,100,4).mean(axis=1)
        dest=OUT/name;dest.mkdir(exist_ok=True)
        np.savetxt(dest/'blocks.csv',np.column_stack(([2.5,7.5,12.5,17.5],b)),delimiter=',',header='time_ps,T_K,PE_eV_atom,P_GPa,rho_g_cm3',comments='')
        stats={}
        # Radial cutoff below half the minimum perpendicular cell height.
        rmax=min(5.,min(1/np.linalg.norm(np.linalg.inv(f.cell.array),axis=0).max()/2 for f in frames[100:])-.05)
        edges=np.arange(0,rmax,.05)
        rdf=[(edges[:-1]+edges[1:])/2]; headers=['r_A']
        for x,y,c in pairs:
            z=[contacts(f,x,y,c) for f in frames]
            stats[x+'-'+y]={'cutoff_A':c,'minimum_A':min(q[0] for q in z),'maximum_frame_minimum_A':max(q[0] for q in z),'fraction_frames_with_contact':float(np.mean([q[0]<c for q in z])),'late_mean_CN':float(np.mean(np.concatenate([q[1] for q in z[100:]])))}
            rdf.append(np.mean([pair(f,x,y,edges,c)[0] for f in frames[100:]],axis=0));headers.append(x+'_'+y)
        np.savetxt(dest/'rdf_late10ps.csv',np.array(rdf).T,delimiter=',',header=','.join(headers),comments='')
        end=read(src/'restart.xyz');end.calc=None;write(dest/'final_candidate.cif',end)
        result[name]={'n_atoms':len(a),'frames':len(frames),'means_T_PE_P_rho':v.mean(axis=0).tolist(),'SD_not_SE':v.std(axis=0,ddof=1).tolist(),'blocks_T_PE_P_rho':b.tolist(),'last_minus_first_block':(b[-1]-b[0]).tolist(),'pairs':stats,'hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in src.iterdir() if p.is_file()}}
    (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:{x:y for x,y in v.items() if x!='hashes'} for k,v in result.items()},indent=2))
