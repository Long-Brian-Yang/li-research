# 方向 2：高速ハライド固体電解質の再現と輸送解析

## 1. 研究課題と範囲

方向 2 では、高伝導ハライドおよびオキシハライドの報告構造を再構築し、
構造緩和、安定性評価、Li イオン輸送解析を再現可能な原子論的ワークフローで
実施する。

> **Li₃YCl₆ と LiNbOCl₄ の Li サブ格子は、物理的に安定な三次元 Li⁺
> 移動ネットワークを形成するか。また、計算された輸送傾向を報告された
> 実験伝導度と整合的に説明できるか。**

本研究はまず再現計算から開始するが、最終的な目的は二つの材料を個別に比較
することではなく、構造指針に基づく材料探索を構築することである。二つの参照
材料は、構造、配位多面体、ordering 仮説、Li 輸送を整理するための基準点である。
大規模な組成探索は、参照材料が各ゲートを通過した後に行う。

研究全体の流れは次の通りである。

```text
高伝導度論文と NGK データ
        ↓ Step 1：空間群、多面体配置、Li 移動ネットワークを整理
元素制約を考慮した組成置換
        ↓ Step 2：構造変化を予測し、明示的モデルを構築
MD による輸送スクリーニング
        ↓ Step 3：候補を順位付けし、明確な go/no-go 結論を出す
```

### インターンシップとしての完了目標

本研究は論文投稿用の完全検証ではなく、インターンシップ成果物としての
再現可能な研究 workflow を完成させることを目的とする。構造指針、明示的な
モデル、ML-MD 解析、優先または除外する領域の結論を説明できればよい。
3–5 ns の長時間計算、完全な DFT force validation、Green–Kubo 伝導度、全元素の
網羅探索、論文レベルの不確実性評価は追加課題であり、完了条件ではない。

### 現在の実行状況

| 作業 | 状態 |
|---|---|
| 文献と構造参照の整理 | 完了 |
| 明示的 ordered model | 制限付きで完了 |
| NEP89/GPUMDkit 300 K screening | 完了；主 fit は 100–300 ps |
| MACE-MPA-0 400 K 計算 | 実行中：job 8441077–8441080 |
| potential 間の比較 | MACE 完了後に実施 |

4 つの MACE job は 10 ps equilibration、100 ps production、1 fs timestep、
各 14 h walltime で実行している。

## 2. 参照材料と実験ベンチマーク

| 系 | 方向 2 における役割 | 構造参照 | 実験ベンチマーク |
|---|---|---|---|
| **Li₃YCl₆** | 高電圧ハライド benchmark；空孔と site ordering の影響を検証 | 報告された平均構造は (P\bar{3}m1) (No. 164)。MD には明示的な有序モデルが必要 | Asano *et al.*, 2018：室温伝導度 >1 mS cm⁻¹ ([DOI](https://doi.org/10.1002/adma.201803075)) |
| **LiNbOCl₄** | mixed-anion オキシハライドの高伝導 benchmark | screenshot 由来の参照は (Cmc2_1) (No. 36)。O/Cl と Li の占有を明示化する必要 | Tanaka *et al.*, 2023：室温 (\sigma_{Li}\approx10.4) mS cm⁻¹ ([DOI](https://doi.org/10.1002/anie.202217581)) |

実験値は圧粉体の EIS 伝導度であり、MD が最初に与えるのは tracer 拡散係数と
Nernst–Einstein 推定値である。比較表には温度、セルサイズ、計算時間、伝導度の
定義、不確実性を必ず明記する。

## 3. 構造ファイルに関する必須方針

screenshot から再構成した CIF は、部分占有と disorder を含む平均結晶構造で
ある。全サイトをそのまま展開すると組成が誤る。特に Li₃YCl₆ の screenshot
CIF を直接展開すると、目標組成とは異なる原子数になる。これらの CIF は出典
記録と可視化確認にのみ使用する。

production input は次の条件をすべて満たさなければならない。

- 明示的な full-occupancy atom list であること。
- 元素数と nominal formula が正しいこと。
- 周期セル、有限座標、重複原子なしであること。
- production 前に周期境界を含む最短原子間距離を検証すること。
- source、ordering、relaxation 状態、validation JSON、commit を記録すること。

現在の Li₃YCl₆ 候補は三つの異なる Li/Y ordering である。これらは実験構造を
確定する三つのコピーではなく、輸送感度を調べる独立な構造仮説である。

## 4. 現在の構造セット

| 系 | production サイズ | 原子数 | 目的 |
|---|---:|---:|---|
| Li₃YCl₆ model 01–03 | 2×2×4 | 各 480 | 主な有限サイズ・replica 解析。緩和済み 2×2×2 セルを (c) 軸方向に一回繰り返す |
| LiNbOCl₄ | 2×2×2 | 2×2×2 model | 実行可能なセルサイズでの比較 benchmark |

Li₃YCl₆ 2×2×4 候補の組成は Li₁₄₄Y₄₈Cl₂₈₈ であり、最短原子間距離は約
2.39–2.46 Å である。これは入力が幾何学的に使用可能であることを示すが、
緩和済みセルを繰り返しただけであり、独立した 2×2×4 full relaxation と同じ
ではない。論文レベルの主張には、追加の full relaxation が必要である。

構造ファイルは [`structures/ordered/`](../../structures/ordered/) に整理して
いる。生成した CIF、XYZ、LAMMPS data、validation file は
[`structures/ordered/Li3YCl6/2x2x4/`](../../structures/ordered/Li3YCl6/2x2x4/)
に保存されている。

## 5. ワークフローと判定ゲート

```text
reference CIF / 報告構造
        ↓
明示的な占有・ordering model
        ↓  Gate 0：組成、幾何、出典
MACE または DFT 構造緩和
        ↓  Gate 1：収束、崩壊なし、妥当な体積
supercell と周期境界の確認
        ↓  Gate 2：有限サイズと短時間安定性
300 K ML-MD：平衡化 + production replica
        ↓  Gate 3：温度、エネルギー、距離、MSD の安定性
MSD → DLi → σNE；可能なら charge-current 解析
        ↓  Gate 4：block 不確実性と手法比較
移動機構の解析と実験比較
        ↓
再現レポート、または明示的に記録した失敗モード
```

### Gate 0 — 構造整合性

potential を呼び出す前に、以下を記録する。

| 確認項目 | 合格条件 |
|---|---|
| 組成 | 目標 ordered composition と一致し、削除操作で化学式を合わせていない |
| 占有率 | production site の occupancy がすべて 1.0 |
| 座標 | 座標と cell の全要素が finite |
| 距離 | 非物理的な重なりがなく、周期最短距離を報告 |
| セル | 正しい triclinic vector、角度、周期境界 |
| 出典 | source CIF、ordering rule、generator、validation commit を記録 |

### Gate 1 — 構造緩和

まず MACE-MPA-0 または DFT で原子位置を緩和する。必要に応じて体積・セルの
緩和を続けるが、checkpoint、GPU、収束条件、cell shape を固定したかどうかを
記録する。Li₃YCl₆ の三つの ordering は、輸送感度が判明するまで保持する。

緩和後には少なくとも次を確認する。

- force と energy の収束。
- 体積・密度の異常な変化がないこと。
- Li–Cl、Y–Cl、Nb–O、Nb–Cl の短すぎる接触がないこと。
- framework の崩壊や原子重なりがないこと。
- 緩和後も framework が化学的・幾何学的に妥当であること。

MACE-MPA-0 と NEP89 は screening tool であり、単独で実験構造や実験伝導度を
検証するものではない。

### Gate 2 — セルサイズと短時間安定性

Li₃YCl₆ は parent (c) 軸が短く、既報の Li₃YCl₆ MLMD でも伝導度と superionic
transition が supercell size に敏感であるため、2×2×4 を優先する。LiNbOCl₄
は parent (c) 軸が比較的長いため、2×2×2 を実用的な baseline とする。

長時間計算の前に 1,000–10,000 step の GPU smoke test を行い、以下を確認する。

- potential が全元素を認識すること。
- 最終 step までエラーなく到達すること。
- 温度制御が有効であること。
- trajectory 上で原子が周期境界を越えても異常な飛びを示さないこと。
- エネルギーまたは距離に急激な破綻がないこと。

## 6. 構造指針に基づく探索への拡張

今回のコメントを踏まえると、方向 2 の成果は伝導度の数値だけでは不十分で
あり、どの構造領域を優先または除外できるかを示す必要がある。

### Step 1 — 高伝導構造モチーフの整理

論文と NGK 試行データを、空間群、stacking、配位多面体の接続、Li site の
topology、vacancy pattern、anion arrangement で整理する。空間群だけでは不十分
であり、同じ空間群でも Li bottleneck と移動ネットワークが異なる可能性がある。
Li₃YCl₆ と LiNbOCl₄ はこの構造地図の基準点であり、候補全体ではない。

### Step 2 — 元素制約下の組成置換と構造予測

元素制約を守りながら、Step 1 で抽出した構造モチーフ内で cation/anion を置換
する。組成を変えると安定空間群、多面体配置、Li vacancy network が変わり得る
ため、一つの CIF を盲目的に再利用せず、妥当な構造を予測または列挙できる
workflow が必要である。候補は NGK データと論文を基礎にし、明示的 ordering、
relaxation、安定性チェックを行う。

### Step 3 — MD スクリーニングと判断

構造と安定性のゲートを通過した候補だけを MD で評価する。輸送、構造・機械的
安定性、合成可能性、元素制約を合わせて順位付けする。候補数が多い場合は、
記録可能な surrogate model または descriptor model で MD 候補を絞る。負の結果も
有用であり、除外できる構造・組成領域を明確に示す。最終報告には必ず結論または
go/no-go 境界を記載し、「予測モデルを作れなかった」だけで終わらせない。

## 7. production MD プロトコル

室温付近の最初の production protocol は次のように固定する。

| パラメータ | 値 |
|---|---:|
| Ensemble | Langevin NVT |
| 温度 | 300 K |
| timestep | 1 fs |
| equilibration | 100 ps (100,000 step) |
| production | 1 ns (1,000,000 step) |
| 座標出力 | 1,000 step ごと (1 ps) |
| thermodynamic output | 1,000 step ごと |
| 独立 replica | Li₃YCl₆: 3；LiNbOCl₄: 初期 1、必要なら追加 |

TSUBAME の入口は
[`gpumd_nep89_300K_2x2x4.sh`](../../hpc/tsubame_26icp/gpumd_nep89_300K_2x2x4.sh)
である。production では Li₃YCl₆ 2×2×4 と LiNbOCl₄ 2×2×2 を使用する。
別の potential と比較する場合も、まず同じ protocol を使う。

### 1 ns は最初の production であり、最終値を保証しない

300 K では 400 K より Li 移動が遅くなる可能性がある。1 ns は安定した MSD
linear regime の有無を調べるには有効だが、統計誤差が小さいとは限らない。
production を少なくとも 5 block に分割する。block 間の D の変動が約 30% を
超える場合は、精密な数値を報告せず、その系を 3–5 ns に延長する。

## 8. 輸送解析

### 7.1 Li-only MSD と自己拡散

skewed な Li₃YCl₆ cell では、full triclinic cell を使った fractional-coordinate
unwrapping を行う。単純な Cartesian minimum-image unwrapping は安全ではない。

Li 原子だけについて次を計算する。

\[
\mathrm{MSD}(t)=\left\langle\left|\mathbf r_i(t)-\mathbf r_i(0)\right|^2\right\rangle_i
\]

明確に linear な production interval のみを fit する。三次元 Einstein estimate は

\[
D_{Li}=\frac{1}{6}\frac{d\,\mathrm{MSD}(t)}{dt}.
\]

fit window、slope、Li 数、frame 数、replica mean、replica standard deviation、
block confidence interval を記録する。

### 7.2 伝導度の定義

初期推定には Nernst–Einstein 式を使う。

\[
\sigma_{NE}=\frac{n_{Li}q_{Li}^{2}D_{Li}}{k_BT}.
\]

これは Li の self-diffusion に基づき、distinct Li–Li correlation を無視する。
したがって、厳密な実験伝導度として表示してはいけない。可能なら collective
charge-current または Green–Kubo conductivity も計算し、

\[
H=\frac{\sigma_{collective}}{\sigma_{NE}}
\]

を Haven/correlation factor として報告する。σ<sub>NE</sub> だけを得た場合は、
全表と図で `Nernst–Einstein estimate` と明記する。

### 7.3 追加する機構解析

輸送が観測された候補について、次を計算または可視化する。

- Li probability density と site occupation。
- 方向別 MSD ((x,y,z)) と異方性。
- Li–Li および Li–framework radial distribution function。
- Li coordination number と局所 bottleneck size。
- residence time と jump-length distribution。
- framework RMS displacement と minimum-distance history。
- O/Cl または Y/Nb の局所環境と Li jump の相関。

目的は、単なる数値ランキングではなく、二つの材料の差を構造的に説明する
ことである。

## 9. 温度と実験値の比較

解釈の前に計算と実験の条件をそろえる。

| 項目 | 実験 | 現在の ML-MD |
|---|---|---|
| 温度 | 通常は約 298 K | 300 K production；既往 screening は 400 K |
| 試料 | 圧粉体；bulk、grain boundary、packing を含む | 理想的な周期 ordered crystal |
| 観測量 | EIS total ionic conductivity | Li tracer (D)、および σ<sub>NE</sub> |
| disorder | 実験の平均・disordered structure | replica ごとの一つの explicit ordering |

室温 benchmark は Li₃YCl₆ が約 1 mS cm⁻¹ 超、LiNbOCl₄ が 10.4 mS cm⁻¹ である。
400 K の計算値を 298 K の実験値と直接比較してはいけない。Arrhenius 外挿を示す
場合は、測定または独立に妥当化した activation energy とその不確実性を併記する。

## 10. 再現判定

### Reproduction pass

次の条件を満たしたとき、方向 2 の reproduction stage を通過とする。

1. production structure の組成が正しく、trajectory 中も安定である。
2. independent ordering または replica が再現可能な輸送傾向を示す。
3. MSD fit に記録可能な linear window がある。
4. fit window や block size を変えても結論が変わらない。
5. 温度と conductivity definition の実験との差を明記する。
6. 少なくとも一つの independent potential または DFT short trajectory で
   force/structure sanity check を行う。

計算値が EIS 値と完全一致する必要はない。精密に見える不確かな数値より、
再現可能な傾向と定量化された差の方が有用である。

### No-go または再構築条件

以下の場合はモデルを止めて作り直す。

- explicit model の組成が違う、または hidden partial occupancy が残る。
- MD 中に構造崩壊または非物理的な短距離接触が生じる。
- 非線形 MSD plateau や少数の jump だけから拡散を推定している。
- 一つの短い trajectory だけで強い結論を出している。
- σ<sub>NE</sub> を collective または experimental conductivity として報告する。
- generic potential が force/energy 検証なしに極端な高移動度を示す。

## 11. データと報告の checklist

各 run directory には以下を保存する。

```text
model.cif or model.xyz
validation.json
run.in
thermo.out
dump.xyz
gpumd.out or lammps.log
msd.csv
diffusion_summary.json
figure_msd.png
figure_thermo.png
```

最終比較表には少なくとも以下を含める。

```text
material | ordering_id | supercell | potential | T_K | equilibration_ps |
production_ns | n_Li | fit_window_ps | D_Li_cm2_s | sigma_NE_mS_cm |
sigma_collective_mS_cm | block_std | structure_status | confidence | source
```

すべての値に `experimental`、`calculated`、`target` のいずれかを付け、温度、
手法、単位、出典を記録する。

## 12. 直ちに実施する項目

1. 現在の 300 K、1 ns GPUMD/NEP89 run を完了し、四つの exit status を確認する。
2. corrected triclinic trajectory に対して MSD と block analysis を行う。
3. Li₃YCl₆ の 2×2×4 結果と、以前の 2×2×2・400 K screening をサイズ・温度
   感度の比較として整理する。
4. LiNbOCl₄ の single-run uncertainty が大きければ replica を二つ以上追加する。
5. 代表構造を MACE-MPA-0 と比較する。DFT force の spot check は時間があれば
   追加する。
6. collective charge correlation を確認するまで、σ<sub>NE</sub> を単に「ionic
   conductivity」と表記しない。

## 13. リポジトリの入口

- [`structures/`](../../structures/) — ordered CIF/XYZ/LAMMPS input と validation metadata
- [`simulation/gpumd_nep89/`](../../simulation/gpumd_nep89/) — NEP89 protocol、解析、図
- [`simulation/mace_mpa0/`](../../simulation/mace_mpa0/) — MACE-MPA-0 と LAMMPS workflow
- [`hpc/tsubame_26icp/`](../../hpc/tsubame_26icp/) — TSUBAME job script
- [`docs/literature/papers_zh.md`](../literature/papers_zh.md) と
  [`docs/literature/papers_ja.md`](../literature/papers_ja.md) — 二言語の文献ノートと
  DOI 付き実験 context
