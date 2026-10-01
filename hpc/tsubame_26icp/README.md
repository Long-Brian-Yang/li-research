# TSUBAME 計算環境

このディレクトリには、TSUBAME 用 path configuration、engine build recipe、短時間 benchmark、model input、production MD、事前検査を置く。ローカル PC 向けの portable installation package ではない。

| directory | 内容 |
|---|---|
| `config/` | canonical path variables（`yang_paths.sh`） |
| `build/` | engine 別の build／compile |
| `benchmark/` | model/backend の短時間比較 |
| `inputs/` | LAMMPS template、MACE checkpoint 変換 |
| `production/` | 材料別 MD job と入力 |
| `validation/` | project path、package、GPU preflight |

詳細な MACE stack、job 前確認、build・移行時の注意は[日本語 MACE／TSUBAME／会社移行ガイド](../../docs/engineering/mace_tsubame_company_migration_ja.md)、全ディレクトリ・code catalog は[技術ガイド](../../docs/engineering/repository_technical_guide_ja.md)を参照する。

## 実行前の安全確認

job を準備する前に、checkout、権限、path、model/structure checksum、組成、time step、温度、ensemble、出力容量、scheduler resource を確認する。GPU test や production 計算は login node で直接実行せず、TSUBAME の現行 scheduler と resource policy を守る。

`validation/validate_project.sh` は TSUBAME 側の path/import 確認であり、科学的妥当性を保証しない。job の終了 status だけで structure・potential・transport の検証を完了したとみなさない。root level に残る古い script には移行前の個人 path があるため、現行 subdirectory の recipe を優先する。
