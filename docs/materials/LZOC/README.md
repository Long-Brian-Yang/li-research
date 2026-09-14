# LZOC：建模、运行与分析记录

对象：Li₁.₇₅ZrCl₄.₇₅O₀.₅；现有工作结构为候选 3，192 原子（Li42 Zr24 O12 Cl114）。候选用于探索性计算，不表示已验证为最优或充分平衡的非晶结构。

## 1. 汇报与文献

- 日常汇报：[日语](../../daily_reports/2026-09-14/ja.md) / [English](../../daily_reports/2026-09-14/en.md)。主要讲述候选来源、制备、平衡检查和 MACE 600 K 计算方案。
- 三篇论文：[阅读报告入口](../../literature/lzoc_top3/README.md)。
- [MACE 600 K 日语详细分析](analysis_MACE_600K_20260914_ja.md)：与上述汇报分开，包含数值及体积膨胀、骨架移动等限制。

## 2. 建模与平衡（按流程阅读）

1. [文献构型衍生的三组制备](lzoc_reference_trials_2026-09-11.md)
2. [候选选择与原始记录](../../../materials/candidates/LZOC/archive/completed_reference_trials/SELECTION.md)
3. [候选 3 额外 50 ps 平衡](lzoc_candidate3_equilibration_8634186.md)
4. [平衡后检查](../../../materials/candidates/LZOC/archive/equilibration_8634186/analysis/README.md)
5. [结构文件入口（CIF / data）](../../../materials/candidates/LZOC/README.md)

## 3. 温度分支与分析

- [四温度 MACE 方案](lzoc_next_md_plan_2026-09-11.md)：保留方案讨论当时的判断。
- [MACE job 8635176 设置和输出路径](../../../materials/candidates/LZOC/MD_4T_8635176.md)
- [NEP89 四温度设置和输出路径](../../../materials/candidates/LZOC/NEP89_4T_20260912.md)
- [2026-09-12 分析快照](../../../results/LZOC/analysis_20260912/README.md)
- [体积／骨架检查](../../../results/LZOC/analysis_20260912/expansion_framework_audit.md)

这些是带日期的运行／分析记录，不是实时状态。2026-09-12 的分析快照只涵盖当时已分析的 MACE 四温度和 NEP89 600 K，不能误认为后续 NEP89 全温度分析已完成。

## 4. 早期方案（非当前结构）

- [256 原子高温筛选诊断](lzoc_R1_high_temperature_diagnostic_2026-09-11.md)
- [256 原子候选制备协议](lzoc_candidate_protocol_2026-09-11.md)

早期记录保留用于追溯，不与文献衍生的 192 原子候选 3 混用。目录整理不重新拟合、替换轨迹或改变既有数值。
