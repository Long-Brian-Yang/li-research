# 方向 2 研究方案：高 Li⁺ 传导结构筛选

## 0. 研究定义

**方向 2 的核心问题：**

> 在高对称性、空位工程和 mixed-anion 结构中，找出具有连续 Li⁺ 三维迁移网络、低迁移能垒并达到 σ<sub>Li</sub> >10 mS cm⁻¹ 的固态电解质。

本阶段暂定比较两种结构：

1. **Li₃YCl₆**：P\bar3m1（No. 164），高电压卤化物 benchmark。
2. **LiNbOCl₄**：Cmc2₁（No. 36），mixed-anion oxyhalide，高传导重点候选。

仓库中的两个 CIF 目前都是由截图重建的 provisional 版本，不能直接作为最终生产计算输入。

## 1. 总体路线

```text
原始 CIF 复核
  ↓
占位/无序模型生成
  ↓
结构标准化与 DFT 弛豫
  ↓
热力学与动力学稳定性筛选
  ↓
短时间 AIMD 初筛
  ↓
长时间 AIMD 或 ML-MD
  ↓
MSD → DLi → σLi
  ↓
迁移通道、空位和结构描述符分析
  ↓
候选排序与下一轮结构设计
```

## 2. Phase 0：结构文件和数据完整性

### 必须完成

- 获取 Li₃YCl₆ 和 LiNbOCl₄ 的原始 CIF，而不是截图重建版。
- 核对空间群、晶格参数、原子坐标、占位率、ADP 和化学计量。
- 对部分占位生成多个显式有序模型；每个模型保留唯一 ID。
- 检查模型的总化学式、电荷平衡和最短原子间距。

### 输出

```text
structures/raw/Li3YCl6_original.cif
structures/raw/LiNbOCl4_original.cif
structures/ordered/Li3YCl6_ordered_*.cif
structures/ordered/LiNbOCl4_ordered_*.cif
structures/structure_manifest.csv
```

### Gate 0

没有原始 CIF 或无法解释部分占位时，不进入正式 MD；只能进行模型开发和敏感性分析。

## 3. Phase 1：结构标准化与 DFT 弛豫

对每个有序模型：

1. 标准化晶胞和原子排序。
2. 进行离子位置、晶格参数和体积弛豫。
3. 检查是否保持目标空间群，或发生结构畸变。
4. 比较不同有序模型的相对能量。

### 建议记录

| 字段 | 内容 |
|---|---|
| code | VASP / Quantum ESPRESSO 等 |
| functional | 使用的 DFT 泛函 |
| cutoff / k-mesh | 收敛参数 |
| force / stress tolerance | 弛豫标准 |
| relaxed lattice | 弛豫后晶格参数 |
| ΔE | 相对于最低能模型的能量 |
| symmetry change | 是否发生对称性降低 |

### Gate 1

保留：结构弛豫收敛、无异常短键、化学式正确、相对能量合理的模型。删除：明显重构、严重短键或无法收敛的模型。

## 4. Phase 2：热力学和结构稳定性

对通过 Gate 1 的模型计算：

- energy above hull；
- formation energy；
- 声子或有限温度稳定性（资源允许时）；
- 结构在短时间 NVT/NPT MD 中是否保持。

### 初始筛选标准

\[
E_{\mathrm{hull}} < 50\ \mathrm{meV\ atom^{-1}}
\]

该阈值是初筛标准，不代表绝对合成判据。必须同时记录相图来源和计算设置。

## 5. Phase 3：Li⁺ 扩散初筛

### AIMD 设计

对每个候选至少设置多个温度点，例如 300–800 K 的温度区间；实际温度范围根据结构稳定性和 Li⁺ 位移情况调整。

建议先做短时间 AIMD 初筛，再对高潜力模型做长时间计算。所有模型必须使用一致的：

- 时间步长；
- 超胞大小；
- 采样间隔；
- 温度控制方法；
- 预热和生产阶段长度。

### 分析量

1. Li-only MSD；
2. Li self-diffusion coefficient D<sub>Li</sub>；
3. Arrhenius activation energy E<sub>a</sub>；
4. Li vacancy occupation；
5. Li–Li correlation / Haven ratio；
6. Cl/O/Nb/Y framework stability。

由 Einstein relation 得到扩散系数：

\[
D_{\mathrm{Li}}=\frac{1}{6}\frac{d}{dt}\left\langle|r(t)-r(0)|^2\right\rangle
\]

电导率至少同时报告两种定义：

- Nernst–Einstein conductivity：从 Li self-diffusion 得到；
- collective/Green–Kubo conductivity：考虑 Li–Li 相关运动。

不能把 Nernst–Einstein 结果直接当作实验电导率。

### Gate 2

- MSD 在生产区间出现稳定线性区；
- 不同时间窗口得到的 D<sub>Li</sub> 结果一致；
- 至少两个独立初始速度/无序构型得到相近趋势；
- 结构没有在 MD 中非物理坍塌。

## 6. Phase 4：高温扩散与 ML-MD

如果 300 K AIMD 中 Li 位移不足，不能直接判定材料“不导 Li”。可在结构稳定的前提下：

1. 使用较高温度 AIMD 获得扩散事件；
2. 用 Arrhenius 关系估计温度依赖；
3. 资源允许时，用 DFT 数据训练 ML potential；
4. 用 ns 级 ML-MD 回到 300 K 附近验证扩散。

ML-MD 必须用独立 DFT 构型检查能量、力和结构分布，不能只看训练误差。

## 7. Phase 5：迁移机制和结构描述符

对于高 σ 候选，重点回答：

- Li⁺ 是通过 1D、2D 还是 3D 网络迁移？
- Li vacancy 位于哪个晶位？
- O²⁻/Cl⁻ 混合是否降低迁移瓶颈？
- P\bar3m1 与 Cmc2₁ 的 Li 子晶格差异是什么？
- Li–Li correlation 是否显著降低 collective conductivity？
- 迁移瓶颈和局部配位环境能否解释 σ 的差异？

输出应包括：Li probability density、迁移路径、bottleneck size、配位数、局部结构与 MSD 的对应关系。

## 8. 两种材料的比较框架

| 维度 | Li₃YCl₆ | LiNbOCl₄ |
|---|---|---|
| 结构类型 | P\bar3m1，层状/高对称卤化物框架 | Cmc2₁，mixed-anion oxyhalide |
| 方向 2 价值 | 高电压 halide benchmark、空位/无序参考 | >10 mS cm⁻¹ 实验 benchmark、O/Cl 混合阴离子 |
| 关键变量 | Li/Y 位点占位、Li vacancy、有序化方式 | Li/Cl 部分占位、O/Cl 配置、局部 Nb 配位 |
| 首要风险 | 部分占位模型对扩散结果影响较大 | 部分占位和有序化可能改变迁移网络 |
| 首要输出 | vacancy–MSD–σ 关系 | mixed-anion–bottleneck–σ 关系 |

## 9. Go / No-Go 标准

### Go

- 结构在 DFT 和 MD 中稳定；
- energy above hull 处于可接受范围；
- MSD 有可靠线性区；
- 多个构型/温度给出一致的高扩散趋势；
- 迁移机制可以由结构分析解释。

### No-Go 或返工

- 结果只来自单个部分占位随机构型；
- MD 中结构坍塌或出现非物理短键；
- σ 只由 Nernst–Einstein 单一估计得到；
- 温度外推没有多个温度点支持；
- 原始 CIF 与照片重建模型差异过大。

## 10. 最终交付物

```text
01_structure_validation/
02_dft_relaxation/
03_hull_and_stability/
04_aimd_screening/
05_mlmd_longtime/
06_msd_diffusion_conductivity/
07_migration_mechanism/
08_comparison_report/
```

最终比较表至少包含：

`structure_id | material | space_group | occupancy_model | E_hull | T | MD_time | D_Li | sigma_NE | sigma_collective | E_a | mechanism | confidence | source`

