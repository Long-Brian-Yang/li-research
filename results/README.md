# Derived analysis results

This tree keeps compact, inspectable analysis products: CSV/JSON tables, source-data extracts, checksums/manifests, report figures, and dated snapshots. It is not the primary home for the current scientific narrative; see the [Japanese](../docs/materials/materials_overview_ja.md) and [English](../docs/materials/materials_overview_en.md) Material Reviews.

## Major result collections

| Directory | Role |
|---|---|
| `publication_all_materials/` | Consolidated crystalline benchmark figure/source-data package and supplementary material |
| `midterm_Li3YCl6_MACE_M3GNet/` | Midterm benchmark report snapshot, tables, and plots |
| `amorphous_review_20260915/` | Dated LZOC, LSZC, Li₃PS₄, LiPON analysis, comparison, and follow-up records |
| `amorphous_validation_20260914/` | Earlier amorphous preparation/validation snapshot |
| `LZOC/` | LZOC MACE–NEP and legacy comparison analysis |
| `gpumd_nep89/` | GPUMD/NEP89 trajectory analysis, derived figure/table outputs, and historical 300 K benchmark |
| `analysis/Li3YCl6/` | Additional Li₃YCl₆ analysis artifacts |

The date-stamped folders are immutable research snapshots unless a report explicitly points to a newer replacement. Check the local README and source hashes in each folder before using values in a current comparison.

## What is and is not stored here

- Track compact derived tables, figure sources/exports, manifests, and reproduction notes needed to inspect reported results.
- Keep complete multi-hundred-megabyte MD trajectories, restarts, scheduler logs, compiled models, and model weights in their established local/TSUBAME archive.
- The root `.gitignore` intentionally excludes many raw trajectories, `runs/`, model files, restart/dump files, and downloaded paper source material.
- `materials/evidence/` contains selected named structures and uniformly sampled representative XYZ exports; quantitative calculations use the complete source trajectory identified in the applicable provenance manifest, not those display samples.

See the [engineering guide](../docs/engineering/repository_technical_guide_zh.md#7-输入输出报告与溯源) for the input → analysis → report path and reproducibility limits.
