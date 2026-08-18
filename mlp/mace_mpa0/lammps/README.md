# MACE-MPA-0 + LAMMPS workflow

This directory is the LAMMPS backend for the Direction 2 reproduction study.
It is intended for **ordered** Li₃YCl₆ and LiNbOCl₄ models after the partial
occupancies in the screenshot-derived CIFs have been resolved.

## Why this workflow

Use ASE/MACE for a short sanity check and structure preparation, then use
LAMMPS for longer GPU trajectories.  The MACE-MPA-0 checkpoint is not read by
LAMMPS as-is: it must first be converted to the LAMMPS ML-IAP format.

## 1. Install and convert the model

Install MACE in the environment used for conversion:

```bash
python -m pip install mace-torch ase
```

Convert a downloaded MACE-MPA-0 checkpoint (the exact checkpoint filename may
vary with the MACE release):

```bash
python mace/cli/create_lammps_model.py medium-mpa-0.model \
  --format=mliap
```

The converter writes the corresponding `*-mliap_lammps.pt` file next to the
checkpoint; use that generated filename in the LAMMPS input.

Keep the conversion environment and the LAMMPS runtime compatible.  For GPU
execution, build/run on the same NVIDIA architecture when possible.

The repository also includes a wrapper:

```bash
bash mlp/mace_mpa0/lammps/convert_model.sh /path/to/mace-mpa-0-medium.model
```

## 2. Build LAMMPS

Use a recent LAMMPS build with ML-IAP, Python, MPI, and Kokkos enabled.  The
MACE ML-IAP interface is still evolving, so record the LAMMPS commit, CUDA
version, GPU model, MACE version, and model checksum for every production run.

The input templates use `pair_style mliap unified`:

```text
pair_style mliap unified medium-mpa-0-mliap_lammps.pt 0
```

The `pair_coeff` element order must exactly match the atom-type order in the
LAMMPS data file:

| System | `pair_coeff` order |
|---|---|
| Li₃YCl₆ | `Li Y Cl` |
| LiNbOCl₄ | `Li Nb O Cl` |

## 3. Prepare a LAMMPS data file

```bash
python mlp/mace_mpa0/lammps/prepare_data.py \
  runs/mace_mpa0/Li3YCl6_ordered_01_relaxed.cif \
  --output runs/mace_mpa0/Li3YCl6_ordered_01.data \
  --elements Li Y Cl
```

The converter rejects partial occupancies and validates that all requested
elements are present.  It is a preparation utility, not a substitute for
checking the ordered structure chemically.

Repeat with the Direction 2 oxyhalide model using `--elements Li Nb O Cl`.
The screenshot-reconstructed CIFs in this repository are intentionally
rejected because they contain partial occupancies; replace them with explicit
ordered CIFs first.

## 4. Run

Edit the `read_data`, model path, and output paths in `in.minimize` and
`in.md`.  For NVIDIA/Kokkos builds, a typical launch is:

```bash
lmp -k on g 1 -sf kk -pk kokkos newton on neigh half -in in.md
```

Use `timestep 0.001` in `units metal` (1 fs).  Start with a short 300–500 K
test, inspect energy/volume/structure, and only then extend the trajectory.
The first conductivity estimate is exploratory and should be checked against
DFT spot calculations and an independent potential.

Use the material-specific inputs:

```bash
lmp -k on g 1 -sf kk -pk kokkos newton on neigh half \
  -in mlp/mace_mpa0/lammps/in.minimize.LiNbOCl4
lmp -k on g 1 -sf kk -pk kokkos newton on neigh half \
  -in mlp/mace_mpa0/lammps/in.md.LiNbOCl4
```

For Li₃YCl₆, use `in.minimize` and `in.md`.  Change `read_data` and the model
path if files are stored outside the working directory.

## 5. Estimate Li self-diffusion

After MD, the dump files contain unwrapped Li coordinates (`xu yu zu`).  The
included analyzer fits the long-time slope of the Li self-MSD:

```bash
python mlp/mace_mpa0/lammps/msd_diffusion.py \
  Li3YCl6_ordered_01_mace_md.lammpstrj \
  --li-type 1 \
  --output Li3YCl6_msd.txt
```

LAMMPS atom type 1 is Li when `prepare_data.py` is called with `Li` first.
The resulting self-diffusion coefficient is an initial screening value; a
collective conductivity calculation needs an additional charge-current or
Einstein-Helfand analysis and finite-size/convergence checks.

## Limitations

- The current Mac workspace has no CUDA device and no installed MACE package;
  no MACE or LAMMPS trajectory is claimed here.
- Foundation-model results are not automatically validated for every ordered
  halide/oxyhalide configuration.  Check forces, cell stability, and chemical
  plausibility before interpreting Li diffusion.
- Partial-occupancy CIFs must never be sent directly to LAMMPS.

## TSUBAME execution (26ICP)

The intended test environment is the TSUBAME project/group **26ICP**.  It is
separate from the original Ishikawa account and filesystem; do not copy the
old `/gs/fs/tga-ishikawalab/...` paths into these inputs.

Copy this directory and the ordered structures into a 26ICP working directory,
load the MACE-compatible Python environment and the Kokkos-enabled LAMMPS
module provided by your group, then submit the job body with the TSUBAME queue
and resource options required for your installation.  The job body itself is:

```bash
bash mlp/mace_mpa0/lammps/job_tsubame_26icp.sh in.md
# or
bash mlp/mace_mpa0/lammps/job_tsubame_26icp.sh in.md.LiNbOCl4
```

The script prints the host, project label, LAMMPS executable, and input file
before starting.  Confirm that the scheduler allocation is charged to 26ICP
and that `lmp -h` reports ML-IAP and Kokkos before submitting a long run.  The
exact `pjsub` resource-group/queue flags are intentionally left to the local
TSUBAME configuration rather than hard-coding Ishikawa-specific settings.
