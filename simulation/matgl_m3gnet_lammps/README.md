# MatGL/M3GNet + LAMMPS GPU test

This directory is an isolated benchmark for the native MatGL LAMMPS interface
to M3GNet. It does not replace the current MACE or SevenNet workflow.

The benchmark uses the explicit 240-atom Li₃YCl₆ 2×2×2 ordered model and runs
1,000 steps at 400 K. The input uses `pair_style matgl/kk`, which requires a
LAMMPS build with the ML-MATGL and Kokkos CUDA packages. The exported
TorchScript model must be produced with MatGL's `mgl create-lammps-model`
command; a model is deliberately not included in this repository.

The TSUBAME job exits with `BLOCKED` rather than silently falling back to a
different potential when the MatGL-enabled executable or model is missing.

## Reference

- [MatGL LAMMPS interface](https://github.com/materialyzeai/matgl/tree/main/lammps)
- [MatGL README](https://github.com/materialyzeai/matgl/blob/main/README.md)

Input data for the benchmark is generated from:
`structures/ordered/Li3YCl6/2x2x2/model_03/Li3YCl6_ordered_03_2x2x2.cif`.
