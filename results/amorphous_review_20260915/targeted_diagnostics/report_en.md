> Superseded LZOC figures have been removed. Only the 2 fs series is displayed in the maintained Material Review; archived numerical data below are unchanged.

> Historical snapshot. The complete, maintained report is [here](../../../docs/materials/materials_overview_en.md).

# Targeted diagnostics: structure and transport sensitivity

15 September 2026 · [日本語](report_ja.md) · [Settings and completion record](../../../docs/materials/targeted_diagnostics_20260915.md)

## 1. LSZC: volume relaxation does not resolve local-structure disagreement

![LSZC volume and local structure](LSZC_volume_structure_diagnostic.png)

**Panels a–d:** stage-relative density; consecutive 5 ps pressure means; Zr–O and Zr–Cl RDFs. Blue is the preceding 400 K NVT hold; red is the subsequent 400 K, 1 bar NPT diagnostic. These are sequential stages of one 272-atom structure, not independent replicas or simultaneous branches. Each stage lasts 20 ps. RDFs use ten snapshots at 11–20 ps (1 ps spacing), minimum-image distances, per-frame volume normalisation and 0.05 Å bins; curves are not smoothed. Lines connecting pressure means are guides, not continuous measurements. The 1 bar line applies to the NPT target, not a pressure constraint on NVT.

| Quantity | Previous NVT | NPT diagnostic |
|---|---:|---:|
| Density, final 10 ps (g/cm³) | 1.86376, fixed cell | 1.81550 |
| Zr–O mean coordination, cutoff 2.6 Å | 1.53156 | 1.51594 |
| Zr–Cl mean coordination, cutoff 3.2 Å | 4.21781 | 4.25969 |
| Fraction of S with four O neighbours, cutoff 2.0 Å | 1.00 | 1.00 |

Coordination averages use 100 final-stage frames at 0.1 ps spacing. The density decreases by about 2.59% relative to the starting fixed cell; pressure block means are reduced, but RDF first-shell peaks and Zr coordination remain similar. Thus this short pressure-relaxation test **does not correct the reference mismatch**. It neither proves an equilibrated glass nor identifies the potential as the sole cause. Preparation, finite size, and model applicability remain possible contributors. The reference EXAFS comparison and its non-equivalence to a simple cutoff count are retained in the [earlier analysis](../final_comparisons/report_en.md).

## 2. LZOC: a smaller timestep does not remove all sensitivity


**Panels a–d:** lithium time-origin-averaged MSD; apparent diffusion coefficient across fitting windows; framework-species MSD; consecutive 20 ps potential-energy means. Both runs start from identical positions, velocities and cell, at 380 K, with NVT Nosé–Hoover chain and a 100 fs coupling time. Each lasts 80 ps. Only the integration timestep differs (blue 0.5 fs; red 2 fs). MSD is shown to 40 ps lag, using the full 80 ps trajectory plus its starting frame; periodic wrapping and whole-system mass-weighted centre-of-mass motion are removed. No species-specific drift subtraction is used.

| MSD fit window (ps) | D, 0.5 fs (cm²/s) | D, 2 fs (cm²/s) | Relative difference |
|---|---:|---:|---:|
|5–20|1.13169×10⁻⁶|1.18405×10⁻⁶|−4.4%|
|10–30|1.09127×10⁻⁶|1.12433×10⁻⁶|−2.9%|
|10–40|1.00361×10⁻⁶|8.95684×10⁻⁷|+12.1%|

The relative difference is `(D_0.5fs / D_2fs − 1) × 100%`. These are diagnostic slopes, not established asymptotic diffusivities. The free-intercept relation is

$$\mathrm{MSD}(\tau)=b+6D\tau,\qquad D[\mathrm{cm^2/s}]=\frac{m[\mathrm{\AA^2/ps}]}{6}\times10^{-4}.$$

Here τ is lag time, m the fitted slope, b the intercept and D the apparent three-dimensional self-diffusion coefficient. The nonzero short-time offset affects log–log MSD slopes; values below one alone do not prove anomalous diffusion. Combined with window sensitivity and continued framework motion, these data do not yet establish long-time convergence. No new Ea or room-temperature conductivity is adopted. One trajectory per timestep gives no independent-replica confidence interval, and differences cannot be attributed uniquely to integration error rather than finite sampling.

## 3. What is complete and what remains

- Completed: run completion checks, thermal blocks, LSZC density/RDF/coordination comparison, LZOC MSD/framework/fit-window comparison, local full-trajectory backup, numerical tables and figures.
- LSZC: retain as a discrepancy case; simply extending the same NPT is not a demonstrated remedy.
- LZOC: retain both settings as sensitivity controls, not a replacement of the original data or an updated formal Ea.
- LiPON and Li₃PS₄: the previously documented N–N contact and network-connectivity limitations remain; no new DFT or arbitrary trajectory manipulation was performed.

## Data and verification

[Fit results and input hashes](results.json) · [LSZC coordination time series](LSZC_structure.csv) · [Plotting script](../../../scripts/structures/plot_targeted_diagnostics.py) · [Calculation script](../../../scripts/structures/analyze_targeted_diagnostics.py)

Both figures are exported as PNG/PDF/SVG. The existing Li-diffusion presentation style is retained: 22 pt titles, 19 pt axis labels, 15 pt ticks/legends, 3 pt summary lines and 1.8 pt frames; each panel is 7.2×5.8 inches before display scaling. Each quantitative curve is preserved in a CSV or the reproducible calculation inputs. RDF frames and time blocks are correlated samples of one structure, not additional independent replicas. No error bars, significance tests or confidence claims are implied. The images were visually inspected for legibility, clipping and legend overlap; these are presentation figures, not a final journal-size submission package.
