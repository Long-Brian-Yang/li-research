"""Conditional extrapolation and geometric LSZC connectivity; no source mutation."""
from pathlib import Path
import json,csv,hashlib
import numpy as np
from scipy.stats import linregress
from ase.io import read,write
from complete_amorphous_comparisons import sigma_mscm
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'portfolio_supplement'
def extrapolate(t,d):
 r=linregress(1/np.asarray(t),np.log(d))
 return -r.slope*8.617333262145e-5,float(np.exp(r.intercept+r.slope/300)),r.rvalue**2
def run():
 OUT.mkdir(exist_ok=True,parents=True)
 source=BASE/'final_comparisons/LZOC_fit_table.csv'
 a=np.loadtxt(source,delimiter=',',skiprows=1);rows=[]
 initial=read(BASE/'source/LZOC_NHC80/aimd_aligned_340K_8675022/production/model.xyz')
 for lo,hi in [(5,20),(10,30),(10,40)]:
  v=a[(a[:,0]==1)&(a[:,2]==lo)&(a[:,3]==hi)]
  v=v[np.argsort(v[:,1])];assert np.array_equal(v[:,1],[340,360,380])
  ea,d,r2=extrapolate(v[:,1],v[:,4]);sig=sigma_mscm(d,42,initial.get_volume(),300)
  rows.append([lo,hi,ea,r2,d,sig,sig/43.3,sig/2.42])
 np.savetxt(OUT/'LZOC_300K_conditional.csv',rows,delimiter=',',header='lo_ps,hi_ps,Ea_app_eV,Arrhenius_R2,D300_extrap_cm2_s,sigma300_extrap_mS_cm,ratio_theory300K,ratio_experiment298point15K',comments='')
 p=BASE/'source/LSZC_npt400/dump.xyz';frames=read(p,index=':')[-100:];counts=[];links=[]
 for k,b in enumerate(frames):
  s=np.array(b.get_chemical_symbols());dist=b.get_all_distances(mic=True)
  zo=dist[np.ix_(s=='Zr',s=='O')]<2.6;zc=dist[np.ix_(s=='Zr',s=='Cl')]<3.2
  so=dist[np.ix_(s=='S',s=='O')]<2.0
  assert np.all(so.sum(1)==4)
  # Number of unique Zr neighbours of each sulfate (through any of its O).
  sz=(so.astype(int)@zo.T.astype(int))>0
  counts.extend(np.c_[zo.sum(1),zc.sum(1),zo.sum(1)+zc.sum(1)].tolist())
  links.append([10.1+.1*k,float((sz.sum(1)>=2).mean()),float(sz.sum(1).mean()),float((sz.sum(1)==0).mean()),float((zo.sum(0)>=2).mean())])
 counts=np.array(counts);hist=[]
 for i,name in enumerate(['Zr_O','Zr_Cl','Zr_total_O_Cl']):
  n=np.bincount(counts[:,i]);hist.extend([[name,j,int(c),float(c/n.sum())] for j,c in enumerate(n)])
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from li_diffusion_style import apply_style
 plt.rcParams.update({'svg.fonttype':'none','pdf.fonttype':42})
 fig,axs=plt.subplots(1,3,layout='constrained')
 for i,(ax,title) in enumerate(zip(axs,['Zr–O (<2.6 Å)','Zr–Cl (<3.2 Å)','Zr: O + Cl neighbours'])):
  n=np.bincount(counts[:,i]);ax.plot(np.arange(len(n)),n/n.sum(),'o-',color='#31688e')
  ax.set(title=title,xlabel='Neighbour count',ylabel='Atom–frame fraction',ylim=(0,1),xticks=np.arange(len(n)))
 apply_style(fig)
 for ext in ['png','pdf','svg']:fig.savefig(OUT/f'LSZC_coordination.{ext}',dpi=220)
 svg=OUT/'LSZC_coordination.svg';svg.write_text('\n'.join(v.rstrip() for v in svg.read_text().splitlines())+'\n');plt.close(fig)
 with (OUT/'LSZC_coordination_distribution.csv').open('w') as f:
  w=csv.writer(f,lineterminator='\n');w.writerow(['pair','neighbours','atom_frames','fraction']);w.writerows(hist)
 np.savetxt(OUT/'LSZC_sulfate_connectivity.csv',links,delimiter=',',header='time_ps,sulfate_fraction_linking_2plus_Zr,mean_Zr_per_sulfate,sulfate_fraction_no_Zr,O_fraction_linking_2plus_Zr',comments='')
 # GPUMD-ready copy retains snapshot positions/velocities; add masses only.
 src=BASE/'LiPON/contact_snapshots/melt_frame021.xyz';b=read(src)
 assert len(b)==124 and 'vel' in b.arrays
 b.new_array('mass',b.get_masses());b.info={}
 write(OUT/'LiPON_precontact_input.xyz',b,format='extxyz',columns=['symbols','positions','mass','vel'])
 result={'LZOC':rows,'LZOC_volume_A3':initial.get_volume(),'LSZC_mean_CN':counts.mean(0).tolist(),'LSZC_connectivity_means':np.mean(links,axis=0)[1:].tolist(),'hashes':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [source,p,src]}}
 (OUT/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
