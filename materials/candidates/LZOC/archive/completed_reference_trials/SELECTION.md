# LZOC candidate selection — 2026-09-11

Candidate 3 (Kim 2025 Supplementary Data 18-derived seed; TSUBAME job
8631935.3) is selected for the next stage. Candidates 1 and 2 remain retained
as preparation records; no additional independent structures are requested.

## Checked output

- Composition: Li42 Zr24 O12 Cl114, 192 atoms.
- Final structure: `source_3/candidate_final.data`.
- Preparation log: `source_3/candidate.log`.
- Preparation: 55 ps MD followed by fixed-cell atomic minimization.
- Final density: 1.9832557 g/cm³ (instantaneous final cell, not an NPT average).
- Minimum periodic interatomic distance: 1.91825 Å.
- Final minimization force two-norm: 0.0099607853 eV/Å;
  maximum force component: 0.0020793083 eV/Å.
- NPT density means for consecutive 1 ps blocks from 45–55 ps:
  2.0061, 1.9708, 1.9541, 1.9356, 1.9448, 1.9127, 1.9396,
  1.9193, 1.9497, 1.9349 g/cm³.

The density does not decrease monotonically during the last five blocks, but
10 ps of NPT sampling does not establish full equilibration. The final
minimization relaxes atomic positions, not the simulation cell.

## Interpretation and pending work

This is a provisional selection, not proof of the most stable or fully
amorphous structure. Residual crystalline order has not yet been quantified.
Numerical completion and absence of obvious overlaps do not establish model
accuracy. Formal 50 ps equilibration + 200 ps production has not been submitted;
its target temperature must be specified before submission.

Remote source:
`/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/reference_8631935/source_3/`
