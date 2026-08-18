# 候補固体電解質の開発マトリクス（日本語）

本ファイルは、文献の結論を候補材料の実行可能な評価表へ変換したものである。数値は現在のプロジェクトノートから整理した暫定値であり、`—` は原論文または計算出力から補う必要がある項目を示す。

## 1. 統一評価指標

| 指標 | 目標 | 暫定スコア（0–3） | データ源・方法 |
|---|---:|---|---|
| Li⁺ 伝導度 σ<sub>Li</sub> | >10 mS cm⁻¹ | 0: <1；1: 1–3；2: 3–10；3: >10 | MD：MSD、D<sub>Li</sub>、Nernst–Einstein または Green–Kubo；実験 EIS |
| Young’s modulus E | <30 GPa | 0: >60；1: 30–60；2: 10–30；3: <10 | DFT elastic tensor C<sub>ij</sub>；ナノインデンテーション/超音波 |
| Energy above hull | 低いほどよい | 0: >100 meV atom⁻¹；1: 50–100；2: 20–50；3: <20 | Materials Project/DFT phase diagram；計算条件を明記 |
| 低コスト・入手性 | rare-element-free 優先 | 0: Ta/Gd/La/In 主体；1: 希少元素が多い；2: 微量添加；3: Li–Zr–Al–O–Cl 主体 | 元素、価格、サプライチェーン調査 |
| 耐酸化性 V<sub>ox</sub> | >5 V vs. Li | 0: <4；1: 4–4.5；2: 4.5–5；3: >5 | 分解反応エネルギー/電気化学窓；熱力学と速度論を区別 |
| 正極との化学安定性 | 明確な副反応なし | 0: 強反応；1: 高い反応エネルギー；2: 許容可能な界面；3: 明確な反応なし | NMC811 などとの ΔE<sub>reaction</sub> |
| 耐熱性 | 150 °C で劣化なし | 0: 明確な分解；1: 部分劣化；2: ほぼ安定；3: 実験でも安定 | 熱分解/速度論、DSC/TGA、150 °C 保持試験 |
| 合成・成形性 | 再現可能な実験経路 | 0: 既知経路なし；1: 極端条件；2: 実験室で調製可；3: 簡便・スケール可能 | Energy above hull、合成経路、相純度、圧密密度 |

総合点は hard gate の代わりではない。まず energy above hull が高すぎる候補や合成不能な候補を除外し、その後 σ、E、コストを重み付けして順位付けする。

## 2. 現在の候補スコア（暫定）

| 候補 | σ | E | 合成可能性 | コスト/元素 | V<sub>ox</sub> | 正極安定性 | 熱安定性 | 合成/成形 | 総合判断 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Composition 1：Li–Zr–Ta–Gd–Cl–O | 1 | 2–3 | — | 0 | 1 | — | — | — | 力学 benchmark；コストと耐酸化性が制約 |
| Composition 2：Li–La–Zr–Ta–Cl–O–Br | 2 | — | — | 0–1 | — | — | — | — | transport/framework benchmark；希少元素を減らし σ を倍増する必要 |
| Composition 3：Li–Zr–Al–Cl–O | 1 | 3 | — | 3 | — | — | — | 2 | 産業化に有望な baseline；核心課題は σ 向上 |

このスコアは現在の要約情報に基づく暫定値であり、最終的な材料ランキングではない。原データを補完後に重みと順位を確定する。

## 3. 論文から候補設計への対応

| 設計課題 | 主要論文 | 継承できる設計原理 | 追加すべき検証 |
|---|---|---|---|
| >10 mS cm⁻¹ を達成する | Tanaka 2023；Asano 2018 | mixed-anion、開放 Li⁺ ネットワーク、高電圧適合 | MD 条件、実験 EIS、Eₐ、bulk/GB 寄与 |
| E<30 GPa にする | Hu 2026；Hu 2023 | oxychloride、機械的コンプライアンス、圧密性 | 完全な C<sub>ij</sub>、異方性、ナノインデンテーション条件 |
| コストを下げる | Wang 2021；Hu 2023/2026 | Zr–Al–O–Cl、Ta/Gd/La/In 主体を避ける | 原料価格、収率、スケールアップ工程 |
| 3D migration network を作る | Yin 2023；Kim 2021；Li 2024 | 空孔、相転移、stacking descriptor | P6₃/m/C2/m/Pnma の安定性・合成可能性 |
| 正極との適合性を確保する | Asano 2018；Li & Du 2025 | V<sub>ox</sub> と ΔE<sub>reaction</sub> を分けて評価 | NMC811 反応エネルギー、界面相、サイクル後抵抗 |

## 4. 統一データ入力テンプレート

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

## 5. 現時点での最優先課題

Composition 3 の Li–Zr–Al–O–Cl 低コスト化学空間を維持しつつ、P6₃/m など高伝導構造の特徴を取り込める候補を優先する。energy above hull を第一の hard gate とし、その後 MD の σ と DFT の E による二目的スクリーニングを行う。

## 6. プロジェクト図の配置

3 枚の開発方針図を `figures/` に追加した後、以下のパスで固定参照できる。

- `figures/development-goals.png`：開発目標と優先度
- `figures/candidate-compositions.png`：3つの候補組成の比較
- `figures/element-screening-rules.png`：元素、毒性、コスト、入手性のルール
