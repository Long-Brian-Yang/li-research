"""Source-backed postprocessing of completed LZOC/LSZC trials; no raw edits."""
from pathlib import Path
import json
import hashlib
import numpy as np
from ase import Atoms
from ase.io import read
from analyze_lzoc_production import window_msd, unwrap, read_gpumd, fit_msd

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'

def frame_metrics(a,pairs,edges):
    s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True)
    np.fill_diagonal(d,np.inf);gs=[];cs=[]
    height=1/np.linalg.norm(np.linalg.inv(a.cell.array),axis=0).max()
    if edges[-1]>=height/2:raise ValueError('RDF exceeds safe cell cutoff')
    for x,y,cut in pairs:
        nx=sum(s==x);ny=sum(s==y);z=d[np.ix_(s==x,s==y)]
        norm=nx*(ny-int(x==y))*4*np.pi/3*np.diff(edges**3)/a.get_volume()
        gs.append(np.histogram(z,edges)[0]/norm);cs.append(float((z<cut).sum(1).mean()))
    return np.array(gs),np.array(cs),float(d.min())

def block_slopes(x,dt,nblocks,window):
    out=[]
    for part in np.array_split(x[:-1],nblocks):
        y=window_msd(part);t=np.arange(len(y))*dt;m=(t>=window[0])&(t<=window[1])
        out.append(float(np.polyfit(t[m],y[m],1)[0]/6*1e-4))
    return np.array(out)

def run():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.titlesize':16,
        'axes.labelsize':14,'axes.linewidth':1.2,'lines.linewidth':2,'legend.fontsize':11,
        'svg.fonttype':'none','pdf.fonttype':42,'axes.grid':True,'grid.alpha':.18})
    dest=BASE/'analysis_complete';dest.mkdir(exist_ok=True)
    colors=['#32688e','#34ad86','#b73b46'];styles=['-','--','-.'];allresults={}
    pairs=[('Li','Cl',3.2),('Zr','Cl',3.2),('Zr','O',2.6),('Cl','Cl',4.)]
    edges=np.arange(0,5.0001,.05);r=(edges[:-1]+edges[1:])/2
    def save(fig,name):
        from li_diffusion_style import apply_style
        apply_style(fig)
        fig.savefig(dest/(name+'.png'),dpi=300)
        fig.savefig(dest/(name+'.pdf'));fig.savefig(dest/(name+'.svg'));plt.close(fig)
    def csv(name,a,h):np.savetxt(dest/name,a,delimiter=',',header=h,comments='')
    figth,ath=plt.subplots(3,3,figsize=(14,9),layout='constrained')
    figms,ams=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    figr,ar=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    figc,ac=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    figb,ab=plt.subplots(1,2,figsize=(12,4.5),layout='constrained')
    figf,af=plt.subplots(1,3,figsize=(14,4.5),layout='constrained')
    for i,temp in enumerate([340,360,380]):
        p=BASE/f'source/LZOC_transport/{temp}K/production'
        ts,x,c,s=read_gpumd(p/'dump.xyz');a=read(p/'model.xyz')
        assert len(ts)==2000 and np.allclose(np.diff(ts),.1) and np.allclose(c,c[0])
        assert np.array_equal(s,a.get_chemical_symbols()) and len(a)==192
        x=np.concatenate([a.positions[None],x]);t=np.arange(len(x))*.1
        xu=unwrap(x,c[0]);xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
        li=xu[:,s=='Li'];y=window_msd(li)
        for k in [1,100,500]:assert np.isclose(y[k],np.mean(np.sum((li[k:]-li[:-k])**2,2)),atol=1e-8)
        block=block_slopes(li,.1,4,(5,20));windows=[(5,40),(10,50),(20,80),(20,100)]
        fits=[fit_msd(t,y,*w) for w in windows]
        csv(f'LZOC_{temp}K_msd.csv',np.c_[t,y],'lag_ps,MSD_A2')
        csv(f'LZOC_{temp}K_block_D.csv',np.c_[[25,75,125,175],block],'block_center_ps,slope_D_cm2_s')
        ams[0].plot(t,y,color=colors[i],ls=styles[i],label=f'{temp} K')
        ams[1].loglog(t[1:1001],y[1:1001],color=colors[i],ls=styles[i],label=f'{temp} K')
        ab[0].plot([25,75,125,175],block/1e-6,'o'+styles[i],color=colors[i],label=f'{temp} K')
        ab[1].plot(range(4),[f['D_cm2_s']/1e-6 for f in fits],'o'+styles[i],color=colors[i])
        th=np.loadtxt(p/'thermo.out');assert th.shape==(4000,18) and np.isfinite(th).all()
        tt=np.arange(1,4001)*.05;vals=np.c_[th[:,0],th[:,2]/192,th[:,3:6].mean(1)]
        csv(f'LZOC_{temp}K_thermo.csv',np.c_[tt,vals],'time_ps,T_K,PE_eV_atom,P_GPa')
        for j,label in enumerate(['Temperature (K)','Potential energy (eV/atom)','Pressure (GPa)']):
            ath[j,i].plot(tt,vals[:,j],color=colors[i],lw=.8,alpha=.65)
            ath[j,i].plot(tt.reshape(-1,100).mean(1),vals[:,j].reshape(-1,100).mean(1),color='#222222',lw=1.7)
            if j==0:ath[j,i].set_title(f'LZOC — {temp} K')
            if i==0:ath[j,i].set_ylabel(label)
            if j==2:ath[j,i].set_xlabel('Time (ps)')
        gs=[];cs=[];mins=[];sample=np.arange(10,2001,10)
        for k in sample:
            f=Atoms(s,positions=x[k],cell=c[0],pbc=True);g,cn,mi=frame_metrics(f,pairs,edges)
            gs.append(g);cs.append(cn);mins.append(mi)
        gs=np.array(gs);cs=np.array(cs);g0,cn0,_=frame_metrics(a,pairs,edges)
        csv(f'LZOC_{temp}K_rdf.csv',np.column_stack([r]+[v for j in range(4) for v in [g0[j],gs[100:,j].mean(0)]]),'r_A,'+','.join(f'{u}_{v}_{z}' for u,v,_ in pairs for z in ['initial','late']))
        csv(f'LZOC_{temp}K_coordination.csv',np.c_[t[sample],cs,mins],'time_ps,'+','.join(u+'_'+v for u,v,_ in pairs)+',minimum_pair_A')
        for j,(u,v,cut) in enumerate(pairs):
            ar.flat[j].plot(r,gs[100:,j].mean(0),color=colors[i],ls=styles[i],label=f'{temp} K')
            ar.flat[j].set(title=f'{u}–{v}',xlabel='r (Å)',ylabel='g(r)')
            ac.flat[j].plot(t[sample],cs[:,j],color=colors[i],ls=styles[i],label=f'{temp} K',alpha=.9)
            ac.flat[j].set(title=f'{u}–{v} (< {cut:g} Å)',xlabel='Time (ps)',ylabel='Mean neighbour count')
        species={}
        for u in ['Zr','O','Cl']:
            z=window_msd(xu[:,s==u]);species[u]=float(z[800]);af[i].plot(t,z,label=u)
        af[i].set(title=f'{temp} K',xlabel='Lag time (ps)',ylabel='Framework MSD (Å²)');af[i].legend()
        allresults[str(temp)]={'block_D_values_cm2_s':block.tolist(),'block_mean':float(block.mean()),'block_SD_not_SE':float(block.std(ddof=1)),
            'windows':fits,'framework_MSD80_A2':species,'late_mean_CN':cs[100:].mean(0).tolist(),'pairs':pairs,
            'sampled_minimum_pair_A':float(min(mins)),'sampled_structure_frames':200,'rdf_late_frames':100,
            'hashes':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['dump.xyz','thermo.out','model.xyz']}}
        print('LZOC',temp,allresults[str(temp)],flush=True)
    ams[0].set(xlabel='Lag time (ps)',ylabel='Li MSD (Å²)',title='Time-origin averaged MSD',xlim=(0,100))
    ams[1].set(xlabel='Lag time (ps)',ylabel='Li MSD (Å²)',title='Log–log view');ams[0].legend();ams[1].legend()
    ab[0].set(xlabel='50 ps block centre (ps)',ylabel='Slope estimate (10⁻⁶ cm²/s)',title='Within-trajectory blocks (5–20 ps fit)');ab[0].legend()
    ab[1].set(xticks=range(4),xticklabels=['5–40','10–50','20–80','20–100'],xlabel='Fit lag window (ps)',ylabel='Slope estimate (10⁻⁶ cm²/s)',title='Window sensitivity (full trajectory)')
    ar[0,0].legend();ac[0,0].legend()
    for f,n in [(figth,'LZOC_thermodynamics'),(figms,'LZOC_MSD'),(figr,'LZOC_RDF'),(figc,'LZOC_coordination'),(figb,'LZOC_MSD_robustness'),(figf,'LZOC_framework_MSD')]:save(f,n)
    # LSZC: preparation and hold, not a transport-production dataset.
    p=BASE/'source/LSZC_anneal';pr=[('S','O',1.9),('Zr','O',2.6),('Zr','Cl',3.2),('Li','Cl',3.2)]
    frames=read(p/'hold/dump.xyz',index=':');a=read(p/'ramp/model.xyz');assert len(frames)==200 and len(a)==272
    gs=[];cs=[];mins=[]
    for f in frames:
        g,cn,mi=frame_metrics(f,pr,edges);gs.append(g);cs.append(cn);mins.append(mi)
    gs=np.array(gs);cs=np.array(cs);g0,_,_=frame_metrics(a,pr,edges)
    csv('LSZC_coordination.csv',np.c_[np.arange(1,201)*.1,cs,mins],'hold_time_ps,S_O,Zr_O,Zr_Cl,Li_Cl,minimum_pair_A')
    csv('LSZC_RDF.csv',np.column_stack([r]+[v for j in range(4) for v in [g0[j],gs[100:,j].mean(0)]]),'r_A,'+','.join(u+'_'+v+'_'+z for u,v,_ in pr for z in ['before_ramp','late_hold']))
    f,axs=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for j,(u,v,_) in enumerate(pr):
        axs.flat[j].plot(r,g0[j],color='#777777',ls='--',label='Before ramp (1 frame)')
        axs.flat[j].plot(r,gs[100:,j].mean(0),color='#32688e',label='400 K, last 10 ps')
        axs.flat[j].set(title=f'{u}–{v}',xlabel='r (Å)',ylabel='g(r)')
    axs[0,0].legend();save(f,'LSZC_RDF')
    f,axs=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for j,(u,v,cut) in enumerate(pr):
        axs.flat[j].plot(np.arange(1,201)*.1,cs[:,j],color='#32688e')
        axs.flat[j].set(title=f'{u}–{v} (< {cut:g} Å)',xlabel='Hold time (ps)',ylabel='Mean neighbour count')
    save(f,'LSZC_coordination')
    f,axs=plt.subplots(3,1,figsize=(10,9),layout='constrained');table=[]
    for stage,offset in [('ramp',0),('hold',100)]:
        th=np.loadtxt(p/stage/'thermo.out');tt=np.arange(1,len(th)+1)*.05+offset;vals=np.c_[th[:,0],th[:,2]/272,th[:,3:6].mean(1)];table.append(np.c_[tt,vals])
        for j in range(3):axs[j].plot(tt,vals[:,j],color='#32688e',lw=.7,alpha=.65)
    for ax,label in zip(axs,['Temperature (K)','Potential energy (eV/atom)','Pressure (GPa)']):
        ax.set_ylabel(label);ax.axvline(100,color='k',ls='--',lw=1)
    axs[0].set_title('LSZC — ramp and 400 K hold');axs[-1].set_xlabel('Time (ps)');save(f,'LSZC_thermodynamics')
    csv('LSZC_thermo.csv',np.concatenate(table),'time_ps,T_K,PE_eV_atom,P_GPa')
    allresults['LSZC']={'late_mean_CN':cs[100:].mean(0).tolist(),'pairs':pr,'minimum_hold_pair_A':min(mins),'hashes':{str(q.relative_to(p)):hashlib.sha256(q.read_bytes()).hexdigest() for q in p.glob('*/*') if q.name in ['model.xyz','dump.xyz','thermo.out']}}
    # Author deposited geometry is a structural reference, not experimental RDF.
    refpath=ROOT/'materials/candidates/LSZC/source/Supplementary Data 2.txt'
    ref=read(refpath,format='cif');gr,cr,mr=frame_metrics(ref,pr,edges)
    refdensity=float(ref.get_masses().sum()*1.66053906660/ref.get_volume())
    ours=float(a.get_masses().sum()*1.66053906660/a.get_volume())
    allresults['LSZC']['author_Data2']={'n_atoms':len(ref),'density_g_cm3':refdensity,'our_density_g_cm3':ours,
        'relative_density_difference_percent':(ours/refdensity-1)*100,'CN':cr.tolist(),'minimum_pair_A':mr,
        'sha256':hashlib.sha256(refpath.read_bytes()).hexdigest(),'meaning':'single author-deposited geometry, not experiment or thermal average'}
    csv('LSZC_author_reference_RDF.csv',np.column_stack([r]+[v for j in range(4) for v in [gr[j],gs[100:,j].mean(0)]]),'r_A,'+','.join(u+'_'+v+'_'+z for u,v,_ in pr for z in ['author_single','ours_late']))
    f,axs=plt.subplots(2,2,figsize=(11,8),layout='constrained')
    for j,(u,v,_) in enumerate(pr):
        axs.flat[j].plot(r,gr[j],color='#777777',ls='--',label='Author geometry (1088 atoms)')
        axs.flat[j].plot(r,gs[100:,j].mean(0),color='#32688e',label='NEP, 400 K (272 atoms)')
        axs.flat[j].set(title=f'{u}–{v}',xlabel='r (Å)',ylabel='g(r)')
    axs[0,0].legend(fontsize=9);save(f,'LSZC_author_structure_comparison')
    (dest/'summary.json').write_text(json.dumps(allresults,indent=2)+'\n')
    print('Saved',dest,flush=True)

if __name__=='__main__':run()
