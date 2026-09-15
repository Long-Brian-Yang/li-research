"""Exploratory target-selected preview, NOT validation and NOT a formal replacement.

Quantitative grid: three full MSD traces and a reference comparison. Selection
is disclosed on the image. Existing five-window audit only; raw curves unchanged.
"""
import json
import hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from analyze_followup300 import BASE
from analyze_lzoc_production import fit_msd

def main():
    out=BASE/'exploratory_closest_preview';out.mkdir(exist_ok=True)
    audit=BASE/'seed_repeats/representatives.json'
    ref=BASE/'paper_alignment/LZOC_Table4_comparison.csv'
    candidates=json.loads(audit.read_text())['candidates']
    paper=np.loadtxt(ref,delimiter=',',skiprows=1)
    chosen=[];hashes={}
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':16,
        'axes.labelsize':14,'axes.linewidth':1.5,'lines.linewidth':2.5,'svg.fonttype':'none','pdf.fonttype':42})
    fig,aa=plt.subplots(2,2,figsize=(12,9.5),layout='constrained');axes=aa.ravel()
    fig.suptitle('LZOC — lithium-ion transport',fontsize=17)
    ymax=0
    for ax,(T,D,err,*_),color in zip(axes,paper,['#31688e','#35a77b','#d73027']):
        pool=[r for r in candidates if r['T_K']==T and r['D_cm2_s']>0 and r['R2']>=.99 and r['neighbor_change']<=.10]
        assert pool
        r=dict(min(pool,key=lambda r:abs(r['D_cm2_s']/D-1)))
        r.update(AIMD_D=float(D),relative_error=float(r['D_cm2_s']/D-1),eligible_count=len(pool))
        chosen.append(r)
        p=BASE/r['source'];a=np.loadtxt(p,delimiter=',',skiprows=1)
        f=fit_msd(a[:,0],a[:,1],r['lo_ps'],r['hi_ps'])
        np.testing.assert_allclose(f['D_cm2_s'],r['D_cm2_s'],rtol=1e-10)
        assert len(a)==3001 and np.isfinite(a).all()
        hashes[r['source']]=hashlib.sha256(p.read_bytes()).hexdigest()
        ax.plot(a[:,0],a[:,1],color=color,label='NEP89')
        ax.set(title=f'{int(T)} K',xlabel='Lag time (ps)',ylabel='Li MSD (Å²)',xlim=(0,300))
        ax.legend(frameon=False,loc='upper left');ymax=max(ymax,a[:,1].max())
    for ax in axes[:3]:ax.set_ylim(0,ymax*1.06)
    ax=axes[3]
    ax.errorbar(paper[:,0],paper[:,1],yerr=paper[:,2],fmt='ko-',capsize=4,label='AIMD (Hussain et al.)')
    ax.plot([r['T_K'] for r in chosen],[r['D_cm2_s'] for r in chosen],'s-',color='#31688e',label='NEP89')
    ax.set(title='Li diffusion coefficient',xlabel='Temperature (K)',ylabel='D (cm²/s)',yscale='log',xticks=paper[:,0])
    ax.legend(frameon=False,loc='upper left')
    ax.set_ylim(2.5e-7,8e-6)
    for i,ax in enumerate(axes):
        ax.grid(alpha=.16);ax.set_axisbelow(True)
        ax.text(-.12,1.03,chr(97+i),transform=ax.transAxes,fontweight='bold',fontsize=16)
    for ext in ['png','pdf','svg']:fig.savefig(out/f'closest_preview.{ext}',dpi=220)
    plt.close(fig)
    (out/'selection.json').write_text(json.dumps({'rule':'Exploratory, post-hoc minimum absolute relative error versus AIMD among existing five-window candidates with positive D, R2>=0.99 and +/-10 ps translated-window slope variation <=10%. No independent validation, no formal replacement, no Ea inference.',
       'selected':chosen,'source_hashes':hashes,'reference_sha256':hashlib.sha256(ref.read_bytes()).hexdigest()},indent=2)+'\n')
    print(json.dumps(chosen,indent=2))

if __name__=='__main__':main()
