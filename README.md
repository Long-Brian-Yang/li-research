# Li Research: Direction 2 Halide Electrolytes

This repository contains the working materials for **Direction 2**: reproducing
and comparing fast-ion-conducting halide and oxyhalide solid electrolytes with
MACE-MPA-0 and LAMMPS.

The current computational scope is deliberately narrow:

- **Li₃YCl₆** — the high-voltage halide benchmark reported by Asano *et al.*
- **LiNbOCl₄** — the mixed-anion oxyhalide benchmark reported by Tanaka *et al.*

The immediate objective is to establish a reproducible structure → relaxation →
MD workflow for these two reference systems. New chemistry is out of scope until
the Direction 2 reproduction and uncertainty gates are passed.

## Current status

The execution status and work-package boundaries are tracked in the
[benchmark comparison](docs/development/benchmarks/benchmark_comparison.md).

1. Screenshot-derived CIF information has been converted into explicit ordered
   candidates. The original CIFs contain partial occupancies and are not sent
   directly to MD.
2. Three ordered Li₃YCl₆ occupancy models and one ordered LiNbOCl₄ model have
   been converted to LAMMPS data files.
3. The calculation workflow supports MACE, SevenNet, M3GNet/MatGL and GPUMD.
4. The current benchmark set uses a shared relaxed Li₃YCl₆ structure; physical
   diffusion studies remain a separate, model-specific relaxation and MD phase.

Relaxed structures and MD workspaces from TSUBAME are stored under
`runs/relax/<timestamp>/` and `runs/md/<timestamp>/`.
These results are screening data, not yet validated transport values: the next
step is short MD, followed by force and structure checks against DFT or
experiment.

## Reproducible workflow

```text
ordered CIF candidates
        ↓
LAMMPS data validation
        ↓
MACE-MPA-0 ionic relaxation (fixed cell)
        ↓
MACE-MPA-0 isotropic volume relaxation
        ↓
short NVT MD on TSUBAME GPU
        ↓
Li MSD / diffusion screening and structural sanity checks
```

The main entry points are:

- [`structures/`](structures/) — explicit ordered CIF and LAMMPS data files;
- [`src/li_research/`](src/li_research/) — maintained structure, conversion and
  analysis utilities;
- [`hpc/tsubame_26icp/`](hpc/tsubame_26icp/) — active build and benchmark
  launchers;
- [`hpc/tsubame_26icp/validation/validate_project.sh`](hpc/tsubame_26icp/validation/validate_project.sh)
  — pre-submission environment/path validation;
- [`docs/development/protocols/project_layout.md`](docs/development/protocols/project_layout.md)
  — authoritative TSUBAME layout and naming convention.

## Structure policy

The crystallographic CIFs reconstructed from screenshots represent average
structures with disorder and partial occupancies. Expanding every listed site
creates an incorrect composition, especially for Li₃YCl₆. Therefore:

- raw/screenshot CIFs are retained for reference only;
- every MD input must use an explicitly ordered model;
- element counts and minimum interatomic distances must be validated before
  relaxation;
- different Li/Y orderings are treated as separate candidates, not as one
  definitive crystal structure.

## Literature notes

The literature section is intentionally bilingual. The Chinese and Japanese
paper notes, keywords, DOI links, and comparison tables are preserved here:

- [Chinese paper notes](docs/literature/papers_zh.md)
- [日本語論文ノート](docs/literature/papers_ja.md)

These notes provide the experimental benchmarks and motivation for Direction 2;
they are not the computational workflow itself.

## Direction 2 research plan

The project plan is maintained in two synchronized Markdown files:
[`docs/development/plans/direction2_plan_en.md`](docs/development/plans/direction2_plan_en.md)
and
[`docs/development/plans/direction2_plan_ja.md`](docs/development/plans/direction2_plan_ja.md).

## Reproducibility notes

Record the MACE checkpoint, LAMMPS executable, GPU model, input data filename,
supercell, temperature, timestep, and trajectory length for every MD run.
MACE foundation-model results are exploratory until checked against DFT forces,
experimental structure/transport data, and an independent potential.

The canonical TSUBAME directory and script naming rules are in
[project_layout.md](docs/development/protocols/project_layout.md). Superseded
short-lived artifacts are removed after their unique information has been
merged into the current documentation; reproducible raw calculation outputs
remain in timestamped `runs/` and `results/` directories.
