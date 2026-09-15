"""Re-average unchanged 900 K trajectories; no smoothing or trajectory selection.

Python quantitative-grid contract: compare four local pair distributions between
MACE and NEP, not their accuracy. Preserve 150–200 ps, 0.05 A shells; increase
sampling from 21 to all 501 saved frames. Source CSVs and hashes are retained.
GPUMDkit plt_rdf.py reference: one pair per panel, direct lines, no filter.
"""
import hashlib
import json
import numpy as np
from ase import Atoms
from ase.io import read
from analyze_lzoc_production import read_dump, read_gpumd
from finish_amorphous_analysis import frame_metrics
from paper_aligned_analysis import ROOT, OUT

def main():
    pairs=[('Li','Cl',3.2),('Li','O',2.7),('Zr','Cl',3.2),('Zr','O',2.6)]
    edges=np.arange(0,5.0001,.05)
    radii=(edges[:-1]+edges[1:])/2
    report={'reference':'https://github.com/zhyan0603/GPUMDkit/blob/main/Scripts/plt_scripts/plt_rdf.py',
            'window_ps':[150,200], 'bin_A':.05, 'smoothing':False, 'models':{}}
    for model in ['MACE','NEP89']:
        if model=='MACE':
            path=ROOT/'results/LZOC/analysis_20260912/source/mace/900K_R1/production/trajectory.lammpstrj'
            t,x,c,s=read_dump(path)
        else:
            path=ROOT/'results/LZOC/legacy_comparison_20260915/source_900K/production/dump.xyz'
            t,x,c,s=read_gpumd(path)
            initial=read(path.parent/'model.xyz')
            x=np.concatenate([initial.positions[None],x]);t=np.r_[0,t]
        assert len(t)==2001 and np.allclose(np.diff(t),.1) and np.allclose(c,c[0])
        selected=np.flatnonzero((t>=150-1e-8)&(t<=200+1e-8))
        assert len(selected)==501
        values=[]
        for k in selected:
            a=Atoms(s,positions=x[k],cell=c[0],pbc=True)
            g,_,_=frame_metrics(a,pairs,edges)
            values.append(g)
        values=np.array(values);mean=values.mean(axis=0)
        assert np.isfinite(mean).all() and (mean>=0).all()
        # Reproduce the original sparse average as a source/parser regression check.
        old=np.loadtxt(OUT/f'legacy_{model}_900K_RDF.csv',delimiter=',',skiprows=1)
        np.testing.assert_allclose(values[::25].mean(axis=0).T,old[:,1:],atol=1e-9)
        np.savetxt(OUT/f'legacy_{model}_900K_RDF_dense.csv',np.c_[radii,mean.T],delimiter=',',
                   header='r_A,'+','.join(a+'_'+b for a,b,_ in pairs),comments='')
        report['models'][model]={'frames':501,'source':str(path.relative_to(ROOT)),
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'max_abs_change_from_sparse':float(np.max(np.abs(mean.T-old[:,1:])))}
        print(model,'501 frames verified',flush=True)
    (OUT/'legacy_RDF_dense_provenance.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
