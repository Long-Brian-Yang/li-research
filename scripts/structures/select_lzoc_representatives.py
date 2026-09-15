"""Exploratory stability-ranked display selection; no AIMD values are loaded."""
import json
import numpy as np
from analyze_followup300 import BASE
from analyze_lzoc_production import fit_msd

def main():
    candidates=[];selected=[]
    windows=[(20,80),(20,100),(20,150),(40,150),(50,200)]
    for T in [340,360,380]:
        sources=[(f'8676684.{[340,360,380].index(T)+1}',BASE/f'followup300/LZOC_{T}K_300ps_MSD.csv')]
        if T!=380:
            sources += [(f'8677221.{rep+(0 if T==340 else 2)}',BASE/f'seed_repeats/LZOC_{T}K_R{rep}_MSD.csv') for rep in [1,2]]
        local=[]
        for job,path in sources:
            a=np.loadtxt(path,delimiter=',',skiprows=1)
            for lo,hi in windows:
                f=fit_msd(a[:,0],a[:,1],lo,hi)
                neighbours=[fit_msd(a[:,0],a[:,1],lo+d,hi+d)['D_cm2_s'] for d in [-10,10]]
                change=max(abs(x/f['D_cm2_s']-1) for x in neighbours) if f['D_cm2_s']>0 else float('inf')
                local.append(dict(T_K=T,job=job,source=str(path.relative_to(BASE)),**f,neighbor_change=change))
        eligible=[r for r in local if r['D_cm2_s']>0 and r['R2']>=.99]
        assert eligible, f'No eligible representative at {T}'
        best=min(eligible,key=lambda r:(r['neighbor_change'],-(r['hi_ps']-r['lo_ps']),-r['R2']))
        selected.append(best);candidates.extend(local)
    result={'selection_rule':'Post-analysis exploratory selection: five prespecified-for-this-audit windows, positive slope and R2 >=0.99; rank by max relative slope change when translating window by +/-10 ps, then longer duration, then R2. Does not establish asymptotic diffusion or an unbiased population estimate. No AIMD values used. Original and repeat histories differ; all source records retained.',
            'selected':selected,'candidates':candidates}
    (BASE/'seed_repeats/representatives.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(selected,indent=2))

if __name__=='__main__':main()
