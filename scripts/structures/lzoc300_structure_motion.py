"""Local structure and radial displacement probabilities from unchanged 300 ps runs."""
from pathlib import Path
import json,hashlib
import numpy as np
from ase.io import read,iread
from analyze_lzoc_production import unwrap
from finish_amorphous_analysis import frame_metrics

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'results/amorphous_review_20260915/followup300'
PAIRS=[('Li','O',2.7),('Li','Cl',3.2),('Zr','O',2.6),('Zr','Cl',3.2)]

def main():
    results=[];hashes={}
    for T in [340,360,380]:
        p=ROOT/f'results/amorphous_review_20260915/source/LZOC300/nhc300_{T}K_8676684'
        a=read(p/'model.xyz');fs=list(iread(p/'dump.xyz'));s=np.array(a.get_chemical_symbols())
        assert len(fs)==3000 and len(a)==192
        edges=np.arange(0,5.0001,.05);gs=[];counts=[[] for _ in PAIRS]
        for f in fs[999::20]:
            g,_,_=frame_metrics(f,PAIRS,edges);gs.append(g)
            d=f.get_all_distances(mic=True)
            for i,(x,y,cut) in enumerate(PAIRS):counts[i].extend((d[np.ix_(s==x,s==y)]<cut).sum(1).tolist())
        np.savetxt(OUT/f'LZOC_{T}K_RDF.csv',np.c_[(edges[:-1]+edges[1:])/2,np.mean(gs,0).T],delimiter=',',header='r_A,LiO,LiCl,ZrO,ZrCl',comments='')
        bins=np.arange(0,21);probs=[]
        for c in counts:
            assert max(c)<len(bins)
            v=np.bincount(c,minlength=len(bins))/len(c);assert np.isclose(v.sum(),1);probs.append(v)
        np.savetxt(OUT/f'LZOC_{T}K_CN.csv',np.c_[bins,*probs],delimiter=',',header='CN,LiO,LiCl,ZrO,ZrCl',comments='')
        xu=unwrap(np.array([a.positions]+[f.positions for f in fs]),a.cell.array)
        xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
        disp=[];de=np.linspace(0,30,301);tail=[]
        for lag in [100,400,800]:
            radii=np.linalg.norm(xu[lag:,s=='Li']-xu[:-lag,s=='Li'],axis=2).ravel()
            assert radii.max()<de[-1]
            prob=np.histogram(radii,de)[0]/len(radii)/np.diff(de)
            assert np.isclose(np.sum(prob*np.diff(de)),1)
            disp.append(prob);tail.append(dict(lag_ps=lag*.1,rms_A=float(np.sqrt(np.mean(radii**2))),fraction_over3A=float(np.mean(radii>3))))
        np.savetxt(OUT/f'LZOC_{T}K_radial_displacement.csv',np.c_[(de[:-1]+de[1:])/2,*disp],delimiter=',',header='r_A,P10_Ainv,P40_Ainv,P80_Ainv',comments='')
        results.append(dict(T_K=T,mean_CN=[float(np.mean(c)) for c in counts],RDF_peak_r_A=[float(((edges[:-1]+edges[1:])/2)[np.argmax(g)]) for g in np.mean(gs,0)],displacements=tail))
        hashes[str((p/'dump.xyz').relative_to(ROOT))]=hashlib.sha256((p/'dump.xyz').read_bytes()).hexdigest()
    data=dict(records=results,pairs=PAIRS,method='RDF/CN: 101 frames,100–300 ps every2 ps, 0.05 A bins, no smoothing; fixed project cutoffs, not experimental CN. Radial displacement P(r,t)=4*pi*r^2*Gs(r,t); all origins,COM corrected,0.1 A bins. 3 A is descriptive threshold, not a site-defined jump.',source_hashes=hashes)
    (OUT/'structure_motion.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data['records'],indent=2))

if __name__=='__main__':main()
