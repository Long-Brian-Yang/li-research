#!/usr/bin/env bash
# Short legacy MACE-LAMMPS GPU smoke test for the current two structures.
#$ -cwd
#$ -V
#$ -l gpu_1=1
#$ -l h_rt=0:30:00
#$ -N smoke_mace_new
set -euo pipefail
ROOT="${TSUBAME_TEST_ROOT:-$PWD}"
LAMMPS="$ROOT/lammps-mace-gpu-install/bin/lmp"
MODEL="$ROOT/mace-mpa-0-medium.model-lammps.pt"
OUT="$ROOT/mace_smoke_400K_new_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUT"
module load gcc/14.2.0
module load openmpi/5.0.10-gcc
module load python/3.14.3
export LD_LIBRARY_PATH="$ROOT/venv/lib64/python3.9/site-packages/torch/lib:${LD_LIBRARY_PATH:-}"
[[ -x "$LAMMPS" && -s "$MODEL" ]]
run_case() {
  local name="$1" data="$2" elements="$3" masses="$4" seed="$5"
  local input="$OUT/in.$name"
  cat > "$input" <<EOF
clear
units metal
atom_style atomic
boundary p p p
newton on
atom_modify map yes
read_data $data
$masses
pair_style mace no_domain_decomposition
pair_coeff * * $MODEL $elements
timestep 0.001
thermo 100
thermo_style custom step temp pe ke etotal press vol lx ly lz
thermo_modify flush yes
velocity all create 400.0 $seed mom yes rot no dist gaussian
fix nvt all nvt temp 400.0 400.0 0.1
dump traj all custom 100 $OUT/${name}.lammpstrj id type xu yu zu vx vy vz
run 1000
write_data $OUT/${name}_final.data
EOF
  "$LAMMPS" -k on g 1 -sf kk -pk kokkos newton on neigh half -in "$input" -log "$OUT/${name}.log"
}
run_case Li3YCl6_03 "$ROOT/Li3YCl6_ordered_03_2x2x4.data" "Li Y Cl" $'mass 1 6.94\nmass 2 88.90584\nmass 3 35.45' 41003
run_case LiNbOCl4 "$ROOT/LiNbOCl4_ordered_2x2x3.data" "Li Nb O Cl" $'mass 1 6.94\nmass 2 92.90638\nmass 3 16.00\nmass 4 35.45' 41004
echo "Legacy MACE smoke test completed: $OUT"
