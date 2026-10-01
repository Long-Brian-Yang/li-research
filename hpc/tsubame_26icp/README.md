# TSUBAME job and engine workflows

This directory holds TSUBAME-specific path configuration, engine build recipes, short benchmark jobs, model input templates, production MD scripts, and non-submitting preflight checks. It is not a portable local installation package.

The full environment matrix, deployment sequence, source-code catalog, and data boundaries are maintained in the [repository technical guide](../../docs/engineering/repository_technical_guide_zh.md#3-运行环境与依赖).

## Supported directory layout

```text
config/       canonical TSUBAME paths (`yang_paths.sh`)
build/        per-engine build/compile recipes
benchmark/    short backend/model comparison jobs
inputs/       maintained LAMMPS input templates and MACE conversion helper
production/   material-specific MD jobs and their engine inputs
validation/   project path/package and GPU environment preflight
```

All canonical jobs should source `config/yang_paths.sh` and use its environment, model, engine, structure, run, benchmark, and result variables. External models and binaries reside on TSUBAME and are not versioned here.

## Preflight and run safety

On TSUBAME, from the repository root and after confirming the checkout and access rights, run:

```bash
bash hpc/tsubame_26icp/validation/validate_project.sh
qsub -g tgj-26ICP hpc/tsubame_26icp/validation/check_mace_env_gpu.sh
```

The first script inspects cluster paths and imports remote Python packages; it is not a local check or scientific validation. The second command submits a short GPU preflight through SGE; do not invoke that GPU script directly on a login node. For a production job, review the complete script and verify source structure/checksum, model, composition, timestep, temperature, ensemble, output location, task-array size, and scheduler resources before submission. Job completion alone does not establish structural correctness or literature agreement.

## Root-level historical/specialized scripts

Older and diagnostic scripts remain directly in this directory for traceability and some may still be referenced by historical records. They are not automatically equivalent to the maintained subdirectory versions. In particular, root `build_matgl_m3gnet_gpu.sh` contains an obsolete pre-migration environment path. Prefer the current `build/`, `benchmark/`, `production/`, and `validation/` counterparts, and inspect root-level scripts before use. `validate_project.sh` deliberately scans for known legacy path patterns and should fail if one is present.

Do not delete or relocate old entry points until their remote call sites, job logs, and documented provenance have been checked.
