# Li₃YCl₆ priority analyses (600 K)

All plots use the formal TSUBAME-synchronized LAMMPS trajectories for MACE-MPA-0 (600 K/R3) and M3GNet (600 K/R2). MDAnalysis is used for trajectory reading; unwrapped coordinates are used for MSD/diffusion and periodic minimum-image distances for RDF.

- `Li3YCl6_directional_MSD_600K.png`: x/y/z and total MSD.
- `Li3YCl6_diffusion_block_averaging_600K.png`: five-block D uncertainty.
- `Li3YCl6_RDF_600K.png`: Li–Cl and Y–Cl RDF.
- `Li3YCl6_thermo_cell_stability_600K.png`: temperature/energy/pressure/cell stability proxies from `md.log`.
- `Li3YCl6_jump_and_van_hove_600K.png`: displacement and self Van-Hove distributions.

These are supplementary analyses; the primary Arrhenius/MSD figures remain in the parent `plots/` directory.
