# ハライド固体電解質 論文整理（日本語）

## 車載全固体電池に向けた開発フレームワーク

この文献群の目的は、単なるハライド SSE の調査から、車載全固体電池の要求仕様から候補材料を逆算する段階へ移行することである。低コスト・低毒性・入手性のよい元素空間で、合成可能かつ機械的に柔軟で、高速 Li⁺ 輸送を示す新構造を探索する。

### 定量的な開発目標

| 目標特性 | 目標値 | 優先度 | 主な評価方法 |
|---|---:|---|---|
| Li⁺ 伝導度 | >10 mS cm⁻¹ | 高 | 分子動力学（MD）：MSD → D<sub>Li</sub> → σ<sub>Li</sub> |
| 成形性 / Young’s modulus | <30 GPa | 高 | 第一原理弾性テンソル C<sub>ij</sub> → E |
| 合成可能性 | 低い energy above hull | 高 | energy above hull / 熱力学スクリーニング |
| 低コスト | rare-element-free を優先 | 中 | 元素組成、価格、サプライチェーン |
| 耐酸化性 | >5 V vs. Li | 中 | 分解反応エネルギー / 酸化電位 |
| 化学安定性 | 正極との副反応なし | 中 | 正極との反応エネルギー ΔE<sub>reaction</sub> |
| 耐熱性 | 150 °C で劣化なし | 低 | 熱分解・速度論関連計算 |

高優先度は単なる「最高伝導度」ではなく、次の組合せである。

> **Fast Li transport + Mechanical compliance + Synthesizability**

電気化学的安定窓と実際の正極適合性は別々に評価する必要がある：`electrochemical window ≠ actual cathode compatibility`。

### 3つの候補組成の位置づけ

| 候補 | 代表組成・構造 | 現在の強み | 現在のボトルネック | 開発上の位置づけ |
|---|---|---|---|---|
| Composition 1 | Li–Zr–Ta–Gd–Cl–O；約 Li₁.₅Zr₀.₃Ta₀.₆Gd₀.₁Cl₄.₈O₀.₆ | σ≈3 mS cm⁻¹；E≈12 GPa で力学目標を達成 | Ta/Gd は高コスト；耐酸化性は約4.2 V；σは未達 | mechanical-compliance benchmark |
| Composition 2 | Li–La–Zr–Ta–Cl–O–Br；P6₃/m-related framework | σ≈5 mS cm⁻¹で輸送性が最良 | La/Ta は rare-element-free でない；10 mS cm⁻¹未満 | high-conductivity framework benchmark |
| Composition 3 | Li–Zr–Al–Cl–O；1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ | 低コスト・低毒性・入手性；E≈1.41 GPa | σ≈2–2.5 mS cm⁻¹で、さらなる向上が必要 | 産業化を見据えた baseline |

### 候補材料の探索手順

1. **存在性スクリーニング：** energy above hull で現実的な合成可能性を確認する。
2. **輸送スクリーニング：** 熱力学スクリーニングを通過した候補について MD を行い、MSD、D<sub>Li</sub>、σ<sub>Li</sub> を計算する。目標は >10 mS cm⁻¹。
3. **力学スクリーニング：** C<sub>ij</sub> から Young’s modulus を求め、E<30 GPa を目指す。
4. **電気化学スクリーニング：** V<sub>ox</sub>>5 V と、候補/正極間の ΔE<sub>reaction</sub> を同時に評価する。
5. **多目的トレードオフ：** 全指標を同時に満たせない場合は、伝導度・機械的コンプライアンス・合成可能性という高優先度項目を優先する。

### 元素・アニオンのスクリーニングルール

| 区分 | 現在のルール | 候補空間への意味 |
|---|---|---|
| 優先元素 | Li、Zr、Al、O、Cl | 低コスト・低毒性・入手性がよく、Composition 3 の基盤となる |
| 少量なら許容 | Zr、Nb；Ga/Ge など | 主元素ではなく構造・輸送制御用の微量添加として検討 |
| コスト面で不利 | Ta、Gd、La、および Mo–Hg 付近の多くの遷移金属 | benchmark には使えるが産業化主体系には不向き |
| 注意して使用 | Zn | 耐酸性低下や電子伝導発現の懸念 |
| 原則回避 | In および図示された毒性元素 | 安全・環境・規制上のリスク |
| 硫黄の条件付き使用 | SO₄²⁻ は可；S²⁻ は不可 | 硫黄全体ではなく sulfide 型の化学空間を排除 |
| 供給性で除外 | 図示された灰色領域 | 計算性能が高くても入手性が低ければ候補から除外 |

**現在の中心課題：** rare-element-free の Li–Zr–Al–O–Cl など低コスト化学空間で、合成可能かつ十分に柔らかく、σ<sub>Li</sub>>10 mS cm⁻¹ を示す新構造を見つけること。

### 3つの開発方向と論文の対応

| 方向 | 具体的な意味 | 主な論文 | プロジェクトでの役割 |
|---|---|---|---|
| **方向 1：機械的コンプライアンス** | Young’s modulus <30 GPa、圧密性、サイクル変形への追従 | Hu 2023、Hu 2026；Asano 2018 | 力学 benchmark を作り、高伝導候補の硬さを制約 |
| **方向 2：高伝導構造** | P6₃/m、空孔/相転移、mixed-anion、3D migration network | Asano 2018、Kim 2021、Tanaka 2023、Yin 2023、Li 2024 | 現在の主線：σ を 2–5 mS cm⁻¹ から >10 mS cm⁻¹ へ向上 |
| **方向 3：低コスト化学空間** | rare-element-free の Li–Zr–Al–O–Cl、低毒性、入手性 | Wang 2021、Hu 2023、Hu 2026 | 産業化に向けた元素空間とコストを制約 |
| **総合フレームワーク** | 伝導、力学、安定性、コスト、実用 ASSB を統合評価 | Li & Du 2025（Review） | 3方向を統一的に評価する方法を提供 |

**現在の主線：** この 9 論文は**方向 2**を transport/framework の主線とし、方向 1 の力学的制約と方向 3 の産業化制約を組み合わせて最終候補を絞り込む。

## 1. Asano et al., 2018 — Advanced Materials

### Type
Research Article（原著論文）

### Title
Solid Halide Electrolytes with High Lithium-Ion Conductivity for Application in 4 V Class Bulk-Type All-Solid-State Batteries

### Material
Li₃YCl₆、Li₃YBr₆

### Keywords
Li₃YCl₆ · Li₃YBr₆ · ハライド SSE · chloride SSE · 高電圧正極 · イオン伝導度 · grain-boundary resistance · 変形性 · 酸化安定性 · bulk-type ASSB

### 3文要約
1. Li₃YCl₆ と Li₃YBr₆ という高 Li⁺ 伝導性のハライド固体電解質を報告し、室温で >1 mS cm⁻¹ の伝導度を達成した。
2. 材料は良好な変形性と酸化安定性を示し、冷間加圧ペレットでは顕著な追加 grain-boundary resistance が見られなかった。
3. ハライド SSE を 4 V 級正極へ直接適用できることを実証し、現代の chloride solid electrolyte 研究の重要な基盤を築いた。

### 開発目標との関連
高電圧ハライド SSE の実現可能性を示し、`>5 V` の耐酸化性と 4 V 正極適合性の基準を与える。一方、車載目標には mS cm⁻¹ 級伝導度だけでは不十分である。

### DOI
[10.1002/adma.201803075](https://doi.org/10.1002/adma.201803075)

## 2. Kim et al., 2021 — ACS Materials Letters

### Type
Research Article（原著論文）

### Title
Lithium Ytterbium-Based Halide Solid Electrolytes for High Voltage All-Solid-State Batteries

### Material
Li₃YbCl₆、Li₃₋ₓYb₁₋ₓZrₓCl₆

### Keywords
Li₃YbCl₆ · Zr 置換 · 異価ドーピング · Li 空孔 · 相転移 · trigonal 相 · orthorhombic 相 · 高電圧安定性 · 混合金属ハライド · migration network

### 3文要約
1. Li₃YbCl₆ および Li₃₋ₓYb₁₋ₓZrₓCl₆ 系列の Yb 系 chloride SSE を開発した。
2. Yb³⁺ を Zr⁴⁺ で異価置換することにより Li vacancy と結晶構造を同時に制御し、trigonal/orthorhombic の構造発展を観察した。
3. ハライド SSE のイオン輸送は空孔濃度だけでなく、composition–structure–migration network の関係から理解すべきであり、同時に高電圧酸化安定性も維持できることを示した。

### 開発目標との関連
異価置換と相転移によって migration network を制御する方針を支持し、Composition 2 の構造エンジニアリングの根拠となる。ただし cost、energy above hull、E<30 GPa も併せて評価する必要がある。

### DOI
[10.1021/acsmaterialslett.1c00142](https://doi.org/10.1021/acsmaterialslett.1c00142)

## 3. Wang et al., 2021 — Nature Communications

### Type
Research Article（原著論文）

### Title
A Cost-Effective and Humidity-Tolerant Chloride Solid Electrolyte for Lithium Batteries

### Material
Li₂ZrCl₆

### Keywords
Li₂ZrCl₆ · 低コスト · 耐湿性 · Zr 系 chloride · 4 V 正極 · メカノケミカル合成 · イオン伝導度 · 変形性 · 低コスト前駆体 · 耐湿安定性

### 3文要約
1. 低コストな Li₂ZrCl₆ chloride SSE を提案し、室温で約 0.81 mS cm⁻¹ の Li⁺ 伝導度を示した。
2. 高価な Y/In/Sc/rare-earth chloride と比較して原料コストを大幅に下げながら、良好な変形性と 4 V 正極適合性を維持した。
3. 相対湿度 5% の環境に曝露しても顕著な吸湿や伝導度低下が見られず、従来の多くの chloride SSE より低湿度環境への耐性が高いことを示した。

### 開発目標との関連
低コスト Zr chemistry、耐湿性、4 V 正極適合性を直接支持し、Li–Zr–Al–O–Cl の産業化ルートにとって重要な化学的先例となる。

### DOI
[10.1038/s41467-021-24697-2](https://doi.org/10.1038/s41467-021-24697-2)

## 4. Tanaka et al., 2023 — Angewandte Chemie International Edition

### Type
Research Article（原著論文）

### Title
New Oxyhalide Solid Electrolytes with High Lithium Ionic Conductivity >10 mS cm⁻¹ for All-Solid-State Batteries

### Material
LiNbOCl₄、LiTaOCl₄

### Keywords
LiNbOCl₄ · LiTaOCl₄ · オキシハライド · 混合アニオン · アニオンエンジニアリング · 超イオン伝導 · >10 mS cm⁻¹ · Li⁺ migration environment · 高レート性能 · bulk-type ASSB

### 3文要約
1. 新しい oxyhalide である LiNbOCl₄ と LiTaOCl₄ を報告し、室温伝導度はそれぞれ約 10.4 と 12.4 mS cm⁻¹ に達した。
2. ハライド骨格に O²⁻ と Cl⁻ を同時に導入し、mixed-anion / anion engineering によって Li⁺ の migration environment を再構築した。
3. ハライド/オキシハライド SSE の伝導度を 10⁻² S cm⁻¹ 級へ押し上げ、bulk-type ASSB で優れた高レート性能を示した。

### 開発目標との関連
mixed-anion と新構造によって `10 mS cm⁻¹` の壁を越えられる可能性を直接示す。今後はコスト、合成可能性、弾性率、正極との反応エネルギーを追加評価する必要がある。

### DOI
[10.1002/anie.202217581](https://doi.org/10.1002/anie.202217581)

## 5. Yin et al., 2023 — Nature

### Type
Research Article（原著論文）

### Title
A LaCl₃-Based Lithium Superionic Conductor Compatible with Lithium Metal

### Material
Ta ドープ LaCl₃

### Keywords
LaCl₃ · Ta ドーピング · La 空孔 · UCl₃-type framework · 1D-to-3D migration · Li 金属適合性 · 不動態化界面 · gradient interphase · 活性化エネルギー · rare-earth chloride

### 3文要約
1. UCl₃-type LaCl₃ framework の広い 1D Li⁺ channels を利用し、新しい rare-earth chloride SSE を開発した。
2. Ta⁵⁺ doping により La vacancies を導入して一次元 Li⁺ channels を三次元 migration network へ接続し、30 °C で 3.02 mS cm⁻¹、Eₐ = 0.197 eV を達成した。
3. Li metal との接触時に自己制限的な gradient passivation interphase が形成され、高速 Li⁺ 輸送と優れた Li-metal compatibility を両立した。

### 開発目標との関連
P6₃/m-related high-conductivity framework と Li-metal 界面設計の根拠となる。一方、Ta/La の資源・コスト問題から、最終産業化組成より transport benchmark として有用である。

### DOI
[10.1038/s41586-023-05899-8](https://doi.org/10.1038/s41586-023-05899-8)

## 6. Hu et al., 2023 — Nature Communications

### Type
Research Article（原著論文）

### Title
A Cost-Effective, Ionically Conductive and Compressible Oxychloride Solid-State Electrolyte for Stable All-Solid-State Lithium-Based Batteries

### Material
Li₁.₇₅ZrCl₄.₇₅O₀.₅

### Keywords
Li₁.₇₅ZrCl₄.₇₅O₀.₅ · オキシクロライド · 混合アニオン · 圧縮性 · 相対密度 · 低コスト · イオン伝導度 · NMC811 · 長期サイクル · 実用 ASSB

### 3文要約
1. Li₁.₇₅ZrCl₄.₇₅O₀.₅ oxychloride SSE を開発し、室温で 2.42 mS cm⁻¹ のイオン伝導度を実現した。
2. 300 MPa で 94.2% の相対密度に達し、原料コストも約 $11.60 kg⁻¹ と見積もられ、伝導度・圧縮性・コストを総合的に最適化した。
3. NMC811-based positive electrode と組み合わせた全固体電池で 2000 サイクル超を実現し、実用 SSE は最高 bulk conductivity だけで評価すべきでないことを示した。

### 開発目標との関連
rare-element-free Li–Zr–Al–O–Cl の強い baseline であり、mS cm⁻¹ 級伝導、圧密性、低コスト、長期サイクルを同時に示す。ただし σ を約 2.42 mS cm⁻¹ から >10 mS cm⁻¹ へ高める必要がある。

### DOI
[10.1038/s41467-023-39522-1](https://doi.org/10.1038/s41467-023-39522-1)

## 7. Li et al., 2024 — Nature Communications

### Type
Research Article（原著論文）

### Title
Structural Regulation of Halide Superionic Conductors for All-Solid-State Lithium Batteries

### Material
構造タイプ：hcp-T、hcp-O、ccp-M

### Keywords
Cationic polarization factor · τ · hcp-T · hcp-O · ccp-M · stacking structure · 構造予測 · composition–structure 関係 · Li-ion transport · 材料スクリーニング · descriptor-guided discovery

### 3文要約
1. chemical composition から lithium halide SSE の stacking structure を予測するため、cationic polarization factor τ を提案した。
2. 代表的な構造を hcp-T、hcp-O、ccp-M に分類し、composition → structure → Li-ion transport の関係を構築した。
3. この descriptor を候補材料のスクリーニングと実験設計に適用し、ハライド開発を trial-and-error から descriptor-guided materials discovery へ発展させた。

### 開発目標との関連
composition → structure → Li transport の計算スクリーニングを支える。許容元素空間の中で P6₃/m、C2/m、Pnma などの高伝導構造族を優先探索するために利用できる。

### DOI
[10.1038/s41467-023-43886-9](https://doi.org/10.1038/s41467-023-43886-9)

## 8. Hu et al., 2026 — Nature Communications

### Type
Research Article（原著論文）

### Title
Mechanically Compliant and Cost-Effective 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ Solid Electrolyte for All-Solid-State Batteries with Improved Cycling Stability

### Material
1.4Li₂O–0.75ZrCl₄–0.25AlCl₃

### Keywords
機械的コンプライアンス · Li-Zr-Al-O-Cl · ヤング率 · 硬さ · 高負荷正極 · 化学機械的安定性 · イオン伝導度 · 変形性 · 界面安定性 · 低コスト · mechanical mismatch

### 3文要約
1. 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ 固体電解質を開発し、25 °C で約 2.55 mS cm⁻¹ のイオン伝導度を示した。
2. Hardness 約 0.22 GPa、Young’s modulus 約 1.41 GPa という非常に高い mechanical compliance により、電解質が電極のサイクル中の変形に追従しやすい。
3. 固体電解質設計の重点を単一の伝導度から、Li-ion transport + mechanics + interface + cost の多目的最適化へ広げた。

### 開発目標との関連
Composition 3 の直接的な baseline である。非常に低い Young’s modulus（約 1.41 GPa）と低コストは魅力的だが、構造・欠陥設計により伝導度を 2–2.5 mS cm⁻¹ から >10 mS cm⁻¹ へ向上させる必要がある。

### DOI
[10.1038/s41467-025-68210-5](https://doi.org/10.1038/s41467-025-68210-5)

## 9. Li & Du, 2025 — ACS Nano（Review）

### Type
Review（総説）

### Title
Building a Better All-Solid-State Lithium-Ion Battery with Halide Solid-State Electrolyte

### Material
F/Cl/Br/I-based halide SSE（レビュー）

### Keywords
ハライド SSE · Review · F/Cl/Br/I chemistry · イオン伝導度 · 活性化エネルギー · 電子伝導度 · 電気化学的安定窓 · 界面接触安定性 · 合成 · 構造–物性相関 · 実用 ASSB 指標

### 3文要約
1. F/Cl/Br/I-based halide SSE の組成、構造、合成、全固体電池への応用を体系的にまとめた。
2. ionic conductivity と activation energy だけでなく、electronic conductivity、electrochemical stability window、interfacial contact stability など実用上の指標も重点的に議論した。
3. composition/structure → Li transport → stability/interface → practical ASSB performance という、ハライド SSE を総合評価する設計枠組みを提示した。

### 開発目標との関連
σ、E、energy above hull、酸化電位、正極反応エネルギー、熱安定性、コスト、界面を同時に扱う必要があることを示す、今回の開発フロー全体の評価フレームワークである。

### DOI
[10.1021/acsnano.4c15005](https://doi.org/10.1021/acsnano.4c15005)

## キーワードマップ

| 年 | 中核材料・テーマ | 最重要 Keyword | DOI |
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

## 詳細比較表

> 「—」は、今回のノートで統一的な数値を記録していない項目を示す。原論文を確認した後に追記できる。

| # | 年 | 種類 | 電解質・テーマ | 室温 Li⁺ 伝導度 | 構造・輸送メカニズム | 高電圧・界面安定性 | 力学・湿度・コスト | 電池・応用実証 | 核心的貢献 | DOI |
|---:|---:|---|---|---:|---|---|---|---|---|---|
| 1 | 2018 | Research Article | Li₃YCl₆ / Li₃YBr₆ | >1 mS cm⁻¹ | 高 Li⁺ 伝導；変形性；低 grain-boundary resistance | 酸化安定；4 V 正極適合 | 冷間加圧；— | 4 V class bulk-type ASSB | chloride SSE 研究の基盤を形成 | [リンク](https://doi.org/10.1002/adma.201803075) |
| 2 | 2021 | Research Article | Li₃YbCl₆；Li₃₋ₓYb₁₋ₓZrₓCl₆ | — | Zr⁴⁺/Yb³⁺ 異価置換；Li vacancy；trigonal→orthorhombic | 高電圧酸化安定性 | 混合金属組成；— | 高電圧 ASSB 候補 | composition–structure–migration network の視点を提示 | [リンク](https://doi.org/10.1021/acsmaterialslett.1c00142) |
| 3 | 2021 | Research Article | Li₂ZrCl₆ | 約0.81 mS cm⁻¹ | Zr 系 chloride；メカノケミカル合成 | 4 V 正極適合；5% RH 後も明確な低下なし | 低コスト；変形性；耐湿性 | Li battery / 4 V cathode | Zr による低コスト化と耐湿性を実証 | [リンク](https://doi.org/10.1038/s41467-021-24697-2) |
| 4 | 2023 | Research Article | LiNbOCl₄ / LiTaOCl₄ | 約10.4 / 12.4 mS cm⁻¹ | O²⁻/Cl⁻ mixed-anion；anion engineering | mixed-anion による Li⁺ migration environment 再構築 | — | bulk-type ASSB；高レート性能 | oxyhalide の伝導度を 10⁻² S cm⁻¹ 級へ向上 | [リンク](https://doi.org/10.1002/anie.202217581) |
| 5 | 2023 | Research Article | Ta-doped LaCl₃ | 30 °C で 3.02 mS cm⁻¹；Eₐ=0.197 eV | La vacancy；1D→3D migration network | Li metal 接触で gradient passivation interphase | — | Li-metal-compatible SSE | 高速伝導と Li-metal compatibility を両立 | [リンク](https://doi.org/10.1038/s41586-023-05899-8) |
| 6 | 2023 | Research Article | Li₁.₇₅ZrCl₄.₇₅O₀.₅ | 2.42 mS cm⁻¹ | oxychloride；mixed-anion | NMC811 界面と長期サイクル安定性 | 300 MPa で相対密度 94.2%；約 $11.60 kg⁻¹ | NMC811；>2000 cycles | 伝導度・圧縮性・コストを総合最適化 | [リンク](https://doi.org/10.1038/s41467-023-39522-1) |
| 7 | 2024 | Research Article | Structural regulation；hcp-T/O、ccp-M | — | Cationic polarization factor τ；stacking structure descriptor | 構造スクリーニングで安定材料探索を支援 | — | 候補材料の選別と実験設計 | trial-and-error を descriptor-guided discovery へ転換 | [リンク](https://doi.org/10.1038/s41467-023-43886-9) |
| 8 | 2026 | Research Article | 1.4Li₂O–0.75ZrCl₄–0.25AlCl₃ | 25 °C で約2.55 mS cm⁻¹ | Li-Zr-Al-O-Cl；chemo-mechanical design | 界面とサイクル変形に対する安定性 | Hardness≈0.22 GPa；E≈1.41 GPa；低コスト | high-loading cathode；サイクル安定性向上 | mechanics を SSE の多目的設計へ導入 | [リンク](https://doi.org/10.1038/s41467-025-68210-5) |
| 9 | 2025 | **Review** | F/Cl/Br/I-based halide SSE | 総説として比較 | composition/structure→transport | electrochemical window；electronic conductivity；interfacial contact stability | synthesis、activation energy、実用指標 | practical ASSB 評価枠組み | 材料からデバイスまでの総合設計指針 | [リンク](https://doi.org/10.1021/acsnano.4c15005) |

## テーマ別インデックス

| テーマ | 対応論文 | 追跡すべき問い |
|---|---|---|
| 高電圧適合性 | 1、2、3、4 | 4 V 正極下で低い界面抵抗と耐酸化性をどう維持するか？ |
| 構造・空孔エンジニアリング | 2、5、7 | 空孔濃度、積層、migration network はどのように協調するか？ |
| Oxyhalide / mixed-anion | 4、6、8 | O²⁻/Cl⁻ 混合アニオンは輸送と力学特性にどう影響するか？ |
| Li-metal 界面 | 5、9 | 安定で薄く自己制限的な passivation interphase をどう形成するか？ |
| コストと製造性 | 3、6、8、9 | 原料費、圧密密度、プロセス窓、量産性をどう両立するか？ |
| 力学とサイクル寿命 | 1、3、6、8、9 | 機械的コンプライアンスを高負荷・長寿命性能へどう変換するか？ |
