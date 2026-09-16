"""Same-window structure screening, not proof of equilibrium or model accuracy.

Python quantitative grids: late RDF, CN distributions, NPT block means.
Each has one role; no diffusion fit and no synthetic/adjusted trajectories.
Outputs are slide-sized PNG and editable PDF/SVG with CSV/JSON provenance.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys
import numpy as np
from ase.io import read
sys.path.insert(0,str(Path(__file__).resolve().parent))
from plot_lzoc_preparation import read_md

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'materials/candidates/LZOC/archive/completed_reference_trials'
OUT=ROOT/'docs/daily_reports/2026-09-14/figures'
PAIRS=[('Li','Cl',3.2),('Li','O',2.7),('Zr','Cl',3.0),('Zr','O',2.6)]
EXPECTED_HASH=['91d606ba361e06759d02b2d4df0c32b43d9e4acd12898aba17be9dd7894c8699',
 'ee3a55196a5122325063cb016c8ade67ff71b3ab1a3343a7d3d4ad22f8342837',
 '7e8064b138d260cad65c9400f5377eccecd2fbbae68fec919e737d06ff220b07']

def pair_stats(atoms,x,y,edges,cutoff):
    symbols=np.array(atoms.get_chemical_symbols())
    dm=atoms.get_all_distances(mic=True)
    np.fill_diagonal(dm,np.inf)
    distances=dm[np.ix_(symbols==x,symbols==y)]
    cn=(distances<=cutoff).sum(axis=1)
    nx=(symbols==x).sum();ny=(symbols==y).sum()
    denom=nx*(ny-int(x==y))*4*np.pi/3*np.diff(edges**3)/atoms.get_volume()
    rdf=np.histogram(distances,edges)[0]/denom if np.all(denom>0) else np.full(len(edges)-1,np.nan)
    return rdf,cn

def load_late(p):
    text=p.read_text();mapping=None;steps=[]
    for block in text.split('ITEM: TIMESTEP\n')[1:]:
        lines=block.splitlines();steps.append(int(lines[0]))
        idx=next(i for i,l in enumerate(lines) if l.startswith('ITEM: ATOMS'))
        rows=[l.split() for l in lines[idx+1:]]
        current={int(r[0]):(int(r[1]),r[2]) for r in rows}
        assert len(rows)==192 and set(current)==set(range(1,193))
        if mapping is None:mapping=current
        assert current==mapping
    assert np.array_equal(steps,np.arange(0,110001,100))
    assert Counter(v[1] for v in mapping.values())==Counter(Li=42,Zr=24,O=12,Cl=114)
    frames=read(p,format='lammps-dump-text',index=':')
    late=[a for a in frames if 100000<=a.info['timestep']<=110000][::5]
    assert len(late)==21
    for a in late:
        assert Counter(a.get_chemical_symbols())==Counter(Li=42,Zr=24,O=12,Cl=114)
        assert np.isfinite(a.positions).all() and a.get_volume()>0
        assert np.min(1/np.linalg.norm(a.cell.reciprocal(),axis=1))>9
    return late

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,'axes.titlesize':17,
        'axes.labelsize':15,'axes.linewidth':1.2,'lines.linewidth':2,'pdf.fonttype':42,'svg.fonttype':'none'})
    OUT.mkdir(exist_ok=True,parents=True)
    rdf_fig,rdf_ax=plt.subplots(2,2,figsize=(11,8))
    cn_fig,cn_ax=plt.subplots(2,2,figsize=(11,8))
    block_fig,block_ax=plt.subplots(2,1,figsize=(10,7),sharex=True)
    colors=['#32688E','#B37525','#766097'];styles=['-','--','-.'];markers=['o','s','^']
    edges=np.arange(0,4.50001,.05);summary={}
    for i,(c,ls,m) in enumerate(zip(colors,styles,markers),1):
        p=BASE/f'source_{i}/candidate.lammpstrj'
        sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==EXPECTED_HASH[i-1]
        frames=load_late(p);entry={'trajectory_sha256':sha,'total_frames':1101,'sampled_frames':21,'pairs':{}}
        rdf_data=[(edges[:-1]+edges[1:])/2];rdf_names=['r_A'];cn_rows=[]
        for k,(x,y,cut) in enumerate(PAIRS):
            rdfs=[];coords=[]
            for a in frames:
                g,cn=pair_stats(a,x,y,edges,cut);rdfs.append(g);coords.extend(cn.tolist())
            mean=np.mean(rdfs,axis=0);rdf_data.append(mean);rdf_names.append(f'{x}_{y}')
            freq=np.bincount(coords,minlength=13)/len(coords)
            assert abs(freq.sum()-1)<1e-12
            for n,pr in enumerate(freq):cn_rows.append([k,cut,n,pr])
            entry['pairs'][f'{x}-{y}']={'cutoff_A':cut,'mean_CN':float(np.mean(coords)),
                'observations':len(coords),'distribution':freq.tolist(),'rdf_peak_r_A':float(rdf_data[0][np.argmax(mean)])}
            rdf_ax.flat[k].plot(rdf_data[0],mean,color=c,ls=ls,label=f'Candidate {i}')
            cn_ax.flat[k].plot(np.arange(len(freq)),freq,marker=m,markersize=5,color=c,ls=ls,label=f'Candidate {i}')
        np.savetxt(OUT/f'candidate_{i}_late_rdf.csv',np.column_stack(rdf_data),delimiter=',',header=','.join(rdf_names),comments='')
        np.savetxt(OUT/f'candidate_{i}_late_coordination.csv',cn_rows,delimiter=',',header='pair_index,cutoff_A,CN,probability',comments='')
        a=read_md(BASE/f'source_{i}/candidate.log');blocks=[]
        for lo in range(45,55):
            b=a[(a[:,1]>lo)&(a[:,1]<=lo+1)];assert len(b)==20
            blocks.append([lo+.5,b[:,9].mean(),b[:,4].mean()/192,b[:,3].mean()])
        blocks=np.array(blocks)
        for k in (0,1):block_ax[k].plot(blocks[:,0],blocks[:,k+1],color=c,ls=ls,marker=m,label=f'Candidate {i}')
        np.savetxt(OUT/f'candidate_{i}_npt_blocks.csv',blocks,delimiter=',',header='center_ps,rho_mean_g_cm3,PE_mean_eV_atom,T_mean_K',comments='')
        entry['block_boundary']='(start,start+1] ps; 20 correlated thermo samples per block'
        summary[str(i)]=entry
        print('Processed candidate',i,flush=True)
    for k,(x,y,cut) in enumerate(PAIRS):
        r=rdf_ax.flat[k];r.set(title=f'{x}–{y}',xlabel='Distance (Å)',ylabel='g(r)',xlim=(0,4.5),ylim=(0,None))
        a=cn_ax.flat[k];a.set(title=f'{x}–{y} (cutoff {cut:.1f} Å)',xlabel='Coordination number',ylabel='Probability',xlim=(-.3,10.3),ylim=(0,None))
        # Integer ticks; include all populated bins even when beyond default view.
        max_cn=max(max(j for j,p in enumerate(summary[str(i)]['pairs'][f'{x}-{y}']['distribution']) if p>0) for i in (1,2,3))
        a.set_xlim(-.3,max(3,max_cn+1)+.3);a.set_xticks(range(0,max(3,max_cn+1)+1,1 if max_cn<8 else 2))
    rdf_fig.suptitle('LZOC — local structure at 300 K (50–55 ps)',fontsize=19)
    cn_fig.suptitle('LZOC — coordination distributions (50–55 ps)',fontsize=19)
    block_fig.suptitle('LZOC — NPT relaxation at 300 K',fontsize=19)
    block_ax[0].set_ylabel(r'Mean density (g cm$^{-3}$)')
    block_ax[1].set_ylabel('Mean PE (eV/atom)');block_ax[1].set_xlabel('Preparation time (ps)')
    block_ax[1].set_xlim(45,55)
    block_fig.text(.5,.01,'1 ps block means; connected points are guides, not a fit or confidence interval.',ha='center',fontsize=11)
    for fig,axes,name in [(rdf_fig,rdf_ax,'LZOC_three_candidate_RDF'),(cn_fig,cn_ax,'LZOC_three_candidate_coordination'),(block_fig,block_ax,'LZOC_three_candidate_NPT_blocks')]:
        for ax in axes.flat:ax.grid(alpha=.18)
        axes.flat[0].legend(fontsize=11)
        fig.tight_layout(rect=[0,.035,1,.95])
        for ext in ('png','pdf','svg'):
            dest=OUT/f'{name}.{ext}';fig.savefig(dest,dpi=200)
            if ext=='svg':dest.write_text('\n'.join(l.rstrip() for l in dest.read_text().splitlines())+'\n')
        plt.close(fig)
    (OUT/'candidate_structure_summary.json').write_text(json.dumps(summary,indent=2)+'\n')

if __name__=='__main__':main()
