# Li–Zr–O–Cl electrolytes: three priority readings

Date: 2026-09-11 | Project target: **Li₁.₇₅ZrCl₄.₇₅O₀.₅**

## 1. Main conclusion

There is a direct experimental reference for our nominal composition, as well as two particularly useful Zr-based studies of local structure and ion transport. However, **matching a chemical formula is not equivalent to reproducing an experimental microstructure**. These readings support studying Li–Zr–O–Cl, but they do not independently validate our current melt–quench structure or MACE potential.

The reading order below is based on relevance: exact composition first, amorphous local structure second, and structural identification plus AIMD third. It is not a bibliometric ranking.

## 2. Composition and experimental reference map

| Reading | Composition associated with the listed measurement | Conductivity at 25 °C | Interpretation |
|---|---|---:|---|
| Hu et al. (2023) | Li₁.₇₅ZrCl₄.₇₅O₀.₅ | 2.42 mS/cm = 2.42 × 10⁻³ S/cm | Direct nominal-composition reference for this project |
| Zhang et al. (2024) | Li₃ZrCl₄O₁.₅ | 1.35 ± 0.07 mS/cm | Related amorphous oxychloride, not the same composition |
| Kim et al. (2025) | 0.8Li₂O–ZrCl₄; nominal Li₁.₆ZrCl₄O₀.₈ | 1.78 mS/cm | Related composition and processing route; not an interchangeable baseline |

Sources: [Hu et al.](https://www.nature.com/articles/s41467-023-39522-1), [Zhang et al.](https://doi.org/10.1021/jacs.3c07343), [Kim et al.](https://www.nature.com/articles/s41467-025-65702-2).

**25 °C means 298.15 K, not exactly 300 K.** Report the experimental measurement temperature explicitly when comparing it with a simulated 300 K extrapolation. Also, pellet relative density is not an absolute density in g/cm³.

## 3. Paper 1 — original reference for the target composition

**L. Hu et al., “A cost-effective, ionically conductive and compressible oxychloride solid-state electrolyte for stable all-solid-state lithium-based batteries.”** *Nature Communications* **14**, 3807 (2023). Published 27 June 2023. [DOI: 10.1038/s41467-023-39522-1](https://doi.org/10.1038/s41467-023-39522-1).

### Research question and methods

The study asks whether a Zr-based oxychloride can combine high ionic conductivity with favorable processing properties. It explores the LiCl–ZrCl₄–Li₂O composition space using mechanochemical preparation, diffraction, structural refinement, microscopy, and electrochemical impedance measurements. The preparation includes prolonged high-energy ball milling; it is not a thermal melt–quench synthesis.

### Main findings

- The target Li₁.₇₅ZrCl₄.₇₅O₀.₅ reaches **2.42 mS/cm at 25 °C**.
- The material is highly disordered but contains crystalline components. The structural discussion includes two crystalline phases embedded in a strongly amorphized material; it does not establish a single homogeneous glass.
- The paper associates enhanced conduction with amorphous species rather than simply with coexistence of two crystalline phases.
- The reported **94.2% relative density under 300 MPa** describes pellet compaction. It does not supply an absolute mass density for initializing an MD box.

These findings and their composition dependence are reported in the [publisher full text](https://www.nature.com/articles/s41467-023-39522-1).

### Figures to read

Read **Fig. 1** for phase identification, **Fig. 3** for the optimized LiCl-deficient compositions and transport, and **Fig. 4** for compressibility. Fig. 2 concerns the earlier composition series, so do not assign all its numbers to the optimized target.

### What we can use, and what we cannot

**Use:** the formula and measured conductivity as the primary composition-matched experimental reference.

**Do not assume:** that a melt-quenched homogeneous cell reproduces the ball-milled specimen, that relative pellet density fixes our simulation density, or that every structural fraction reported for another member of the series applies to the target. The target activation energy has **not been numerically transcribed and independently checked in these notes**; no value from another composition is substituted for it.

**Project interpretation:** our Li₅₆Zr₃₂O₁₆Cl₁₅₂ cell has the intended nominal ratio, but its local structure, density, and degree of crystallinity remain separate validation questions.

## 4. Paper 2 — amorphous local structure in a related Zr composition

**S. Zhang et al., “Amorphous Oxyhalide Matters for Achieving Lithium Superionic Conduction.”** *Journal of the American Chemical Society* **146**(5), 2977–2985 (2024). Online 29 January 2024. [DOI: 10.1021/jacs.3c07343](https://doi.org/10.1021/jacs.3c07343). [Author-hosted full text](https://www.eng.uwo.ca/nanoenergy/publications/2024-amorphoxyh.pdf).

### Evidence summary

For **Li₃ZrCl₄O₁.₅**, the impedance-derived activation energy is **0.294 ± 0.003 eV**. Scattering and absorption measurements, interpreted with reverse Monte Carlo modelling, support interconnected Zr-centered oxygen/chlorine coordination environments. Read **Fig. 2** for transport and **Fig. 3** for structure. Reverse Monte Carlo reconstruction is not a dynamical trajectory. NMR and impedance probe different aspects of motion; their barriers should not be conflated. [Source](https://www.eng.uwo.ca/nanoenergy/publications/2024-amorphoxyh.pdf).

### Project interpretation — not a reported result for our cell

This reading motivates a structural question for our own calculations: does oxygen connect Zr-centered environments, and how do those environments constrain Li motion? We should therefore examine Zr–O and Zr–Cl correlations and coordination distributions alongside Li–O and Li–Cl, rather than treating Li MSD alone as a structural validation.

Its activation energy is **not a target to impose on Li₁.₇₅ZrCl₄.₇₅O₀.₅**. Agreement obtained by selecting trajectories or fitting windows to approach that number would not establish model accuracy.

## 5. Paper 3 — structural identification and an AIMD reference

**J.-S. Kim et al., “Divalent anion-driven framework regulation in Zr-based halide solid electrolytes for all-solid-state batteries.”** *Nature Communications* **16**, 10678 (2025). Published 27 November 2025. [DOI: 10.1038/s41467-025-65702-2](https://doi.org/10.1038/s41467-025-65702-2).

### Research question and methods

The paper examines how oxygen or sulfur changes Zr-based halide frameworks and ion conduction. Laboratory diffraction is combined with higher-resolution synchrotron measurements, pair-distribution-function analysis, spectroscopy, DFT, and AIMD. Importantly, weak or broad laboratory diffraction features are not treated as sufficient proof of complete amorphization.

### Main findings and scope

The oxygen-containing specimens reveal nanocrystalline hcp-related structural features, whereas the sulfur-containing system shows a different framework. The authors connect divalent-anion incorporation to local distortion and changes in Li migration environments. This is a reason to investigate nanocrystallinity in our candidate, not proof that all materials in the earlier papers must have the same structure. Composition, preparation, and measurement sensitivity differ. [Full text](https://www.nature.com/articles/s41467-025-65702-2).

### AIMD conditions worth retaining

| Item | Reported method |
|---|---|
| Important oxygen-containing simulation composition | Li₂.₅ZrCl₅.₅O₀.₅ — different from both our target and the nominal experimental 0.8Li₂O–ZrCl₄ mixture |
| Ensemble | NVT, Nosé–Hoover thermostat |
| Thermostat period | 80 fs |
| Simulation cells | 1 × 1 × 2 supercells, cell-vector lengths greater than 10 Å |
| Temperature range | 600–900 K |
| Heating | From 100 K to target temperature over 2 ps |
| Production duration | 300 ps |
| Time step | 2 fs |

Source: computational methods in the [paper](https://www.nature.com/articles/s41467-025-65702-2). The reported range is retained without assuming an unverified list of discrete temperatures.

Read **Fig. 1** for structural identification, **Figs. 2–3** for local structure, **Fig. 4** for simulated transport, and **Fig. 5** for migration-environment interpretation. Supplementary structural datasets are available from the publisher, but have not been independently reconstructed in this reading exercise.

**Correction checked:** the 29 January 2026 [Author Correction](https://doi.org/10.1038/s41467-026-68882-7) corrects the spelling of **Yoon Seok Jung**; it does not report a change to the transport results.

## 6. Implications for our next simulation

The following are **our methodological conclusions**, not results already demonstrated for our candidate:

1. **One candidate is sufficient for a pilot, not for structural uncertainty.** It can test whether the workflow runs and reveal obvious failures. Independent preparations are needed before claiming representative amorphous transport.
2. **Separate composition from phase identity.** Describe the present system as a “melt-quenched model at the nominal Li₁.₇₅ZrCl₄.₇₅O₀.₅ composition” until local order and density have been assessed.
3. **MACE remains a hypothesis to test.** These papers are not validations of our checkpoint. Element coverage alone does not establish accuracy for oxygen/chlorine chemistry, high-temperature liquids, forces, stress, or diffusion barriers.
4. **Do not transfer an AIMD time step automatically.** Our potential, thermostat, cell, and temperature require their own numerical checks. Neither 200 ps nor 300 ps guarantees converged diffusion.
5. **Keep structural and transport evidence connected.** Prioritize density/volume and energy evolution; RDF and coordination distributions; then Li MSD, diffusion uncertainty, and multi-temperature activation energy. A visually plausible snapshot is insufficient.
6. **Compare conductivity with like quantities.** An experimental conductivity and a tracer-diffusion-based Nernst–Einstein estimate are not necessarily identical, particularly when ion motions are correlated.

For an uncorrelated monovalent-Li estimate, the working conversion is

$$
\sigma_{\mathrm{NE}}(T)=\frac{n_{\mathrm{Li}}e^2D_{\mathrm{Li}}(T)}{k_{\mathrm B}T},\qquad n_{\mathrm{Li}}=N_{\mathrm{Li}}/V.
$$

Here $D_{\mathrm{Li}}$ is the Li self-diffusion coefficient, $n_{\mathrm{Li}}$ is number density, $e$ is the elementary charge, and $k_{\mathrm B}$ is Boltzmann's constant. SI inputs give S/m; **1 S/m = 10 mS/cm**. The number density and approximation must be stated, rather than treating the experimental conductivity as a directly measured diffusion coefficient.

## 7. Reading and reuse limitations

Publisher metadata and main texts were consulted; the reports are not an exhaustive audit of all supplementary information or a reproduction of the simulations. Exact numerical values not checked are identified as such. Papers 1 and 3 are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); these notes are original paraphrases with attribution. Paper 2 is summarized briefly and linked without reproducing its figures or full text. See [verification notes](source_notes.md).
