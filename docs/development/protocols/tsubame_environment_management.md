# TSUBAME benchmark environment management

The canonical directory and naming rules are defined in
[`project_layout.md`](project_layout.md). This file records environment details
without introducing a second path convention.

The seven backends are kept as separate environments. A benchmark result is
valid only when the environment, model file, executable, structure checksum and
input protocol are recorded together.

## Common reference

- Structure: `Li3YCl6_03_mace_cell_relaxed.data`
- Composition: Li₃YCl₆, 240 atoms
- Relaxation: completed before benchmark; the same geometry is converted to
  each backend's native format
- MD protocol: 400 K, 1 fs, 100 warm-up steps, reset, 1000 timed steps
- Thermo: step, temperature, potential/kinetic/total energy, pressure

## Backend isolation

| Backend | Environment | Executable/interface | Model | Structure format |
|---|---|---|---|---|
| GPUMD | none (compiled CUDA executable) | GPUMD CUDA | NEP89 | GPUMD XYZ |
| MACE-MP-0b3 medium | `yang/envs/mace_env` | LAMMPS ML-IAP/Kokkos | MACE-MP-0b3 | LAMMPS data |
| MACE-MPA-0 medium | `yang/envs/mace_env` | LAMMPS ML-IAP/Kokkos | MACE-MPA-0 | LAMMPS data |
| SevenNet standard | `yang/envs/sevennet_env` | LAMMPS `e3gnn/parallel` | 7net-omni | LAMMPS data |
| SevenNet-nano | `yang/envs/sevennet_env` | LAMMPS `e3gnn` | 7net-nano | LAMMPS data |
| M3GNet CPU | `yang/envs/matgl_env` | MatGL LAMMPS `matgl` | M3GNet TorchScript | LAMMPS data |
| M3GNet GPU | `yang/envs/matgl_env` | MatGL LAMMPS `matgl/kk` | M3GNet TorchScript | LAMMPS data |

## Canonical TSUBAME runtime locations

The MACE, SevenNet, M3GNet/MatGL and GPUMD runtimes are kept under the same
`tgj-26ICP` project workspace and user folder `yang`. Obsolete launchers and
unneeded historical installation directories are removed after their relevant
configuration has been captured in the current scripts and documentation; the
old home-directory SevenNet environment has been retired.

| Backend | Canonical project path | Python environment |
|---|---|---|
| MACE | `/gs/fs/tgj-26ICP/uf03782/yang/li-research` | `.../yang/envs/mace_env` |
| SevenNet | `/gs/fs/tgj-26ICP/uf03782/yang/li-research` | `.../yang/envs/sevennet_env` |
| M3GNet/MatGL | `.../yang/li-research/engines/{matgl,lammps/matgl}` | `.../yang/envs/matgl_env` |
| GPUMD + NEP89 | `.../yang/li-research/engines/{gpumd,gpumdkit}` | GPU executable + GPUMDkit tools |

Each environment directory should contain the launch script, preflight file,
model checksum, executable version, input file, stdout/stderr, and final
`PERFORMANCE` line. Do not overwrite a previous run; use a timestamped run
directory.

The current GPU artifact is `models/m3gnet/m3gnet_matgl_gpu_fixed.pt`. MatGL
source is loaded from `engines/matgl/source/src` through `yang_paths.sh`.

## Important distinction

The common relaxed structure is for a fair backend-speed comparison. It does
not claim that every model has independently optimized the structure. For a
physical diffusion comparison, each model must additionally have its own
relaxation and stability check, stored as a separate run.
