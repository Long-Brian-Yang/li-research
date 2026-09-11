# LZOC：候选结构检查与后续 MD 方案

## 当前结论

采用候选 3，组成为 Li42Zr24O12Cl114（192 原子），对应
Li1.75ZrCl4.75O0.5。已完成 55 ps 制备及额外 50 ps、300 K/1 bar
NPT 平衡。后者任务号 8634186，实际运行耗时 54 分 22 秒。

末段局部配位相近、密度不再持续单向下降；仍可能存在缓慢松弛。
可以作为探索性 MD 的起始结构，但不宣称完全收敛、完全非晶化或势函数
已被实验验证。不再增加候选结构。NEP89/GPUMD 部署已取消，继续使用 MACE。

- [平衡后检查、RDF 与数值](../materials/candidates/LZOC/equilibration_8634186/analysis/README.md)
- [制备后初步检查](../materials/candidates/LZOC/completed_reference_trials/candidate3_check/README.md)
- [三组制备归档](../materials/candidates/LZOC/completed_reference_trials/README.md)

## 讨论中的四温度方案：尚未提交

| 项目 | 设置 |
|---|---|
| 模型 | MACE-MPA-0 |
| 初始结构 | 候选 3，采用新增 50 ps 平衡后的结构 |
| 温度点 | 600、700、800、900 K |
| 每个温度 | 升温 → 50 ps 目标温度平衡 → 200 ps production |
| Production 系综 | NVT |
| 时间步长 | 0.5 fs |
| 组数 | 每个温度先 1 组，共 4 个温度分支 |
| 目标分析 | MSD、D(T)、Arrhenius/Ea、结构与热力学稳定性、分段收敛性 |

300 K 已完成的平衡不能替代各目标温度的平衡。升温时长、目标温度平衡
使用的系综及 NVT 体积选择尚待在运行输入中明确；上述讨论不是已提交任务。
200 ps 不保证扩散收敛，应保留原始数据并按统计质量判断是否需要延长。
同一起始非晶结构的四个温度分支不是四个独立非晶构型。

## 与参考 AIMD 的关系

参考 Kim 等（2025），DOI [10.1038/s41467-025-65702-2](https://doi.org/10.1038/s41467-025-65702-2)。
此前核实并整理的 AIMD 条件为 NVT、600–900 K、2 ps 升温、300 ps
production、2 fs 时间步长、80 fs 温控周期。

**核实的是 600–900 K 范围；600/700/800/900 K 这一离散列表是本项目
建议方案，不声称已逐点核实为原文温度列表。** 我们保留 0.5 fs 和讨论过的
200 ps，因此属于参考 AIMD 温度范围，不是完全复现 AIMD 设置。

论文相关 AIMD 组成为 Li2.5ZrCl5.5O0.5，与本项目组成不同；不能直接
把不同组成的传导率或 Ea 当作同一体系的验证目标。

- [日语阅读报告及 AIMD 条件](literature/lzoc_top3/reading_report_ja.md)
- [英语阅读报告及 AIMD 条件](literature/lzoc_top3/reading_report_en.md)

此前聊天提供的 `reading_report_zh.md` 链接不存在，应以上面已存在的
日语或英语报告为准。

## 存储范围

GitHub 保存本次方案、结构端点、日志、RDF 数值和检查脚本。
完整轨迹保存在 TSUBAME 与本地，不提交到 Git。
