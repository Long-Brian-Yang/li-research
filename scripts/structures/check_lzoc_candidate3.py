"""Read-only-source diagnostic; outputs JSON and RDF arrays, not a crystallinity fraction.

Run with ASE 3.26 and NumPy. RDF uses ASE triclinic minimum-image distances,
explicit shell volumes and finite-population normalization, excluding self pairs.
Reciprocal intensities compare the same initial-cell hkl values, following the
changing cell: I(h)=|sum exp(2 pi i h.s)|²/N. No scattering-factor weighting.
"""
from pathlib import Path
from collections import Counter
import hashlib
import itertools
import json
import numpy as np
from ase.io import read

ROOT = Path(__file__).resolve().parents[2]
P = ROOT/'materials/candidates/LZOC/archive/completed_reference_trials/source_3'
OUT = P.parent/'candidate3_check'
OUT.mkdir(exist_ok=True)
expected = Counter(Li=42, Zr=24, O=12, Cl=114)
reference_mapping = None
for block in (P/'candidate.lammpstrj').read_text().split('ITEM: TIMESTEP\n')[1:]:
    lines = block.splitlines()
    offset = next(i for i, line in enumerate(lines) if line.startswith('ITEM: ATOMS'))
    records = [line.split() for line in lines[offset+1:]]
    assert len(records) == 192
    mapping = {int(row[0]): (int(row[1]), row[2]) for row in records}
    assert set(mapping) == set(range(1,193))
    if reference_mapping is None:
        reference_mapping = mapping
    assert mapping == reference_mapping
frames = read(P/'candidate.lammpstrj', format='lammps-dump-text', index=':')
steps = np.array([a.info['timestep'] for a in frames])
assert np.array_equal(steps, np.arange(0,110001,100))
for a in frames:
    assert Counter(a.get_chemical_symbols()) == expected
    assert np.isfinite(a.positions).all() and a.get_volume() > 0
late = [a for a in frames if 100000 <= a.info['timestep'] <=110000][::5]
initial = read(P/'initial_minimized.data',format='lammps-data',atom_style='atomic',Z_of_type={1:3,2:40,3:8,4:17})
assert initial.get_chemical_symbols() == late[0].get_chemical_symbols()
rows = {}
for line in (P/'candidate.log').read_text().split('undump traj')[0].splitlines():
    try:
        v = list(map(float,line.split()))
    except ValueError:
        continue
    if len(v)==14 and v[2]==192 and 45<=v[1]<=55:
        rows[v[1]]=v
thermo = np.array(sorted(rows.values(),key=lambda v:v[1]))
blocks = []
for start in range(45,55):
    b=thermo[(thermo[:,1]>=start)&(thermo[:,1]<start+1)]
    blocks.append(dict(start_ps=start,**{name:float(b[:,i].mean()) for name,i in [('T_K',3),('PE_eV',4),('volume_A3',8),('density_g_cm3',9)]}))
end=thermo[thermo[:,1]>=50]
stats={name:dict(mean=float(end[:,i].mean()),sd=float(end[:,i].std(ddof=1)),slope_per_ps=float(np.polyfit(end[:,1],end[:,i],1)[0])) for name,i in [('T_K',3),('PE_eV',4),('volume_A3',8),('density_g_cm3',9)]}
edges=np.linspace(0,4.5,91)
shell=4*np.pi/3*np.diff(edges**3)
pairs=[('Li','Cl'),('Li','O'),('Zr','Cl'),('Zr','O'),('Cl','Cl')]
rdfs={}; minima=[]
for label,group in [('initial',[initial]),('late',late)]:
    accum={f'{x}-{y}':[] for x,y in pairs}
    for a in group:
        height=1/np.linalg.norm(a.cell.reciprocal(),axis=1)
        assert min(height)>2*edges[-1]
        dm=a.get_all_distances(mic=True); np.fill_diagonal(dm,np.inf)
        if label=='late': minima.append(float(dm.min()))
        symbols=np.array(a.get_chemical_symbols())
        for x,y in pairs:
            nx=(symbols==x).sum();ny=(symbols==y).sum()
            counts=np.histogram(dm[np.ix_(symbols==x,symbols==y)].ravel(),edges)[0]
            norm=nx*(ny-(x==y))*shell/a.get_volume()
            accum[f'{x}-{y}'].append(counts/norm)
    rdfs[label]={k:np.mean(v,axis=0) for k,v in accum.items()}
columns=[(edges[:-1]+edges[1:])/2];names=['r_A']
for label,values in rdfs.items():
    for pair,v in values.items(): columns.append(v);names.append(label+'_'+pair)
np.savetxt(OUT/'rdf.csv',np.column_stack(columns),delimiter=',',header=','.join(names),comments='')
h=np.array([v for v in itertools.product(range(-8,9),repeat=3) if v!=(0,0,0) and next(x for x in v if x)>0])
q=2*np.pi*np.linalg.norm(h@initial.cell.reciprocal(),axis=1)
h=h[(q>=1)&(q<=5)]
order={}
for element in ['Cl','Zr']:
    mask=np.array(initial.get_chemical_symbols())==element
    def intensity(a,hh):
        phase=2*np.pi*a.get_scaled_positions()[mask]@hh.T
        return np.abs(np.exp(1j*phase).sum(axis=0))**2/mask.sum()
    ref=intensity(initial,h); top=np.argsort(ref)[-10:][::-1]
    values=np.array([intensity(a,h[top]) for a in late])
    order[element]=dict(hkl=h[top].tolist(),initial=ref[top].tolist(),late_mean=values.mean(axis=0).tolist(),ratio_of_sums=float(values.mean(axis=0).sum()/ref[top].sum()))
result=dict(frame_count=len(frames),steps=[int(steps[0]),int(steps[-1])],late_structure_frames=len(late),late_structure_window_ps=[50,55],counts=dict(expected),late_min_pair_A=min(minima),thermo_1ps_blocks=blocks,thermo_last5ps=stats,initial_peak_retention=order,sha256={name:hashlib.sha256((P/name).read_bytes()).hexdigest() for name in ['candidate.lammpstrj','candidate.log','initial_minimized.data']},limitations=['Only 192 atoms and 5 ps late structure sampling.','RDF rmax 4.5 A cannot establish absence of long-range order.','Initial peak retention is an unweighted diagnostic, not crystalline fraction.','Frame fluctuations are correlated; SD is not standard error.'])
(OUT/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
