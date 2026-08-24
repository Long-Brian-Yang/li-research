# Source code

`src/` contains reusable Python code only. It does not contain TSUBAME job
scripts, CIF/data files, raw trajectories, or generated results.

```text
src/li_research/
├── structures/          # ordered-model and supercell builders
├── conversion/          # CIF/LAMMPS/extended-XYZ conversion utilities
└── analysis/
    ├── lammps/          # Li MSD and tracer-diffusion analysis
    └── gpumd/           # GPUMDkit preparation and GPUMD analysis
```

Execution wrappers and model-specific input templates belong in `hpc/`;
calculation-ready structures belong in `structures/`; derived outputs and raw
trajectories belong in `results/` on TSUBAME.
