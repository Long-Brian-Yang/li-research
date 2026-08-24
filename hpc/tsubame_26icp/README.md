# TSUBAME launchers

This directory contains the supported submission, build, benchmark and analysis
launchers for Direction 2. Every launcher sources `config/yang_paths.sh`, which defines
the canonical `yang/` workspace and its `models`, `engines`, `structures`,
`benchmarks`, `runs` and `results` roots.

```text
hpc/tsubame_26icp/
├── config/      # canonical paths and environment locations
├── build/       # reproducible engine/build scripts
├── benchmark/   # short, standardized speed tests
├── inputs/      # maintained LAMMPS input templates
├── production/  # relaxation + long-MD submission scripts
└── validation/  # non-submitting environment and layout checks
```

Naming convention:

- `build_<engine>_<backend>.sh` — build or install an engine.
- `benchmark_<engine>_<model>_<backend>.sh` — reproducible speed test.
- `relax_<model>_<structure>.sh` — structure relaxation.
- `md_<model>_<structure>_<temperature>K.sh` — production MD.
- `analyze_<engine>_<dataset>.py` — post-processing.

Only launchers and templates that use `config/yang_paths.sh` and the canonical
`engines/`, `models/`, `structures/`, `benchmarks/`, `runs/`, and `results/`
locations are kept here. Obsolete launchers are removed once their necessary
configuration has been incorporated into the maintained workflow.

Run `validation/validate_project.sh` before submitting a new benchmark or
production job.
