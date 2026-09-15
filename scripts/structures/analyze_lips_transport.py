"""Analyse completed Li3PS4 four-temperature control; never modify trajectories.

Fixed diagnostic windows, one glass per T, block spread is not a replica CI.
Chen source numbers retain original file labels; Fig.3a axis establishes D units.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,csv
import numpy as np
from ase import Atoms
from ase.io import read,iread
from analyze_lzoc_production import window_msd,unwrap,fit_msd
from complete_amorphous_comparisons import sigma_mscm
from finish_amorphous_analysis import frame_metrics,block_slopes
from structure_followup import motifs
from li_diffusion_style import apply_style

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'Li3PS4_transport'
TS=[300,500,700,900]
WINDOWS=[(5,20),(10,40),(20,80),(40,100)]
COLORS=['#5e3c99','#31688e','#35b779','#d73027']

def save(fig,name):
    import matplotlib.pyplot as plt
    apply_style(fig)
    for ext in ('png','pdf','svg'):
        fig.savefig(OUT/f'{name}.{ext}',dpi=220)
    svg=OUT/f'{name}.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)

def run():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42})
    OUT.mkdir(parents=True,exist_ok=True)
    results={};hashes={};rows=[];fitrows=[];network=[]
    fm,am=plt.subplots(2,2,layout='constrained')
    ff,af=plt.subplots(2,2,layout='constrained')
    ft,at=plt.subplots(2,2,layout='constrained')
    fr,ar=plt.subplots(2,2,layout='constrained',sharey='row')
    fb,ab=plt.subplots(1,2,layout='constrained')
    for i,T in enumerate(TS):
        p=BASE/f'source/Li3PS4_transport/transport_{T}K_8675738'
        assert (p/'completed.txt').exists()
        for q in p.rglob('*'):
            if q.is_file():hashes[str(q.relative_to(ROOT))]=hashlib.sha256(q.read_bytes()).hexdigest()
        prod=p/'production';a=read(prod/'model.xyz');s=np.array(a.get_chemical_symbols())
        assert Counter(s)==Counter(Li=192,P=64,S=256)
        frames=list(iread(prod/'dump.xyz'))
        assert len(frames)==2000
        times=np.array([v.info['Time'] for v in frames])/1000
        np.testing.assert_allclose(times,np.arange(1,2001)*.1,atol=1e-7)
        assert all(np.array_equal(s,v.get_chemical_symbols()) for v in frames)
        assert all(np.allclose(a.cell,v.cell,atol=1e-7,rtol=0) for v in frames)
        x=np.array([a.positions]+[v.positions for v in frames]);assert np.isfinite(x).all()
        fracdelta=np.diff(x,axis=0)@np.linalg.inv(a.cell.array)
        micdelta=fracdelta-np.round(fracdelta)
        xu=unwrap(x,a.cell.array)
        com=np.average(xu,axis=1,weights=a.get_masses())
        corrected=xu-com[:,None,:]
        t=np.arange(2001)*.1
        y={el:window_msd(corrected[:,s==el]) for el in ('Li','P','S')}
        # Independent brute-force check of FFT MSD on the real trajectory.
        errs=[]
        for lag in (10,200,800):
            direct=np.mean(np.sum((corrected[lag:,s=='Li']-corrected[:-lag,s=='Li'])**2,axis=2))
            errs.append(abs(direct-y['Li'][lag]))
        assert max(errs)<1e-7
        fits=[fit_msd(t,y['Li'],*w) for w in WINDOWS]
        for v in fits:fitrows.append([T,v['lo_ps'],v['hi_ps'],v['D_cm2_s'],v['R2'],v['intercept_A2'],v['alpha']])
        blocks=block_slopes(corrected[:,s=='Li'],.1,4,(5,20))
        np.savetxt(OUT/f'{T}K_MSD.csv',np.c_[t,y['Li'],y['P'],y['S']],delimiter=',',header='lag_ps,Li_A2,P_A2,S_A2',comments='')
        raw=window_msd(xu[:,s=='Li'])
        d_raw=fit_msd(t,raw,20,80)['D_cm2_s']
        stage_results={}
        for stage,length in [('ramp',200),('equil',1000),('production',4000)]:
            th=np.loadtxt(p/stage/'thermo.out');assert th.shape==(length,18) and np.isfinite(th).all()
            vol=np.linalg.det(th[:,9:].reshape(-1,3,3));assert np.all(vol>0)
            rho=a.get_masses().sum()*1.6605390666/vol
            vals=np.c_[th[:,0],th[:,2]/512,th[:,3:6].mean(1),rho]
            np.savetxt(OUT/f'{T}K_{stage}_thermo.csv',np.c_[np.arange(1,length+1)*.05,vals],delimiter=',',header='time_ps,T_K,PE_eV_atom,P_GPa,rho_g_cm3',comments='')
            stage_results[stage]={'mean_T_K':float(vals[:,0].mean()),'mean_P_GPa':float(vals[:,2].mean()),'mean_rho_g_cm3':float(rho.mean()),'rho_first_quarter':float(rho[:length//4].mean()),'rho_last_quarter':float(rho[-length//4:].mean()),'PE_last_quarter_minus_first_eV_atom':float(vals[-length//4:,1].mean()-vals[:length//4,1].mean())}
            if stage=='production':
                for j in range(4):
                    # 5 ps block means for legibility; complete raw data in CSV.
                    vals5=vals.reshape(40,100,4).mean(1)
                    at.flat[j].plot(np.arange(40)*5+2.5,vals5[:,j],color=COLORS[i],ls=['-','--','-.',':'][i],label=f'{T} K')
        ax=am.flat[i];ax.plot(t[:1001],y['Li'][:1001],color=COLORS[i],label='Li MSD')
        ax.set(title=f'{T} K: lithium',xlabel='Lag time (ps)',ylabel='MSD (Å²)',ylim=(0,None));ax.legend()
        for el,ls in [('P','--'),('S',':')]:af.flat[i].plot(t[:1001],y[el][:1001],ls=ls,label=el)
        af.flat[i].set(title=f'{T} K: framework control',xlabel='Lag time (ps)',ylabel='MSD (Å²)');af.flat[i].legend()
        ab[0].plot(np.arange(4),np.array([v['D_cm2_s'] for v in fits])*1e6,'o-',color=COLORS[i],label=f'{T} K')
        ab[1].plot([25,75,125,175],blocks*1e6,'o-',color=COLORS[i],label=f'{T} K')
        # Fixed cutoffs, 10 samples in early and late 50 ps intervals.
        edges=np.arange(0,5.0001,.05);r=(edges[:-1]+edges[1:])/2
        pairs=[('Li','S',3.2),('P','S',2.6)]
        structure={}
        for label,ids in [('early',range(0,500,50)),('late',range(1500,2000,50))]:
            gs=[];cs=[];cn4=[];isolated=[];mins=[]
            for idx in ids:
                aa=frames[idx];g,c,minimum=frame_metrics(aa,pairs,edges);gs.append(g);cs.append(c);mins.append(minimum)
                dd=aa.get_all_distances(mic=True);np.fill_diagonal(dd,np.inf)
                ps=dd[np.ix_(s=='P',s=='S')]<2.6;pp=dd[np.ix_(s=='P',s=='P')]<2.6
                mo=motifs(ps,pp);cn4.append(float((ps.sum(1)==4).mean()));isolated.append(mo.get('P1S4',0)/64)
                for motif,count in mo.items():network.append([T,label,float(times[idx]),motif,count])
            g=np.mean(gs,axis=0)
            np.savetxt(OUT/f'{T}K_{label}_RDF.csv',np.c_[r,g.T],delimiter=',',header='r_A,Li_S,P_S',comments='')
            for j in range(2):ar[j,int(label=='late')].plot(r,g[j],color=COLORS[i],ls=['-','--','-.',':'][i],label=f'{T} K')
            structure[label]={'CN_LiS_PS':np.mean(cs,axis=0).tolist(),'P_four_S_fraction':float(np.mean(cn4)),'P_isolated_P1S4_fraction':float(np.mean(isolated)),'minimum_distance_A':float(min(mins))}
        sig=sigma_mscm(fit['D_cm2_s'],192,a.get_volume(),T)
        results[str(T)]={'fits':fits,'block_D_5to20_cm2_s':blocks.tolist(),'block_SD_not_SE_cm2_s':float(blocks.std(ddof=1)),'sigma_NE_apparent_mS_cm':sig,'stages':stage_results,'structure':structure,'volume_A3':float(a.get_volume()),'MSD80_A2':{el:float(v[800]) for el,v in y.items()},'max_fractional_MIC_step':float(np.abs(micdelta).max()),'max_COM_displacement_A':float(np.linalg.norm(com-com[0],axis=1).max()),'raw_D20to80_cm2_s':d_raw,'independent_MSD_error_A2':max(errs)}
        rows.append([T,fit['D_cm2_s'],sig,fit['R2'],fit['alpha'],float(blocks.std(ddof=1)),stage_results['production']['mean_rho_g_cm3']])
        print(T,json.dumps(results[str(T)]),flush=True)
    for j,label in enumerate(['Temperature (K)','Potential energy (eV/atom)','Pressure (GPa)','Density (g/cm³)']):
        at.flat[j].set(title='Production: 5 ps means',xlabel='Time (ps)',ylabel=label);at.flat[j].legend(loc='upper center',bbox_to_anchor=(.5,-.2),ncol=4)
    for j,pair in enumerate(['Li–S','P–S']):
        for k,label in enumerate(['early','late']):ar[j,k].set(title=f'{pair}: {label}',xlabel='r (Å)',ylabel='g(r)');ar[j,k].legend()
    ab[0].set(xticks=np.arange(4),xticklabels=['5–20','10–40','20–80','40–100'],xlabel='Fit window (ps)',ylabel='Apparent D (10⁻⁶ cm²/s)',title='Common-window sensitivity')
    ab[1].set(xlabel='50 ps block centre (ps)',ylabel='Apparent D (10⁻⁶ cm²/s)',title='Block fits: 5–20 ps');ab[0].legend();ab[1].legend()
    for ax in ab:
        ax.set_yscale('log')
        ax.legend(loc='upper center',bbox_to_anchor=(.5,-.2),ncol=4)
    for fig,name in [(fm,'Li_MSD'),(ff,'framework_MSD'),(ft,'thermodynamics'),(fr,'RDF_early_late'),(fb,'fit_sensitivity')]:save(fig,name)
    np.savetxt(OUT/'transport_summary.csv',rows,delimiter=',',header='T_K,D_app_20to80_cm2_s,sigma_NE_app_mS_cm,R2,alpha,block_SD_5to20_cm2_s,rho_g_cm3',comments='')
    np.savetxt(OUT/'fit_windows.csv',fitrows,delimiter=',',header='T_K,lo_ps,hi_ps,D_app_cm2_s,R2,intercept_A2,alpha',comments='')
    with (OUT/'geometric_components.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['T_K,interval,time_ps,motif,count'.split(',')][0]);w.writerows(network)
    from scipy.stats import linregress
    high=np.array(rows)[1:]
    slope=linregress(1/high[:,0],np.log(high[:,1]))
    ea={'range_K':[500,700,900],'Ea_apparent_eV':float(-slope.slope*8.617333262e-5),'R2':float(slope.rvalue**2),'status':'exploratory only: 500 K offset and 900 K network motion; no 300 K extrapolation'}
    (OUT/'analysis.json').write_text(json.dumps({'results':results,'highT_diagnostic':ea,'hashes':hashes},indent=2)+'\n')
    # Reference source grid has a mislabeled header; official Fig.3a is ln[D(cm²/s)].
    ref=np.genfromtxt(BASE/'final_comparisons/Chen2025_Fig._3a.csv',delimiter=',',skip_header=1)
    f,ax=plt.subplots(layout='constrained')
    ax.semilogy(1000/np.array(TS),np.array(rows)[:,1],'o-',color=COLORS[1],label='NEP89: apparent D (20–80 ps)')
    ax.semilogy(ref[:,0],ref[:,2],'s--',color='#777777',label='Chen 2025: glass, Fig. 3a')
    ax.set(xlabel='1000 / T (K⁻¹)',ylabel='D (cm²/s)',title='Li₃PS₄: transport comparison');ax.legend();save(f,'D_reference_comparison')
    comp=[]
    for T,D,*_ in rows:
        idx=np.argmin(abs(ref[:,0]-1000/T));assert abs(ref[idx,0]-1000/T)<1e-7
        comp.append([T,D,ref[idx,2],D/ref[idx,2]])
    np.savetxt(OUT/'reference_comparison.csv',comp,delimiter=',',header='T_K,NEP_apparent_D_cm2_s,Chen_glass_D_cm2_s,ratio_diagnostic_not_accuracy',comments='')

if __name__=='__main__':run()
