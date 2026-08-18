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

The current workspace does not yet have `mace-torch` installed. The scripts therefore have not been executed against the model checkpoint.

## Relaxation

```bash
python mlp/mace_mpa0/relax.py \
  structures/ordered/Li3YCl6_ordered_01.cif \
  --output runs/mace_mpa0/Li3YCl6_ordered_01_relaxed.cif
```

The script uses `medium-mpa-0` explicitly and relaxes both atomic positions and the cell.

## Exploratory MD

```bash
python mlp/mace_mpa0/md.py \
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

