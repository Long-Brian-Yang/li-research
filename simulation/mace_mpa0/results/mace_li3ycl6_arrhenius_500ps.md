# MACE-MPA-0: Li₃YCl₆ 500 ps Arrhenius analysis

## Protocol

- Structure: explicit ordered Li₃YCl₆ model 03, 240 atoms.
- MD: LAMMPS + MACE legacy GPU interface, 1 fs timestep.
- Each completed run: 50 ps equilibration + 500 ps production.
- Arrhenius fit: total Li MSD, 100–500 ps production window.
- Temperatures with complete MSD files: 400, 600, 800 and 1000 K.

## Fit

Using

\[
D(T)=D_0\exp\left(-\frac{E_a}{k_BT}\right),
\]

the four-point fit gives:

| Quantity | MACE result |
|---|---:|
| Activation energy, `E_a` | **0.148 eV** |
| Prefactor, `D_0` | **1.71 × 10⁻⁴ cm² s⁻¹** |
| Arrhenius `R²` | **0.957** |
| Extrapolated `D(300 K)` | **5.56 × 10⁻⁷ cm² s⁻¹** |

The 500 K and 700 K trajectories were produced, but complete MSD files were
not available in the current result directory and were therefore not included
in this fit.

## Comparison with the experimental reference

The project literature/presentation reference lists an experimental activation
energy of approximately **0.40 eV** for Li₃YCl₆. The MACE value is therefore
lower by about **0.252 eV** (about **63% lower**). This means that the present
generic MACE model predicts a weaker temperature dependence than the
experimental reference; it should not be described as a quantitative match.

The literature notes report a room-temperature conductivity benchmark above
1 mS cm⁻¹, while the presentation table also contains `5.1 × 10⁻⁴ S cm⁻¹`
(`0.51 mS cm⁻¹`). Using the explicit model cell (72 Li atoms; volume about
5282.8 Å³) and the Nernst–Einstein conversion, the extrapolated MACE value is
approximately **0.47 mS cm⁻¹ at 300 K**. It is close to the 0.51 mS cm⁻¹
presentation value, but remains below the broader `>1 mS cm⁻¹` literature
benchmark. This is a `σ_NE` estimate, not a collective Green–Kubo or pressed
pellet EIS conductivity.

The result is sensitive to ordering, finite-size effects, the generic-potential
approximation and the MSD fit window. It is suitable for the internship
workflow validation, not as a publication-level validation of MACE accuracy.
