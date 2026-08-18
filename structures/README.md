# Structure data

This directory separates source/reference structures from calculation-ready
ordered models.

| Folder | Purpose | Calculation status |
|---|---|---|
| [`reference/photo_reconstructed/`](reference/photo_reconstructed/) | CIFs reconstructed from screenshots | Inspection only; not production-ready |
| [`raw/`](raw/) | Original deposited CIFs supplied by the research team | Source data; verify provenance |
| [`ordered/`](ordered/) | Explicit full-occupancy models for DFT/ML-MD | Production input after validation |

The screenshot-reconstructed CIFs contain partial occupancies.  They must be
ordered and checked against the original CIF before conversion to a LAMMPS data
file.

## Li₃YCl₆ 2×2×4 validation

The `ordered/Li3YCl6/2x2x4/` models contain 480-atom cells made by repeating
the previously relaxed 2×2×2 models once along `c`.  All three models have
Li₁₄₄Y₄₈Cl₂₈₈ stoichiometry, finite coordinates, and minimum interatomic
distances of 2.39–2.46 Å.  They are suitable for a short GPUMD stability
check, but a full 2×2×4 relaxation should still precede production-quality
MD.
