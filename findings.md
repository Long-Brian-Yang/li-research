# Project findings

## Computational scope

- Direction 2 only: Li₃YCl₆ and LiNbOCl₄.
- Direction 3 chemistry-development material is out of the current execution
  scope.
- Direction 2 now includes a later structure-guided discovery extension:
  structural motif mapping → constrained substitution/structure prediction →
  MD screening and an explicit go/no-go conclusion.
- Literature notes remain bilingual; computational documentation is English.

## Structures

- The screenshot-derived CIFs are average/disordered crystallographic models.
- Li₃YCl₆ contains partial Li/Y occupancies; expanding all sites gives an
  incorrect composition.
- Production MD therefore uses explicit ordered models and treats the three
  Li₃YCl₆ orderings as separate replicas.

## NEP89

- 300 K runs exist for Li₃YCl₆_01/_02/_03 and LiNbOCl₄.
- Official GPUMDkit plots are in `simulation/gpumd_nep89/figures/300K_2x2x4_gpumdkit/`.
- Primary fitting window is 100–300 ps; window sensitivity is recorded in
  `window_sensitivity_300K_2x2x4.csv`.
- The 300 K NEP89 values are screening estimates and are much lower than the
  paper benchmarks.

## MACE

- MACE-MPA-0 + LAMMPS GPU trajectories were previously produced at 400 K, but
  the first batches stopped at 48–75 ps despite the intended 100 ps.
- New jobs 8441077–8441080 were submitted independently with 14 h walltime.
- Do not compare the current 400 K MACE values directly with 300 K NEP89 until
  a matched protocol is available.

## Interpretation rules

- `D_Li` is tracer/self-diffusion.
- `sigma_NE` is a Nernst–Einstein estimate and is not collective Green–Kubo or
  pressed-powder EIS conductivity.
- Experimental discrepancy cannot be assigned solely to the fit window; model,
  ordering, temperature, finite size, and conductivity definition all matter.
