# Targeted diagnostic runs / 問題切り分けの追加計算

> Historical execution record. Current figures, settings and conclusions are integrated into [English](materials_overview_en.md) / [日本語](materials_overview_ja.md). Update those two reports for future status changes.

[Full illustrated English report](../../results/amorphous_review_20260915/targeted_diagnostics/report_en.md) · [図・表付き日本語報告](../../results/amorphous_review_20260915/targeted_diagnostics/report_ja.md)

## Completed results / 完了結果

Both tasks finished normally; complete trajectories were downloaded locally. The postprocessing checks passed: LSZC200 frames/400 thermodynamic records; LZOC800 frames/1600 records; finite values; identical LZOC starting positions, cell and velocities. The tested MSD helper passed its direct-sum regression test (five existing analysis tests passed).

| Diagnostic | Result | Interpretation |
|---|---|---|
|LSZC NPT, final10 ps|Density1.81550 g/cm³ versus initial1.86376; Zr–O CN1.51594; Zr–Cl CN4.25969; all sampled S remain fourfold O-coordinated|Volume relaxation did not resolve the reference discrepancy. No claim of repaired structure|
|LZOC380 K NHC, 10–40 ps fitted D|0.5 fs:1.00361×10⁻⁶ cm²/s;2 fs:8.95684×10⁻⁷ cm²/s|About12.1% higher in this window, not an order-of-magnitude change; a single-trajectory sensitivity result|
|LZOC0.5 fs, fitting-window check|D=1.13169/1.09127/1.00361×10⁻⁶ cm²/s for5–20/10–30/10–40 ps|Window sensitivity remains; no new validated Ea or300 K extrapolation|

The 10–40 ps log–log MSD slopes remain approximately0.56 and0.57, and the free-fit intercept is approximately1 Å². High linear-fit R² alone therefore does not establish long-time diffusion. At5–20 and10–30 ps, timestep differences are approximately−4.4% and−2.9%, respectively: the12.1% value is not a universal correction factor.

**日本語：** 両ジョブは正常終了し、全軌跡をローカルへ保存した。LSZCはNPT後もZr配位の差が残り、密度も低下したため、単なる体積緩和で修復できたとは言えない。新LZOCの0.5 fs対照では10–40 psの見かけのDが約12.1%増加したが、短い解析区間では差の符号も異なる。時間刻み変更だけで輸送の収束を証明したわけではない。既存データは変更せず、根拠のない追加延長は行っていない。

[Numerical results and source hashes](../../results/amorphous_review_20260915/targeted_diagnostics/results.json) · [LSZC time series](../../results/amorphous_review_20260915/targeted_diagnostics/LSZC_structure.csv) · [LZOC0.5 fs MSD](../../results/amorphous_review_20260915/targeted_diagnostics/NHC_0.5fs_MSD.csv) · [LZOC2 fs MSD](../../results/amorphous_review_20260915/targeted_diagnostics/NHC_2fs_MSD.csv) · [Reproducible analysis](../../scripts/structures/analyze_targeted_diagnostics.py)

The following sections record the executed settings. Completion, structural checks and diagnostic comparisons are finished; quantitative reproduction and long-time transport convergence remain unestablished.

## English

Submitted array **8675392.1–2**, 15 September 2026. These are controlled diagnostics, not confirmed repairs or exact reproductions of a paper. Existing results remain unchanged. Both use the existing NEP89/GPUMD installation and preserved restart velocities, with no velocity reinitialisation or manual density adjustment.

| Task | System | Settings | Question |
|---|---|---|---|
|8675392.1|LSZC, 272 atoms|400 K, 1 bar (0.0001 GPa), NPT MTTK, 20 ps; timestep 0.5 fs; temperature/pressure periods 100/1000 fs|Does allowing volume relaxation change the low-density fixed-cell structure?|
|8675392.2|Reconstructed LZOC, 192 atoms|380 K, NVT Nosé–Hoover chain, 80 ps; timestep 0.5 fs, coupling 100 fs|Is the previous NHC result sensitive to the 2 fs timestep?|

Thermodynamic output every 0.05 ps; trajectory every 0.1 ps; restart every 1 ps. Each task has a 15-minute scheduler limit. Completion checks require the GPUMD completion marker, expected atom/record counts and finite thermodynamic values. These checks do not prove equilibration.

LSZC starts from `packed272_anneal_8674277/hold/restart.xyz` (SHA256 `c3c17a4d4b62d5b2decfe314946abb1668290784806e08371a85d514f3795795`). Compare block density, pressure, potential energy, Zr–O/Zr–Cl RDF and coordination, and S–O coordination with the preceding NVT hold. Do not force agreement with the experimental coordination number or author-geometry density. Persistent disagreement remains a model limitation.

LZOC starts from `transport_380K_8674278/equil/restart.xyz` (SHA256 `2006cc9502d9ae18133c81d8b27fd02890484b5f20f799c0f102eb14d0df5dd9`), identical to the original NHC 2 fs production input. Unlike the earlier MTTK/NHC comparison, only timestep changes; the physical thermostat coupling remains 100 fs. Compare identical 80 ps windows, species-resolved MSD, fitting-window sensitivity and energy blocks. A single trajectory pair is a sensitivity check, not a statistically established timestep error or validated activation energy.

LiPON short N–N contacts and Li₃PS₄ network-component differences remain recorded limitations. No atom deletion, trajectory substitution, fitted target rescaling, DFT or blind production extension was performed. The legacy LZOC route remains archived.

Outputs are fresh directories below the remote repository's `runs/amorphous/`: `LSZC/nep89/packed272_npt400_8675392/` and `LZOC_Hussain2024/nep89/nhc_dt05_380K_8675392/`. The diagnostic comparisons are complete and linked above; a successful repair is not demonstrated.

## 日本語

2026年9月15日に **8675392.1–2** を投入した。既存結果は保存し、原因を切り分ける追加計算とする。修復済み、または文献の厳密再現とは扱わない。

- **LSZC、272原子**：既存400 K保持の最終構造から、400 K・1 barで20 psのNPT MTTKを実施。時間刻み0.5 fs、温度／圧力結合周期100／1000 fs。固定セルの影響を調べ、密度・圧力・エネルギーのブロック変化、Zr–O／Zr–Cl RDFと配位、S–O四配位を比較する。実験値に合わせた密度調整はしない。
- **新LZOC、192原子**：従来のNHC／2 fs計算と同じ380 K初期状態から、NVT Nosé–Hoover鎖・0.5 fs・80 psを実施。温度結合は100 fsを維持し、時間刻みだけを変更する。同じ時間範囲のMSD・解析区間感度・エネルギーを比較する。単一軌跡の対照から収束やEaの妥当性を断定しない。

熱力学量は0.05 ps、軌跡は0.1 ps、restartは1 ps間隔で出力した。正常終了と有限値の確認は基本検査であり、平衡の証明ではない。診断結果の解析と図表は完了し、上記報告に整理した。

LiPONの短いN–N接触とLi₃PS₄のネットワーク差は限界として保持する。原子削除、軌跡の差し替え、数値の再スケーリング、DFT、根拠のない長時間延長は実施しない。旧LZOCも追加しない。

[Job script](../../hpc/tsubame_26icp/production/amorphous_targeted_diagnostics.sh) · [English portfolio](materials_overview_en.md) · [日本語全体整理](materials_overview_ja.md)
