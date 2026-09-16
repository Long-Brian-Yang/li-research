"""Three MACE candidates: residual initial order and stage-specific motion.

Python-only quantitative grids, source-backed PNG/PDF/SVG. Structural projections
are not migration paths; reciprocal intensity is not a crystalline fraction.
"""
from pathlib import Path
from collections import Counter
import itertools,json,hashlib,sys
import numpy as np
from ase.io import read
sys.path.insert(0,str(Path(__file__).resolve().parent))
from compare_lzoc_candidates import EXPECTED_HASH
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'materials/candidates/LZOC/archive/completed_reference_trials'
OUT=ROOT/'docs/daily_reports/2026-09-14/figures'
MASS={'Li':6.94,'Zr':91.224,'O':15.999,'Cl':35.45}
ELEMENTS=list(MASS)

def read_unwrapped(path):
    t=[];xs=[];hs=[];orig=[];symbols=None
    for block in path.read_text().split('ITEM: TIMESTEP\n')[1:]:
        ls=block.splitlines();t.append(int(ls[0])*.0005)
        assert int(ls[2])==192 and 'xy xz yz' in ls[3]
        b=np.array([list(map(float,l.split())) for l in ls[4:7]])
        xy,xz,yz=b[:,2]
        lo=np.array([b[0,0]-min(0,xy,xz,xy+xz),b[1,0]-min(0,yz),b[2,0]])
        hi=np.array([b[0,1]-max(0,xy,xz,xy+xz),b[1,1]-max(0,yz),b[2,1]])
        length=hi-lo;h=np.array([[length[0],0,0],[xy,length[1],0],[xz,yz,length[2]]])
        cols=ls[7].split()[2:];rows=sorted([l.split() for l in ls[8:]],key=lambda r:int(r[0]))
        assert [int(r[0]) for r in rows]==list(range(1,193))
        sy=[r[cols.index('element')] for r in rows]
        if symbols is None:symbols=sy
        assert sy==symbols
        xs.append([[float(r[cols.index(c)]) for c in ['xu','yu','zu']] for r in rows]);hs.append(h);orig.append(lo)
    assert Counter(symbols)==Counter(Li=42,Zr=24,O=12,Cl=114)
    t=np.array(t);assert np.allclose(t,np.arange(1101)*.05)
    return t,np.array(xs),np.array(hs),np.array(orig),np.array(symbols)

def displacements(x,h,origin,masses):
    s=np.einsum('tni,tij->tnj',x-origin[:,None,:],np.linalg.inv(h))
    # xu already unwrapped: do not apply image flags or round fractional increments.
    ds=np.diff(s,axis=0)
    dr=np.einsum('tni,tij->tnj',ds,(h[1:]+h[:-1])/2)
    d=np.concatenate([np.zeros_like(x[:1]),np.cumsum(dr,axis=0)])
    return d-np.average(d,axis=1,weights=masses)[:,None,:]

def main():
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':13,'axes.titlesize':16,
        'axes.labelsize':14,'lines.linewidth':1.8,'pdf.fonttype':42,'svg.fonttype':'none'})
    OUT.mkdir(exist_ok=True,parents=True)
    cols=['#32688E','#B37525','#766097'];ec=['#32688E','#B37525','#C25454','#766097']
    stages=[('1500 K NVT',0,10),('Cooling NVT',10,40),('300 K NVT',40,45),('300 K NPT',45,55)]
    motion,ma=plt.subplots(4,3,figsize=(13,12),sharey='row')
    order,oa=plt.subplots(1,2,figsize=(11,4.8))
    structures,sa=plt.subplots(2,3,figsize=(11,7.5),sharex=True,sharey=True)
    summary={}
    for i in (1,2,3):
        p=BASE/f'source_{i}/candidate.lammpstrj';sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==EXPECTED_HASH[i-1]
        t,x,h,origin,sy=read_unwrapped(p);mass=np.array([MASS[e] for e in sy])
        assert np.isfinite(x).all() and (np.linalg.det(h)>0).all()
        # Isotropic NPT changes scale only: no cell-flip representation jumps.
        assert np.allclose(h/np.cbrt(np.linalg.det(h))[:,None,None],h[0]/np.cbrt(np.linalg.det(h[0])),atol=1e-5)
        ref=read(BASE/f'source_{i}/initial_minimized.data',format='lammps-data',atom_style='atomic',Z_of_type={1:3,2:40,3:8,4:17})
        assert np.array_equal(ref.get_chemical_symbols(),sy)
        last=read(p,format='lammps-dump-text',index=-1)
        assert np.allclose(last.cell,h[-1])
        entry={'sha256':sha,'stages':{},'order':{}}
        for j,(name,lo,hi) in enumerate(stages):
            mask=(t>=lo)&(t<=hi);d=displacements(x[mask],h[mask],origin[mask],mass)
            values=np.array([(d[:,sy==e]**2).sum(axis=2).mean(axis=1) for e in ELEMENTS]).T
            if hi<=45:
                raw=x[mask]-x[mask][0];raw-=np.average(raw,axis=1,weights=mass)[:,None,:]
                assert np.allclose(d,raw,atol=1e-7)
            for k,e in enumerate(ELEMENTS):ma[j,i-1].plot(t[mask]-lo,values[:,k],color=ec[k],ls=['-','--','-.',':'][k],label=e)
            ma[j,i-1].set_xlim(0,hi-lo);ma[j,i-1].set_xlabel('Time within stage (ps)')
            if i==1:ma[j,0].set_ylabel(name+'\nMSD (Å²)')
            entry['stages'][name]={'start_ps':lo,'end_ps':hi,'endpoint_MSD_A2':dict(zip(ELEMENTS,values[-1].tolist()))}
            np.savetxt(OUT/f'candidate_{i}_stage_{j+1}_msd.csv',np.column_stack([t[mask]-lo,values]),delimiter=',',header='stage_time_ps,Li_A2,Zr_A2,O_A2,Cl_A2',comments='')
        ma[0,i-1].set_title(f'Candidate {i}')
        hh=np.array([v for v in itertools.product(range(-8,9),repeat=3) if v!=(0,0,0) and next(z for z in v if z)>0])
        q=2*np.pi*np.linalg.norm(hh@ref.cell.reciprocal(),axis=1);hh=hh[(q>=1)&(q<=5)]
        sample=np.arange(1000,1101,5)
        frac=np.einsum('tni,tij->tnj',x[sample]-origin[sample,None,:],np.linalg.inv(h[sample]))
        for j,e in enumerate(['Cl','Zr']):
            mask=sy==e;n=mask.sum();s0=ref.get_scaled_positions()[mask]
            I0=abs(np.exp(2j*np.pi*s0@hh.T).sum(axis=0))**2/n
            top=np.argsort(I0)[-10:][::-1];selected=hh[top]
            It=abs(np.exp(2j*np.pi*np.einsum('tni,ki->tnk',frac[:,mask],selected)).sum(axis=1))**2/n
            ratio=It.sum(axis=1)/I0[top].sum()
            entry['order'][e]={'hkl':selected.tolist(),'initial_intensity':I0[top].tolist(),'late_ratio_mean':float(ratio.mean())}
            oa[j].plot(t[sample],ratio,color=cols[i-1],ls=['-','--','-.'][i-1],label=f'Candidate {i}')
            np.savetxt(OUT/f'candidate_{i}_{e}_order.csv',np.column_stack([t[sample],ratio]),delimiter=',',header='time_ps,initial_peak_intensity_retention',comments='')
        for row,s in enumerate([ref.get_scaled_positions()%1,frac[-1]%1]):
            for k,e in enumerate(ELEMENTS):sa[row,i-1].scatter(s[sy==e,0],s[sy==e,1],s=20 if e!='Cl' else 12,color=ec[k],alpha=.65,label=e,marker=['o','s','^','.'][k])
            sa[row,i-1].set_xlim(0,1);sa[row,i-1].set_ylim(0,1);sa[row,i-1].set_aspect('equal');sa[row,i-1].set_xlabel('Fractional a')
        sa[0,i-1].set_title(f'Candidate {i}')
        summary[str(i)]=entry
    ma[0,2].legend(fontsize=10,loc='upper left',ncol=2)
    motion.suptitle('LZOC — stage-specific atomic motion',fontsize=20)
    motion.text(.5,.005,'Single-origin, all-atom mass-COM corrected; NPT excludes affine cell deformation. No D fit.',ha='center',fontsize=11)
    for j,e in enumerate(['Cl','Zr']):
        oa[j].set(title=e+' initial-peak retention',xlabel='Preparation time (ps)',ylabel='Intensity / initial intensity',xlim=(50,55),ylim=(0,1.05))
        oa[j].axhline(1,color='.6',ls=':',lw=1)
    oa[0].legend(fontsize=11)
    order.suptitle('LZOC — residual initial order (not crystalline fraction)',fontsize=18)
    sa[0,0].set_ylabel('Initial minimized\nFractional b');sa[1,0].set_ylabel('55 ps finite-T endpoint\nFractional b')
    structures.suptitle('LZOC — wrapped fractional projections',fontsize=19)
    handles,labels=sa[0,0].get_legend_handles_labels();structures.legend(handles,labels,ncol=4,loc='lower center')
    for fig,axs,name in [(motion,ma,'LZOC_three_candidate_stage_MSD'),(order,oa,'LZOC_three_candidate_initial_order'),(structures,sa,'LZOC_three_candidate_structure_projection')]:
        for ax in axs.flat:ax.grid(alpha=.15)
        fig.tight_layout(rect=[0,.04,1,.95])
        for ext in ('png','pdf','svg'):
            dest=OUT/f'{name}.{ext}';fig.savefig(dest,dpi=180)
            if ext=='svg':dest.write_text('\n'.join(l.rstrip() for l in dest.read_text().splitlines())+'\n')
        plt.close(fig)
    (OUT/'candidate_order_motion_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
