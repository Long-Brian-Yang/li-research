# Candidate 3 additional equilibration

Submitted 2026-09-11 after user approval. Job **8634186** (`lzoc_eq300`),
group `tgj-26ICP`, one `gpu_1`, wall-time limit 90 minutes.

- Source: `reference_8631935/source_3/relaxed_300K.data`, the finite-temperature
  endpoint including velocities, not the subsequently minimized structure.
- Source SHA256: `85029f6b8a24ca7fee1e05543f571d7bb80e775846b6aac917ce03f5a82932fc`.
- MACE-MPA-0, 192 atoms, Li42Zr24O12Cl114.
- 300 K, 1 bar isotropic NPT; timestep 0.5 fs; 100,000 steps = 50 ps.
- Atomic positions, cell and velocities retained; thermostat/barostat state
  reinitialized (data-file continuation, not a binary-restart continuation).
- Output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/equilibrate_8634186/`.
- No automatic production job or additional candidate generation.

After completion, inspect successive density/energy blocks and residual order
before accepting the structure for a separately specified production temperature.
The job completed successfully in 54 min 22 s; final data and restart were
generated. See the [post-equilibration check](../materials/candidates/LZOC/equilibration_8634186/analysis/README.md)
and [proposed next temperatures](lzoc_next_md_plan_2026-09-11.md).
Numerical completion does not imply full physical equilibration.
