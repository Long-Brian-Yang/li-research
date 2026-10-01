# 文書目録

## 現行の主資料

| 資料 | 用途 |
|---|---|
| [日本語 Material Review](materials/materials_overview_ja.md) | 材料別背景、文献値、計算条件、結果、図、定義、解釈を統合した主報告 |
| [English Material Review](materials/materials_overview_en.md) | 日本語主報告の英語版 |
| [リポジトリ技術ガイド](engineering/repository_technical_guide_ja.md) | ディレクトリ、環境、TSUBAME、deploy、core code、分析 code、data provenance、tests |
| [MACE／TSUBAME／会社移行ガイド](engineering/mace_tsubame_company_migration_ja.md) | MACE runtime、TSUBAME 上の build/preflight、会社 HPC へ移行する際の確認項目 |
| [DFT・fine-tuning workflow](engineering/dft_and_finetuning_ja.md) | DFT label の作成・分割・品質検査、MACE fine-tune と物理検証の提案 |

## 開発・文献・発表

- [開発・benchmark](development/README.md)：計算 protocol、性能測定、研究計画。
- [LZOC 文献読解](literature/lzoc_top3/README.md)：原著論文、DOI、日英読解メモ。
- [LZOC 構造・計算準備](materials/LZOC/README.md)：候補構造、調製過程、関連 input。
- [中間発表資料](../results/midterm_Li3YCl6_MACE_M3GNet/)：結晶 benchmark の図と記録。
- [総合発表成果](../results/publication_all_materials/)：発表用図・数値・supplement。
- [日報一覧](daily_reports/README.md)：時点付きの作業記録。現状の決定版資料ではない。

## 更新方針

- 科学的な説明と最終図は日英 Material Review の該当節を直接更新する。
- HPC・依存関係・deploy・再利用 code の説明は日本語技術ガイドと隣接 README を更新する。
- DFT/fine-tuning は会社内の license、data governance、計算環境が決定するまで、提案手順として記述する。
- 履歴資料はその時点の記録として保持する。古い値を current analysis として再利用せず、新旧の状態を明確にする。
- 複数の独立 trajectory がある場合、どれか一つを文献値に合わせて選ぶ解析を設けず、全件を同一規約で扱う。
