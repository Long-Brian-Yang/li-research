# Li–Zr–Al–O–Cl 固体電解質の具体的な開発計画

## 研究テーマ

> **Li–Zr–Al–O–Cl 低コスト系において、構造・アニオンエンジニアリングにより σ<sub>Li</sub> >10 mS cm⁻¹、E <30 GPa を満たす新規固体電解質を探索する。**

最初から数十種類の元素へ拡張せず、Composition 3 を基準にした小規模で解釈可能なスクリーニングから始める。

## 1. 基準材料を固定する

Baseline として次の組成を用いる。

\[
1.4\mathrm{Li_2O}-0.75\mathrm{ZrCl_4}-0.25\mathrm{AlCl_3}
\]

現在の基準値：

- σ<sub>Li</sub> ≈ 2–2.5 mS cm⁻¹
- Young’s modulus ≈ 1.41 GPa
- 低コスト
- rare-element-free

これを「性能が不十分な材料」ではなく、低コスト・機械的コンプライアンスをすでに持つ、伝導度最適化のための baseline と位置づける。

## 2. 第1ラウンドで変える変数は3つに限定する

| 変数 | 推奨範囲 | 目的 |
|---|---|---|
| Al/Zr 比 | Al-poor、baseline、Al-rich | Li vacancy と格子の柔軟性を制御 |
| O/Cl 比 | O-poor、baseline、O-rich | mixed-anion migration environment を制御 |
| Zr の少量 Nb 置換 | 0、5、10 at% | 構造分極と連続的な Li⁺ migration channel を導入 |

Nb は少量ドーパントとしてのみ検討する。Ta/Nb を主成分にすると低コスト方針が弱くなるため、主相を Nb/Ta 系へ移行させない。

## 3. 構造スクリーニング

各組成について、次の構造候補を検討する。

- P6₃/m
- C2/m
- Pnma
- hcp-T / hcp-O / ccp-M 関連構造

優先する候補は、次の3条件を同時に満たすものとする。

\[
\text{低い }E_{\mathrm{hull}}
+
\text{連続的な Li migration network}
+
\text{低い Young’s modulus}
\]

構造候補は単に空間群で選ぶのではなく、Li サイトの連結性、空孔濃度、ボトルネック、アニオン配列も確認する。

## 4. 実際のスクリーニング順序

長時間 MD を全候補へ最初から適用せず、以下の段階で絞り込む。

1. `Energy above hull <50 meV atom⁻¹` を第1の hard gate とする。
2. 構造緩和と力学的安定性を確認する。
3. 300–500 K の短時間 AIMD で Li の移動開始を初期スクリーニングする。
4. Li の MSD、D<sub>Li</sub>、σ<sub>Li</sub> を計算する。
5. σ<sub>Li</sub> が高い候補について完全な弾性テンソル C<sub>ij</sub> と Young’s modulus を計算する。
6. 最後に V<sub>ox</sub>、正極との反応エネルギー、熱安定性を評価する。

伝導度は、可能であれば Nernst–Einstein 推定だけでなく、相関係数を含む Green–Kubo または Haven ratio による補正も記録する。

## 5. 第1版のランキング重み

| 指標 | 重み |
|---|---:|
| σ<sub>Li</sub> | 40% |
| Young’s modulus | 25% |
| Energy above hull | 20% |
| 酸化安定性 / 正極安定性 | 10% |
| コスト・入手性 | 5% |

ただし、重み付き合計点だけで候補を決めない。以下を hard gate とする。

\[
E_{\mathrm{hull}}<50\ \mathrm{meV\ atom^{-1}}
\]

\[
E<30\ \mathrm{GPa}
\]

最終的な伝導度目標は次の通り。

\[
\sigma_{\mathrm{Li}}>10\ \mathrm{mS\ cm^{-1}}
\]

## 6. Go / No-Go 判断

- Li–Zr–Al–O–Cl の全候補が 5 mS cm⁻¹ 未満の場合：5–10% Nb 置換を導入する。
- 5–8 mS cm⁻¹ に到達する場合：O/Cl 比と構造タイプを優先的に最適化する。
- 10 mS cm⁻¹ に近づく場合：正極安定性、150 °C 安定性、合成可能性の実験検証へ進む。
- 大量の Nb/La/Ta を入れないと 10 mS cm⁻¹ に到達できない場合：低コスト方針から外れるため、高価な元素の拡張を停止する。

## 7. 最終的な研究方針

> **Li–Zr–Al–O–Cl を化学的境界とし、P6₃/m・C2/m・Pnma を構造探索空間とする。σ<sub>Li</sub> >10 mS cm⁻¹ を中心目標に置き、E <30 GPa と合成可能性を hard constraint とする。**

この方針では、方向 2（高伝導構造）を科学的な主線、方向 3（低コスト化学空間）を元素制約、方向 1（機械的コンプライアンス）を性能制約として扱う。

## 8. 実験値との比較に使う基準

計算スクリーニングの結果は、以下の文献実験値と同じ表で比較する。ただし、計算値・目標値・実験値を混同しない。

| 参考 | 実験的ベンチマーク |
|---|---|
| Asano et al., 2018 | Li₃YCl₆ / Li₃YBr₆：室温 >1 mS cm⁻¹；4 V 正極適合 |
| Wang et al., 2021 | Li₂ZrCl₆：約0.81 mS cm⁻¹；5% RH 後も明確な劣化なし |
| Tanaka et al., 2023 | LiNbOCl₄：約10.4 mS cm⁻¹；LiTaOCl₄：約12.4 mS cm⁻¹ |
| Hu et al., 2023 | Li₁.₇₅ZrCl₄.₇₅O₀.₅：2.42 mS cm⁻¹；94.2% 相対密度；>2000 cycles |
| Hu et al., 2026 | Li–Zr–Al–O–Cl：約2.55 mS cm⁻¹ @25 °C；Young’s modulus 約1.41 GPa |

候補材料の各数値には、必ず `Experimental`、`Calculated`、`Target` のいずれか、温度、測定/計算手法、出典を付記する。

