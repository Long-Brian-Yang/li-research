# Li Research — Halide Solid Electrolytes

卤化物/卤氧化物固态电解质的文献整理、方向 2 复现和方向 3 候选材料开发。

## Project map

| Area | Contents |
|---|---|
| [`docs/literature/`](docs/literature/) | 中文/日语论文笔记、关键词、DOI 与横向表格 |
| [`docs/development/`](docs/development/) | 开发目标、方向 2 方案、方向 3 方案与筛选矩阵 |
| [`structures/`](structures/) | 参考结构、照片重建 CIF、后续有序模型入口 |
| [`simulation/`](simulation/) | MACE-MPA-0、LAMMPS 输入、数据转换和扩散分析 |
| [`hpc/tsubame_26icp/`](hpc/tsubame_26icp/) | TSUBAME 26ICP 作业入口 |

## Start here

- [中文论文笔记](docs/literature/papers_zh.md) · [日本語論文ノート](docs/literature/papers_ja.md)
- [中文开发矩阵](docs/development/development_matrix_zh.md) · [日本語開発マトリクス](docs/development/development_matrix_ja.md)
- [方向 2 研究方案](docs/development/direction2_plan_zh.md)
- [方向 3 日本語開発計画](docs/development/development_plan_ja.md)
- [结构数据说明](structures/README.md)
- [MACE-MPA-0 总说明](simulation/mace_mpa0/README.md)
- [MACE + LAMMPS 说明](simulation/mace_mpa0/lammps/README.md)
- [TSUBAME 26ICP job](hpc/tsubame_26icp/job_lammps.sh)

## Current scope

方向 2 目前优先复现 Li₃YCl₆ 和 LiNbOCl₄；方向 3 以 Li–Zr–Al–O–Cl 低成本体系为开发基线。照片重建 CIF 仅用于结构核对，不能直接用于生产 DFT/MD；必须先建立明确的有序模型。
