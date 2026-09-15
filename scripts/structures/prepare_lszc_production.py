"""Prepare requested LSZC production; 350 K remains exploratory."""
import json, hashlib
import numpy as np
from ase.io import read, write
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
out=ROOT/'materials/candidates/LSZC/production300_inputs'
out.mkdir(exist_ok=True)
info={}
for T,mode in [(320,'nvt'),(350,'npt')]:
    source=ROOT/f'results/amorphous_review_20260915/source/LSZC_split50/split50_{T}K_{mode}_8677026'
    a=read(source/'restart.xyz');assert len(a)==272
    vel=a.arrays['vel'].copy();frac=a.get_scaled_positions(wrap=False).copy()
    th=np.loadtxt(source/'thermo.out');assert th.shape==(1000,18) and np.isfinite(th).all()
    volume=a.get_volume()
    if T==350:
        volume=float(np.linalg.det(th[-500:,9:].reshape(-1,3,3)).mean())
        a.set_cell(a.cell*(volume/a.get_volume())**(1/3),scale_atoms=True)
        np.testing.assert_allclose(a.get_scaled_positions(wrap=False),frac)
    write(out/f'{T}K.xyz',a,format='extxyz',columns=['symbols','positions','mass','vel'])
    b=read(out/f'{T}K.xyz');np.testing.assert_allclose(b.arrays['vel'],vel,atol=1e-8)
    np.testing.assert_allclose(b.get_volume(),volume,rtol=1e-8)
    info[str(T)]={'volume_A3':volume,'input_sha256':hashlib.sha256((out/f'{T}K.xyz').read_bytes()).hexdigest(),
      'source_hashes':{n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in ['restart.xyz','thermo.out']},
      'method':'320 K: preserve completed NVT cell; 350 K: mean volume of additional NPT 25–50 ps, then 50 ps NVT before production. Density drift unresolved; exploratory fixed-volume transport.'}
(out/'provenance.json').write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps(info,indent=2))
