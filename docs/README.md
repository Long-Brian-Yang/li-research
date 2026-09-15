# Documentation index / 文档导航

按用途阅读；带日期的报告记录当时的状态，不代表实时队列或最终科学结论。

| 类别 | 入口 | 内容 |
|---|---|---|
| 非晶研究主报告（仅维护这两份） | [日本語](materials/materials_overview_ja.md) / [English](materials/materials_overview_en.md) | 按材料集中设置、27组图、表格、公式、文献对照、未解决事项与数据保存规则 |
| 历史设置快照 | [2026-09-15 阶段设置](materials/current_run_settings_20260915.md) / [旧中文总览](materials/materials_overview_zh.md) | 历史记录，不作为当前状态入口；以两份主报告为准 |
| 日常汇报 | [Daily reports](daily_reports/README.md) | 按日期整理，英语／日语分别保存 |
| LZOC 建模与运行 | [LZOC](materials/LZOC/README.md) | 候选背景、制备、平衡、协议与探索性分析 |
| 三篇论文阅读 | [LZOC literature](literature/lzoc_top3/README.md) | 英语／日语阅读报告及来源笔记 |
| 开发与计算规范 | [Development](development/README.md) | 环境、协议、benchmark、研究计划 |
| 中期发表 | [中期结果目录](../results/midterm_Li3YCl6_MACE_M3GNet/) | Markdown 与配套图片、表格共同保存；目录名称沿用历史名称 |
| 最终发表 | [最终结果目录](../results/publication_all_materials/) | 两个材料的图、说明与源数据 |
| 结构文件 | [LZOC structures](../materials/candidates/LZOC/README.md) | CIF、LAMMPS data、结构来源及运行清单 |
| TSUBAME 使用 | [HPC](../hpc/tsubame_26icp/README.md) | 作业与集群运行说明 |

## 历史记录与使用规则

- 当前非晶研究内容只更新上述日语／英语主报告；不再新建分散的进度 Markdown。旧短报告保留为可追溯的历史快照。

- [早期 Arrhenius 组合筛选](best_arrhenius_combinations.md) 与 [SevenNet 81 组枚举](development/results/sevennet_700_800_900_1000_all_81.md) 是历史探索，不应自动作为当前最终结果。
- 图表和结构的 README 保持与对应文件同目录，不为分类而拆散依赖关系。
- 新日报放入 `daily_reports/YYYY-MM-DD/`，语言分别为 `ja.md`、`en.md`。
- 建模和分析记录写明材料、日期、job ID、数据来源和限制；不通过整理文档改变数值、模型标签或轨迹选择。
- 完整轨迹仍存于 TSUBAME／本地，不随本次文档整理上传。
