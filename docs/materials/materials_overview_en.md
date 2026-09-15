# Material Review — Amorphous Solid Electrolytes

Updated 15 September 2026. [日本語](materials_overview_ja.md)

This is the complete English Material Review. Read the methods, figures, numerical tables and interpretation here in sequence; opening another report is not required. Source files and scripts are optional audit material collected at the end. Eleven core figure groups replace the previous 43 displays. Redundant diagnostics are summarized directly in tables; unfavourable results are retained. This revision changes presentation, not trajectories, fit windows, numerical results or simulation settings.

## Contents

- [Status and preparation](#status)
- [Definitions and units](#methods)
- [Reconstructed LZOC](#lzoc)
- [LSZC](#lszc)
- [Li₃PS₄](#lps)
- [LiPON](#lipon)
- [Legacy LZOC: MACE–NEP](#legacy)
- [Remaining work and source record](#remaining)

<a id="status"></a>
## Status and preparation

Four chemical systems, five preparation routes. New and legacy LZOC have the same nominal composition; LZOC/LSZC are the oxyhalide main line, Li₃PS₄ a method control and LiPON a limitation case. Cancelled Zhou2024 work is not counted as executed. Crystalline Li₃YCl₆/LiNbOCl₄ work is unchanged.

|Route|Model size|Completed / submitted|Interpretation|
|---|---|---|---|
|New LZOC|192: Li42Zr24Cl114O12|340/360/380 K production, matched80 ps NHC/MTTK comparison and380 K timestep diagnostic analysed|Direct AIMD table comparison available; long-time convergence not established|
|LSZC|272: Li32Zr32Cl128S16O64|Cluster packing, relaxation,400 K NPT and200 ps NVT analysed;320/330/340/350 K array8676216 submitted|Sulfate retained; Zr environment and density differ from reference; new four-temperature results await analysis|
|Li₃PS₄|512: Li192P64S256|300/500/700/900 K200 ps production analysed, array8675738|Transport differs from reference;300 K plateau and900 K host motion remain|
|LiPON|124: Li47P16O56N5|Preparation,pressure release and paired0.5/0.25 fs checks analysed|Short N–N contacts persist; no long transport prediction|
|Legacy LZOC|192, same nominal LZOC|600 K detailed comparison,700–900 K MSD/RDF andfour-temperature timing analysed|Efficiency and structural sensitivity, not an accuracy ranking|

“Submitted” is not “analysed.” The new LSZC array is not assessed in this figure-only revision. No new MD or DFT was submitted here.

### Preparation and literature differences

|Route|Executed preparation / transport|Reference and difference|
|---|---|---|
|New LZOC|100 K2 ps;500 K30 ps;1000 K50 ps;1500 K30 ps;2000 K20 ps; cooling via1500/1000/500/100 K,2 ps each;300 K20+50 ps. Transport details below.|[Hussain2024](https://doi.org/10.1038/s41524-024-01346-y):192-atom reconstructed NEP is not its48-atom AIMD transport model or exact preparation protocol|
|LSZC|Five finite cluster types, two copies each +32Li; fixed-cell relaxation to0.0493 eV/Å;300 K20 ps NVT;100 ps ramp to400 K;20 ps hold;20 ps400 K1 bar NPT;200 ps NVT|[Tang2026](https://doi.org/10.1038/s41467-026-69737-x):independent272-atom packing, not the author's1088-atom geometry or tuned MACE|
|Li₃PS₄|1500 K100 ps NPT;1500→300 K480 ps (2.5 K/ps);300 K20 ps hold;10 ps temperature ramp +50 ps NPT1 bar +200 ps NVT at each target;0.5 fs|[Chen2025](https://doi.org/10.1038/s41467-025-56322-x):thermal schedule reference; NEP replaces DeePMD; start, coupling and production schedule differ|
|LiPON|2000 K10 ps;2000→250 K7 ps;250 K20 ps;250 K1 bar20 ps release;0.5 fs|[Seth2025](https://doi.org/10.1021/acsmaterialsau.4c00117):selected parameters only; NEP replaces NequIP, independent precursor|
|Legacy LZOC|Earlier candidate3;600/700/800/900 K;600 K50 ps NPT+200 ps NVT|Exploratory workflow; not retrospectively labelled a literature reproduction|

NPT target1 bar=0.0001 GPa; project temperature/pressure coupling periods100/1000 fs unless specified. Production thermo/trajectory intervals generally0.05/0.1 ps. New LSZC array uses10 ps400→target NPT,50 ps target NPT,300 ps NVT;320/330/340/350 K follow the paper's temperature grid, while0.5 fs/272 atoms/NEP differ from3 fs/1088 atoms/tuned MACE. Each temperature starts from the same prepared glass, not independent glass replicas.

<a id="methods"></a>
## Definitions and units

For lag time τ, the time-origin-averaged Li MSD is

$$
\mathrm{MSD}(\tau)=\frac{1}{N_{\mathrm{Li}}N_o(\tau)}
\sum_{i,t_0}|\mathbf r_i(t_0+\tau)-\mathbf r_i(t_0)|^2.
$$

N_Li is Li atom count, N_o the valid-origin count and r the unwrapped position after **whole-system mass-weighted COM correction**, not Li-only COM subtraction. For the free-intercept fit MSD=aτ+b,

$$
D_{\mathrm{app}}[\mathrm{cm^2/s}]=\frac{a[\mathrm{\AA^2/ps}]}{6}\times10^{-4},\qquad
\sigma_{\mathrm{NE}}=\frac{(N_{\mathrm{Li}}/V)e^2D}{k_BT}.
$$

V is cell volume, e the Li⁺ elementary charge, k_B the Boltzmann constant and T absolute temperature. Use D in m²/s and V in m³ for SI conductivity: D[cm²/s]×10⁻⁴; V[Å³]×10⁻³⁰. Then σ[mS/cm]=10σ[S/m]=10³σ[S/cm]. NE conversion neglects inter-ion correlations and inherits all apparent-D limitations. Experimental conductivity is not experimental self-D.

Arrhenius fits use lnD=lnD₀−E_a/(k_BT), with k_B=8.617333262145×10⁻⁵ eV/K. The reported E_a diagnostics below are not validated barriers. R² alone does not demonstrate diffusion or convergence; α is the log–log MSD slope and can be affected by a nonzero intercept.

RDFs use periodic minimum-image distances, excluded self-pairs and shell/number-density normalization. CN counts neighbours below declared cutoffs. No smoothing, trajectory rescaling or target-E_a selection is used. Temporal blocks and atom–origin observations are correlated; their SD is not an independent-glass confidence interval.

<a id="lzoc"></a>
## Reconstructed LZOC

### Matched transport and direct AIMD comparison

![LZOC transport and AIMD comparison](../../results/amorphous_review_20260915/overview_figures/01_LZOC_transport.png)

**a–c:** same80 ps starting positions, cell and stored velocities; MTTK0.5 fs uses the first80 ps of the retained200 ps run, NHC2 fs uses80 ps production following a separate2 ps check. Production restarts from the original input, not the check endpoint. Both have100 fs coupling and density2.2340 g/cm³. All three MSD panels share y limits and show0–40 ps lag. **d:** our10–40 ps slopes compared with the author's tracer D* from Supplementary Table4; error bars reproduce its reported ±. Lines guide the eye, not an Arrhenius fit.

|T (K)|AIMD D* (cm²/s), reported ±|NEP NHC2 fs D_app|NEP MTTK0.5 fs D_app|NHC / AIMD D*|
|---:|---:|---:|---:|---:|
|340|(2.09±0.06)×10⁻⁶|3.270×10⁻⁷|1.080×10⁻⁷|0.156|
|360|(1.77±0.04)×10⁻⁶|5.501×10⁻⁷|5.266×10⁻⁷|0.311|
|380|(3.50±0.10)×10⁻⁶|8.957×10⁻⁷|1.705×10⁻⁶|0.256|

[Hussain2024](https://doi.org/10.1038/s41524-024-01346-y) distinguishes tracer D* from charge D; the former matches single-particle MSD. The340→360 K decrease in the published tracer values is retained. The controls differ jointly in thermostat/timestep and use192 rather than48 atoms, so this is neither strict AIMD reproduction nor an isolated potential comparison.

Repeated thermodynamic/RDF diagnostics are reduced to their essential findings: temperature control is maintained, energy still relaxes, and framework motion is nonzero. NHC340 K Cl MSD(40 ps)=0.923 Å² versus0.447 Å² for matched MTTK. A separate380 K NHC0.5 fs check changes D by−4.4/−2.9/+12.1% for5–20/10–30/10–40 ps windows. These are sensitivity results, not an accuracy guarantee.

### Supporting numerical checks

The original MTTK200 ps series is distinct from the matched80 ps comparison. Its20–80 ps slopes and basic statistics are:

|T (K)|D_app (cm²/s)|R²|Mean T (K)|Mean P (GPa)|
|---:|---:|---:|---:|---:|
|340|1.814×10⁻⁷|0.9965|339.761|−0.1860|
|360|1.715×10⁻⁷|0.9657|360.543|−0.1106|
|380|1.028×10⁻⁶|0.9984|380.174|−0.2227|

All cells have imposed density2.2340 g/cm³. The380 K potential energy continues to decrease in its final50 ps block. This table records the earlier results without substituting them into the AIMD comparison.

For the isolated380 K NHC timestep check, the same80 ps duration, starting positions/velocities/cell and100 fs coupling were used:

|MSD window (ps)|D,0.5 fs (cm²/s)|D,2 fs (cm²/s)|Relative change|
|---|---:|---:|---:|
|5–20|1.13169×10⁻⁶|1.18405×10⁻⁶|−4.4%|
|10–30|1.09127×10⁻⁶|1.12433×10⁻⁶|−2.9%|
|10–40|1.00361×10⁻⁶|8.95684×10⁻⁷|+12.1%|

Relative change=(D_0.5fs/D_2fs−1)×100%. Different finite-trajectory realizations and sampling remain relevant; this is not a certified integration-error bound.

### Conditional extrapolation, retained as a table only

|NHC common MSD window (ps)|Apparent E_a (eV)|Arrhenius R²|D300 (cm²/s)|Conditional σ300 (mS/cm)|
|---|---:|---:|---:|---:|
|5–20|0.2196|0.72188|1.706×10⁻⁷|8.90|
|10–30|0.3245|0.99271|7.761×10⁻⁸|4.05|
|10–40|0.2803|0.99982|9.097×10⁻⁸|4.74|

All windows use the same three-temperature NHC series, V=4990.647 Å³ and42Li. The model volume is not independently equilibrated at300 K. [Hu2023](https://doi.org/10.1038/s41467-023-39522-1) reports2.42 mS/cm at298.15 K; Hussain reports a theoretical43.3±3.3 mS/cm at300 K and0.25±0.10 eV. Different temperatures, physical samples, preparation and estimators limit direct comparison. No window is selected for agreement and no validated300 K prediction is claimed. The original 200 ps estimates are listed in the supporting-check table above, separately from the 80 ps estimates.

<a id="lszc"></a>
## LSZC

### Completed400 K pilot

![LSZC transport and relaxation](../../results/amorphous_review_20260915/overview_figures/02_LSZC_transport.png)

**a:** Li MSD and20–80 ps fit; **b:** framework MSD, including substantial Cl motion; **c:** raw PE per atom and5 ps means; **d:** four consecutive50 ps blocks, each fitted at5–20 ps lag. Block estimates and the full-trajectory fit use different windows and are not interchangeable error bars.200 ps production8676040.3 is complete; apparent transport coexists with residual relaxation.

|Quantity|400 K result|
|---|---:|
|D_app,20–80 ps|1.1003×10⁻⁶ cm²/s|
|R² / log–log α|0.99919 /0.748|
|Conditional σ_NE|19.43 mS/cm|
|D over the four specified full-trajectory windows|1.083–1.152×10⁻⁶ cm²/s|
|D across50 ps blocks,5–20 ps fits|0.255–1.941×10⁻⁶ cm²/s|
|Mean T / P|399.71 K /0.03884 GPa|
|Fixed density|1.81705 g/cm³|
|Final-minus-first50 ps mean PE|−0.01070 eV/atom|

The conductivity is conditional NE conversion with32Li and8421.93 Å³, not a validated experimental value. Do not divide400 K conductivity by303 K experiment to claim an accuracy score.

### Coordination and mobility

![LSZC coordination-conditioned mobility](../../results/amorphous_review_20260915/overview_figures/03_LSZC_mobility.png)

Li–O CN is measured at each origin (<2.7 Å), then displacement over10 ps is evaluated; origins are1 ps apart. For CN0/1/2/3, mean |Δr|²=1.693/1.598/1.446/0.979 Å². Open points for CN4/5/6 remain visible but unconnected: only43/9/1 observations support them. The count panel makes this limitation explicit. Common coordination states support a qualitative lower-O/higher-mobility association, not causation. Counts are correlated Li–origin observations, not independent samples; no uncertainty band is invented.

### Structural correspondence, not full agreement

![LSZC structure versus reference distances](../../results/amorphous_review_20260915/overview_figures/04_LSZC_structure.png)

Early0.1–45.1 ps and late150.1–195.1 ps each use10 snapshots,0.05 Å bins, no smoothing. Dotted lines are experimental **EXAFS fitted distances**, not experimental RDF peaks or a total PDF. The Zr–O position discrepancy remains; similar Zr–Cl peak positions alone do not establish reproduction.

|Quantity|NEP400 K production, late|Tang2026 experiment|
|---|---:|---:|
|Zr–O CN (<2.6 Å)|1.553|2.6, EXAFS fit|
|Zr–Cl CN (<3.2 Å)|4.250|3.0, EXAFS fit|
|Density|1.81705 g/cm³, fixed at400 K|2.05 g/cm³, experimental sample|
|Fitted Zr–O / Zr–Cl distances|See model RDF above|2.23 /2.45 Å|

Direct cutoff counts and EXAFS fitted CN differ in definition. All sampled sulfates retain four O neighbours(<2.0 Å). Earlier NPT checks give93.75% of sulfates linked to at least two Zr and2.75 Zr per sulfate; this is local connectivity, not proof of percolation. Modest cutoff changes and20 ps pressure relaxation did not remove the coordination discrepancy.

[Tang2026](https://doi.org/10.1038/s41467-026-69737-x) reports1.5 mS/cm at30 °C and0.33 eV; Figure1 source data instead lists1.4383 mS/cm and0.33052 eV for x=0.5. Keep those source distinctions. The deposited geometry density2.03549 g/cm³ is not the experimental density. Four-temperature production8676216 is submitted; D(T)/E_a comparison and properly weighted total PDF remain pending. Ordinary partial RDF is not substituted for total PDF.

<a id="lps"></a>
## Li₃PS₄

### Four-temperature transport

![Li3PS4 four-temperature MSD](../../results/amorphous_review_20260915/overview_figures/05_LPS_MSD.png)

All four200 ps productions have2,000 saved frames plus their input frame.0–100 ps lag is displayed; dashed fits use20–80 ps with a free intercept. **Different y ranges** expose the300 K plateau; panel heights must not be used to compare amplitudes. At300 K, MSD(80 ps)=0.414 Å² and α=0.049, so the slope is not a converged long-time diffusivity.

|T (K)|D_app (cm²/s)|R²|α|Conditional σ_NE (mS/cm)|
|---:|---:|---:|---:|---:|
|300|7.143×10⁻⁹|0.93452|0.049|0.989|
|500|7.090×10⁻⁷|0.99968|0.660|56.9|
|700|8.079×10⁻⁶|0.99989|0.925|450|
|900|3.615×10⁻⁵|0.99983|0.964|1490|

These are conditional conversions, particularly not a validated300 K conductivity.300 K slopes span7.14×10⁻⁹–4.99×10⁻⁸ cm²/s across windows.

![Li3PS4 reference and framework](../../results/amorphous_review_20260915/overview_figures/06_LPS_reference.png)

**a:** NEP and Chen2025 glass D at the same temperatures; lines are guides, not a forced all-temperature Arrhenius fit. The source workbook's conductivity header conflicts with the official Fig.3a axis ln[D(cm²/s)]; the published axis defines this comparison. Chen's curve is **DeePMD glass MD, not experimental or AIMD D**. **b:** P/S MSD at80 ps lag for every temperature. It rises to5.99/12.50 Å² at900 K; the framework is not immobile.

|T (K)|Chen glass D (cm²/s)|NEP / Chen|
|---:|---:|---:|
|300|1.186×10⁻⁹|6.02|
|500|9.350×10⁻⁸|7.58|
|700|1.524×10⁻⁶|5.30|
|900|9.106×10⁻⁶|3.97|

Different model, preparation and density remain confounders. A500/700/900 K-only diagnostic givesE_a=0.3795 eV,R²=0.99927 versus the paper's0.47 eV annotation; ranges are not matched and this is not extrapolated to300 K. [Mirmira2021](https://doi.org/10.1039/D1TA02754A) provides an experimental-literature anchor of0.35 mS/cm at293.15 K for ball-milled amorphous LPS. This is not a same-temperature comparison to the conditional0.989 mS/cm at300 K.

### Local structure and its limits

![Li3PS4 literature structure](../../results/amorphous_review_20260915/overview_figures/07_LPS_structure.png)

NEP's final10 ps preparation hold is compared with published glass source curves: Li–S RDF peak2.425 Å versus2.459 Å; S–P–S mean109.40°. Angle distributions are independently normalized to unit area (NEP2° bins versus finer source grid). The author's averaging temperature/window is not independently confirmed; local resemblance is not full structural validation.

The preparation graph contains51 P₁S₄,5 P₂S₇ and1 P₃S₁₀ components, plus7 S without a P edge, at P–S2.4/2.6/2.8 Å and P–P2.6 Å; counts conserve64P/256S. These are geometric components, not verified charge/species assignments. At900 K, four-S-coordinated P falls99.38→94.38% between early and late production.

Basic checks remain recorded without another repetitive figure: mean T=300.32/500.65/700.32/899.88 K; mean P=+0.252/−0.120/−0.134/−0.244 GPa; fixed densities2.2270/2.1493/2.0915/1.9886 g/cm³. Fixed NVT density is imposed, not proof of equilibrium.

<a id="lipon"></a>
## LiPON

![LiPON contact diagnosis](../../results/amorphous_review_20260915/overview_figures/08_LiPON_contacts.png)

**a:**250 K pressure release leaves minimum N–N1.270–1.347 Å in all200 samples. Mean P improves to0.00614 GPa and density2.50908 g/cm³, but contact remains. **b:** the same precontact snapshot is tested at2000 K for2 ps with0.5/0.25 fs,100 fs coupling and0.01 ps output. N76–N108 stays below1.6 Å in198/200 samples in both branches. Halving the timestep is not a demonstrated repair. The panels are different stages, not consecutive sections of one time axis.

|Paired2000 K check|0.5 fs|0.25 fs|
|---|---:|---:|
|Minimum N76–N108 (Å)|1.1791|1.1787|
|Final N76–N108 (Å)|1.2327|1.2776|
|Fraction below1.6 Å|99%|99%|
|Mean temperature (K)|2024.48|2004.80|

The1.6 Å line is a screening cutoff, not a universal bond criterion. Late P–O/P–N counts(<2.1 Å)=3.688/0.438;2/5 N atoms have a short N neighbour. Formation was traced to2.2–2.3 ps of the original2000 K hold. A distance does not identify chemical charge/bond order. Retain this limitation case; no DFT or long production is proposed.

<a id="legacy"></a>
## Legacy LZOC: MACE–NEP

### Efficiency and different densities

![Legacy runtime and density](../../results/amorphous_review_20260915/overview_figures/09_legacy_cost_density.png)

**a:** actual job runtimes, excluding queue time, use a logarithmic y axis so both workflows remain visible. **b:**600 K NPT density uses the same y axis for both models; dotted line is the common300 K input, not experiment. NEP is faster and expands less in this workflow, but these facts alone do not establish experimental accuracy.

|600 K quantity|MACE / LAMMPS|NEP89 / GPUMD|
|---|---:|---:|
|200 ps engine-reported production time|189.93 min|6.11 min|
|Production density|1.468304 g/cm³|1.875429 g/cm³|
|Volume increase from300 K input|30.3%|2.0%|
|D_app,20–80 ps|1.7197×10⁻⁵ cm²/s|1.0757×10⁻⁵ cm²/s|

Engine time ratio31.10; sum of four whole-job runtimes18 h25 min versus34 min. These are not parallel elapsed times or a controlled potential-kernel benchmark: engine, node, preprocessing, seed, density and structure differ.

### Complete runtime table

|Temperature (K)|MACE whole-job time (min)|NEP whole-job time (min)|
|---:|---:|---:|
|600|247.17|9.07|
|700|300.33|8.37|
|800|241.42|8.36|
|900|316.25|8.29|

Whole-job time includes setup/equilibration and is different from the600 K production-only189.93/6.11 min above. Both workflows requested one GPU; they are not hardware-identical kernel measurements. NEP was selected for economical exploratory throughput, not because lower expansion proves correctness.

### Archived high-temperature motion

![Legacy model motion](../../results/amorphous_review_20260915/overview_figures/10_legacy_motion.png)

**a–c:** time-origin-averaged Li MSD, common y limits,700/800/900 K existing200 ps productions. **d:**900 K framework curves; color identifies species and line style identifies model. All700/800 K framework source curves remain available. Substantial host movement precludes interpreting this solely as Li diffusion in a static host.

|T (K)|MACE D (cm²/s)|NEP D (cm²/s)|MACE / NEP density (g/cm³)|
|---:|---:|---:|---:|
|700|3.429×10⁻⁵|1.686×10⁻⁵|1.14742 /1.78576|
|800|5.353×10⁻⁵|3.615×10⁻⁵|1.27278 /1.66334|
|900|6.257×10⁻⁵|5.267×10⁻⁵|0.92513 /1.53955|

All D fits use20–80 ps. Mean temperatures are within1.1 K of target; final-minus-first50 ps PE changes are−0.00385/−0.00059/−0.00015 eV/atom for MACE and−0.00976/−0.01075/−0.00922 for NEP. Retain relaxation/density differences as limitations.

![Legacy representative RDF](../../results/amorphous_review_20260915/overview_figures/11_legacy_structure.png)

The former12-panel grid is replaced by a readable900 K representative four-pair view:21 snapshots over150–200 ps,0.05 Å bins, no smoothing. All700/800 K numerical RDFs are retained as source data. Similar peak positions can coexist with large framework motion. This is not experimental or AIMD RDF. Separate NPT-extension analysis is still pending.

<a id="remaining"></a>
## Remaining work and source record

|Item|Remaining work|
|---|---|
|LSZC320/330/340/350 K|Retrieve/check array8676216 outputs, then compare D(T),conditional σ andE_a; no completed result claimed here|
|Experimental total PDF / structure factor|Match temperature and scattering weights; ordinary partial RDF is insufficient|
|Legacy extra NPT runs|Separate analysis; not represented by production plots|
|New LZOC / Li₃PS₄|Current paper-facing comparisons are available, with non-convergence/preparation limits explicitly retained|
|LiPON|Limitation case; no demonstrated repair from pressure release or timestep halving|
|Independent-glass uncertainty|Not established; temperature branches and time blocks are not independent glasses|

**Figure policy:**43→11 core groups. Repeated raw-temperature/pressure grids, near-duplicate RDFs, flat CN traces and redundant fit diagnostics are removed from the master display, not from source data. Replaced exports unique to the previous supplement are deleted; historical images still referenced by older reports remain archived. Git history can restore removed exports. No CSV, trajectory, fit or adverse finding is deleted.

Images use PNG/PDF/SVG with editable text, at most two columns and consistent document-width typography. Raw trajectories remain local/on TSUBAME, outside this commit. The≤100-point alert remains a separate monitor, not a live balance in this report.

## Optional source archive

The report above contains the interpretation and required numerical comparisons. The links below are only for checking original arrays or rerunning the analysis.

<details>
<summary>Source data and reproducibility files</summary>

- [Source hashes and figure inventory](../../results/amorphous_review_20260915/overview_figures/provenance.json)
- [Replot script](../../scripts/structures/curate_overview_figures.py)
- [LZOC and reference source tables](../../results/amorphous_review_20260915/final_comparisons)
- [LSZC400 K and legacy high-temperature source tables](../../results/amorphous_review_20260915/paper_alignment)
- [Li₃PS₄ transport source tables](../../results/amorphous_review_20260915/Li3PS4_transport)
- [LiPON and additional diagnostic source tables](../../results/amorphous_review_20260915/portfolio_supplement)

</details>
