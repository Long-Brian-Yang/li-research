# Direction 2: Reproduction and transport analysis of fast halide electrolytes

## 1. Research question and scope

Direction 2 asks whether the reported high-conductivity halide and oxyhalide
frameworks can be reconstructed, relaxed, and analysed with a reproducible
atomistic workflow:

> **Can the Li sublattice of Li₃YCl₆ and LiNbOCl₄ sustain a physically stable,
> three-dimensional Li-ion migration network, and can the calculated transport
> trends be reconciled with the reported experimental conductivity?**

The project starts with reproduction, but the intended endpoint is a
structure-guided search rather than two isolated material case studies. The
two reference systems provide benchmark structures, polyhedral motifs,
ordering hypotheses, and transport data for the subsequent search. Large-scale
chemistry is deferred until the reference-system gates are passed.

The complete research logic is:

```text
high-conductivity papers and NGK data
        ↓ Step 1: identify space groups, polyhedral arrangements, and Li networks
composition-constrained substitutions
        ↓ Step 2: predict structure changes and construct explicit models
MD transport screening
        ↓ Step 3: rank candidates and state a clear go/no-go conclusion
```

## 2. Reference systems and experimental anchors

| System | Role in Direction 2 | Structural reference | Experimental anchor |
|---|---|---|---|
| **Li₃YCl₆** | High-voltage halide benchmark; tests vacancy/order sensitivity | Reported average structure is (P\bar{3}m1) (No. 164); explicit ordered models are required for MD | Asano *et al.*, 2018: room-temperature conductivity reported above 1 mS cm⁻¹ ([DOI](https://doi.org/10.1002/adma.201803075)) |
| **LiNbOCl₄** | Mixed-anion oxyhalide high-conductivity benchmark | Screenshot-derived reference is (Cmc2_1) (No. 36); O/Cl and Li occupancy must be made explicit | Tanaka *et al.*, 2023: (\sigma_{Li}\approx10.4) mS cm⁻¹ at room temperature ([DOI](https://doi.org/10.1002/anie.202217581)) |

The experimental values are pellet/EIS conductivities, whereas MD initially
provides a tracer diffusion coefficient and a Nernst–Einstein estimate. They
must be compared with explicit labels for temperature, cell size, simulation
time, conductivity definition, and uncertainty.

## 3. Non-negotiable structure policy

The screenshot-reconstructed CIFs are average crystallographic descriptions.
They contain partial occupancies and disorder. Expanding every listed site
creates an incorrect composition; in particular, direct expansion of the
Li₃YCl₆ screenshot gives a non-stoichiometric atom count. Such files are kept
for provenance and visual inspection only.

Every production input must satisfy all of the following:

- explicit full-occupancy atom list;
- correct elemental counts and charge-balanced nominal formula;
- periodic cell with finite coordinates and no duplicate atoms;
- minimum interatomic distance checked before dynamics;
- source, ordering choice, relaxation status, and commit recorded in a
  validation JSON file.

The current Li₃YCl₆ candidates are three distinct explicit Li/Y orderings.
They are independent structural hypotheses, not three copies of one proven
experimental configuration.

## 4. Current structure set

| System | Production-size input | Atoms | Purpose |
|---|---:|---:|---|
| Li₃YCl₆ models 01–03 | 2×2×4 | 480 each | Main finite-size and replica study; made by repeating the relaxed 2×2×2 cells once along (c) |
| LiNbOCl₄ | 2×2×2 | 2×2×2 model | Reference comparison at a manageable cell size |

For the Li₃YCl₆ 2×2×4 candidates, the validated counts are
Li₁₄₄Y₄₈Cl₂₈₈ and the shortest distances are approximately 2.39–2.46 Å.
These checks establish that the input is geometrically usable, but repeating a
relaxed cell is not equivalent to a fresh full 2×2×4 relaxation. A full
relaxation remains a higher-confidence follow-up before publication-quality
claims.

Structure files are organised under
[`structures/ordered/`](../../structures/ordered/). The generated 2×2×4 CIF,
XYZ, LAMMPS data, and validation files are in
[`structures/ordered/Li3YCl6/2x2x4/`](../../structures/ordered/Li3YCl6/2x2x4/).

## 5. Workflow and decision gates

```text
reference CIF / reported structure
        ↓
explicit occupancy and ordering model
        ↓  Gate 0: formula, geometry, provenance
MACE or DFT structural relaxation
        ↓  Gate 1: convergence, no collapse, sensible volume
supercell and periodic-boundary check
        ↓  Gate 2: finite-size setup and short stability run
300 K ML-MD: equilibration + production replicas
        ↓  Gate 3: stable T, energy, distances, MSD linearity
MSD → DLi → σNE; charge-current analysis where possible
        ↓  Gate 4: block uncertainty and method comparison
mechanism analysis and comparison with experiment
        ↓
reproduction report or explicitly documented failure mode
```

### Gate 0 — structure integrity

Before any potential is called, record:

| Check | Acceptance condition |
|---|---|
| Formula | Matches the intended ordered composition; no deleted atoms used to force stoichiometry |
| Occupancy | Every production site has occupancy 1.0 |
| Coordinates | All coordinates and cell entries are finite |
| Distances | No unphysical overlap; report the minimum periodic distance |
| Cell | Correct triclinic vectors, angles, and periodic boundary conditions |
| Provenance | Source CIF, ordering rule, generator, and validation commit recorded |

### Gate 1 — relaxation

Use MACE-MPA-0 or DFT to relax atomic positions first. A cell/volume pass may
follow, but the input, checkpoint, GPU, convergence criteria, and whether the
cell shape was fixed must be recorded. Retain all three Li₃YCl₆ orderings;
do not silently select the lowest-energy model before transport sensitivity is
known.

At minimum, inspect the relaxed structure for:

- force and energy convergence;
- unreasonable volume or density change;
- short Li–Cl, Y–Cl, Nb–O, or Nb–Cl contacts;
- loss of the intended framework or atom overlap;
- differences in relative energy between ordering models.

MACE-MPA-0 and NEP89 are screening tools here. Neither result alone validates
the experimental structure or proves the experimental conductivity.

### Gate 2 — cell-size and short stability check

The 2×2×4 Li₃YCl₆ cell is preferred because the parent (c) axis is short and
published Li₃YCl₆ MLMD work found conductivity and the superionic transition
to be sensitive to supercell size. The 2×2×2 LiNbOCl₄ cell is a practical
baseline because its parent (c) axis is already longer.

Before the long run, perform a 1,000–10,000-step GPU smoke test and verify:

- the potential recognises all elements;
- the run reaches the final step without an error;
- temperature control is active;
- no atoms leave the periodic cell in the stored trajectory;
- no sudden energy or distance catastrophe occurs.

## 6. Structure-guided discovery extension

The comments on the proposed Direction 2 clarify that a useful outcome is not
only a conductivity number. The project must also determine which structural
regions can be excluded or prioritised.

### Step 1 — identify the high-conductivity structural motifs

Organise the literature and NGK trial data by space group, stacking type,
polyhedral connectivity, Li-site topology, vacancy pattern, and anion
arrangement. Space group labels alone are insufficient: the same space group
can contain different Li bottlenecks and migration networks. Li₃YCl₆ and
LiNbOCl₄ are reference points for this map, not the complete candidate set.

### Step 2 — composition-constrained substitution and structure prediction

Apply the project’s element constraints while substituting cations or anions in
the identified motifs. A composition change can change the stable space group,
polyhedral arrangement, and Li-vacancy network, so the workflow must be able to
predict or enumerate plausible structures rather than reusing one CIF blindly.
Candidate models should be based on NGK data and the literature, followed by
explicit ordering, relaxation, and stability checks.

### Step 3 — MD screening and decision

Run MD only after the structural and stability gates. Rank candidates using
transport, mechanical/structural stability, synthesizability, and element
constraints. If the candidate set becomes large, use a documented surrogate or
descriptor model to prioritise MD. A negative result is still useful if it
clearly identifies a screened-out structural/compositional region. The final
report must state a conclusion or a go/no-go boundary; “a prediction model
could not be built” is not an adequate endpoint.

## 7. Production MD protocol

The first near-room-temperature production protocol is fixed as follows:

| Parameter | Value |
|---|---:|
| Ensemble | Langevin NVT |
| Temperature | 300 K |
| Timestep | 1 fs |
| Equilibration | 100 ps (100,000 steps) |
| Production | 1 ns (1,000,000 steps) |
| Coordinate output | every 1,000 steps (1 ps) |
| Thermodynamic output | every 1,000 steps |
| Independent replicas | Li₃YCl₆: 3; LiNbOCl₄: initially 1, then add replicas if needed |

The current TSUBAME entry point is
[`gpumd_nep89_300K_2x2x4.sh`](../../hpc/tsubame_26icp/gpumd_nep89_300K_2x2x4.sh).
The production run uses Li₃YCl₆ 2×2×4 models and the LiNbOCl₄ 2×2×2
benchmark. The same protocol should be used when comparing another potential.

### Why 1 ns is a first production run, not automatically the final one

At 300 K, Li motion can be substantially slower than at 400 K. One nanosecond
is long enough to test whether a stable linear MSD regime exists, but it does
not guarantee a small statistical error. Divide the production trajectory into
at least five blocks. If the block-to-block diffusion coefficient varies by
more than roughly 30%, extend that system to 3–5 ns rather than reporting a
single precise number.

## 8. Transport analysis

### 7.1 Li-only MSD and self-diffusion

Unwrap trajectories using fractional coordinates and the full triclinic cell.
Cartesian minimum-image unwrapping is unsafe for the skewed Li₃YCl₆ cell.
For Li atoms only, calculate:

\[
\mathrm{MSD}(t)=\left\langle\left|\mathbf r_i(t)-\mathbf r_i(0)\right|^2\right\rangle_i
\]

Fit only the demonstrably linear production interval. The three-dimensional
Einstein estimate is:

\[
D_{Li}=\frac{1}{6}\frac{d\,\mathrm{MSD}(t)}{dt}.
\]

Report the fit window, slope, number of Li atoms, number of frames, replica
mean, replica standard deviation, and block confidence interval.

### 7.2 Conductivity definitions

The initial estimate is Nernst–Einstein:

\[
\sigma_{NE}=\frac{n_{Li}q_{Li}^{2}D_{Li}}{k_BT}.
\]

This is a self-diffusion estimate and neglects distinct Li–Li correlations. It
must not be presented as the exact experimental conductivity. Where the code
and trajectory support it, also calculate a collective charge-current or
Green–Kubo conductivity and report the ratio

\[
H=\frac{\sigma_{collective}}{\sigma_{NE}}
\]

as a Haven/correlation factor. If only σ<sub>NE</sub> is available, label the result
`Nernst–Einstein estimate` in every table and figure.

### 7.3 Additional mechanism observables

For any candidate showing measurable transport, calculate or visualise:

- Li probability density and site occupation;
- directional MSD ((x,y,z)) and anisotropy;
- Li–Li and Li–framework radial distribution functions;
- Li coordination number and local bottleneck size;
- residence times and jump-length distributions;
- framework RMS displacement and minimum-distance history;
- correlation between local O/Cl or Y/Nb environments and Li jumps.

The goal is to explain *why* the two materials differ, not merely to rank two
numbers.

## 9. Temperature and experiment comparison

The simulation and experiment must be aligned before interpretation:

| Quantity | Experiment | Current ML-MD |
|---|---|---|
| Temperature | Usually near 298 K | 300 K production; earlier screening was 400 K |
| Sample | Pressed powder/pellet; bulk + grain-boundary/packing effects | Ideal periodic ordered crystal |
| Observable | EIS total ionic conductivity | Li tracer (D), then σ<sub>NE</sub> unless collective analysis is available |
| Disorder | Experimental average/disordered structure | One explicit ordering per replica |

The room-temperature benchmarks are approximately >1 mS cm⁻¹ for Li₃YCl₆ and
10.4 mS cm⁻¹ for LiNbOCl₄. A 400 K simulation value must not be compared
directly with these 298 K numbers. Arrhenius extrapolation may be shown only
with a measured or independently justified activation energy and with its
uncertainty.

## 10. Reproduction criteria

### Reproduction pass

A system passes the Direction 2 reproduction stage when:

1. all production structures have correct composition and remain stable;
2. independent orderings or replicas give a reproducible transport trend;
3. the MSD fit is linear over a documented window;
4. extending the fit window or block size does not change the conclusion;
5. the temperature and conductivity-definition mismatch with experiment is
   explicitly reported;
6. at least one independent potential or DFT short trajectory provides a
   force/structure sanity check.

Exact equality to the EIS value is not required. A defensible trend and a
quantified discrepancy are more informative than an apparently precise but
uncertain number.

### No-go or rework conditions

Stop and rebuild the model if any of the following occurs:

- the explicit model has the wrong composition or hidden partial occupancy;
- the structure collapses or develops nonphysical contacts;
- diffusion is inferred from a non-linear MSD plateau or a handful of jumps;
- only one short trajectory supports a strong conclusion;
- σ<sub>NE</sub> is reported as if it were collective or experimental conductivity;
- a generic potential gives extreme mobility without force/energy validation.

## 11. Data and reporting checklist

Each run directory must contain:

```text
model.cif or model.xyz
validation.json
run.in
thermo.out
dump.xyz
gpumd.out or lammps.log
msd.csv
diffusion_summary.json
figure_msd.png
figure_thermo.png
```

The final comparison table must include:

```text
material | ordering_id | supercell | potential | T_K | equilibration_ps |
production_ns | n_Li | fit_window_ps | D_Li_cm2_s | sigma_NE_mS_cm |
sigma_collective_mS_cm | block_std | structure_status | confidence | source
```

Every reported value must be tagged as `experimental`, `calculated`, or
`target`, and must include temperature, method, units, and source.

## 12. Immediate action list

1. Finish the current 300 K, 1 ns GPUMD/NEP89 run and verify all four exit
   statuses.
2. Run the same MSD/block analysis on the corrected triclinic trajectories.
3. Compare the 2×2×4 Li₃YCl₆ results with the earlier 2×2×2 400 K screening
   only as a size/temperature sensitivity study.
4. Add at least two LiNbOCl₄ replicas if its single-run uncertainty is large.
5. Cross-check representative configurations with MACE-MPA-0 and, where
   possible, DFT energies/forces.
6. Report σ<sub>NE</sub>, not “ionic conductivity”, until collective charge
   correlations and experimental comparability have been addressed.

## 13. Repository entry points

- [`structures/`](../../structures/) — ordered CIF/XYZ/LAMMPS inputs and
  validation metadata;
- [`simulation/gpumd_nep89/`](../../simulation/gpumd_nep89/) — NEP89 protocol,
  analysis notes, and figures;
- [`simulation/mace_mpa0/`](../../simulation/mace_mpa0/) — MACE-MPA-0 and
  LAMMPS conversion/relaxation workflow;
- [`hpc/tsubame_26icp/`](../../hpc/tsubame_26icp/) — TSUBAME job scripts;
- [`docs/literature/papers_zh.md`](../literature/papers_zh.md) and
  [`docs/literature/papers_ja.md`](../literature/papers_ja.md) — bilingual
  literature notes and DOI-linked experimental context.
