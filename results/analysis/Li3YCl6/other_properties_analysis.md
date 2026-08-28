# Li₃YCl₆：轨迹的补充分析

本页使用已同步的 LAMMPS 输出进行补充分析，模型按 MACE-MPA-0、SevenNet-nano 和 M3GNet 分开处理。扩散系数与 Arrhenius 拟合不在本页重复定义，重点是检查温度控制、能量/压力波动以及 Li–Cl 局部结构。

## 已生成的图

每个模型的图位于 `results/plots/Li3YCl6/<model>/`：

- `thermo_temperature_stability.png`：目标温度与实际平均温度及波动；
- `thermo_energy_pressure.png`：势能和压力随温度的汇总；
- `*_rdf_LiCl.png`：Li–Cl 径向分布函数；
- `*_coordination.png`：3.0 Å 截断下的平均 Li–Cl 配位数。

原始数值表：

- `results/plots/Li3YCl6/thermo_summary.csv`
- `results/plots/Li3YCl6/coordination_LiCl_summary.csv`

## 读取和解释

- 温度：检查实际温度是否围绕目标温度运行；误差条是轨迹内标准差的模型/温度汇总。
- 能量：观察升温时势能是否连续变化，以及是否出现明显跳变。
- 压力：NVT 中压力本身可以有较大瞬时波动，因此主要用于检查异常漂移，不能仅凭平均压力判定结构失稳。
- RDF：第一峰位置和峰形用于比较 Li–Cl 最近邻环境；峰展宽通常反映热振动和局部无序增加。
- 配位数：采用 Li–Cl 距离 3.0 Å 的统一截断，仅用于模型间相对比较。

## 当前结论边界

这些图可以支持“轨迹是否出现明显热力学或局部结构异常”的初步判断，但不能替代晶格参数、体积、键角分布或长时间相变分析。若要作为最终报告结果，应继续使用同一条轨迹、同一时间区间和同一截断定义进行模型间比较。
