# Literature-derived LZOC preparation trials

## Current status — 2026-09-11

All three preparation jobs completed. Candidate 3 was provisionally selected
by the user; full amorphization and physical equilibration remain unverified.
Final structures, intermediate endpoints, logs and actual job inputs are
archived in [completed_reference_trials](../materials/candidates/LZOC/completed_reference_trials/README.md).
The chronology below preserves earlier submission-time status; it is not a
live queue report. No formal 50+200 ps transport job has been submitted.

User approved two starting configurations, 55 ps preparation each, on 2026-09-11. Goal: compare physical plausibility and retain one candidate; no automatic 50+200 ps transport jobs.

- Job array: **8631903**, tasks **1 and 2**, group **tgj-26ICP**.
- Resources: each task gpu_1=1, h_rt=1:30:00.
- Task1: Kim2025 Supplementary Data4-derived target, `materials/candidates/LZOC/kim2025_derived_seed`.
- Task2: Kim2025 Supplementary Data19-derived target, `materials/candidates/LZOC/kim2025_data19_seed`.
- Both: Li42Zr24O12Cl114 (192 atoms), target Li1.75ZrCl4.75O0.5, same initial volume5227.1769 Å³, density2.13291 g/cm³.
- Sources are related configurations, not independently generated amorphous replicas. Each removes18 LiCl pairs from a2x2x1 parent supercell using recorded fixed-seed construction; no energy-optimal vacancy arrangement claimed.

## Workflow

MACE-MPA-0 ML-IAP/Kokkos; fixed-cell initial CG minimization; new1500K velocities;10ps1500K NVT mixing;30ps NVT cooling to300K;5ps300K NVT;10ps300K/1bar isotropic NPT;fixed-cell final CG minimization. MD step0.5fs. Minimization force-two-norm tolerance0.01eV/Å; actual stopping criterion must be inspected.

Output root: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/reference_8631903/source_1/` and `source_2/`. Each stores input, provenance, source metadata, hashes, log, trajectory and stage endpoints.

## Acceptance remains pending

Verify initial/final minimization stopping reason, preserved composition, no lost atoms, all-species MIC distances, density and energy evolution in the unconstrained-volume segment, local coordination and residual crystalline order. No predetermined density or experimental activation-energy target is imposed. Fixed-volume stability is not NPT equilibration;55ps alone does not certify amorphization. Record any anomalies rather than smooth or relabel them.

Five tests passed (3builder,2job contracts), shell syntax passed, CIF/LAMMPS roundtrip previously verified forData4. Submitted successfully; final structures are not yet accepted. Existing256atom job8631595 was not cancelled or overwritten.

## Subsequent scope change

User subsequently requested one additional trial. Added **8631935.3**, explicitly submitted with `qsub -g tgj-26ICP -t 3` (not resubmitting tasks1/2). Source: Kim2025 Data18, the600K AIMD starting configuration, adjusted to192atoms with the same composition and construction method. Same55ps workflow,1GPU,90min limit. Output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/reference_8631935/source_3/`. Six local builder/job tests passed. Three related starting configurations now form the comparison; they are not three independent amorphous replicas. Acceptance remains pending.

User retired the original256atom branch after the two literature trials started. A targeted cancellation of job8631595 was requested after confirming it was running at approximately42.5/55ps. Existing files are retained, not deleted, and excluded from final candidate selection. Only8631903.1 and8631903.2 remain in the active comparison. This is a scope decision, not evidence that the original structure was physically invalid.
