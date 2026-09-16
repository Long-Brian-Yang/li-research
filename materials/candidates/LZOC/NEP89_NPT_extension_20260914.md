# NEP89: additional 50 ps NPT diagnostics — 2026-09-14

User-approved diagnostic continuation only. No new production and no change to existing trajectories.

| T / K | Source job | Extension job | New output directory relative to project root |
|---|---|---|---|
| 900 | 8653330 | 8665994 | runs/amorphous/LZOC/nep89/900K_npt_extension_8665994 |
| 800 | 8653329 | 8665995 | runs/amorphous/LZOC/nep89/800K_npt_extension_8665995 |
| 700 | 8653328 | 8665996 | runs/amorphous/LZOC/nep89/700K_npt_extension_8665996 |

Group `tgj-26ICP`; one `gpu_1` per job, 15-minute wall-time limit (not predicted runtime). 600 K is unchanged.

## Conditions and provenance

- Start from the original run's `equilibration/restart.xyz`, not its production endpoint.
- Preserve the 192 atoms, species, cell, positions and velocities. No minimization or velocity reassignment.
- A new GPUMD process initializes its thermostat/barostat internal state. This is not an exact checkpoint continuation of all extended-system variables.
- Same NEP89 model and GPUMD binary, with SHA256 checks against the original run version.
- NPT MTTK at the respective target temperature and 1 bar (`0.0001 GPa`). Isotropic pressure control; timestep 0.5 fs, tperiod 200 steps, pperiod 2000 steps.
- 100000 steps = 50 ps; thermo every 0.05 ps, trajectory every 0.1 ps, restart every 1 ps.
- New time begins at zero; add 50 ps when plotting against the original NPT history. Do not join this directly to the old NVT production as one continuous run.
- Outputs are created in fresh job-ID directories; an existing output directory causes failure, not overwrite.

Source restart SHA256:

| T / K | SHA256 |
|---|---|
| 700 | fe19e28dcea7fa88d365139a55e4ef5e74c043341ddb0f95f6157f8bbf27f0d7 |
| 800 | b02492a930764ab44700cb028395f3a0982c70fe870b78b32814a187d64b86bf |
| 900 | 7aa09e4c73e5cc09619e2b2db73cd35a92f0ef31773600d282e7d0db0002d827 |

Local job specification: `hpc/tsubame_26icp/production/nep89_npt_extension.sh`.
Remote snapshot: `hpc/tsubame_26icp/production/nep89_npt_extension_20260914.sh`.
Project root on TSUBAME: `/gs/fs/tgj-26ICP/uf03782/yang/li-research`.
Two local contract tests and bash syntax check passed; qsub accepted all three jobs. This does not imply run completion or physical equilibration.

## Decision after completion

Compare consecutive density, potential-energy and volume blocks; inspect RDF/coordination and framework motion. Include the initial transient from reinitialization in interpretation. No universal percentage threshold or target diffusion coefficient is imposed. If density keeps changing or the framework is mobile, investigate structure/potential applicability rather than extending indefinitely. If a different equilibrated cell is adopted, a separately approved production run is needed; retain the old production as its own exploratory result.
