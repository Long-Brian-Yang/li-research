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
