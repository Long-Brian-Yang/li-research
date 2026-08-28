# MACE + LAMMPS 環境利用ガイド

この文書は、TSUBAME 上で MACE-MPA-0 または MACE-MP-0b3 と GPU 対応 LAMMPS を使用するための外部利用者向け手順です。パスは利用者ごとに異なるため、ハードコードせず、プロジェクトのパス設定ファイルから読み込みます。

## 1. プロジェクトの基本パス

現在のプロジェクトの標準パスは次のとおりです。

```text
/gs/fs/tgj-26ICP/uf03782/yang/li-research
```

他の利用者は、このパスをそのまま使わず、自分のプロジェクト領域に置き換えてください。

```bash
export PROJECT_ROOT=/gs/fs/<group>/<user>/<project>
export PATH_CONFIG="$PROJECT_ROOT/hpc/tsubame_26icp/config/yang_paths.sh"
source "$PATH_CONFIG"
```

`yang_paths.sh` は、環境、モデル、構造、LAMMPS、計算結果のパスを一括管理する設定ファイルです。

## 2. 標準ディレクトリ構成

```text
li-research/
├── envs/                 # Python 環境
│   └── mace_env/
├── models/               # MACE の変換済みモデル
├── structures/           # LAMMPS data / CIF
├── engines/              # GPU 対応 LAMMPS
├── runs/                 # MD 実行結果
├── results/              # MSD、拡散係数、Arrhenius 解析
├── hpc/tsubame_26icp/    # qsub スクリプトとパス設定
└── docs/                 # 手順書と研究記録
```

## 3. パス設定の読み込み

```bash
cd "$PROJECT_ROOT"
source hpc/tsubame_26icp/config/yang_paths.sh

echo "$MACE_ENV"
echo "$MACE_LMP_MLIAP"
echo "$MODELS_ROOT"
echo "$STRUCTURES_ROOT"
```

標準設定では、主な変数は次のようになります。

| 変数 | 内容 |
|---|---|
| `MACE_ENV` | MACE Python 環境 |
| `MACE_LMP_MLIAP` | MACE ML-IAP/Kokkos 対応 LAMMPS 実行ファイル |
| `MODELS_ROOT` | 変換済み MACE モデルの保存先 |
| `STRUCTURES_ROOT` | LAMMPS data ファイルの保存先 |
| `RUNS_ROOT` | MD の出力先 |
| `RESULTS_ROOT` | MSD / Arrhenius 結果の保存先 |

利用者独自の場所を使う場合は、`source` より前に環境変数を設定します。

```bash
export YANG_ROOT=/gs/fs/<group>/<user>
export PROJECT_ROOT="$YANG_ROOT/<project>"
export ENV_ROOT="$YANG_ROOT/envs"
export MACE_ENV="$ENV_ROOT/mace_env"
export ENGINES_ROOT="$PROJECT_ROOT/engines"
export MODELS_ROOT="$PROJECT_ROOT/models"
export STRUCTURES_ROOT="$PROJECT_ROOT/structures"
export RUNS_ROOT="$PROJECT_ROOT/runs"
export RESULTS_ROOT="$PROJECT_ROOT/results"
export MACE_LMP_MLIAP="$ENGINES_ROOT/lammps/mace/install_mliap_gpu/bin/lmp"
```

### 外部利用者の計算結果の保存先

外部利用者が自分の `PROJECT_ROOT` を設定して実行した場合、MD の結果はその利用者のプロジェクト領域に保存されます。

```text
$RUNS_ROOT/md/<model>/<structure>/<temperature>/replica_<n>/<job_id>/
$RESULTS_ROOT/mdanalysis/
```

例えば、次のように設定した場合、結果は共有プロジェクトではなく利用者自身の領域に作成されます。

```bash
export PROJECT_ROOT=/gs/fs/<group>/<user>/<project>
export RUNS_ROOT="$PROJECT_ROOT/runs"
export RESULTS_ROOT="$PROJECT_ROOT/results"
```

逆に、`RUNS_ROOT` と `RESULTS_ROOT` を変更せずに実行すると、結果は設定ファイルに書かれた既定のプロジェクト領域へ保存されます。共有領域への書き込み権限がない場合や、他の利用者の結果と混在する場合があるため、外部利用者は必ず自分のパスを設定してください。

## 4. 環境の確認

```bash
test -x "$MACE_LMP_MLIAP"
test -d "$MACE_ENV"
test -s "$MODELS_ROOT/mace/mace-mpa-0-medium.model-mliap_lammps.pt"

"$MACE_ENV/bin/python" - <<'PY'
import torch
import mace
print("MACE:", mace.__version__)
print("PyTorch:", torch.__version__)
print("CUDA:", torch.version.cuda)
print("CUDA available:", torch.cuda.is_available())
PY
```

`CUDA available: True` だけでは LAMMPS が GPU 版であることを保証しません。LAMMPS 側も確認します。

```bash
"$MACE_LMP_MLIAP" -h 2>&1 | grep -E "KOKKOS|ML-IAP|mliap" || true
```

## 5. MACE モデル

この workflow では、MACE の Python checkpoint をそのまま LAMMPS に渡さず、LAMMPS ML-IAP 形式に変換したモデルを使用します。

```text
models/mace/mace-mpa-0-medium.model-mliap_lammps.pt
models/mace/mace-mp-0b3-medium.model-mliap_lammps.pt
```

モデルと対象元素が一致していることを確認してください。Li₃YCl₆ では `Li Y Cl`、LiNbOCl₄ では `Li Nb O Cl` の順序を LAMMPS input の `pair_coeff` と一致させます。

## 6. GPU LAMMPS の実行

```bash
module purge
module load gcc/14.2.0
module load cuda/12.8.0
module load openmpi/5.0.7-gcc

source "$PROJECT_ROOT/hpc/tsubame_26icp/config/yang_paths.sh"
export CUDA_VISIBLE_DEVICES=0

"$MACE_LMP_MLIAP" \\
  -k on g 1 -sf kk \\
  -pk kokkos newton on neigh half \\
  -in "$PROJECT_ROOT/simulation/mace_mpa0/lammps/in.md_ordered_400K"
```

正式な qsub 実行では、プロジェクトの production script を使用してください。

```bash
qsub -g <group> \\
  -v YANG_PATHS_FILE="$PROJECT_ROOT/hpc/tsubame_26icp/config/yang_paths.sh" \\
  "$PROJECT_ROOT/hpc/tsubame_26icp/production/md_mace_mpa0_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh"
```

別の温度だけを実行する場合は、スクリプトが対応している環境変数を使用します。

```bash
qsub -g <group> -t 1-3 -tc 3 \\
  -v TEMPERATURES_OVERRIDE=1000 \\
  "$PROJECT_ROOT/hpc/tsubame_26icp/production/md_mace_mpa0_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh"
```

## 7. 出力の確認

各 replica の出力には、少なくとも次のファイルが生成されます。

```text
relax.log
relax.stdout
relaxed.data
md.log
md.stdout
msd_li.dat
trajectory.lammpstrj
final.data
run_metadata.txt
environment.txt
```

計算完了の最低条件は次のとおりです。

```bash
test -s relaxed.data
test -s msd_li.dat
test -s trajectory.lammpstrj
test -s final.data
grep -E "Loop time|Performance:" md.log
```

`trajectory.lammpstrj` は MDAnalysis による MSD 再解析に使用します。`thermo` 出力は `md.log` に保存されるため、温度、エネルギー、圧力、セルサイズも確認できます。

## 8. 外部利用者が変更すべき項目

外部利用者は次の項目だけを自分の環境に合わせて変更してください。

1. `YANG_ROOT`、`PROJECT_ROOT`
2. `ENV_ROOT` と `MACE_ENV`
3. `MODELS_ROOT`、`STRUCTURES_ROOT`、`RUNS_ROOT`
4. `MACE_LMP_MLIAP`
5. qsub の `-g <group>`
6. input 内の `pair_coeff` の元素順序

スクリプト本体に絶対パスを直接書き込む方法は避け、`yang_paths.sh` または利用者独自の paths file で管理してください。

## 9. よくあるエラー

### `command not found: lmp`

`MACE_LMP_MLIAP` が正しいか確認し、直接実行してください。

```bash
ls -l "$MACE_LMP_MLIAP"
```

### `CUDA available: False`

GPU queue、CUDA module、Python 環境を確認します。ログインノードでの確認だけで GPU 動作を判定しないでください。

### `Cannot open model` または元素数のエラー

モデルパス、`pair_coeff` の元素順序、LAMMPS data の atom type 数を確認してください。

### relaxation は完了するが MD 出力がない

`md.stderr`、`md.log`、`md.stdout` の最後の 50 行を確認してください。`final.data` がない場合は正式結果として扱わないでください。

## 10. 再現性のための記録

各計算では、次の情報を記録してください。

- Git commit
- 使用した paths file
- MACE / PyTorch / CUDA のバージョン
- LAMMPS 実行ファイルの場所
- model ファイルの場所
- 構造ファイルの場所
- 温度、timestep、equilibration、production
- job ID と replica 番号

これにより、別のユーザーや別の TSUBAME プロジェクト領域でも同じ workflow を再現できます。
