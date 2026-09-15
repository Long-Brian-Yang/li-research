> Historical snapshot. The complete, maintained report is [here](../../../docs/materials/materials_overview_en.md).

# Legacy LZOC candidate 3: MACE / NEP comparison

15 September 2026. [日本語](report_ja.md). Replotted from the audited 12 September results; no new MD or trajectory modification. This is a workflow/structure comparison, not completed experimental–AIMD–MLIP accuracy validation. The common starting candidate contains Li42Zr24O12Cl114 (192 atoms).

## 1. Runtime

![Runtime](01_runtime.png)

Left: actual scheduler job runtimes excluding queues for 600/700/800/900 K. Right: engine-reported 600 K production runtime for 200 ps, 400,000 steps, 0.5 fs. MACE/LAMMPS took 11,395.5 s; NEP89/GPUMD 366.428 s, a ratio of 31.10. Both requested gpu_1, but nodes, engines and preprocessing differ; this is not an isolated potential-kernel benchmark. The four-job sums are 18 h 25 min versus 34 min, not parallel elapsed time or points cost. [Timing provenance and job IDs](../../../docs/materials/LZOC/candidate3_mace_nep_comparison.md).

## 2. Density and thermodynamics at 600 K

![Density and thermodynamics](02_density_thermodynamics.png)

Each model has 50 ps NPT followed by 200 ps NVT. Matched axes are used by column. The dotted density is the common 300 K input, not experiment. NVT density is imposed by the final NPT cell. Energy is explicitly (PE−its own production mean)/192, converted to meV/atom. Zero-centred energy is a plotting definition, not zero absolute potential energy; it is not an NVE conservation test. Comparing absolute energies of distinct potentials would not establish accuracy.

|600 K quantity|MACE|NEP89|
|---|---:|---:|
|Production density / g cm⁻³|1.468304|1.875429|
|Volume increase relative to 300 K input|30.3%|2.0%|
|Mean temperature / K|598.89|599.96|

These trajectories occupy different densities and structures. Larger motion cannot be attributed only to a different migration barrier, and smaller expansion does not itself establish realism.

## 3. Local structure

![RDF and coordination](03_RDF_coordination.png)

RDF uses the last 50 ps, 21 frames spaced 2.5 ps apart, periodic minimum-image distances, excluded self-pairs, 0.05 Å bins and no smoothing. The five pairs have matched definitions in both models. Coordination cutoffs are Li–Cl 3.2, Li–O 2.7, Zr–Cl 3.0, Zr–O 2.6 and Cl–Cl 4.0 Å. Cl–Cl denotes geometric neighbours, not valence. Lines between categorical coordination points only guide the eye. Frame SD is in `coordination.csv`; it is not independent-replica uncertainty. No individual-atom coordination distribution is inferred from these means.

|Late mean neighbour count|MACE|NEP89|
|---|---:|---:|
|Li–Cl|3.666|4.542|
|Li–O|0.145|0.293|
|Zr–Cl|4.442|4.839|
|Zr–O|1.125|1.208|
|Cl–Cl|4.472|6.355|

Similar short-range peak positions do not demonstrate a stationary framework. This plot contains model results only, not experimental or AIMD RDF curves.

## 4. Li transport and framework motion

![MSD and framework](04_MSD_framework.png)

Top left: time-origin averaged Li MSD with total-system mass-weighted COM motion removed, not Li-only COM subtraction. The display ends at 100 ps; the CSV retains the full lag range. Fit MSD=aτ+b with free intercept and D_app=(a/6)×10⁻⁴ cm²/s for a in Å²/ps. τ is lag time, not a selected percentage of the trajectory.

|600 K estimate|MACE|NEP89|
|---|---:|---:|
|D_app, 20–80 ps / cm² s⁻¹|1.7197×10⁻⁵|1.0757×10⁻⁵|
|Linear R²|0.9965|0.9998|
|Four-block mean / cm² s⁻¹|2.3955×10⁻⁵|1.006×10⁻⁵|
|Four-block SD / cm² s⁻¹|0.4886×10⁻⁵|0.281×10⁻⁵|

Top right compares full-trajectory lag windows. Bottom left uses four consecutive 50 ps blocks, each fitted over 5–20 ps lag. Block SD is temporal variability, not a confidence interval and not an error bar for the full-trajectory 20–80 ps estimate. High linear R² does not demonstrate converged diffusion.

Bottom right compares **single-origin**, total-system-COM-corrected displacement at 200 ps. It is a different estimator from the time-origin averaged Li curve. Zr/O/Cl endpoints are respectively 58.32/43.18/92.74 Å² for MACE and 9.87/5.60/21.00 Å² for NEP. These show appreciable framework motion; they do not alone prove melting or chemical decomposition. Lines between species only guide the eye.

## 5. Interpretation and data scope

NEP was faster and showed less expansion and weaker framework motion in this 600 K comparison. This supports its use for economical exploratory work, not a claim of superior experimental accuracy. The comparison changes potential, engine, preprocessing, velocity seed and relaxed cell simultaneously. No DFT is proposed. No new Ea or 300 K conductivity extrapolation is made from these structurally differing states.

All four-temperature timing records are included. Structural/transport panels cover **600 K only**: NEP's later 700–900 K and extra NPT runs are not analysed in this package and have not been substituted with another route. The next stage, if desired, is the same source-verified analysis of those existing runs, not new MD.

[Script](../../../scripts/structures/plot_legacy_lzoc_comparison.py), [summary and CSV input hashes](summary.json), [source audit](../analysis_20260912/README.md). Re-run with the existing Python/numpy/matplotlib environment from the repository root. Four figures exported as PNG/PDF/SVG with editable vector text. Data and scripts are committed; raw trajectories are retained separately and not uploaded in this commit.
