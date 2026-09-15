# AIMD-aligned NEP transport control / AIMD条件に合わせたNEP比較

## Completion / 完了確認（2026-09-15）

All three tasks completed: each production has 1600 thermo records, 800 trajectory frames, completion marker and GPUMD finished log. Outputs downloaded locally. Matched first-80-ps analysis: [English](../../../results/amorphous_review_20260915/final_comparisons/report_en.md) / [日本語](../../../results/amorphous_review_20260915/final_comparisons/report_ja.md). Initial positions/cell/stored velocities agree with the earlier production input. No strict-reproduction claim; no adopted converged Ea. All numerical source hashes are included in the report directory.

## English

Hussain et al. (2024), [DOI](https://doi.org/10.1038/s41524-024-01346-y), reports amorphous transport at 340/360/380 K for80 ps, NVT Nosé–Hoover,2 fs. This control uses those temperatures, timestep and transport duration, with GPUMD Nosé–Hoover chain (`nvt_nhc`). Coupling100 fs (`50` timesteps) is our retained physical coupling choice, not a verified paper setting. [GPUMD syntax](https://gpumd.org/gpumd/input_parameters/ensemble_standard.html), [coupling units](https://gpumd.org/gpumd/input_parameters/ensemble.html).

Each run starts from the corresponding equil/restart.xyz of job8674278, i.e. the identical initial position, cell and velocity used for the earlier200 ps production. Existing10 ps ramp and50 ps pre-equilibration history are retained; no new ramp or50 ps stage is added. A separate2 ps smoke run must pass finite thermo/count/temperature checks before the80 ps run, which restarts from the original input, not the smoke endpoint. No automatic fallback to0.5 fs. These checks detect gross numerical failure, not timestep convergence or equilibrium.

Remaining differences: NEP89 rather than DFT;192 rather than48 atoms; independently reconstructed seed and adapted high-temperature preparation; no DFT cell optimization; thermostat implementation and unreported coupling. This is NOT exact AIMD reproduction or a test isolating one parameter. Old results are preserved. Compare the first80 ps of old production with new80 ps using identical analysis windows; compare thermostat/timestep effects jointly, without selecting windows to target Ea. Review temperature, energy, minimum distances, RDF/coordination and MSD before fitting transport.

## 日本語

340／360／380 K、時間刻み2 fs、NVT、80 psの輸送計算を文献に合わせる。GPUMDのNosé–Hoover chainを使用し、結合時間100 fsは本研究の設定として明記する。各温度の旧計算のproduction開始状態から再開し、元の構造・セル・速度と事前の平衡化履歴を維持する。独立した2 psの数値確認後、同じ開始状態から80 psを計算する。旧結果は上書きしない。

NEP／DFT、原子数、構造生成履歴、温控実装が異なるため、厳密なAIMD再現とは呼ばない。数値確認の合格は平衡やポテンシャル精度の証明ではない。旧計算の最初の80 psと同じ解析条件で比較する。

## Submission

Submitted 2026-09-15: job-array **8675022.1–3**, mapping1=340 K,2=360 K,3=380 K. gpu_1, walltime15 min per task. Group balance216.72 points and deposit12.26 were read separately before submission. Submission is not completion.

Remote output: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/runs/amorphous/LZOC_Hussain2024/nep89/aimd_aligned_{340,360,380}K_8675022/`, with separate `smoke/` and `production/` folders. Input hashes and executable/model hashes are recorded by each task.
