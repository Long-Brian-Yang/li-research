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
[Direction 2 project status](docs/development/project_status_en.md).

1. Screenshot-derived CIF information has been converted into explicit ordered
   candidates. The original CIFs contain partial occupancies and are not sent
   directly to MD.
2. Three ordered Li₃YCl₆ occupancy models and one ordered LiNbOCl₄ model have
   been converted to LAMMPS data files.
3. MACE-MPA-0 GPU ionic relaxation has been tested on TSUBAME 26ICP.
4. Isotropic variable-volume relaxation is being run from the fixed-cell
   relaxed structures. Cell shape is kept fixed in this first variable-cell
   pass.

Relaxed structures from TSUBAME are stored under `relax_runs/<timestamp>/`.
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
- [`simulation/mace_mpa0/`](simulation/mace_mpa0/) — model, conversion,
  relaxation, MD, and diffusion-analysis utilities;
- [`simulation/mace_mpa0/lammps/README.md`](simulation/mace_mpa0/lammps/README.md)
  — MACE + LAMMPS input conventions;
- [`hpc/tsubame_26icp/relax_ordered_gpu.sh`](hpc/tsubame_26icp/relax_ordered_gpu.sh)
  — fixed-cell ionic relaxation;
- [`hpc/tsubame_26icp/relax_cell_ordered_gpu.sh`](hpc/tsubame_26icp/relax_cell_ordered_gpu.sh)
  — isotropic variable-volume relaxation.

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

The complete English research plan, including structure policy, supercell
choices, MACE/NEP89 workflow, 300 K production protocol, MSD and conductivity
definitions, uncertainty analysis, and reproduction gates is in
[`docs/development/direction2_plan_en.md`](docs/development/direction2_plan_en.md).
The corresponding Japanese version is
[`docs/development/direction2_plan_ja.md`](docs/development/direction2_plan_ja.md).

## Reproducibility notes

Record the MACE checkpoint, LAMMPS executable, GPU model, input data filename,
supercell, temperature, timestep, and trajectory length for every MD run.
MACE foundation-model results are exploratory until checked against DFT forces,
experimental structure/transport data, and an independent potential.
