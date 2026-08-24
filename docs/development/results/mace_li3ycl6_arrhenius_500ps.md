# MACE-MPA-0: Li₃YCl₆ 500 ps composite analysis

## Protocol

- Explicit ordered Li₃YCl₆ model 03, 240 atoms.
- LAMMPS + MACE legacy GPU interface, 1 fs timestep.
- 50 ps equilibration + 500 ps production at each temperature.
- MSD fit window: 100–500 ps of production.
- Selected trajectories: 400, 500, 600, 700, 800 and 1000 K.

## LAMMPS/trajectory cross-check

LAMMPS `compute msd` was used as the primary output where an `*_msd.dat` file
was saved. The trajectories were independently read in a repaired MDAnalysis
environment (NumPy 1.26.4 + MDAnalysis 2.7.0); the LAMMPS `xu/yu/zu` columns
were then used for the independent unwrapped Li-MSD calculation. This avoids
mixing wrapped and unwrapped coordinates.

| Temperature | LAMMPS D (cm² s⁻¹) | Trajectory D (cm² s⁻¹) | Check |
|---:|---:|---:|---|
| 400 K | 2.704 × 10⁻⁶ | 2.704 × 10⁻⁶ | identical |
| 500 K | not saved | 2.734 × 10⁻⁶ | trajectory only |
| 600 K, latest | 6.996 × 10⁻⁶ | 6.996 × 10⁻⁶ | identical |
| 700 K | not saved | 1.083 × 10⁻⁵ | trajectory only |
| 800 K | 1.959 × 10⁻⁵ | 1.959 × 10⁻⁵ | identical |
| 1000 K | 3.736 × 10⁻⁵ | 3.736 × 10⁻⁵ | identical |

The original 600 K trajectory is also complete, but gives
`D = 9.331 × 10⁻⁶ cm² s⁻¹`, compared with `6.996 × 10⁻⁶ cm² s⁻¹` for the
latest 600 K run. This is a 33% replica-to-replica difference and is retained
as a trajectory-history uncertainty.

## Six-temperature Arrhenius fit

Using

\[
D(T)=D_0\exp\left(-\frac{E_a}{k_BT}\right),
\]

the six selected trajectory values give:

| Quantity | Composite result |
|---|---:|
| Activation energy, `E_a` | **0.159 eV** |
| Prefactor, `D_0` | **1.78 × 10⁻⁴ cm² s⁻¹** |
| Arrhenius `R²` | **0.900** |
| Extrapolated `D(300 K)` | **3.80 × 10⁻⁷ cm² s⁻¹** |

The previous four-point result (`E_a = 0.148 eV`) used only temperatures with
saved LAMMPS MSD files. It is superseded by this six-temperature trajectory
analysis.

## Comparison with the experimental reference

The project literature/presentation reference lists an experimental activation
energy of approximately **0.40 eV** for Li₃YCl₆. The composite MACE value is
lower by about **0.241 eV** (about **60% lower**), indicating a weaker
temperature dependence than the experimental reference.

Using the explicit model cell (72 Li atoms; volume about 5282.8 Å³) and the
Nernst–Einstein conversion, the extrapolated MACE value is approximately
**0.32 mS cm⁻¹ at 300 K**. This is below the 0.51 mS cm⁻¹ value shown in the
presentation table and below the broader literature benchmark of `>1 mS
cm⁻¹`. This is a `σ_NE` estimate, not a collective Green–Kubo or pressed-pellet
EIS conductivity.

The result is sensitive to ordering, finite-size effects, replica history, the
generic-potential approximation and the MSD fit window. It is suitable for
internship workflow validation, not publication-level validation of MACE
accuracy.
