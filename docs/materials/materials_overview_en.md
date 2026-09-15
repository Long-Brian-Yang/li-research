# Material Review — Amorphous Solid Electrolytes

Updated 15 September 2026. [日本語](materials_overview_ja.md)

This Material Review follows one argument: the measured efficiency of NEP89 makes multi-material exploration feasible, while its agreement with literature must be assessed separately for structure and transport. Each material is introduced through its reference question, compared numerically, interpreted physically and closed with a bounded conclusion. Fifteen figure groups and the essential numerical tables are embedded below; no separate report is needed. This revision expands the discussion and organizes existing figures without changing data or simulations.

## How this review is maintained

The narrative omits scheduler IDs, velocity seed numbers and filesystem paths. These remain in source provenance. Plot legends identify materials, temperatures and models; fitting and selection details are stated once in the relevant methods paragraph, not repeated in each caption.

**Plotting convention:** For subsequent figures and revisions in this project, use the corresponding GPUMDkit plotting script as the primary reference, including MSD, RDF, Arrhenius and thermodynamic plots where supported. Inspect the actual script before adapting it; preserve readable report-wide fonts, units and model identities. Distinguish plotting conventions from calculation definitions: do not silently change averaging, normalization, fitting windows or source trajectories to match an example. Document any such methodological change. When GPUMDkit has no matching plot, state the adaptation rather than claiming it is a GPUMDkit output. This convention applies to future plotting; it does not mean all existing figures have already been redrawn.

All subsequent results are inserted, revised or replaced directly in the relevant material section of this review, with the Japanese version updated in parallel. Each section follows the paper's question and reference results, our corresponding calculation, numerical comparison, structural interpretation and conclusion. Figures, numerical tables, necessary equations and symbol definitions, settings, limitations and next steps belong in the body—not behind links to separate reports. Source files and DOI links are optional provenance only. Superseded results are clearly identified rather than silently mixed with current results; pending analyses remain labelled pending. Separate progress reports are not created unless explicitly requested.

**Figure location:** all active review images and their vector exports are in `docs/materials/figures/`, referenced here as `figures/...`. Future revisions replace the corresponding asset there and update both language versions together. Historical source exports are retained only for older reports.

## Contents

- [1. MACE versus NEP: why NEP was selected](#legacy)
- [2. LZOC: the primary AIMD comparison](#lzoc)
- [3. LSZC: extending the comparison to experiment](#lszc)
- [4. Li₃PS₄: a sulfide transferability comparison](#lps)
- [5. LiPON: limits of applicability](#lipon)
- [6. Synthesis: reproduction, deviations and next steps](#remaining)
- [Supporting methods: preparation and conditions](#status)
- [Supporting methods: definitions and units](#methods)

<a id="legacy"></a>
## 1. MACE versus NEP: why NEP was selected

The first question is practical: which workflow allows us to investigate several amorphous electrolytes within the available computing budget? The existing candidate-3 LZOC calculations provide the starting comparison. We select NEP89/GPUMD for its observed throughput, not as a claim that NEP is intrinsically more accurate than MACE. The subsequent material sections test how far that economical choice reproduces published structure and transport results.

### Background: separating computational cost from predictive accuracy

This comparison establishes the method choice before the material comparisons begin. The old LZOC structure provides a shared chemical starting point, but its high-temperature results are not a reference truth: a potential can run quickly and maintain a finite trajectory while still predicting a different density or local environment. Runtime and physical response must therefore be read as two separate outcomes.

For the present study, the practical benefit of the faster workflow is the ability to examine several materials and temperature conditions. Whether that workflow remains useful scientifically is then decided by the literature comparisons below. This is an assessment of the implemented MACE/LAMMPS and NEP89/GPUMD workflows, not a general ranking of the two potential families.

### Construction and comparison design

The legacy comparison starts from the previously prepared 192-atom candidate 3, not from the Hussain reconstruction used in the next section. Candidate 3 is the working structure selected for continued testing; its selection does not establish that it is the most stable possible glass. MACE and NEP are evaluated at the same nominal composition and temperature, but each potential produces its own subsequent structural and density evolution. The 600 K comparison includes 50 ps NPT followed by 200 ps NVT production.

This is a **workflow-level NNP comparison**, not a same-configuration force-error benchmark. Runtime measures practical cost; density, species-resolved MSD and RDF measure the resulting material response. Because the simulation engines and resulting densities differ, a difference in D cannot be assigned solely to the potential's migration barrier. Neither potential was retrained here against the reference data. NEP is carried forward for its measured computational advantage, while its predictive performance is assessed separately below.

![Legacy runtime and density](figures/09_legacy_cost_density.png)

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

![Legacy model motion](figures/10_legacy_motion.png)

**a–c:** time-origin-averaged Li MSD, common y limits,700/800/900 K existing200 ps productions. **d:**900 K framework curves; color identifies species and line style identifies model. All700/800 K framework source curves remain available. Substantial host movement precludes interpreting this solely as Li diffusion in a static host.

|T (K)|MACE D (cm²/s)|NEP D (cm²/s)|MACE / NEP density (g/cm³)|
|---:|---:|---:|---:|
|700|3.429×10⁻⁵|1.686×10⁻⁵|1.14742 /1.78576|
|800|5.353×10⁻⁵|3.615×10⁻⁵|1.27278 /1.66334|
|900|6.257×10⁻⁵|5.267×10⁻⁵|0.92513 /1.53955|

All D fits use20–80 ps. Mean temperatures are within1.1 K of target; final-minus-first50 ps PE changes are−0.00385/−0.00059/−0.00015 eV/atom for MACE and−0.00976/−0.01075/−0.00922 for NEP. Retain relaxation/density differences as limitations.

![Legacy representative RDF](figures/11_legacy_structure.png)

The 900 K four-pair view follows [GPUMDkit's RDF plotting method](https://github.com/zhyan0603/GPUMDkit/blob/main/Scripts/plt_scripts/plt_rdf.py): direct lines, one pair per panel, without interpolation or smoothing filters. We retain a 2×2 layout and report-matched fonts for readability. RDFs now average all 501 saved frames over the same 150–200 ps interval (0.1 ps spacing), instead of 21 sparse frames; 0.05 Å bins, spherical-shell normalization and the original trajectories are unchanged. This changes the sampling average, not merely styling. Correlated frames are not independent replicas; denser sampling does not guarantee elimination of noise. Original sparse CSVs and all 700/800 K RDFs remain archived. Similar peak positions can coexist with large framework motion. This is not experimental or AIMD RDF. The separately analysed NPT extensions are summarized below.

### Completed 50 ps NPT extensions

The existing NEP 700/800/900 K extensions have now been analysed separately from production. Each contains 1000 finite thermo records at 0.05 ps. No additional run was submitted.

|T (K)|Start → final density (g/cm³)|First → last 10 ps mean density|Endpoint volume change|Mean P (GPa)|PE last−first 10 ps (meV/atom)|
|---:|---|---|---:|---:|---:|
|700|1.7858 → 1.4642|1.8034 → 1.5366|+21.96%|+0.00017|−6.235|
|800|1.6633 → 1.6285|1.6191 → 1.5331|+2.14%|+0.00277|−4.406|
|900|1.5396 → 1.0914|1.3569 → 1.1245|+41.06%|+0.00266|−6.237|

Average pressure near the target does not establish structural equilibration. Endpoint and block-average densities are both given because instantaneous NPT volumes fluctuate, especially at 800 K. Continued expansion and decreasing PE at 700/900 K weaken the interpretation of the earlier high-temperature results as a stable, fixed host. This supports retaining the route as a model-sensitivity and efficiency comparison, not using it to validate room-temperature conductivity. No further blind extension is planned.

### Physical interpretation and conclusion

Expansion changes both the number density used in the Nernst–Einstein conversion and the environment through which Li moves. Consequently, different D values after NPT cannot be assigned exclusively to a difference in the migration barrier of the two potentials. The accompanying framework MSD also matters: transport through a rearranging host is not the same physical regime as Li migration through an approximately stationary framework.

**Method-choice conclusion:** the measured cost advantage justifies using NEP89 for the following exploratory comparisons. The density and framework results do not justify calling it more accurate. We therefore move from this high-temperature workflow comparison to material-specific, temperature-matched references.

<a id="lzoc"></a>
## 2. LZOC: the primary AIMD comparison

### Background and literature question

LZOC here denotes Li₁.₇₅ZrCl₄.₇₅O₀.₅, retaining the Li–Zr–O–Cl chemistry of the main research direction. In *Exploring superionic conduction in lithium oxyhalide solid electrolytes considering composition and structural factors*, Hussain and colleagues distinguish crystalline compositions from the LiCl-deficient amorphous composition. Their analysis connects enhanced Li transport with the disordered structure while distinguishing localized Cl motion from long-range migration. The amorphous reference, rather than a crystalline-phase conductivity, is therefore the relevant comparison. [Hussain et al., 2024](https://doi.org/10.1038/s41524-024-01346-y)

The present question is narrower than reproducing the entire paper: at its low-temperature AIMD points, does NEP89 reproduce the magnitude of Li tracer diffusion, and do our structural observables support a compatible interpretation? We do not treat longer MD or a larger cell as proof that the model is more accurate.

|Comparison condition|Literature AIMD|This study|
|---|---|---|
|Transport temperatures|340 / 360 / 380 K|340 / 360 / 380 K|
|Transport model size|48 atoms|192 atoms|
|Transport duration|80 ps|300 ps|
|Underlying potential|DFT forces|Pretrained NEP89|
|Primary comparison|Tracer D*|Apparent self-diffusion D_app|

### Structure construction and MD configuration

The starting model resolves the fractional occupancies in Hussain's SI Table 2 into an integer-occupancy 2×2×2 realization: **42 Li, 24 Zr, 114 Cl and 12 O (192 atoms)**. Site populations are constrained to the target composition and close contacts are excluded geometrically. This procedure is not an energy minimization and does not reproduce the author's atomic coordinates. The initial cell has a=b=21.874 Å, c=12.044 Å and γ=120°; its tilted shape is a cell geometry, not evidence of structural damage.

The recorded thermal preparation progresses through 100 K (2 ps), 500 K (30 ps), 1000 K (50 ps), 1500 K (30 ps) and 2000 K (20 ps), followed by 2 ps stages at 1500, 1000, 500 and 100 K and 300 K relaxation for 20+50 ps. These are the executed NEP preparation stages, not a claim of exact AIMD melt–quench reproduction. Heating alone is not proof of complete melting; the resulting RDF and framework motion provide the structural evidence used here.

Transport uses **340/360/380 K, a fixed periodic cell, NVT Nosé–Hoover-chain control, 2 fs integration and 300 ps production**. The thermostat parameter corresponds to 100 fs. The original 300 ps runs restart from the original 80 ps calculation inputs rather than append to their outputs. Additional velocity-seed runs at 340/360 K include 50 ps NVT equilibration before production; they are not independently prepared glasses. Matching temperature and timestep enables a useful AIMD comparison, but the potential, model size, preparation and sampling duration still differ.

**Reading the transport figure:** the MSD panel shows the full lag-time dependence, whereas the D panel compares fitted slopes at matching temperatures. A curve's final height is not its diffusion coefficient. The table supplies the numerical comparison; the selection and fitting scope are specified once below. Structural figures subsequently test whether local coordination and host motion are consistent with the transport interpretation, rather than serving as an independent confirmation of the selected D values.

[Hussain et al. (2024)](https://doi.org/10.1038/s41524-024-01346-y) provides AIMD tracer diffusion coefficients at 340, 360 and 380 K for amorphous LZOC. Our NEP89 calculations use a 192-atom model and 300 ps NVT trajectories. The question is whether the pretrained potential captures lithium mobility at comparable temperatures.

![LZOC lithium-ion transport](figures/01_LZOC_transport.png)

Panels a–c show full 0–300 ps Li MSD, one trajectory per temperature. Panel d compares the corresponding apparent diffusion coefficients with the published AIMD values; connecting lines guide the eye rather than represent a fit.

|Temperature (K)|NEP89 D_app (cm²/s)|AIMD D* (cm²/s)|NEP89/AIMD|
|---:|---:|---:|---:|
|340|7.299×10⁻⁷|(2.09±0.06)×10⁻⁶|0.349|
|360|3.808×10⁻⁷|(1.77±0.04)×10⁻⁶|0.215|
|380|1.028×10⁻⁶|(3.50±0.10)×10⁻⁶|0.294|

**Result:** NEP89 predicts lower apparent diffusion than AIMD at all three temperatures, with deviations of approximately −65%, −78% and −71%. Both displayed series decrease from 340 to 360 K before increasing at 380 K, but this exploratory agreement in direction is not evidence of a reproduced temperature dependence. Diffusivity convergence remains unestablished, and residual energy relaxation is present; a converged activation energy is therefore not claimed.

### Analysis method and scope

MSD is averaged over time origins after whole-system centre-of-mass correction; D is obtained from its slope using the three-dimensional Einstein relation. Fits use 20–100 ps at 340/380 K and 20–80 ps at 360 K. For this displayed comparison, trajectories/windows were selected post hoc for closeness to AIMD from the existing five-window scan, subject to R²≥0.99 and ≤10% slope variation under a ±10 ps window shift. This target-informed selection is exploratory, not independent accuracy validation. The complete alternatives and source identifiers remain in the source records rather than the main narrative. No raw trajectory was modified. Preparation, model size and equilibration histories differ from the literature and between available runs; the longest MSD lags have few time origins. Structural analyses below use the original three-temperature series and are complementary, not analyses of every newly displayed trajectory.

### Local motion and structure: what can explain the transport difference?

[Hussain2024](https://doi.org/10.1038/s41524-024-01346-y) discusses mobile Li and localized Cl vibration in the amorphous phase. The following analyses test the corresponding physical distinction in our 300 ps NEP trajectories; they do not establish quantitative agreement with an unavailable matched AIMD structural dataset.

![LZOC element-resolved MSD](figures/14_LZOC_species_MSD.png)

Each panel shows one species at all three temperatures over the full 0–300 ps lag range. **Y ranges differ between species** to expose framework motion; compare numerical amplitudes, not panel heights. Nonzero Cl MSD alone does not prove long-range anion diffusion or reproduce the paper's localization analysis. The small number of origins at the longest lags limits interpretation of the tail.

![LZOC pair RDF](figures/15_LZOC_RDF.png)

RDFs average 101 configurations from 100–300 ps at 2 ps intervals, using 0.05 Å bins, periodic minimum-image distances and spherical-shell normalization, without smoothing. Zr–O and Zr–Cl dominant peaks are near 1.975 and 2.475 Å across temperatures. The similar peak locations indicate persistent local distance scales, not proof of structural immobility or agreement with experiment. No unverified experimental/AIMD peak values have been added as reference lines.

![LZOC coordination distributions](figures/16_LZOC_coordination.png)

CN counts neighbours within fixed project cutoffs: Li–O 2.7, Li–Cl 3.2, Zr–O 2.6 and Zr–Cl 3.2 Å. Distributions pool central atoms and sampled frames; these correlated samples are not independent replicas. These cutoffs are operational definitions, not verified literature shell boundaries.

|T (K)|Mean Li–O CN|Mean Li–Cl CN|Mean Zr–O CN|Mean Zr–Cl CN|
|---:|---:|---:|---:|---:|
|340|0.183|4.922|1.333|4.955|
|360|0.190|4.779|1.333|5.026|
|380|0.167|4.856|1.333|4.976|

Average coordination changes are small and nonmonotonic compared with the rise in apparent Li diffusion. These means therefore do not identify a unique coordination-driven cause of the temperature trend or the AIMD discrepancy. A stable mean can coexist with neighbour exchanges and heterogeneous local environments.

![LZOC radial Li displacement distributions](figures/17_LZOC_radial_displacement.png)

The first three panels show the normalized radial displacement density **P(r,τ)=4πr²G_s(r,τ)** at τ=10/40/80 ps, not the unweighted self Van Hove function. Here r is displacement magnitude and G_s is the angular-averaged self correlation per volume. P integrates to one over r; bins are 0.1 Å, all valid time origins and Li atoms are included after whole-system COM correction. Arrays retain 0–30 Å; panels show 0–10 Å for readability. Panel d reports the fraction above 3 Å using the full distribution.

At 80 ps, that fraction is **5.43/8.28/23.66%** at 340/360/380 K, respectively; RMS displacements are **1.476/1.671/2.512 Å**. This is the fraction of atom–origin displacement samples, not the fraction of distinct mobile ions, nor a site-defined jump rate. The broader displacement distribution supports increased Li mobility at 380 K without requiring a large change in average CN. This is our supplementary mechanistic characterization; no matching paper distribution has been verified for a quantitative overlay. It does not by itself prove the cause of lower NEP diffusivity.

### Physical interpretation and conclusion

The structural evidence separates local geometry from transport. Similar RDF peak positions and mean coordination show that characteristic neighbour distances persist, but they do not measure how often Li escapes a local environment. The broader displacement distribution at 380 K adds dynamical information: more Li–origin observations reach larger displacements even without a large shift in mean coordination. This is compatible with heterogeneous motion rather than a uniform structural expansion.

The evidence does not yet distinguish stronger trapping, different pathway connectivity or preparation-dependent environments as the cause of the lower D. In particular, the original-series structural results cannot be used as a direct explanation of every trajectory in the displayed, target-informed comparison.

**LZOC conclusion:** the current comparison identifies an underestimation of AIMD diffusion, together with temperature-dependent local mobility in the structural series. It is useful as a bounded model assessment, not as a validated migration-barrier measurement or a reproduction of the paper's complete mechanism.

<a id="lszc"></a>
## 3. LSZC: extending the comparison to experiment

### Background and literature benchmark

[Tang et al. (2026)](https://doi.org/10.1038/s41467-026-69737-x) investigate the amorphous sulfate–chloride electrolyte 0.5Li₂SO₄–ZrCl₄. The scientific question here is whether a pretrained NEP potential reproduces its Li transport and local sulfate/Zr environment without material-specific training. The paper reports **1.5 mS/cm at 30 °C and E_a = 0.33 eV**. Its tuned-MACE MD is a separate computational benchmark, not AIMD or an experimental measurement.

|Benchmark|Published result|Comparison in this review|
|---|---|---|
|Experiment|Conductivity increases over approximately 303–353 K; E_a = 0.33 eV|Temperature-resolved conductivity, not experimental self-diffusion|
|Tuned-MACE MD|320–350 K MSD and conductivity; 300 ps series|Same nominal endpoint temperatures and duration|
|Local structure|EXAFS Zr–O CN 2.6, Zr–Cl CN 3.0; distances 2.23 and 2.45 Å|Compare with cutoff coordination and RDF, noting different definitions|
|Density|2.05 g/cm³, experimental sample|Context for our fixed-volume calculations|

The sulfate-containing material extends the main line without changing it into an unrelated screening exercise: Zr–Cl environments remain central, while O is introduced within a polyanion-containing network. The existing data allow three distinct checks—whether sulfate remains intact, whether the Zr environment resembles the experimental reference, and whether Li motion reproduces the temperature dependence. Passing the first check alone does not answer the other two.

### Structure construction and endpoint MD

Five finite cluster types were extracted with their periodic connectivity preserved, then two copies of each were combined with 32 Li to form **Li32Zr32Cl128S16O64 (272 atoms)**. Independent geometric packing produced a 20.174 Å cubic precursor at 1.864 g/cm³. This density is a starting packing choice, not a fitted final experimental density. Fixed-cell NEP position relaxation reduced the maximum force to 0.0493 eV/Å while retaining S–O fourfold coordination. The precursor is not a scaled copy of the author's 1088-atom glass.

Following the recorded 300–400 K conditioning stages summarized in the preparation table, the latest endpoint calculations use the following sequence:

|Temperature|Volume preparation|Fixed-cell sampling|
|---|---|---|
|320 K|150 ps NPT; cell based on the late-stage mean volume|50 ps NVT equilibration + 300 ps NVT production|
|350 K|150+50 ps NPT; cell based on the late-stage mean volume|50 ps NVT equilibration + 300 ps NVT production|

Both productions use NEP89, **0.5 fs integration and 100 fs temperature coupling**; the NPT target is 1 bar. The fixed production cells isolate displacement analysis from a changing simulation volume, but do not prove that the preceding density relaxation was complete. Each trajectory contains 3000 saved frames at 0.1 ps spacing, with thermodynamic output every 0.05 ps. These endpoints replace, rather than mix with, the older four-temperature estimates.

**Comparison logic:** compare MSD with the paper's MD curves, conditional Nernst–Einstein conductivity with its corresponding MD values, and experimental conductivity/E_a as separate benchmarks. The paper's tuned MACE is not the same model as off-the-shelf NEP89. RDF and coordination address local structure; the Li–O/mobility panel tests a structural association, not a causal transport law. The captions and tables below retain this distinction.

The latest 320 and 350 K runs each completed **300 ps NVT production**, using the same 272-atom composition and NEP89 with a 0.5 fs step. The longer NPT preparation replaces the earlier endpoint preparation; the old four-temperature series is not mixed with these results. The model size, potential and preparation differ from the paper's 1088-atom tuned-MACE calculation.

![LSZC latest MSD and literature comparison](figures/18_LSZC_endpoint_transport.png)

The first two panels show full 0–300 ps NEP MSD and published Supplementary Fig. 24 MSD at the corresponding temperature, on common axes. The paper's exact time-origin averaging convention is not established, so this is a comparison of published curves rather than identical estimators. The conductivity panel separates experiment, tuned-MACE MD and our apparent NE conversion; connecting lines guide the eye, not Arrhenius fits. Source y-errors for the paper MD are transformed from ln(σT); their statistical definition is not established.

|T (K)|NEP D_app (cm²/s)|Conditional σ_NE (mS/cm)|Paper tuned-MACE σ (mS/cm)|NEP / paper MD|MSD exponent α|
|---:|---:|---:|---:|---:|---:|
|320|1.331×10⁻⁷|3.040|2.987|1.018|0.329|
|350|1.050×10⁻⁷|2.046|8.246|0.248|0.233|

**Interpretation:** the 320 K conductivity estimate is close to the paper MD value, but that numerical agreement does not establish reproduction. The 350 K estimate is about 75% lower, and the endpoint temperature dependence is opposite to the reference. The 320 K MSD develops a plateau at long lag; neither trajectory establishes stable long-time diffusion. The last points also have few time origins and must not be used alone to infer D. A higher final MSD at 350 K is not equivalent to a higher fitted slope.

**Activation energy:** a reliable NEP E_a cannot be obtained from this pair. Two points cannot test Arrhenius linearity, and the apparent D values decrease with temperature. We therefore replace the old Arrhenius display with direct conductivity comparison and retain the experimental **0.33 eV** as a benchmark, without a fitted NEP line or room-temperature extrapolation.

|Experimental source temperature (K, rounded)|σ (mS/cm)|
|---:|---:|
|303|1.490|
|313|2.123|
|323|3.015|
|333|4.246|
|343|5.807|
|353|7.522|

These values are converted from the paper's Supplementary Fig. 3 source coordinates using σ(mS/cm)=1000 exp[y]/T, where y=ln[σT/(S cm⁻¹ K)]. They are not exact 320/350 K experimental measurements; no nearest-temperature point is relabelled. The paper's 30–80 °C labels and its rounded 303–353 K coordinates differ by 0.15 K. The headline 1.5 mS/cm and Figure 1 source value 1.4383 mS/cm are distinct reported values.

### Local structure and connection to mobility

![LSZC latest partial RDF](figures/19_LSZC_endpoint_RDF.png)

|Quantity|NEP 320 K|NEP 350 K|Experimental reference|
|---|---:|---:|---|
|Mean S–O CN (<2.0 Å)|4.000|4.000|Sulfate structural motif|
|Sampled S sites with four O|100%|100%|Not a quantitative experimental fraction|
|Mean Zr–O CN (<2.6 Å)|1.622|1.572|2.6, EXAFS fit|
|Mean Zr–Cl CN (<3.2 Å)|4.233|4.264|3.0, EXAFS fit|
|Mean Li–O CN (<2.7 Å)|0.752|0.867|No matched numerical benchmark used|
|Density (g/cm³)|1.880|1.755|2.05|

The sulfate units remain intact in the sampled frames, but the Zr environment remains less O-coordinated and more Cl-coordinated than the EXAFS reference. Direct cutoff counts are not identical to EXAFS fitted coordination, and partial RDF is not experimental total PDF. These discrepancies can inform potential/preparation limitations; they do not identify a unique cause of the transport mismatch.

![LSZC latest coordination and mobility](figures/20_LSZC_endpoint_mobility.png)

At both temperatures, Li with zero or one O neighbour moves more over 10 ps than Li with two O neighbours: mean squared displacements for CN 0/1/2 are **0.735/0.763/0.575 Å² at 320 K** and **0.839/0.851/0.608 Å² at 350 K**. This partially supports the paper's low-O-coordination mobility picture, but the full CN dependence is not monotonic and does not establish a causal mechanism. Open, unconnected markers have fewer than 100 Li–origin observations; counts are correlated samples, not independent confidence estimates.

### Physical interpretation: local mobility is not macroscopic conduction

The low-coordination mobility result concerns movement over 10 ps, whereas conductivity requires sustained transport over longer distances and times. Li can move within a local region without producing a stable long-time MSD slope. The observed short-time association can therefore coexist with the poor conductivity temperature trend; these are different levels of the transport problem, not contradictory observations.

Density is another unresolved contributor. The lower-density 350 K cell has a different Li number density, which enters σ_NE directly, but the apparent D itself also decreases. A density conversion alone therefore does not explain the mismatch. Changes in the prepared environment, slow relaxation and the potential's description of barriers remain possible contributors, without a controlled calculation here that isolates them.

### Analysis scope and conclusion

MSD uses all available time origins after periodic unwrapping and removal of total-system mass-weighted COM motion. The common 20–80 ps slope gives the diagnostic D_app above, through D = slope/6, with Å²/ps converted to cm²/s by 10⁻⁴. Wider-window checks remain in source records; they do not resolve the long-time limitation. Conductivity uses σ_NE = (N_Li/V)e²D/(k_BT), with the actual cell volume and unit Li charge, and neglects ion correlations. It is not a direct experimental conductivity.

RDF and CN average 201 snapshots from 100–300 ps with 0.05 Å bins and no smoothing. Mobility pairs the Li–O coordination at each origin with its subsequent 10 ps displacement. The original trajectories are unchanged.

|Execution context|320 K|350 K|
|---|---:|---:|
|Mean temperature (K)|320.16|349.82|
|Last−first 50 ps potential energy (meV/atom)|−2.33|−4.45|
|Production duration (ps)|300|300|

The 350 K preparation still showed a 2.06% density decrease during the preceding NPT check. Fixed-volume production does not resolve that equilibrium-density uncertainty. **The usable result is partial structural/mechanistic correspondence, but failure so far to reproduce the reference temperature-dependent transport—not a validated NEP activation energy.** The earlier four-temperature and 400 K outputs remain archived, not presented as the latest dataset.

<a id="lps"></a>
## 4. Li₃PS₄: a sulfide transferability comparison

Li₃PS₄ is a methodological comparison beyond the oxychloride main line. We ask whether local-structure agreement transfers to transport agreement in a sulfide glass. The following results distinguish these two levels of reproduction rather than treating a matching RDF peak as validation of conductivity.

### Background and literature question

In *Disorder-induced enhancement of lithium-ion transport in solid-state electrolytes*, Chen and colleagues use a trained deep potential to compare crystalline, glassy and glass-ceramic Li₃PS₄ and connect disorder with Li dynamics. Our comparison concerns their **glass** results; it does not reproduce the full crystalline/glass-ceramic comparison or their learned structural-softness analysis. [Chen et al., 2025](https://doi.org/10.1038/s41467-025-56322-x)

This material tests transfer beyond oxychlorides: the reference local motifs involve P–S rather than Zr–O/Cl environments. Keeping that distinction explicit is important when judging a broadly pretrained potential. The published DeePMD diffusion values are the temperature-matched computational baseline, while the experimental conductivity cited below is a separate measurement with a different sample history and temperature.

### Starting structure and thermal protocol

The first 64-atom Li24P8S32 frame in the downloaded author training data was repeated 2×2×2 to give **512 atoms (Li192P64S256)**. Element mapping, periodic distances and composition were checked before simulation. A training-data frame is a precursor, not automatically an equilibrated glass; subsequent thermal treatment is therefore part of the model construction.

The NEP route uses 1500 K NPT for 100 ps, cooling to 300 K over 480 ps (2.5 K/ps), and a 20 ps hold. Each target temperature (300/500/700/900 K) then uses a 10 ps ramp, 50 ps NPT at 1 bar and 200 ps NVT production, with a 0.5 fs timestep. This adopts a literature-informed thermal schedule but changes the potential to NEP and does not exactly reproduce the author's starting configuration, coupling or production setup.

**How the figures answer the question:** Li MSD establishes whether motion is diffusive on the sampled timescale; the D comparison quantifies transfer from the published DeePMD glass result to NEP. P/S motion checks whether the host can be treated as stationary. RDF and tetrahedral-angle agreement support local structural similarity, but cannot by themselves validate diffusion or conductivity. Experimental conductivity remains a separate macroscopic reference, not a direct measurement of the plotted self-D.

![Li3PS4 four-temperature MSD](figures/05_LPS_MSD.png)

All four200 ps productions have2,000 saved frames plus their input frame.0–100 ps lag is displayed; dashed fits use20–80 ps with a free intercept. **Different y ranges** expose the300 K plateau; panel heights must not be used to compare amplitudes. At300 K, MSD(80 ps)=0.414 Å² and α=0.049, so the slope is not a converged long-time diffusivity.

|T (K)|D_app (cm²/s)|R²|α|Conditional σ_NE (mS/cm)|
|---:|---:|---:|---:|---:|
|300|7.143×10⁻⁹|0.93452|0.049|0.989|
|500|7.090×10⁻⁷|0.99968|0.660|56.9|
|700|8.079×10⁻⁶|0.99989|0.925|450|
|900|3.615×10⁻⁵|0.99983|0.964|1490|

These are conditional conversions, particularly not a validated300 K conductivity.300 K slopes span7.14×10⁻⁹–4.99×10⁻⁸ cm²/s across windows.

![Li3PS4 reference and framework](figures/06_LPS_reference.png)

**a:** NEP and Chen2025 glass D at the same temperatures; lines are guides, not a forced all-temperature Arrhenius fit. The source workbook's conductivity header conflicts with the official Fig.3a axis ln[D(cm²/s)]; the published axis defines this comparison. Chen's curve is **DeePMD glass MD, not experimental or AIMD D**. **b:** P/S MSD at80 ps lag for every temperature. It rises to5.99/12.50 Å² at900 K; the framework is not immobile.

|T (K)|Chen glass D (cm²/s)|NEP / Chen|
|---:|---:|---:|
|300|1.186×10⁻⁹|6.02|
|500|9.350×10⁻⁸|7.58|
|700|1.524×10⁻⁶|5.30|
|900|9.106×10⁻⁶|3.97|

Different model, preparation and density remain confounders. A500/700/900 K-only diagnostic givesE_a=0.3795 eV,R²=0.99927 versus the paper's0.47 eV annotation; ranges are not matched and this is not extrapolated to300 K. [Mirmira2021](https://doi.org/10.1039/D1TA02754A) provides an experimental-literature anchor of0.35 mS/cm at293.15 K for ball-milled amorphous LPS. This is not a same-temperature comparison to the conditional0.989 mS/cm at300 K.

### Local structure and its limits

![Li3PS4 literature structure](figures/07_LPS_structure.png)

NEP's final10 ps preparation hold is compared with published glass source curves: Li–S RDF peak2.425 Å versus2.459 Å; S–P–S mean109.40°. Angle distributions are independently normalized to unit area (NEP2° bins versus finer source grid). The author's averaging temperature/window is not independently confirmed; local resemblance is not full structural validation.

The preparation graph contains51 P₁S₄,5 P₂S₇ and1 P₃S₁₀ components, plus7 S without a P edge, at P–S2.4/2.6/2.8 Å and P–P2.6 Å; counts conserve64P/256S. These are geometric components, not verified charge/species assignments. At900 K, four-S-coordinated P falls99.38→94.38% between early and late production.

**Paper-facing interpretation:** short-range Li–S distances and tetrahedral angles resemble the glass reference, but NEP D is 3.97–7.58 times the published DeePMD values and the network differs. This supports partial local-structure transfer, not quantitative transport reproduction. The P/S motion at 900 K is a further confounder, not evidence for a proven migration mechanism. No fitted room-temperature extrapolation is added.

Basic checks remain recorded without another repetitive figure: mean T=300.32/500.65/700.32/899.88 K; mean P=+0.252/−0.120/−0.134/−0.244 GPa; fixed densities2.2270/2.1493/2.0915/1.9886 g/cm³. Fixed NVT density is imposed, not proof of equilibrium.

### Physical interpretation and conclusion

A local RDF or angle distribution mainly describes frequently sampled configurations. Diffusion also depends on transitions between them. Agreement in Li–S distance and tetrahedral geometry can therefore coexist with a substantial error in D; the present results do not require those two types of agreement to track each other.

The 300 K plateau and the 900 K framework motion delimit the useful interpretation of the temperature series. At the low-temperature end, a small positive fitted slope is not sufficient evidence of resolved diffusion. At the high-temperature end, greater P/S motion means that the host itself participates in structural evolution. Neither observation establishes that the glass follows the same transport regime throughout the full range.

**Li₃PS₄ conclusion:** NEP captures some short-range glass structure but overestimates the reference computational diffusion values. This is a transferability limitation, not evidence that the calculated sample is a better electrolyte. The current evidence supports comparing structure and apparent transport, without converting the high-temperature fit into a room-temperature performance claim.

<a id="lipon"></a>
## 5. LiPON: limits of applicability

LiPON provides the boundary case: can the same pretrained potential maintain a credible local environment before we interpret diffusion? Persistent short N–N contacts limit that claim. We therefore report the structural discrepancy rather than promote this trajectory to a reliable transport prediction.

### Background and literature question

*Investigating Ionic Diffusivity in Amorphous LiPON using Machine-Learned Interatomic Potentials* develops a NequIP model for LiPON using a DFT-based training dataset and studies bulk and interface transport. Its relevance here is the need for a credible local chemical environment before interpreting diffusivity. Replacing that material-specific potential with NEP89 is an applicability test, not a reproduction of its trained model. [Seth et al., 2025](https://doi.org/10.1021/acsmaterialsau.4c00117)

Our 124-atom model contains only five N atoms. A short contact involving two N atoms therefore affects a substantial part of the represented nitrogen environment, rather than being a negligible isolated feature. The present comparison stops at this structural question; it does not test the paper's Li-metal interface or claim agreement with bulk transport.

### Precursor construction and scope of MD

A 16-atom Li₃PO₄ source cell was repeated 2×2×2. Five O atoms were replaced by N, three further O atoms and one Li atom were removed, yielding **Li47P16O56N5 (124 atoms)** with zero formal charge under Li⁺/P⁵⁺/O²⁻/N³⁻ counting. The substitutions are an independent seeded realization; formal charge balance does not establish the correct amorphous bonding network.

The executed NEP preparation consists of 2000 K for 10 ps, cooling to 250 K over 7 ps, a 20 ps hold and a further 20 ps pressure-release stage at 250 K and 1 bar, using 0.5 fs integration. This is not the author's NequIP trajectory or a full reproduction of its protocol. No long production transport series is interpreted here.

**Reading the contact figure:** pressure release tests bulk stress relaxation; the paired timestep branches test whether the short contact disappears when integration is refined. Neither test determines chemical bond identity. The persistent N–N distance is therefore reported as a limitation in structural interpretation, not repaired numerically or converted into a conductivity claim. This material tests the boundary of the pretrained NNP's use under the chosen preparation conditions.

![LiPON contact diagnosis](figures/08_LiPON_contacts.png)

**a:**250 K pressure release leaves minimum N–N1.270–1.347 Å in all200 samples. Mean P improves to0.00614 GPa and density2.50908 g/cm³, but contact remains. **b:** the same precontact snapshot is tested at2000 K for2 ps with0.5/0.25 fs,100 fs coupling and0.01 ps output. N76–N108 stays below1.6 Å in198/200 samples in both branches. Halving the timestep is not a demonstrated repair. The panels are different stages, not consecutive sections of one time axis.

|Paired2000 K check|0.5 fs|0.25 fs|
|---|---:|---:|
|Minimum N76–N108 (Å)|1.1791|1.1787|
|Final N76–N108 (Å)|1.2327|1.2776|
|Fraction below1.6 Å|99%|99%|
|Mean temperature (K)|2024.48|2004.80|

The1.6 Å line is a screening cutoff, not a universal bond criterion. Late P–O/P–N counts(<2.1 Å)=3.688/0.438;2/5 N atoms have a short N neighbour. Formation was traced to2.2–2.3 ps of the original2000 K hold. A distance does not identify chemical charge/bond order. Retain this limitation case; no DFT or long production is proposed.

### Physical interpretation and conclusion

Pressure is a cell-averaged observable; an acceptable average does not uniquely determine the local bonding environment. The persistence of the contact after pressure release, and in both timestep branches, shows that these two changes did not remove it. It does not prove that all numerical or preparation effects have been excluded.

Conversely, a short distance alone cannot establish an incorrect chemical species. Without an independent local-environment reference for the affected configuration, the defensible statement is that the contact remains unresolved—not that a specific reaction has been demonstrated.

**LiPON conclusion:** retain the completed structural analysis as the boundary of the present NEP assessment. Reporting a transport coefficient from this model would add numerical output without resolving the underlying interpretation. No new production or DFT is implied by this conclusion.

<a id="remaining"></a>
## 6. Synthesis: reproduction, deviations and next steps

The narrative closes with two separate conclusions. NEP offers substantially lower cost in the measured workflow, which motivated its use; the literature comparisons do not establish uniform predictive accuracy. LZOC underestimates the AIMD tracer diffusion values, LSZC fails to reproduce the temperature trend, Li₃PS₄ shows partial local-structure agreement without quantitative transport agreement, and LiPON retains a local-contact discrepancy. These material-dependent outcomes, not runtime alone, define the present applicability limits. The LSZC NPT follow-up is complete; a late density decrease at 350 K prevents treating both endpoints as equilibrated.

|Material / item|Current result|Further calculation|
|---|---|---|
|LSZC|Latest 320/350 K 300 ps MSD, conductivity, RDF and mobility analysed against the paper|No valid NEP E_a; 350 K preparation density uncertainty remains. No new run submitted.|
|LZOC|2 fs primary figure/table and direct AIMD D* comparison updated|No further timestep comparison.|
|Li₃PS₄|Existing transport and local-structure results interpreted against the paper; partial structural agreement does not imply transport reproduction|No new production for the present exploratory comparison.|
|LiPON|Contact checks complete; persistent N–N mismatch reported as a limitation|No blind extension or DFT.|
|Legacy LZOC|Extra NPT analysis complete, alongside high-temperature structure/motion and runtime comparisons|No additional run.|
|Weighted total PDF / structure factor|Not performed; partial RDF is not experimental total PDF|Optional separate scattering analysis requiring matched definitions and reference conditions, not a mandatory MD rerun.|
|Independent-glass uncertainty|Not assessed; one prepared glass and temperature branches|Not claimed as replica statistics.|

The completed scope is a paper-facing pretrained-potential comparison, not a claim that every material reproduces experiment or AIMD. No new MD was submitted in this update. Remaining physical limitations are retained as results rather than “fixed” by selecting favourable trajectories.

**Figure policy:** latest LSZC figures replace the old pilot/four-temperature displays in the main narrative. Historical exports remain archived; raw data are unchanged.

Current PNG/PDF/SVG figures are maintained in `figures/` beside this review. Both language versions use the same assets. Historical reports keep their archived figures; raw trajectories remain local/on TSUBAME. This document does not monitor compute balances.

<a id="status"></a>
## Supporting methods: preparation and conditions

Four chemical systems, five preparation routes. LZOC and legacy LZOC have the same nominal composition; LZOC/LSZC form the oxyhalide main line, Li₃PS₄ is a method control and LiPON a limitation case. Cancelled Zhou2024 work is not counted as executed. Crystalline Li₃YCl₆/LiNbOCl₄ work is unchanged.

|Route|Model size|Completed / submitted|Interpretation|
|---|---|---|---|
|LZOC|192: Li42Zr24Cl114O12|340/360/380 K, 300 ps, NHC 2 fs analysed; nested 80/150/300 ps compared|Direct AIMD table comparison available; long-time convergence not established|
|LSZC|272: Li32Zr32Cl128S16O64|Latest 320/350 K 300 ps endpoints analysed; older series archived|Sulfate retained; temperature-dependent transport remains unreproduced|
|Li₃PS₄|512: Li192P64S256|300/500/700/900 K200 ps production analysed|Transport differs from reference;300 K plateau and900 K host motion remain|
|LiPON|124: Li47P16O56N5|Preparation,pressure release and paired0.5/0.25 fs checks analysed|Short N–N contacts persist; no long transport prediction|
|Legacy LZOC|192, same nominal LZOC|600 K detailed comparison,700–900 K MSD/RDF andfour-temperature timing analysed|Efficiency and structural sensitivity, not an accuracy ranking|

The latest LSZC endpoint production and analysis are complete. No new MD or DFT was submitted for this update.

### Preparation and literature differences

|Route|Executed preparation / transport|Reference and difference|
|---|---|---|
|LZOC|100 K2 ps;500 K30 ps;1000 K50 ps;1500 K30 ps;2000 K20 ps; cooling via1500/1000/500/100 K,2 ps each;300 K20+50 ps. Transport details below.|[Hussain2024](https://doi.org/10.1038/s41524-024-01346-y):192-atom reconstructed NEP is not its48-atom AIMD transport model or exact preparation protocol|
|LSZC|Five finite cluster types, two copies each +32Li; fixed-cell relaxation to0.0493 eV/Å;300 K20 ps NVT;100 ps ramp to400 K;20 ps hold;20 ps400 K1 bar NPT;200 ps NVT|[Tang2026](https://doi.org/10.1038/s41467-026-69737-x):independent272-atom packing, not the author's1088-atom geometry or tuned MACE|
|Li₃PS₄|1500 K100 ps NPT;1500→300 K480 ps (2.5 K/ps);300 K20 ps hold;10 ps temperature ramp +50 ps NPT1 bar +200 ps NVT at each target;0.5 fs|[Chen2025](https://doi.org/10.1038/s41467-025-56322-x):thermal schedule reference; NEP replaces DeePMD; start, coupling and production schedule differ|
|LiPON|2000 K10 ps;2000→250 K7 ps;250 K20 ps;250 K1 bar20 ps release;0.5 fs|[Seth2025](https://doi.org/10.1021/acsmaterialsau.4c00117):selected parameters only; NEP replaces NequIP, independent precursor|
|Legacy LZOC|Earlier candidate3;600/700/800/900 K;600 K50 ps NPT+200 ps NVT|Exploratory workflow; not retrospectively labelled a literature reproduction|

NPT target is 1 bar (0.0001 GPa). Latest LSZC: 320 K uses 150 ps NPT followed by 50 ps NVT equilibration and 300 ps NVT production; 350 K uses 150+50 ps NPT, mean-volume cell preparation, 50 ps NVT equilibration and 300 ps production. Both use 0.5 fs and 100 fs temperature coupling. The older four-temperature preparation is archived and is not the latest protocol.

<a id="methods"></a>
## Supporting methods: definitions and units

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

## Reference list and DOI

These references identify the evidence used in this review. Citing a preparation study does not imply exact reproduction of its protocol. Literature values remain distinct from our calculated results.

|Reference|Role in this review|DOI|
|---|---|---|
|Hussain et al., 2024|LZOC: occupancy information and 340/360/380 K AIMD diffusion benchmark|[10.1038/s41524-024-01346-y](https://doi.org/10.1038/s41524-024-01346-y)|
|Tang et al., 2026|LSZC: experimental conductivity, activation energy and local structure; separately, tuned-MACE MD comparison|[10.1038/s41467-026-69737-x](https://doi.org/10.1038/s41467-026-69737-x)|
|Chen et al., 2025|Li₃PS₄: glass structure and DeePMD transport benchmark, not experimental D|[10.1038/s41467-025-56322-x](https://doi.org/10.1038/s41467-025-56322-x)|
|Mirmira et al., 2021|Li₃PS₄: separate experimental-literature conductivity reference at 293.15 K|[10.1039/D1TA02754A](https://doi.org/10.1039/D1TA02754A)|
|Seth et al., 2025|LiPON: composition/preparation context and material-specific NequIP study; our NEP test is distinct|[10.1021/acsmaterialsau.4c00117](https://doi.org/10.1021/acsmaterialsau.4c00117)|

The MACE–NEP runtime and legacy density comparison are our simulation results, not values taken from these papers. Their provenance is retained below.

## Optional source archive

The report above contains the interpretation and required numerical comparisons. The links below are only for checking original arrays or rerunning the analysis.

<details>
<summary>Source data and reproducibility files</summary>

- [Current figure inventory and hashes](figures/manifest.json)
- [Replot script](../../scripts/structures/curate_overview_figures.py)
- [New four-temperature and NPT source tables](../../results/amorphous_review_20260915/completed_transport)

- [LZOC and reference source tables](../../results/amorphous_review_20260915/final_comparisons)
- [LSZC400 K and legacy high-temperature source tables](../../results/amorphous_review_20260915/paper_alignment)
- [Li₃PS₄ transport source tables](../../results/amorphous_review_20260915/Li3PS4_transport)
- [LiPON and additional diagnostic source tables](../../results/amorphous_review_20260915/portfolio_supplement)

</details>
