# MACE ML-IAP input templates

These are maintained LAMMPS templates for the MACE ML-IAP/Kokkos workflow.
They require an explicit ordered structure and a converted MACE checkpoint.

- `convert_mace_checkpoint_mliap.sh` converts a MACE checkpoint to ML-IAP.
- `in_relax_cell.*` performs a FIRE cell relaxation.
- `in_nvt_400K_10ps_eq_100ps_prod.*` is the short NVT protocol.
- `in_nvt_500K_exploratory.*` is a short exploratory NVT template.

The canonical TSUBAME execution environment is defined by
`../../config/yang_paths.sh`; benchmark launchers remain under `../../benchmark/`.
The legacy `pair_style mace` templates and provisional partial-occupancy tests
were removed and must not be reused for new calculations.
