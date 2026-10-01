# 研究 workflow scripts

`scripts/structures/` は材料固有の構造作製、後処理、図生成、evidence package 作成、TSUBAME job wrapper を含む。`src/li_research/` の再利用 helper と `hpc/` の build/job input とは役割が異なる。

| file 名の先頭 | 主な役割 |
|---|---|
| `build_`、`prepare_`、`pack_`、`extract_` | 候補構造、組成、配列、cluster、文献 source data の作成・変換 |
| `analyze_`、`finish_`、`complete_`、`summarize_` | MSD／拡散／Arrhenius、局所構造、全反復診断、表作成 |
| `check_`、`compare_`、`validate_`、`review_` | 構造・provenance の検査、定義済み比較 |
| `plot_`、`curate_`、`li_diffusion_style.py` | 図、文献比較、共通スタイル、figure manifest |
| `submit_*.sh` | TSUBAME SGE wrapper。遠隔計算を起動する場合がある |

全 file の入口・入力/出力・実行環境は[日本語技術ガイド](../docs/engineering/repository_technical_guide_ja.md#5-コアコードと分析コード)に整理した。

## 実行前に読むこと

材料パスが script 内に定義される場合がある。同じ directory の別 module を import する場合もあるため、実行前に全文・入力データ・provenance・出力先を確認する。`submit_*.sh` は単なる解析ではなく外部計算を開始し得る。報告図は `docs/materials/figures/`、完全な raw trajectory は既定の TSUBAME／ローカル archive に保存する。

解析で複数の独立 trajectory がある場合、文献値への近さで1本だけ選ばず、すべてを同じ解析規約に適用する。
