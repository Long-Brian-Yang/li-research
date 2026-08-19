# Direction 2 master plan

This is the single project-facing entry point for the internship study. The
computational scope is limited to two reference materials:

- **Li₃YCl₆** — Asano *et al.*, *Advanced Materials* (2018), halide benchmark;
- **LiNbOCl₄** — Tanaka *et al.*, *Angewandte Chemie International Edition*
  (2023), mixed-anion oxyhalide benchmark.

The goal is an interpretable, reproducible screening workflow, not a
publication-grade materials claim.

## 1. Research logic from the proposal comments

```text
literature + NGK trial data
        ↓ Step 1: map high-conductivity structures
space groups + stacking + polyhedral connectivity
Li-site topology + vacancies + anion arrangement
        ↓ Step 2: constrained composition substitution
structure prediction/enumeration + explicit ordered models
        ↓ Step 3: MD transport screening
MSD → D_Li → σ_NE → prioritisation / Go–No-Go conclusion
```

The two reference materials are structural and transport anchors. They are not
the final candidate space.

## 2. What must be completed for the internship

The minimum useful deliverable is:

1. explain which structural motifs are associated with fast Li transport;
2. organise a small, interpretable candidate set under element constraints;
3. construct and validate explicit models;
4. run ML-MD and analyse MSD/σ_NE consistently; and
5. state which regions are prioritised or screened out, with limitations.

The following are optional follow-ups, not completion blockers: 3–5 ns runs,
full DFT force validation, Green–Kubo conductivity, exhaustive chemical search,
and publication-level uncertainty analysis.

## 3. Structure policy

The screenshot-derived CIFs are average/disordered crystallographic models with
partial occupancies. They are retained for provenance and visual inspection,
not sent directly to production MD.

Every production model must have:

- full occupancy and the correct nominal formula;
- explicit ordering recorded as a separate model/replica;
- finite coordinates and a valid periodic cell;
- minimum-distance and overlap checks; and
- source, ordering rule, relaxation status, and validation record.

Current explicit models:

| System | Models | Production purpose |
|---|---:|---|
| Li₃YCl₆ | 3 Li/Y orderings | Ordering and replica sensitivity |
| LiNbOCl₄ | 1 explicit model | O/Cl mixed-anion benchmark |

## 4. Current computational status

| Work package | Method | Status | Location |
|---|---|---|---|
| Literature | Bilingual paper notes | Complete | [`docs/literature/`](../literature/) |
| Structures | Explicit CIF/XYZ/LAMMPS models | Complete with limitations | [`structures/`](../../structures/) |
| MACE | MACE-MPA-0 + LAMMPS GPU, 400 K | Running | TSUBAME jobs below |
| NEP89 | GPUMD + NEP89, 300 K | Screening complete | [`simulation/gpumd_nep89/`](../../simulation/gpumd_nep89/) |
| Comparison | Matched potential/temperature analysis | After MACE completion | Pending |

### MACE jobs currently running

Each system is a separate 14 h job to avoid serial walltime cutoffs:

| Job | System | Protocol |
|---:|---|---|
| 8441077 | Li₃YCl₆_01 | 400 K; 10 ps equilibration + 100 ps production |
| 8441078 | Li₃YCl₆_02 | 400 K; 10 ps equilibration + 100 ps production |
| 8441079 | Li₃YCl₆_03 | 400 K; 10 ps equilibration + 100 ps production |
| 8441080 | LiNbOCl₄ | 400 K; 10 ps equilibration + 100 ps production |

All use a 1 fs timestep. A run is accepted as complete only after the
trajectory contains the full 100 ps production segment and passes the basic
temperature/energy/structure checks.

### NEP89 baseline

The existing NEP89 screening set contains three Li₃YCl₆ replicas and one
LiNbOCl₄ run at 300 K. Official GPUMDkit MSD and thermo plots are the primary
figures. The main fit window is 100–300 ps; alternative windows are recorded in
`window_sensitivity_300K_2x2x4.csv`.

MACE 400 K and NEP89 300 K values must not be treated as a direct model
comparison. The first comparison should align temperature, cell size,
trajectory length, and MSD fitting protocol.

## 5. Analysis definitions

For Li-only self-diffusion:

\[
D_{Li}=\frac{1}{6}\frac{d\,\mathrm{MSD}(t)}{dt}.
\]

The first conductivity estimate is:

\[
\sigma_{NE}=\frac{n_{Li}q_{Li}^{2}D_{Li}}{k_BT}.
\]

This is a tracer/Nernst–Einstein estimate. It is not automatically equal to
collective Green–Kubo conductivity or pressed-powder EIS conductivity.

Every result table should state temperature, supercell, timestep, production
length, fit window, number of Li atoms, potential, and whether the value is
σ_NE or collective conductivity.

## 6. Decision gates

### Gate A — model integrity

Correct formula, explicit occupancy, valid cell, no overlaps, and provenance.

### Gate B — relaxation/stability

No framework collapse, sensible volume/energy, reasonable contacts, and no
runtime errors.

### Gate C — transport screening

Stable temperature, a visible MSD regime, documented fit window, and a
reasonable sensitivity to the chosen fit interval.

### Gate D — internship conclusion

Identify the structural/compositional regions to prioritise and the regions to
de-prioritise. A negative screening result is acceptable if the reason and
limitations are explicit.

## 7. Next actions

1. Wait for MACE jobs 8441077–8441080 to finish and verify actual trajectory
   lengths.
2. Convert the completed MACE trajectories to compact CSV/MSD summaries.
3. Compare MACE and NEP89 under clearly labelled temperature and cell-size
   conditions.
4. Build a small structural motif/candidate table from the nine papers and NGK
   data.
5. Write the internship conclusion: prioritised motifs, rejected regions, and
   recommended next experiment or calculation.

## 8. Detailed references

- [Japanese Direction 2 plan](direction2_plan_ja.md)
- [English detailed protocol](direction2_plan_en.md)
- [Project status archive](project_status_en.md)
- [MACE workflow](../../simulation/mace_mpa0/README.md)
- [NEP89/GPUMDkit workflow](../../simulation/gpumd_nep89/README.md)
