# Final publication figure package

This directory contains the standardized figures for both materials and all three models.

## Materials and principal temperatures

- Li₃YCl₆: 600 K for local-structure and thermodynamic figures; 400/600/800/1000 K for MSD and Arrhenius analysis.
- LiNbOCl₄: 800 K for local-structure and thermodynamic figures; 600/800/1000/1200 K for MSD and Arrhenius analysis.

The LiNbOCl₄ Arrhenius panel includes the experimental reference trend from Tanaka et al. (room-temperature conductivity 10.4–10.7 mS cm⁻¹, reported (E_a\approx0.24) eV; [DOI](https://doi.org/10.1002/anie.202217581)). The dashed line is the Arrhenius trend reconstructed from those reported values, not a fit to the present MD points.

## Figure groups

- `main/`: individual and combined four-temperature MSD figures.
- `arrhenius/`: all-model Arrhenius fits.
- `arrhenius/Arrhenius_all_materials_all_models.png`: combined 1×2 Arrhenius figure for both materials.
- `rdf/`: Li–Cl, framework-cation–Cl, and Cl–Cl RDF comparisons.
- `coordination/`: Li–Cl coordination distributions.
- `thermodynamics/`: model-separated temperature, energy, and pressure stability panels.

All newly generated figures use the common white-background style with consistent typography and line widths. Model colors are MACE-MPA-0 (blue), SevenNet-nano (green), and M3GNet (red). Missing trajectories are skipped rather than replaced with fabricated data.
