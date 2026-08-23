# Unified benchmark status

The complete comparison set contains eight tested model/interface entries: three
MACE entries, two SevenNet entries, one GPUMD/NEP89 entry, and M3GNet in CPU and
GPU modes. MACE-MPA-0 is now benchmarked through the canonical ML-IAP/Kokkos
CUDA interface; its older legacy result is retained only as a diagnostic baseline.

## Common structure

The reference structure is the 240-atom Li₃YCl₆ ordered model after MACE-based
cell/ionic relaxation:

`Li3YCl6_03_mace_cell_relaxed.data`

This file is the common speed-benchmark geometry. It must be converted to XYZ
for GPUMD; the conversion must preserve atom order, cell vectors, composition,
and the relaxation coordinates.

## Current status

| Backend | Relaxed input | Benchmark status | Note |
|---|---:|---|---|
| GPUMD + NEP89 | relaxed XYZ generated from the converged LAMMPS dump | completed | production speed: 311,304 atom·step/s |
| MACE-MP-0b3 medium + ML-IAP | yes | completed | canonical Python 3.10/Kokkos CUDA rerun: 36.938 steps/s |
| MACE-MP-0b2-small + ML-IAP | yes | completed | canonical Python 3.10/Kokkos CUDA rerun: 53.124 steps/s |
| MACE-MPA-0 medium + ML-IAP | yes | completed | canonical Python 3.10/Kokkos CUDA rerun: 39.176 steps/s; legacy baseline was 10.316 steps/s |
| SevenNet standard / 7net-omni | yes | completed | official `e3gnn/parallel`; 8.579 steps/s on 1 GPU, 6.314 steps/s on 2 GPUs; CUDA + CUDA-aware MPI verified |
| SevenNet-nano | yes | completed | unified run completed |
| M3GNet CPU | yes, restarted | completed | 3.285 steps/s for the 1000-step timed section |
| M3GNet GPU | yes | completed | patched TorchScript; 56.621 steps/s for the 1000-step timed section |

## Relaxation versus speed benchmark

The speed comparison should use one identical relaxed geometry for all models.
It is not the same as a physical diffusion study in which every potential is
allowed to relax its own structure. That second study is a separate phase and
requires model-specific relaxation, stability checks, and production MD.

## Required before calling the eight-entry set complete

1. Store each model's executable, model checksum, input, stdout/stderr, and
   performance line in a timestamped environment directory.
