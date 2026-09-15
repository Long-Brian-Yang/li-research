# LiPON NEP89 / GPUMD preparation trial

## 2026-09-15 diagnostic continuation

Submitted job8674143,group tgj-26ICP,gpu_1,10-minute wall limit. Output `runs/amorphous/LiPON/nep89/release_8674143/`. Original preparation data retained unchanged.

User authorized continuing investigation. Prior20 ps250 K NVT mean pressure-2.80025 GPa and persistent N-N below1.6 A remain unresolved. A separate250 K,1 bar,20 ps isotropic NPT trial releases fixed volume without altering species or contacts. Keep0.5 fs,MTTK100/1000 fs,retain velocities; extended barostat/thermostat state reinitialized. This is our diagnostic,not the author's preparation or transport production. Related-composition DFT force RMSE0.4301 eV/A means pressure stabilization alone cannot validate NEP chemistry. Review N-N distances,P-N/P-O coordination,density and stress before further work.

Reference: Seth et al., *Investigating Ionic Diffusivity in Amorphous LiPON using Machine-Learned Interatomic Potentials*, ACS Materials Au 5, 458–468 (2025), https://doi.org/10.1021/acsmaterialsau.4c00117.
Author manuscript: https://sai-mat-group.github.io/pdfs/papers/seth-acsmaterau-2025.pdf, Methods p.460.

This is an independent NEP89 evaluation following the 2025 composition and preparation schedule, NOT a NequIP or AIMD reproduction, and not the exact experimental sample of the separate 2018 JACS study.

## Input

Author repository https://github.com/sai-mat-group/ann-lipon, revision `1818171dc4423404dc292c51f7593a7366a6599f`.
Parent: `DFT Dataset/Initial_set of_structures/Input_files_mp_13725/CONTCAR`, relaxed Li6P2O8.
Repeat 2x2x2 -> Li48P16O64. Replace 5 O with N; remove 3 additional O and 1 Li -> Li47P16O56N5, 124 atoms, formally charge neutral. Exact normalized formula Li2.9375PO3.5N0.3125.

Substitution/removal pattern is independently generated using seed 20260914, not the unpublished author pattern. All zero-based parent indices and hashes are in validation.json. No optimization toward a desired diffusion result.

Cell: 9.797107 x 10.542271 x 12.293883 Angstrom. Initial density 2.337933 g/cm3. Minimum periodic distance 1.557936 Angstrom. Source CONTCAR, initial CIF and GPUMD xyz retained together. This is a crystalline-derived precursor, not a certified amorphous configuration.

## Single preparation trial

| Stage | Setting | Duration | Source |
|---|---|---|---|
| Atomic minimization | fixed cell FIRE 0.01 eV/A, max 10000 iterations | convergence-limited | diagnostic choice |
| Smoke | NVT 300 K | 1 ps | diagnostic choice |
| Heating | NVT 300 to 2000 K | 5 ps | diagnostic choice |
| Melt | NVT 2000 K | 10 ps | paper Methods |
| Quench | NVT 2000 to 250 K, 250 K/ps | 7 ps | paper Methods |
| Relaxation diagnostic | NVT 250 K | 20 ps | diagnostic choice, not presumed equilibrated |

Total 43 ps. Timestep 0.5 fs, deliberately smaller than paper's 1 fs preparation step; GPUMD MTTK thermostat period 200 timesteps (100 fs), project choice. No NPT density adjustment, no interfaces, no production diffusion fit. Fixed density can impose residual pressure and must be checked rather than interpreted as proof of equilibrium.

Existing runtime: `engines/gpumd/source/src/gpumd`; model `models/nep89/nep/nep89_20250409/nep89_20250409.txt`, under `/gs/fs/tgj-26ICP/uf03782/yang/li-research`.
Job: `hpc/tsubame_26icp/production/lipon_nep89_trial.sh`. One gpu_1 slot, 15 minute walltime ceiling, not a runtime forecast.

Before production: check completion and temperature/energy/pressure; periodic pair distances, P-O/P-N coordination and N bridging, loss of crystalline order, and force accuracy against available DFT data. Finite outputs do not establish model accuracy or successful glass formation. Element coverage alone is insufficient.
