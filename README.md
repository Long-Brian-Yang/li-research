# Li Research — リチウム固体電解質の MLIP 分子動力学

本リポジトリは、結晶・非晶質 Li イオン固体電解質を対象とする機械学習原子間ポテンシャル（MLIP）の benchmark、分子動力学（MD）、構造・輸送解析、文献比較のコードと資料を管理する。構造・計算入力・コードから、MSD／拡散係数／Arrhenius／RDF／配位分析、発表図と証拠資料までを追跡する。

## はじめに

- **材料ごとの科学的結果・文献比較：** [日本語 Material Review](docs/materials/materials_overview_ja.md) · [英語 Material Review](docs/materials/materials_overview_en.md)
- **環境・デプロイ・コード・解析フローの全体像：** [リポジトリ技術ガイド（日本語）](docs/engineering/repository_technical_guide_ja.md)
- **MACE／TSUBAME／会社環境への移行：** [運用・移行ガイド（日本語）](docs/engineering/mace_tsubame_company_migration_ja.md)
- **DFT 学習データと MACE fine-tuning：** [提案 workflow（日本語）](docs/engineering/dft_and_finetuning_ja.md)
- **文書目録：** [docs/README.md](docs/README.md)
- **構造・材料候補：** [structures](structures/README.md) · [materials](materials/README.md)
- **再利用 Python コード・研究 script：** [src](src/README.md) · [scripts](scripts/README.md)
- **TSUBAME build／benchmark／計算入力：** [HPC ガイド](hpc/tsubame_26icp/README.md)
- **派生データとレポート：** [results](results/README.md)

## リポジトリ構成

| パス | 責務 |
|---|---|
| `src/li_research/` | 再利用できる構造生成、形式変換、MSD／拡散、RDF、作図 helper |
| `scripts/structures/` | 材料ごとの構造準備、解析、図・evidence 作成 |
| `hpc/` | TSUBAME 環境、engine build、benchmark、入力、production job |
| `simulation/` | engine／model 別 LAMMPS 入力 |
| `structures/` | 参照 CIF と計算用結晶構造 |
| `materials/candidates/` | 非晶質候補の作製履歴・provenance |
| `materials/evidence/` | レポートを裏付ける命名済み構造と抽出 frame |
| `results/` | 解析表、図、manifest、日付付き履歴 |
| `docs/materials/` | Material Review と本文図 |
| `tests/` | 数値、構造、データ契約、図、文書の検査 |

## エンドツーエンド workflow

```text
文献・実験値
    ↓
結晶構造／作製した非晶質候補
    ↓ 組成・幾何・出典を検証
engine と potential の事前確認・構造緩和
    ↓
対象温度・ensemble の MD
    ↓
全 trajectory に共通の MSD／D／Arrhenius／RDF 等の解析
    ↓
同じ物理量・定義・単位で文献／実験と比較
    ↓
表・図・source manifest → Material Review
```

## 再現性とデータ境界

repo には単一の Python lock file がなく、TSUBAME 環境、build 済み engine、ML model weight、完全な production trajectory は通常 Git 外で管理する。HPC 設定は個人/group の絶対パスを含むため、実行前に必ず確認する。大容量の raw trajectory は管理者承認済みの cluster/storage に保存し、Git には解析 code、妥当な入力、軽量な派生データ、hash と図 manifest を登録する。

複数 trajectory がある解析では、文献値との一致や数値の良否で trajectory／replica を事後選別しない。全反復を共通規約で処理し、完了 marker と物理的な妥当性を区別する。TSUBAME 向け [`validate_project.sh`](hpc/tsubame_26icp/validation/validate_project.sh) は cluster-side preflight であり、local test や科学的 validation の代替ではない。

現在の材料状況は日英 Material Review を参照する。日付付き報告や旧解析スナップショットは履歴資料であり、現在の queue 状態とは限らない。
