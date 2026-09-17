"""Compare self MSD with SI Table 4 tracer D*, not charge D."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from paper_aligned_analysis import BASE,OUT,save

def main():
    source=np.loadtxt(BASE/'final_comparisons/LZOC_fit_table.csv',delimiter=',',skiprows=1)
    temperatures=np.array([340,360,380])
    tracer=np.array([2.09,1.77,3.50])*1e-6
    error=np.array([.06,.04,.10])*1e-6
    charge=np.array([2.66,3.03,6.02])*1e-6
    series=[]
    for setting in [0,1]:
        selected=source[(source[:,0]==setting)&(source[:,2]==10)&(source[:,3]==40)]
        selected=selected[np.argsort(selected[:,1])]
        np.testing.assert_array_equal(selected[:,1],temperatures)
        series.append(selected[:,4])
    np.savetxt(OUT/'LZOC_Table4_comparison.csv',np.column_stack([temperatures,tracer,error,charge,*series,series[0]/tracer,series[1]/tracer]),delimiter=',',header='T_K,paper_tracer_D_cm2_s,paper_tracer_reported_plusminus,paper_charge_D_cm2_s,NEP_MTTK_D_app_cm2_s,NEP_NHC_D_app_cm2_s,MTTK_over_tracer,NHC_over_tracer',comments='')
    f,ax=plt.subplots(layout='constrained')
    ax.errorbar(temperatures,tracer,yerr=error,fmt='ko-',label='AIMD tracer D*: SI Table 4')
    for y,label,c in zip(series,['NEP: MTTK, 0.5 fs','NEP: NHC, 2 fs'],['#31688e','#d73027']):
        ax.plot(temperatures,y,'o--',label=label,color=c)
    ax.set(yscale='log',xlabel='Temperature (K)',ylabel='D (cm²/s)',title='LZOC: same-temperature comparison')
    ax.legend();save(f,'LZOC_Table4_comparison')

if __name__=='__main__':main()
