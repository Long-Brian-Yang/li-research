# Direction 2 project status

This document is the execution map for the current computational project. The
scope is limited to two literature reference materials:

1. **Li₃YCl₆** — Asano *et al.*, *Advanced Materials* (2018), high-voltage
   halide benchmark.
2. **LiNbOCl₄** — Tanaka *et al.*, *Angewandte Chemie International Edition*
   (2023), mixed-anion oxyhalide benchmark.

## Work packages

| Package | Purpose | Method | Status | Output |
|---|---|---|---|---|
| Literature | Establish experimental benchmarks and design rationale | Paper notes | Complete | `docs/literature/` |
| Structure | Convert disordered screenshot CIFs into explicit ordered models | CIF/LAMMPS validation | Complete with limitations | `structures/`, `structures/README.md` |
| MACE | Reference ML-MD using MACE-MPA-0 | LAMMPS GPU, 400 K | Running | TSUBAME jobs 8441077–8441080 |
| NEP89 | Independent potential comparison | GPUMD + NEP89, 300 K | Screening complete | `simulation/gpumd_nep89/` |
| Comparison | Quantify potential/temperature/ordering effects | Matched MSD and σ_NE analysis | Pending MACE completion | To be added |
| Validation | Check force accuracy and structural stability | DFT spot checks and longer replicas | Pending | To be added |

## Proposed Direction 2 discovery logic

The project is not limited to reproducing two isolated compositions. After the
reference gates, the work expands in three controlled steps:

1. **Structural map:** identify space groups, stacking, polyhedral connectivity,
   Li-site topology, vacancy patterns, and anion arrangements associated with
   high conductivity in the literature and NGK data.
2. **Constrained substitution:** replace elements only within the approved
   element space, while allowing for composition-induced structure changes and
   explicitly constructing new ordered models.
3. **MD decision:** screen stable models, rank transport and stability, and
   provide a clear go/no-go conclusion. If the candidate set is too large, use a
   documented descriptor/surrogate model to select MD candidates.

The two current materials are therefore **reference anchors and structural
training examples**, not the final search space.

## Internship-level completion target

This is an internship deliverable, not a publication package. Completion does
not require publication-grade uncertainty, 3–5 ns trajectories, Green–Kubo
conductivity, or exhaustive DFT validation. The practical target is to:

1. explain the relevant structural motifs;
2. organise a small, interpretable candidate set;
3. construct and validate explicit models;
4. run ML-MD and calculate MSD/σ_NE consistently; and
5. provide a clear prioritisation or no-go conclusion with limitations.

Longer trajectories, DFT spot checks, and collective conductivity are useful
follow-ups, but they are not completion blockers for the internship report.

## MACE run currently in progress

Each system is submitted as an independent job to avoid serial walltime
cutoffs:

| Job | Material | Protocol |
|---:|---|---|
| 8441077 | Li₃YCl₆_01 | 400 K, 10 ps equilibration + 100 ps production |
| 8441078 | Li₃YCl₆_02 | 400 K, 10 ps equilibration + 100 ps production |
| 8441079 | Li₃YCl₆_03 | 400 K, 10 ps equilibration + 100 ps production |
| 8441080 | LiNbOCl₄ | 400 K, 10 ps equilibration + 100 ps production |

All use a 1 fs timestep and a 14 h walltime request. The final result is not
accepted until the trajectory contains the complete 100 ps production segment.

## NEP89 baseline

The current NEP89 screening baseline is a 300 K, 2×2×4 Li₃YCl₆ set with three
ordered replicas and one LiNbOCl₄ run. Official GPUMDkit MSD and thermo figures
are the primary figures. The main diffusion fit uses 100–300 ps; alternative
windows are recorded for sensitivity analysis.

These values are not directly comparable with the current MACE runs because the
temperatures and supercells differ. A model comparison must first align those
conditions.

## Analysis rules

- Report `D_Li` as tracer/self-diffusion.
- Report `σ_NE` as a Nernst–Einstein estimate, not as collective Green–Kubo or
  pressed-powder EIS conductivity.
- Keep full trajectories on TSUBAME; commit compact CSVs, text summaries, and
  official plots to GitHub.
- Do not use partial-occupancy CIFs or repair composition by deleting atoms.
