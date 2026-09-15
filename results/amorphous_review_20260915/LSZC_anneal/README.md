# LSZC 272原子退火：基础验证

后续RDF、配位和作者结构对照现已完成：[日语图文报告](../analysis_complete/report_ja.md)／[英语图文报告](../analysis_complete/report_en.md)。作者结构曲线不是实验RDF，完整非晶与输运验证尚未确立。

来源：TSUBAME任务8674277，300→400 K、100 ps；400 K保温20 ps。NEP89/GPUMD，NVT-MTTK，0.5 fs。原始输入和输出保存在相邻`../source/LSZC_anneal/`；SHA256见`basic_validation.json`。

## 核查结果

- 组成：Li32 Zr32 Cl128 S16 O64，全部1200帧原子顺序与数量一致。
- 升温段2000条、保温段400条18列thermo，均有限值；晶胞体积为正。
- 保温平均温度399.420 K，平均压力0.03957 GPa；NVT固定密度1.86376 g/cm³，不能作为密度收敛证据。
- 保温四个5 ps块势能为−5.460845、−5.461280、−5.461363、−5.461795 eV/atom。末两块相差−0.000431 eV/atom，仍有轻微下降，不宣称严格平衡。
- 保温段最短原子间距1.35098 Å；仅凭全局最短距离不能判断某种化学键合理。
- S–O采用1.9 Å几何截断。升温的16000个S-帧计数中，15997个为4配位、3个为3配位；保温3200个计数中3199个为4、1个为3。最后10 ps全部为4配位。短暂越过截断不能直接解释为断键。
- 最后10 ps平均配位：Zr–O 1.53156（2.6 Å）、Zr–Cl 4.21781（3.2 Å）、Li–O 0.88844（2.8 Å）、Li–Cl 4.275（3.2 Å）。这些是操作性截断定义，不是已验证实验配位数。

## 数据与方法

`ramp_blocks.csv`、`hold_blocks.csv`按时间等分四块；压力为GPUMD三个法向分量平均，势能除以272，密度由原子质量与晶胞行列式计算。

`rdf_late10ps.csv`使用保温最后100帧，0.05 Å bin、0–5 Å范围、周期最小镜像、排除自身配对，按球壳体积和数密度归一化后逐帧平均。本模型晶胞足以覆盖该范围。未进行人为平滑。

`final_candidate.cif`为末态，不是新优化结构。当前检查支持继续探索性结构与输运比较；尚未完成与文献RDF的定量比较，也未单独确认非晶性、尺寸效应或给出扩散系数。

## English

The 272-atom composition and frame ordering are retained. The 400 K hold averages 399.42 K. Energy shows a small residual decrease; all S atoms have four O neighbours in the final 10 ps at a 1.9 Å cutoff. Rare earlier threefold counts are retained as cutoff-defined observations, not interpreted as proven bond breaking. This is a basic numerical/structural screen, not certification of amorphous structure or quantitative transport accuracy.

## 日本語

272原子の組成・原子順序は維持された。400 K保持段の平均温度は399.42 K。エネルギーには小さい低下が残る。最後の10 psでは、1.9 Åのカットオフで全SがO四配位であった。それ以前の少数の三配位計数も記録し、直ちに結合切断とは解釈しない。基本的な数値・構造確認であり、非晶性や輸送特性の定量精度を保証するものではない。
