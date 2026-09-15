"""Matched-duration diagnostics of existing trajectories; no input mutation or MD.

Run with the analysis environment. First run extract_chen_source.py with
the bundled spreadsheet runtime.
"""
from pathlib import Path
import json, hashlib, itertools
import numpy as np
from ase import Atoms
from ase.io import read
from analyze_lzoc_production import window_msd, fit_msd, read_gpumd, unwrap
from finish_amorphous_analysis import frame_metrics, block_slopes

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/amorphous_review_20260915'
OUT=BASE/'final_comparisons'
PAIRS=[('Li','Cl',3.2),('Zr','Cl',3.2),('Zr','O',2.6),('Cl','Cl',4.)]
EDGES=np.arange(0,5.00001,.05)
COLORS=['#31688e','#d73027','#35b779']

def sigma_mscm(d,n,v,t):
    """D cm²/s, N_Li count, volume Å³, T K -> mS/cm."""
    return n/(v*1e-30)*(1.602176634e-19)**2*(d*1e-4)/(1.380649e-23*t)*10

def angle_distribution(a,center,neighbour,cut):
    s=np.array(a.get_chemical_symbols());angles=[]
    for i in np.flatnonzero(s==center):
        ids=np.flatnonzero(s==neighbour)
        v=a.get_distances(i,ids,mic=True,vector=True)
        v=v[np.linalg.norm(v,axis=1)<cut]
        v=v/np.linalg.norm(v,axis=1)[:,None]
        angles.extend(np.degrees(np.arccos(np.clip(v[j]@v[k],-1,1))) for j,k in itertools.combinations(range(len(v)),2))
    return np.array(angles)

def writecsv(name,values,header):
    np.savetxt(OUT/(name+'.csv'),values,delimiter=',',header=header,comments='')

def save(fig,name):
    from li_diffusion_style import apply_style
    import matplotlib.pyplot as plt
    apply_style(fig)
    for ext in ['png','pdf','svg']:fig.savefig(OUT/(name+'.'+ext),dpi=300)
    svg=OUT/(name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    plt.close(fig)

def hashes(p):
    return {str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest()
            for q in p.rglob('*') if q.is_file() and q.name in ['model.xyz','dump.xyz','run.in','thermo.out','completed.txt']}

def run():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'lines.linewidth':2})
    OUT.mkdir(exist_ok=True,parents=True);results={};source={}
    fm,am=plt.subplots(1,3,layout='constrained',sharey=True)
    ft,at=plt.subplots(3,3,layout='constrained')
    fr,ar=plt.subplots(2,2,layout='constrained')
    fb,ab=plt.subplots(1,3,layout='constrained')
    ff,af=plt.subplots(1,3,layout='constrained')
    for i,temp in enumerate([340,360,380]):
        initial=None
        for j,(tag,p) in enumerate([
            ('MTTK_0.5fs',BASE/f'source/LZOC_transport/{temp}K/production'),
            ('NHC_2fs',BASE/f'source/LZOC_NHC80/aimd_aligned_{temp}K_8675022/production')]):
            source.update(hashes(p));ts,x,c,s=read_gpumd(p/'dump.xyz');a=read(p/'model.xyz')
            assert np.allclose(np.diff(ts),.1) and np.allclose(c,c[0])
            assert np.array_equal(s,a.get_chemical_symbols()) and len(a)==192
            if initial is None:initial=a.copy()
            else:
                np.testing.assert_allclose(initial.positions,a.positions,atol=1e-9)
                np.testing.assert_allclose(initial.cell,a.cell,atol=1e-9)
                if 'vel' in a.arrays:np.testing.assert_allclose(initial.arrays['vel'],a.arrays['vel'])
            x=np.concatenate([a.positions[None],x[:800]]);t=np.arange(801)*.1
            assert len(x)==801 and ts[799]>79.99
            xu=unwrap(x,c[0]);xu-=np.average(xu,axis=1,weights=a.get_masses())[:,None,:]
            li=xu[:,s=='Li'];y=window_msd(li)
            fits=[fit_msd(t,y,*w) for w in [(5,20),(10,30),(10,40)]]
            blocks=block_slopes(li,.1,4,(2,8));key=f'LZOC_{temp}K_{tag}'
            species={el:window_msd(xu[:,s==el]) for el in ['Li','Zr','O','Cl']}
            writecsv(key+'_MSD',np.column_stack([t,*species.values()]),'lag_ps,Li_A2,Zr_A2,O_A2,Cl_A2')
            writecsv(key+'_blocks',np.c_[[10,30,50,70],blocks],'center_ps,D_cm2_s_fit2to8ps')
            am[i].plot(t[:401],y[:401],color=COLORS[j],label=tag.replace('_',' '))
            ab[i].plot([10,30,50,70],blocks/1e-6,'o-',color=COLORS[j],label=tag.replace('_',' '))
            for k,el in enumerate(['Zr','O','Cl']):
                af[i].plot(t[:401],species[el][:401],color=COLORS[j],ls=['-','--',':'][k],label=f'{tag} {el}')
            th=np.loadtxt(p/'thermo.out')[:1600];assert th.shape==(1600,18) and np.isfinite(th).all()
            tt=np.arange(1,1601)*.05;vals=np.c_[th[:,0],th[:,2]/192,th[:,3:6].mean(1)]
            writecsv(key+'_thermo',np.c_[tt,vals],'time_ps,T_K,PE_eV_atom,P_GPa')
            blockmeans=vals.reshape(4,400,3).mean(1)
            for k in range(3):
                at[k,i].plot(tt,vals[:,k],color=COLORS[j],lw=.6,alpha=.35)
                at[k,i].plot([10,30,50,70],blockmeans[:,k],'o-',color=COLORS[j],label=tag.replace('_',' '))
            g=[];cn=[]
            for idx in range(410,801,10):
                gg,cc,_=frame_metrics(Atoms(s,positions=x[idx],cell=c[0],pbc=True),PAIRS,EDGES)
                g.append(gg);cn.append(cc)
            g=np.mean(g,0);cn=np.array(cn)
            writecsv(key+'_RDF',np.column_stack([(EDGES[:-1]+EDGES[1:])/2,*g]),'r_A,Li_Cl,Zr_Cl,Zr_O,Cl_Cl')
            if temp==360:
                for k in range(4):ar.flat[k].plot((EDGES[:-1]+EDGES[1:])/2,g[k],color=COLORS[j],label=tag.replace('_',' '))
            results[key]={'fits':fits,'block_D_cm2_s':blocks.tolist(),'block_SD_not_SE':float(blocks.std(ddof=1)),
                'late_CN':cn.mean(0).tolist(),'T_mean_K':float(vals[:,0].mean()),'P_mean_GPa':float(vals[:,2].mean()),
                'PE_last20_minus_first20_eV_atom':float(blockmeans[-1,1]-blockmeans[0,1]),
                'rho_g_cm3':float(a.get_masses().sum()*1.6605390666/a.get_volume()),
                'sigma_NE_apparent_mS_cm':sigma_mscm(fits[-1]['D_cm2_s'],42,a.get_volume(),temp),
                'MSD40_A2':{el:float(v[400]) for el,v in species.items()}}
            print(key,results[key],flush=True)
        for ax in [am[i],ab[i],af[i]]:ax.set_title(f'{temp} K');ax.legend()
        af[i].legend(loc='upper center',bbox_to_anchor=(.5,-.2),ncol=2)
        am[i].set(xlabel='Lag time (ps)',ylabel='Li MSD (Å²)')
        ab[i].set(xlabel='20 ps block centre (ps)',ylabel='Apparent D (10⁻⁶ cm²/s)')
        af[i].set(xlabel='Lag time (ps)',ylabel='Framework MSD (Å²)')
        for k,label in enumerate(['Temperature (K)','Potential energy (eV/atom)','Pressure (GPa)']):
            at[k,i].set(xlabel='Time (ps)',ylabel=label,title=f'{temp} K' if k==0 else '');at[k,i].legend()
    for ax,(u,v,_) in zip(ar.flat,PAIRS):ax.set(title=f'360 K: {u}–{v}',xlabel='r (Å)',ylabel='g(r)');ax.legend()
    for fig,name in [(fm,'LZOC_matched80_MSD'),(ft,'LZOC_matched80_thermo'),(fr,'LZOC_matched80_RDF'),(fb,'LZOC_matched80_blocks'),(ff,'LZOC_matched80_framework')]:save(fig,name)
    # Local-structure checks: final low-temperature holds are not transport production.
    for name,p,pairs in [
        ('Li3PS4',ROOT/'results/amorphous_validation_20260914/source/Li3PS4/relaxation',[('P','S',2.6),('Li','S',3.2)]),
        ('LiPON',BASE/'source/LiPON',[('P','O',2.1),('P','N',2.1),('N','N',1.6)]),
        ('LSZC',BASE/'source/LSZC_anneal/hold',[('S','O',1.9),('Zr','O',2.6),('Zr','Cl',3.2)])]:
        source.update(hashes(p));frames=read(p/'dump.xyz',index=':');late=frames[len(frames)//2:]
        safe=min(1/np.linalg.norm(np.linalg.inv(a.cell.array),axis=0).max()/2 for a in late)
        edges=EDGES[EDGES<safe]
        assert edges[-1]>max(v for _,_,v in pairs)
        gs=[];cs=[];nn=[];angles=[];hist=[[] for _ in pairs]
        for a in late:
            g,c,_=frame_metrics(a,pairs,edges);gs.append(g);cs.append(c)
            s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf)
            for k,(u,v,cut) in enumerate(pairs):hist[k].extend((d[np.ix_(s==u,s==v)]<cut).sum(1).tolist())
            if name=='Li3PS4':angles.extend(angle_distribution(a,'P','S',2.6))
            if name=='LiPON':nn.append(float(d[np.ix_(s=='N',s=='N')].min()))
        g=np.mean(gs,0);cs=np.array(cs);r=(edges[:-1]+edges[1:])/2
        writecsv(name+'_late_RDF',np.column_stack([r,*g]),'r_A,'+','.join(u+'_'+v for u,v,_ in pairs))
        f,axs=plt.subplots(1,len(pairs),layout='constrained')
        cnprobs={}
        for k,(ax,(u,v,cut)) in enumerate(zip(np.ravel(axs),pairs)):
            counts=np.bincount(hist[k]);probs=counts/counts.sum();cnprobs[u+'-'+v]=probs.tolist()
            ax.plot(np.arange(len(probs)),probs,'o-',color=COLORS[0]);ax.set(title=f'{name}: {u}–{v} (<{cut:g} Å)',xlabel='Neighbour count',ylabel='Atom–frame fraction',ylim=(0,1.05),xticks=np.arange(len(probs)))
            writecsv(name+'_'+u+v+'_CN',np.c_[np.arange(len(probs)),probs],'neighbour_count,atom_frame_fraction')
        save(f,name+'_coordination_distribution')
        th=np.loadtxt(p/'thermo.out');vol=np.linalg.det(th[:,9:].reshape(-1,3,3));rho=a.get_masses().sum()*1.6605390666/vol
        vals=np.c_[th[:,0],th[:,2]/len(a),th[:,3:6].mean(1),rho]
        writecsv(name+'_hold_thermo',np.c_[np.arange(1,len(th)+1)*.05,vals],'time_ps,T_K,PE_eV_atom,P_GPa,rho_g_cm3')
        results[name]={'n_atoms':len(a),'n_late_frames':len(late),'RDF_rmax_A':float(edges[-1]),'late_CN':cs.mean(0).tolist(),'CN_atom_frame_fractions':cnprobs,
            'T_mean_K':float(vals[:,0].mean()),'P_mean_GPa':float(vals[:,2].mean()),'rho_mean_g_cm3':float(rho.mean()),
            'PE_last_half_minus_first_half_eV_atom':float(vals[len(th)//2:,1].mean()-vals[:len(th)//2,1].mean())}
        if name=='Li3PS4':
            ref=np.loadtxt(OUT/'Chen2025_Fig._1e.csv',delimiter=',',skiprows=1)
            refang=np.loadtxt(OUT/'Chen2025_Fig._1f.csv',delimiter=',',skiprows=1)
            f,axs=plt.subplots(1,2,layout='constrained')
            axs[0].plot(r,g[1],label='NEP89: final 10 ps',color=COLORS[0]);axs[0].plot(ref[:,0],ref[:,2],label='Chen 2025: glass',color=COLORS[1],ls='--')
            ae=np.arange(0,181,2);ah=np.histogram(angles,ae,density=True)[0]
            refy=refang[:,2]/np.trapezoid(refang[:,2],refang[:,0])
            axs[1].plot((ae[:-1]+ae[1:])/2,ah,label='NEP89: final 10 ps',color=COLORS[0]);axs[1].plot(refang[:,0],refy,label='Chen 2025: glass',color=COLORS[1],ls='--')
            axs[0].set(title='Li–S RDF',xlabel='r (Å)',ylabel='g(r)',xlim=(0,5))
            axs[1].set(title='S–P–S angles',xlabel='Angle (°)',ylabel='Probability density (degree⁻¹)',xlim=(60,160))
            for ax in axs:ax.legend()
            save(f,'Li3PS4_Chen_structure_comparison')
            writecsv('Li3PS4_angles',np.c_[(ae[:-1]+ae[1:])/2,ah],'angle_degree,density_per_degree')
            results[name]['mean_SPS_angle_degree']=float(np.mean(angles))
        if name=='LiPON':
            allnn=[]
            for a in frames:
                s=np.array(a.get_chemical_symbols());d=a.get_all_distances(mic=True);np.fill_diagonal(d,np.inf);allnn.append(d[np.ix_(s=='N',s=='N')].min())
            f,ax=plt.subplots(layout='constrained');ax.plot(np.arange(1,len(frames)+1)*.1,allnn,color=COLORS[1]);ax.axhline(1.6,color='gray',ls='--',label='Diagnostic cutoff')
            ax.set(title='LiPON: persistent short N–N contact',xlabel='Release time (ps)',ylabel='Minimum N–N distance (Å)');ax.legend();save(f,'LiPON_NN_release')
            writecsv('LiPON_NN_release',np.c_[np.arange(1,len(frames)+1)*.1,allnn],'time_ps,minimum_NN_A')
            results[name]['NN_min_max_A']=[float(min(allnn)),float(max(allnn))]
        if name=='LSZC':
            f,axs=plt.subplots(1,2,layout='constrained')
            for k,(u,v,_) in enumerate(pairs[1:]):
                axs[0].plot(k,cs[:,k+1].mean(),'o',ms=10,color=COLORS[0],label='NEP89 cutoff count' if k==0 else None)
                axs[0].plot(k,[2.6,3.0][k],'s',ms=10,color=COLORS[1],label='Tang 2026 EXAFS fit' if k==0 else None)
                axs[1].plot(r,g[k+1],color=COLORS[k],label=f'{u}–{v}')
                axs[1].axvline([2.23,2.45][k],ls='--',color=COLORS[k],label=f'EXAFS {u}–{v}')
            axs[0].set(title='Different coordination definitions',xticks=[0,1],xticklabels=['Zr–O','Zr–Cl'],ylabel='Coordination number',ylim=(0,5.5));axs[0].legend()
            axs[1].set(title='RDF and EXAFS bond lengths',xlabel='r (Å)',ylabel='g(r)',xlim=(1.5,4));axs[1].legend();save(f,'LSZC_EXAFS_comparison')
            results[name]['EXAFS_reference']={'Zr-O_CN':2.6,'Zr-Cl_CN':3.0,'Zr-O_A':2.23,'Zr-Cl_A':2.45,'DOI':'10.1038/s41467-026-69737-x'}
        print(name,results[name],flush=True)
    rows=[];earows=[]
    for j,tag in enumerate(['MTTK_0.5fs','NHC_2fs']):
        for temp in [340,360,380]:
            v=results[f'LZOC_{temp}K_{tag}']
            for fit in v['fits']:
                rows.append([j,temp,fit['lo_ps'],fit['hi_ps'],fit['D_cm2_s'],fit['R2'],fit['alpha'],fit['intercept_A2']])
        for k,(lo,hi) in enumerate([(5,20),(10,30),(10,40)]):
            ds=np.array([results[f'LZOC_{temp}K_{tag}']['fits'][k]['D_cm2_s'] for temp in [340,360,380]])
            slope,intercept=np.polyfit(1/np.array([340,360,380]),np.log(ds),1)
            earows.append([j,lo,hi,-slope*8.617333262145e-5])
    writecsv('LZOC_fit_table',rows,'setting_0MTTK_1NHC,T_K,lag_lo_ps,lag_hi_ps,D_app_cm2_s,R2,log_log_alpha,intercept_A2')
    writecsv('LZOC_Ea_diagnostic_NOT_validated',earows,'setting_0MTTK_1NHC,lag_lo_ps,lag_hi_ps,diagnostic_Ea_eV')
    (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    (OUT/'source_hashes.json').write_text(json.dumps(source,indent=2)+'\n')

if __name__=='__main__':run()
