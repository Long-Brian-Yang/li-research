# Results directory

This directory stores interpreted tables and historical publication packages.
The company-facing report does not require readers to navigate these folders;
its canonical figures are collected in `docs/materials/figures/` and its
inspectable structures/representative trajectories in `materials/evidence/`.

## Maintained result groups

| Directory | Role |
|---|---|
| `amorphous_review_20260915/` | Source tables and analyses for LZOC, LSZC, Li₃PS₄ and LiPON |
| `LZOC/` | MACE–NEP89 benchmark and legacy LZOC comparison |
| `publication_all_materials/` | Consolidated crystalline Li₃YCl₆/LiNbOCl₄ publication package |
| `midterm_Li3YCl6_MACE_M3GNet/` | Midterm presentation snapshot and supporting plots |
| `gpumd_nep89/` | Early GPUMD/NEP89 benchmark records |
| `amorphous_validation_20260914/` | Early amorphous-structure validation snapshot |

Raw trajectories and scheduler outputs are intentionally ignored by Git and
remain in the local/TSUBAME archive. Derived CSV/JSON tables and report assets
are versioned. Superseded duplicate publication trees and preview-only figures
are not retained in the active repository.
