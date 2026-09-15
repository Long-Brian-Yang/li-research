# 新LZOC三温度：基础验证与探索性MSD

后续RDF、配位、骨架MSD及分块分析现已完成：[日语图文报告](../analysis_complete/report_ja.md)／[英语图文报告](../analysis_complete/report_en.md)。下文的待分析表述保留为本次基础检查的历史记录。

来源：TSUBAME 8674278.1–3，192原子，340/360/380 K；NEP89/GPUMD，NVT，0.5 fs。各10 ps升温、50 ps平衡段、200 ps生产。三个分支均已核实完成标记、各阶段GPUMD结束信息、200/1000/4000条有限thermo记录及正确末态组成。三个完整生产轨迹已下载至`../source/LZOC_transport/`。

| 温度/K | 生产平均T/K | 平均P/GPa | 末态最短距离/Å | 20–80 ps斜率换算值/cm² s⁻¹ |
|---|---|---|---|---|
|340|339.761|−0.1860|1.8590|1.814×10⁻⁷|
|360|360.543|−0.1106|1.8799|1.715×10⁻⁷|
|380|380.174|−0.2227|1.8765|1.028×10⁻⁶|

最后一列是**有限时段的表观斜率估计，不是已确认收敛的自扩散系数**。所有温度均按相同方法计算，没有为目标Ea选窗口。

## 方法和证据

每个生产轨迹2000帧、间隔0.1 ps；加入生产输入的t=0帧。核查元素顺序、有限坐标、恒定晶胞；按相邻帧分数坐标最小镜像展开，减去全体系质量加权质心位移，再计算Li的多时间起点MSD。相邻保存帧的最大最小镜像位移为2.22–2.39 Å；该检查不能排除保存间隔内不可观测的多次跨胞。

FFT的滞后1、100、500帧三个结果分别与直接求平均交叉核对，均在1e−8容差内一致。复用`analyze_lzoc_production.py`的`read_gpumd/unwrap/window_msd/fit_msd`，未改原始数据。

MSD拟合为带截距最小二乘；D=slope/6，Å²/ps到cm²/s乘10⁻⁴。20–80表示**滞后时间ps，不是轨迹百分比**。窗口敏感性使用5–40、10–50、20–80、20–100 ps，完整数值见`exploratory_msd.json`，MSD曲线源数据见各温度`*_msd.csv`。

## 必须保留的解释

- 340/360 K的MSD在80 ps仅约1.95/2.16 Å²，振动或局域运动偏置不可忽略。20–80 ps截距约1.09/1.37 Å²；较高线性R²不能单独证明扩散收敛。
- 原始MSD的对数斜率约0.30/0.25/0.63，需结合非零截距解释，不能仅据此确定异常扩散机制。
- 360 K换窗口得到约1.72–4.04×10⁻⁷ cm²/s，说明时段敏感性仍重要。
- 380 K四个50 ps块势能为−4.890838、−4.892221、−4.891540、−4.894401 eV/atom，末段下降尚需结合结构对照。其他温度也不凭一次检查宣称严格平衡。
- NVT密度固定2.23400 g/cm³，不是独立的密度平衡验证；平均压力非零如实报告。
- 暂不计算正式Ea或300 K外推。三温度RDF、配位时间变化、分块输运误差、文献定量比较及非晶性判断仍待补齐。不要求新增DFT。

## English

All three runs completed and the production trajectories were downloaded. Basic composition, timing, finite-value and cell checks passed. The slope-derived values above remain exploratory: low-temperature MSD has a substantial intercept and fit-window dependence, while the 380 K potential energy decreases in the final block. No converged diffusivity, formal activation energy or 300 K extrapolation is claimed.

## 日本語

三温度の計算終了と生産軌跡の保存を確認した。組成・時間間隔・有限値・晶胞の基本確認を実施。表の値は有限時間窓の傾きから得た探索的推定値であり、収束した拡散係数とはしない。低温MSDの切片と窓依存性、380 K末段のポテンシャルエネルギー低下を留意点として残し、正式な活性化エネルギーや300 K外挿は報告しない。
