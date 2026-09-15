# 文献流程对照执行记录：2026-09-15

## 最新基础验证更新

8674277与8674278.1–3均已核查完成。已下载LSZC退火输出及新LZOC三温度生产轨迹，进行组成、记录数、有限值、温度/势能/压力分块和末态检查。

- [LSZC基础验证与RDF源数据](../../results/amorphous_review_20260915/LSZC_anneal/README.md)：400 K平均399.42 K，最后10 ps的S均为O四配位；保留少数早期截断计数变化。
- [新LZOC基础验证及探索性MSD](../../results/amorphous_review_20260915/LZOC_transport/README.md)：三温度已结束；MSD已计算并交叉核对，低温采样和拟合窗口影响仍明显，暂不报告正式Ea。

下文为历史提交记录；未完成的是结构与文献定量比较等分析，不是这些作业本身。本轮未新增计算或DFT，尚未Git push。

最新队列复查：LSZC 8674277 已生成全部阶段完成标记，结构结果尚待分析；新 LZOC 8674278.1–3 均为运行状态（r）。以下提交记录保留，不能将“已提交”误读为全部分析完成。本轮尚未 Git push。

采用用户确认的“文献流程对照＋必要检查”标准，不新增DFT，不要求穷尽式势函数验证。计算正常结束不等于定量准确；可比条件与改动仍须注明。本文记录提交，不声称生产结果已完成。

## 提交前必要检查

| 来源任务 | 本次输出 | 检查结果 |
|---|---|---|
| LSZC8674265 |400条thermo及末态 |平均T297.19K、P0.05968GPa；末块T301.58K；16个S均O四配位，最短距离1.389Å。势能仍在松弛，继续退火探索，不宣称平衡 |
| 新LZOC8674222 |1000条thermo及末态 |平均T302.26K、P−0.07995GPa；末两块势能−4.89832、−4.89810eV/atom，末态最短距离1.844Å。允许进入探索性对照，不宣称完成晶胞优化 |

二者密度因NVT恒定，不作为收敛证据。新LZOC三个温度分支同源，非三个独立非晶构型。

## 已提交任务

| 路线 | Job | 流程 | 输出前缀（runs/amorphous/下） |
|---|---|---|---|
| LSZC272原子 |8674277|300→400K NVT100ps（1K/ps）＋400K NVT20ps|LSZC/nep89/packed272_anneal_8674277/|
| 新LZOC192原子 |8674278.1|300→340K10ps＋340K平衡50ps＋production200ps，全NVT|LZOC_Hussain2024/nep89/transport_340K_8674278/|
| 新LZOC192原子 |8674278.2|300→360K10ps＋360K平衡50ps＋production200ps，全NVT|LZOC_Hussain2024/nep89/transport_360K_8674278/|
| 新LZOC192原子 |8674278.3|300→380K10ps＋380K平衡50ps＋production200ps，全NVT|LZOC_Hussain2024/nep89/transport_380K_8674278/|

共同设置：NEP89/GPUMD，0.5fs，MTTK温控周期200步=100fs，保留来源速度，阶段之间重初始化温控状态。thermo0.05ps、轨迹0.1ps、restart1ps。每任务gpu_1=1，walltime上限30分钟，不是预计耗时。各阶段数值结束和有限值检查通过后顺序继续；科学合理性在输出后对照分析，不由脚本自动认证。

文献对应：LSZC的300→400K与1K/ps来自Tang2026 SI图20，400K20ps为本项目选择；不重复图中为初始密度匹配而设的5kbar压缩。团簇提取与装箱为独立改编，未完整复制作者AIMD团簇生成过程。

LZOC340/360/380K来自Hussain2024的48原子输运分支；当前192原子结构按其96原子升降温分支改编。明确是跨分支、跨势函数流程对照，不是严格复现。10/50/200ps为本项目选择，温度跨度较窄，Ea的不确定性与扩散采样不足均需报告，不强行拟合或外推300K。

## 完成后的分析

- LSZC：末段RDF、S–O和Zr配位、温度能量压力、无序结构特征；若300/400K短时轨迹不能解析扩散，只报告结构，不强行给D或Ea。
- 新LZOC：三温度MSD/D、窗口敏感性、框架位移、RDF；只在扩散区间有足够采样时报告Ea。实验电导与自扩散量必须区分，转换使用有明确单位的Nernst–Einstein关系并注明假设。
- Li3PS4：已有结构与输运参考对照继续整理，尚未在本次新增production。LiPON：已知短N–N差异作为局限，现有数据可作探索结构对照，不删除异常。旧LZOC保留MACE/NEP比较。

当前还没有完成所有材料的最终对照，以上待分析项不可写成完成。提交前余额221.65、deposit7.55points；未安排DFT。

## English / 日本語

Submitted LSZC job8674277 (300→400K at1K/ps,100ps;400K20ps hold) and reconstructed-LZOC array8674278.1–3 (340/360/380K;10ps ramp,50ps equilibration,200ps production per branch). All use NEP89/GPUMD,NVT,0.5fs. Literature-informed adaptations, not exact reproduction; noDFT. Completion and final analysis remain pending.

LSZC8674277（300→400K、1K/psで100ps＋400K20ps保持）と新LZOC8674278.1–3（340/360/380K、各10ps昇温＋50ps平衡段＋200ps本計算）を投入。NEP89/GPUMD、NVT、0.5fs。文献を参考にした改編であり厳密再現ではない。DFTは実施せず、終了確認と最終解析は未完了。
