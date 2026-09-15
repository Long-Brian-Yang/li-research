# 旧 LZOC 候选 3：MACE／NEP89 时间与选择依据

核查日期：2026-09-15。对象为192原子 Li₄₂Zr₂₄O₁₂Cl₁₁₄，旧候选3，不是Hussain2024重建路线。

## 1. 结论

有实际运行时间对照。**NEP89/GPUMD 的效率明显更高，600 K 下的膨胀和骨架重排也比本批 MACE 结果弱，因此有理由优先用它开展后续探索。但这不是“最终验证 NEP 更准确”。** 当前旧路线仍作为对照保留，不继续扩大长计算。

效率数据本次重新查询TSUBAME；结构与扩散数字来自2026-09-12已核验轨迹的分析，不是本次重新计算。这里依据现有证据整理选择理由，不声称此前已有正式的模型优劣验收。

## 2. 四温度整作业时间

采用 `qacct` 的 `ru_wallclock`，即实际作业运行时间（与start/end差一致），不含排队。未用请求的walltime上限、CPU累计时间或另一个`wallclock`字段替代。八个任务均`failed=0, exit_status=0`。

| T / K | MACE任务 | MACE运行秒数（约时分秒） | NEP89任务 | NEP运行秒数（约时分秒） | MACE/NEP耗时比 |
|---|---|---:|---|---:|---:|
| 600 | 8635176.1 | 14830.478（4:07:10） | 8635527 | 544.344（0:09:04） | 27.24 |
| 700 | 8635176.2 | 18019.970（5:00:20） | 8653328 | 502.105（0:08:22） | 35.89 |
| 800 | 8635176.3 | 14485.452（4:01:25） | 8653329 | 501.880（0:08:22） | 28.86 |
| 900 | 8635176.4 | 18975.057（5:16:15） | 8653330 | 497.137（0:08:17） | 38.17 |
| 合计 | 4个任务 | 66310.957（18:25:11） | 4个任务 | 2045.466（0:34:05） | 32.42 |

合计是任务运行时长之和，不是并行提交后的日历等待时间，也不是实际points账单。不包含此前MACE制备、额外300 K平衡或NEP后续50 ps NPT延长。

### 更直接的600 K生产段对比

两者均为192原子、0.5 fs、400000步，即200 ps NVT production：

| 引擎计时口径 | 时间 | 备注 |
|---|---:|---|
| MACE/LAMMPS `Loop time` | 11395.5 s（3:09:56） | 1进程，日志35.102 steps/s |
| NEP89/GPUMD `Time used for this run` | 366.428 s（0:06:06） | 日志209591 atom·step/s |

生产段耗时比约 **31.10**。两个引擎计时范围不完全相同，故这是本批实现的实测对照，不是严格隔离所有变量的内核benchmark。

### 比较条件与限制

- 两者来自同一候选3，采用gpu_1资源类别；任务运行在不同节点，不保证相同GPU实例或负载。
- MACE-MPA-0使用LAMMPS ML-IAP/Kokkos；NEP89使用GPUMD。模型与实现同时变化，不能把加速归因于单一算法或CPU/GPU切换。
- MACE流程：10 ps升温＋50 ps NPT＋200 ps NVT，共260 ps。
- NEP另有固定晶胞最小化及1 ps smoke，MD共261 ps；独立速度种子和预处理，最终NPT晶胞也不同。因此整作业不是完全相同工作负载。
- 两者Tdamp/Pdamp或对应耦合周期均设置约100 fs/1 ps，但不同引擎系综实现不等同。

## 3. 600 K结构与扩散对照

共同300 K输入密度约1.913855 g/cm³，只是模拟参考，不是实验密度。

| 指标 | MACE | NEP89 |
|---|---:|---:|
| production密度 / g cm⁻³ | 1.468304 | 1.875429 |
| 相对300 K输入体积增加 | 30.3% | 2.0% |
| Zr自身质心校正后MSD(200 ps) / Å² | 57.965 | 9.805 |
| 起始Zr–Cl近邻在末帧保留率 | 64.8% | 89.6% |
| 暂定Li自扩散D / cm² s⁻¹ | 1.7197×10⁻⁵ | 1.0757×10⁻⁵ |
| 同一lag区间log–log MSD指数α | 0.777 | 0.924 |

近邻截断Zr–Cl=3.0 Å；保留率只比较首末帧，不是键寿命。D由多时间起点MSD、全体系质心校正、20–80 ps **lag time**拟合，不能误写成20–80%轨迹截取。

这些结果支持“在这个600 K试跑中，NEP的框架移动和膨胀更弱”，不证明密度更高一定更真实。MACE的800/900 K末段NPT密度还在变化；NEP600 K仍有骨架位移与残余松弛，后续高温结果也需独立检查。

旧MACE四温度的表观Ea=0.20544 eV受结构状态变化影响，不能当已验证的稳定固态迁移势垒；不以它或预期实验值来挑选模型。旧单温分析中的“NEP只有一个温度”仅描述2026-09-12分析快照，不能当当前队列／数据清单。

## 4. 为什么后来优先继续NEP

1. **计算效率**：本批200 ps生产段约31倍加速，适合有限points下的制备、结构筛查和参数诊断。
2. **本体系的初步结构表现**：600 K相对输入的膨胀更小、Zr移动更弱、Zr–Cl近邻保持更高，而MACE本批出现明显异常。
3. **执行环境可复用**：已有NEP89/GPUMD模型、脚本及来源hash记录，便于团队复用和可追溯比较。
4. **准确性仍待验证**：同组成实验密度／结构或匹配构型DFT仍必要。新材料中的LiPON短N–N问题也说明NEP不能因快速就普遍视为正确。

因此建议把“最终选择NEP”改为：**“基于计算效率与初步结构诊断，后续探索优先采用NEP89/GPUMD；准确性验证尚未完成，MACE保留为对照。”**

## 5. 汇报用英文／日文

### English

For the 192-atom legacy LZOC candidate, the 600 K job took 4 h 7 min with MACE/LAMMPS and 9 min with NEP89/GPUMD. The corresponding 200 ps production timings were 11395.5 and 366.428 s, respectively, an approximately 31-fold difference. NEP also showed less expansion and weaker framework rearrangement in this particular 600 K trial. These observations motivated prioritizing NEP for further exploratory work, not a conclusion that it was quantitatively more accurate. The workflows and engines differ, and validation against matching experimental or DFT data remains necessary.

### 日本語

192原子の旧LZOC候補について、600 Kのジョブ実行時間はMACE/LAMMPSで約4時間7分、NEP89/GPUMDで約9分であった。200 psの本計算部分はそれぞれ11395.5秒と366.428秒で、約31倍の差があった。また、この600 K試行ではNEPの体積膨張と骨格再配置が比較的小さかった。このため、以降の探索的検討ではNEPを優先した。ただし、計算工程と実装が異なるため厳密な速度ベンチマークではなく、NEPの定量精度が優れていると実証したものでもない。同組成の実験または対応するDFTデータによる検証は引き続き必要である。

## 6. 根拠と再確認方法

- 計時：`qacct -j 8635176`、`qacct -j 8635527`、`qacct -j 8653328`、`qacct -j 8653329`、`qacct -j 8653330`。
- [構造・拡散の分析](../../../results/LZOC/analysis_20260912/README.md)
- [膨張・骨格監査](../../../results/LZOC/analysis_20260912/expansion_framework_audit.md)
- [MACE設定](../../../materials/candidates/LZOC/MD_4T_8635176.md)
- [NEP設定](../../../materials/candidates/LZOC/NEP89_4T_20260912.md)
- 生ログ：`results/LZOC/analysis_20260912/source/mace/600K_R1/stdout.txt`、`source/nep89/production/stdout.txt`（後者も同じ分析ディレクトリ内）。

本次只新增分析说明，不更改轨迹、Ea、模型标签；未提交新计算或Git push。
