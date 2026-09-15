"""Geometric connectivity and fixed cutoff sensitivity; no trajectory editing."""
from pathlib import Path
from collections import Counter
import hashlib,json,csv
import numpy as np
from ase.io import read
from scipy.sparse.csgraph import connected_components

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/amorphous_review_20260915/structure_followup'

def motifs(ps,pp):
    ps=np.asarray(ps,bool);pp=np.asarray(pp,bool)
    n,m=ps.shape
    assert pp.shape==(n,n) and np.array_equal(pp,pp.T)
    adj=np.zeros((n+m,n+m),bool)
    adj[:n,:n]=pp;adj[:n,n:]=ps;adj[n:,:n]=ps.T
    count,labels=connected_components(adj,directed=False)
    return dict(Counter(f'P{sum(labels[:n]==i)}S{sum(labels[n:]==i)}' for i in range(count)))

def run():
    OUT.mkdir(parents=True,exist_ok=True);result={};hashes={}
    p=ROOT/'results/amorphous_validation_20260914/source/Li3PS4/relaxation/dump.xyz'
    hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    frames=read(p,index=':')[-10:];table=[]
    for cut in [2.4,2.6,2.8]:
        totals=Counter();pfractions=[];bridges=[];ppairs=[]
        for idx,a in enumerate(frames):
            s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf)
            ps=d[np.ix_(s=='P',s=='S')]<cut;pp=d[np.ix_(s=='P',s=='P')]<2.6
            counts=motifs(ps,pp);totals.update(counts)
            pfractions.append(counts.get('P1S4',0)/sum(s=='P'))
            bridges.append(float((ps.sum(0)>=2).mean()));ppairs.append(int(pp.sum()//2))
            for motif,count in counts.items():table.append([cut,2.6,11+idx,motif,count])
        result[str(cut)]={'component_counts_over_10_frames':dict(totals),
            'fraction_of_P_in_isolated_P1S4':float(np.mean(pfractions)),
            'fraction_of_S_shared_by_at_least_two_P':float(np.mean(bridges)),
            'mean_PP_pairs_below_2point6_A':float(np.mean(ppairs))}
    with (OUT/'Li3PS4_geometric_components.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['PS_cutoff_A','PP_cutoff_A','time_ps','geometric_component','count']);w.writerows(table)
    p=ROOT/'results/amorphous_review_20260915/source/LSZC_anneal/hold/dump.xyz'
    hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
    frames=read(p,index=':')[-100:];distances=[]
    for a in frames:
        s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True)
        distances.append({el:d[np.ix_(s=='Zr',s==el)] for el in ['O','Cl']})
    sweep=[]
    for el,cuts in [('O',[2.2,2.4,2.6,2.8,3.0]),('Cl',[2.8,3.0,3.2,3.4,3.6])]:
        for cut in cuts:
            cn=np.array([(d[el]<cut).sum(1).mean() for d in distances])
            sweep.append([el,cut,float(cn.mean()),float(cn.std(ddof=1))])
    with (OUT/'LSZC_cutoff_sensitivity.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['Zr_neighbour','cutoff_A','mean_CN','frame_SD_not_SE']);w.writerows(sweep)
    (OUT/'results.json').write_text(json.dumps({'Li3PS4':result,'LSZC':sweep,'hashes':hashes},indent=2)+'\n')
    print(json.dumps({'Li3PS4':result,'LSZC':sweep},indent=2))

if __name__=='__main__':run()
