# 派生解析結果

この directory には CSV／JSON、source data extract、checksum/manifest、レポート図、日付付き解析記録など、確認可能なサイズの成果を保存する。現在の科学的説明は[日本語](../docs/materials/materials_overview_ja.md)／[英語](../docs/materials/materials_overview_en.md)Material Review を参照する。

| directory | 内容 |
|---|---|
| `publication_all_materials/` | 結晶 benchmark の図・source data・supplement |
| `midterm_Li3YCl6_MACE_M3GNet/` | 中間発表 benchmark snapshot |
| `amorphous_review_20260915/` | LZOC、LSZC、Li₃PS₄、LiPON の日付付き分析・比較 |
| `amorphous_validation_20260914/` | 旧非晶質作製／検証記録 |
| `LZOC/` | LZOC MACE–NEP と旧比較 |
| `gpumd_nep89/` | GPUMD／NEP89 の解析と歴史的 300 K benchmark |

日付付きフォルダは特定時点の研究記録であり、更新された主報告と混同しない。利用前に各 README、解析 method、source hash を確認する。

## 保存境界

- CSV／JSON、図の元データ、manifest、provenance を追跡可能な状態で管理する。
- 数百 MB の raw trajectory、restart、scheduler log、compiled model、checkpoint は承認済み TSUBAME／archive に置く。
- `.gitignore` は `runs/`、model file、restart/dump 等の一部を除外する。
- `materials/evidence/` の均等抽出 frame は閲覧・構造確認用であり、定量解析は manifest が示す完全 trajectory を使う。

[技術ガイド](../docs/engineering/repository_technical_guide_ja.md#7-データ再現性報告)では入力→解析→報告の経路と再現性の限界を説明する。
