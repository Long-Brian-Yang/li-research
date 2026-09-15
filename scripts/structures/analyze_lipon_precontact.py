"""Matched2 ps restart diagnostic; geometry alone does not assign chemical bonds."""
from pathlib import Path
import json,hashlib
import numpy as np
from ase.io import read
ROOT=Path(__file__).resolve().parents[2];BASE=ROOT/'results/amorphous_review_20260915';OUT=BASE/'portfolio_supplement'
def run():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from li_diffusion_style import apply_style
 fig,ax=plt.subplots(layout='constrained');res={};hashes={}
 for tag,label,color in [('dt05','0.5 fs','#31688e'),('dt025','0.25 fs','#d73027')]:
  p=BASE/f'source/LiPON_precontact/precontact_{tag}_8676059'
  assert (p/'completed.txt').exists()
  frames=read(p/'dump.xyz',index=':');assert len(frames)==200
  t=np.array([a.info['Time']/1000 for a in frames]);np.testing.assert_allclose(t,np.arange(1,201)*.01)
  vals=[]
  for a in frames:
   s=np.array(a.get_chemical_symbols());assert len(a)==124 and s[75]==s[107]=='N'
   d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf)
   vals.append([d[75,107],d[np.ix_(s=='N',s=='N')].min()])
  vals=np.array(vals);hit=np.flatnonzero(vals[:,0]<1.6)
  th=np.loadtxt(p/'thermo.out');assert th.shape==(200,18) and np.isfinite(th).all()
  res[tag]={'pair76_108_min_A':float(vals[:,0].min()),'pair76_108_max_A':float(vals[:,0].max()),'fraction_samples_pair_below1point6':float(len(hit)/len(t)),'first_sample_below1point6_ps':float(t[hit[0]]) if len(hit) else None,'final_pair_A':float(vals[-1,0]),'mean_T_K':float(th[:,0].mean())}
  np.savetxt(OUT/f'LiPON_{tag}_NN.csv',np.c_[t,vals],delimiter=',',header='elapsed_ps,pair76_108_A,minimum_all_NN_A',comments='')
  for q in p.iterdir():
   if q.is_file():hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
  ax.plot(t,vals[:,0],color=color,label=label)
 ax.axhline(1.6,color='gray',ls='--',label='Diagnostic threshold')
 ax.set(title='LiPON: same precontact start',xlabel='Restart elapsed time (ps)',ylabel='N76–N108 distance (Å)');ax.legend()
 apply_style(fig)
 for ext in ['png','pdf','svg']:fig.savefig(OUT/f'LiPON_timestep_NN.{ext}',dpi=220)
 svg=OUT/'LiPON_timestep_NN.svg';svg.write_text('\n'.join(v.rstrip() for v in svg.read_text().splitlines())+'\n');plt.close(fig)
 (OUT/'LiPON_diagnostic.json').write_text(json.dumps({'results':res,'source_hashes':hashes},indent=2)+'\n');print(json.dumps(res,indent=2))
if __name__=='__main__':run()
