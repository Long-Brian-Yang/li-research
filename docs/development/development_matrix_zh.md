# 候选固态电解质开发矩阵（中文）

本文件把文献结论转换为候选材料的可执行评价表。当前数值仅整理自项目已有笔记；`—` 表示需要从原始论文或计算输出补齐，不能视为已验证数据。

## 1. 统一评价指标

| 指标 | 目标 | 建议评分（0–3） | 数据来源/方法 |
|---|---:|---|---|
| Li⁺ 传导度 σ<sub>Li</sub> | >10 mS cm⁻¹ | 0: <1；1: 1–3；2: 3–10；3: >10 | MD：MSD、D<sub>Li</sub>、Nernst–Einstein 或 Green–Kubo；实验 EIS |
| Young’s modulus E | <30 GPa | 0: >60；1: 30–60；2: 10–30；3: <10 | DFT elastic tensor C<sub>ij</sub>；纳米压痕/超声实验 |
| Energy above hull | 越低越好 | 0: >100 meV atom⁻¹；1: 50–100；2: 20–50；3: <20 | Materials Project/DFT phase diagram；需注明计算设置 |
| 低成本/供应性 | rare-element-free 优先 | 0: Ta/Gd/La/In 主体；1: 稀有元素较多；2: 少量掺杂；3: Li–Zr–Al–O–Cl 主体 | 元素筛选、价格与供应链调查 |
| 耐氧化性 V<sub>ox</sub> | >5 V vs. Li | 0: <4；1: 4–4.5；2: 4.5–5；3: >5 | 分解反应能/电化学窗口；需区分动力学与热力学 |
| 正极化学稳定性 | 无明显副反应 | 0: 强反应；1: 反应能较高；2: 可形成可接受界面；3: 无明显反应 | 与 NMC811 等正极的 ΔE<sub>reaction</sub> |
| 耐热性 | 150 °C 无劣化 | 0: 明显分解；1: 部分劣化；2: 基本稳定；3: 稳定并有实验验证 | 热分解/动力学计算、DSC/TGA、150 °C 保持实验 |
| 合成与成形 | 可复现实验路线 | 0: 无已知路线；1: 高压/极端条件；2: 可实验室制备；3: 简单、可放大且可压实 | Energy above hull、合成路线、相纯度、压实密度 |

建议总分不替代硬门槛：先排除 energy above hull 过高或无法合成的候选，再对剩余材料按 σ、E 和成本加权排序。

## 2. 当前候选评分草表

| 候选 | σ | E | 可合成性 | 成本/元素 | V<sub>ox</sub> | 正极稳定性 | 热稳定性 | 合成/成形 | 总体判断 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Composition 1：Li–Zr–Ta–Gd–Cl–O | 1 | 2–3 | — | 0 | 1 | — | — | — | 机械 benchmark；成本和氧化稳定性限制产业化 |
| Composition 2：Li–La–Zr–Ta–Cl–O–Br | 2 | — | — | 0–1 | — | — | — | — | transport/framework benchmark；需去稀有元素并翻倍 σ |
| Composition 3：Li–Zr–Al–Cl–O | 1 | 3 | — | 3 | — | — | — | 2 | 最有产业化吸引力的 baseline；核心任务是提升 σ |

评分是基于目前摘要信息的暂定值，不是最终材料排名。补齐原始数据后再锁定权重和排序。

## 3. 论文到候选设计的映射

### 方向编号

- **方向 1：机械柔顺性** —— `E <30 GPa`，对应 Hu 2023、Hu 2026。
- **方向 2：高传导结构** —— P6₃/m、空位/相变、mixed-anion、3D migration network；是当前主线。
- **方向 3：低成本化学空间** —— Li–Zr–Al–O–Cl 等 rare-element-free 体系，对应 Wang 2021、Hu 2023、Hu 2026。

Li & Du 2025 为 Review，提供三个方向的综合评价框架，不归入单一方向。

| 设计问题 | 关键论文 | 可继承的设计原则 | 需要补的验证 |
|---|---|---|---|
| 如何达到 >10 mS cm⁻¹ | Tanaka 2023；Asano 2018 | mixed-anion、开放 Li⁺ 网络、高电压兼容 | MD 设置、实验 EIS、Eₐ、体相/晶界贡献 |
| 如何把 E 压到 <30 GPa | Hu 2026；Hu 2023 | oxychloride、机械顺应性、压实性 | 完整 C<sub>ij</sub>、各向异性、纳米压痕条件 |
| 如何降低成本 | Wang 2021；Hu 2023/2026 | Zr–Al–O–Cl、避免 Ta/Gd/La/In 主体 | 原料价格基准、产率、规模化工艺 |
| 如何构造 3D migration network | Yin 2023；Kim 2021；Li 2024 | 空位工程、相变、stacking descriptor | P6₃/m/C2/m/Pnma 的稳定性和可合成性 |
| 如何保证正极兼容 | Asano 2018；Li & Du 2025 | 区分 V<sub>ox</sub> 与 ΔE<sub>reaction</sub>，评估界面 | NMC811 反应能、界面相、循环后阻抗 |

## 4. 统一数据录入模板

每个新候选材料至少记录以下字段：

```text
candidate_id:
nominal_composition:
structure_space_group:
structure_source:
energy_above_hull_meV_atom:
md_temperature_K:
md_time_ns:
md_supercell:
sigma_Li_mS_cm:
activation_energy_eV:
youngs_modulus_GPa:
elastic_tensor_Cij:
oxidation_limit_V_vs_Li:
cathode_reaction_energy_eV_atom:
thermal_test_temperature_C:
thermal_hold_time_h:
precursor_cost_USD_kg:
synthesis_route:
relative_density_percent:
source_or_commit:
confidence:
open_questions:
```

## 5. 当前最重要的下一步

优先寻找能继承 Composition 3 的 Li–Zr–Al–O–Cl 低成本化学空间、同时具有 P6₃/m 或其他高传导结构特征的候选；用 energy above hull 做第一道硬筛选，再以 MD 的 σ 和 DFT 的 E 进行双目标筛选。

## 6. 项目图表位置

将三张开发方针图放入 `figures/` 后，可在此处固定引用：

- `figures/development-goals.png`：开发目标与优先级
- `figures/candidate-compositions.png`：三个候选组成比较
- `figures/element-screening-rules.png`：元素、毒性、成本与供应性规则
