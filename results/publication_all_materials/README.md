# Final publication figure package

This directory contains the standardized figures for both materials and all three models.

## Materials and principal temperatures

- Li₃YCl₆: 600 K for local-structure and thermodynamic figures; 400/600/800/1000 K for MSD and Arrhenius analysis.
- LiNbOCl₄: 800 K for local-structure and thermodynamic figures; 600/800/1000/1200 K for MSD and Arrhenius analysis.

The LiNbOCl₄ Arrhenius panel follows the Li₃YCl₆ plotting logic. Model diffusion coefficients are converted to conditional Nernst–Einstein conductivity using the 224-atom model cell (32 Li; 5127.4186 Å³), and the ordinate is $\ln(\sigma_{\mathrm{NE}}T)$. The experimental reference from Tanaka et al. is anchored at the reported room-temperature conductivity of 10.4 mS cm⁻¹ and extended with the reported $E_a\approx0.24$ eV ([DOI](https://doi.org/10.1002/anie.202217581)). It is an experimental conductivity reference, not an experimental tracer-diffusion curve.

## Figure groups

- `main/`: individual and combined four-temperature MSD figures.
- `arrhenius/`: all-model Arrhenius fits.
- `arrhenius/Arrhenius_all_materials_all_models.png`: combined 1×2 Arrhenius figure for both materials.
- `rdf/`: Li–Cl, framework-cation–Cl, and Cl–Cl RDF comparisons.
- `coordination/`: Li–Cl coordination distributions.
- `thermodynamics/`: model-separated temperature, energy, and pressure stability panels.

LiNbOCl₄ transport estimates use all completed MSD trajectories for each model and temperature, with a common 20–500 ps fit. Re-executions using the same initial-velocity seed are averaged within that seed; distinct seeds are then weighted equally. The corresponding full per-trajectory and summary data are `supplementary/source_data/LiNbOCl4_trajectory_diffusion.csv` and `supplementary/source_data/LiNbOCl4_D_Ea_summary.csv`.

All newly generated figures use the common white-background style with consistent typography and line widths. Model colors are MACE-MPA-0 (blue), SevenNet-nano (green), and M3GNet (red). The LiNbOCl₄ analysis stops with an error if any model–temperature group has no trajectory, rather than silently omitting the group.
