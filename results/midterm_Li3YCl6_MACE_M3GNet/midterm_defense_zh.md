# Li₃YCl₆ 中期答辩整理

## 1. 研究主题

本阶段以 Li₃YCl₆ 为代表材料，使用 MACE、M3GNet 和 SevenNet 三个模型。论文信息和 benchmark 结果将在后文说明。

## 2. 材料简介：Li₃YCl₆

Li₃YCl₆ 是氯化物型锂离子固态电解质，具有用于全固态锂电池高电压正极的研究价值。Asano 等人的研究报道了室温 mS/cm 级别的 Li⁺ 电导率（超过 1 mS/cm），因此 Li₃YCl₆ 可作为氯化物固态电解质研究中的代表性 benchmark。

基于文献结构，建立了适用于 MD 计算的有序结构模型。本阶段结果用于在同一结构模型上比较 MACE 与 M3GNet 的 Li⁺ 输运趋势。

### 结构要点

- 该材料属于氯化物阴离子骨架中的 Li⁺/Y³⁺ 卤化物 framework，代表性晶体学描述为 $P\bar{3}m1$（No. 164）。
- 基于文献结构，建立了适用于 MD 的 full-occupancy 有序模型。
- 在有序模型基础上建立 supercell，用于周期性边界条件下的 Li⁺ 迁移分析。

## 3. 模型环境的构建顺序

环境按照“复现既有方法 → 建立 GPU 版本 → 引入新模型”的顺序逐步构建。

1. **M3GNet + LAMMPS CPU**：复现 NGK 侧使用过的计算环境。
2. **M3GNet + LAMMPS GPU**：在本研究侧使用相同模型的 GPU backend。
3. **MACE + LAMMPS GPU**：作为本研究新增的通用模型环境。
4. **SevenNet + LAMMPS**：作为本研究新增的比较模型环境。

通过这一顺序，可以区分势函数模型差异与 CPU/GPU 运行后端差异。GPU 主要改善计算速度，并不意味着 GPU 版本的模型精度会自动更高。

## 4. 现有计算的问题

- 既有结果缺少与实验值和企业参考值的统一比较。
- 计算环境和输入条件不够统一，结果复现困难。
- 现有流程不适合直接进行长时间、大规模离子输运 MD。

## 5. 本阶段的改进方案

### 模型

本阶段纳入 benchmark 的通用机器学习势如下。

| 模型 | 代表论文 | DOI / 文献链接 |
|---|---|---|
| <img src="https://github.com/ACEsuit.png?size=96" width="48" alt="MACE logo"> **MACE** | **A foundation model for atomistic materials chemistry** | [arXiv:2401.00096](https://arxiv.org/abs/2401.00096) |
| <img src="https://github.com/materialyzeai.png?size=96" width="48" alt="M3GNet logo"> **M3GNet** | **A universal graph deep learning interatomic potential for the periodic table** | [10.1038/s43588-022-00349-3](https://doi.org/10.1038/s43588-022-00349-3) |
| <img src="https://raw.githubusercontent.com/MDIL-SNU/SevenNet/main/SevenNet_logo.png" width="48" alt="SevenNet logo"> **SevenNet** | **Scalable Parallel Algorithm for Graph Neural Network Interatomic Potentials in Molecular Dynamics Simulations** | [10.1021/acs.jctc.4c00190](https://doi.org/10.1021/acs.jctc.4c00190) |

### 短时间 MD benchmark

使用相同的 Li₃YCl₆ 2×2×2 结构（240 atoms），先进行 100 step warm-up，再对 1,000 step 计时。所有速度均统一采用 LAMMPS log 中的 `timesteps/s`。

| 模型／运行方式 | 结构 | GPU / MPI | warm-up + 计时 | 速度 (timesteps/s) | 备注 |
|---|---|---|---:|---:|---|
| MACE-MPA-0-medium / ML-IAP-Kokkos GPU | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **39.176** | canonical interface |
| MACE-MP-0b3-medium / ML-IAP-Kokkos GPU | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **36.938** | canonical interface |
| MACE-MP-0b2-small / ML-IAP-Kokkos GPU | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **53.124** | 短时间 benchmark |
| MACE-MPA-0-medium / legacy GPU interface | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **10.316** | 接口基线 |
| SevenNet-nano / LAMMPS e3gnn | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **69.261** | 已确认 CUDA |
| SevenNet standard / e3gnn/parallel | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **8.579** | 已确认 CUDA-aware MPI |
| M3GNet / LAMMPS matgl/kk GPU | Li₃YCl₆ 2×2×2（240 atoms） | 1 GPU / 1 MPI | 100 + 1,000 | **56.621** | 已确认 GPU backend |
| M3GNet / LAMMPS native CPU | Li₃YCl₆ 2×2×2（240 atoms） | CPU | 100 + 1,000 | **3.285** | CPU 参考 |

- **MACE**：用于结构优化和 LAMMPS MD。
- **M3GNet**：作为已有企业计算路线的对照模型。
- **SevenNet**：作为额外构建的比较模型。

本阶段比较的是通用模型在相同结构、相同温度和相同分析流程下的结果，不将其解释为针对 Li₃YCl₆ 专门微调后的高精度模型。

### 计算引擎

采用 LAMMPS 进行 MD。相较于 Python/ASE 直接驱动，LAMMPS 更适合统一管理 NVT、长时间运行、轨迹输出和重启计算。

## 6. 计算对象与条件

| 项目 | 设置 |
|---|---|
| 材料 | Li₃YCl₆ |
| 结构 | 基于文献结构建立的 Li/Y 有序模型 |
| 超胞 | 2×2×2（全方向周期性边界条件） |
| 结构优化 | 先使用 FIRE 法优化原子位置和晶胞，再进行 MD |
| 温度 | 400、600、800、1000 K |
| 系综 | NVT |
| 温度控制 | Nose–Hoover thermostat |
| timestep | 1 fs |
| 平衡 | 50 ps |
| 生产阶段 | 500 ps |
| 主要扩散分析 | Li 原子 MSD → D → Arrhenius 拟合 |
| MSD 拟合区间 | 去除平衡段后，采用统一的 10–90% 区间 |

## 7. 计算流程

```mermaid
flowchart TD
    A[文献结构] --> B[建立有序模型]
    B --> C[2×2×2 超胞]
    C --> D[FIRE 结构优化]
    D --> E[NVT 平衡<br/>50 ps]
    E --> F[NVT production MD<br/>500 ps]
    F --> G[Li MSD 分析]
    G --> H[扩散系数 D]
    H --> I[Arrhenius 拟合<br/>Eₐ・300 K 外推]
    I --> J[与实验值、NGK 参考值比较]
```

## 8. 中期主要结果

| 模型 | (E_a) | (R^2) | (D(300\,K)) | 说明 |
|---|---:|---:|---:|---|
| MACE-MPA-0 | 0.302 eV | 0.991 | (1.55\times10^{-8}\,\mathrm{cm^2\,s^{-1}}) | Arrhenius 外推（MSD 25–90%） |
| M3GNet (GPU) | 0.212 eV | 0.998 | (1.02\times10^{-7}\,\mathrm{cm^2\,s^{-1}}) | Arrhenius 外推 |
| 实验参考 | 约 0.40 eV | — | (\sigma(300\,K)=5.1\times10^{-4}\,\mathrm{S\,cm^{-1}}) | 文献值 |
| NGK M3GNet (CPU reference) | 约 0.18 eV | — | (\sigma(300\,K)=9.69\times10^{-3}\,\mathrm{S\,cm^{-1}}) | 企业参考值 |

这些结果用于比较模型趋势和工作流一致性；由于使用的是通用模型，不能直接宣称已经达到实验精度。

## 9. 中期主图

![Li₃YCl₆ Arrhenius / Ea 比较](plots/Li3YCl6_Arrhenius_MACE_M3GNet_exp_company.png)

![Li₃YCl₆ MACE-MPA-0 四温度 MSD](plots/Li3YCl6_MSD_4T_MACE_MPA_0.png)

![Li₃YCl₆ M3GNet 四温度 MSD](plots/Li3YCl6_MSD_4T_M3GNet.png)

![Li–Cl RDF](plots/Li3YCl6_LiCl_RDF_600K_MACE_M3GNet.png)

![Y–Cl RDF](plots/Li3YCl6_YCl_RDF_600K_MACE_M3GNet.png)

![Cl–Cl RDF](plots/Li3YCl6_ClCl_RDF_600K_MACE_M3GNet.png)

![Li–Cl 配位数](plots/Li3YCl6_LiCl_coordination_600K_MACE_M3GNet.png)

![Li–Cl 配位数波动](plots/Li3YCl6_LiCl_coordination_fluctuations_600K_MACE_M3GNet.png)

![热力学波动](plots/Li3YCl6_thermodynamic_fluctuations_600K_MACE_M3GNet.png)

## 10. Supplementary 分析

以下内容不作为中期主讲图，但用于确认结果可靠性：

![方向性 MSD](plots/supplementary_priority/Li3YCl6_directional_MSD_600K.png)

![block averaging 扩散误差](plots/supplementary_priority/Li3YCl6_diffusion_block_averaging_600K.png)

![RDF 综合图](plots/supplementary_priority/Li3YCl6_RDF_600K.png)

![Li 跳跃与 Van Hove](plots/supplementary_priority/Li3YCl6_jump_and_van_hove_600K.png)

![晶胞稳定性](plots/supplementary_priority/Li3YCl6_thermo_cell_stability_600K.png)

![热力学稳定性](plots/supplementary_priority/Li3YCl6_thermodynamic_stability_600K_MACE_M3GNet.png)

## 11. 图表解释要点

### Arrhenius 图

横轴为 (1000/T)，纵轴为 (ln D)。直线斜率对应活化能 (E_a)。虚线部分是根据高温 MD 结果向 300 K 的外推，不是 300 K 的直接 MD 计算。MACE-MPA-0 与 M3GNet 的 (E_a) 和外推值不同，说明通用势函数对 Li⁺ 迁移势垒的描述存在模型依赖性。

### MSD 图

MSD 随时间近似线性增长，表示 Li⁺ 已进入扩散阶段；斜率越大，扩散越快。低温下曲线斜率较小、统计波动更明显，因此低温 MSD 主要用于确认趋势，扩散系数应结合统一拟合区间和多温度 Arrhenius 分析判断。

### RDF 图

Li–Cl、Y–Cl 和 Cl–Cl RDF 用于比较局部配位环境和阴离子骨架。峰位置反映平均近邻距离，峰宽和峰高反映热振动及局部结构分布。两种模型的峰位置相近时，说明它们给出了相似的局部结构；峰形不同则表示模型对局部无序程度的描述不同。

### 配位数图

Li–Cl 配位数由 Li–Cl RDF 的第一配位壳层积分得到，用于补充 RDF 的定性判断。它反映 Li 周围平均 Cl 配位环境，不应直接等同于固定晶体学配位数。

### 热力学波动图

温度、势能、总能量和压力在生产阶段围绕平均值波动，且没有持续漂移，说明该段 MD 在数值上保持稳定。稳定性判断应关注是否存在突发能量漂移或温度失控，而不是要求曲线完全水平。

### 结果边界

本阶段的重点是验证工作流和比较通用模型趋势。MACE-MPA-0 与 M3GNet 均未针对 Li₃YCl₆ 专门 fine-tune，因此 (D)、(E_a) 和 300 K 外推值不能直接替代实验测量值。后续若需要提高定量精度，应使用 DFT/AIMD 数据进行验证或微调。

## 12. 中期结论

本阶段完成了 Li₃YCl₆ 的有序结构、supercell、通用机器学习势、LAMMPS MD 和扩散分析流程。MACE-MPA-0 与 M3GNet 在相同计算条件下均可完成稳定 MD，并能得到可拟合的温度依赖扩散结果。

下一阶段将重点放在统一轨迹来源、误差与收敛性评估，以及将同一套分析流程扩展到 LiNbOCl₄ 和其他候选固态电解质。
