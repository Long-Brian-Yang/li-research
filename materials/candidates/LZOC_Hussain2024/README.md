# Li1.75ZrCl4.75O0.5 — Hussain 2024 reference audit

Source: https://doi.org/10.1038/s41524-024-01346-y
Supplement: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41524-024-01346-y/MediaObjects/41524_2024_1346_MOESM1_ESM.pdf

Separate from older Kim2025-derived LZOC candidates. New reconstructed192-atom trial submitted as job8671250 (group tgj-26ICP), output `runs/amorphous/LZOC_Hussain2024/nep89/trial_8671250`. Submission does not establish successful execution.

## Newly authorized trial

User authorized a reconstructed seed. `seed_192` now contains a 2x2x2 realization of Table 2: Li42 Zr24 Cl114 O12. Integer quotas preserve the rounded site occupancies and exact stoichiometry. A fixed random objective selects a feasible configuration under distance exclusions; this is NOT electrostatic/DFT ground-state selection. Initial minimum distance 2.3632 A, density 2.2340 g/cm3. No old LZOC coordinates reused.

The first bounded GPUMD trial uses NEP89, fixed-cell FIRE relaxation (0.01 eV/A, ceiling10000 steps), 100 K2 ps then500 K30 ps, following the first two durations of the96-atom branch. Our adaptations:192 atoms,0.5 fs,MTTK100 fs thermostat,NEP instead ofDFT. Inspect optimization convergence,temperature,energy,coordination and cell before hotter stages. No2000 K melt,quench ortransport is automatically submitted. A successful32 ps run cannot establish amorphization orpotential accuracy.

## Verified 96-atom protocol (SI page 23)

| Stage | Temperature K | Time ps |
|---|---:|---:|
| Heating | 100 | 2 |
| Heating | 500 | 30 |
| Heating | 1000 | 50 |
| Heating | 1500 | 30 |
| Melting | 2000 | 20 |
| Relaxation | spin-polarized DFT, positions and volume | not MD |
| Cooling | 1500 / 1000 / 500 / 100 | 2 at each temperature |
| Final equilibration | 300 | 20 |

The paper's 340/360/380 K transport study belongs to the smaller 48-atom branch, not the 96-atom branch. The smaller branch describes conflicting 80/100 ps residence at 1000 K. Do not merge branches without documenting the adaptation.

## Structure limitation

SI Table 2 provides P-3m1 average sites with fractional occupancies and a=10.937 A,c=6.022 A, not the author's ordered atomic configuration. Mixed O/Cl sites and Li/Zr vacancies need discrete occupation assignment and relaxation. Reconstructing such a configuration is a new model, not recovery of original coordinates. Do not reuse old candidate3 and relabel it as Hussain2024.

NEP89/GPUMD substitution for DFT/AIMD, a larger cell, thermostat parameters, and any volume-relaxation replacement must be explicitly documented. No transport production before numerical and structural checks. User approved reconstructed starting structure.

Initial static NEP: -4.395256698 eV/atom, max force4.637612358 eV/A, pressure-3.918993932 GPa. This is an unrelaxed structure, not evidence of equilibrium. Composition/geometry/CIF roundtrip unit test passed; submission script passed bash syntax check.

## NEP high-temperature continuation (2026-09-15)

Heating completed. Preliminary 2000 K diagnostic:200 frames separated by0.1 ps, MIC accumulated displacements with arithmetic mean translation removed; endpoint MSD Li586.88,Cl157.07,O65.63,Zr63.42 A2 over19.9 ps. Minimum pair distance sampled every10frames1.64289 A. Strong framework mobility supports cooling exploration, not proof of complete melting or accuracy.

Cooling job8674094 submitted: fixed-cell NEP FIRE positions only (target0.01 eV/A,max10000 steps), new1500 K velocities seed20260915,1500/1000/500/100 K each2 ps then300 K20 ps. Total28 ps. Deliberate deviation: author's post-melt DFT cell relaxation NOT performed. Final pressure/structure must be checked before ambient-pressure claims or further transport. Output `runs/amorphous/LZOC_Hussain2024/nep89/cooling_8674094/`.

Submitted job8673813, group tgj-26ICP, gpu_1,15-minute wall limit. Output `runs/amorphous/LZOC_Hussain2024/nep89/heating_8673813/`. No completion claimed at submission.

Trial8671250 completed32 ps in54.75 s. Last10 ps mean temperature496.053 K, pressure-0.0754417 GPa. This verifies finite numerical execution, not convergence of the initial minimization or amorphous character.
User authorized NEP exploration. Continue from the pinned500 K restart with1000 K50 ps,1500 K30 ps,2000 K20 ps. Retain positions/velocities, reinitialize MTTK each stage, fixed cell,0.5 fs. Separate stage trajectories and thermo are retained. The author's subsequent DFT position/volume relaxation is not silently replaced; stop after heating to examine framework motion, RDF and coordination before choosing an explicitly documented NEP relaxation/cooling adaptation.
