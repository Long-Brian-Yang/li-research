# Li Research — MLIP molecular dynamics for lithium-ion electrolytes

This repository contains code, inputs, evidence, and reports for evaluating machine-learning interatomic potentials (MLIPs) in crystalline and amorphous lithium-ion solid electrolytes. The research workflow connects literature-derived structures and reported measurements to model benchmarking, MD, transport/structure analysis, and company-facing evidence.

## Start here

- **Scientific results and literature story:** [Japanese Material Review](docs/materials/materials_overview_ja.md) · [English Material Review](docs/materials/materials_overview_en.md)
- **Engineering, environment, deployment, core code, analysis code, tests, and data map:** [Repository technical guide (Chinese)](docs/engineering/repository_technical_guide_zh.md)
- **Documentation index:** [docs/README.md](docs/README.md)
- **Structures/material candidates:** [structures](structures/README.md) · [materials](materials/README.md)
- **Reusable Python code:** [src](src/README.md) · **Research scripts:** [scripts](scripts/README.md)
- **TSUBAME builds, benchmarks, and job inputs:** [HPC guide](hpc/tsubame_26icp/README.md)
- **Derived data and report packages:** [results](results/README.md)

## Repository map

| Path | Responsibility |
|---|---|
| `src/li_research/` | Reusable structure builders, file converters, MSD/diffusion, RDF, and plotting helpers |
| `scripts/structures/` | Material-specific preparation, analysis, figure/evidence generation, and SGE wrappers |
| `hpc/` | TSUBAME environment paths, engine builds, short benchmarks, input templates, production scripts, and preflights |
| `simulation/` | Engine/model-specific LAMMPS inputs and notes |
| `structures/` | Reference CIFs and calculation-ready crystalline structures |
| `materials/candidates/` | Candidate construction and provenance for amorphous systems |
| `materials/evidence/` | Named initial structures and representative trajectories supporting report figures |
| `results/` | Derived analysis tables, figures, source manifests, and dated result snapshots |
| `docs/materials/` | Maintained scientific review and canonical report figures |
| `tests/` | Numerical, data-contract, figure, report, and path checks |

## End-to-end research workflow

```text
literature / experimental reference
        ↓
ordered crystal or prepared amorphous candidate
        ↓
composition, geometry, and provenance validation
        ↓
engine + potential preflight and structure relaxation
        ↓
temperature/ensemble-specific MD on the appropriate runtime
        ↓
MSD, diffusion, Arrhenius, RDF/coordination, and stability analyses
        ↓
same-definition comparison with paper/experiment
        ↓
derived tables + canonical figures + source/evidence manifests
        ↓
Material Review
```

## Reproducibility and data boundaries

The repository does not contain a single pinned local Python environment. TSUBAME environments, compiled engines, ML model weights, and complete production trajectories are external to Git; their expected paths and build recipes are documented under `hpc/` and in the [technical guide](docs/engineering/repository_technical_guide_zh.md). Large/raw artifacts are intentionally excluded by `.gitignore`. The repository tracks analysis code, calculation inputs where appropriate, derived tables/figures, checksums/manifests, and compact representative evidence.

Before running any cluster script, inspect its model/input/output paths and scheduler settings. `hpc/tsubame_26icp/validation/validate_project.sh` is a TSUBAME-side preflight, not a local test and not a scientific validation. Do not interpret a job completion marker as proof that a potential or transport result is physically validated.

For the authoritative current material status, use the maintained Material Review rather than dated daily reports or historical experiment snapshots.
