# DFT 学習データ作成と MACE fine-tuning の提案手順

## 1. 現状と目的

この文書は、汎用 MACE foundation model を材料専用 MLIP へ拡張するときの再現可能な手順案である。現時点で、このリポジトリに完成した DFT ラベル生成 workflow、会社用 DFT software license、fine-tuned model、検証済み学習設定が揃っているという意味ではない。会社の機密データを扱う場合は、承認された計算機・コード・保存先が確定してから進める。

目的は「指定された実験値に合う trajectory を選ぶ」ことではない。DFT に基づく固定データ分割と前もって決めた物理検証で、対象材料群に対してモデルが再現可能かを判定し、その結果を候補材料の優先順位づけに使うことである。

## 2. 全体 workflow

```text
対象組成・構造・物性要件を決める
        ↓
汎用 MACE による構造緩和／短い MD／探索構造生成
        ↓
構造・温度・組成・局所環境を多様に含む DFT snapshot を設計
        ↓
承認済み DFT engine で energy / force / 必要に応じ stress を計算
        ↓
重複・収束・単位・元素・力・stress の品質検査
        ↓
構造単位で train / validation / held-out test 分割
        ↓
foundation MACE baseline と fine-tuned model を比較
        ↓
energy / force / stress error と構造・MD・輸送の検証
        ↓
合格した version を固定し、候補材料の同条件 screening へ
        ↖──────── DFT 追加学習データへの feedback ────────↙
```

### Gate A：対象範囲と教師モデル

最初に対象元素、組成範囲、酸化状態、温度・圧力、欠陥／界面を定義する。教師データの範囲外までモデルが妥当だと仮定しない。DFT functional、擬ポテンシャル、spin、U、dispersion、smearing、cutoff、k-point、SCF/ionic convergence を固定する。すべてのラベルは同じ計算水準で取得し、異なる設定を混在させる場合はデータセットの別 domain として管理し、エネルギーの基準差を補正する。

### Gate B：構造集合の設計

データ候補には次の局所環境・状態を明示的に含める。

- 初期結晶構造と軽い摂動、格子・原子位置の relaxation 周辺。
- 融解／急冷／緩和を含む非晶質構造と複数の独立な作製系列。
- 対象温度範囲から等間隔に取る平衡スナップショット。
- Li の異なる配位、移動途中、欠陥近傍、低頻度だが現実的な局所構造。
- 事前定義した stress/force 異常や ensemble disagreement で検出された構造。ただし「文献に近い拡散値」を選別基準にしない。
- 組成探索を行うなら組成端点と中間組成を区別して保持する。

全時刻フレームを独立サンプルとして扱うと、同一 trajectory の隣接frameが train と test に跨り、誤差を過小評価する。分割単位は parent structure、独立した作製系列、trajectory、組成とする。固定 random seed と split manifest を保存し、test set はモデル選択に使わない。

## 3. DFT 計算の実務設定

### 3.1 engine 選択

会社が利用権を持つ DFT package と計算資源を選ぶ。Quantum ESPRESSO は公開可能な代表例だが、導入・擬ポテンシャルの種類、functional、収束基準は材料と計算資源に応じて合意する。VASP を用いる場合は、会社の組織・利用者が有効なライセンスを持つことを事前確認する。所属大学のライセンスを会社へ持ち出す前提にしない。

### 3.2 収束と均一性

採用する plane-wave cutoff、k-point density、SCF tolerance、force/energy convergence、smearing、spin、cell stress 条件は、数個の代表構造で収束試験して決める。計算ログと出力だけを残すのではなく、構造、入力 deck、pseudo potential 名と checksum、code version、MPI/GPU 設定、計算収束状態を manifest に記録する。

energy/force を学習に使う前に以下を確認する。

1. SCF が正常収束し、NaN、未完了 ionic step、警告を見落としていない。
2. 全構造の元素・原子数・周期 cell が入力と一致する。
3. total energy が eV、force が eV/Å に変換され、stress の符号・規約・単位が統一されている。
4. 原子力の最大値と最小原子間距離を検査し、異常配置を別途レビューする。
5. 重複構造、ほぼ同一の隣接frame、欠損ラベルを検出する。
6. 構造ごとの計算設定が共通か、domain として識別できる。

強い反発域を教師データに含める場合も、物理的にあり得ない原子重なりを無条件に混ぜず、MD で遭遇し得る領域と数値的異常を区別する。

### 3.3 extended XYZ への出力

MACE training guide の標準的な既定キーは energy と forces である。リポジトリに保存する extxyz には各 frame の格子・PBC と、統一した property key/units の energy、force、任意の stress を記録する。実際に用いる MACE CLI/version のキー名、stress sign と shape は公式資料および小さい parse test で確認する。例えば `energy` と `forces` という列名だけで、stress の単位が自動で一致するとは限らない。

dataset manifest に少なくとも次を含める。

| 項目 | 記録内容 |
|---|---|
| dataset ID | version、作成日、対象組成、frame 数、構造系列 ID |
| DFT provenance | code/version、functional、pseudo、cutoff、k-point、convergence |
| units/keys | energy、force、stress の extxyz key、単位、符号規約 |
| partition | train/validation/test の parent IDs と固定 seed |
| integrity | 入力・出力・pseudo の SHA-256、failed calculation list |
| governance | data owner、classification、承認 storage、共有可否 |

## 4. fine-tuning の計画

### 4.1 まず比較するモデル

同一 train/validation/test split に対し、最低限、(1) 未調整 foundation checkpoint、(2) fine-tuned checkpoint を評価する。対象 domain が狭ければ MACE 公式ガイドの通常 fine-tune を基準にする。幅広い OOD 範囲を扱い foundation model の能力を保持したいときは、replay を組み合わせる multihead 等を検討する。データが極めて少ない場合に LoRA を候補として比較できるが、どの方法も材料ごとの検証なしに優越すると仮定しない。

MACE の fine-tuning docs では、学習法、foundation model、energy baseline/E0、optimizer 等の選択が性能に影響し、replay による forgetting 抑制を説明している。機能は更新され得るため、実行時に使用する version の公式 guide と CLI `--help` を確認する。

### 4.2 学習の開始条件と記録

fine-tune 前に基準モデルを immutably archive し、checkpoint hash、MACE version、PyTorch/CUDA version、dtype、species mapping、E0 initialization、train/valid/test manifest、seed、optimizer、learning rate、batch size、loss weights、scheduler、epoch/patience を保存する。hyperparameter は validation set で決め、held-out test の誤差を見て変更しない。

この文書は example workflow であり、学習率、epoch、batch size などを材料一般の既定値として指定しない。利用する checkpoint と MACE version の fine-tuning interface に合わせ、少数の探索実験を事前設計して選定条件を記録する。

### 4.3 validation と合格判定

以下を組み合わせて判断する。

| 検証軸 | 指標例 | 注意点 |
|---|---|---|
| Held-out DFT fit | energy MAE/RMSE (meV/atom)、force MAE/RMSE (eV/Å)、stress error | parent/trajectory を分離した test のみを最終評価に使う |
| 構造・力学 | cell、密度、配位、RDF、energy drift、異常短距離接触 | 元データを作った条件に対応させる |
| MD 安定性 | 複数温度の finite trajectory、thermal stability、構造変化 | 1 seed の完走だけで安定性を主張しない |
| 輸送 | 全独立 repeat に同じ MSD fit protocol、D(T)、Arrhenius | 文献に合う repeat を選んで報告しない |
| baseline 比較 | foundation checkpoint と fine-tuned model を同一 split/条件で比較 | test data leakage を避ける |
| OOD／安全性 | 対象外組成・極端配位での外挿挙動 | 利用範囲を明記し、外側を無条件に保証しない |

受け入れ基準は計算開始前に、材料用途と会社側の評価要件に合わせて決定する。「test RMSE が下がった」だけでは十分でない。予測力、局所構造、熱力学安定性、輸送挙動の全体が改善するか確認する。悪化した特性があれば目的範囲を狭めるか、教師データを追加する。

## 5. 反復学習 loop と model release

1. baseline checkpoint を固定し、構造緩和・MD・候補条件を同一 input で実行。
2. 事前定義した uncertainty または領域不足指標で、DFT 追加対象の structure を抽出。抽出はフレームの多様性・新規性・入力範囲に基づき、目標となる拡散値への近さには基づかない。
3. DFT を実行し、入力・log・収束・label quality を確認。
4. 新データと既存 replay set を versioning し、train/validation を更新。held-out test は維持する。
5. fine-tune し、同じ test／MD protocol で baseline と比較。
6. 合格なら model card、scope、hash、software manifest とともに release。未達なら原因を分類して次の DFT batch を決定。

各リリースに checkpoint SHA-256、学習 data ID、コード commit、environment lock/container digest、適用元素・組成範囲、検証表、既知の制限、モデル license を添える。会社の機密構造から学習した checkpoint 自体も機密資産として扱う。

## 6. 実装前 checklist

- [ ] 会社が使える DFT engine、license、計算資源を確定した
- [ ] 対象元素、組成、温度、構造 domain と採用基準を定義した
- [ ] MACE checkpoint の利用・fine-tune・社内配布条件を確認した
- [ ] DFT 設定と擬ポテンシャルの provenance を固定した
- [ ] train/validation/test を構造系列単位で分離した
- [ ] extxyz の key、units、stress convention を parse test した
- [ ] baseline と fine-tune を同条件で比較する test protocol を用意した
- [ ] 全 trajectory/repeat を同じ解析に通すコードと図を用意した
- [ ] checkpoint/data/log の社内保存・アクセス権を合意した

## 7. 公式資料

- [MACE training guide](https://mace-docs.readthedocs.io/en/latest/guide/training.html)
- [MACE fine-tuning guide](https://mace-docs.readthedocs.io/en/latest/guide/finetuning.html)
- [MACE fine-tuning guidance](https://mace-docs.readthedocs.io/en/latest/guide/finetuning_guidance.html)
- [MACE installation](https://mace-docs.readthedocs.io/en/latest/guide/installation.html)
- [MACE foundation models and licenses](https://github.com/ACEsuit/mace-foundations)
- [Quantum ESPRESSO user guide](https://www.quantum-espresso.org/Doc/user_guide_PDF/pw_user_guide.pdf)
- [VASP licensing FAQ](https://www.vasp.at/info/faq/who_can_license/)
- [LAMMPS ML-IAP documentation](https://docs.lammps.org/pair_mliap.html)
