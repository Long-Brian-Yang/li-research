# Li3PS4: NEP89 / GPUMD preparation trial

Status: input validated locally; scheduler status recorded separately. This is a NEP89 evaluation, not a reproduction of the original DeePMD potential. No diffusion or glass-validation result is claimed yet.

## Traceable starting structure

Reference: Chen et al., *Disorder-induced enhancement of lithium-ion transport in solid-state electrolytes*, Nature Communications 16, 1057 (2025), https://doi.org/10.1038/s41467-025-56322-x.

Source: https://github.com/OxideGlassGroupAAU/LiPS at revision `552d32c1f800cc51776a3d8c055399c29f521c31`.
Directory: `data.init/init_data/beta-Li3PS4/3000K/deepmd/Li24P8S32`.
Files: coord.raw, box.raw, type.raw, type_map.raw; hashes in validation.json.

The zero-based first training frame is repeated 2x2x2 to yield 512 atoms: Li192 P64 S256. This is a dataset-derived melt starting configuration, NOT a certified relaxed crystal or author's final glass. No atoms are substituted or deleted. The source's 3000 K training label is not the glass preparation temperature.

Initial orthogonal cell: 25.6380 x 16.4400 x 24.4940 Angstrom. Density 1.853264 g/cm3; minimum periodic pair distance 2.002797 Angstrom. `input/initial.cif` and `input/model.xyz` describe the same initial coordinates.

## Protocol and deviations

| Stage | Ensemble / temperature | Duration | Basis |
|---|---|---|---|
| Position minimization | FIRE, fixed cell, force target 0.01 eV/A | max 10000 iterations | project diagnostic |
| Smoke | NVT 300 K | 1 ps | project diagnostic |
| Heating | NPT 300 to 1500 K | 10 ps | project heating-duration choice |
| Melt | NPT 1500 K | 100 ps | paper Methods |
| Quench | NPT 1500 to 300 K | 480 ps, 2.5 K/ps | paper Methods |
| Relaxation check | NPT 300 K | 20 ps | project diagnostic, not presumed equilibrated |

All MD: 0.5 fs timestep. GPUMD MTTK, isotropic 1 bar (0.0001 GPa), thermostat/barostat periods 200/2000 timesteps (100/1000 fs), seed 20260914. Pressure value, coupling periods, isotropic constraint, initial frame, cell size and final 20 ps are explicitly project choices, not asserted author settings. The inspected repository tree did not contain the simulation templates mentioned in the paper.

Total MD preparation: 611 ps. One gpu_1 slot, one-hour scheduler ceiling, NOT a predicted runtime or point charge. Numerical failures stop stage advancement. Volume range 0.5–2 times starting volume and T<5000 K are emergency checks, not physical acceptance criteria. No automatic long production follows.

## Runtime and required review

- Executable: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/engines/gpumd/source/src/gpumd`
- Potential: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/models/nep89/nep/nep89_20250409/nep89_20250409.txt`
- Job: `hpc/tsubame_26icp/production/lips_nep89_trial.sh`
- Results: `runs/amorphous/Li3PS4/nep89/preparation_JOBID/`, independent of earlier LZOC runs.

Before production: inspect actual stage completion; density and energy trends; P-S coordination and S-P-S angles; RDF/structure factor for loss of long-range order; short-distance outliers and framework mobility; compare NEP89 forces against available DFT frames. A numerical smoke-test pass alone does not validate NEP89 accuracy or prove glass formation.
