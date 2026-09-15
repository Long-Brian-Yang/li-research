# Material Review — Amorphous Solid Electrolytes

Updated 15 September 2026. [日本語](materials_overview_ja.md)

This is the complete English Material Review. Read the methods, figures, numerical tables and interpretation here in sequence; opening another report is not required. Source files and scripts are optional audit material collected at the end. Thirteen core figure groups summarize the material comparisons. Redundant diagnostics are summarized directly in tables; unfavourable results are retained. This update adds analysis of completed trajectories without changing simulation inputs or trajectories.

## How this review is maintained

All subsequent results are inserted, revised or replaced directly in the relevant material section of this review, with the Japanese version updated in parallel. Each section follows the paper's question and reference results, our corresponding calculation, numerical comparison, structural interpretation and conclusion. Figures, numerical tables, necessary equations and symbol definitions, settings, limitations and next steps belong in the body—not behind links to separate reports. Source files and DOI links are optional provenance only. Superseded results are clearly identified rather than silently mixed with current results; pending analyses remain labelled pending. Separate progress reports are not created unless explicitly requested.

## Contents

- [Status and preparation](#status)
- [Definitions and units](#methods)
- [Reconstructed LZOC](#lzoc)
- [LSZC](#lszc)
- [Li₃PS₄](#lps)
- [LiPON](#lipon)
- [Legacy LZOC: MACE–NEP](#legacy)
- [Completed work and remaining limitations](#remaining)

<a id="status"></a>
## Status and preparation

Four chemical systems, five preparation routes. New and legacy LZOC have the same nominal composition; LZOC/LSZC are the oxyhalide main line, Li₃PS₄ a method control and LiPON a limitation case. Cancelled Zhou2024 work is not counted as executed. Crystalline Li₃YCl₆/LiNbOCl₄ work is unchanged.

|Route|Model size|Completed / submitted|Interpretation|
|---|---|---|---|
|New LZOC|192: Li42Zr24Cl114O12|340/360/380 K, 80 ps, NHC 2 fs primary comparison analysed|Direct AIMD table comparison available; long-time convergence not established|
|LSZC|272: Li32Zr32Cl128S16O64|400 K pilot and 320/330/340/350 K, 300 ps array8676216 analysed|Sulfate retained, but Zr environment/density and the temperature trend differ from reference|
|Li₃PS₄|512: Li192P64S256|300/500/700/900 K200 ps production analysed, array8675738|Transport differs from reference;300 K plateau and900 K host motion remain|
|LiPON|124: Li47P16O56N5|Preparation,pressure release and paired0.5/0.25 fs checks analysed|Short N–N contacts persist; no long transport prediction|
|Legacy LZOC|192, same nominal LZOC|600 K detailed comparison,700–900 K MSD/RDF andfour-temperature timing analysed|Efficiency and structural sensitivity, not an accuracy ranking|

Completed job status and completed analysis are distinguished throughout. The four LSZC productions and legacy NPT extensions are now analysed; no new MD or DFT was submitted here.

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

For the LSZC conductivity comparison, x=1000/T and y=ln[σT/(S cm⁻¹ K)]; if y=mx+b is justified, E_a=−1000k_Bm. This is a fit to σT, not σ alone. Different temperature-dependent number densities can make its slope differ from a fit to D. A poor or nonphysical regression is retained only as a diagnostic, without a predicted room-temperature value.

RDFs use periodic minimum-image distances, excluded self-pairs and shell/number-density normalization. CN counts neighbours below declared cutoffs. No smoothing, trajectory rescaling or target-E_a selection is used. Temporal blocks and atom–origin observations are correlated; their SD is not an independent-glass confidence interval.

<a id="lzoc"></a>
## Reconstructed LZOC

### Paper question and 2 fs transport comparison

[Hussain et al. (2024)](https://doi.org/10.1038/s41524-024-01346-y) investigates whether LiCl-deficient amorphous LZOC supports fast Li transport. Our comparison now uses only the completed NEP NVT Nosé–Hoover-chain **2 fs, 80 ps, 340/360/380 K** series. The coupling period is our 100 fs setting; 192 atoms, the reconstructed starting structure and NEP are not the paper's 48-atom AIMD setup. A separate 2 ps execution check preceded production, which restarted from the original input rather than the check endpoint. Density is 2.2340 g/cm³. Earlier 0.5 fs tests remain archived and are not a competing primary series.

![LZOC transport and AIMD comparison](../../results/plots/amorphous/01_LZOC_transport.png)

Only the 2 fs, 80 ps production series is plotted at 340/360/380 K. Superseded 0.5 fs and timestep-comparison figure exports have been removed; raw data remain archived.

**a–c:** all-time-origin Li MSD at the three temperatures, common y scale and 0–40 ps lag. **d:** 10–40 ps slope estimates against the paper's tracer D* in Supplementary Table 4. Reported ± values are reproduced as given, not reinterpreted as replica confidence intervals. Lines guide the eye.

|T (K)|AIMD D* (cm²/s), reported ±|NEP 2 fs D_app (cm²/s)|NEP / AIMD|
|---:|---:|---:|---:|
|340|(2.09±0.06)×10⁻⁶|3.270×10⁻⁷|0.156|
|360|(1.77±0.04)×10⁻⁶|5.501×10⁻⁷|0.311|
|380|(3.50±0.10)×10⁻⁶|8.957×10⁻⁷|0.256|

NEP gives approximately 69–84% lower tracer-diffusion estimates than the source table. The published 340→360 K decrease is retained rather than replaced by points on a fitted line. Thus the current result captures increasing NEP mobility with temperature but does not quantitatively reproduce the AIMD values. Tracer D* and charge D are different observables.

The paper discusses localized Cl motion; a nonzero Cl MSD alone is not evidence of long-range anion diffusion. Our NHC 340 K Cl MSD at 40 ps is 0.923 Å². Energy relaxation and framework motion remain relevant, so we do not attribute all differences solely to the potential or claim long-time convergence.

### Conditional extrapolation from the same 2 fs series

|MSD window (ps)|Diagnostic E_a (eV)|R²|D(300 K) (cm²/s)|σ_NE(300 K) (mS/cm)|
|---|---:|---:|---:|---:|
|5–20|0.2196|0.72188|1.706×10⁻⁷|8.90|
|10–30|0.3245|0.99271|7.761×10⁻⁸|4.05|
|10–40 — primary comparison|0.2803|0.99982|9.097×10⁻⁸|4.74|

These archived fit values are diagnostic, not a validated room-temperature prediction; the primary slope window is unchanged. The common volume is 4990.647 Å³ with 42 Li, not a separately equilibrated 300 K volume. [Hu et al. (2023)](https://doi.org/10.1038/s41467-023-39522-1) reports 2.42 mS/cm at 298.15 K; Hussain reports a theoretical 43.3±3.3 mS/cm at 300 K and 0.25±0.10 eV. Physical sample, temperature, preparation and transport estimators differ. Agreement of one extrapolation is weaker evidence than the direct temperature-resolved comparison above.

<a id="lszc"></a>
## LSZC

### Four-temperature transport and the paper comparison

**Completed analysis:** all four tasks 8676216.1–4 completed 300 ps production. Downloaded trajectories were checked for 272 atoms, unchanged element order, a fixed cell, 3000 frames at 0.1 ps, and finite thermo records. FFT MSD was checked against direct displacement averages. The primary 20–80 ps fit was fixed before inspecting the results, matching the existing 400 K analysis; no temperature or replica was replaced.

![LSZC four temperatures versus published MSD](../../results/plots/amorphous/12_LSZC_4T_MSD.png)

The shaded interval is the primary fitting interval; all panels share axes. NEP uses centre-of-mass-corrected, all-time-origin MSD from the full 300 ps production. The dashed curves are Tang's published Supplementary Fig. 24 source arrays, shown over the same 0–100 ps interval. Their exact time-origin averaging convention is not established, so the overlay is not a strictly identical estimator comparison. The workbook labels its first column “MSD”, but the published axes and array ranges identify it as time in ps and the second as MSD in Å²; the extraction follows the published figure, not the reversed headers.

|T (K)|NEP D_app (cm²/s)|NEP σ_app (mS/cm)|Tang tuned-MACE σ (mS/cm)|NEP / reference|MSD exponent α|
|---:|---:|---:|---:|---:|---:|
|320|1.408×10⁻⁷|3.183|2.987|1.066|0.303|
|330|4.003×10⁻⁷|8.855|4.086|2.167|0.572|
|340|2.661×10⁻⁷|5.561|6.624|0.839|0.447|
|350|1.043×10⁻⁷|2.215|8.246|0.269|0.260|

Here α is the log–log MSD slope over the same 20–80 ps interval. The ordinary linear-fit R² values are 0.9908/0.9965/0.9990/0.9921, but high R² does not establish asymptotic diffusion when the MSD includes a large localized-motion offset. Conductivities are conditional Nernst–Einstein conversions using each cell volume; they are not independent conductivity measurements or converged long-time transport coefficients. Fit-window D ranges are 1.408–3.258, 3.763–5.391, 2.632–3.807 and 1.043–1.588 ×10⁻⁷ cm²/s, respectively. These ranges describe estimator sensitivity, not independent-glass confidence intervals.

![LSZC conductivity and Arrhenius comparison](../../results/plots/amorphous/13_LSZC_literature_transport.png)

**a:** direct temperature-resolved values; lines guide the eye. Tang Fig. 3g is tuned-MACE MD, not AIMD or experiment. The separate open square near 300 K is the author's 3 ns result and is not combined with the four 300 ps points. The published inverse temperatures are rounded (3.125, 3.030, 2.941, 2.857); conversions use T=1000/x rather than silently replacing the source coordinates. **b:** NEP points are displayed without an Arrhenius regression line. Source error bars are the workbook's stated y-errors in ln(σT), transformed exponentially in panel a; their statistical definition was not independently established.

The conversion is y=ln[σT/(S cm⁻¹ K)], hence σ(mS/cm)=1000 exp(y)/T. The experimental Supplementary Fig. 3 source coordinates give:

|T from published 1000/T (K, rounded here)|Experimental σ (mS/cm)|
|---:|---:|
|303.000|1.490|
|313.000|2.123|
|323.000|3.015|
|333.000|4.246|
|343.000|5.807|
|353.000|7.522|

These are source-coordinate conversions, not six new measurements by us. The paper labels measurements 30–80 °C, whereas its source x values correspond to 303–353 K; keep this 0.15 K convention difference explicit. The headline 1.5 mS/cm at 30 °C and Figure 1 source value 1.4383 mS/cm are retained as distinct reported values, not silently reconciled.

**Conclusion:** a near match at 320 K does not establish reproduction: the NEP temperature trend is nonmonotonic and does not follow either reference series. A forced ln(σT) fit gives a diagnostic slope corresponding to −0.1097 eV with R²=0.0600 (ln D: −0.1148 eV, R²=0.0637). This is not a reportable physical activation energy; no NEP room-temperature extrapolation is reported. Refitting the four published MD ln(σT) points yields 0.3696 eV, R²=0.9863, and the six experimental points 0.3302 eV, R²=0.9997; these are our regressions of source points, not new author-reported values.

Basic checks support completed execution, not full equilibration: mean T=319.73/329.87/339.81/349.64 K and P=−0.00070/+0.04764/+0.02975/+0.10571 GPa. Density is 1.8603/1.8773/1.8274/1.9112 g/cm³ versus the experimental reference 2.05. First-to-last-quarter PE changes are −3.413/−6.567/−8.568/+0.958 meV/atom. All sampled late S sites retain four O neighbours (ten frames per temperature, cutoff 2.0 Å), while mean Zr–O coordination is only 1.456–1.563 and Zr–Cl is 4.256–4.366. Preserving sulfate alone therefore does not reproduce the full Zr environment or transport. Preparation, finite sampling, cell density and potential applicability are plausible contributors; these results do not isolate their causal effects.

### Completed400 K pilot

![LSZC transport and relaxation](../../results/plots/amorphous/02_LSZC_transport.png)

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

![LSZC coordination-conditioned mobility](../../results/plots/amorphous/03_LSZC_mobility.png)

Li–O CN is measured at each origin (<2.7 Å), then displacement over10 ps is evaluated; origins are1 ps apart. For CN0/1/2/3, mean |Δr|²=1.693/1.598/1.446/0.979 Å². Open points for CN4/5/6 remain visible but unconnected: only43/9/1 observations support them. The count panel makes this limitation explicit. Common coordination states support a qualitative lower-O/higher-mobility association, not causation. Counts are correlated Li–origin observations, not independent samples; no uncertainty band is invented.

### Structural correspondence, not full agreement

![LSZC structure versus reference distances](../../results/plots/amorphous/04_LSZC_structure.png)

Early0.1–45.1 ps and late150.1–195.1 ps each use10 snapshots,0.05 Å bins, no smoothing. Dotted lines are experimental **EXAFS fitted distances**, not experimental RDF peaks or a total PDF. The Zr–O position discrepancy remains; similar Zr–Cl peak positions alone do not establish reproduction.

|Quantity|NEP400 K production, late|Tang2026 experiment|
|---|---:|---:|
|Zr–O CN (<2.6 Å)|1.553|2.6, EXAFS fit|
|Zr–Cl CN (<3.2 Å)|4.250|3.0, EXAFS fit|
|Density|1.81705 g/cm³, fixed at400 K|2.05 g/cm³, experimental sample|
|Fitted Zr–O / Zr–Cl distances|See model RDF above|2.23 /2.45 Å|

Direct cutoff counts and EXAFS fitted CN differ in definition. All sampled sulfates retain four O neighbours(<2.0 Å). Earlier NPT checks give93.75% of sulfates linked to at least two Zr and2.75 Zr per sulfate; this is local connectivity, not proof of percolation. Modest cutoff changes and20 ps pressure relaxation did not remove the coordination discrepancy.

[Tang2026](https://doi.org/10.1038/s41467-026-69737-x) reports1.5 mS/cm at30 °C and0.33 eV; Figure1 source data instead lists1.4383 mS/cm and0.33052 eV for x=0.5. Keep those source distinctions. The deposited geometry density2.03549 g/cm³ is not the experimental density. Four-temperature transport and its unsuccessful Arrhenius trend are analysed above; correctly weighted total PDF remains outside this completed analysis. Ordinary partial RDF is not substituted for total PDF.

<a id="lps"></a>
## Li₃PS₄

### Four-temperature transport

![Li3PS4 four-temperature MSD](../../results/plots/amorphous/05_LPS_MSD.png)

All four200 ps productions have2,000 saved frames plus their input frame.0–100 ps lag is displayed; dashed fits use20–80 ps with a free intercept. **Different y ranges** expose the300 K plateau; panel heights must not be used to compare amplitudes. At300 K, MSD(80 ps)=0.414 Å² and α=0.049, so the slope is not a converged long-time diffusivity.

|T (K)|D_app (cm²/s)|R²|α|Conditional σ_NE (mS/cm)|
|---:|---:|---:|---:|---:|
|300|7.143×10⁻⁹|0.93452|0.049|0.989|
|500|7.090×10⁻⁷|0.99968|0.660|56.9|
|700|8.079×10⁻⁶|0.99989|0.925|450|
|900|3.615×10⁻⁵|0.99983|0.964|1490|

These are conditional conversions, particularly not a validated300 K conductivity.300 K slopes span7.14×10⁻⁹–4.99×10⁻⁸ cm²/s across windows.

![Li3PS4 reference and framework](../../results/plots/amorphous/06_LPS_reference.png)

**a:** NEP and Chen2025 glass D at the same temperatures; lines are guides, not a forced all-temperature Arrhenius fit. The source workbook's conductivity header conflicts with the official Fig.3a axis ln[D(cm²/s)]; the published axis defines this comparison. Chen's curve is **DeePMD glass MD, not experimental or AIMD D**. **b:** P/S MSD at80 ps lag for every temperature. It rises to5.99/12.50 Å² at900 K; the framework is not immobile.

|T (K)|Chen glass D (cm²/s)|NEP / Chen|
|---:|---:|---:|
|300|1.186×10⁻⁹|6.02|
|500|9.350×10⁻⁸|7.58|
|700|1.524×10⁻⁶|5.30|
|900|9.106×10⁻⁶|3.97|

Different model, preparation and density remain confounders. A500/700/900 K-only diagnostic givesE_a=0.3795 eV,R²=0.99927 versus the paper's0.47 eV annotation; ranges are not matched and this is not extrapolated to300 K. [Mirmira2021](https://doi.org/10.1039/D1TA02754A) provides an experimental-literature anchor of0.35 mS/cm at293.15 K for ball-milled amorphous LPS. This is not a same-temperature comparison to the conditional0.989 mS/cm at300 K.

### Local structure and its limits

![Li3PS4 literature structure](../../results/plots/amorphous/07_LPS_structure.png)

NEP's final10 ps preparation hold is compared with published glass source curves: Li–S RDF peak2.425 Å versus2.459 Å; S–P–S mean109.40°. Angle distributions are independently normalized to unit area (NEP2° bins versus finer source grid). The author's averaging temperature/window is not independently confirmed; local resemblance is not full structural validation.

The preparation graph contains51 P₁S₄,5 P₂S₇ and1 P₃S₁₀ components, plus7 S without a P edge, at P–S2.4/2.6/2.8 Å and P–P2.6 Å; counts conserve64P/256S. These are geometric components, not verified charge/species assignments. At900 K, four-S-coordinated P falls99.38→94.38% between early and late production.

**Paper-facing interpretation:** short-range Li–S distances and tetrahedral angles resemble the glass reference, but NEP D is 3.97–7.58 times the published DeePMD values and the network differs. This supports partial local-structure transfer, not quantitative transport reproduction. The P/S motion at 900 K is a further confounder, not evidence for a proven migration mechanism. No fitted room-temperature extrapolation is added.

Basic checks remain recorded without another repetitive figure: mean T=300.32/500.65/700.32/899.88 K; mean P=+0.252/−0.120/−0.134/−0.244 GPa; fixed densities2.2270/2.1493/2.0915/1.9886 g/cm³. Fixed NVT density is imposed, not proof of equilibrium.

<a id="lipon"></a>
## LiPON

![LiPON contact diagnosis](../../results/plots/amorphous/08_LiPON_contacts.png)

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

![Legacy runtime and density](../../results/plots/amorphous/09_legacy_cost_density.png)

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

![Legacy model motion](../../results/plots/amorphous/10_legacy_motion.png)

**a–c:** time-origin-averaged Li MSD, common y limits,700/800/900 K existing200 ps productions. **d:**900 K framework curves; color identifies species and line style identifies model. All700/800 K framework source curves remain available. Substantial host movement precludes interpreting this solely as Li diffusion in a static host.

|T (K)|MACE D (cm²/s)|NEP D (cm²/s)|MACE / NEP density (g/cm³)|
|---:|---:|---:|---:|
|700|3.429×10⁻⁵|1.686×10⁻⁵|1.14742 /1.78576|
|800|5.353×10⁻⁵|3.615×10⁻⁵|1.27278 /1.66334|
|900|6.257×10⁻⁵|5.267×10⁻⁵|0.92513 /1.53955|

All D fits use20–80 ps. Mean temperatures are within1.1 K of target; final-minus-first50 ps PE changes are−0.00385/−0.00059/−0.00015 eV/atom for MACE and−0.00976/−0.01075/−0.00922 for NEP. Retain relaxation/density differences as limitations.

![Legacy representative RDF](../../results/plots/amorphous/11_legacy_structure.png)

The former12-panel grid is replaced by a readable900 K representative four-pair view:21 snapshots over150–200 ps,0.05 Å bins, no smoothing. All700/800 K numerical RDFs are retained as source data. Similar peak positions can coexist with large framework motion. This is not experimental or AIMD RDF. The separately analysed NPT extensions are summarized below.

### Completed 50 ps NPT extensions

The existing NEP 700/800/900 K extensions (8665996/8665995/8665994) have now been analysed separately from production. Each contains 1000 finite thermo records at 0.05 ps. No additional run was submitted.

|T (K)|Start → final density (g/cm³)|First → last 10 ps mean density|Endpoint volume change|Mean P (GPa)|PE last−first 10 ps (meV/atom)|
|---:|---|---|---:|---:|---:|
|700|1.7858 → 1.4642|1.8034 → 1.5366|+21.96%|+0.00017|−6.235|
|800|1.6633 → 1.6285|1.6191 → 1.5331|+2.14%|+0.00277|−4.406|
|900|1.5396 → 1.0914|1.3569 → 1.1245|+41.06%|+0.00266|−6.237|

Average pressure near the target does not establish structural equilibration. Endpoint and block-average densities are both given because instantaneous NPT volumes fluctuate, especially at 800 K. Continued expansion and decreasing PE at 700/900 K weaken the interpretation of the earlier high-temperature results as a stable, fixed host. This supports retaining the route as a model-sensitivity and efficiency comparison, not using it to validate room-temperature conductivity. No further blind extension is planned.

<a id="remaining"></a>
## Completed work and remaining limitations

|Material / item|Current result|Further calculation|
|---|---|---|
|LSZC|Four temperatures analysed and compared with published tuned-MACE and experimental series; no valid NEP E_a extracted|Not automatically repeated. Longer sampling would be a separate follow-up if a converged transport claim is required.|
|New LZOC|2 fs primary figure/table and direct AIMD D* comparison updated|No further timestep comparison.|
|Li₃PS₄|Existing transport and local-structure results interpreted against the paper; partial structural agreement does not imply transport reproduction|No new production for the present exploratory comparison.|
|LiPON|Contact checks complete; persistent N–N mismatch reported as a limitation|No blind extension or DFT.|
|Legacy LZOC|Extra NPT analysis complete, alongside high-temperature structure/motion and runtime comparisons|No additional run.|
|Weighted total PDF / structure factor|Not performed; partial RDF is not experimental total PDF|Optional separate scattering analysis requiring matched definitions and reference conditions, not a mandatory MD rerun.|
|Independent-glass uncertainty|Not assessed; one prepared glass and temperature branches|Not claimed as replica statistics.|

The completed scope is a paper-facing pretrained-potential comparison, not a claim that every material reproduces experiment or AIMD. No new MD was submitted in this update. Remaining physical limitations are retained as results rather than “fixed” by selecting favourable trajectories.

**Figure policy:**13 core groups, including the two new LSZC paper comparisons. Repeated raw-temperature/pressure grids, near-duplicate RDFs, flat CN traces and redundant fit diagnostics are removed from the master display, not from source data. Replaced exports unique to the previous supplement are deleted; historical images still referenced by older reports remain archived. Git history can restore removed exports. No CSV, trajectory, fit or adverse finding is deleted.

Images use PNG/PDF/SVG with editable text, at most two columns and consistent document-width typography. Raw trajectories remain local/on TSUBAME, outside this commit. The≤100-point alert remains a separate monitor, not a live balance in this report.

## Optional source archive

The report above contains the interpretation and required numerical comparisons. The links below are only for checking original arrays or rerunning the analysis.

<details>
<summary>Source data and reproducibility files</summary>

- [Source hashes and figure inventory](../../results/plots/amorphous/provenance.json)
- [Replot script](../../scripts/structures/curate_overview_figures.py)
- [New four-temperature and NPT source tables](../../results/amorphous_review_20260915/completed_transport)

- [LZOC and reference source tables](../../results/amorphous_review_20260915/final_comparisons)
- [LSZC400 K and legacy high-temperature source tables](../../results/amorphous_review_20260915/paper_alignment)
- [Li₃PS₄ transport source tables](../../results/amorphous_review_20260915/Li3PS4_transport)
- [LiPON and additional diagnostic source tables](../../results/amorphous_review_20260915/portfolio_supplement)

</details>
