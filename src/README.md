# Reusable Python modules

`src/li_research/` contains small reusable modules for ordered structure creation, format conversion, and selected LAMMPS/GPUMD analysis. The complete file-by-file map, environment assumptions, and testing guidance are in the [repository technical guide](../docs/engineering/repository_technical_guide_zh.md#5-核心代码src).

```text
li_research/
├── structures/       ordered crystal builders and supercell utilities
├── conversion/       CIF/LAMMPS/extended-XYZ conversion and occupancy checks
└── analysis/
    ├── lammps/       Li MSD/diffusion, jumps, and model-comparison plots
    ├── gpumd/        GPUMDkit input preparation and GPUMD post-processing
    ├── rdf/          trajectory RDF recomputation
    └── arrhenius/    crystalline benchmark Arrhenius figures
```

## Runtime note

The repository has no `pyproject.toml`, `setup.py`, or pinned dependency file. Scientific modules use libraries including ASE, NumPy, SciPy, and Matplotlib; individual source files define their actual requirements. They can be invoked from the repository root with `PYTHONPATH=src` when their input paths and dependencies are available. Many material-specific analyses instead live under `scripts/structures/` and are not installed as a package.

Do not put LAMMPS/GPUMD job scripts, model weights, raw trajectories, or generated results in this tree; those belong to `hpc/`, external model/runtime storage, or `results/` as appropriate.
