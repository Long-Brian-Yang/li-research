# 0.5Li2SO4-ZrCl4: author structure / NEP89 preflight

## Current scope (2026-09-14)

### Authorized 272-atom continuation

Pressure-release task8674095 submitted; output `runs/amorphous/LSZC/nep89/seed272_release_8674095/`,group tgj-26ICP,gpu_1,10-minute limit.

2026-09-15 inspection of job8671205: 3 ps density block means2.42319,2.48072,2.47635,2.50074 g/cm3; final2.51976 versus starting1.86376. Last3 ps T299.403 K,P0.47940 GPa. Final minimum distance1.40517 A; all16 S have4 O within1.9 A (fixed diagnostic cutoff). Density is substantially above author Data2's2.03549 g/cm3, which is a model reference, not an experimental acceptance threshold. Hold the scheduled heating. User-authorized continuation uses a separate300 K1 bar20 ps isotropic NPT pressure-release diagnostic,0.5 fs,retained velocities,MTTK periods100/1000 fs. This is a project diagnostic NOT the published protocol. No automatic density-fitting pressure search,heating orproduction.

First bounded step: `seed_272/run.in`, 300 K NPT, isotropic 0.5 GPa (=5 kbar), 12 ps. Temperature, pressure and duration follow Supplementary Fig. 20, page 16. NEP89, 0.5 fs timestep, MTTK thermostat/barostat periods 100 fs/1 ps and the replicated seed are OUR adaptations, not the author's fine-tuned MACE reproduction. The figure next specifies 300–400 K heating at 1 K/ps; that stage is held pending density/structure checks. No density-matching pressure search or transport is automatic. Crucially, this seed is not the author's packed amorphous cluster model, and low-temperature equilibration alone does not prove amorphization.

User considers 136 atoms too small. Prepared `seed_272/initial_structure.cif` and `seed_272/model.xyz` by repeating Data 1 along the shortest axis (1x2x1): Li32 Zr32 Cl128 S16 O64. This preserves parent density and composition but repeats its local structure; it is NOT an equilibrated amorphous structure. No 272-atom MD submitted yet. `input/` remains the completed 1088-atom diagnostic provenance and must not be confused with `seed_272/`.

User requested a smaller model instead of 1088 atoms. The 1088-atom diagnostic 8671146 already completed; no continuation is authorized/planned. Author Data 1 provides a 136-atom AIMD seed (Li16 Zr16 Cl64 S8 O32); it is NOT the final amorphous structure and requires reconstruction/validation before glass transport analysis. The input directory below still records the completed 1088-atom diagnostic, not a prepared 136-atom job.

Source: Tang et al., *Polyanion-stabilized amorphous halide electrolytes with low lithium content for all-solid-state lithium batteries*, Nature Communications 17, 3326 (2026), https://doi.org/10.1038/s41467-026-69737-x.

Publisher ZIP: https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41467-026-69737-x/MediaObjects/41467_2026_69737_MOESM3_ESM.zip

Data 1 is an optimized crystal-unit model for AIMD sampling (136 atoms). Data 2 is the optimized amorphous MACE model (1088 atoms); Data 3 is the final MLFF-MD configuration. Data 2 was used for the completed diagnostic; Data 1 is the source of the new 272-atom seed. These are three structure snapshots, NOT full DFT force/energy training trajectories. No trained checkpoint is included in this ZIP.

Input composition: Li128 Zr128 Cl512 S64 O256. Orthogonal cell: 37.58492917 x 26.60036590 x 30.07934277 A. Density 2.03549388 g/cm3. Minimum periodic interatomic distance 1.44162570 A. No replication, substitutions or melt-quench were applied.

## Bounded diagnostic, not reproduction or production

- Existing NEP89 (20250409) / GPUMD; author used system-finetuned MACE.
- Initial static CPU NEP: energy -5.40399724 eV/atom, max force 2.96753667 eV/A, pressure -1.43242892 GPa (compression positive).
- 300 K NVT MTTK, dt 0.5 fs, thermostat period 200 steps, seed 20260914; 20000 steps = 10 ps.
- Fixed author cell, no prior minimization: this intentionally tests response to the potential change. Initial transient is not equilibrated production.
- gpu_1, 10-minute wall-clock ceiling; no automatic continuation.
- Inspect sulfate coordination, RDF, temperature, energy and pressure before any production. Numerical survival is not a DFT accuracy test.

Experimental reference in the paper: 1.5 mS/cm at 30 C, Ea 0.33 eV. Neither is a fitting target. A 10 ps run cannot provide reliable room-temperature conductivity.

Original publisher files retained locally and on the project filesystem for provenance. Public redistribution/licensing must be checked before GitHub upload.
