# Direction 2: alternative MLIP candidates

## Recommendation

For the current Li–Y–Cl–Nb–O benchmark, the first alternative to prioritize is
**SevenNet-0 / SevenNet-nano**, followed by a properly parallelized SevenNet
standard test. Both have already been run with the project structures in LAMMPS.
The current short benchmark gives approximately 69 steps/s for SevenNet-nano,
versus approximately 56.6 steps/s for M3GNet GPU. This is a speed result only;
it is not evidence that SevenNet is more accurate.

## Candidate ranking

| Priority | Candidate | LAMMPS status | Suitability for Li₃YCl₆ / LiNbOCl₄ | Decision |
|---:|---|---|---|---|
| 1 | SevenNet-nano | `e3gnn` tested | Directly covers the tested elements and is currently fast | Shortlist for screening |
| 2 | SevenNet standard / 7net-omni | `e3gnn/parallel` available; current run needs a fair parallel benchmark | Same chemistry; potentially better accuracy than nano, but speed depends strongly on MPI/GPU setup | Re-run with matched protocol |
| 3 | MACE-MP-0b3 small/medium | LAMMPS ML-IAP available | 89-element foundation model includes Li, Y, Cl, Nb and O | Accuracy cross-check, not current speed leader |
| 4 | Allegro, material-specific | LAMMPS plugin supports Kokkos/MPI/multi-GPU | Promising for fast production MD after training on this chemistry | Future option; requires DFT/AIMD training data |
| 5 | CHGNet | Primarily ASE-oriented; LAMMPS support exists but is not the current production path | Useful independent energy/force check, but not the first choice for this chloride workflow | Optional validation only |

## Why Allegro is not an immediate replacement

Allegro is designed as a strictly local E(3)-equivariant potential and has a
LAMMPS plugin with Kokkos, MPI and multi-GPU support. However, a reliable
Li–Y–Cl–Nb–O model would need material-specific training data. A universal
pretrained model that is both validated for these two electrolytes and directly
ready for production LAMMPS MD has not been established in this project.

## Required accuracy checks

For any model proposed as “faster and more accurate than M3GNet”, compare all
models on the same relaxed structures and the same trajectory protocol:

1. energy and force differences on identical snapshots;
2. relaxed lattice parameters and minimum interatomic distances;
3. structural stability during the same temperature schedule;
4. Li MSD and diffusion coefficient;
5. Arrhenius activation energy when multiple temperatures are available;
6. consistency with the reported experimental conductivity range.

Only after these checks should a model be described as more accurate. A larger
`steps/s` value alone only demonstrates a faster implementation for the tested
system size and backend.

## Practical decision

The immediate production order is:

```text
SevenNet-nano speed screening
        ↓
SevenNet standard fair parallel benchmark
        ↓
M3GNet GPU reference
        ↓
MACE-MPA-0 / MACE-MP-0b3 independent cross-check
        ↓
Allegro fine-tuning only if a material-specific dataset is available
```
