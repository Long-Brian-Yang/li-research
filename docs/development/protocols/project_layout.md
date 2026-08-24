# Project layout and naming standard

This is the canonical layout for the Direction 2 calculation project. The GitHub
repository is the source of scripts, documentation and small metadata files;
TSUBAME stores compiled engines, models and large trajectories.

## Canonical TSUBAME workspace

```text
/gs/fs/tgj-26ICP/uf03782/yang/li-research/
    ├── src/li_research/         # reusable Python: structures, conversion, analysis
    ├── docs/development/       # plans, benchmark records and results
    ├── hpc/tsubame_26icp/      # config/, build/, benchmark/, inputs/, validation/
    ├── structures/             # ordered cells and supercells
    ├── models/{mace,sevennet,m3gnet,nep89}/
    ├── engines/{lammps,gpumd,gpumdkit}/
    ├── benchmarks/{lammps,gpumd,summary}/
    ├── runs/{relax,md}/        # timestamped calculation workspaces
    ├── results/{md,diffusion,benchmark,analysis,validation}/
    └── archive/                # created only when a dated legacy record is retained
```

There is no root-level compatibility layer. New jobs must use variables from
`hpc/tsubame_26icp/config/yang_paths.sh` and write new outputs below `results/` or
`benchmarks/` or `runs/`; they must not create new root-level result directories.

## Naming rules

Use lowercase `snake_case` for scripts/directories, except chemical formulas.

```text
build_<engine>_<backend>.sh
benchmark_<engine>_<model>_<backend>.sh
relax_<model>_<structure>.sh
md_<model>_<structure>_<temperature>K.sh
analyze_<engine>_<dataset>.py
```

Structure names are `Li3YCl6_03` and `LiNbOCl4`; temperatures use `400K`,
`500K`, etc. A production run directory includes a timestamp or job ID, for
example `results/md/mace_mliap/Li3YCl6_03/400K/job_8474204`.

## Path policy

Scripts must source `config/yang_paths.sh` through `YANG_PATHS_FILE`, because SGE runs
from a spool copy and `$0` is not the project path. Active scripts must not contain
hard-coded `/home/2/...`, `tga-ishikawalab`, or pre-migration project paths.
Site-local software environments and compiled executables remain outside the Git
repository.
