"""Recompose existing source tables for the EN/JA overview; no new MD/refits.

Contract: eleven evidence-bearing figures, at most two columns, fixed document
width. Keep model/reference mismatches and sparse data visible. PNG/PDF/SVG
with editable text; source SHA256 and export inventory accompany the figures.
"""
from pathlib import Path
import hashlib
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'overview_figures'
P=BASE/'paper_alignment';F=BASE/'final_comparisons';L=BASE/'Li3PS4_transport'
OLD=ROOT/'results/LZOC/legacy_comparison_20260915'
BLUE='#31688e';RED='#d73027';GREEN='#35a77b';GRAY='#727272';PURPLE='#654394'
HASHES={};EXPORTS=[]

def load(path):
    HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    a=np.loadtxt(path,delimiter=',',skiprows=1)
    assert a.ndim==2 and np.isfinite(a[:,:-1]).all(),path
    return a

def js(path):
    HASHES[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
    return json.loads(path.read_text())

def grid(rows=1,cols=2):
    return plt.subplots(rows,cols,figsize=(12,4.65*rows),layout='constrained',squeeze=False)

def finish(fig,name):
    for i,ax in enumerate(fig.axes):
        ax.text(-.13,1.045,chr(97+i),transform=ax.transAxes,fontweight='bold',fontsize=16)
        ax.grid(alpha=.16);ax.set_axisbelow(True)
        if ax.get_legend():ax.legend(frameon=False,fontsize=11.5)
    fig.canvas.draw()
    for ext in ('png','pdf','svg'):
        path=OUT/f'{name}.{ext}';fig.savefig(path,dpi=220)
        if ext=='svg':path.write_text('\n'.join(s.rstrip() for s in path.read_text().splitlines())+'\n')
    EXPORTS.append(name);plt.close(fig)

def lzoc():
    fig,aa=grid(2);axes=aa.ravel()
    for ax,T in zip(axes,[340,360,380]):
        for model,c,ls in [('MTTK_0.5fs',BLUE,'-'),('NHC_2fs',RED,'--')]:
            a=load(F/f'LZOC_{T}K_{model}_MSD.csv');a=a[a[:,0]<=40]
            ax.plot(a[:,0],a[:,1],color=c,ls=ls,label=model.replace('_',' '))
        ax.set(title=f'{T} K',xlabel='Lag time (ps)',ylabel='Li MSD (Å²)',ylim=(0,5.7));ax.legend()
    a=load(P/'LZOC_Table4_comparison.csv');ax=axes[3]
    ax.errorbar(a[:,0],a[:,1],yerr=a[:,2],fmt='ko-',capsize=4,label='AIMD tracer D*')
    for j,c,ls,lab in [(4,BLUE,'-','NEP: MTTK 0.5 fs'),(5,RED,'--','NEP: NHC 2 fs')]:
        ax.plot(a[:,0],a[:,j],'o',color=c,ls=ls,label=lab)
    ax.set(title='AIMD comparison',xlabel='Temperature (K)',ylabel='D (cm²/s)',yscale='log',xticks=a[:,0]);ax.legend()
    finish(fig,'01_LZOC_transport')

def lszc():
    a=load(P/'LSZC400_MSD.csv');a=a[a[:,0]<=100];summary=js(P/'LSZC400_summary.json')
    fig,aa=grid(2);axes=aa.ravel();fit=summary['fits'][2]
    axes[0].plot(a[:,0],a[:,1],color=BLUE,label='Li: 400 K')
    x=np.array([20,80]);axes[0].plot(x,fit['intercept_A2']+6e4*fit['D_cm2_s']*x,'k--',label='20–80 ps fit')
    axes[0].set(title='Lithium motion',xlabel='Lag time (ps)',ylabel='MSD (Å²)');axes[0].legend()
    for j,el,c,ls in [(2,'Zr',BLUE,'--'),(3,'Cl',GREEN,'-'),(4,'S',RED,':'),(5,'O',PURPLE,'-.')]:
        axes[1].plot(a[:,0],a[:,j],label=el,color=c,ls=ls)
    axes[1].set(title='Framework motion',xlabel='Lag time (ps)',ylabel='MSD (Å²)');axes[1].legend()
    t=load(P/'LSZC400_thermo.csv')
    axes[2].plot(t[:,0],t[:,2],color=BLUE,alpha=.3,lw=.7,label='Raw PE / atom')
    blocks=t.reshape(40,50,4).mean(axis=1)
    axes[2].plot(blocks[:,0],blocks[:,2],color='black',label='5 ps means')
    axes[2].set(title='Residual energy relaxation',xlabel='Time (ps)',ylabel='Potential energy (eV/atom)');axes[2].legend()
    b=load(P/'LSZC400_blocks.csv');axes[3].plot(b[:,0],b[:,1]*1e6,'o-',color=BLUE)
    axes[3].set(title='Four 50 ps blocks',xlabel='Block centre (ps)',ylabel='D (10⁻⁶ cm²/s)',ylim=(0,2.15))
    finish(fig,'02_LSZC_transport')
    mob=load(P/'LSZC400_conditioned_mobility.csv');z=mob[mob[:,0]==10]
    fig,aa=grid();ax=aa[0];dense=z[:,2]>=50
    ax[0].plot(z[dense,1],z[dense,3],'o-',color=BLUE,label='At least 50 observations')
    ax[0].plot(z[~dense,1],z[~dense,3],'o',mfc='white',mec=GRAY,ms=8,label='Fewer than 50 observations')
    ax[0].set(title='Mobility vs starting Li–O CN',xlabel='Li–O neighbours (<2.7 Å)',ylabel='10 ps mean |Δr|² (Å²)',xticks=z[:,1]);ax[0].legend()
    ax[1].bar(z[:,1],z[:,2],color=[BLUE if d else '#cccccc' for d in dense])
    for row in z:ax[1].text(row[1],row[2]+60,str(int(row[2])),ha='center',fontsize=11)
    ax[1].set(title='Sampling behind each point',xlabel='Li–O neighbours (<2.7 Å)',ylabel='Li–origin observations',xticks=z[:,1],ylim=(0,2900))
    finish(fig,'03_LSZC_mobility')
    fig,aa=grid()
    for a,label,c,ls in [(load(P/'LSZC400_early_RDF.csv'),'Early',GRAY,'--'),(load(P/'LSZC400_late_RDF.csv'),'Late',BLUE,'-')]:
        for ax,j in zip(aa[0],[3,4]):ax.plot(a[:,0],a[:,j],label=label,color=c,ls=ls)
    for ax,title,ref in zip(aa[0],['Zr–O','Zr–Cl'],[2.23,2.45]):
        ax.axvline(ref,color=RED,ls=':',label=f'EXAFS distance: {ref} Å')
        ax.set(title=title,xlabel='r (Å)',ylabel='g(r)',xlim=(1.3,4));ax.legend()
    finish(fig,'04_LSZC_structure')

def lips():
    fig,aa=grid(2);summary=js(L/'analysis.json')
    for ax,T,c in zip(aa.ravel(),[300,500,700,900],[PURPLE,BLUE,GREEN,RED]):
        a=load(L/f'{T}K_MSD.csv');a=a[a[:,0]<=100]
        ax.plot(a[:,0],a[:,1],color=c,label='Li MSD')
        fit=summary['temperatures'][str(T)]['fits'][2] if 'temperatures' in summary else summary['results'][str(T)]['fits'][2]
        x=np.array([20,80]);ax.plot(x,fit['intercept_A2']+6e4*fit['D_cm2_s']*x,'k--',label='20–80 ps fit')
        ax.set(title=f'{T} K'+(' — plateau' if T==300 else ''),xlabel='Lag time (ps)',ylabel='Li MSD (Å²)');ax.legend()
    finish(fig,'05_LPS_MSD')
    fig,aa=grid();ax=aa[0];a=load(L/'reference_comparison.csv')
    for j,c,ls,lab in [(1,BLUE,'-','NEP89: apparent D'),(2,GRAY,'--','Chen 2025: glass MD')]:
        ax[0].plot(a[:,0],a[:,j],'o',color=c,ls=ls,label=lab)
    ax[0].set(title='Same-temperature reference',xlabel='Temperature (K)',ylabel='D (cm²/s)',yscale='log');ax[0].legend()
    endpoints=[]
    for T in [300,500,700,900]:
        a=load(L/f'{T}K_MSD.csv');endpoints.append(a[np.isclose(a[:,0],80)][0,2:4])
    endpoints=np.array(endpoints)
    for j,el,c,ls in [(0,'P',BLUE,'--'),(1,'S',RED,'-')]:ax[1].plot([300,500,700,900],endpoints[:,j],'o',color=c,ls=ls,label=el)
    ax[1].set(title='Framework motion at 80 ps lag',xlabel='Temperature (K)',ylabel='MSD (Å²)',yscale='log');ax[1].legend()
    finish(fig,'06_LPS_reference')
    fig,aa=grid();ax=aa[0]
    a=load(F/'Li3PS4_late_RDF.csv');b=load(F/'Chen2025_Fig._1e.csv')
    ax[0].plot(a[:,0],a[:,2],color=BLUE,label='NEP: final 10 ps hold')
    ax[0].plot(b[:,0],b[:,2],color=RED,ls='--',label='Chen 2025: glass')
    ax[0].set(title='Li–S RDF',xlabel='r (Å)',ylabel='g(r)',xlim=(0,5));ax[0].legend()
    a=load(F/'Li3PS4_angles.csv');b=load(F/'Chen2025_Fig._1f.csv')
    for x,y,c,ls,lab in [(a[:,0],a[:,1],BLUE,'-','NEP: final 10 ps hold'),(b[:,0],b[:,2],RED,'--','Chen 2025: glass')]:
        y=y/np.trapezoid(y,x);ax[1].plot(x,y,color=c,ls=ls,label=lab)
    ax[1].set(title='S–P–S angles',xlabel='Angle (°)',ylabel='Probability density (degree⁻¹)',xlim=(60,160));ax[1].legend()
    finish(fig,'07_LPS_structure')

def lipon():
    fig,aa=grid();ax=aa[0];a=load(F/'LiPON_NN_release.csv')
    ax[0].plot(a[:,0],a[:,1],color=BLUE,label='250 K release')
    ax[0].set(title='Pressure-release diagnostic',xlabel='Release time (ps)',ylabel='Minimum N–N distance (Å)')
    for name,c,ls,lab in [('dt05',BLUE,'-','0.5 fs'),('dt025',RED,'--','0.25 fs')]:
        a=load(BASE/f'portfolio_supplement/LiPON_{name}_NN.csv');ax[1].plot(a[:,0],a[:,1],label=lab,color=c,ls=ls,lw=1.5)
    ax[1].set(title='2000 K: paired timestep test',xlabel='Restart elapsed time (ps)',ylabel='N76–N108 distance (Å)')
    for a in ax:a.axhline(1.6,color=GRAY,ls=':',label='Screening cutoff');a.set_ylim(1.15,1.75);a.legend()
    finish(fig,'08_LiPON_contacts')

def legacy():
    fig,aa=grid();ax=aa[0];a=load(OLD/'timing.csv')
    for j,m,c,ls in [(1,'MACE / LAMMPS',BLUE,'-'),(2,'NEP89 / GPUMD',RED,'--')]:
        ax[0].plot(a[:,0],a[:,j]/60,'o',color=c,ls=ls,label=m)
        d=load(OLD/f'{"MACE" if j==1 else "NEP89"}_600K_equilibration_thermo.csv')
        ax[1].plot(d[:,0],d[:,6],color=c,ls=ls,lw=1.4,label=m)
    ax[0].set(title='Four-temperature job runtimes',xlabel='Temperature (K)',ylabel='Runtime (min)',yscale='log');ax[0].legend()
    ax[1].axhline(1.913855,color=GRAY,ls=':',label='Common 300 K input')
    ax[1].set(title='600 K: NPT density',xlabel='Time (ps)',ylabel='Density (g/cm³)');ax[1].legend()
    finish(fig,'09_legacy_cost_density')
    fig,aa=grid(2)
    for ax,T in zip(aa.ravel(),[700,800,900]):
        for m,c,ls in [('MACE',BLUE,'-'),('NEP89',RED,'--')]:
            a=load(P/f'legacy_{m}_{T}K_MSD.csv');a=a[a[:,0]<=100];ax.plot(a[:,0],a[:,1],color=c,ls=ls,label=m)
        ax.set(title=f'{T} K: Li',xlabel='Lag time (ps)',ylabel='MSD (Å²)',ylim=(0,430));ax.legend()
    ax=aa[1,1]
    for m,ls in [('MACE','-'),('NEP89','--')]:
        a=load(P/f'legacy_{m}_900K_MSD.csv');a=a[a[:,0]<=100]
        for j,el,c in [(2,'Zr',BLUE),(3,'O',PURPLE),(4,'Cl',GREEN)]:ax.plot(a[:,0],a[:,j],color=c,ls=ls,label=f'{m}: {el}')
    ax.set(title='900 K: framework',xlabel='Lag time (ps)',ylabel='MSD (Å²)');ax.legend(ncol=2,fontsize=10)
    finish(fig,'10_legacy_motion')
    fig,aa=grid(2)
    for m,c,ls in [('MACE',BLUE,'-'),('NEP89',RED,'--')]:
        a=load(P/f'legacy_{m}_900K_RDF.csv')
        for j,ax in enumerate(aa.ravel(),1):ax.plot(a[:,0],a[:,j],color=c,ls=ls,label=m)
    for ax,title in zip(aa.ravel(),['Li–Cl','Li–O','Zr–Cl','Zr–O']):
        ax.set(title=f'900 K: {title}',xlabel='r (Å)',ylabel='g(r)');ax.legend()
    finish(fig,'11_legacy_structure')

def main():
    OUT.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.titlesize':16,'axes.labelsize':14,'xtick.labelsize':12,'ytick.labelsize':12,'axes.linewidth':1.5,'lines.linewidth':2.5,'legend.frameon':False,'svg.fonttype':'none','pdf.fonttype':42})
    lzoc();lszc();lips();lipon();legacy()
    assert len(EXPORTS)==11
    (OUT/'provenance.json').write_text(json.dumps({'sources_sha256':HASHES,'figures':EXPORTS,'operation':'Presentation only: original CSV ordinates retained; no refits. Angle PDFs normalized to unit area; 5 ps energy means and framework80 endpoints as labelled.','size_inches':[12,4.65],'rows':'1 or 2','font_pt':{'title':16,'axis':14,'ticks':12,'legend':11.5}},indent=2)+'\n')
    print('Created',len(EXPORTS),'figure families from',len(HASHES),'sources')

if __name__=='__main__':main()
