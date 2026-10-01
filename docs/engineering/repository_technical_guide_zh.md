# Li Research 仓库技术总览

本文是仓库的工程入口，集中说明目录职责、运行环境、TSUBAME 部署与构建、核心代码、材料分析代码、测试及数据归档规则。科研结果和文献叙事仍以 [日文 Material Review](../materials/materials_overview_ja.md) 与 [英文 Material Review](../materials/materials_overview_en.md) 为准；本文说明“代码如何产生和核查结果”，不复制结果正文。

> **状态口径：** 本文仅依据 Git 中可见的脚本、配置和文档整理。TSUBAME 上的实际软件版本、模型文件是否存在、队列状态和完整轨迹不能由本地仓库单独确认。凡未由版本化文件固定的内容均标作“集群侧/需现场确认”。

## 1. 项目边界与建议阅读顺序

该仓库包括晶态 benchmark、非晶固体电解质建模与输运分析、MLIP/MD 引擎比较、文献数据整理和企业报告证据。它不是一个单一的 Python 应用：复用算法、一次性科研分析、HPC 构建和具体计算输入分属不同目录。

建议阅读顺序：

1. [根目录 README](../../README.md)：项目和入口导航。
2. [环境与部署](#3-运行环境与依赖)：本地代码与 TSUBAME 集群环境的边界。
3. [代码地图](#5-核心代码src)：复用模块和各类脚本职责。
4. [分析工作流](#6-分析代码与结果流)：结构、生产 MD、后处理到报告图表的路径。
5. [Material Review](../materials/materials_overview_ja.md)：科学结果、文献比较和结论。

## 2. 仓库目录总图

```text
li-research/
├── README.md                         项目总入口
├── src/li_research/                  可复用 Python 模块
├── scripts/structures/               材料/研究任务脚本：准备、分析、作图、提交
├── hpc/                              TSUBAME 路径、构建、benchmark、输入、生产和检查
├── simulation/                       引擎专用 LAMMPS 输入及测试说明
├── structures/                       CIF、明确占位结构和计算输入结构
├── materials/
│   ├── candidates/                   候选构建、准备结构、验证和 provenance
│   ├── evidence/                     报告引用的命名结构与代表轨迹；见本地 manifest
│   └── references/                   文献结构/来源材料
├── results/                          派生表、报告图、分析快照和历史结果
├── docs/
│   ├── materials/                    当前科学综述、定义、图与 figure manifest
│   ├── development/                  benchmark、协议、开发计划与技术结果
│   ├── literature/                   论文笔记、DOI 和来源核对
│   ├── presentations/                中期/最终发表内容
│   └── daily_reports/                按日期保存的阶段记录
└── tests/                            算法约定、数据契约和图表检查
```

代码目前已按“可复用库 / 任务脚本 / HPC 部署 / 输入模板”分区。`scripts/structures/` 中有脚本按同目录模块名导入其他脚本，测试也有直接按路径加载脚本的情况；因此未经导入依赖审计，不要只为目录整齐而批量移动或改名。当前安全的整理方法是保留稳定路径、使用本索引维护用途与阶段标签。

## 3. 运行环境与依赖

### 3.1 两类运行环境

| 环境 | 用途 | 仓库内依据 | 不由仓库保证的部分 |
|---|---|---|---|
| 本地开发机 | 阅读/编辑 Markdown、运行轻量分析和测试 | `src/`、`scripts/`、`tests/` | 没有版本锁定的 Python 环境文件；本机安装包版本不代表 TSUBAME 版本 |
| TSUBAME `tgj-26ICP` | GPU MD、构建引擎、生产计算和大轨迹后处理 | `hpc/tsubame_26icp/config/yang_paths.sh`、SGE 作业脚本和构建脚本 | 登录账号权限、节点模块、模型/二进制是否存在、队列资源、实际运行状态需登录集群确认 |
| 共享 NEP/GPUMD 环境 | 团队共享的 GPUMD+NEP89 小型验证路径 | `hpc/shared/nep89_gpumd/` | 共享路径和权限仅适用于文档指定的项目组，不可视作通用安装 |

仓库**没有**可直接 `pip install -e .` 的 `pyproject.toml`/`setup.py`，也没有 `requirements.txt`、Conda YAML、容器或锁文件。因此不要声称项目有一个完全固定、可在任意机器复现的 Python 环境。

### 3.2 TSUBAME 路径与工具链

规范变量定义在 [`yang_paths.sh`](../../hpc/tsubame_26icp/config/yang_paths.sh)：

| 变量 | 默认职责/路径 |
|---|---|
| `YANG_ROOT` | `/gs/fs/tgj-26ICP/uf03782/yang` 用户工作根目录 |
| `PROJECT_ROOT` | `$YANG_ROOT/li-research` 仓库副本 |
| `ENV_ROOT` | `$YANG_ROOT/envs`，Python 环境父目录 |
| `STRUCTURES_ROOT`, `MODELS_ROOT`, `ENGINES_ROOT` | 结构、模型权重、编译引擎所在目录 |
| `BENCHMARKS_ROOT`, `RUNS_ROOT`, `RESULTS_ROOT` | benchmark、运行工作区、派生结果根目录 |
| `MACE_ENV`, `SEVENNET_ENV`, `MATGL_ENV` | 三个相互隔离的 Python 环境 |
| `MACE_LMP_MLIAP`, `SEVENNET_LMP`, `MATGL_LMP` | 对应模型后端的 LAMMPS 可执行文件 |
| `GPUMD_ENGINE`, `NEP89_MODEL` | GPUMD 可执行文件和 NEP89 势文件 |

集群配方中实际出现的工具链如下。版本按各脚本记载，不应将不同引擎的 CUDA/OpenMPI 组合混为一套：

| 引擎/后端 | Python 环境或二进制 | 构建时模块/特征 | 说明 |
|---|---|---|---|
| MACE-MPA-0 / MACE-MP-0b3 + LAMMPS ML-IAP/Kokkos | `mace_env`；脚本注释和 wheel 路径指向 Python 3.10 | GCC 14.2.0、CUDA 12.8.0、OpenMPI 5.0.7-gcc、Kokkos Hopper90/SM90 | GPU 预检查脚本另检查 PyTorch、MACE、cuEquivariance 与 CuPy；确切包版本未锁定 |
| SevenNet + LAMMPS e3gnn | `sevennet_env` | GCC 14.2.0、CUDA 12.8.0、OpenMPI 5.0.7-gcc；patched LAMMPS | env 中 Python/Torch 精确版本未在仓库锁定 |
| M3GNet/MatGL + LAMMPS | `matgl_env`；MatGL source/build 位于 `engines/` | GCC 14.2.0、OpenMPI 5.0.10-gcc、Kokkos CUDA、SM90 | CPU 与 GPU 后端独立 benchmark；MatGL/PyTorch 版本需集群侧核对 |
| GPUMD/NEP89 | 编译好的 GPUMD/NEP 二进制和 NEP89 文本权重 | GPUMD 构建配方使用 GCC 14.2.0 + CUDA 13.1.1；共享 helper 加载 CUDA 12.8.0 | 按目标二进制的编译配置使用模块；不要把两个脚本的 CUDA 版本视为同一构建 |
| NequIP/Allegro | `allegro_env` 配方 | GCC、CMake、OpenMPI；需目标元素 checkpoint 和 `pair_allegro` | 独立/实验路线；无适用 checkpoint 时不可用于生产 |

H100/Compute Capability 9.0 是若干 GPU 构建脚本中的编译目标，不代表每个作业都已实测可用。模型权重、GPU LAMMPS/GPUMD 二进制和 Conda/venv 本体都不随 Git 提交。

### 3.3 Python 科学计算依赖

从当前 Python 源码 imports 可确认主要依赖族为：

- **结构与轨迹**：ASE；特定轨迹诊断用 MDAnalysis。
- **数值计算**：NumPy、SciPy。
- **绘图**：Matplotlib。
- **论文补充材料/表格提取**：OpenPyXL。
- **测试**：pytest 运行测试函数和 `unittest` 测试类。
- **标准库**：argparse、csv、json、hashlib、pathlib、subprocess、typing 等。

这是按源代码 imports 整理的依赖清单，不是经过版本解析的安装锁文件。MACE、SevenNet、MatGL、PyTorch、LAMMPS、GPUMD、CUDA 和 MPI 属于独立引擎运行栈；不要把它们塞进一个随意拟定的通用 `requirements.txt`。

本次整理时的本地检查环境快照为 Python 3.9、NumPy 1.26.4、SciPy 1.13.0、ASE 3.22.1、Matplotlib 3.8.4；当前环境没有 `pytest`、`MDAnalysis` 或 `openpyxl`。这只是本次审计机器的实测状态，不是项目支持版本或部署锁定。要运行对应的测试/脚本需按模块实际依赖安装；集群 MLIP/GPU 软件栈以 TSUBAME 配置为准。

## 4. 部署、构建与作业入口

### 4.1 规范部署目录

```text
hpc/tsubame_26icp/
├── config/       yang_paths.sh：所有集群路径变量的唯一规范入口
├── build/        引擎编译、安装/接口构建及 Allegro checkpoint 编译
├── benchmark/    短时、共结构的模型/后端速度测试
├── inputs/       MACE-LAMMPS 输入模板及模型转换帮助
├── production/   晶体和非晶结构的长时作业及其 LAMMPS/GPUMD 输入
└── validation/   环境路径和 GPU Python 栈预检查；不等同于科学验证
```

### 4.2 集群侧标准步骤

以下命令描述流程；需要在有权限的 TSUBAME 登录环境中执行。本文本身不会提交作业或改变队列。

1. **检查工作副本与统一路径配置。** 作业应 source `config/yang_paths.sh`，优先使用变量而非重复硬编码路径。
2. **构建/确认运行时。** 选用 `build/` 中与目标后端匹配的脚本；检查 model、engine、结构格式及 CUDA/MPI 接口匹配。
3. **静态检查与环境预检。** 在集群端运行：

   ```bash
   bash -n hpc/tsubame_26icp/build/build_mace_mliap_gpu_maceenv.sh
   bash hpc/tsubame_26icp/validation/validate_project.sh
   ```

`validate_project.sh` 会检查集群路径、模型、可执行文件、结构文件、HPC Shell 语法以及 Python 包导入。它依赖完整 TSUBAME 环境，不是本地 CI；缺少集群文件会正常报错。

4. **先短 benchmark/smoke，再正式生产。** benchmark 用于计算后端的运行速度；production 脚本可能创建运行目录并提交/执行大量 MD，运行前需逐项核对温度、原子数、时间步、模拟时长、模型、输入结构和输出目录。
5. **按运行目录保留 provenance。** 生产脚本中可见的最佳实践包括复制输入、写 settings/provenance、记录 SHA256、保留 stdout/stderr、thermo、restart 和 completion marker。完成标记只说明程序结束/基础数值检查通过，不等于结构、势函数或输运结论已经科学验证。
6. **把大原始输出留在集群/本地归档。** 向 Git 纳入可解释的分析表、图、输入元数据、哈希和抽样 evidence，不纳入整条大型轨迹/检查点。

团队共享 GPUMD 入口单独维护在 [`hpc/shared/nep89_gpumd/`](../../hpc/shared/nep89_gpumd/README_ja.md)：`paths.sh` 载入其编译所需模块并设置共享 GPUMD/NEP89 路径，`run_gpumd.sh` 从用户自己的工作目录读取 `model.xyz`、`run.in` 并将每个作业结果写入用户专属结果目录，`run_1ps.in` 是连接性 smoke input。共享模型和可执行文件按只读使用；该入口不是新材料结构的验证协议。

### 4.3 构建入口索引

| 构建内容 | 规范入口 |
|---|---|
| MACE ML-IAP/Kokkos LAMMPS | [`build_mace_mliap_gpu_maceenv.sh`](../../hpc/tsubame_26icp/build/build_mace_mliap_gpu_maceenv.sh) |
| SevenNet e3gnn/parallel LAMMPS | [`build_sevennet_parallel_gpu.sh`](../../hpc/tsubame_26icp/build/build_sevennet_parallel_gpu.sh) |
| MatGL/M3GNet Kokkos GPU LAMMPS | [`build_matgl_m3gnet_gpu.sh`](../../hpc/tsubame_26icp/build/build_matgl_m3gnet_gpu.sh) |
| GPUMD/NEP | [`build_gpumd.sh`](../../hpc/tsubame_26icp/build/build_gpumd.sh) |
| Allegro LAMMPS 与模型转换 | [`build_allegro_lammps.sh`](../../hpc/tsubame_26icp/build/build_allegro_lammps.sh)、[`compile_allegro_model.sh`](../../hpc/tsubame_26icp/build/compile_allegro_model.sh) |
| MACE checkpoint 转 LAMMPS ML-IAP 格式 | [`inputs/mace_mliap/README.md`](../../hpc/tsubame_26icp/inputs/mace_mliap/README.md) |

规范 benchmark 入口（均是 TSUBAME SGE 作业脚本）：`benchmark/gpumd_nep89_300K_2x2x4.sh`、`benchmark/gpumd_nep89_400K.sh`、`benchmark/gpumd_nep89_smoke.sh`、`benchmark/mace_mp0b2_small_mliap_benchmark.sh`、`benchmark/mace_mp0b3_medium_mliap_canonical_benchmark.sh`、`benchmark/mace_mpa0_medium_mliap_canonical_benchmark.sh`、`benchmark/matgl_m3gnet_cpu_benchmark.sh`、`benchmark/matgl_m3gnet_gpu_benchmark.sh`、`benchmark/sevennet_nano_serial_benchmark.sh`、`benchmark/sevennet_parallel_benchmark.sh`。

`inputs/mace_mliap/` 含两个 readme/conversion 辅助文件及六个晶体 LAMMPS 输入：Li₃YCl₆/LiNbOCl₄ 的 400 K 生产模板、两材料的 500 K exploratory 模板、两材料的 cell relaxation 模板。它们是计算模板，不代表相关作业现在仍在运行或是当前唯一模型选择。

规范 production 入口按任务分类如下（`.lmp`/`.py` 是对应运行输入/程序，不一定是直接提交脚本）：

- **晶态三模型：** `production/md_mace_mpa0_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh`、`production/md_m3gnet_gpu_li3ycl6_03_400K_3rep_50ps_eq_500ps_prod.sh`、`production/md_sevennet_nano_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh`。
- **LZOC：** `production/amorphous_compare_20260915.sh`、`amorphous_lzoc_4t.sh/.lmp`、`amorphous_lzoc_candidate.sh/.lmp`、`amorphous_lzoc_equilibrate.sh/.lmp`、`amorphous_lzoc_high_temperature.sh/.lmp`、`amorphous_lzoc_pilot.sh/.py`、`amorphous_lzoc_reference.sh/.lmp`、`amorphous_targeted_diagnostics.sh`、`check_lzoc_virial.sh/.py`、`lzoc192_hold300.sh`、`lzoc_aimd_aligned_80ps.sh`、`lzoc_hussain192_cool.sh`、`lzoc_hussain192_heat.sh`、`lzoc_hussain192_trial.sh`、`lzoc_nep89.sh`、`nep89_npt_extension.sh`。
- **LSZC：** `production/lszc_272_npt.sh`、`lszc_272_release.sh`、`lszc_nep89_preflight.sh`、`lszc_packed272_smoke.sh`、`lszc_paper_temperatures.sh`。
- **Li₃PS₄：** `production/lips_nep89_trial.sh`、`lips_transport_control.sh`。
- **LiPON：** `production/lipon_600K_600ps_repeats.sh`、`lipon_600K_600ps_repeats_R6_R7.sh`、`lipon_nep89_release.sh`、`lipon_nep89_trial.sh`、`lipon_transport_bulk.sh`、`lipon_transport_repeats.sh`。
- **跨材料后续：** `production/portfolio_followup.sh`。

配套输入/检查代码的完整路径：`hpc/tsubame_26icp/production/amorphous_lzoc_4t.lmp`、`amorphous_lzoc_candidate.lmp`、`amorphous_lzoc_equilibrate.lmp`、`amorphous_lzoc_high_temperature.lmp`、`amorphous_lzoc_pilot.py`、`amorphous_lzoc_reference.lmp`、`hpc/tsubame_26icp/production/check_lzoc_virial.py`；`hpc/tsubame_26icp/inputs/mace_mliap/convert_mace_checkpoint_mliap.sh`；`hpc/tsubame_26icp/validation/check_mace_env_gpu.sh`。它们分别是 LAMMPS 输入、NEP/结构诊断或引擎预检查，不应当作通用分析 CLI。

三个会生成材料结构/转换结果的入口支持 `--output-dir`：`scripts/structures/prepare_hussain2024.py` 指向目标 seed 目录，`prepare_lszc_272.py` 指向 seed 输出目录，`prepare_lszc_nep.py` 指向 LSZC 输出根目录。默认值仍是原仓库候选路径；自动化测试传临时目录，避免覆盖跟踪的候选结构。

以上清单只是代码归档，不是“当前生产队列”清单。某些脚本名称带 `trial`, `exploratory`, `followup`, 日期或重复编号；其科学状态和调用路径必须回查对应 README/provenance，不能只凭文件存在判断为正式工作流。

### 4.4 HPC 根目录遗留脚本的使用等级

规范脚本在上述子目录；`hpc/tsubame_26icp/` 根层仍留有早期或专门诊断入口，包括：

`build_mace_mliap_gpu314_b3.sh`、`build_matgl_m3gnet_gpu.sh`、`convert_mace_mliap_compat.py`、`install_cueq_cuda13.sh`、`mace_mp0b3_medium_ase_benchmark.sh`、`mace_mp0b3_medium_mliap_benchmark.sh`、`mace_mp0b3_medium_mliap_cpu_smoke.sh`、`mace_mp0b3_medium_mliap_gpu_diagnostic.sh`、`matgl_m3gnet_cpu_benchmark.sh`、`matgl_m3gnet_gpu_benchmark.sh`、`md_ordered_400K_gpu.sh`、`setup_mace_py314.sh`、`smoke_test_mace_400K_new.sh`。

这些文件没有被删除，避免破坏历史记录或调用点；也不能因此把它们全称为当前支持的入口。尤其根层 `build_matgl_m3gnet_gpu.sh` 含迁移前的 `/gs/fs/tga-ishikawalab/...` 环境路径。**新任务以规范子目录脚本为优先；运行任何根层脚本前须检查路径、模型、环境和输出设置。** `validate_project.sh` 扫描旧路径，发现命中会失败，这是防止误用旧配置的保护行为。

## 5. 核心代码（`src/li_research/`）

`src/` 是可复用工具层，不是当前所有材料任务唯一入口。所有具体数据目录和绘图输出需结合脚本中的常量/参数核对。

| 模块 | 文件 | 职责 |
|---|---|---|
| 晶体构建 | `structures/build_2x2x2.py` | 从初步/截图重建 CIF 生成首轮显式有序 2×2×2 模型并检查计量比、距离 |
| 晶体构建 | `structures/build_li3ycl6_ordered.py` | 枚举占位有序 Li₃YCl₆ 模型和 2×2×2 超胞 |
| 晶体扩胞 | `structures/make_li3ycl6_2x2x4.py` | 从有序 Li₃YCl₆ 2×2×2 构造、验证 2×2×4 |
| 晶体构建 | `structures/make_linboocl4_2x2x3.py` | 构建 LiNbOCl₄ 2×2×3 有序候选 |
| 格式转换 | `conversion/prepare_data.py` | CIF→LAMMPS data；检测 CIF 部分占位以避免未经排序直接投入 MD |
| 格式转换 | `conversion/lammps_data_to_extxyz.py` | LAMMPS data→周期 extended XYZ |
| 格式转换 | `conversion/relaxed_lammps_dump_to_extxyz.py` | 最终 LAMMPS relaxation dump→确定性 GPUMD extxyz |
| LAMMPS 输运分析 | `analysis/lammps/msd_diffusion.py` | 从 LAMMPS custom dump 读取 Li 坐标并计算 MSD/示踪扩散 |
| LAMMPS 输运分析 | `analysis/lammps/analyze_li_jumps.py` | 统计可比较轨迹中的 Li 跳跃 |
| LAMMPS 作图 | `analysis/lammps/plot_selected_msd_three_models.py` | 三模型 Li₃YCl₆ MSD 图 |
| LAMMPS 作图 | `analysis/lammps/plot_linboocl4_msd_three_models.py` | LiNbOCl₄ 三模型 MSD 图 |
| GPUMD 输入/后处理 | `analysis/gpumd/prepare_gpumdkit_unwrapped.py` | 将坐标展开并准备 GPUMDkit MSD 输入 |
| GPUMD 后处理 | `analysis/gpumd/analyze_gpumdkit_windows.py` | 对 GPUMDkit MSD 输出的指定时间窗口拟合并比较 |
| GPUMD 后处理 | `analysis/gpumd/analyze_300K_2x2x4.py` | 分析已完成 300 K、Li₃YCl₆ 2×2×4 GPUMD 轨迹，导出表和图 |
| Arrhenius 作图 | `analysis/arrhenius/plot_li3ycl6_arrhenius_midterm.py` | Li₃YCl₆ 中期 Arrhenius 图 |
| Arrhenius 作图 | `analysis/arrhenius/plot_linboocl4_arrhenius.py` | LiNbOCl₄ Arrhenius 图，区分实验电导参考与实验 tracer-D |
| RDF | `analysis/rdf/recompute_li3ycl6_rdf.py` | 从选定的 600 K LAMMPS 轨迹重新计算 Li₃YCl₆ RDF |

根目录的 `src/README.md` 仅作入口；具体函数定义、单位、分析窗口与输出位置以对应脚本和结果 manifest 为准。
各子目录的 `__init__.py` 是 Python package 标记文件，不含独立的科学计算流程。

## 6. 分析代码与结果流

### 6.1 通用计算链

```text
文献/原始结构
  → 有序/候选结构与 composition 验证
  → LAMMPS data / GPUMD extxyz 格式转换
  → 对应引擎与势函数的短预检、弛豫/平衡
  → 温度/压力路径下生产 MD（原始轨迹留本地/TSUBAME）
  → MSD、D、Arrhenius、RDF/配位/键角/骨架动力学分析
  → 对照实验或文献同定义数值
  → 导出 CSV/JSON、专业图表和来源信息
  → 同步至 Material Review 与 figure manifest
```

### 6.2 `scripts/structures/` 逐组清单

脚本依照文件名和当前实现归为下列任务组；“候选/历史”表示应先查看输入路径和注释，并不等于文件可删除。

| 任务组 | 脚本 | 内容 |
|---|---|---|
| 结构准备/转换 | `prepare_hussain2024.py`, `build_lzoc_reference.py`, `prepare_lszc_272.py`, `prepare_lszc_nep.py`, `prepare_lszc_production.py`, `prepare_lszc_split_followup.py`, `prepare_lips_nep.py`, `prepare_lipon_nep.py`, `pack_lszc.py`, `extract_lszc_clusters.py` | 参考构型重建、非晶候选准备、打包/抽簇及 NEP 输入准备 |
| 证据与结构核查 | `build_material_evidence_package.py`, `structure_followup.py`, `compare_lzoc_candidates.py`, `check_lzoc_candidate3.py`, `check_lzoc_equilibration.py`, `validate_amorphous_trials.py`, `review_release_trials.py`, `refresh_legacy_rdf.py`, `summarize_legacy_highT.py`, `lzoc_order_motion.py`, `lzoc300_structure_motion.py` | 检查结构、哈希、构型差异、有序性/运动特征，构建代表结构/轨迹 evidence |
| LZOC 输运与重复轨迹 | `analyze_lzoc_production.py`, `analyze_lzoc_seed_repeats.py`, `analyze_followup300.py`, `select_lzoc_representatives.py`, `preview_lzoc_closest.py`, `lzoc_table4_comparison.py` | MSD、D、重复轨迹诊断、文献温度点比较与候选分析 |
| LSZC 输运/局部结构 | `analyze_lszc_endpoints.py`, `analyze_lszc_matched_repeats.py`, `extract_tang_transport.py`, `extract_chen_source.py` | 端点/四温度输运、重复轨迹及文献数据提取 |
| Li₃PS₄ 输运/结构 | `analyze_lips_transport.py`, `analyze_lips_r1_remote.py` | 输运、局部配位/角度、异质动力学和结果表 |
| LiPON 输运/结构 | `analyze_lipon_transport.py`, `analyze_lipon_repeats.py`, `analyze_lipon_600k_long.py`, `analyze_lipon_precontact.py` | 输运/Arrhenius、重复轨迹、长时间温度点、短接触诊断 |
| 多材料汇总 | `finish_amorphous_analysis.py`, `complete_amorphous_comparisons.py`, `finish_materials_transport.py`, `paper_aligned_analysis.py`, `legacy_paper_alignment.py`, `portfolio_supplement.py`, `analyze_targeted_diagnostics.py` | 汇总多材料输运/文献比较/诊断；历史脚本先与当前报告状态核对 |
| 作图和报告资产 | `plot_amorphous_arrhenius_comparisons.py`, `plot_lips_r1_report.py`, `plot_literature_correspondence.py`, `plot_lzoc_preparation.py`, `plot_targeted_diagnostics.py`, `plot_legacy_lzoc_comparison.py`, `curate_overview_figures.py`, `li_diffusion_style.py` | Arrhenius、结构、诊断、统一风格、报告图更新和 figure manifest 整理 |
| TSUBAME 作业包装 | `submit_lips_r1_analysis.sh`, `submit_lps_r1_transport.sh`, `submit_lszc_endpoint_npt150.sh`, `submit_lszc_matched4t.sh`, `submit_lszc_production300.sh`, `submit_lszc_split50.sh`, `submit_lzoc_nhc300.sh`, `submit_lzoc_seed300.sh`, `submit_preparation_repeats.sh` | SGE job wrappers；可能执行远端计算，不能当作普通本地脚本随意运行 |

其中具体输入/输出常由脚本顶部路径常量、CLI 参数、TSUBAME `RUNS_ROOT` 或对应结果目录决定。执行分析前先阅读该脚本的 `main()/run()` 和路径变量，并从当前结果的 `README.md`/manifest 确认数据版本；不要用旧脚本对新轨迹覆盖正式结果。

### 6.3 分析方法与语义边界

- **MSD/D：** 读取轨迹、处理周期边界/坐标展开，再在脚本定义的时间窗拟合 MSD 斜率；不同脚本可能使用单原点或多原点平均、不同窗口和粒子选择，必须按输出表/源码核对定义。
- **Arrhenius：** 以温度和扩散系数或条件 Nernst–Einstein 电导率拟合；实验若只给室温电导与 (E_a)，只能构造实验电导参考线，不能称为实验 tracer diffusion 曲线。文中公式与单位集中列在 Material Review 的定义章节。
- **RDF/配位/键角：** 依照周期最小镜像距离及脚本截断定义统计局部结构；分析结果应包含来源轨迹、温度、取样区间和 cut-off 元数据。
- **轨迹稳定性：** 温度、能量、体积、压力、最小距离和成分守恒是计算/结构检查，不等价于实验预测准确性。
- **复现与文献对照：** 相同物理量、组成、温度、边界/ensemble 和单位才可直接数值对比；NEP、MACE 等通用预训练势得到的偏差必须保留在结论中。

## 7. 输入、输出、报告与溯源

| 文件位置 | 内容/权威性 |
|---|---|
| `structures/raw/`, `structures/reference/` | 来源/重建 CIF；部分占位结构须先排序，不可默认直接用于 MD |
| `structures/ordered/` | 晶态显式全占位模型和结构说明 |
| `materials/candidates/<material>/` | 非晶候选、初始模型、制备协议、验证 JSON、特定 provenance；存在 archive 子目录 |
| `materials/evidence/` | 报告用命名结构与抽样轨迹；`README.md` 及 `manifest.json` 记录名称、图号、来源；抽帧 XYZ 用于可视化/检查，不替代完整轨迹定量分析 |
| `docs/materials/figures/` | 主报告当前图；`manifest.json` 管理图名/来源 |
| `results/publication_all_materials/` | 当前发表图包、supplementary、源数据与图组 |
| `results/midterm_Li3YCl6_MACE_M3GNet/` | 中期展示快照和配套分析 |
| `results/amorphous_review_20260915/` | 多材料非晶分析的日期版本结果，含若干按分析主题拆分的目录 |
| `results/amorphous_validation_20260914/` | 较早非晶准备/验证快照 |
| `results/LZOC/`, `results/gpumd_nep89/`, `results/analysis/` | LZOC 专项、GPUMD 旧路线与附加分析结果；需读其目录 README 识别现行性 |
| `runs/` | 本地运行历史/忽略输出目录；完整 production 原始轨迹优先留本地或 TSUBAME |

Git 忽略策略见根 `.gitignore`：模型 `*.model`/`*.pt`、大轨迹 `*.lammpstrj`、restart/dump/data、`runs/` 和论文原始下载 source 常不入库。分析复核依靠提交的必要输入、CSV/JSON、文件哈希、图、manifest 及证据抽样；无法从 Git 单独还原的源轨迹应标明 TSUBAME/本地来源，不能伪称仓库已包含。

## 8. 测试与验证

仓库当前有 43 个 `tests/` 文件，混用 pytest 函数和 unittest 类。轻量本地入口为：

```bash
python -m pytest -q
```

它需要 pytest 及测试 imports（最低限度常见为 NumPy、ASE、Matplotlib；部分组还需 SciPy、MDAnalysis、OpenPyXL），并从仓库根目录运行。标准库备选 `python -m unittest discover -s tests` 不会发现所有 pytest 风格的自由测试函数，只覆盖 unittest 测试类。没有 requirements lock，因此若测试因模块缺失失败，应先记录实际依赖缺口，不应把未安装直接报告为代码回归。

本次本地环境没有 pytest，因此用标准库命令实际执行了 unittest 子集（74 tests）；pytest 风格测试未在该环境运行，不能据此宣称全体 43 个测试文件均通过。三项结构生成/转换测试现在都将结果写入临时目录；直接运行生成脚本时不传参数，仍会使用历史默认输出路径。

测试按职责覆盖：

| 测试主题 | 代表文件 |
|---|---|
| LZOC 结构、MD 协议、输运、参考文献 | `test_lzoc_*.py`, `test_hussain2024.py`, `test_candidate_structure_comparison.py` |
| LSZC 结构、重复计算、四温度图和配位 | `test_lszc_*.py`, `test_pack_lszc.py` |
| Li₃PS₄/LiPON 输运和局部结构 | `test_lips_*.py`, `test_lipon_*.py` |
| 多材料汇总、验证与证据包 | `test_finish_*.py`, `test_amorphous_*.py`, `test_material_evidence_package.py`, `test_preparation_repeats.py`, `test_release_review.py` |
| 图表/Markdown/报告约定 | `test_*figure*.py`, `test_markdown_math_rendering.py`, `test_company_report_tone.py`, `test_portfolio_supplement.py` |
| GPUMD 与分析约定 | `test_shared_gpumd.py`, `test_nep89_npt_extension.py`, `test_lips_transport_analysis.py`, `test_paper_aligned_analysis.py` |

本地 pytest 只验证代码/文件约定；它不会验证 CUDA、模型文件、LAMMPS/GPU 二进制、TSUBAME 路径或 scheduler。集群环境检查使用前述 `validation/` 脚本；真实 MD 是否正确还需 thermodynamics、结构和文献对应分析。

## 9. 维护规则与当前整理结论

1. 根 README 负责项目定位和导航；详细工程事实只维护在本技术总览及各源代码近邻 README，科学结论维护在 Material Review。
2. 改动后端环境时，同步 `yang_paths.sh`、相应 `build/` 入口、验证脚本和本文环境表；不要凭记忆添加版本号。
3. 新增可复用通用函数放 `src/li_research/`；依赖材料专用输入/报告路径的工作流留在 `scripts/structures/`，HPC submit/build wrapper 留在 `hpc/`。
4. 新脚本头部写明目的、输入、输出、所需环境/模型和是否会提交作业；结果脚本保留 provenance/hash。
5. 旧脚本不因命名过时就删除。先搜索调用、测试、报告引用和运行记录；若仍不确定，标为历史/未验证，继续保留。
6. 更新文档时检查日英 Material Review、figure manifest、证据包和结果 README 是否引用同一数据版本；不能只改一处造成版本漂移。

本轮仓库审计能安全确认：核心目录边界基本存在，主要工作缺口是入口文档重复/过时、HPC 根层旧脚本缺少状态标记、依赖没有锁定。代码暂不批量迁移或删除；本指南提供逐目录地图和环境部署路径，后续若要做物理重构，应单独制定兼容性迁移与逐步测试计划。
