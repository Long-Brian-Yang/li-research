"""Replot audited legacy results; do not refit or alter trajectories.

Contract: quantitative grids distinguish workflow cost, structure and motion;
they do not rank predictive accuracy. Python, PNG/PDF/SVG, editable text.
"""
from pathlib import Path
import json
import hashlib
import shutil
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT/'results/LZOC/analysis_20260912'
OUT = ROOT/'results/LZOC/legacy_comparison_20260915'

def run():
    OUT.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.labelsize':14,
        'axes.titlesize':15,'lines.linewidth':2.2,'axes.linewidth':1.1,
        'svg.fonttype':'none','pdf.fonttype':42})
    data=json.loads((SRC/'results.json').read_text())
    hashes={}
    def read(name):
        p=SRC/name
        hashes[name]=hashlib.sha256(p.read_bytes()).hexdigest()
        shutil.copy2(p,OUT/name)
        a=np.loadtxt(p,delimiter=',',skiprows=1)
        assert np.isfinite(a).all(), name
        return a
    def save(fig,name):
        from li_diffusion_style import apply_style
        apply_style(fig)
        for ext in ['png','pdf','svg']:fig.savefig(OUT/f'{name}.{ext}',dpi=300,bbox_inches='tight')
        plt.close(fig)
    models=['MACE','NEP89']; colors=['#31688e','#d73027']; styles=['-','--']
    times=np.array([[600,14830.478,544.344],[700,18019.970,502.105],
        [800,14485.452,501.880],[900,18975.057,497.137]])
    np.savetxt(OUT/'timing.csv',times,delimiter=',',header='T_K,MACE_job_seconds,NEP_job_seconds',comments='')
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for i,m in enumerate(models):
        axes[0].plot(times[:,0],times[:,i+1]/3600,styles[i],color=colors[i],marker='o',label=m)
    axes[0].set(xlabel='Temperature (K)',ylabel='Job runtime (h)',title='Four-temperature workflow cost');axes[0].legend()
    seconds=[11395.5,366.428]
    axes[1].bar(models,np.array(seconds)/60,color=colors)
    axes[1].set(ylabel='Production runtime (min)',title='600 K: 200 ps production')
    for i,s in enumerate(seconds):axes[1].text(i,s/60+3,f'{s/60:.2f}',ha='center')
    axes[1].set_ylim(0,220)
    save(fig,'01_runtime')
    fig,axes=plt.subplots(2,3,figsize=(14,7),layout='constrained')
    for i,m in enumerate(models):
        npt=read(f'{m}_600K_equilibration_thermo.csv');p=read(f'{m}_600K_production_thermo.csv')
        for ax,x,y in [(axes[i,0],npt[:,0],npt[:,6]),(axes[i,1],p[:,0],p[:,1]),
                       (axes[i,2],p[:,0],(p[:,2]-p[:,2].mean())/192*1000)]:
            ax.plot(x,y,color=colors[i],lw=.6,alpha=.6)
            ax.set_xlabel('Time (ps)')
        axes[i,0].set(ylabel='Density (g/cm³)',title=f'{m}: NPT density',ylim=(1.15,2.2))
        axes[i,0].axhline(1.913855,c='gray',ls=':',label='300 K input');axes[i,0].legend(fontsize=10)
        axes[i,1].set(ylabel='Temperature (K)',title=f'{m}: NVT temperature',ylim=(440,760))
        axes[i,1].axhline(600,c='gray',ls=':')
        axes[i,2].set(ylabel='PE − mean PE (meV/atom)',title=f'{m}: NVT energy fluctuations',ylim=(-30,30))
    save(fig,'02_density_thermodynamics')
    fig,axes=plt.subplots(2,3,figsize=(14,7),layout='constrained')
    pairs=['Li-Cl','Li-O','Zr-Cl','Zr-O','Cl-Cl']
    cn=[]
    for i,m in enumerate(models):
        r=read(f'{m}_600K_rdf.csv')
        for j,pair in enumerate(pairs):
            axes.flat[j].plot(r[:,0],r[:,6+j],styles[i],color=colors[i],label=m)
            axes.flat[j].set(title=pair,xlabel='r (Å)',ylabel='g(r)',xlim=(0,4.5))
            for period in ['early','late']:
                v=data[f'{m}_600K']['CN'][period][pair]
                cn.append([m,pair,period,v['mean'],v['frame_sd']])
    axes.flat[0].legend()
    for i,m in enumerate(models):
        vals=[data[f'{m}_600K']['CN']['late'][p]['mean'] for p in pairs]
        axes.flat[5].plot(np.arange(5),vals,styles[i],marker='o',color=colors[i],label=m)
    axes.flat[5].set(xticks=np.arange(5),xticklabels=pairs,ylabel='Mean neighbour count',title='Late coordination');axes.flat[5].tick_params(axis='x',rotation=25)
    np.savetxt(OUT/'coordination.csv',np.array(cn,dtype=str),fmt='%s',delimiter=',',header='model,pair,period,mean,frame_SD',comments='')
    save(fig,'03_RDF_coordination')
    fig,axes=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    windows=['5-40','10-50','20-80','20-100']; rows=[]
    for i,m in enumerate(models):
        a=read(f'{m}_600K_msd.csv');d=data[f'{m}_600K']
        axes[0,0].plot(a[:,0],a[:,1],styles[i],color=colors[i],label=m)
        axes[0,1].plot(windows,[d['fit_windows'][w]['D_cm2_s']*1e5 for w in windows],styles[i],marker='o',color=colors[i])
        axes[1,0].plot([1,2,3,4],np.array(d['block_D_cm2_s'])*1e5,styles[i],marker='o',color=colors[i])
        species=['Li','Zr','O','Cl'];v=[d['species'][s]['MSD_200ps_A2'] for s in species]
        axes[1,1].plot(species,v,styles[i],marker='o',color=colors[i])
        for s,val in zip(species,v):rows.append([m,s,val])
    axes[0,0].set(xlim=(0,100),ylim=(0,130),xlabel='Lag time (ps)',ylabel='Li MSD (Å²)',title='Time-origin averaged MSD');axes[0,0].legend()
    axes[0,1].set(xlabel='Fit lag window (ps)',ylabel='D_app (10⁻⁵ cm²/s)',title='Full-trajectory window sensitivity')
    axes[1,0].set(xlabel='50 ps trajectory block',ylabel='D_app (10⁻⁵ cm²/s)',title='Block fits: 5–20 ps lag',xticks=[1,2,3,4])
    axes[1,1].set(ylabel='Single-origin MSD at 200 ps (Å²)',title='Li and framework motion')
    np.savetxt(OUT/'species_endpoint.csv',np.array(rows,dtype=str),fmt='%s',delimiter=',',header='model,species,system_COM_corrected_MSD_A2',comments='')
    save(fig,'04_MSD_framework')
    subset={f'{m}_600K':data[f'{m}_600K'] for m in models}
    hashes['results.json']=hashlib.sha256((SRC/'results.json').read_bytes()).hexdigest()
    (OUT/'summary.json').write_text(json.dumps({'source_sha256':hashes,'data':subset},indent=2)+'\n')
    print('Saved four comparison figures and source data:',OUT)

if __name__=='__main__':run()
