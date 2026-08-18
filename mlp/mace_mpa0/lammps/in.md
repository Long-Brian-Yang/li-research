# MACE-MPA-0 / LAMMPS ML-IAP: exploratory NVT MD
clear
units metal
atom_style atomic
boundary p p p
newton on

variable model string medium-mpa-0-mliap_lammps.pt
variable data string Li3YCl6_ordered_01_mace_relaxed.data
variable T equal 500.0
read_data ${data}

pair_style mliap unified ${model} 0
pair_coeff * * Li Y Cl

neighbor 2.0 bin
neigh_modify delay 0 every 1 check yes
timestep 0.001
thermo 1000
thermo_style custom step temp pe ke etotal press vol lx ly lz

velocity all create ${T} 18473 mom yes rot no dist gaussian
fix thermostat all nvt temp ${T} ${T} 0.1
dump traj all custom 1000 Li3YCl6_ordered_01_mace_md.lammpstrj id type xu yu zu vx vy vz
restart 10000 Li3YCl6_ordered_01.restart.*
run 25000
unfix thermostat
undump traj
write_data Li3YCl6_ordered_01_mace_md_final.data
