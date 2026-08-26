# Allegro + LAMMPS

This directory defines an independent Allegro/NequIP LAMMPS workflow. It is
separate from MACE, SevenNet, and M3GNet environments.

## Status

The environment/build scripts are prepared, but a checkpoint trained for the
target elements is still required. The checkpoint must support Li, Y, Cl, Nb,
and O before it is used for Li₃YCl₆ or LiNbOCl₄.

## TSUBAME setup

```bash
source /gs/fs/tgj-26ICP/uf03782/yang/li-research/hpc/tsubame_26icp/config/yang_paths.sh
bash "$PROJECT_ROOT/hpc/tsubame_26icp/build/build_allegro_lammps.sh"
```

Compile a checkpoint on the same machine used for MD:

```bash
bash "$PROJECT_ROOT/hpc/tsubame_26icp/build/compile_allegro_model.sh" \
  "$MODELS_ROOT/allegro/model.ckpt" \
  "$MODELS_ROOT/allegro/model.nequip.pt2" cuda
```

The official AOTInductor target is `pair_allegro`. The LAMMPS executable must
be built with the `pair_nequip_allegro` interface and KOKKOS in the precision
required by that interface. Do not use an Allegro checkpoint whose element
map does not include the target composition.

## LAMMPS input pattern

```lammps
pair_style allegro
pair_coeff * * /path/to/model.nequip.pt2 Li Y Cl
```

The exact element order must match the checkpoint. Run a short energy/force
and 1 ps GPU smoke test before relaxation and production MD.
