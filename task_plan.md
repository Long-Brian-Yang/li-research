# Direction 2 project plan

## Goal

Build a reproducible Direction 2 workflow for Li₃YCl₆ and LiNbOCl₄, from
literature benchmark and explicit ordered structures to validated ML-MD
transport results. Keep MACE and NEP89 results separate and comparable only
after matching temperature, cell, trajectory length, and analysis.

## Phases

1. **Scope and literature** — completed
   - Keep the nine-paper bilingual notes.
   - Restrict the computational scope to Li₃YCl₆ and LiNbOCl₄.
2. **Structure policy** — completed with limitations
   - Do not use screenshot CIFs directly: partial occupancies require explicit
     ordered models.
   - Keep Li₃YCl₆ orderings as separate replicas.
3. **MACE reference runs** — in progress
   - Four independent 400 K jobs (8441077–8441080), 10 ps equilibration +
     100 ps production, 1 fs timestep, 14 h walltime.
   - Verify completion, trajectory length, stability, and MSD after jobs finish.
4. **NEP89 reference runs** — completed for the current screening stage
   - 300 K 2×2×4 Li₃YCl₆ replicas and LiNbOCl₄ run.
   - Official GPUMDkit MSD/thermo plots and 100–300 ps primary fit are stored.
5. **Matched comparison** — pending
   - Compare MACE and NEP89 only with matched temperature and supercell.
   - Report tracer/NE conductivity separately from experimental EIS values.
6. **Validation and publication-ready organization** — pending
   - Check model forces/energies against DFT snapshots.
   - Add uncertainty, finite-size, ordering, and potential-dependence analysis.
   - Commit only compact trajectories/results; retain full trajectories on TSUBAME.

## Current decision

The immediate priority is to finish the four new MACE jobs and analyze them
before changing the NEP89 protocol or drawing a model-to-experiment conclusion.

## Errors encountered

| Issue | Resolution |
|---|---|
| Screenshot Li₃YCl₆ CIF expands to wrong composition | Use explicit ordered models; never delete atoms to repair it |
| Earlier MACE jobs stopped before 100 ps | Submit one system per job with 14 h walltime |
| Custom plots were mistaken for GPUMDkit plots | Official GPUMDkit outputs are now the primary figures |
