"""Package already computed, reviewed results for the inline data renderer."""
from pathlib import Path
import json
import numpy as np
p=Path(__file__).resolve().parent
a=json.loads((p/'results.json').read_text())
rows=[]
for key,v in a.items():
    x=np.loadtxt(p/f'{key}_equilibration_thermo.csv',delimiter=',',skiprows=1)
    for lo in range(50):
        b=x[(x[:,0]>=lo)&(x[:,0]<lo+1)]
        rows.append(dict(time_ps=lo+.5,density_g_cm3=float(b[:,6].mean()),run=key))
source=dict(label='TSUBAME LZOC: MACE 8635176 / NEP89 8635527',files=[dict(label='NPT log.lammps / thermo.out')],
    filters=['192 atoms, Li42Zr24O12Cl114','NPT stage only: 0–50 ps'],
    caveats=['One structure and one branch per temperature.','Lines show 1 ps block means; the MD used 0.05 ps thermodynamic sampling.','Density is a simulation result, not an experimental measurement.'],
    evidenceFlow=[dict(kind='calculation',title='Density',detail='LAMMPS density column; GPUMD density from total atomic mass / determinant of the instantaneous cell. 1 ps block averaging is for display only.')])
chart=dict(schemaVersion=1,id='lzoc-npt-density',title='LZOC — NPT density evolution',chart=dict(type='line',x='time_ps',y='density_g_cm3',series='run',xLabel='NPT time (ps)',yLabel='Density (g/cm³)',showXAxisLabel=True),rows=rows,source=source)
(p/'density_chart.json').write_text(json.dumps(chart,indent=2))
receipt=dict(schemaVersion=1,items=[dict(id='density',title='NPT density changes',queries=[dict(id='density-blocks',source=source,columns=['time_ps','density_g_cm3','run'],rows=rows)])])
(p/'density_sources.json').write_text(json.dumps(receipt,indent=2))
summary=[]
for key,v in a.items():
    summary.append(dict(run=key,T_mean_K=v['thermo']['T_K']['mean'],T_sd_K=v['thermo']['T_K']['sd'],D_cm2_s=v['fit_windows']['20-80']['D_cm2_s'],MSD_fit_R2=v['fit_windows']['20-80']['R2'],Zr_MSD_200ps_A2=v['species']['Zr']['MSD_200ps_A2'],Cl_MSD_200ps_A2=v['species']['Cl']['MSD_200ps_A2']))
src=dict(label='TSUBAME production trajectories and thermodynamic logs',files=[dict(label='MACE jobs 8635176.1–4'),dict(label='NEP89 job 8635527'),dict(label='analyze_lzoc_production.py'),dict(label='results.json / arrhenius.json')],
    caveats=['Single structure, single run per condition; no independent-replica uncertainty.','20–80 ps lag fit is provisional, not a percentage of production.','MACE density expansion and framework motion limit the interpretation as solid-state Li diffusion.','NEP89 includes extra minimization and uses a different integrator.','NEP89 has one temperature only: activation energy cannot be fitted.'],
    filters=['Only the 200 ps NVT production stage','Li diffusion uses all 42 Li atoms','System mass-weighted COM motion removed'],
    evidenceFlow=[dict(kind='validation',title='Source and algorithm checks',detail='Five downloaded production trajectory SHA256 hashes match TSUBAME. Each has 192 atoms and 2001 analysis frames, including the GPUMD t=0 input frame. FFT MSD matches direct calculation at five real trajectory lags; three algorithm tests passed.'),dict(kind='calculation',title='MSD and activation energy',detail='Time-origin averaged MSD, affine slope on 20–80 ps lag. D = slope/6 × 1e−4 cm²/s. MACE ln(D) versus 1/T: Ea=0.20543958 eV, R²=0.97725156. Across six lag windows Ea=0.17621635–0.20543958 eV; descriptive, not a validated solid-state migration barrier.')])
(p/'analysis_sources.json').write_text(json.dumps(dict(schemaVersion=1,items=[dict(id='transport-structure',title='Production transport and structure checks',queries=[dict(id='production-summary',source=src,columns=list(summary[0]),rows=summary)])]),indent=2))
