# Research task scripts

`scripts/structures/` contains one-off or material-specific structure preparation, post-processing, figure generation, evidence packaging, and TSUBAME job wrappers. These are workflow entry points, distinct from reusable helpers in `src/li_research/` and build/job templates in `hpc/`.

| Filename family | Typical responsibility |
|---|---|
| `build_`, `prepare_`, `pack_`, `extract_` | Generate or transform candidates, composition/orderings, clusters, and paper source data |
| `analyze_`, `finish_`, `complete_`, `summarize_` | MSD/diffusion/Arrhenius, local structure, repeat diagnostics, and cross-material tables |
| `check_`, `compare_`, `validate_`, `review_`, `select_` | Structure/provenance checks and controlled comparison or representative selection |
| `plot_`, `curate_`, `li_diffusion_style.py` | Material figures, literature comparison panels, report styles, and figure manifest updates |
| `submit_*.sh` | TSUBAME SGE submission wrappers; may launch remote calculations |

For a filename-by-filename index, inputs/outputs, run environment, and the HPC boundary, see the [technical guide](../docs/engineering/repository_technical_guide_zh.md#6-分析代码与结果流).

## Before running

Many scripts encode material-specific paths or import sibling modules by their current location. Read the full script, check source data/provenance and output path, and verify that it targets the intended run. Do not launch `submit_*.sh` scripts from a local shell as if they were harmless analyses. Report figures are written to `docs/materials/figures/`; complete raw trajectories remain in local/TSUBAME archives.
