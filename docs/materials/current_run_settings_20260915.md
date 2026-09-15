# Current simulation settings / 現在の計算設定 / 当前实际设置

Snapshot: 2026-09-15. This records executed/submitted settings, not a claim of strict literature reproduction or validated equilibrium.
以下记录实际工程设置，不把任务正常结束等同于非晶形成或准确性验证。以下は実設定の記録であり、原論文の厳密再現や平衡化の認定ではない。

## Latest status / 最新状态 / 最新状況

- **8674222: new LZOC, 300 K, 50 ps hold completed.** Remote `completed.txt` and `Finished running GPUMD.` confirmed during this update. The new hold trajectory has not yet been reanalysed for convergence. 新增50 ps正常结束，尚待追加段收敛分析。追加50 psは正常終了したが、収束解析は未実施。
- LSZC: five finite geometric clusters extracted from author Data1; two copies each plus32Li give272atoms. Packing, relaxation and amorphous validation remain unfinished; no new packing MD job. 已完成团簇提取，未完成装箱。クラスター抽出済み、配置・緩和は未完了。
- LiPON: N–N pair at row indices76/108 first crosses1.6Å between2.2–2.3ps of2000K hold and persists. Three diagnostic full-cell snapshots saved; DFT not run. 化学验证待完成。化学的妥当性の検証待ち。
- Li3PS4: existing611ps preparation/validation retained; no new formal transport production or low-temperature DFT in this update.
- Legacy LZOC candidate3: comparison only; no additional long run.

## Protocol matrix

| Route | Atoms | Actual stages | Potential / engine | Important deviations |
|---|---:|---|---|---|
| Legacy LZOC candidate3 |192| MACE:10ps heating,50ps1barNPT,200psNVT at600/700/800/900K; NEP additionally position minimization and1ps smoke; NEP700–900K later50psNPT diagnostics | MACE-MPA-0/LAMMPS ML-IAP Kokkos; NEP89/GPUMD | Independent velocities/preprocessing/cells; not a potential-only benchmark |
| Reconstructed LZOC |192|100K2ps;500K30ps;1000K50ps;1500K30ps;2000K20ps; fixed-cell NEP position minimization;1500/1000/500/100K2ps each;300K20ps; additional300K50psNVT |NEP89/GPUMD| Author96atom branch adapted to192atoms and NEP; no post-melt DFT volume optimization; additional50ps is our diagnostic |
| LSZC seed |272|300K5kbar12psNPT;300K1bar20psNPT |NEP89/GPUMD| Crystal-unit replicated seed, not author packed glass. Do not apply this status to the new unpacked cluster library |
| Li3PS4 |512| Position minimization;300K1ps smoke;300→1500K10psNPT;1500K100psNPT;1500→300K480psNPT (2.5K/ps);300K20psNPT |NEP89/GPUMD| Literature melt/quench schedule with changed potential, seed, size and coupling details |
| LiPON |124| Position minimization;300K1ps;300→2000K5ps;2000K10ps;2000→250K7ps (250K/ps);250K20ps, all NVT; then250K1bar20psNPT |NEP89/GPUMD| Literature melt/quench steps plus project diagnostics, independent substitutions, smaller timestep; not Lacivita2018 protocol |

## Common implementation details

- Timestep0.5fs. GPUMD MTTK thermostat period200steps=100fs; barostat period2000steps=1ps where NPT is used. Pressure1bar=0.0001GPa;5kbar=0.5GPa. These coupling choices are project settings.
- Latest LZOC hold: retain coordinates, cell and velocities from8674094/300K/restart.xyz; reinitialize thermostat state; no new minimization or velocity seed.100000steps,thermo every100steps(0.05ps),dump every200steps(0.1ps),restart every2000steps(1ps).
- Latest scheduler request: group`tgj-26ICP`,gpu_1=1,15minute ceiling; ceiling is not expected runtime or point charge.
- NEP model: `models/nep89/nep/nep89_20250409/nep89_20250409.txt`; SHA256 `75168ece02e840e4a32644f982b78d43cba697f5b64b4c8134ab66c7a8c28be1`.
- Latest restart SHA256: `af388d2b6a5aa90a2e4bc802656f30efd8bbab296f03b08c8e64ac10ec8f2a7f`.
- Runtime: `engines/gpumd/source/src/gpumd`; gcc14.2.0,CUDA12.8.0. Per-job provenance records actual binary/model/input hashes. Input paths are under TSUBAME project root `/gs/fs/tgj-26ICP/uf03782/yang/li-research`.

## Source and navigation

- [中文总览](materials_overview_zh.md) / [日本語](materials_overview_ja.md) / [English](materials_overview_en.md): references and deviations.
- [Diagnostics](../../results/amorphous_review_20260915/README.md): block statistics, RDF, coordination, snapshot provenance.
- [Legacy MACE/NEP runtime comparison](LZOC/candidate3_mace_nep_comparison.md).
- [Latest submitted script](../../hpc/tsubame_26icp/production/lzoc192_hold300.sh).

Raw trajectories, pretrained weights and publisher PDFs are excluded from this documentation commit. The scripts require the documented runtime and source data on TSUBAME/local storage; a source-code checkout alone is not a complete raw-data archive. Historical “not pushed” notes refer to their writing time, not the eventual synchronization status of this commit.
