> Historical snapshot. The complete, maintained report is [here](../../../docs/materials/materials_overview_en.md).

# Structural follow-up: connectivity and cutoff sensitivity

15 September 2026. [日本語](report_ja.md) · [Main report](../final_comparisons/report_en.md)

This completes two previously unresolved analyses using existing trajectories. No new MD or DFT, altered coordinates, selected replacement replicas or adjusted target values were used.

## 1. Li₃PS₄: coordination does not determine connectivity

We analysed the last ten frames (11–20 ps, 1 ps spacing) of the existing 300 K NPT hold. A periodic minimum-image graph includes P–S edges below each of 2.4/2.6/2.8 Å and P–P edges below 2.6 Å. Li is excluded. Labels below describe connected-component atom counts, **not independently verified chemical species or bond orders**. Free S in this graph means no P neighbour at these cutoffs, not necessarily an isolated physical atom.

All ten frames and all three P–S cutoffs give the same counts:

| Geometric component | Components per frame | P atoms represented | Fraction of all 64 P |
|---|---:|---:|---:|
|P₁S₄|51|51|79.6875%|
|P₂S₇|5|10|15.6250%|
|P₃S₁₀|1|3|4.6875%|
|S without a P edge|7|0|—|

Atom conservation: 51+2×5+3=64 P; 4×51+7×5+10+7=256 S. Seven S atoms per frame have at least two P neighbours (2.7344% of S). No P–P pairs fall below 2.6 Å. Results are identical over this cutoff range; no cutoff was chosen to match a paper.

The earlier result “all P have four S neighbours” remains correct, but it does not imply all P belong to isolated PS₄. The [Chen 2025 structural comparison](../final_comparisons/report_en.md#4-li₃ps₄-published-source-data-comparison) concerns RDF and angle distributions. The author's chemical-speciation percentages are not automatically comparable with this graph's P-weighted fractions; definitions and denominators must match before reporting an error percentage. **Local RDF/angle agreement does not establish network/speciation agreement.**

Source: [per-frame components](Li3PS4_geometric_components.csv), [summary and trajectory hashes](results.json). These frames come from one prepared glass, not ten independent glasses.

## 2. LSZC: is the Zr coordination discrepancy a cutoff artefact?

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

[All values and frame SD](LSZC_cutoff_sensitivity.csv). SD is temporal variability, not uncertainty across independent structures. The earlier Zr–O RDF maximum difference also remains; none of the source distances has been changed.

## 3. What remains, and why more plots alone cannot finish it

| Route | Still unresolved | Appropriate next computational question |
|---|---|---|
|LZOC|Long-time D/Ea convergence; joint thermostat/timestep sensitivity|A controlled continuation from preserved restart, with a declared observation duration and unchanged fit-window audit; not selecting the better-looking Ea|
|LSZC|Density and Zr environment versus reference|Whether a separately labelled ambient-pressure density-relaxation diagnostic changes the local environment; not assuming it will repair NEP|
|Li₃PS₄|Network/speciation agreement and transport|Verify source classification definitions; a dedicated transport trajectory is required before claiming D/Ea|
|LiPON|Persistent short N–N contact|Retain the documented limitation; mere MD extension is not chemical validation, and no DFT is requested|

No new calculation is claimed to have started in this follow-up. The analyses above narrow the next questions without treating numerical completion as experimental validation. Existing preparation, MSD and reference figures remain in the main report.

## 4. Reproduction

[Script](../../../scripts/structures/structure_followup.py) · [Tests](../../../tests/test_structure_followup.py). Run with the existing ASE/numpy/scipy environment: `python scripts/structures/structure_followup.py`. Input SHA256 hashes are in JSON. Four graph tests cover isolated tetrahedra, shared-S dimers, P–P-connected dimers and unconnected atoms. A separate atom-count conservation check verifies the reported material totals.
