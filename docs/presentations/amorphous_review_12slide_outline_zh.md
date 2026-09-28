# Li离子输运NNP评估：12页PPT内容大纲

> **贯穿全篇的主线**  
> 先确认NNP和计算引擎能否高效运行，再用晶体基准识别模型差异，最后把工作流扩展到四种化学环境不同的非晶电解质。结论同时评价计算效率、结构可信度和输运准确性。

**版式决定：** 四种非晶结构不集中塞进同一页。第6–9页各安排一种材料，每页采用“左侧结构/代表轨迹，右侧一张主结果图”的统一版式。

参考：[materials review](../materials/materials_overview_ja.md) ｜ [结构与代表轨迹清单](../../materials/evidence/README.md) ｜ [结构/轨迹manifest](../../materials/evidence/manifest.json)

---

## 1｜研究目标与整体路线：为什么从晶体走向非晶？

**一句话结论：** 评估预训练势对Li输运的适用性，从计算效率出发，经晶体验证，再扩展到结构和制备历史更复杂的非晶材料。

- NNP使大体系、长时间MD成为可能，但跑得快并不表示结构和输运预测准确。
- 晶体提供规则、可比较的基准；非晶还需要处理局部配位分布、网络连接和热处理历史。
- 全篇路线：NNP性能benchmark → Li₃YCl₆/LiNbOCl₄晶体验证 → LZOC/LSZC/Li₃PS₄/LiPON非晶扩展。
- 三个评价问题：效率如何？玻璃结构是否合理？输运与实验、AIMD或材料专用势是否一致？

**建议画面：** 晶体到非晶的研究路线图。此页只放概念示意，不放四个材料的详细结构图。

## 2｜NNP性能benchmark：效率如何支持长时间MD？

**一句话结论：** GPU化和NEP89/GPUMD大幅提高生产计算效率，为长时间模拟提供条件；速度比较与精度验证分开报告。

- M3GNet–LAMMPS：CPU到1块H100 GPU，吞吐量3.285→56.621 steps/s，约17.2倍。
- 600 K production：MACE/LAMMPS 189.93 min；NEP89/GPUMD 6.11 min，约31.1倍时间差。
- 图中注明硬件、模型、MD engine和测量条件，不把不同计算工作流表述成完全同条件的精度对比。

**主图：** [MACE–NEP runtime与density比较](../materials/figures/09_MACE_NEP_runtime_density.png)。CPU/GPU吞吐量可用两个醒目的数字或小条形图呈现。

**布局：** 速度数据为主，底部加一句“效率优势使长时间模拟可行；准确度由后续材料benchmark评估”。

## 3｜晶体benchmark设计：两种晶体、三种通用模型

**一句话结论：** 先在结构规则、参考数据明确的晶体中确认模型差异，为非晶测试建立基线。

- Li₃YCl₆：240原子有序结构；MACE-MPA-0、SevenNet-nano、M3GNet GPU。
- LiNbOCl₄：336原子有序结构；采用相同三模型比较框架。
- 多温度NVT轨迹用于计算Li MSD、扩散系数和Arrhenius活化能。
- 实验活化能基准：Li₃YCl₆约0.400 eV；LiNbOCl₄约0.240 eV。

**结构素材：** [Li₃YCl₆初始结构](../../materials/evidence/crystalline/Li3YCl6/initial_structure.xyz)；[LiNbOCl₄初始结构](../../materials/evidence/crystalline/LiNbOCl4/initial_structure.xyz)。

**建议画面：** 两个结构快照并排，下面用简短流程标出模型、温度系列和输运分析。实验传导度换算与Li自扩散是不同物理量，后续结果页要明确区分。

## 4｜晶体结果：模型选择会改变输运预测

**一句话结论：** 同一晶体和分析方法下，模型间Ea及室温外推仍有差异，说明模型选择必须验证。

| 材料 | MACE-MPA-0 Ea | SevenNet-nano Ea | M3GNet GPU Ea | 实验基准Ea |
|---|---:|---:|---:|---:|
| Li₃YCl₆ | 0.302 eV | 0.246 eV | 0.212 eV | 0.400 eV |
| LiNbOCl₄ | 0.313 eV | 0.357 eV | 0.397 eV | 0.240 eV |

- Li₃YCl₆：模型都显示温度升高时扩散增加，但Ea和室温外推值依赖模型。
- LiNbOCl₄：模型差异明显；M3GNet Arrhenius线性相对较弱，R²=0.8768。
- 结晶基准告诉我们：进入非晶后，不能只展示一个模型的扩散曲线。

**主图：** [Li₃YCl₆模型间MSD](../materials/figures/01_Li3YCl6_three_model_MSD.png) 与 [LiNbOCl₄模型间MSD](../materials/figures/02_LiNbOCl4_three_model_MSD.png)。角落可加 [Li₃YCl₆ Arrhenius](../materials/figures/03_Li3YCl6_Arrhenius.png) 和 [LiNbOCl₄ Arrhenius](../materials/figures/04_LiNbOCl4_Arrhenius.png)。

## 5｜非晶动机、材料选择与共同计算流程

**一句话结论：** 四种材料按化学挑战逐步扩展；每种都有对应的结构与输运参照。

| 材料 | 化学特征 | 主要检验问题 | 主要参照 |
|---|---|---|---|
| LZOC | 含氧锆氯化物玻璃 | 氧氯化物中能否重现实验/AIMD温度响应？ | AIMD |
| LSZC | 硫酸根修饰锆氯化物 | SO₄单元和输运定量是否保持？ | 实验、专用MACE |
| Li₃PS₄ | P–S硫代磷酸盐玻璃 | 从氯化物网络向硫化物网络能否迁移？ | DeePMD、文献 |
| LiPON | P–O–N酸氮化物玻璃 | 混合阴离子和N局部拓扑能否描述？ | 实验、专用NequIP |

**同页下方放共同流程：** 玻璃构建/弛豫 → 密度、RDF、配位检查 → 多温度MD → MSD、扩散、Arrhenius → 对应材料的文献基准。

**图案建议：** 左侧用化学跨度箭头 Cl/O → SO₄/Cl → P/S → P/O/N；右侧用5步细流程。不要在本页再放原子结构图，以免抢走第6–9页内容。

## 6｜LZOC：AIMD温度响应的非晶基准

**一句话结论：** NEP89呈现可与AIMD对照的温度响应，但绝对扩散偏低；非单调数据不强行给出单一Ea。

- 材料角色：从含氧氯化物晶体/基准问题延伸到非晶局部环境。
- 文献比扩散系数约0.22–0.35；温度响应可比较，绝对尺度仍有偏差。
- 展示局部配位和Li迁移，解释为何不对整组数据作单一Arrhenius拟合。

**左侧结构/轨迹：** [LZOC分析起始结构](../../materials/evidence/amorphous/LZOC/analysis_start.xyz)；[340 K代表轨迹](../../materials/evidence/amorphous/LZOC/NEP89_340K_representative_part01.xyz)。由XYZ渲染同一玻璃盒，并将Li轨迹以短路径叠加。

**右侧主图：** [LZOC输运比较](../materials/figures/01_LZOC_transport.png)。可选小图：[放射方向位移](../materials/figures/17_LZOC_radial_displacement.png)。

## 7｜LSZC：硫酸根修饰氯化物中的定量比较

**一句话结论：** LSZC是四种非晶体系中与实验定量吻合最好的一例，同时考验SO₄结构保持。

- 结构问题：硫酸根单元嵌入Zr氯化物网络后是否仍合理？Zr周围局部环境如何变化？
- 输运结果：NEP89 Ea=0.351 eV，实验Ea=0.330 eV。
- 展示结构、Zr配位和传导曲线，避免只凭活化能接近就宣称所有输运量都一致。

**左侧结构/轨迹：** [LSZC分析起始结构](../../materials/evidence/amorphous/LSZC/analysis_start.xyz)；[330 K代表轨迹](../../materials/evidence/amorphous/LSZC/NEP89_330K_representative_part01.xyz)。结构渲染中固定SO₄四面体颜色，Li用醒目颜色或短时间路径表示。

**右侧主图：** [LSZC输运比较](../materials/figures/18_LSZC_transport_comparison.png)。可选小图：[PDF与Zr配位](../materials/figures/27_LSZC_PDF_and_Zr_coordination.png)。

## 8｜Li₃PS₄：向硫化物网络的转移性

**一句话结论：** NEP89给出接近文献的Ea，但扩散绝对值更大，并显示出明显的动态异质性。

- 材料角色：将阴离子网络从含氯体系切换到P–S硫化物玻璃。
- 输运结果：NEP89 Ea=0.419 eV；Chen DeePMD报告Ea=0.470 eV；扩散比值约3.37–45.5。
- 300 K点不纳入NEP89拟合；拟合区间为500–900 K。
- 强调Ea接近不等于绝对扩散正确。

**左侧结构/轨迹：** [Li₃PS₄分析起始结构](../../materials/evidence/amorphous/Li3PS4/analysis_start.xyz)；[700 K代表轨迹](../../materials/evidence/amorphous/Li3PS4/NEP89_700K_representative_part01.xyz)。用P/S突出PS₄四面体，Li运动以短路径或热图显示。

**右侧主图：** [Li₃PS₄ Arrhenius比较](../materials/figures/31_Li3PS4_Arrhenius_comparison.png)。拟合线与数据点分开表达。可选辅助证据：[局部结构](../materials/figures/07_Li3PS4_local_structure.png) 或 [动态异质性](../materials/figures/28_Li3PS4_dynamic_heterogeneity.png)。

## 9｜LiPON：混合阴离子网络的适用性边界

**一句话结论：** NEP89保留热激活趋势，但Li输运绝对值大幅偏高；这是四系中更严格的局部化学测试。

- 结构问题：N可处于apical/bridging环境；检查P–O–N局部网络及其热稳定性。
- 输运结果：NEP89 Ea=0.428 eV（D）/0.415 eV（σ）；Bates实验Ea=0.55 eV。扩散文献比约6.84×10³–1.65×10⁴。
- Figure 24的Hamon 3.3 μS/cm和Figure 32的Bates 2.3±0.7 μS/cm是不同文献基准。
- Figure 32虚线为Bates 300 K单点与报告Ea构成的外推，不是高温实测系列。

**左侧结构/轨迹：** [LiPON Preparation-B构建结构](../../materials/evidence/amorphous/LiPON/construction_initial.xyz)；[900 K代表轨迹](../../materials/evidence/amorphous/LiPON/NEP89_900K_representative_part01.xyz)。O/N使用不同颜色，并在角落用小示意图区分N局部环境。

**右侧主图：** [LiPON Arrhenius比较](../materials/figures/32_LiPON_Arrhenius_comparison.png)。如需结构佐证，选 [LiPON玻璃结构](../materials/figures/21_LiPON_glass_structure.png) 或 [温度RDF](../materials/figures/25_LiPON_temperature_RDF.png) 之一，避免两图都缩小。

## 10｜跨材料总结与结论

**一句话结论：** 通用NNP适合高效结构构建和趋势筛选，但绝对输运预测需要材料级验证或校准。

| 体系 | 温度/结构表现 | 绝对输运表现 |
|---|---|---|
| 晶体 | 同一基准下不同模型给出不同Ea | 模型选择影响室温外推 |
| LZOC | 可比较AIMD温度响应 | 扩散偏低；不赋单一Ea |
| LSZC | 保持硫酸根相关结构 | 与实验定量对应最好 |
| Li₃PS₄ | 热活化并有动态异质性 | Ea接近但扩散偏高 |
| LiPON | O/N网络仍需严格验证 | 扩散绝对值显著偏高 |

- 应用建议：用通用势做高效构建、长时间机制探索和相对趋势筛选。
- 总结判断：效率让更长轨迹成为可能，但结构可信度和材料级输运验证决定结果能否支持实际筛选。
- 最后强调：NNP的价值来自“速度 × 可验证性”，而不是速度单项。

**建议结尾画面：** 效率、结构可信度、输运准确性三列总结；不把不同指标压成缺乏依据的单一总分。

---

## 11｜提案一：采用分层NNP筛选与验证流程

**提案目标：** 把本研究得到的效率优势用于公司候选材料筛选，同时避免把未经验证的通用势输运值直接作为决策依据。

1. **快速筛选：** 对候选组成和结构使用通用预训练势，比较结构稳定性、相对温度趋势和局部网络特征。
2. **候选收敛：** 对少量优先材料补充材料相关参考计算，例如短程AIMD/DFT或材料专用势，检查结构与Li迁移机制。
3. **定量确认：** 对进入重点决策的材料，用实验或经验证的参考体系校准活化能和绝对传导度。
4. **结果分级：** 明确标出模型适用范围、证据等级和不确定性；未经过校准的通用势结果仅用于相对趋势筛选。

**预期价值：** 将较昂贵的参考计算集中在少数候选材料上，并降低单一通用势高估/低估导致的筛选风险。

**图案建议：** 三阶段漏斗或流程图：通用NNP广筛 → 专项验证候选 → 实验/校准后用于决策。每阶段下方标出对应的计算成本和可信度层级，不预设未经验证的数值门槛。

## 12｜提案二：为一个优先非晶材料启动验证试点

**提案目标：** 与材料团队共同选定一个优先非晶电解质，先验证工作流的可重复性和定量边界，再决定是否扩展到更多组成。

- **结构重复性：** 对同一候选组成构建多个独立玻璃样本，比较密度、RDF/PDF、配位与关键网络单元。
- **输运验证：** 选取代表温度进行长时间MD，报告Li自扩散、条件性Nernst–Einstein传导度和Arrhenius趋势；在计算可行时检查集体电荷输运。
- **参考锚点：** 对关键温度和局部结构使用AIMD/DFT或材料专用势验证，并与可获得的实验结构和传导数据对照。
- **阶段性交付：** 候选材料结构包、轨迹与分析表、模型适用范围/误差说明，以及是否值得扩展筛选的建议。

**试点判据：** 先确认独立玻璃之间的结构与输运差异可量化、主要结论对重复样本稳定，再增加温度点或组成范围。具体误差阈值和资源规模在选定材料后与团队共同确定。

**预期价值：** 将“快速生成结果”推进到“可复现、可对照、可支持材料决策”的非晶筛选流程。

**图案建议：** 以结构重复 → 结构验证 → 输运验证 → 决策报告四步时间线呈现；在旁边列出试点交付物。清楚标注这是后续提案，不是本研究已完成的计算。

## 全套版式建议

- 第6–9页统一采用两栏：左侧约45%放该材料的结构快照/代表轨迹，右侧约55%放一张主结果图及两条结论。
- 每个材料页最多再加一张小型辅助图；RDF、配位和误差细节放backup slides。
- 四种结构图保持视角、原子半径、背景、比例尺、元素配色一致。展示完整玻璃盒时不清楚，就用局部放大并说明视图范围。
- 仓库中的XYZ是为展示与溯源等间隔抽帧的文件。定量分析使用manifest记录的TSUBAME完整轨迹；不要从抽帧文件重新计算MSD或扩散系数。
- 轨迹动画只播放清晰的短片段，并标温度、模型、时间窗口和抽帧方式；Li路径不要遮挡关键网络原子。
- 若演讲时间有限，优先讲清每页标题中的一句话结论，详细模拟条件和次要图表放备份页。
