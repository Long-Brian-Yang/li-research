# Li1.75ZrCl4.75O0.5：正式结构入口

以后直接查看本目录即可。当前选择候选 3，192 原子：Li42Zr24O12Cl114。

| 用途 | CIF（查看结构） | LAMMPS data（计算） |
|---|---|---|
| 能量最小化后的结构 | [structure_minimized.cif](structure_minimized.cif) | [structure_minimized.data](structure_minimized.data) |
| 最新 300 K、50 ps 平衡后的结构，后续 MD 起点 | [structure_equilibrated_300K.cif](structure_equilibrated_300K.cif) | [structure_equilibrated_300K.data](structure_equilibrated_300K.data) |

两个结构属于同一候选的不同阶段。最小化结构来自制备任务 8631935.3，
原子力已收敛，属于固定晶胞的原子位置优化；并不是完整晶胞优化。
最新结构来自随后平衡任务 8634186，含有限温度热涨落，不能称为零温最小能结构。
Data 中的原子类型 1/2/3/4 对应 Li/Zr/O/Cl；CIF 仅供结构查看，不携带速度。

目前结构可作为探索性 MD 的起点，但未声称完全非晶化、完全收敛或已被实验验证。

## 后续方案

MACE，600/700/800/900 K，每温度先一组：升温 → 50 ps 目标温度平衡 →
200 ps NVT production，时间步长 0.5 fs。温度列表是本项目方案，参考文献
已核实的温度范围为 600–900 K，不声称原文就是这四点。
已提交任务数组 **8635176.1–4**，详见 [运行设置与输出路径](MD_4T_8635176.md)。

## 归档（通常不需要打开）

历史候选、原始日志、中间结构和检查数据统一放入 [archive/](archive/)。
保留它们是为了追溯结果，不需要在这些文件中挑选正式结构。

- [最新检查结论](archive/equilibration_8634186/analysis/README.md)
- [三组制备记录](archive/completed_reference_trials/README.md)
- [详细运行方案](../../../docs/materials/LZOC/lzoc_next_md_plan_2026-09-11.md)

本次整理仅修改本地/GitHub 布局；TSUBAME 原始运行路径未移动，实际运行
脚本快照及 provenance 中的历史路径保持原样。轨迹不上传 GitHub。
