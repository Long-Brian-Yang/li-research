# MACE-MPA-0 workflow

## Completed 500 ps Li₃YCl₆ reference analysis

The completed 50 ps equilibration + 500 ps production runs for the selected
ordered Li₃YCl₆ model are summarized in
[`results/mace_li3ycl6_arrhenius_500ps.md`](results/mace_li3ycl6_arrhenius_500ps.md).
The 400/600/800/1000 K Arrhenius fit gives `E_a = 0.148 eV`,
`D_0 = 1.71 × 10⁻⁴ cm² s⁻¹`, and an extrapolated `D(300 K) = 5.56 × 10⁻⁷
cm² s⁻¹`. These are preliminary generic-MACE screening results and are not
treated as a quantitative reproduction of the experimental conductivity.

This directory configures the explicit MACE foundation checkpoint `medium-mpa-0` (MACE-MPA-0) for the Direction 2 reproduction study.

## Scope

- Relax ordered Li₃YCl₆ and LiNbOCl₄ structures.
- Run short NVT exploratory MD on `2×2×2` supercells.
- Do not use the screenshot-reconstructed CIFs directly for production MD: they contain partial occupancies and must first be converted into explicit ordered models.

## Install

In a clean environment:

```bash
python -m pip install mace-torch ase
```

The TSUBAME test workspace uses `mace-torch==0.3.13` to convert the official
`mace-mpa-0-medium.model` checkpoint into the legacy LAMMPS TorchScript format.
The resulting CPU LAMMPS executable is built from the ACEsuit `mace` branch.

## Relaxation

```bash
python simulation/mace_mpa0/relax.py \
  structures/ordered/Li3YCl6_ordered_01.cif \
  --output runs/mace_mpa0/Li3YCl6_ordered_01_relaxed.cif
```

The script uses `medium-mpa-0` explicitly and relaxes both atomic positions and the cell.

## Exploratory MD

```bash
python simulation/mace_mpa0/md.py \
  runs/mace_mpa0/Li3YCl6_ordered_01_relaxed.cif \
  --output-dir runs/mace_mpa0/Li3YCl6_ordered_01_md \
  --supercell 2 2 2 \
  --temperature 500 \
  --steps 25000
```

This is an exploratory trajectory, not a final conductivity result. Report the model name, temperature, timestep, supercell, trajectory length, and whether the result is Nernst–Einstein or collective conductivity.

## Required validation

Before trusting a trajectory:

1. Compare MACE relaxed geometry with DFT spot checks.
2. Confirm the model does not collapse the framework.
3. Compare MACE and DFT forces on sampled snapshots.
4. Repeat with at least two ordered occupancy models.
5. Cross-check the most important result with a second potential or DFT-AIMD.

## TSUBAME LAMMPS smoke test

The reproducible batch script is
`hpc/tsubame_26icp/build_and_test_mace.sh`. It builds the MACE-enabled LAMMPS
executable, loads the converted checkpoint, minimizes two explicit ordered
structures, and runs a short 200-step NVT trajectory for each system. Submit it
from the group-disk workspace with:

```bash
qsub -g tgj-26ICP hpc/tsubame_26icp/build_and_test_mace.sh
```

The earlier job `8437131` used screenshot-reconstructed provisional data and must
be discarded: the overlap-removal workaround changed the Li₃YCl₆ composition.
The current script refuses to run unless `Li3YCl6_ordered.data` and
`LiNbOCl4_ordered.data` are present. These ordered inputs must be generated from
the original CIFs (or explicitly documented order/disorder models), not by
deleting atoms from the provisional files.
