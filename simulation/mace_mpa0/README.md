# MACE-MPA-0 workflow

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
executable, loads the converted checkpoint, minimizes the two provisional
structures, and runs a short 200-step NVT trajectory for each system. Submit it
from the group-disk workspace with:

```bash
qsub -g tgj-26ICP hpc/tsubame_26icp/build_and_test_mace.sh
```

The successful test used job `8437131` and produced both LAMMPS trajectories and
final data files. These are software-pipeline checks only: the input CIFs were
reconstructed from screenshots and contain partial occupancies, so the output
must not be used as a conductivity result until explicit ordered CIFs are
provided and validated.
