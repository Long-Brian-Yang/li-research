# Li离子输运NNP评估：10页PPT内容大纲

> **贯穿全篇的主线**  
> 先确认NNP和计算引擎能否高效运行，再用晶体基准识别模型差异，最后把工作流扩展到四种化学环境不同的非晶电解质。结论要同时评价计算效率、结构可信度和输运准确性。

本文件供制作PPT时参考。每页列出核心结论、应讲内容、建议图表和素材路径。非晶结构与轨迹文件已在仓库中整理；第8页建议给四种材料各放一个同风格结构/轨迹小图。

参考资料：[materials review](../materials/materials_overview_ja.md) ｜ [结构与代表轨迹清单](../../materials/evidence/README.md) ｜ [结构/轨迹manifest](../../materials/evidence/manifest.json)

---

## 1｜研究目标与整体路线：预训练势能否可靠地预测Li输运？

**一句话结论：** 本研究把计算效率、晶体输运和非晶结构—输运验证串成一条证据链。

- 研究目标：评估预训练神经网络势（NNP）在Li离子输运模拟中的适用范围。
- 路线：NNP/MD引擎效率benchmark → Li₃YCl₆与LiNbOCl₄晶体验证 → LZOC、LSZC、Li₃PS₄、LiPON非晶扩展。
- 三个评价问题：跑得是否足够快？结构是否合理？输运结果与实验、AIMD或材料专用势是否一致？

**建议画面：** 一条由“计算性能”到“晶体”再到“四种非晶化学”的横向研究路线；背景可用结构快照拼图。

**讲述重点：** NNP产生轨迹只是起点，不能代替物理验证。

## 2｜NNP性能benchmark：计算效率如何支持长时间MD？

**一句话结论：** GPU化和NEP89/GPUMD显著提高了生产计算效率，为大体系、长轨迹提供计算条件；速度本身不代表精度。

- M3GNet–LAMMPS：从CPU迁移到1块H100 GPU，吞吐量由3.285提升至56.621 steps/s，约17.2倍。
- 600 K production对比：MACE/LAMMPS为189.93 min，NEP89/GPUMD为6.11 min，约31.1倍时间差。
- 清楚标注模型、MD engine、硬件和测试条件；避免把不同硬件/工作流说成完全同条件精度对比。

**建议主图：** [MACE–NEP runtime与density比较](../materials/figures/09_MACE_NEP_runtime_density.png)。CPU/GPU吞吐量可做成旁边的大数字或小条形图。

**布局：** 左侧展示17.2倍、右侧展示31.1倍；底部放一句“效率比较与精度验证分开进行”。

## 3｜晶体benchmark设计：两个晶体、三种通用模型

**一句话结论：** 先在结构规则、文献数据较清楚的晶体中比较模型，为非晶测试建立基线。

- Li₃YCl₆：240原子有序结构；MACE-MPA-0、SevenNet-nano、M3GNet GPU。
- LiNbOCl₄：336原子有序结构；采用相同三模型比较思路。
- 使用多温度NVT轨迹，从Li MSD得到扩散系数，再由Arrhenius关系拟合Ea并外推室温值。
- 参考实验值：Li₃YCl₆的Ea约0.400 eV；LiNbOCl₄的Ea约0.240 eV。说明实验传导度换算和自扩散并非同一物理量。

**结构图素材：** [Li₃YCl₆初始晶体结构](../../materials/evidence/crystalline/Li3YCl6/initial_structure.xyz)；[LiNbOCl₄初始晶体结构](../../materials/evidence/crystalline/LiNbOCl4/initial_structure.xyz)。

**建议画面：** 上半部并排显示两个晶体结构，下半部用简洁图标表示“三模型 × 多温度 × MSD/Arrhenius”。

## 4｜晶体结果：模型选择会改变输运预测

**一句话结论：** 三种通用势的预测并不等价，晶体结果已显示出模型依赖性。

| 材料 | MACE-MPA-0 Ea | SevenNet-nano Ea | M3GNet GPU Ea | 实验基准Ea |
|---|---:|---:|---:|---:|
| Li₃YCl₆ | 0.302 eV | 0.246 eV | 0.212 eV | 0.400 eV |
| LiNbOCl₄ | 0.313 eV | 0.357 eV | 0.397 eV | 0.240 eV |

- Li₃YCl₆：三种模型都显示温度升高时Li扩散增加，但Ea和室温外推值有差异。
- LiNbOCl₄：模型间差异仍明显；M3GNet的Arrhenius线性较弱，R²=0.8768。
- 这一页的结论是“模型必须验证”，不需要在10页内逐一解释所有误差来源。

**建议主图：** [Li₃YCl₆模型间MSD](../materials/figures/01_Li3YCl6_three_model_MSD.png)、[LiNbOCl₄模型间MSD](../materials/figures/02_LiNbOCl4_three_model_MSD.png)；空间足够时在角落放[两种晶体的Arrhenius图](../materials/figures/03_Li3YCl6_Arrhenius.png)与[LiNbOCl₄ Arrhenius图](../materials/figures/04_LiNbOCl4_Arrhenius.png)。

**视觉提醒：** 不要同时塞入全部MSD、Ea、D(300 K)和实验线；选一组主图，其他数值放口头说明或备份页。

## 5｜为什么研究非晶：输运还取决于局部网络和制备历史

**一句话结论：** 非晶电解质没有单一的周期晶格路径，Li输运需要与无序网络结构一起评估。

- 非晶结构具有分布式键长、配位和自由体积，平均组成无法完整描述局部Li环境。
- 相似的Li局部运动是否能形成连续长程传输，取决于宿主网络的拓扑和连接性。
- 熔融、淬火、退火等热历史会改变结构，因此需要结合密度、RDF、配位、骨架运动和MSD分析。
- 研究意义：测试预训练势离开规则晶格后，是否仍能保持合理的玻璃结构和热激活趋势。

**建议画面：** 左侧晶体的规则迁移路径，右侧非晶中多种局部配位与不均匀Li路径；旁边用“结构 + 动力学 + 输运”三个标签。

## 6｜为何选择四种材料：构成化学多样的benchmark

**一句话结论：** 四个体系逐步改变阴离子网络和局部化学，能测试不同类型的势函数转移性。

| 材料 | 化学位置 | 选择理由／主要考验 |
|---|---|---|
| LZOC | 含氧锆氯化物玻璃 | 延续原始氧氯化物问题；与AIMD温度响应比较 |
| LSZC | 硫酸根修饰的锆氯化物玻璃 | 在氯化物背景中加入SO₄单元；检验结构保持与实验定量对应 |
| Li₃PS₄ | 硫代磷酸盐玻璃 | 从氯化物网络切换到P–S硫化物网络；检验跨阴离子转移 |
| LiPON | 磷酸盐氧氮化物玻璃 | 加入N并引入apical/bridging等局部环境；检验混合阴离子和网络拓扑 |

**建议图示：** 四列材料卡片或化学跨度轴：O–Cl锆盐 → SO₄/Cl混合网络 → P–S网络 → P–O–N网络。每格放组成式、网络简图和对应参照类型。

**讲述重点：** 这是按化学挑战和文献基准设计的一组benchmark，不是四个互不相关的材料案例。

## 7｜非晶计算流程：从玻璃结构到可比较的输运量

**一句话结论：** 用同一条分析逻辑检查各材料，同时保留材料间合理不同的参考证据。

1. 构建并弛豫非晶结构，记录组成、密度和热处理历史。
2. 先检查结构：密度、RDF/PDF、配位、关键多阴离子/混合阴离子单元、宿主骨架稳定性。
3. 对多个温度做NEP89/GPUMD输运模拟；从完整轨迹计算Li MSD、扩散系数及Arrhenius行为。
4. 与各材料对应的AIMD、实验、DeePMD或材料专用MLIP进行比较。
5. 分开报告温度趋势、活化能和绝对扩散/传导度偏差；不把不同物理量直接混算。

**建议图示：** “结构制备 → 结构验证 → 多温度MD → MSD/Arrhenius → 文献对照”的流程图，底部标出不同材料采用的参考证据。

## 8｜非晶结构结果：四个体系各自展示结构或轨迹

**一句话结论：** 结构可视化要让观众看见每个材料的真实原子网络，并与该体系的输运/结构证据对应。

**建议用四宫格；每格都放一张由该材料XYZ渲染的原子结构图，并在图下配一条短Li路径或代表轨迹缩略图。**

| 材料 | 结构/轨迹素材 | 配套结构证据 |
|---|---|---|
| LZOC | [analysis_start.xyz](../../materials/evidence/amorphous/LZOC/analysis_start.xyz)；[340 K代表轨迹](../../materials/evidence/amorphous/LZOC/NEP89_340K_representative_part01.xyz) | [RDF](../materials/figures/15_LZOC_RDF.png)、[配位](../materials/figures/16_LZOC_coordination.png) |
| LSZC | [analysis_start.xyz](../../materials/evidence/amorphous/LSZC/analysis_start.xyz)；[330 K代表轨迹](../../materials/evidence/amorphous/LSZC/NEP89_330K_representative_part01.xyz) | [局部RDF](../materials/figures/19_LSZC_partial_RDF.png)、[PDF/Zr配位](../materials/figures/27_LSZC_PDF_and_Zr_coordination.png) |
| Li₃PS₄ | [analysis_start.xyz](../../materials/evidence/amorphous/Li3PS4/analysis_start.xyz)；[700 K代表轨迹](../../materials/evidence/amorphous/Li3PS4/NEP89_700K_representative_part01.xyz) | [局部结构](../materials/figures/07_Li3PS4_local_structure.png)、[动态异质性](../materials/figures/28_Li3PS4_dynamic_heterogeneity.png) |
| LiPON | [Preparation-B structure](../../materials/evidence/amorphous/LiPON/construction_initial.xyz)；[900 K代表轨迹](../../materials/evidence/amorphous/LiPON/NEP89_900K_representative_part01.xyz) | [玻璃结构](../materials/figures/21_LiPON_glass_structure.png)、[温度依赖RDF](../materials/figures/25_LiPON_temperature_RDF.png) |

**渲染建议：** 四格保持同一视角、背景、比例尺和Li颜色；突出各自关键网络（SO₄、PS₄、磷酸盐/N环境等）。若用动态轨迹，播放短片段即可，不要把整段动画缩小到看不清。

**重要说明：** 清单中的XYZ是从完整轨迹等间隔抽帧的可视化/溯源材料；定量分析使用manifest记录的完整TSUBAME轨迹，不从抽帧XYZ重新计算MSD或扩散系数。

## 9｜非晶输运结果：温度趋势与绝对偏差要分开讲

**一句话结论：** 四系整体显示热激活行为，但绝对输运准确度有明显材料依赖性。

| 材料 | NEP89 Ea | 文献Ea | 主要比较结论 |
|---|---:|---:|---|
| LZOC | 不正式赋值 | AIMD温度响应 | 温度趋势可比，扩散尺度约为参照的0.22–0.35 |
| LSZC | 0.351 eV | 0.330 eV | 与实验定量对应最好，硫酸根结构得以保持 |
| Li₃PS₄ | 0.419 eV | 0.470 eV | Ea接近，但绝对扩散高约3.37–45.5倍，且有动态异质性 |
| LiPON | 0.428 eV（D）/0.415 eV（σ） | 0.550 eV | 保持热激活趋势，但扩散比值高约6.84×10³–1.65×10⁴ |

**建议图表：**
- 主体用一张上述比较表或分面dot plot呈现Ea和输运比值。
- 小图只选2–4张关键Arrhenius图，避免四图缩小后标签不可读：优先LSZC、Li₃PS₄、LiPON；LZOC用其温度响应图并标注“不作单一Ea拟合”。
- 可链接全部四图：[LZOC](../materials/figures/29_LZOC_Arrhenius_comparison.png) ｜ [LSZC](../materials/figures/30_LSZC_Arrhenius_comparison.png) ｜ [Li₃PS₄](../materials/figures/31_Li3PS4_Arrhenius_comparison.png) ｜ [LiPON](../materials/figures/32_LiPON_Arrhenius_comparison.png)。

**讲述重点：** Ea接近不等于扩散绝对值正确；实验传导度、条件性Nernst–Einstein传导度和Li tracer diffusion要标清物理量。

## 10｜结论与下一步：把效率优势转成可控的材料筛选

**一句话结论：** 通用NNP适合高效结构构建和趋势筛选；绝对输运预测仍需要材料级验证或校准。

- 性能：GPU/NEP工作流显著缩短长时间MD所需时间。
- 晶体：模型差异已经影响Ea与室温外推，说明模型身份和验证条件不能省略。
- 非晶：四种化学环境下，结构/温度趋势具有可分析性，但绝对输运偏差因材料而异。
- 应用建议：先用通用势筛选结构与相对趋势，再对重点材料进行材料专用势验证、AIMD短轨迹校验或实验校准。

**建议结尾画面：** “效率 × 结构可信度 × 输运准确度”三列总结，不合并成缺乏依据的总分；右下角放下一步验证路线。

---

## 全套视觉统一规则

- 所有非晶结构图统一相机角度、边框、元素色和Li高亮色；结构快照必须标材料、温度和模型。
- 每页一个主要结论；通常一张主图加最多两张辅助图。正文不要重复图题里的信息。
- 四宫格如果原子结构太密，显示局部放大而非整盒原子球；标一个周期盒示意或尺度信息。
- 轨迹视频只用于说明代表性运动路径，并注明温度、时间窗口及抽样方式；定量判断以完整轨迹分析和图表为准。
- 如果汇报时间较短，保留第8页四材料结构四宫格，第9页用精简对比表；详细RDF、协调数、误差分析放入backup slides。
