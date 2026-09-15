# Amorphous materials — consolidated research record

Updated 15 September 2026. [日本語](materials_overview_ja.md)

### Active continuation: Li₃PS₄ transport control

Array **8675738.1–4** has been submitted (300/500/700/900 K, maximum two concurrent tasks). This closes the missing dedicated-transport step only when completed and analysed; it is not a completed reproduction. Every branch starts independently from the same512-atom preparation endpoint, SHA256 `a92cb37de5d8aaf4fd110edcb8aa85ebc6a1b9798b8588d2c1dbae08f25c45df`. NEP89/GPUMD,0.5 fs;10 ps300→target ramp (300 K branch is a hold),50 ps NPT1 bar,200 ps NVT; MTTK periods100/1000 fs. Output0.05 ps thermo/0.1 ps trajectory. Numerical and broad volume guardrails run after each stage; they do not certify structural agreement. Each task has a30-minute scheduler limit. [Submitted script](../../hpc/tsubame_26icp/production/lips_transport_control.sh).

Rechecked [Chen2025 Methods and transport discussion](https://www.nature.com/articles/s41467-025-56322-x): the paper uses0.5 fs structural MD and discusses300–900 K transport, with non-Arrhenius behaviour at low temperature. The selected four temperatures are a subset of the published source grid; the10/50/200 ps schedule, fixed-cell production and coupling periods are project choices, not a verified exact paper protocol. NEP and our512-atom preparation remain different from the author's DeePMD model. No room-temperature Ea extrapolation will be forced across a non-diffusive regime.

**Reference-unit check remains open:** the Fig.3a source workbook labels columns as conductivity(S/cm), whereas the article describes Fig.3a as diffusion coefficients. Preserve the published values/labels; do not silently reinterpret their units or compute a quantitative error until the plotted axis/source discrepancy is resolved. Planned outputs are Li and framework MSD, window/block fits, RDF/network stability, and then conditional D/σ with limitations. Other material limitations remain below; this submission does not resolve LSZC/LiPON chemistry.

This is the single maintained English record; the Japanese companion contains the same evidence. Settings, figures, tables, interpretation and remaining work are collected here. Earlier short reports are historical snapshots, not separate current-status pages. Original data and figure paths are unchanged. This consolidation submits no new MD and does not change fitted results.

## Contents

- [Status and scope](#status)
- [Preparation and reference matching](#settings)
- [Definitions and units](#methods)
- [Reconstructed LZOC](#lzoc)
- [LSZC](#lszc)
- [Li₃PS₄](#lps)
- [LiPON](#lipon)
- [Legacy LZOC / MACE–NEP](#legacy)
- [Remaining work and decision rules](#remaining)

<a id="status"></a>
## Status and scope

Four chemical systems, five preparation routes. New and legacy LZOC share a composition. LZOC/LSZC remain the oxyhalide-related main line; Li₃PS₄ is a methodological control and LiPON a limitation case. The crystalline Li₃YCl₆/LiNbOCl₄ work is not modified. The cancelled Zhou2024 route is not counted as executed.

| Route | Atoms / composition | Completed work | Current interpretation |
|---|---|---|---|
|New LZOC|192; Li42Zr24Cl114O12|Preparation,340/360/380 K200 ps;80 ps NHC controls;380 K0.5 fs control; structure/transport diagnostics|No converged Ea or room-temperature conductivity|
|LSZC|272; Li32Zr32Cl128S16O64|Independent cluster packing and relaxation,400 Khold,20 ps NPT; RDF/CN/EXAFS/cutoff comparisons|Sulfate retained; density and Zr environment disagree with reference|
|Li₃PS₄|512; Li192P64S256|Preparation,300 Khold; RDF/angle/source-data and graph-connectivity comparisons|Local agreement does not establish network or transport agreement|
|LiPON|124; Li47P16O56N5|Preparation,250 Kpressure release; N–N contact tracing and coordination|Persistent short contacts; not a validated transport structure|
|Legacy LZOC|192; same nominal LZOC|MACE/NEP600 K comparison; four-temperature timing|Efficiency/structural-sensitivity control, not an accuracy ranking|

Completed jobs are listed below; no claim is made about unrelated jobs or a live queue from this document snapshot. Diagnostic8675392.1–2 finished and its complete trajectories were saved locally.

<a id="settings"></a>
## Preparation and reference matching

| Route | Executed preparation / conditions | Reference and important difference |
|---|---|---|
|New LZOC|100 K2 ps;500 K30 ps;1000 K50 ps;1500 K30 ps;2000 K20 ps; staged cooling through1500/1000/500/100 K2 ps each,300 K20+50 ps; inherited fixed cell|Hussain2024 has distinct preparation/transport branches.192-atom NEP and this diagnostic heating/cooling history are not its48-atom AIMD transport model or exact full protocol|
|LSZC|Five finite cluster types, two copies each plus32Li; fixed-cell relaxation to0.0493 eV/Å;300 K20 ps NVT;300→400 K100 ps;400 K20 ps; then400 K1 bar20 ps NPT|Tang2026 deposited1088-atom glass is a reference, not this independently packed272-atom model. Old compressed replicated seed is not substituted|
|Li₃PS₄|1500 K100 ps NPT;1500→300 K480 ps (2.5 K/ps);300 K20 ps hold;0.5 fs|Chen2025 thermal schedule is a reference. NEP replaces DeePMD; replicated training-frame start, coupling and final hold differ|
|LiPON|2000 K10 ps;2000→250 K7 ps (250 K/ps);250 K20 ps;additional1 bar20 ps release;0.5 fs|Selected Seth2025 parameters; NEP replaces NequIP, independent precursor and timestep differ; pressure release is a project diagnostic|
|Legacy LZOC|Earlier candidate3 preparation;600/700/800/900 K branches;600 K comparison uses50 ps NPT+200 ps NVT|Retained exploratory workflow, not a retrospectively claimed literature reproduction|

**Timestep disposition:** keep the complete2 fs NHC series as the literature-aligned comparison branch, not a validated accuracy benchmark. Keep the380 K0.5 fs run as sensitivity evidence; do not delete it, silently replace individual temperatures or mix settings to fit Ea. The original MTTK0.5 fs200 ps series is also retained. Thermostat coupling100 fs is a project setting, not an independently verified paper parameter.

For current new diagnostics, positions/cell/velocities are preserved, NEP hash is checked, thermo output is0.05 ps and trajectory output0.1 ps. NPT uses1 bar=0.0001 GPa and temperature/pressure periods100/1000 fs. No DFT, artificial density fitting or target-Ea trajectory selection is included.

<a id="methods"></a>
## Definitions, units and statistical meaning

### Methods, units and statistical meaning

For Li motion, the time-origin averaged mean-square displacement is

$$\mathrm{MSD}(\tau)=\frac{1}{N_{\mathrm{Li}}N_o(\tau)}\sum_{i,t_0}|\mathbf r_i(t_0+\tau)-\mathbf r_i(t_0)|^2.$$

Here N_Li is the Li atom count; N_o is the number of valid origins at lag τ; r is the unwrapped position after total-system COM correction. For MSD = aτ+b in three dimensions,

$$D_{\mathrm{app}}[\mathrm{cm^2/s}]=\frac{a[\mathrm{\AA^2/ps}]}{6}\times10^{-4}.$$

The diagnostic Nernst–Einstein conversion uses Li⁺ charge q=e, number density n=N_Li/V (not N_Li alone), Boltzmann constant k_B and absolute T:

$$\sigma_{\mathrm{NE}}=\frac{n e^2 D}{k_B T},\qquad \sigma[\mathrm{mS/cm}]=10\sigma[\mathrm{S/m}]=10^3\sigma[\mathrm{S/cm}].$$

Use D[cm²/s]×10⁻⁴ to obtain m²/s and V[Å³]×10⁻³⁰ to obtain m³. JSON contains conditional σ_NE at the simulated temperatures; these ignore ion–ion cross correlations and inherit the apparent-D limitations. No experimental self-D is inferred without the relevant density and correlation assumptions. The sensitivity-only Arrhenius calculation fits ln D_app = ln D₀ − Ea/(k_B T), so Ea = −k_B × slope versus 1/T; k_B = 8.617333262145×10⁻⁵ eV/K. [All fit windows](../../results/amorphous_review_20260915/final_comparisons/LZOC_fit_table.csv) and [diagnostic Ea only](../../results/amorphous_review_20260915/final_comparisons/LZOC_Ea_diagnostic_NOT_validated.csv) are supplied.

RDFs normalize counts by neighbour number density and exact spherical-shell volume; self-pairs are excluded. CN is the direct number of neighbours within the stated cutoff. LiPON r_max = 4.75 Å; other new RDFs use 5 Å, below half the smallest perpendicular cell height. No smoothing or trajectory editing is applied. Mean pressure is the mean of the three normal stresses. Energy is divided by atom count; temporal drift is distinct from absolute energy across potentials. One glass per route is available; temporal SD is not an independent-replica uncertainty.

<a id="lzoc"></a>
## Reconstructed LZOC

### Matched LZOC comparison

Jobs 8675022.1–3 completed their separate 2 ps numerical check and 80 ps production at 340/360/380 K. Each production starts from its original input, not the check endpoint. The earlier 200 ps trajectories are truncated to their **first 80 ps only for this comparison**. Coordinates, cell and stored velocities match at the start; each dataset contains the initial configuration plus 800 frames spaced 0.1 ps apart. Raw 200 ps results are retained.

| Setting | Earlier route | New control |
|---|---|---|
| Potential, atoms, density | NEP89, 192, 2.2340 g/cm³ | Same |
| Ensemble | NVT MTTK | NVT Nosé–Hoover chain |
| Timestep | 0.5 fs | 2 fs |
| Thermostat coupling | 100 fs | 100 fs; project choice, not verified paper value |
| Compared duration | First 80 ps of 200 ps | 80 ps |
| Prehistory | Existing 10 ps ramp + 50 ps equilibration stage | Identical inherited start |

The 340/360/380 K, 2 fs and 80 ps transport settings follow [Hussain et al., 2024](https://doi.org/10.1038/s41524-024-01346-y). However, that transport branch used 48-atom AIMD. Our preparation draws on another branch and retains a reconstructed 192-atom NEP model without DFT volume optimization. **This is a joint thermostat/timestep control, not strict AIMD reproduction or an isolated timestep test.** [Full execution record](../../materials/candidates/LZOC_Hussain2024/aimd_aligned_80ps.md).

![Matched MSD](../../results/amorphous_review_20260915/final_comparisons/LZOC_matched80_MSD.png)

MSD uses all available time origins after periodic unwrapping and total-system mass-weighted centre-of-mass subtraction. All three panels share the same y scale; only lags up to 40 ps are displayed, while CSVs retain 80 ps. Neither Li-only COM removal nor amplitude rescaling is used. The two settings nearly coincide at 360 K but differ at 340 and 380 K.

| T / K | MTTK D_app / cm² s⁻¹ | NHC D_app / cm² s⁻¹ | MTTK R² | NHC R² |
|---|---:|---:|---:|---:|
|340|1.080×10⁻⁷|3.270×10⁻⁷|0.8409|0.9784|
|360|5.266×10⁻⁷|5.501×10⁻⁷|0.9894|0.9942|
|380|1.705×10⁻⁶|8.957×10⁻⁷|0.9987|0.9616|

All entries use a **10–40 ps lag fit with a free intercept**. These are finite-window apparent slopes, not certified long-time self-diffusion coefficients. The NHC log–log slopes are 0.333/0.464/0.574; an intercept and restricted sampling can affect this diagnostic, so it is not by itself proof of anomalous diffusion.

![Block sensitivity](../../results/amorphous_review_20260915/final_comparisons/LZOC_matched80_blocks.png)

Four consecutive 20 ps blocks are each fitted over 2–8 ps lag. Blocks are correlated portions of one trajectory, not independent glass replicas. A slightly negative block slope at 340 K is retained as a sign of estimator noise/plateau behaviour; it is not a physical negative diffusivity. Every full-trajectory 5–20, 10–30 and 10–40 ps fit is in [results.json](../../results/amorphous_review_20260915/final_comparisons/results.json). No window was chosen to obtain a desired Ea. Applying Arrhenius mechanically to the three NHC apparent slopes yields 0.220/0.325/0.280 eV for those windows respectively. **These are sensitivity diagnostics, not reported material activation energies; no 300 K extrapolation is adopted.**

![Matched thermodynamics](../../results/amorphous_review_20260915/final_comparisons/LZOC_matched80_thermo.png)

Thin traces are raw records, thick markers consecutive 20 ps means. Energy is absolute potential energy per atom, not zero-centred. Mean temperatures and pressures are stored in JSON; residual energy relaxation must be considered along with temperature control. Fixed NVT density does not demonstrate equilibrium. A finite 2 fs run is not a timestep-convergence test.

![Matched RDF](../../results/amorphous_review_20260915/final_comparisons/LZOC_matched80_RDF.png)

The representative 360 K comparison averages 40 frames at 41–80 ps, one per ps. Both settings use 0.05 Å bins and identical normalization/cutoffs. Data for all three temperatures are supplied. Similar first-shell statistics do not establish identical long-range structure or transport.

![Framework motion](../../results/amorphous_review_20260915/final_comparisons/LZOC_matched80_framework.png)

Framework MSD uses the same time-origin and COM treatment as Li. Zr/O/Cl displacements include vibrations and structural relaxation; these curves must not automatically be labelled anion diffusion. In the NHC 340 K case, Cl MSD at 40 ps is 0.923 Å² versus 0.447 Å² in the matched MTTK trajectory, accompanying the changed Li motion.

#### Experimental/AIMD context, not forced agreement

[Hu et al., 2023](https://doi.org/10.1038/s41467-023-39522-1) reports 2.42 mS/cm at 25 °C for nominal Li₁.₇₅ZrCl₄.₇₅O₀.₅; the experimental sample is not identical to one simulated amorphous configuration. Hussain's theoretical extrapolation is 43.3 ± 3.3 mS/cm at 300 K, with Ea = 0.25 ± 0.10 eV. These are different reference types and are not local D(T) measurements. Our higher-temperature apparent slopes cannot be compared as a room-temperature accuracy score.

### LZOC: a smaller timestep does not remove all sensitivity

![LZOC timestep and framework comparison](../../results/amorphous_review_20260915/targeted_diagnostics/LZOC_timestep_diagnostic.png)

**Panels a–d:** lithium time-origin-averaged MSD; apparent diffusion coefficient across fitting windows; framework-species MSD; consecutive 20 ps potential-energy means. Both runs start from identical positions, velocities and cell, at 380 K, with NVT Nosé–Hoover chain and a 100 fs coupling time. Each lasts 80 ps. Only the integration timestep differs (blue 0.5 fs; red 2 fs). MSD is shown to 40 ps lag, using the full 80 ps trajectory plus its starting frame; periodic wrapping and whole-system mass-weighted centre-of-mass motion are removed. No species-specific drift subtraction is used.

| MSD fit window (ps) | D, 0.5 fs (cm²/s) | D, 2 fs (cm²/s) | Relative difference |
|---|---:|---:|---:|
|5–20|1.13169×10⁻⁶|1.18405×10⁻⁶|−4.4%|
|10–30|1.09127×10⁻⁶|1.12433×10⁻⁶|−2.9%|
|10–40|1.00361×10⁻⁶|8.95684×10⁻⁷|+12.1%|

The relative difference is `(D_0.5fs / D_2fs − 1) × 100%`. These are diagnostic slopes, not established asymptotic diffusivities. The free-intercept relation is

$$\mathrm{MSD}(\tau)=b+6D\tau,\qquad D[\mathrm{cm^2/s}]=\frac{m[\mathrm{\AA^2/ps}]}{6}\times10^{-4}.$$

Here τ is lag time, m the fitted slope, b the intercept and D the apparent three-dimensional self-diffusion coefficient. The nonzero short-time offset affects log–log MSD slopes; values below one alone do not prove anomalous diffusion. Combined with window sensitivity and continued framework motion, these data do not yet establish long-time convergence. No new Ea or room-temperature conductivity is adopted. One trajectory per timestep gives no independent-replica confidence interval, and differences cannot be attributed uniquely to integration error rather than finite sampling.

### Original 200 ps series (not the matched80 ps estimator)

### LZOC thermodynamics

![LZOC thermodynamics](../../results/amorphous_review_20260915/analysis_complete/LZOC_thermodynamics.png)

Each column is one temperature. Coloured traces show all thermo records; black lines connect consecutive 5 ps block averages, not independent observations. Potential energy is absolute NEP energy per atom, not a zero-centred difference. Pressure is the mean of the three normal components. Axes auto-scale separately, so compare values rather than visual fluctuation heights.

| Target / K | Mean T / K | Mean P / GPa | Fixed density / g cm⁻³ |
|---|---:|---:|---:|
|340|339.761|−0.1860|2.2340|
|360|360.543|−0.1106|2.2340|
|380|380.174|−0.2227|2.2340|

Temperatures track their targets. The 380 K energy declines in the final 50 ps block, so stationarity is not established. Constant NVT density is imposed, not evidence of density convergence. Source: `LZOC_*K_thermo.csv` and [four-block records](../../results/amorphous_review_20260915/LZOC_transport/basic_thermo_validation.json).

### Li MSD and fit sensitivity

![LZOC MSD](../../results/amorphous_review_20260915/analysis_complete/LZOC_MSD.png)

Periodic trajectories are unwrapped between saved frames, and total-system mass-weighted centre-of-mass motion is removed. Li-only centre-of-mass subtraction is not used. The plotted MSD averages all available time origins. The linear view stops at 100 ps to avoid the least-sampled long-lag tail; CSV files retain all 200 ps lags. FFT results were checked against direct displacement averages at three lags.

MSD(τ) = mean over Li atoms and valid origins of |r(t+τ)−r(t)|². Fit MSD = aτ+b, with a free intercept. The finite-window estimate is D_app = a/6 ×10⁻⁴ cm²/s when a is in Å²/ps. These are exploratory slopes, not established long-time diffusion coefficients.

| T / K | D_app, 20–80 ps / cm² s⁻¹ | Linear R² | Intercept / Å² |
|---|---:|---:|---:|
|340|1.814×10⁻⁷|0.9965|1.085|
|360|1.715×10⁻⁷|0.9657|1.366|
|380|1.028×10⁻⁶|0.9984|1.553|

![LZOC MSD robustness](../../results/amorphous_review_20260915/analysis_complete/LZOC_MSD_robustness.png)

Left: four contiguous 50 ps trajectory blocks, each fitted over 5–20 ps lag. Right: full-trajectory fits with four specified lag windows. These two panels have different lag definitions and must not be treated as equivalent estimators. No window was selected to target an activation energy.

| T / K | Mean of four block slopes / cm² s⁻¹ | Block SD / cm² s⁻¹ |
|---|---:|---:|
|340|4.551×10⁻⁷|2.397×10⁻⁷|
|360|6.505×10⁻⁷|7.285×10⁻⁸|
|380|1.300×10⁻⁶|4.505×10⁻⁷|

SD describes within-trajectory block variability, not a standard error, confidence interval or independent-replica uncertainty. The 380 K block values decrease from 1.865×10⁻⁶ to about 0.950×10⁻⁶ cm²/s. Low-temperature intercepts and window sensitivity limit diffusion interpretation. A log–log slope below one alone is not proof of anomalous diffusion because of the finite intercept. **No formal Ea or 300 K extrapolation is reported.**

Data: `LZOC_*K_msd.csv`, `LZOC_*K_block_D.csv`, `summary.json`.

### LZOC local structure and framework motion

![LZOC RDF](../../results/amorphous_review_20260915/analysis_complete/LZOC_RDF.png)

RDFs use 100 frames from 101–200 ps, spaced 1 ps apart, minimum-image periodic distances, excluded self-pairs and shell/number-density normalization. Bin width 0.05 Å, range 0–5 Å, below half the minimum perpendicular cell height. No smoothing. Large Zr–O peak height partly reflects a dilute O denominator and localized distances; peak height alone is not a coordination number or an error.

![LZOC coordination](../../results/amorphous_review_20260915/analysis_complete/LZOC_coordination.png)

Time series sample 1–200 ps at 1 ps spacing. Cutoffs appear in titles; Cl–Cl is a geometrical neighbour count, not chemical valence. Late Li–Cl means are 4.850, 4.752, 4.804; Zr–Cl 4.997, 4.987, 4.966; Zr–O 1.333, 1.333, 1.332 at 340/360/380 K. Similar local statistics do not certify long-range disorder or thermodynamic stability.

![LZOC framework MSD](../../results/amorphous_review_20260915/analysis_complete/LZOC_framework_MSD.png)

Zr/O/Cl time-origin averaged MSD is computed with the same unwrapping and system-COM correction as Li. At 80 ps, Zr is 0.249–0.498 Å², O 0.183–0.301 Å² and Cl 0.661–0.968 Å². Nonzero framework MSD may include local relaxation/vibration and is not automatically anion conduction. Data: `LZOC_*K_rdf.csv`, `LZOC_*K_coordination.csv`; framework curves are regenerated from the script and raw trajectories.

<a id="lszc"></a>
## LSZC

### LSZC: actual experimental structural anchors

The current route uses independently packed clusters (272 atoms), not the earlier replicated crystalline seed. Following packing/position relaxation and a 300 K diagnostic, it completed a 100 ps ramp to 400 K and 20 ps hold. The last 10 ps contains 100 saved configurations.

![LSZC coordination](../../results/amorphous_review_20260915/final_comparisons/LSZC_coordination_distribution.png)

All sampled S atoms retain four O neighbours below 1.9 Å. Zr–O and Zr–Cl exhibit distributions rather than a single coordination state. Fractions count atom–frame observations and do not represent independent-sample probabilities or formal confidence intervals.

![LSZC experimental comparison](../../results/amorphous_review_20260915/final_comparisons/LSZC_EXAFS_comparison.png)

| Quantity | Current NEP trajectory | Tang 2026 experiment |
|---|---:|---:|
| Zr–O coordination |1.532; cutoff 2.6 Å|2.6; EXAFS fitted CN|
| Zr–Cl coordination |4.218; cutoff 3.2 Å|3.0; EXAFS fitted CN|
| Zr–O first RDF maximum / fitted distance|1.875 Å|2.23 Å|
| Zr–Cl first RDF maximum / fitted distance|2.425 Å|2.45 Å|

The Zr–O discrepancy is substantial even though sulfate tetrahedra survive. RDF maxima (0.05 Å bins) and EXAFS fitted shell distances are different observables; the dashed lines mark fitted bond lengths, not phase-uncorrected Fourier-transform peak positions. Temperature, size, density, preparation and potential also differ. This is a diagnostic comparison, not a quantitative fit to the experiment. Source: [Tang et al., 2026](https://doi.org/10.1038/s41467-026-69737-x), main text and Supplementary Table 9.

Current imposed density is 1.86376 g/cm³ versus 2.03549 g/cm³ in author Data 2 (8.44% lower); the latter is a deposited geometry, **not an experimental density measurement**. [Author-geometry RDF comparison and ramp thermodynamics](../../results/amorphous_review_20260915/analysis_complete/report_en.md#5-lszc-preparation-and-structural-comparison). Experimental conductivity 1.5 mS/cm at 30 °C and Ea 0.33 eV are future transport anchors. A 400 K preparation hold cannot establish those quantities.

### LSZC: is the Zr coordination discrepancy a cutoff artefact?

The last100 frames of the existing400 K hold (10.1–20 ps) were counted using the following predeclared distance grid. The previous primary cutoffs remain Zr–O2.6 Å and Zr–Cl3.2 Å.

| Zr neighbour | Cutoff / Å | Mean neighbours |
|---|---:|---:|
|O|2.2|1.2994|
|O|2.4|1.4966|
|O|2.6|1.5316|
|O|2.8|1.5466|
|O|3.0|1.6175|
|Cl|2.8|4.0244|
|Cl|3.0|4.1628|
|Cl|3.2|4.2178|
|Cl|3.4|4.2584|
|Cl|3.6|4.2953|

Across these grids, Zr–O remains below the experimental EXAFS fitted CN2.6 and Zr–Cl above CN3.0 reported by [Tang 2026](https://doi.org/10.1038/s41467-026-69737-x). Thus modest variation around our chosen cutoffs does not remove the discrepancy. This does not equate EXAFS fitting with direct neighbour counting, or prove that all conceivable cutoffs fail. Density, preparation, potential and temperature remain different.

[All values and frame SD](../../results/amorphous_review_20260915/structure_followup/LSZC_cutoff_sensitivity.csv). SD is temporal variability, not uncertainty across independent structures. The earlier Zr–O RDF maximum difference also remains; none of the source distances has been changed.

### LSZC: volume relaxation does not resolve local-structure disagreement

![LSZC volume and local structure](../../results/amorphous_review_20260915/targeted_diagnostics/LSZC_volume_structure_diagnostic.png)

**Panels a–d:** stage-relative density; consecutive 5 ps pressure means; Zr–O and Zr–Cl RDFs. Blue is the preceding 400 K NVT hold; red is the subsequent 400 K, 1 bar NPT diagnostic. These are sequential stages of one 272-atom structure, not independent replicas or simultaneous branches. Each stage lasts 20 ps. RDFs use ten snapshots at 11–20 ps (1 ps spacing), minimum-image distances, per-frame volume normalisation and 0.05 Å bins; curves are not smoothed. Lines connecting pressure means are guides, not continuous measurements. The 1 bar line applies to the NPT target, not a pressure constraint on NVT.

| Quantity | Previous NVT | NPT diagnostic |
|---|---:|---:|
| Density, final 10 ps (g/cm³) | 1.86376, fixed cell | 1.81550 |
| Zr–O mean coordination, cutoff 2.6 Å | 1.53156 | 1.51594 |
| Zr–Cl mean coordination, cutoff 3.2 Å | 4.21781 | 4.25969 |
| Fraction of S with four O neighbours, cutoff 2.0 Å | 1.00 | 1.00 |

Coordination averages use 100 final-stage frames at 0.1 ps spacing. The density decreases by about 2.59% relative to the starting fixed cell; pressure block means are reduced, but RDF first-shell peaks and Zr coordination remain similar. Thus this short pressure-relaxation test **does not correct the reference mismatch**. It neither proves an equilibrated glass nor identifies the potential as the sole cause. Preparation, finite size, and model applicability remain possible contributors. The reference EXAFS comparison and its non-equivalence to a simple cutoff count are retained in the [earlier analysis](../../results/amorphous_review_20260915/final_comparisons/report_en.md).

### LSZC preparation and structural comparison

![LSZC thermodynamics](../../results/amorphous_review_20260915/analysis_complete/LSZC_thermodynamics.png)

The dashed marker at 100 ps separates ramp and hold. Mean hold temperature is 399.42 K; pressure 0.03957 GPa. Energy decreases slightly during the hold. No diffusion coefficient is inferred from a heating trajectory.

![LSZC RDF](../../results/amorphous_review_20260915/analysis_complete/LSZC_RDF.png)

Grey: a single pre-ramp configuration. Blue: the last 10 ps of the 400 K hold, 100 frames. Different averaging makes the grey curve noisier; smoothness is not evidence that one structure is more physical. These are within-project structural comparisons.

![LSZC coordination](../../results/amorphous_review_20260915/analysis_complete/LSZC_coordination.png)

S–O uses a 1.9 Å cutoff. Of 3200 S/frame observations during the hold, 3199 are fourfold and one is threefold; all S atoms are fourfold in the last 10 ps. A transient cutoff crossing is not proof of bond breaking. Late means: Zr–O 1.532, Zr–Cl 4.218, Li–Cl 4.275 at the plotted cutoffs.

![LSZC author geometry comparison](../../results/amorphous_review_20260915/analysis_complete/LSZC_author_structure_comparison.png)

Grey is computed from the author's deposited 1088-atom Data 2 geometry, **not an experimental RDF or trajectory average**. Blue is our 272-atom NEP hold. Composition ratios match, but preparation, size, potential, density and averaging differ. The reference geometry density is 2.03549 g/cm³ versus our imposed 1.86376 g/cm³ (about 8.44% lower). Thus local tetrahedral retention does not imply full structural reproduction. Source CSV: `LSZC_author_reference_RDF.csv`; reference SHA256 in `summary.json`.

<a id="lps"></a>
## Li₃PS₄

### Li₃PS₄: published source-data comparison

The existing NEP preparation includes a 1500 K, 100 ps melt and cooling at 2.5 K/ps to 300 K under NPT, as in [Chen et al., 2025](https://doi.org/10.1038/s41467-025-56322-x). NEP replaces DeePMD, and the replicated training-frame start, coupling choices and final 20 ps hold differ. This is not the cancelled Zhou 2024 route. The final hold has only 20 frames at 1 ps spacing; the present structural average uses the final 10 frames.

![Li3PS4 source comparison](../../results/amorphous_review_20260915/final_comparisons/Li3PS4_Chen_structure_comparison.png)

The red curves are **author-provided numerical source data**, not reconstructed screenshots or our AIMD calculations: workbook sheets Fig. 1e (glass Li–S g(r)) and Fig. 1f (glass S–P–S). Our Li–S maximum is 2.425 Å versus 2.459 Å in the source grid. The angular mean is 109.40° and the distributions occupy a similar tetrahedral-angle range. The angle curves are normalized independently to unit area; our bins are 2° versus the author's finer grid. Peak-height differences therefore cannot be interpreted solely as physical differences. The exact averaging temperature/interval of the author Fig. 1 curves is not independently established here; this is a structural benchmark, not a matched-trajectory test.

![Li3PS4 coordination](../../results/amorphous_review_20260915/final_comparisons/Li3PS4_coordination_distribution.png)

All sampled P atoms have four S neighbours below 2.6 Å. Li–S coordination averages 5.366 below 3.2 Å. **P–S four-coordination is not the fraction of isolated PS₄ units**: distinguishing P₂S₆/P₂S₇/PS₄ has now been checked by the geometric connectivity analysis below; no equality with the author's Fig. 1g speciation is claimed. Mean hold T = 298.66 K, P = −0.00012 GPa, density = 2.21305 g/cm³. These local results support this candidate as a useful methodological control, not yet an experimental conductivity prediction.

The paper's workbook and extracted sheet labels are identified in [literature_source.json](../../results/amorphous_review_20260915/final_comparisons/literature_source.json). Structural curves are compared with the paper's glass, not its crystalline or glass-ceramic branches. Extracted transport sheets are retained for provenance but no transport number is transferred to our short hold.

### Li₃PS₄: coordination does not determine connectivity

We analysed the last ten frames (11–20 ps, 1 ps spacing) of the existing 300 K NPT hold. A periodic minimum-image graph includes P–S edges below each of 2.4/2.6/2.8 Å and P–P edges below 2.6 Å. Li is excluded. Labels below describe connected-component atom counts, **not independently verified chemical species or bond orders**. Free S in this graph means no P neighbour at these cutoffs, not necessarily an isolated physical atom.

All ten frames and all three P–S cutoffs give the same counts:

| Geometric component | Components per frame | P atoms represented | Fraction of all 64 P |
|---|---:|---:|---:|
|P₁S₄|51|51|79.6875%|
|P₂S₇|5|10|15.6250%|
|P₃S₁₀|1|3|4.6875%|
|S without a P edge|7|0|—|

Atom conservation: 51+2×5+3=64 P; 4×51+7×5+10+7=256 S. Seven S atoms per frame have at least two P neighbours (2.7344% of S). No P–P pairs fall below 2.6 Å. Results are identical over this cutoff range; no cutoff was chosen to match a paper.

The earlier result “all P have four S neighbours” remains correct, but it does not imply all P belong to isolated PS₄. The [Chen 2025 structural comparison](../../results/amorphous_review_20260915/final_comparisons/report_en.md#4-li₃ps₄-published-source-data-comparison) concerns RDF and angle distributions. The author's chemical-speciation percentages are not automatically comparable with this graph's P-weighted fractions; definitions and denominators must match before reporting an error percentage. **Local RDF/angle agreement does not establish network/speciation agreement.**

Source: [per-frame components](../../results/amorphous_review_20260915/structure_followup/Li3PS4_geometric_components.csv), [summary and trajectory hashes](../../results/amorphous_review_20260915/structure_followup/results.json). These frames come from one prepared glass, not ten independent glasses.

<a id="lipon"></a>
## LiPON

### LiPON: completed diagnosis, unresolved chemistry

The existing route follows selected 2000 K/10 ps melt and 250 K quench parameters from [Seth et al., 2025](https://doi.org/10.1021/acsmaterialsau.4c00117), with an independent 124-atom precursor and NEP instead of NequIP. The 250 K/1 bar/20 ps NPT release is a project diagnostic, not the paper's full protocol. No new DFT is planned or performed.

![LiPON contact](../../results/amorphous_review_20260915/final_comparisons/LiPON_NN_release.png)

The minimum N–N separation stays between 1.270 and 1.347 Å in all 200 release frames. Pressure improves to 0.00614 GPa and density to 2.50908 g/cm³, but this does not remove the contact. The 1.6 Å line is an operational screening cutoff, not a universal chemical acceptance criterion. [Existing origin tracing](../../results/amorphous_review_20260915/LiPON/contact_origin.md) places its formation at 2.2–2.3 ps of the 2000 K hold.

![LiPON coordination](../../results/amorphous_review_20260915/final_comparisons/LiPON_coordination_distribution.png)

Late mean P–O and P–N counts below 2.1 Å are 3.688 and 0.438. Two of five N atoms have a short N neighbour, explaining the 0.4 fraction in the N–N panel. A distance alone does not establish the electronic bonding state. This configuration is retained as a limitation/failure-case analysis, not promoted to a quantitatively validated LiPON transport model. Composition-specific experimental/AIMD validation of this short contact is unavailable; no substitute values are invented.

<a id="legacy"></a>
## Legacy LZOC: MACE versus NEP

### Runtime

#### Additional existing-data audit: 700–900 K thermodynamics

|T/K|MACE mean density/g cm⁻³|NEP mean density/g cm⁻³|MACE ΔPE/eV atom⁻¹|NEP ΔPE/eV atom⁻¹|
|---|---:|---:|---:|---:|
|700|1.14742|1.78576|−0.00385|−0.00976|
|800|1.27278|1.66334|−0.00059|−0.01075|
|900|0.92513|1.53955|−0.00015|−0.00922|

ΔPE is the final50 ps mean minus the first50 ps mean of the existing200 ps NVT production, not an energy difference between potentials. MACE includes its t=0 record (4001 records); NEP has4000 records starting at0.05 ps. Mean temperatures lie within about1.1 K of target. These trajectories have different imposed densities and preparation histories; appreciable NEP energy relaxation and density differences preclude ranking transport accuracy from MSD amplitude alone. This adds thermodynamic analysis, **not yet the missing high-temperature RDF/MSD comparison or the later NPT-extension analysis**. [Table](../../results/LZOC/legacy_comparison_20260915/highT_thermo_summary.csv) · [Hashes](../../results/LZOC/legacy_comparison_20260915/highT_source_hashes.json) · [Script](../../scripts/structures/summarize_legacy_highT.py).

![Runtime](../../results/LZOC/legacy_comparison_20260915/01_runtime.png)

Left: actual scheduler job runtimes excluding queues for 600/700/800/900 K. Right: engine-reported 600 K production runtime for 200 ps, 400,000 steps, 0.5 fs. MACE/LAMMPS took 11,395.5 s; NEP89/GPUMD 366.428 s, a ratio of 31.10. Both requested gpu_1, but nodes, engines and preprocessing differ; this is not an isolated potential-kernel benchmark. The four-job sums are 18 h 25 min versus 34 min, not parallel elapsed time or points cost. [Timing provenance and job IDs](LZOC/candidate3_mace_nep_comparison.md).

### Density and thermodynamics at 600 K

![Density and thermodynamics](../../results/LZOC/legacy_comparison_20260915/02_density_thermodynamics.png)

Each model has 50 ps NPT followed by 200 ps NVT. Matched axes are used by column. The dotted density is the common 300 K input, not experiment. NVT density is imposed by the final NPT cell. Energy is explicitly (PE−its own production mean)/192, converted to meV/atom. Zero-centred energy is a plotting definition, not zero absolute potential energy; it is not an NVE conservation test. Comparing absolute energies of distinct potentials would not establish accuracy.

|600 K quantity|MACE|NEP89|
|---|---:|---:|
|Production density / g cm⁻³|1.468304|1.875429|
|Volume increase relative to 300 K input|30.3%|2.0%|
|Mean temperature / K|598.89|599.96|

These trajectories occupy different densities and structures. Larger motion cannot be attributed only to a different migration barrier, and smaller expansion does not itself establish realism.

### Local structure

![RDF and coordination](../../results/LZOC/legacy_comparison_20260915/03_RDF_coordination.png)

RDF uses the last 50 ps, 21 frames spaced 2.5 ps apart, periodic minimum-image distances, excluded self-pairs, 0.05 Å bins and no smoothing. The five pairs have matched definitions in both models. Coordination cutoffs are Li–Cl 3.2, Li–O 2.7, Zr–Cl 3.0, Zr–O 2.6 and Cl–Cl 4.0 Å. Cl–Cl denotes geometric neighbours, not valence. Lines between categorical coordination points only guide the eye. Frame SD is in `coordination.csv`; it is not independent-replica uncertainty. No individual-atom coordination distribution is inferred from these means.

|Late mean neighbour count|MACE|NEP89|
|---|---:|---:|
|Li–Cl|3.666|4.542|
|Li–O|0.145|0.293|
|Zr–Cl|4.442|4.839|
|Zr–O|1.125|1.208|
|Cl–Cl|4.472|6.355|

Similar short-range peak positions do not demonstrate a stationary framework. This plot contains model results only, not experimental or AIMD RDF curves.

### Li transport and framework motion

![MSD and framework](../../results/LZOC/legacy_comparison_20260915/04_MSD_framework.png)

Top left: time-origin averaged Li MSD with total-system mass-weighted COM motion removed, not Li-only COM subtraction. The display ends at 100 ps; the CSV retains the full lag range. Fit MSD=aτ+b with free intercept and D_app=(a/6)×10⁻⁴ cm²/s for a in Å²/ps. τ is lag time, not a selected percentage of the trajectory.

|600 K estimate|MACE|NEP89|
|---|---:|---:|
|D_app, 20–80 ps / cm² s⁻¹|1.7197×10⁻⁵|1.0757×10⁻⁵|
|Linear R²|0.9965|0.9998|
|Four-block mean / cm² s⁻¹|2.3955×10⁻⁵|1.006×10⁻⁵|
|Four-block SD / cm² s⁻¹|0.4886×10⁻⁵|0.281×10⁻⁵|

Top right compares full-trajectory lag windows. Bottom left uses four consecutive 50 ps blocks, each fitted over 5–20 ps lag. Block SD is temporal variability, not a confidence interval and not an error bar for the full-trajectory 20–80 ps estimate. High linear R² does not demonstrate converged diffusion.

Bottom right compares **single-origin**, total-system-COM-corrected displacement at 200 ps. It is a different estimator from the time-origin averaged Li curve. Zr/O/Cl endpoints are respectively 58.32/43.18/92.74 Å² for MACE and 9.87/5.60/21.00 Å² for NEP. These show appreciable framework motion; they do not alone prove melting or chemical decomposition. Lines between species only guide the eye.

### Interpretation and data scope

NEP was faster and showed less expansion and weaker framework motion in this 600 K comparison. This supports its use for economical exploratory work, not a claim of superior experimental accuracy. The comparison changes potential, engine, preprocessing, velocity seed and relaxed cell simultaneously. No DFT is proposed. No new Ea or 300 K conductivity extrapolation is made from these structurally differing states.

All four-temperature timing records are included. Structural/transport panels cover **600 K only**: NEP's later 700–900 K and extra NPT runs are not analysed in this package and have not been substituted with another route. The next stage, if desired, is the same source-verified analysis of those existing runs, not new MD.

[Script](../../scripts/structures/plot_legacy_lzoc_comparison.py), [summary and CSV input hashes](../../results/LZOC/legacy_comparison_20260915/summary.json), [source audit](../../results/LZOC/analysis_20260912/README.md). Re-run with the existing Python/numpy/matplotlib environment from the repository root. Four figures exported as PNG/PDF/SVG with editable vector text. Data and scripts are committed; raw trajectories are retained separately and not uploaded in this commit.

<a id="remaining"></a>
## Remaining work and decision rules

| Item | Status | What is needed before a stronger claim |
|---|---|---|
|Atom counts, finite outputs, temperature, block energies, distances and RDF/CN|Completed for the analysed stages|Continue these basic checks for any new calculation; successful execution is not equilibration|
|New LZOC D/Ea|Window/block sensitivity established, not converged|A declared longer-time/independent-sampling test if this route is continued; do not select a preferred Ea|
|LSZC reference agreement|NPT and cutoff diagnostics completed; mismatch persists|Revisit preparation/model applicability before transport production; more of the same NPT is not a demonstrated remedy|
|Li₃PS₄ transport and species fractions|Dedicated transport array8675738 submitted; geometric network counted|Finish and validate the trajectories; resolve reference units and species definitions before quantitative comparison|
|LiPON chemistry|Contact origin and persistence documented|Retain limitation without pretending MD extension resolves chemical validity; no DFT available/requested|
|Legacy700–900 K detailed structure/transport|Timing and basic thermodynamics complete; RDF/MSD and later NPT-extension analysis pending|Continue archived-data analysis, not current evidence for model accuracy|
|Independent-glass and size uncertainty|Not established|Do not treat time frames/temperature branches as independent glasses|
|Raman/IR and experimental scattering fits|Not established|Appropriate response/weighting and matching source data are needed; no synthetic experimental curves|

**Record policy:** update these two overview files in place. Keep scripts, PNG/PDF/SVG and CSV/JSON in their existing directories; older Markdown files carry snapshot notices. Raw trajectories remain on TSUBAME and locally, not in Git. Never delete or rescale data to hide disagreement. The existing≤100-point alert remains a separate read-only monitor; no points figure here is a live balance.

All27 existing figure families are embedded above, each with its interpretation. This means documentation coverage is consolidated, not that every material has achieved quantitative experimental agreement. Original snapshots and Git history preserve earlier status records; only this overview is current.
