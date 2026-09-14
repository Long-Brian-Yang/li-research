# Progress report: LZOC structure preparation and MD at 600 K

Report date: September 14, 2026

[日本語](ja.md) · [Daily report index](../README.md)

## 1. Objective

A structural model and MD workflow were prepared to investigate Li-ion motion in amorphous Li₁.₇₅ZrCl₄.₇₅O₀.₅ (LZOC), an oxychloride electrolyte. This report covers structure preparation and the execution of a single-temperature MACE simulation at 600 K.

## 2. Structural model preparation

Structural files for a related composition reported in the literature were used as a starting point, and the composition was adjusted to prepare a computational model. After high-temperature treatment, cooling, room-temperature equilibration, and structural relaxation, candidate 3 was selected as the starting structure for MD.

| Item | Description |
|---|---|
| Target composition | Li₁.₇₅ZrCl₄.₇₅O₀.₅ |
| Total number of atoms | 192 |
| Element counts | Li 42, Zr 24, O 12, Cl 114 |
| Starting structure | Candidate 3 after equilibration at 300 K |
| Boundary conditions | Three-dimensional periodic boundaries |

This is an exploratory model informed by the literature, not a direct reproduction of an experimentally determined amorphous configuration. Its consistency with the real material must be assessed through structural and density analysis.

### Why prepare the structure this way?

An amorphous material does not have a unique periodic atomic arrangement like a crystal, so composition alone does not specify its starting configuration. A related literature structure provides a reference for local coordination rather than starting from a completely random arrangement. However, changing the composition also changes the structure, making further relaxation and validation necessary.

| Preparation stage | Conditions | Purpose and limitations |
|---|---|---|
| Initial relaxation | Optimize atomic positions at fixed cell | Reduce close contacts and large forces introduced by composition changes. Optimization alone does not produce an amorphous structure. |
| High-temperature treatment | 1500 K, NVT, 10 ps | Allow atoms to rearrange away from the initial configuration. Heating alone does not demonstrate complete melting. |
| Cooling | 1500 → 300 K, NVT, 30 ps | Prepare an amorphous candidate from the high-temperature configuration. The MD cooling rate is faster than experimental rates, and the resulting structure may depend on this protocol. |
| Room-temperature hold | 300 K, NVT, 5 ps | Reduce transient changes in temperature and local structure after cooling. |
| Volume relaxation | 300 K, 1 bar, NPT, 10 ps | Allow the volume to adjust as well as atomic positions. This was followed by another fixed-cell atomic relaxation. |
| Additional equilibration | 300 K, 1 bar, NPT, 50 ps | Further relax the candidate and prepare the starting point for subsequent MD. |

The 192-atom model represents the target composition with integer atom counts while keeping the multistage preparation and MD calculations computationally manageable. This does not establish that the system size is converged. Finite-size effects and dependence on amorphous preparation remain limitations to assess when needed.

## 3. MACE MD at 600 K

A single-temperature calculation was performed first to check the simulation workflow.

| Item | Setting |
|---|---|
| Potential | MACE-MPA-0 |
| Implementation | LAMMPS / ML-IAP, GPU |
| Computing facility | TSUBAME |
| Time step | 0.5 fs |
| Heating | 300 → 600 K, NVT, 10 ps |
| Equilibration | 600 K, 1 bar, NPT, 50 ps |
| Production | 600 K, NVT, 200 ps |
| Temperature and pressure control | Nosé–Hoover family; Tdamp 0.1 ps, Pdamp 1 ps |
| Number of simulations | One structure, one run |

Workflow:

**Structure equilibrated at 300 K → heating to 600 K → NPT equilibration → NVT production**

The cell volume was allowed to change during NPT equilibration. The final NPT cell was then held fixed during NVT production. A specified equilibration duration or successful program termination does not, by itself, establish physical validity.

### Why start with one temperature at 600 K?

Starting with one temperature allows the structure input, potential execution, temperature control, and output format to be checked together. The aim was to identify common setup or structural problems before extending the workflow to multiple temperatures.

Li motion is expected to be easier to observe at 600 K than at room temperature, while 600 K is the lower end of the planned 600–900 K range. It was therefore chosen as an initial exploratory condition. This does not guarantee that the experimental phase is preserved at 600 K or that this is the optimal temperature.

### Rationale for the simulation settings

- **Gradual heating:** The temperature was increased over 10 ps rather than changed abruptly, allowing the transient response to be examined.
- **NPT equilibration:** The volume was allowed to adjust at the target temperature and pressure. Persistent density drift near the end would mean that equilibration is not established, even after 50 ps.
- **NVT production:** A fixed cell allows displacements to be analyzed without cell-volume fluctuations. This requires the selected volume to be physically appropriate.
- **A 0.5 fs time step:** This provides a fine temporal resolution for atomic motion. Its adequacy must still be assessed from numerical stability and, if necessary, short time-step comparison tests.
- **A 200 ps production period:** This was selected for initial diffusion and structural analysis. Whether it is sufficient must be evaluated by comparing analysis windows and time blocks.
- **One initial structure and one run:** The initial priority was workflow verification. This cannot quantify variability between independently prepared amorphous structures or establish reproducible material properties.

## 4. Current milestone

Structure preparation and the MACE simulation at 600 K have been completed. Job 8635176.1 terminated normally, and the trajectory and logs, including temperature and energy, were saved.

This report does not present diffusion coefficients, activation energies, multitemperature comparisons, or comparisons between potentials. Physical results will be reported separately after structural validity, density, and convergence have been assessed.

## 5. Next steps

### Priority 1: Assess structural and density validity

Examine temperature, energy, and density as functions of time. In particular, determine whether density reaches a stable range near the end of NPT equilibration and whether the volume changes excessively relative to the initial model. The current simulation has volume and framework behavior that requires further checking, so this assessment takes priority over interpreting diffusion coefficients.

Compare Li–Cl, Li–O, Zr–Cl, and Zr–O radial distribution functions (RDFs) and coordination numbers, and examine Zr, O, and Cl displacements. This distinguishes Li motion from rearrangement of the framework itself. Similar average RDFs do not rule out neighbor exchange or framework motion.

When using density references, distinguish measured density for the same composition from the relative density of a pressed pellet. If discrepancies remain, revisit structure preparation and potential applicability, including energy–volume behavior and stress consistency where necessary. Density and curves should not be adjusted simply to obtain a preferred appearance.

### Priority 2: Analyze Li diffusion and test convergence

After assessing the structural state, calculate the time-origin-averaged Li mean-squared displacement (MSD) from the production trajectory. Treat periodic-boundary crossings and overall center-of-mass motion consistently, and examine whether a normal-diffusion regime can be identified.

Estimate the diffusion coefficient D from the MSD slope, then compare analysis windows and time blocks to assess sensitivity. A high fit R² alone does not establish convergence. If a suitable diffusion regime is not demonstrated, a definitive value should be withheld.

### Priority 3: Extend to temperature dependence where justified

Use the single-temperature checks to assess structural validity, density, and diffusion at other temperatures. If D values from multiple temperatures represent comparable structural states within the same phase, investigate the activation energy Eₐ using an Arrhenius analysis.

Conditions with substantial high-temperature framework flow should not automatically be combined with low-temperature solid-state conditions into one Eₐ fit. Room-temperature extrapolation and quantitative literature comparisons should follow these checks. Additional independent structures or system-size tests should be considered after the single-temperature issues have been clarified.

For this presentation, these analyses are described as next steps; multitemperature results, other-model results, and numerical D or Eₐ comparisons are outside the reporting scope.

## Suggested presentation script

> We prepared a 192-atom model of amorphous LZOC using a related literature structure as a starting point. To reduce dependence on the initial configuration, we performed high-temperature treatment and cooling, followed by structural and volume relaxation at room temperature. We then carried out a single-temperature MD simulation at 600 K using MACE and LAMMPS to examine the workflow and structural behavior. At 600 K, Li motion is expected to be easier to observe than at room temperature, while this temperature is at the lower end of our planned range. The protocol consisted of 10 ps of heating, 50 ps of NPT equilibration, and 200 ps of NVT production. Next, we will assess density and framework motion, in addition to temperature, before interpreting the Li MSD and diffusion coefficient. Today's report therefore focuses on structure preparation and the execution of the single-temperature MD calculation.
