# LZOC MACE：活化能、体积与骨架核查（2026-09-12）

> 日期快照。见 [分析说明与数据存储范围](README.md)；本文归档不改变原始结果，也不代表新增验证或实时状态。

## 判断

当前 600/700/800/900 K 的 Li 自扩散 Arrhenius 拟合给出表观 Ea = 0.20544 eV，R² = 0.97725。它来自时间原点平均 MSD 的 20–80 ps lag 拟合，不是 production 的 20–80%。数值量级并非不可能，但本批结构状态尚不足以支持“稳定非晶固体的本征迁移活化能”这一解释。暂不建议外推室温电导率。

## 数据与方法

MACE：TSUBAME 8635176.1–4；NEP89：8635527。使用本目录 source 中已下载且 production 轨迹哈希与 TSUBAME 核对一致的快照。192 原子：Li42 Zr24 O12 Cl114。来源与主分析定义见 README.md、source_hashes.json、results.json。

本轮额外读取 production 起末帧，采用 ASE triclinic minimum-image 距离核查配位；体积由晶胞行列式独立计算。Zr 位移额外扣除 Zr 自身质心移动。近邻保留率为初始 Zr–X 配对在 200 ps 末帧仍低于相同 cutoff 的比例，不是连续键寿命；允许期间断开后重新形成。Zr–O cutoff 2.6 Å、Zr–Cl 3.0 Å，是统一诊断阈值，不等同化学键判据。

## 体积检查

共同 300 K 起始结构密度 1.913855 g/cm³。体积变化相对该起始结构，不是同温实验热膨胀率。

| 模型 | 温度 K | Production 密度 g/cm³ | 相对起始体积增加 | Zr 自身质心校正后 MSD(200 ps), Å² |
|---|---:|---:|---:|---:|
| MACE | 600 | 1.468304 | 30.3% | 57.965 |
| MACE | 700 | 1.147423 | 66.8% | 88.898 |
| MACE | 800 | 1.272778 | 50.4% | 136.271 |
| MACE | 900 | 0.925128 | 106.9% | 297.596 |
| NEP89 | 600 | 1.875429 | 2.0% | 9.805 |

膨胀发生在 NPT 阶段；之后 NVT 固定的是 NPT 最后一步晶胞，不是末段平均晶胞。800/900 K 最后 10 ps 的密度线性趋势分别为 -0.02060/-0.01600 g cm⁻³ ps⁻¹，不能视为已充分达到密度平台。700 K 的最终密度低于 800 K，也不支持把各温度点直接解释为同一平衡相的常规热膨胀。

## 骨架检查

| 模型 | 温度 K | 初始 Zr–O 对数 | Zr–O 末帧保留率 | 初始 Zr–Cl 对数 | Zr–Cl 末帧保留率 |
|---|---:|---:|---:|---:|---:|
| MACE | 600 | 27 | 100.0% | 105 | 64.8% |
| MACE | 700 | 26 | 96.2% | 104 | 47.1% |
| MACE | 800 | 27 | 92.6% | 99 | 35.4% |
| MACE | 900 | 25 | 92.0% | 99 | 25.3% |
| NEP89 | 600 | 29 | 100.0% | 115 | 89.6% |

Zr 位移不是整体质心漂移造成。Zr–O 局部单元多数保持，但 Zr–Cl 配位身份显著变化，支持框架迁移/重排。不能仅凭平均 RDF 或平均 CN 相近宣称骨架稳定；也不能仅凭这些统计断言化学分解或宏观熔化。NEP89 的重排较弱，但 Zr 位移仍非零，单温结果不构成该模型正确性的验证。

## 输入与压力实现核查

- 实际输入使用 units metal，type 映射 Li/Zr/O/Cl，1 bar NPT，0.5 fs timestep，Tdamp 0.1 ps、Pdamp 1 ps。
- 独立体积/质量密度计算与 thermo 一致；此前单原点 MSD 重构也与 LAMMPS 输出一致。未发现坐标或单位误读的证据。
- TSUBAME 已有 virial_check_8631511：旧 256 原子正交晶胞的两个静态快照，排除动能的压力与有限体积能量导数相比较。在 ΔV/V=0.001 时差值为 0.408 和 0.141 bar，且随扰动减小收敛。
- 当前模型 SHA256 与该检查相同：4dc86cd27a688fb4e90501816368678f6408cba150aefc4bc1cd9270648b9a43。
- 这是反对“普遍压力符号/单位错误”的证据，但不是当前 192 原子倾斜晶胞、高温快照的完整应力验证，也不验证 MACE 对真实材料的准确性。

## 文献参考与边界

1. Hu et al., *A cost-effective, ionically conductive and compressible oxychloride solid-state electrolyte for stable all-solid-state lithium-based batteries*, Nature Communications 14, 3807 (2023). DOI: https://doi.org/10.1038/s41467-023-39522-1 。与本次名义组分相同的 Li1.75ZrCl4.75O0.5，实验 σ(25 °C)=2.42 mS/cm；图 3c–d 提供 Arrhenius 与 Ea。论文样品是高度非晶化且含少量晶相，不等于本次 192 原子纯模拟构型。本轮未从原始数值表核实其精确 Ea，因此不填入猜测值。
2. Zhang et al., *A family of oxychloride amorphous solid electrolytes for long-cycling all-solid-state lithium batteries*, Nature Communications 14, 3780 (2023). DOI: https://doi.org/10.1038/s41467-023-39197-8 。xLi2O–TaCl5 系列实验电导活化能为 0.241–0.277 eV，仅用于同类非晶氧氯化物的量级参考，不能作为本组分的实验真值。
3. Kim et al., *Divalent anion-driven framework regulation in Zr-based halide solid electrolytes for all-solid-state batteries*, Nature Communications 16, 10678 (2025). DOI: https://doi.org/10.1038/s41467-025-65702-2 。用于结构/机制参考，组成和相态不同。2026 更正仅涉及作者姓名，不涉及数据（https://doi.org/10.1038/s41467-026-68882-7）。

实验电导活化能与这里 ln(D) 的自扩散活化能并非无条件相同；比较须核对 ln(σ) 或 ln(σT) 的拟合定义、载流子密度和离子相关性，且实验低温区间与当前 600–900 K 不同。

## 后续判断

当前结果保留为探索性数据，不改曲线、不删异常点、不挑窗口追求目标 Ea。最有针对性的下一项是当前 192 原子代表快照的能量–体积/应力一致性检查，结合可靠密度或 DFT 单点判断势函数适用性；须另行安排计算。单纯延长 NVT 不会修复已经固定下来的低密度。此次未提交新作业、未修改生产参数、未 push。
