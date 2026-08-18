# 卤化物固态电解质论文整理（中文）

## 面向车辆用全固态电池的开发框架

这组论文对应的研究问题已经从“了解卤化物 SSE”推进到“按照车辆用全固态电池要求反推候选材料”：在低成本、低毒、可获得的元素空间内，寻找可合成、足够柔顺且具有快速 Li⁺ 输运的新结构。

### 量化开发目标

| 目标特性 | 目标值 | 优先级 | 当前主要评价方法 |
|---|---:|---|---|
| Li⁺ 传导度 | >10 mS cm⁻¹ | 高 | 分子动力学（MD）：MSD → D<sub>Li</sub> → σ<sub>Li</sub> |
| 成形性 / Young’s modulus | <30 GPa | 高 | 第一性原理弹性张量 C<sub>ij</sub> → E |
| 合成可能性 | 尽可能低的 energy above hull | 高 | Energy above hull / 热力学筛选 |
| 低成本 | rare-element-free 优先 | 中 | 元素组成、价格与供应链筛选 |
| 耐氧化性 | >5 V vs. Li | 中 | 分解反应能 / 氧化电位 |
| 化学稳定性 | 与正极无明显副反应 | 中 | 与正极的反应能 ΔE<sub>reaction</sub> |
| 耐热性 | 150 °C 无劣化 | 低 | 热分解与动力学相关计算 |

高优先级不是单一的“最高 conductivity”，而是：

> **Fast Li transport + Mechanical compliance + Synthesizability**

其中电化学窗口与实际正极兼容性必须分开评价：`electrochemical window ≠ actual cathode compatibility`。

### 三个候选组成的定位

| 候选 | 代表组成 / 结构 | 当前优势 | 当前瓶颈 | 开发定位 |
|---|---|---|---|---|
| Composition 1 | Li–Zr–Ta–Gd–Cl–O；约 Li₁.₅Zr₀.₃Ta₀.₆Gd₀.₁Cl₄.₈O₀.₆ | σ≈3 mS cm⁻¹；E≈12 GPa，机械目标已达成 | Ta/Gd 不利于成本；耐氧化性约 4.2 V；σ 未达标 | mechanical-compliance benchmark |
| Composition 2 | Li–La–Zr–Ta–Cl–O–Br；P6₃/m-related framework | σ≈5 mS cm⁻¹，当前输运最好 | La/Ta 不符合 rare-element-free；仍低于 10 mS cm⁻¹ | high-conductivity framework benchmark |
| Composition 3 | Li–Zr–Al–Cl–O；1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ | 低成本、低毒、易获得；E≈1.41 GPa | σ≈2–2.5 mS cm⁻¹，需进一步提升 | industrially attractive baseline |

### 目标材料的搜索逻辑

1. **存在性筛选：** 先用 energy above hull 判断材料是否具有现实合成可能。
2. **输运筛选：** 对通过热力学筛选的候选进行 MD，计算 MSD、D<sub>Li</sub> 与 σ<sub>Li</sub>，目标为 >10 mS cm⁻¹。
3. **力学筛选：** 从 C<sub>ij</sub> 得到 Young’s modulus，目标为 E<30 GPa。
4. **电化学筛选：** 同时检查 V<sub>ox</sub>>5 V 与候选材料/正极的 ΔE<sub>reaction</sub>。
5. **多目标取舍：** 若无法同时满足全部指标，优先满足高优先级的传导度、机械柔顺性和可合成性。

### 元素与阴离子筛选规则

| 类别 | 当前规则 | 对候选空间的含义 |
|---|---|---|
| 优先元素 | Li、Zr、Al、O、Cl | 低成本、低毒、供应性较好，是 Composition 3 的基础化学空间 |
| 少量可接受 | Zr、Nb；Ga/Ge 等 | 可作为少量结构/输运调控元素，而非主体元素 |
| 成本不利 | Ta、Gd、La，以及 Mo–Hg 区间的许多过渡金属 | 性能有优势时可作 benchmark，但不宜作为产业化主体系 |
| 使用需谨慎 | Zn | 可能降低耐酸性，并带来电子导电风险 |
| 原则上避免 | In 及图示毒性元素 | 安全、环境与法规风险 |
| 硫的限定使用 | SO₄²⁻ 可接受；S²⁻ 禁止 | 不是完全禁硫，而是排除 sulfide 型化学空间 |
| 供应性排除 | 图示灰色区域 | 即使计算性能好，也因入手性不足而不进入候选集 |

**当前核心研究问题：** 如何在 rare-element-free 的 Li–Zr–Al–O–Cl 等低成本化学空间中，找到可合成、足够柔软，同时 σ<sub>Li</sub>>10 mS cm⁻¹ 的新结构。

### 三条开发方向与论文归类

| 方向 | 具体含义 | 主要论文 | 在项目中的作用 |
|---|---|---|---|
| **方向 1：机械柔顺性** | Young’s modulus <30 GPa、可压实、循环形变适配 | Hu 2023、Hu 2026；Asano 2018 | 建立力学 benchmark，并约束高传导候选不能过硬 |
| **方向 2：高传导结构** | P6₃/m、空位/相变、mixed-anion、3D migration network | Asano 2018、Kim 2021、Tanaka 2023、Yin 2023、Li 2024 | 当前主线：把 σ 从 2–5 mS cm⁻¹ 推向 >10 mS cm⁻¹ |
| **方向 3：低成本化学空间** | rare-element-free 的 Li–Zr–Al–O–Cl、低毒、易获得 | Wang 2021、Hu 2023、Hu 2026 | 约束产业化元素空间和成本 |
| **综合框架** | 兼顾传导、力学、稳定性、成本和实用 ASSB | Li & Du 2025（Review） | 提供三条方向的统一评价方法 |

**当前主线判断：** 这 9 篇论文以**方向 2**为 transport/framework 主线，同时用方向 1 的机械约束和方向 3 的产业化约束筛选最终候选。

## 1. Asano et al., 2018 — Advanced Materials

### Type
Research Article（研究论文）

### Title
Solid Halide Electrolytes with High Lithium-Ion Conductivity for Application in 4 V Class Bulk-Type All-Solid-State Batteries

### Material
Li₃YCl₆、Li₃YBr₆

### Keywords
Li₃YCl₆ · Li₃YBr₆ · Halide SSE · Chloride SSE · High-voltage cathode · Ionic conductivity · Grain-boundary resistance · Deformability · Oxidation stability · Bulk-type ASSB

### 三句话总结
1. 报道了 Li₃YCl₆ 和 Li₃YBr₆ 两种高 Li⁺ 电导率卤化物固态电解质，室温电导率达到 >1 mS cm⁻¹。
2. 材料具有较好的可变形性和氧化稳定性，冷压 pellet 中没有明显额外的 grain-boundary resistance。
3. 证明卤化物 SSE 可以直接用于 4 V class cathode，奠定了现代 chloride solid electrolyte 研究的重要基础。

### 与开发目标的关联
证明高电压卤化物 SSE 的可行性，为 `>5 V` 氧化稳定性和 4 V 正极兼容性提供基准；同时提示仅有 mS cm⁻¹ 级传导度还不足以满足车辆目标。

### DOI
[10.1002/adma.201803075](https://doi.org/10.1002/adma.201803075)

## 2. Kim et al., 2021 — ACS Materials Letters

### Type
Research Article（研究论文）

### Title
Lithium Ytterbium-Based Halide Solid Electrolytes for High Voltage All-Solid-State Batteries

### Material
Li₃YbCl₆、Li₃₋ₓYb₁₋ₓZrₓCl₆

### Keywords
Li₃YbCl₆ · Zr substitution · Aliovalent doping · Li vacancy · Phase transition · Trigonal phase · Orthorhombic phase · High-voltage stability · Mixed-metal halide · Migration network

### 三句话总结
1. 开发了 Li₃YbCl₆ 及 Li₃₋ₓYb₁₋ₓZrₓCl₆ 系列 Yb 基 chloride SSE。
2. 通过 Zr⁴⁺ 对 Yb³⁺ 的异价取代，同时调控 Li vacancy 和晶体结构，并观察到 trigonal/orthorhombic structural evolution。
3. 该工作说明 halide SSE 的离子输运不能只看空位浓度，还必须考虑 composition–structure–migration network 的关系，同时保持良好的高电压氧化稳定性。

### 与开发目标的关联
支持通过异价掺杂与相变调控迁移网络的路线，为 Composition 2 的结构工程提供方法依据；但仍需结合 cost、energy above hull 和 E<30 GPa 进行筛选。

### DOI
[10.1021/acsmaterialslett.1c00142](https://doi.org/10.1021/acsmaterialslett.1c00142)

## 3. Wang et al., 2021 — Nature Communications

### Type
Research Article（研究论文）

### Title
A Cost-Effective and Humidity-Tolerant Chloride Solid Electrolyte for Lithium Batteries

### Material
Li₂ZrCl₆

### Keywords
Li₂ZrCl₆ · Cost-effective · Humidity tolerance · Zr-based chloride · 4 V cathode · Mechanochemical synthesis · Ionic conductivity · Deformability · Low-cost precursor · Moisture stability

### 三句话总结
1. 提出了低成本 Li₂ZrCl₆ chloride SSE，室温 Li⁺ conductivity 约为 0.81 mS cm⁻¹。
2. 与许多昂贵的 Y/In/Sc/rare-earth chloride 相比，Zr 基体系显著降低原料成本，同时保留良好的 deformability 和 4 V 正极兼容性。
3. 在 5% relative humidity 环境暴露后没有观察到明显吸湿或 conductivity degradation，说明其低湿环境耐受性优于很多传统 chloride SSE。

### 与开发目标的关联
直接支持低成本 Zr chemistry、耐湿性与 4 V 正极兼容性目标，是 Li–Zr–Al–O–Cl 产业化路线的重要化学先例。

### DOI
[10.1038/s41467-021-24697-2](https://doi.org/10.1038/s41467-021-24697-2)

## 4. Tanaka et al., 2023 — Angewandte Chemie International Edition

### Type
Research Article（研究论文）

### Title
New Oxyhalide Solid Electrolytes with High Lithium Ionic Conductivity >10 mS cm⁻¹ for All-Solid-State Batteries

### Material
LiNbOCl₄、LiTaOCl₄

### Keywords
LiNbOCl₄ · LiTaOCl₄ · Oxyhalide · Mixed-anion · Anion engineering · Superionic conduction · >10 mS cm⁻¹ · Li⁺ migration environment · High-rate performance · Bulk-type ASSB

### 三句话总结
1. 报道了新的 oxyhalide LiNbOCl₄ 和 LiTaOCl₄，室温 conductivity 分别达到约 10.4 和 12.4 mS cm⁻¹。
2. 通过在 halide framework 中同时引入 O²⁻ 和 Cl⁻，利用 mixed-anion / anion engineering 重构 Li⁺ migration environment。
3. 这项工作将 halide/oxyhalide SSE 的 conductivity 推进到 10⁻² S cm⁻¹ 级别，并在 bulk-type ASSB 中展示了优秀的高倍率性能。

### 与开发目标的关联
直接证明 mixed-anion / 新结构路线有机会跨越 `10 mS cm⁻¹` 门槛；后续需要补充成本、可合成性、力学模量和正极反应能评价。

### DOI
[10.1002/anie.202217581](https://doi.org/10.1002/anie.202217581)

## 5. Yin et al., 2023 — Nature

### Type
Research Article（研究论文）

### Title
A LaCl₃-Based Lithium Superionic Conductor Compatible with Lithium Metal

### Material
Ta-doped LaCl₃

### Keywords
LaCl₃ · Ta doping · La vacancy · UCl₃-type framework · 1D-to-3D migration · Li-metal compatibility · Passivation interphase · Gradient interphase · Activation energy · Rare-earth chloride

### 三句话总结
1. 基于 UCl₃-type LaCl₃ framework，利用其宽大的 1D Li⁺ channels 开发了新的 rare-earth chloride SSE。
2. Ta⁵⁺ doping 引入 La vacancies，将原本的一维 Li⁺ 通道连接成三维 migration network，优化材料达到 3.02 mS cm⁻¹ @ 30 °C、Eₐ = 0.197 eV。
3. 材料与 Li metal 接触后形成自限性的 gradient passivation interphase，使其兼具快速 Li⁺ transport 与优秀的 Li-metal compatibility。

### 与开发目标的关联
为 P6₃/m-related high-conductivity framework 与 Li-metal 界面设计提供依据；同时 Ta/La 的资源与成本问题说明它更适合作为 transport benchmark，而不是最终产业化组成。

### DOI
[10.1038/s41586-023-05899-8](https://doi.org/10.1038/s41586-023-05899-8)

## 6. Hu et al., 2023 — Nature Communications

### Type
Research Article（研究论文）

### Title
A Cost-Effective, Ionically Conductive and Compressible Oxychloride Solid-State Electrolyte for Stable All-Solid-State Lithium-Based Batteries

### Material
Li₁.₇₅ZrCl₄.₇₅O₀.₅

### Keywords
Li₁.₇₅ZrCl₄.₇₅O₀.₅ · Oxychloride · Mixed-anion · Compressibility · Relative density · Cost-effective · Ionic conductivity · NMC811 · Long cycling · Practical ASSB

### 三句话总结
1. 开发了 Li₁.₇₅ZrCl₄.₇₅O₀.₅ oxychloride SSE，实现 2.42 mS cm⁻¹ 的室温 ionic conductivity。
2. 材料在 300 MPa 下达到 94.2% relative density，同时估算原料成本仅约 $11.60 kg⁻¹，体现了 conductivity、compressibility 与 cost 的综合优化。
3. 搭配 NMC811-based positive electrode 的实验室全固态电池实现超过 2000 cycles，说明实用 SSE 的评价不能只考虑最高 bulk conductivity。

### 与开发目标的关联
这是 rare-element-free Li–Zr–Al–O–Cl 方向的强 baseline：同时展示 mS cm⁻¹ 级传导、压实性、低成本和长循环，但需要把 σ 从约 2.42 mS cm⁻¹ 推向 >10 mS cm⁻¹。

### DOI
[10.1038/s41467-023-39522-1](https://doi.org/10.1038/s41467-023-39522-1)

## 7. Li et al., 2024 — Nature Communications

### Type
Research Article（研究论文）

### Title
Structural Regulation of Halide Superionic Conductors for All-Solid-State Lithium Batteries

### Material
结构类型：hcp-T、hcp-O、ccp-M

### Keywords
Cationic polarization factor · τ · hcp-T · hcp-O · ccp-M · Stacking structure · Structure prediction · Composition–structure relation · Li-ion transport · Materials screening · Descriptor-guided discovery

### 三句话总结
1. 作者提出 cationic polarization factor τ，尝试从 chemical composition 出发预测 lithium halide SSE 的 stacking structure。
2. 将典型结构归纳为 hcp-T、hcp-O 和 ccp-M 等类别，并建立 composition → structure → Li-ion transport 的关联。
3. 该 descriptor 被进一步用于候选材料筛选和实验设计，使卤化物开发由传统 trial-and-error 向 descriptor-guided materials discovery 转变。

### 与开发目标的关联
为从 composition → structure → Li transport 的计算筛选提供工具，可用于在允许元素空间内优先搜索 P6₃/m、C2/m、Pnma 等高传导结构家族。

### DOI
[10.1038/s41467-023-43886-9](https://doi.org/10.1038/s41467-023-43886-9)

## 8. Hu et al., 2026 — Nature Communications

### Type
Research Article（研究论文）

### Title
Mechanically Compliant and Cost-Effective 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ Solid Electrolyte for All-Solid-State Batteries with Improved Cycling Stability

### Material
1.4Li₂O–0.75ZrCl₄–0.25AlCl₃

### Keywords
Mechanical compliance · Li-Zr-Al-O-Cl · Young's modulus · Hardness · High-loading cathode · Chemo-mechanical stability · Ionic conductivity · Deformability · Interface stability · Cost-effective · Mechanical mismatch

### 三句话总结
1. 开发了 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ 固态电解质，在 25 °C 下具有约 2.55 mS cm⁻¹ 的 ionic conductivity。
2. 最大特点是极高 mechanical compliance：Hardness 约 0.22 GPa、Young’s modulus 约 1.41 GPa，使电解质更容易跟随电极循环过程中的形变。
3. 这项工作把固态电解质设计重点从单纯 conductivity 推进到 Li-ion transport + mechanics + interface + cost 的多目标优化。

### 与开发目标的关联
对应 Composition 3 的直接 baseline：极低 Young’s modulus（约 1.41 GPa）与低成本非常有吸引力，但必须通过结构/缺陷设计把传导度从 2–2.5 mS cm⁻¹ 提升到 >10 mS cm⁻¹。

### DOI
[10.1038/s41467-025-68210-5](https://doi.org/10.1038/s41467-025-68210-5)

## 9. Li & Du, 2025 — ACS Nano（Review）

### Type
Review（综述）

### Title
Building a Better All-Solid-State Lithium-Ion Battery with Halide Solid-State Electrolyte

### Material
F/Cl/Br/I-based halide SSE（综述）

### Keywords
Halide SSE · Review · F/Cl/Br/I chemistry · Ionic conductivity · Activation energy · Electronic conductivity · Electrochemical stability window · Interfacial contact stability · Synthesis · Structure–property relation · Practical ASSB metrics

### 三句话总结
1. 这篇 Review 系统总结了 F/Cl/Br/I-based halide SSE 的组成、结构、合成及全固态电池应用。
2. 作者不仅比较 ionic conductivity 和 activation energy，还重点讨论 electronic conductivity、electrochemical stability window、interfacial contact stability 等实际性能指标。
3. 它提供了一个完整的 halide SSE 设计框架，即从 composition/structure → Li transport → stability/interface → practical ASSB performance 综合评价材料。

### 与开发目标的关联
提供完整的多目标评价框架，提醒开发流程必须同时纳入 σ、E、energy above hull、氧化电位、正极反应能、热稳定性、成本和界面，而不能只优化单一指标。

### DOI
[10.1021/acsnano.4c15005](https://doi.org/10.1021/acsnano.4c15005)

## 关键词地图

| 年份 | 核心材料/主题 | 最核心 Keyword | DOI |
|---|---|---|---|
| 2018 | Li₃YCl₆ / Li₃YBr₆ | High-voltage halide SSE | [DOI](https://doi.org/10.1002/adma.201803075) |
| 2021 | Li₃YbCl₆ + Zr | Vacancy / phase engineering | [DOI](https://doi.org/10.1021/acsmaterialslett.1c00142) |
| 2021 | Li₂ZrCl₆ | Cost + humidity tolerance | [DOI](https://doi.org/10.1038/s41467-021-24697-2) |
| 2023 | LiNbOCl₄ / LiTaOCl₄ | Oxyhalide / >10 mS cm⁻¹ | [DOI](https://doi.org/10.1002/anie.202217581) |
| 2023 | LaCl₃ + Ta | Li-metal compatibility / 1D→3D | [DOI](https://doi.org/10.1038/s41586-023-05899-8) |
| 2023 | Li₁.₇₅ZrCl₄.₇₅O₀.₅ | Compressibility + cost | [DOI](https://doi.org/10.1038/s41467-023-39522-1) |
| 2024 | Structural regulation | Cationic polarization factor τ | [DOI](https://doi.org/10.1038/s41467-023-43886-9) |
| 2025 | Review | Halide SSE overview | [DOI](https://doi.org/10.1021/acsnano.4c15005) |
| 2026 | Li–Zr–Al–O–Cl | Mechanical compliance | [DOI](https://doi.org/10.1038/s41467-025-68210-5) |

## 扩充比较表

> “—”表示你提供的摘要中没有统一给出该指标，后续可继续补充原文数据。

| # | 年份 | 类型 | 电解质/主题 | 室温 Li⁺ 电导率 | 结构或输运机制 | 高电压/界面稳定性 | 力学、湿度与成本 | 电池或应用验证 | 核心贡献 | DOI |
|---:|---:|---|---|---:|---|---|---|---|---|---|
| 1 | 2018 | Research Article | Li₃YCl₆ / Li₃YBr₆ | >1 mS cm⁻¹ | 高 Li⁺ 传导；可变形；低 grain-boundary resistance | 氧化稳定；4 V 正极兼容 | 冷压成型；— | 4 V class bulk-type ASSB | 奠定 chloride SSE 的现代研究基础 | [链接](https://doi.org/10.1002/adma.201803075) |
| 2 | 2021 | Research Article | Li₃YbCl₆；Li₃₋ₓYb₁₋ₓZrₓCl₆ | — | Zr⁴⁺/Yb³⁺ 异价取代；Li vacancy；trigonal→orthorhombic | 高电压氧化稳定 | 混合金属组成；— | 高电压 ASSB 候选 | 建立 composition–structure–migration network 视角 | [链接](https://doi.org/10.1021/acsmaterialslett.1c00142) |
| 3 | 2021 | Research Article | Li₂ZrCl₆ | ≈0.81 mS cm⁻¹ | Zr-based chloride；mechanochemical synthesis | 4 V 正极兼容；5% RH 后无明显 degradation | 低成本；deformability；耐湿 | Li battery / 4 V cathode | 以 Zr 降低成本并提升湿度耐受性 | [链接](https://doi.org/10.1038/s41467-021-24697-2) |
| 4 | 2023 | Research Article | LiNbOCl₄ / LiTaOCl₄ | ≈10.4 / 12.4 mS cm⁻¹ | O²⁻/Cl⁻ mixed-anion；anion engineering | mixed-anion 重构 Li⁺ migration environment | — | bulk-type ASSB；高倍率性能 | 将 oxyhalide 传导度推进至 10⁻² S cm⁻¹ 级 | [链接](https://doi.org/10.1002/anie.202217581) |
| 5 | 2023 | Research Article | Ta-doped LaCl₃ | 3.02 mS cm⁻¹ @ 30 °C；Eₐ=0.197 eV | La vacancy；1D→3D migration network | Li metal 接触形成 gradient passivation interphase | — | Li-metal-compatible SSE | 同时解决快速传导与 Li-metal compatibility | [链接](https://doi.org/10.1038/s41586-023-05899-8) |
| 6 | 2023 | Research Article | Li₁.₇₅ZrCl₄.₇₅O₀.₅ | 2.42 mS cm⁻¹ | Oxychloride；mixed-anion | NMC811 界面与长期循环稳定 | 300 MPa 下 94.2% relative density；≈$11.60 kg⁻¹ | NMC811；>2000 cycles | 综合优化 conductivity、compressibility 与 cost | [链接](https://doi.org/10.1038/s41467-023-39522-1) |
| 7 | 2024 | Research Article | Structural regulation；hcp-T/O、ccp-M | — | Cationic polarization factor τ；stacking structure descriptor | 通过结构筛选间接指导稳定材料发现 | — | 候选材料筛选与实验设计 | 将 trial-and-error 转为 descriptor-guided discovery | [链接](https://doi.org/10.1038/s41467-023-43886-9) |
| 8 | 2026 | Research Article | 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ | ≈2.55 mS cm⁻¹ @ 25 °C | Li-Zr-Al-O-Cl；chemo-mechanical design | interface 与循环形变稳定性 | Hardness≈0.22 GPa；E≈1.41 GPa；cost-effective | high-loading cathode；improved cycling | 将 mechanics 纳入 SSE 多目标优化 | [链接](https://doi.org/10.1038/s41467-025-68210-5) |
| 9 | 2025 | **Review** | F/Cl/Br/I-based halide SSE | 综述比较 | composition/structure→transport | electrochemical window；electronic conductivity；interfacial contact stability | synthesis、activation energy、实际指标 | practical ASSB 评价框架 | 建立从材料到器件的综合设计框架 | [链接](https://doi.org/10.1021/acsnano.4c15005) |

## 主题索引

| 主题 | 对应论文 | 可追踪问题 |
|---|---|---|
| 高电压兼容性 | 1、2、3、4 | 如何在 4 V 正极下保持低界面阻抗与抗氧化性？ |
| 结构与空位工程 | 2、5、7 | 空位浓度、层堆垛与迁移网络如何协同？ |
| Oxyhalide / mixed-anion | 4、6、8 | O²⁻/Cl⁻ 混合阴离子如何同时影响输运与力学？ |
| Li-metal 界面 | 5、9 | 如何形成稳定、薄且自限性的 passivation interphase？ |
| 成本与可制造性 | 3、6、8、9 | 原料成本、压实密度、工艺窗口和规模化如何平衡？ |
| 力学与循环 | 1、3、6、8、9 | 机械顺应性是否能转化为高负载、长循环性能？ |
