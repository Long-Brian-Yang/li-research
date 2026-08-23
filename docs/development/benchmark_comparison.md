# TSUBAME benchmark comparison

Latest short benchmark records from the `tgj-26ICP` H100 environment (24 August
2026). LAMMPS tests use the 240-atom Li₃YCl₆ structure, one MPI rank, one GPU,
100 warm-up steps followed by 1,000 timed steps unless noted otherwise. Higher
`steps/s` means faster execution.

## Detailed result table

The table below records the latest available result for every one of the eight
model/interface entries. For LAMMPS, the timed value is the final 1,000-step
segment after a 100-step warm-up on the 240-atom Li₃YCl₆ ordered benchmark
structure. The reported wall time is the LAMMPS timed-segment loop time.

| Model | Interface | Structure / atoms | GPU / MPI | Warm-up + timed steps | Timed speed | Timed loop time | Result location | Comparability |
|---|---|---:|---|---:|---:|---:|---|---|
| GPUMD + NEP89 | GPUMD CUDA | relaxed Li₃YCl₆ and LiNbOCl₄; protocol-specific | H100 / GPUMD | 1,000-step smoke | ≈1,212 / ≈1,167 steps/s | not recorded in the same format | `benchmarks/gpumd/` | provisional; not the unified LAMMPS protocol |
| SevenNet-nano | LAMMPS `e3gnn` | Li₃YCl₆ / 240 | 1 GPU / 1 MPI rank | 100 + 1,000 | **69.261 steps/s** | 14.4382 s | `results/benchmark/sevennet_nano/` | directly comparable to other 1-GPU LAMMPS tests |
| M3GNet | LAMMPS `matgl/kk` | Li₃YCl₆ / 240 | H100 / 1 MPI rank | 100 + 1,000 | **56.621 steps/s** | 17.6612 s | `m3gnet_matgl/matgl_m3gnet_benchmark/` | GPU confirmed by `pair_matgl/kk: model on cuda` |
| MACE-MP-0b2-small | LAMMPS ML-IAP/Kokkos | Li₃YCl₆ / 240 | H100 / 1 MPI rank | 100 + 1,000 | **53.124 steps/s** | 18.8239 s | `benchmarks/lammps/mace_mliap_gpu/mace_mp0b2_small/` | canonical Python 3.10/Kokkos CUDA |
| MACE-MPA-0-medium | LAMMPS ML-IAP/Kokkos | Li₃YCl₆ / 240 | H100 / 1 MPI rank | 100 + 1,000 | **39.176 steps/s** | 25.5261 s | `benchmarks/lammps/mace_mliap_gpu/mace_mpa0_medium_canonical/` | canonical ML-IAP; legacy baseline 10.316 steps/s |
| MACE-MP-0b3-medium | LAMMPS ML-IAP/Kokkos | Li₃YCl₆ / 240 | H100 / 1 MPI rank | 100 + 1,000 | **36.938 steps/s** | 27.0727 s | `benchmarks/lammps/mace_mliap_gpu/mace_mp0b3_medium_canonical/` | canonical Python 3.10/Kokkos CUDA |
| SevenNet standard / 7net-omni | LAMMPS `e3gnn/parallel` | Li₃YCl₆ / 240 | 1 GPU / 1 MPI rank | 100 + 1,000 | **8.579 steps/s** | 116.567 s | `benchmarks/lammps/sevennet_parallel/np1/` | CUDA and CUDA-aware MPI verified |
| M3GNet | LAMMPS native `matgl` | Li₃YCl₆ / 240 | CPU | 100 + 1,000 | **3.285 steps/s** | not retained in current summary | archived CPU benchmark | CPU baseline; not a GPU comparison |

For the LAMMPS runs, `steps/s` is the primary comparison unit. The equivalent
`katom-step/s` values are available in each `summary.txt` or `lammps.log`; they
are not interchangeable with GPUMD's atom-step/s output without applying the
same atom-count and timing definitions.

## Complete eight-entry benchmark matrix

The complete comparison set for this project contains eight tested entries:

| Entry | Model | Runtime/interface | Required result |
|---:|---|---|---|
| 1 | MACE-MPA-0 medium | LAMMPS ML-IAP/Kokkos | 39.176 steps/s |
| 2 | MACE-MP-0b3 medium | LAMMPS ML-IAP/Kokkos | 36.938 steps/s |
| 3 | MACE-MP-0b2-small | LAMMPS ML-IAP/Kokkos | 53.124 steps/s |
| 4 | SevenNet standard | LAMMPS `e3gnn/parallel` | 8.579 steps/s |
| 5 | SevenNet-nano | LAMMPS `e3gnn` | 69.261 steps/s |
| 6 | NEP89 | GPUMD CUDA | approximately 1212 steps/s |
| 7 | M3GNet | LAMMPS native `matgl` CPU | 3.285 steps/s |
| 8 | M3GNet | LAMMPS `matgl/kk` GPU | 56.621 steps/s |

The model/interface count is therefore eight. MACE-MPA-0 now has a canonical
ML-IAP/Kokkos result; its previous 10.316 steps/s legacy result remains only as
an interface baseline and is not used in the main ranking.

## Interpretation

The current speed ranking is approximately:

```text
GPUMD/NEP89  >>  SevenNet-nano  >  M3GNet GPU
             >  MACE-MP-0b2-small  >  MACE-MPA-0-medium
             >  MACE-MP-0b3-medium > SevenNet standard
             >> M3GNet CPU
```

The SevenNet standard value above supersedes the earlier 8.336 steps/s
diagnostic. A 2-GPU retest reached 6.314 steps/s on the same 240-atom system;
this is a valid parallel run but is slower because the system is too small for
multi-GPU domain decomposition. See
[the full SevenNet retest](sevennet_parallel_retest_2026-08-24.md).

The MACE small result is an additional model-size diagnostic, not a replacement
for the eight-entry comparison set. The official foundation repository
provides MACE-MP-0b3-medium and MACE-MP-0b2-small; it does not provide an
official MACE-MP-0b3-small checkpoint.

The GPUMD value should remain marked provisional until it is rerun with the
same warm-up and timed-step protocol as the LAMMPS jobs. Interface comparisons
must also distinguish model size, neighbor-list policy, MPI decomposition and
whether the result is a GPU or CPU run.
