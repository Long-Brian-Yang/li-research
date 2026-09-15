> Historical snapshot. The complete, maintained report is [here](../../../docs/materials/materials_overview_en.md).

# Completed-run analysis: reconstructed LZOC and LSZC

Updated 15 September 2026. This package completes the stated postprocessing of existing runs, not validation of quantitative predictive accuracy. No new MD or DFT was submitted. [Japanese version](report_ja.md).

## 1. Scope and reproducibility

LZOC: Li42Zr24Cl114O12, 192 atoms, NEP89/GPUMD. Jobs 8674278.1–3 at 340/360/380 K each contain a 10 ps ramp, 50 ps equilibration stage and 200 ps NVT production, timestep 0.5 fs. LSZC: Li32Zr32Cl128S16O64, 272 atoms, job 8674277, 100 ps ramp from 300 to 400 K plus 20 ps NVT hold. Thermostat MTTK period 100 fs. An equilibration stage name does not establish equilibrium.

One prepared configuration per route; temperature branches are not independent glass replicas. Raw data remain unchanged. [Executable analysis](../../../scripts/structures/finish_amorphous_analysis.py), [numerical summary and source SHA256](summary.json), [LZOC basic validation](../LZOC_transport/README.md), [LSZC basic validation](../LSZC_anneal/README.md).

Re-run from repository root with the existing ASE/numpy/scipy/matplotlib Python environment:

```bash
MPLCONFIGDIR=/tmp/lzoc-mpl python scripts/structures/finish_amorphous_analysis.py
```

## 2. LZOC thermodynamics

![LZOC thermodynamics](LZOC_thermodynamics.png)

Each column is one temperature. Coloured traces show all thermo records; black lines connect consecutive 5 ps block averages, not independent observations. Potential energy is absolute NEP energy per atom, not a zero-centred difference. Pressure is the mean of the three normal components. Axes auto-scale separately, so compare values rather than visual fluctuation heights.

| Target / K | Mean T / K | Mean P / GPa | Fixed density / g cm⁻³ |
|---|---:|---:|---:|
|340|339.761|−0.1860|2.2340|
|360|360.543|−0.1106|2.2340|
|380|380.174|−0.2227|2.2340|

Temperatures track their targets. The 380 K energy declines in the final 50 ps block, so stationarity is not established. Constant NVT density is imposed, not evidence of density convergence. Source: `LZOC_*K_thermo.csv` and [four-block records](../LZOC_transport/basic_thermo_validation.json).

## 3. Li MSD and fit sensitivity

![LZOC MSD](LZOC_MSD.png)

Periodic trajectories are unwrapped between saved frames, and total-system mass-weighted centre-of-mass motion is removed. Li-only centre-of-mass subtraction is not used. The plotted MSD averages all available time origins. The linear view stops at 100 ps to avoid the least-sampled long-lag tail; CSV files retain all 200 ps lags. FFT results were checked against direct displacement averages at three lags.

MSD(τ) = mean over Li atoms and valid origins of |r(t+τ)−r(t)|². Fit MSD = aτ+b, with a free intercept. The finite-window estimate is D_app = a/6 ×10⁻⁴ cm²/s when a is in Å²/ps. These are exploratory slopes, not established long-time diffusion coefficients.

| T / K | D_app, 20–80 ps / cm² s⁻¹ | Linear R² | Intercept / Å² |
|---|---:|---:|---:|
|340|1.814×10⁻⁷|0.9965|1.085|
|360|1.715×10⁻⁷|0.9657|1.366|
|380|1.028×10⁻⁶|0.9984|1.553|

![LZOC MSD robustness](LZOC_MSD_robustness.png)

Left: four contiguous 50 ps trajectory blocks, each fitted over 5–20 ps lag. Right: full-trajectory fits with four specified lag windows. These two panels have different lag definitions and must not be treated as equivalent estimators. No window was selected to target an activation energy.

| T / K | Mean of four block slopes / cm² s⁻¹ | Block SD / cm² s⁻¹ |
|---|---:|---:|
|340|4.551×10⁻⁷|2.397×10⁻⁷|
|360|6.505×10⁻⁷|7.285×10⁻⁸|
|380|1.300×10⁻⁶|4.505×10⁻⁷|

SD describes within-trajectory block variability, not a standard error, confidence interval or independent-replica uncertainty. The 380 K block values decrease from 1.865×10⁻⁶ to about 0.950×10⁻⁶ cm²/s. Low-temperature intercepts and window sensitivity limit diffusion interpretation. A log–log slope below one alone is not proof of anomalous diffusion because of the finite intercept. **No formal Ea or 300 K extrapolation is reported.**

Data: `LZOC_*K_msd.csv`, `LZOC_*K_block_D.csv`, `summary.json`.

## 4. LZOC local structure and framework motion

![LZOC RDF](LZOC_RDF.png)

RDFs use 100 frames from 101–200 ps, spaced 1 ps apart, minimum-image periodic distances, excluded self-pairs and shell/number-density normalization. Bin width 0.05 Å, range 0–5 Å, below half the minimum perpendicular cell height. No smoothing. Large Zr–O peak height partly reflects a dilute O denominator and localized distances; peak height alone is not a coordination number or an error.

![LZOC coordination](LZOC_coordination.png)

Time series sample 1–200 ps at 1 ps spacing. Cutoffs appear in titles; Cl–Cl is a geometrical neighbour count, not chemical valence. Late Li–Cl means are 4.850, 4.752, 4.804; Zr–Cl 4.997, 4.987, 4.966; Zr–O 1.333, 1.333, 1.332 at 340/360/380 K. Similar local statistics do not certify long-range disorder or thermodynamic stability.

![LZOC framework MSD](LZOC_framework_MSD.png)

Zr/O/Cl time-origin averaged MSD is computed with the same unwrapping and system-COM correction as Li. At 80 ps, Zr is 0.249–0.498 Å², O 0.183–0.301 Å² and Cl 0.661–0.968 Å². Nonzero framework MSD may include local relaxation/vibration and is not automatically anion conduction. Data: `LZOC_*K_rdf.csv`, `LZOC_*K_coordination.csv`; framework curves are regenerated from the script and raw trajectories.

## 5. LSZC preparation and structural comparison

![LSZC thermodynamics](LSZC_thermodynamics.png)

The dashed marker at 100 ps separates ramp and hold. Mean hold temperature is 399.42 K; pressure 0.03957 GPa. Energy decreases slightly during the hold. No diffusion coefficient is inferred from a heating trajectory.

![LSZC RDF](LSZC_RDF.png)

Grey: a single pre-ramp configuration. Blue: the last 10 ps of the 400 K hold, 100 frames. Different averaging makes the grey curve noisier; smoothness is not evidence that one structure is more physical. These are within-project structural comparisons.

![LSZC coordination](LSZC_coordination.png)

S–O uses a 1.9 Å cutoff. Of 3200 S/frame observations during the hold, 3199 are fourfold and one is threefold; all S atoms are fourfold in the last 10 ps. A transient cutoff crossing is not proof of bond breaking. Late means: Zr–O 1.532, Zr–Cl 4.218, Li–Cl 4.275 at the plotted cutoffs.

![LSZC author geometry comparison](LSZC_author_structure_comparison.png)

Grey is computed from the author's deposited 1088-atom Data 2 geometry, **not an experimental RDF or trajectory average**. Blue is our 272-atom NEP hold. Composition ratios match, but preparation, size, potential, density and averaging differ. The reference geometry density is 2.03549 g/cm³ versus our imposed 1.86376 g/cm³ (about 8.44% lower). Thus local tetrahedral retention does not imply full structural reproduction. Source CSV: `LSZC_author_reference_RDF.csv`; reference SHA256 in `summary.json`.

## 6. Literature comparison and limits

[Hussain 2024](https://doi.org/10.1038/s41524-024-01346-y) uses a 48-atom, 340/360/380 K AIMD transport branch and reports a Li–Cl first peak near 2.5 Å. Our peaks are 2.375/2.375/2.425 Å (0.05 Å bins). This checks local length scale, not predictive accuracy. Our 192-atom NEP route is not exact reproduction. The paper's extrapolated conductivity is a theoretical result, not a matching experimental D(T) dataset.

[Tang 2026](https://doi.org/10.1038/s41467-026-69737-x) and its deposited Data 2 supply the LSZC structural reference above. Our small-cell independent cluster route must remain distinguished from the author's preparation. No experimental conductivity curve was invented for either material.

## 7. Delivery and remaining scientific questions

Delivered: 10 figure families, each PNG/PDF/SVG; source CSV/JSON; script; this report and Japanese version. Completed within this scope: basic thermodynamic/geometry checks, local structural comparison, LZOC MSD/window/block diagnostics and reference-source distinctions.

Not established: converged low-temperature D/Ea, strict amorphous-phase certification, finite-size convergence, replicate uncertainty or agreement with experimental conductivity. These are explicit findings/limits, not missing plots to be filled with assumed data. Further production for LSZC or extension of LZOC needs a separate computational decision. LiPON and Li₃PS₄ are not reanalysed by this script.
