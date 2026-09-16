"""LSZC endpoint analysis using the same trajectories as the primary 4T figure.

Figure contract: full MSD establishes transport shape; conductivity points compare
like units with separate experimental and tuned-MACE references. No two-point Ea
is promoted as a validated activation energy. Static quantitative grids, Python,
PNG/PDF/SVG and CSV source data, no smoothing or hidden trajectory cropping.
"""
from pathlib import Path
from collections import Counter
import hashlib, json
import numpy as np
from ase.io import read, iread
from analyze_lzoc_production import unwrap, window_msd, fit_msd
from complete_amorphous_comparisons import sigma_mscm
from finish_amorphous_analysis import frame_metrics, block_slopes

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'LSZC_endpoints'; OUT.mkdir(exist_ok=True)
FIG=ROOT/'docs/materials/figures'
WINDOWS=[(20,80),(20,100),(20,150),(40,150),(50,200)]
PAIRS=[('S','O',2.),('Zr','O',2.6),('Zr','Cl',3.2),('Li','O',2.7)]
TEMPERATURES=(320,330,340,350)
PRIMARY_SERIES={320:2,330:2,340:2,350:1}

def run():
 records=[]; hashes={}
 for T in TEMPERATURES:
  repeat=PRIMARY_SERIES[T]
  p=BASE/f'source/LSZC_matched4t/R{repeat}_{T}K/production'
  a=read(p/'model.xyz'); s=np.array(a.get_chemical_symbols())
  assert Counter(s)==Counter(Li=32,Zr=32,Cl=128,S=16,O=64)
  frames=list(iread(p/'dump.xyz')); assert len(frames)==3000
  np.testing.assert_allclose([f.info['Time']/1000 for f in frames],np.arange(1,3001)*.1)
  assert all(np.array_equal(s,f.get_chemical_symbols()) and np.allclose(a.cell,f.cell,atol=1e-7,rtol=0) for f in frames)
  x=np.array([a.positions]+[f.positions for f in frames]); assert np.isfinite(x).all()
  xu=unwrap(x,a.cell.array); xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
  t=np.arange(len(x))*.1; li=xu[:,s=='Li']; els=['Li','Zr','Cl','S','O']
  msd={el:window_msd(xu[:,s==el]) for el in els}
  for k in (1,200,800,1500,2999):
   np.testing.assert_allclose(msd['Li'][k],np.mean(np.sum((li[k:]-li[:-k])**2,2)),atol=1e-8)
  np.savetxt(OUT/f'{T}K_MSD.csv',np.c_[t,*[msd[e] for e in els]],delimiter=',',header='lag_ps,'+','.join(els),comments='')
  fits=[fit_msd(t,msd['Li'],*w) for w in WINDOWS]
  # Retain common 20–80 ps diagnostic for continuity, not an optimized Ea.
  f=fits[0]; sig=sigma_mscm(f['D_cm2_s'],32,a.get_volume(),T) if f['D_cm2_s']>0 else None
  th=np.loadtxt(p/'thermo.out'); assert th.shape==(6000,18) and np.isfinite(th).all()
  edges=np.arange(0,5.0001,.05); gs=[]; cs=[]; so4=[]; mob=[]
  for k in range(1000,3001,10):
   atom=a.copy(); atom.positions=x[k]
   g,c,_=frame_metrics(atom,PAIRS,edges); gs.append(g);cs.append(c)
   d=atom.get_all_distances(mic=True)
   so4.append(float(((d[np.ix_(s=='S',s=='O')]<2).sum(1)==4).mean()))
   if k+100<len(x):
    cn=(d[np.ix_(s=='Li',s=='O')]<2.7).sum(1)
    disp=((li[k+100]-li[k])**2).sum(1)
    mob.extend(zip(cn.tolist(),disp.tolist()))
  gs=np.mean(gs,axis=0); cn=np.mean(cs,axis=0)
  np.savetxt(OUT/f'{T}K_RDF.csv',np.c_[(edges[:-1]+edges[1:])/2,gs.T],delimiter=',',header='r_A,'+','.join(u+'-'+v for u,v,_ in PAIRS),comments='')
  mob=np.array(mob); mrows=[]
  for n in np.unique(mob[:,0]):
   z=mob[mob[:,0]==n,1];mrows.append([n,len(z),z.mean()])
  np.savetxt(OUT/f'{T}K_mobility.csv',mrows,delimiter=',',header='Li_O_CN,correlated_observations,mean_displacement_10ps_A2',comments='')
  rec=dict(T=T,repeat=repeat,fit=f,windows=fits,sigma_mS_cm=sig,CN=cn.tolist(),SO4_fraction=float(np.mean(so4)),
   mean_T=float(th[:,0].mean()),PE_change_meV_atom=float((th[-1000:,2].mean()-th[:1000,2].mean())/272*1000),
   density=float(a.get_masses().sum()*1.6605390666/a.get_volume()),
   block_D=block_slopes(li,.1,3,(20,40)).tolist(),MSD300=float(msd['Li'][-1]),mobility=mrows)
  records.append(rec)
  for name in ('model.xyz','dump.xyz','thermo.out','run.in'):
   q=p/name;hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
  print(json.dumps(rec),flush=True)
 (OUT/'analysis.json').write_text(json.dumps(dict(records=records,hashes=hashes,method='Same representative trajectories as the four-temperature transport figure (320/330/340 K R2; 350 K R1). Common 20–80 ps diagnostic; system mass COM corrected all-origin MSD. RDF 100–300 ps every 1 ps, 0.05 A bins. Li–O origin CN / 10 ps displacement; correlated observations, no confidence interval. Mobility figure retains the 320/350 K endpoint comparison.'),indent=2)+'\n')

def build_rdf_figure(rdf_by_temperature):
 import matplotlib.pyplot as plt
 colors={320:'#5e3c99',330:'#31688e',340:'#35b779',350:'#d73027'}
 fig,axes=plt.subplots(2,2,figsize=(12,9.3),layout='constrained')
 for T in TEMPERATURES:
  data=rdf_by_temperature[T]
  for j,ax in enumerate(axes.flat):
   ax.plot(data[:,0],data[:,j+1],color=colors[T],label=f'{T} K')
 for ax,(u,v,_) in zip(axes.flat,PAIRS):
  ax.set(title=f'{u}–{v}',xlabel='r (Å)',ylabel='g(r)',xlim=(1,5));ax.legend()
 return fig

def plot():
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from li_diffusion_style import apply_style
 plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42})
 FIG.mkdir(parents=True,exist_ok=True)
 def save(fig,name):
  apply_style(fig)
  for ext in ('png','pdf','svg'):
   path=FIG/f'{name}.{ext}'
   fig.savefig(path,dpi=200,bbox_inches='tight')
   if ext=='svg':
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
  plt.close(fig)
 colors={320:'#5e3c99',330:'#31688e',340:'#35b779',350:'#d73027'}
 records=json.loads((OUT/'analysis.json').read_text())['records']
 np.savetxt(OUT/'summary.csv',[[r['T'],r['fit']['D_cm2_s'],r['sigma_mS_cm'],r['fit']['R2'],r['fit']['alpha'],r['density'],*r['CN']] for r in records],delimiter=',',header='T_K,D_app_cm2_s,sigma_conditional_mS_cm,R2,alpha,density_g_cm3,CN_SO,CN_ZrO,CN_ZrCl,CN_LiO',comments='')
 rdf_by_temperature={T:np.loadtxt(OUT/f'{T}K_RDF.csv',delimiter=',',skiprows=1) for T in TEMPERATURES}
 fig=build_rdf_figure(rdf_by_temperature)
 save(fig,'19_LSZC_partial_RDF')
 fig,axes=plt.subplots(1,2,layout='constrained')
 for T in (320,350):
  c=colors[T]
  m=np.loadtxt(OUT/f'{T}K_mobility.csv',delimiter=',',skiprows=1)
  common=m[:,1]>=100
  axes[0].plot(m[common,0],m[common,2],'o-',color=c,label=f'{T} K')
  axes[0].plot(m[~common,0],m[~common,2],'o',mfc='none',color=c)
  axes[1].plot(m[:,0],m[:,1],'o-',color=c,label=f'{T} K')
 axes[0].set(title='Li–O coordination and mobility',xlabel='Li–O coordination number',ylabel='10 ps displacement (Å²)')
 axes[1].set(title='Sampling by coordination',xlabel='Li–O coordination number',ylabel='Li–origin observations',yscale='log')
 for ax in axes:ax.legend()
 save(fig,'20_LSZC_coordination_mobility')

if __name__=='__main__':
 run();plot()
