# Ordered calculation structures

Put explicit full-occupancy models here, for example:

```text
Li3YCl6_ordered_01.cif
LiNbOCl4_ordered_01.cif
```

Keep multiple disorder/order realizations as separate files and record their
origin and formula in a manifest before production MD.

## Current (2\times2\times2) status

- `LiNbOCl4/2x2x2/`: earlier pipeline candidate retained for provenance
- `LiNbOCl4/2x2x3/`: literature-aligned follow-up candidate, CIF, LAMMPS data, and validation report
  generated from the screenshot-reconstructed CIF under an explicit full-site
  occupancy assumption. It contains 224 atoms and has a minimum distance of
  1.907 Å.
- `Li3YCl6/2x2x2/`: three 240-atom ordered candidates generated from the
  occupancy-resolved Li₉Y₃Cl₁₈ cell. These require MACE/DFT relaxation and
  cross-model comparison before production MD.
