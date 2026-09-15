"""Numerical and structural screening, not certification of a glass or MLIP."""
from pathlib import Path
from itertools import product
import json
import hashlib
import numpy as np
from ase.io import read

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/amorphous_validation_20260914'

def pair(a,x,y,edges,cut):
    sy=np.array(a.get_chemical_symbols()); d=a.get_all_distances(mic=True)
    np.fill_diagonal(d,np.inf)
    distances=d[np.ix_(sy==x,sy==y)]
    nx=sum(sy==x); ny=sum(sy==y)
    norm=nx*(ny-int(x==y))*4*np.pi/3*np.diff(edges**3)/a.get_volume()
    return np.histogram(distances,edges)[0]/norm,(distances<cut).sum(axis=1)

def order(a,h):
    f=a.get_scaled_positions()[np.array(a.get_chemical_symbols())=='P']
    return np.abs(np.exp(2j*np.pi*f@h.T).mean(axis=0))**2

def main():
    results={}
    for material in ['Li3PS4','LiPON']:
        folder=OUT/'source'/material; dest=OUT/material; dest.mkdir(exist_ok=True)
        initial=read(folder/'smoke/model.xyz')
        n=len(initial); mass=initial.get_masses().sum()
        t=np.loadtxt(folder/'relaxation/thermo.out'); assert t.shape==(400,18) and np.isfinite(t).all()
        cell=t[:,9:].reshape(-1,3,3); vol=np.linalg.det(cell)
        values=np.column_stack((t[:,0],t[:,2]/n,t[:,3:6].mean(axis=1),mass*1.66053906660/vol))
        blocks=values.reshape(4,100,4).mean(axis=1)
        np.savetxt(dest/'relaxation_5ps_blocks.csv',np.column_stack(([2.5,7.5,12.5,17.5],blocks)),delimiter=',',header='time_center_ps,T_K,PE_eV_atom,P_GPa,density_g_cm3',comments='')
        frames=read(folder/'relaxation/dump.xyz',index=':')
        expected=20 if material=='Li3PS4' else 200
        assert len(frames)==expected
        late=frames[-expected//2:]
        assert all(np.array_equal(a.numbers,initial.numbers) for a in frames)
        all_min=[]; nn_min=[]
        for a in frames:
            dm=a.get_all_distances(mic=True); np.fill_diagonal(dm,np.inf); all_min.append(dm.min())
            if material=='LiPON':
                mask=np.array(a.get_chemical_symbols())=='N';nn_min.append(float(dm[np.ix_(mask,mask)].min()))
        pairs=[('P','S',2.6),('Li','S',3.2),('P','P',4.0)] if material=='Li3PS4' else [('P','O',2.1),('P','N',2.1),('Li','O',2.8),('N','P',2.1)]
        rmax=min(5.,min(min(a.cell.lengths()) for a in late)/2-.05)
        edges=np.arange(0,rmax,.05); r=(edges[:-1]+edges[1:])/2
        table=[r]; header=['r_A']; summary={}
        for x,y,cut in pairs:
            gs=[]; cs=[]
            for a in late:
                g,c=pair(a,x,y,edges,cut); gs.append(g);cs.extend(c)
            gi,ci=pair(initial,x,y,edges,cut)
            table.extend([gi,np.mean(gs,axis=0)]);header.extend([x+y+'_initial',x+y+'_late'])
            summary[x+'-'+y]={'cutoff_A':cut,'initial_mean_CN':float(ci.mean()),'late_mean_CN':float(np.mean(cs)),'late_CN_distribution':{str(k):float(np.mean(np.array(cs)==k)) for k in sorted(set(cs))}}
        np.savetxt(dest/'rdf.csv',np.array(table).T,delimiter=',',header=','.join(header),comments='')
        h=np.array([v for v in product(range(-4,5),repeat=3) if v!=(0,0,0)])
        before=order(initial,h); idx=np.argsort(before)[-20:]
        after=np.mean([order(a,h[idx]) for a in late],axis=0)
        np.savetxt(dest/'P_reciprocal_order.csv',np.column_stack((h[idx],before[idx],after)),delimiter=',',header='h,k,l,initial_coherent_fraction,late_coherent_fraction',comments='')
        # Endpoint MIC displacement relative to start of melt, not a diffusivity.
        m=read(folder/'melt/dump.xyz',index=':'); f0=m[0].get_scaled_positions(); fend=m[-1].get_scaled_positions()
        delta=fend-f0;delta-=np.round(delta); dr=delta@m[-1].cell.array
        sy=np.array(initial.get_chemical_symbols())
        result={'n_atoms':n,'relaxation_samples':400,'relaxation_mean':dict(zip(['T_K','PE_eV_atom','P_GPa','rho_g_cm3'],values.mean(axis=0).tolist())),
            'relaxation_SD_not_SE':dict(zip(['T_K','PE_eV_atom','P_GPa','rho_g_cm3'],values.std(axis=0,ddof=1).tolist())),
            'last_minus_first_5ps_block':dict(zip(['T_K','PE_eV_atom','P_GPa','rho_g_cm3'],(blocks[-1]-blocks[0]).tolist())),
            'PE_slope_eV_atom_ps':float(np.polyfit(np.arange(1,401)*.05,values[:,1],1)[0]),
            'initial_density_g_cm3':float(mass*1.66053906660/initial.get_volume()),
            'minimum_distance_relaxation_A':float(min(all_min)), 'pairs':summary,
            'P_initial_top20_order_mean':float(before[idx].mean()),'P_late_same_top20_order_mean':float(after.mean()),
            'melt_endpoint_MIC_displacement2_A2':{s:float(np.mean(np.sum(dr[sy==s]**2,axis=1))) for s in sorted(set(sy))},
            'hashes':{str(p.relative_to(folder)):hashlib.sha256(p.read_bytes()).hexdigest() for p in folder.glob('*/*') if p.name in ['thermo.out','dump.xyz','model.xyz']}}
        if nn_min:
            result['N_N_minimum_distance_range_A']=[min(nn_min),max(nn_min)]
            result['fraction_relaxation_frames_N_N_under_1_6A']=float(np.mean(np.array(nn_min)<1.6))
        results[material]=result
        final=read(folder/'relaxation/restart.xyz');final.calc=None;from ase.io import write
        write(dest/'final_candidate.cif',final)
        print(material,json.dumps({k:v for k,v in result.items() if k!='hashes'}),flush=True)
    (OUT/'structural_thermo_summary.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
