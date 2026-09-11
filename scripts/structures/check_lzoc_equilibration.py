"""Audit completed candidate-3 equilibration using ASE triclinic MIC.
Outputs diagnostic JSON/RDF, not an automatic scientific acceptance decision.
"""
from pathlib import Path
from collections import Counter
import json
import hashlib
import numpy as np
from ase.io import read

ROOT=Path(__file__).resolve().parents[2]
P=ROOT/'materials/candidates/LZOC/equilibration_8634186'
OUT=P/'analysis'
OUT.mkdir(exist_ok=True)
old=ROOT/'materials/candidates/LZOC/completed_reference_trials/candidate3_check'
previous=json.loads((old/'diagnostics.json').read_text())
mapping=None
for block in (P/'equilibration.lammpstrj').read_text().split('ITEM: TIMESTEP\n')[1:]:
    lines=block.splitlines(); offset=next(i for i,x in enumerate(lines) if x.startswith('ITEM: ATOMS'))
    records=[x.split() for x in lines[offset+1:]]
    current={int(x[0]):(int(x[1]),x[2]) for x in records}
    assert len(records)==192 and set(current)==set(range(1,193))
    if mapping is None: mapping=current
    assert current==mapping
frames=read(P/'equilibration.lammpstrj',format='lammps-dump-text',index=':')
assert [a.info['timestep'] for a in frames]==list(range(0,100001,100))
for a in frames:
    assert Counter(a.get_chemical_symbols())==Counter(Li=42,Zr=24,O=12,Cl=114)
    assert np.isfinite(a.positions).all() and a.get_volume()>0
rows={}
for line in (P/'equilibration.log').read_text().splitlines():
    try: v=list(map(float,line.split()))
    except ValueError: continue
    if len(v)==14 and v[2]==192 and 0<=v[1]<=50: rows[v[1]]=v
t=np.array(sorted(rows.values(),key=lambda v:v[1]))
assert len(t)==1001 and t[-1,1]==50
stats={}
for lo,hi in [(0,10),(10,20),(20,30),(30,40),(40,50),(30,50)]:
    b=t[(t[:,1]>=lo)&((t[:,1]<hi) if hi<50 else (t[:,1]<=hi))]
    stats[f'{lo}-{hi}']={name:dict(mean=float(b[:,i].mean()),sd=float(b[:,i].std(ddof=1)),slope_per_ps=float(np.polyfit(b[:,1],b[:,i],1)[0])) for name,i in [('T_K',3),('PE_eV',4),('density_g_cm3',9),('volume_A3',8)]}
pairs=[('Li','Cl',3.2),('Li','O',2.7),('Zr','Cl',3.0),('Zr','O',2.6),('Cl','Cl',4.0)]
edges=np.linspace(0,4.5,91); r=(edges[:-1]+edges[1:])/2;shell=4*np.pi/3*np.diff(edges**3)
allrdf={};cn={};order={};minimum={}
for label,lo,hi in [('30-40',30,40),('40-50',40,50)]:
    group=[a for a in frames if lo*2000<=a.info['timestep']<=hi*2000][::10]
    arrays={f'{x}-{y}':[] for x,y,c in pairs};coord={k:[] for k in arrays};mins=[]
    for a in group:
        assert min(1/np.linalg.norm(a.cell.reciprocal(),axis=1))>9
        d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf);mins.append(float(d.min()))
        sy=np.array(a.get_chemical_symbols())
        for x,y,c in pairs:
            nx=(sy==x).sum();ny=(sy==y).sum();block=d[np.ix_(sy==x,sy==y)]
            arrays[f'{x}-{y}'].append(np.histogram(block.ravel(),edges)[0]/(nx*(ny-(x==y))*shell/a.get_volume()))
            coord[f'{x}-{y}'].append(float((block<c).sum()/nx))
    minimum[label]=min(mins)
    allrdf[label]={k:np.mean(v,axis=0) for k,v in arrays.items()}
    cn[label]={k:float(np.mean(v)) for k,v in coord.items()}
    order[label]={}
    for element in ['Cl','Zr']:
        reference=previous['initial_peak_retention'][element];h=np.array(reference['hkl']);vals=[]
        for a in group:
            mask=np.array(a.get_chemical_symbols())==element
            intensity=np.abs(np.exp(2j*np.pi*a.get_scaled_positions()[mask]@h.T).sum(axis=0))**2/mask.sum()
            vals.append(intensity)
        order[label][element]=float(np.mean(vals,axis=0).sum()/sum(reference['initial']))
columns=[r];names=['r_A']
for label,values in allrdf.items():
    for k,v in values.items(): columns.append(v);names.append(label+'_'+k)
np.savetxt(OUT/'rdf_blocks.csv',np.column_stack(columns),delimiter=',',header=','.join(names),comments='')
peaks={label:{k:float(r[np.argmax(v)]) for k,v in data.items()} for label,data in allrdf.items()}
final=read(P/'equilibrated_300K.data',format='lammps-data',atom_style='atomic',Z_of_type={1:3,2:40,3:8,4:17})
assert np.allclose(final.cell,frames[-1].cell) and np.allclose(final.get_all_distances(mic=True),frames[-1].get_all_distances(mic=True),atol=3e-4)
result=dict(frames=len(frames),composition=dict(Counter(final.get_chemical_symbols())),thermo=stats,rdf_peaks_A=peaks,fixed_cutoff_CN=cn,sampled_min_pair_A=minimum,initial_reflection_retention=order,final_density_g_cm3=float(sum(final.get_masses())*1.6605390666/final.get_volume()),hashes={name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['equilibration.log','equilibration.lammpstrj','equilibrated_300K.data']},limitations=['Fixed CN cutoffs are diagnostic, not fitted RDF minima.','21 frames per RDF block, 0.5 ps sampling; block boundary shared.','Frame SD is fluctuation, not confidence interval.','Reflection retention is not crystalline fraction; new order is not excluded.'])
(OUT/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
