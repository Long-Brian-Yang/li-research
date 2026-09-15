"""Prepare mean-volume 320 K input without changing velocities or species."""
from pathlib import Path
import json, hashlib
import numpy as np
from ase.io import read, write

ROOT=Path(__file__).resolve().parents[2]
source=ROOT/'results/amorphous_review_20260915/source/LSZC150/endpoint_npt150_320K_8676678/equil150'
out=ROOT/'materials/candidates/LSZC/followup_mean_volume_320K'
out.mkdir(exist_ok=True)
a=read(source/'restart.xyz');th=np.loadtxt(source/'thermo.out')
assert len(a)==272 and th.shape==(3000,18) and np.isfinite(th).all()
volume=float(np.linalg.det(th[-1000:,9:].reshape(-1,3,3)).mean())
old=a.get_volume();frac=a.get_scaled_positions(wrap=False).copy()
velocity=a.arrays['vel'].copy()
a.set_cell(a.cell*(volume/old)**(1/3),scale_atoms=True)
np.testing.assert_allclose(a.get_scaled_positions(wrap=False),frac)
np.testing.assert_array_equal(a.arrays['vel'],velocity)
write(out/'model.xyz',a,format='extxyz',columns=['symbols','positions','mass','vel'])
b=read(out/'model.xyz');np.testing.assert_allclose(b.get_volume(),volume,rtol=1e-8)
np.testing.assert_allclose(b.arrays['vel'],velocity,atol=1e-8)
info={'volume_A3':volume,'old_volume_A3':old,'linear_scale':(volume/old)**(1/3),'averaging_interval_ps':[100,150],
      'method':'Arithmetic mean of instantaneous volumes over last 50 ps. Isotropic affine coordinate/cell scaling; velocities retained. 50 ps NVT review precedes production.',
      'source_hashes':{n:hashlib.sha256((source/n).read_bytes()).hexdigest() for n in ['restart.xyz','thermo.out']},
      'input_sha256':hashlib.sha256((out/'model.xyz').read_bytes()).hexdigest()}
(out/'provenance.json').write_text(json.dumps(info,indent=2)+'\n')
print(json.dumps(info,indent=2))
