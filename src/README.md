# 再利用 Python モジュール

`src/li_research/` は、結晶構造生成、形式変換、LAMMPS／GPUMD の解析・作図に使う再利用 module を含む。

```text
li_research/
├── structures/   結晶構造生成と supercell utility
├── conversion/   CIF／LAMMPS／extended-XYZ 変換、占有確認
└── analysis/
    ├── lammps/   Li MSD／拡散、hop 統計、model 図
    ├── gpumd/    GPUMDkit 入力準備と GPUMD 後処理
    ├── rdf/      trajectory から RDF 再計算
    └── arrhenius/結晶 benchmark の Arrhenius 図
```

全コード索引と環境条件は[日本語技術ガイド](../docs/engineering/repository_technical_guide_ja.md#5-コアコードと分析コード)を参照する。

## 実行上の注意

この repo には `pyproject.toml`、`setup.py`、完全固定された依存 file がない。ASE、NumPy、SciPy、Matplotlib 等の要件は module ごとに異なる。repository root から `PYTHONPATH=src` を設定して使う場合も、入力パスと依存を確認する。材料固有の分析は `scripts/structures/` にある。

LAMMPS／GPUMD の job script、model weight、raw trajectory、計算結果はこの再利用 module tree に置かず、それぞれ `hpc/`、承認済み model/runtime storage、`results/` を使う。
