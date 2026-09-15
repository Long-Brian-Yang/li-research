"""Diagnostic evidence grids using the existing Li-diffusion presentation style.

Contract: LSZC volume release does not remove the structural discrepancy;
LZOC timestep changes do not establish transport convergence. Quantitative
grids, 7.2 x 5.8 inches/panel, editable PDF/SVG + 300 dpi PNG, source CSVs.
One structure per route; no confidence intervals or significance tests.
"""
import json
from pathlib import Path
import numpy as np
from ase.io import read
from analyze_lzoc_production import read_gpumd, unwrap, window_msd
from finish_amorphous_analysis import frame_metrics
from li_diffusion_style import apply_style
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'targeted_diagnostics'
BLUE,RED='#31688e','#d73027'

def export(fig,name):
    apply_style(fig)
    for ax,label in zip(fig.axes,'abcd'):
        ax.text(-.09,1.04,label,transform=ax.transAxes,va='bottom',fontweight='bold',fontsize=17)
    for ext in ['png','svg','pdf']:
        fig.savefig(OUT/f'{name}.{ext}',dpi=300)
    q=OUT/f'{name}.svg'
    q.write_text('\n'.join(s.rstrip() for s in q.read_text().splitlines())+'\n')
    plt.close(fig)

def csv(name,a,header):
    np.savetxt(OUT/f'{name}.csv',a,delimiter=',',header=header,comments='')

def run():
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42})
    fig,axes=plt.subplots(2,2,layout='constrained')
    ax=axes.ravel()
    for tag,folder,color in [('Prior NVT','LSZC_anneal/hold',BLUE),('NPT diagnostic','LSZC_npt400',RED)]:
        p=BASE/'source'/folder;frames=read(p/'dump.xyz',index=':')
        assert len(frames)==200
        density=[a.get_masses().sum()/a.get_volume()*1.6605390666 for a in frames]
        ax[0].plot(np.arange(1,201)*.1,density,color=color,label=tag)
        th=np.loadtxt(p/'thermo.out');assert th.shape==(400,18)
        means=th[:,3:6].mean(1).reshape(4,100).mean(1)
        ax[1].plot([2.5,7.5,12.5,17.5],means,'o-',color=color,label=tag)
        csv(tag.replace(' ','_')+'_thermo',np.c_[np.arange(1,401)*.05,th[:,0],th[:,2]/272,th[:,3:6].mean(1)],'time_ps,T_K,PE_eV_atom,P_GPa')
        csv(tag.replace(' ','_')+'_density',np.c_[np.arange(1,201)*.1,density],'time_ps,density_g_cm3')
        edges=np.arange(0,5.00001,.05);gs=[]
        for a in frames[109::10]:
            g,_,_=frame_metrics(a,[('Zr','O',2.6),('Zr','Cl',3.2)],edges);gs.append(g)
        mean=np.mean(gs,axis=0);r=(edges[1:]+edges[:-1])/2
        csv(tag.replace(' ','_')+'_RDF',np.column_stack([r,*mean]),'r_A,Zr_O,Zr_Cl')
        for j in range(2):ax[j+2].plot(r,mean[j],color=color,label=tag)
    ax[0].set(title='LSZC: volume relaxation',xlabel='Stage time (ps)',ylabel=r'Density (g cm$^{-3}$)')
    ax[1].axhline(.0001,color='gray',ls=':',label='Target: 1 bar')
    ax[1].set(title='5 ps pressure block means',xlabel='Stage time (ps)',ylabel='Pressure (GPa)')
    for j,pair in enumerate(['Zr–O','Zr–Cl']):
        ax[j+2].set(title=f'{pair}: final 10 ps',xlabel=r'$r$ (Å)',ylabel=r'$g(r)$',xlim=(1.5,4.5))
    for a in ax:a.legend(loc='best')
    export(fig,'LSZC_volume_structure_diagnostic')

    fig,axes=plt.subplots(2,2,layout='constrained');ax=axes.ravel()
    results=json.loads((OUT/'results.json').read_text())
    for tag,folder,color in [('NHC_0.5fs','LZOC_NHC05_380',BLUE),('NHC_2fs','LZOC_NHC80/aimd_aligned_380K_8675022/production',RED)]:
        a=np.loadtxt(OUT/f'{tag}_MSD.csv',delimiter=',',skiprows=1)
        ax[0].plot(a[:401,0],a[:401,1],color=color,label=tag.replace('_',' '))
        fits=results[tag]['fits'];ax[1].plot(range(3),[v['D_cm2_s']/1e-6 for v in fits.values()],'o-',color=color,label=tag.replace('_',' '))
        p=BASE/'source'/folder;ts,x,c,s=read_gpumd(p/'dump.xyz');initial=read(p/'model.xyz')
        assert len(ts)==800 and np.allclose(c,c[0])
        x=unwrap(np.concatenate([initial.positions[None],x]),c[0]);x-=np.average(x,axis=1,weights=initial.get_masses())[:,None,:]
        curves=[window_msd(x[:,s==el]) for el in ['Zr','O','Cl']]
        csv(tag+'_framework_MSD',np.column_stack([np.arange(801)*.1,*curves]),'lag_ps,Zr_A2,O_A2,Cl_A2')
        for el,y,ls in zip(['Zr','O','Cl'],curves,['-', '--', ':']):
            ax[2].plot(np.arange(401)*.1,y[:401],color=color,ls=ls,label=f'{tag.replace("NHC_", "")} {el}')
        block=np.array(results[tag]['20ps_blocks_T_PE_atom_P'])
        ax[3].plot([10,30,50,70],block[:,1],'o-',color=color,label=tag.replace('_',' '))
    ax[0].set(title='LZOC: 380 K lithium MSD',xlabel='Lag time (ps)',ylabel=r'MSD (Å$^2$)')
    ax[1].set(title='Fitting-window sensitivity',xlabel='Fit window (ps)',ylabel=r'Apparent $D$ ($10^{-6}$ cm$^2$/s)')
    ax[1].set_xticks(range(3),['5–20','10–30','10–40'])
    ax[2].set(title='Framework motion',xlabel='Lag time (ps)',ylabel=r'MSD (Å$^2$)')
    ax[3].set(title='20 ps potential-energy means',xlabel='Time (ps)',ylabel='Potential energy (eV/atom)')
    ax[3].ticklabel_format(axis='y',style='plain',useOffset=False)
    for a in ax:a.legend(loc='best')
    export(fig,'LZOC_timestep_diagnostic')

if __name__=='__main__':run()
