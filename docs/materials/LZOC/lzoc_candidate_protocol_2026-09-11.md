# Single LZOC candidate preparation

> Historical record / 历史记录：保留记录当时的设置与判断，不作为实时任务状态。参见 [材料文档索引](README.md)。

User requested simplified candidate preparation, not further detailed void investigation. No raw data are removed or altered. One replica only; no automatic transport production.

Pressure check 8631511: at fractional volume perturbation 0.001, finite-difference pressure minus virial pressure is +0.407946 bar for the starting frame and +0.141048 bar for the ending frame. Deviations decrease as the perturbation decreases. This supports internal isotropic virial/energy consistency on these two snapshots, not physical accuracy of MACE in all states.

## Source and conditions

- Source: TSUBAME `runs/amorphous/LZOC/mace_mpa0/rebuild_8628860/replica_1/pilot_final.data`, not the expanded high-temperature endpoint.
- Li56 Zr32 O16 Cl152; 19 Å cubic initial box, initial density 2.167293 g/cm³ is a numerical assumption.
- MACE-MPA-0 ML-IAP/Kokkos, 0.5 fs timestep, single gpu_1, group tgj-26ICP.
- 1500 K NVT mixing 10 ps, then NVT cooling to 300 K over 30 ps (40 K/ps).
- 300 K NVT hold 5 ps, then 300 K/1 bar isotropic NPT release 10 ps.
- Save finite-temperature endpoint, then fixed-box minimization (force two-norm tolerance 0.01 eV/Å, max 10000 iterations/30000 force evaluations). Verify actual stopping criterion afterwards.
- Thermostat damping 0.1 ps, barostat damping 1 ps. Trajectory 0.05 ps, checkpoint 1 ps; 55 ps MD total.

## Minimal acceptance gate

Check counts and all-species minimum-image distance distributions, with particular attention to previously anomalous O–O contacts. Review final minimization convergence and the 300 K volume-unconstrained segment's density/energy evolution. Fixed-volume density constancy is not evidence of equilibration. Compare pair RDFs of the quenched/released structure; broad peaks alone cannot uniquely establish amorphous character in a small hot/disordered cell. Retain a candidate label if stationarity or structural identity remains uncertain. A geometry-only pass does not validate force-field accuracy.

Final decision and job status must be recorded after inspecting actual outputs. A successful scheduler exit is not scientific acceptance. No automatic 50 ps equilibration + 200 ps production follows this job.

## Submission

Job `8631595` (`lzoc_candidate`) submitted on 2026-09-11 under group `tgj-26ICP`. Single replica, one GPU, 90-minute walltime limit. Output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC/mace_mpa0/candidate_8631595/`. Five local LZOC static/unit tests and shell syntax check passed. Simulation and scientific acceptance pending.
