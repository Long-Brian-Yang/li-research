# NEP89 exploratory branch — 600 K, one run

Submitted 2026-09-11 as TSUBAME job **8635527**, group tgj-26ICP,
one gpu_1, four-hour wall-time limit. Submission does not establish that
compilation, smoke testing or production have completed.
Output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/nep89/600K_R1_8635527/`.
Uploaded model SHA256: 75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1.
Uploaded model.xyz SHA256: 89de0e0eb18f5fc1d5f36d507bfbe68e77d2e465f64961c174608e980a99fd8e.

GPUMD v5.0, commit 05982941c85b257fdf5a5c69fb7922ce7d7a5c80.
Official potential: GPUMD potentials/nep/nep89_20250409/nep89_20250409.txt.
Source: https://github.com/brucefan1983/GPUMD/tree/v5.0

model.xyz preserves the 192 atoms and triclinic cell of
LZOC/structure_equilibrated_300K.data, SHA256
7450a1a366025fa4094eba6ce414698b2bcc67a6c86cc53c6c9dd2046ce4c584.
Composition: Li42Zr24O12Cl114. Coordinates are periodically wrapped;
MACE velocities are intentionally not copied. Element coverage is verified,
but is not evidence of model accuracy for this composition.

Separate NEP fixed-cell FIRE minimization (force threshold 0.01 eV/Å,
maximum 10000 iterations), then 1 ps 300 K GPU smoke test. The pipeline stops
if minimization fails its force threshold, a stage is incomplete, or thermo
contains nonfinite values or temperatures outside 0–3000 K.
These are numerical gates, not proof of structural validity or convergence.

Then 10 ps 300→600 K NVT ramp, 50 ps 600 K isotropic 1 bar NPT,
200 ps 600 K NVT at the terminal NPT cell. MTTK thermostat/barostat,
dt=0.5 fs, tperiod=200 steps (0.1 ps), pperiod=2000 steps (1 ps).
GPUMD pressure input is GPa: 1 bar = 0.0001 GPa.
Initial velocity seed=20260912. Subsequent stages retain restart velocities.
Source cell shape is preserved during isotropic NPT.

This differs from the MACE branch by an additional NEP minimization and
smoke stage, and by integrator implementation. It is not an identical-state
benchmark. After production, evaluate density, RDF and stationarity before
accepting diffusion results. Do not mix these trajectories with MACE.

Thermo every 0.05 ps; extended XYZ every 0.1 ps including velocities,
forces and potential energies; restart.xyz every 1 ps. Stages have separate
directories. Wrapped GPUMD positions must be unwrapped using the periodic
cell and temporal continuity for subsequent MSD analysis.

Job script: hpc/tsubame_26icp/production/lzoc_nep89.sh.
Only the GPU MD executable is built, not NEP training tools or GPUMDKit.
