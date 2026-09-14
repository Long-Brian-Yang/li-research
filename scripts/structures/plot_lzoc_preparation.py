"""Plot archived 55 ps preparation logs, excluding both minimizations.

Contract: three preparations completed, but this is not full stability validation.
Quantitative grid: columns=candidates; rows=temperature, PE/atom, late NPT density.
Python-only, slide-sized 13x9 inches, PNG/PDF/SVG, raw unsmoothed series.
"""
from pathlib import Path
import hashlib
import json
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'docs/daily_reports/2026-09-14/figures'

def read_md(path):
    # Custom 14-column thermo applies only after initial minimization.
    # Stop BEFORE final minimization, whose step/time columns are not MD time.
    text = path.read_text().split('reset_timestep 0',1)[1].split('undump traj',1)[0]
    rows = {}
    for line in text.splitlines():
        try: values = list(map(float,line.split()))
        except ValueError: continue
        if len(values)==14:
            assert values[2]==192
            rows[values[0]]=values  # repeated stage-boundary records are identical
    a=np.array([rows[k] for k in sorted(rows)])
    assert a.shape==(1101,14) and np.isfinite(a).all()
    assert np.allclose(np.diff(a[:,1]),.05)
    return a

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':14,
                         'axes.titlesize':17,'axes.labelsize':15,'axes.linewidth':1.2,
                         'lines.linewidth':1.8,'pdf.fonttype':42,'svg.fonttype':'none'})
    OUT.mkdir(parents=True,exist_ok=True)
    series=[]; summary={}
    for i in (1,2,3):
        p=ROOT/f'materials/candidates/LZOC/archive/completed_reference_trials/source_{i}/candidate.log'
        a=read_md(p);series.append(a)
        np.savetxt(OUT/f'candidate_{i}_preparation.csv',a,delimiter=',',comments='',
                   header='step,time_ps,atoms,T_K,PE_eV,KE_eV,Etot_eV,P_bar,V_A3,rho_g_cm3,Lx_A,Ly_A,Lz_A,Fmax_component_eV_A')
        blocks={}
        for lo,hi in ((45,50),(50,55)):
            b=a[(a[:,1]>lo)&(a[:,1]<=hi)]
            blocks[f'{lo}_{hi}_ps']={'n':len(b),'T_mean_K':float(b[:,3].mean()),
                'rho_mean_g_cm3':float(b[:,9].mean()),'rho_frame_sd':float(b[:,9].std(ddof=1)),
                'PE_mean_eV':float(b[:,4].mean())}
        summary[str(i)]={'source':str(p.relative_to(ROOT)),
            'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'blocks':blocks}
    fig,axs=plt.subplots(3,3,figsize=(13,9),sharey='row')
    colors=['#32688E','#B37525','#766097']
    for col,(a,c) in enumerate(zip(series,colors)):
        t=a[:,1]
        axs[0,col].set_title(f'Candidate {col+1}')
        axs[0,col].plot(t,a[:,3],color=c)
        target=np.where(t<=10,1500,np.where(t<40,1500-40*(t-10),300))
        axs[0,col].plot(t,target,color='#333333',linestyle='--',linewidth=1.1,label='Target')
        axs[1,col].plot(t,a[:,4]/192,color=c)
        b=a[t>=45];axs[2,col].plot(b[:,1],b[:,9],color=c)
        for row in (0,1):
            ax=axs[row,col];ax.set_xlim(0,55);ax.set_xticks([0,10,20,30,40,45,55])
            ax.tick_params(axis='x',labelsize=11)
            for boundary in (10,40,45): ax.axvline(boundary,color='.6',lw=.8,ls=':')
            ax.set_xlabel('Preparation time (ps)')
        axs[2,col].set_xlim(45,55);axs[2,col].set_xticks([45,50,55])
        axs[2,col].set_xlabel('Preparation time (ps) — NPT')
        axs[2,col].axvline(50,color='.6',lw=.8,ls=':')
        for row in range(3):
            axs[row,col].grid(alpha=.18)
            axs[row,col].text(.03,.92,chr(97+row*3+col),transform=axs[row,col].transAxes,fontweight='bold')
    axs[0,0].set_ylabel('Temperature (K)')
    axs[1,0].set_ylabel('Potential energy (eV/atom)')
    axs[2,0].set_ylabel(r'Density (g cm$^{-3}$)')
    axs[0,2].legend(loc='upper right',fontsize=11)
    fig.suptitle('LZOC — three-candidate preparation',fontsize=20,y=.99)
    fig.text(.5,.015,'0–10 ps: 1500 K NVT  |  10–40 ps: cooling  |  40–45 ps: 300 K NVT  |  45–55 ps: 300 K NPT',ha='center',fontsize=12)
    fig.tight_layout(rect=[0,.04,1,.96],h_pad=1.25)
    for ext in ('png','pdf','svg'):fig.savefig(OUT/f'LZOC_three_candidate_preparation.{ext}',dpi=200)
    plt.close(fig)
    (OUT/'preparation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
