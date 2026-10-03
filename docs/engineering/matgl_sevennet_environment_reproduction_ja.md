# MatGL／M3GNet・SevenNet GPU LAMMPS 構築ガイド

## 目的と再現範囲

本書は MatGL／M3GNet と SevenNet に対応する GPU LAMMPS の構築条件を記録する。各環境の version、lock、archive、Python 環境の再配置手順は [`shared/`](shared/) 内の[MatGL／M3GNet 環境説明](shared/matgl_m3gnet_environment_reproduction_ja.md)と[SevenNet 環境説明](shared/sevennet_environment_reproduction_ja.md)を参照する。Python 環境、GPU LAMMPS 実行ファイル、CUDA driver/toolkit、モデル重みは別々の成果物であり、Python archive だけで LAMMPS や GPU 実行環境まで再現できるわけではない。

環境の基準日は **2026-10-02**。TSUBAME の共有環境を読み取り確認し、パッケージ一覧を lock file として保存した。lock file は TSUBAME 上の採取時点の version snapshot であり、wheel の SHA-256 を含む完全な artifact lock ではない。

| 対象 | Python 環境 | GPU LAMMPS | 状態 |
|---|---|---|---|
| MatGL／M3GNet | Conda、Python 3.12.12、MatGL 4.0.3、PyTorch 2.10.0+cu128 | Kokkos CUDA、ML-MATGL pair style の build recipe あり | Python 環境と再配置 archive を確認。設定済み LAMMPS 実行ファイルと source checkout は TSUBAME の指定場所に存在しない |
| SevenNet | venv、Python 3.9.25、SevenNet 0.13.0、PyTorch 2.6.0+cu124 | patched LAMMPS `e3gnn/parallel` build recipe あり | Python 環境を確認し、再配置可能 archive を作成。指定 LAMMPS 実行ファイルと source checkout は TSUBAME の指定場所に存在しない |

## 環境一覧と成果物

### MatGL／M3GNet

- Canonical environment path: `MATGL_ENV`（`hpc/tsubame_26icp/config/yang_paths.sh` で定義）。TSUBAME 実体は `/gs/fs/tgj-26ICP/uf03782/yang/envs/matgl_env`。
- Conda environment、Python 3.12.12、Linux x86_64、glibc 2.34、採取時の disk usage 約8.0 GB。
- 主要 package: `matgl==4.0.3`, `torch==2.10.0+cu128`, `e3nn==0.4.4`, `ase==3.27.0`, `numpy==2.4.2`。
- `matgl` は PyPI wheel ではなく editable install で、採取時の upstream は `https://github.com/materialyzeai/matgl.git`、commit `25b3a291b0cba570fbda75f4922fb51f004208ae`。package list は配布元を表現しないため、厳密に再現する場合は最後にこの commit を使う。
- PyTorch は CUDA 12.8 runtime build。login node では CUDA device が見えず `torch.cuda.is_available()` が false となるため、GPU 判定は GPU job 内で行う。
- 完全な採取 package snapshot: [`requirements-matgl-py312-cu128.lock.txt`](shared/requirements-matgl-py312-cu128.lock.txt)。
- TSUBAME group share の Conda archive: `/gs/fs/tgj-26ICP/uf03782/yang/envs/share/matgl_env_tsubame_rhel9_x86_64_py312_cuda128_20261002.tar.gz`（約4.4 GB）。SHA-256: `ed8b10586140747d7bc98c0d14e4deebab7cc546798491879dc68c31a7432692`。
- MatGL editable source の commit 固定 sidecar: `/gs/fs/tgj-26ICP/uf03782/yang/envs/share/matgl_source_4.0.3_25b3a29_20261002.tar.gz`（約2.7 MB）。SHA-256: `5dc19809d0f80da80dc9e8433da3b312b027221f9c09ca7a5c0f557d00711aa2`。
- 環境 archive は依存 package を保持し、editable MatGL source は sidecar に分離した。再配置テストでは新 path で `conda-unpack` 後に sidecar source を `pip install --no-deps --no-build-isolation` し、Python 3.12.12、Torch 2.10.0+cu128、MatGL 4.0.3 の import を確認した。

### SevenNet

- Canonical environment path: `SEVENNET_ENV`（同じ path config で定義）。TSUBAME 実体は `/gs/fs/tgj-26ICP/uf03782/yang/envs/sevennet_env`。
- venv、base interpreter `/usr/bin/python3.9`、Python 3.9.25、Linux x86_64、glibc 2.34、採取時の disk usage 約5.2 GB。
- 主要 package: `sevenn==0.13.0`, `torch==2.6.0+cu124`, `e3nn==0.6.0`, `numpy==2.0.2`。
- PyTorch は CUDA 12.4 runtime build。login node の CUDA availability は GPU job での動作試験を意味しない。
- 完全な採取 package snapshot: [`requirements-sevennet-py39-cu124.lock.txt`](shared/requirements-sevennet-py39-cu124.lock.txt)。
- TSUBAME group share archive: `/gs/fs/tgj-26ICP/uf03782/yang/envs/share/sevennet_env_tsubame_rhel9_x86_64_py39_cuda124_20261002.tar.gz`（約3.1 GB）。SHA-256 は隣接する `.sha256` file に記録。
- SHA-256: `4608190f19fe44543a58046d088fe12ecec9333caf4729841da7fdaea825fd94`。
- 2026-10-02 に新しい TSUBAME path へ一時展開し、Python 3.9.25、Torch 2.6.0+cu124、SevenNet import と `python -m sevenn.main.sevenn --help` を確認。GPU 計算そのものは login node では検証していない。
- Archive は venv を同系統の RHEL 9／x86_64／glibc 2.34、同じ `/usr/bin/python3.9` base interpreter を持つ TSUBAME-like host 上で再配置するためのもの。別 OS、別 CPU architecture、異なる base Python がある会社計算機向けの portable binary package ではない。異なるホストでは lock file から環境を再構築する。

## 環境 archive の共有・展開

環境 archive は GitHub に登録しない（サイズとバイナリ配布上の制約がある）。TSUBAME の同一 group share を利用できる相手には、archive と隣接する `.sha256` file を案内する。TSUBAME 外の相手には、社内承認済みの大容量ファイル転送先を使い、archive と checksum sidecar の両方を転送する。sidecar は basename のみを記録しているため、転送先で同じ directory に置き、`sha256sum -c "$ARCHIVE.sha256"` で確認する。model weight は含まれない。

### MatGL／M3GNet archive の展開

環境 archive と commit 固定 source sidecar の両方を取得し、同じ directory に置いて checksum を確認する。MatGL は元環境では editable install だったため、source sidecar の再インストールを省略しない。

```bash
ENV_ARCH=matgl_env_tsubame_rhel9_x86_64_py312_cuda128_20261002.tar.gz
SRC_ARCH=matgl_source_4.0.3_25b3a29_20261002.tar.gz
sha256sum -c "$ENV_ARCH.sha256"
sha256sum -c "$SRC_ARCH.sha256"
MATGL_ENV="$HOME/envs/matgl_env"
mkdir -p "$MATGL_ENV"
tar -xzf "$ENV_ARCH" -C "$MATGL_ENV"
"$MATGL_ENV/bin/conda-unpack"
mkdir -p "$MATGL_ENV/source_bundle"
tar -xzf "$SRC_ARCH" -C "$MATGL_ENV/source_bundle"
"$MATGL_ENV/bin/python" -m pip install --no-deps --no-build-isolation \
  "$MATGL_ENV/source_bundle/matgl_source"
"$MATGL_ENV/bin/python" -c 'import torch, matgl; print(torch.__version__, torch.version.cuda, matgl.__version__)'
```

### SevenNet

```bash
ARCHIVE=/path/to/sevennet_env_tsubame_rhel9_x86_64_py39_cuda124_20261002.tar.gz
sha256sum -c "${ARCHIVE}.sha256"
SEVENNET_ENV="$HOME/envs/sevennet_env"
mkdir -p "$SEVENNET_ENV"
tar -xzf "$ARCHIVE" -C "$SEVENNET_ENV"
"$SEVENNET_ENV/bin/python" -c 'import sys, torch, sevenn; print(sys.prefix); print(torch.__version__, torch.version.cuda); print("SevenNet import OK")'
"$SEVENNET_ENV/bin/python" -m sevenn.main.sevenn --help
```

展開先は archive が想定する venv root として使い、shell activation の代わりにこのように interpreter を直接指定する。`venv-pack` archive に含まれる console-script wrapper の shebang が元の絶対パスを指す場合があるため、`sevenn` 等の wrapper を直接実行する前に shebang を確認・修正する（[`build_sevennet_parallel_gpu.sh`](../../hpc/tsubame_26icp/build/build_sevennet_parallel_gpu.sh) に同じ修正処理がある）。別環境へ展開する場合は、`venv-pack` が前提とする同系統の Python 実行環境を用意し、実行可能 entry point の shebang と import、CLI を確認する。通常と異なる interpreter prefix を使った環境では本 archive をそのまま再利用しない。

## MatGL／M3GNet 用 GPU LAMMPS

### TSUBAME build 条件

構築レシピは [`build_matgl_m3gnet_gpu.sh`](../../hpc/tsubame_26icp/build/build_matgl_m3gnet_gpu.sh)。記載されている主な条件は次のとおり。

| 項目 | build recipe の値 |
|---|---|
| Compiler | GCC 14.2.0 |
| MPI | OpenMPI 5.0.10-gcc |
| LAMMPS backend | Kokkos CUDA + Serial、MPI enabled |
| GPU architecture | Hopper 90 / SM90、`TORCH_CUDA_ARCH_LIST=9.0`、`CMAKE_CUDA_ARCHITECTURES=90` |
| Pair styles | `ML-MATGL` および Kokkos variant |
| Python/Torch linkage | canonical `MATGL_ENV` の PyTorch CMake prefix と Torch shared libraries |
| Install target | `$ENGINES_ROOT/lammps/matgl/install/bin/lmp` |
| Source prerequisite | `$ENGINES_ROOT/lammps/matgl/develop` に準備済みの LAMMPS/MatGL extension source が必要。recipe 自身は source を clone しない |

重要な確認事項：recipe は CUDA 12.8 toolkit/module を明示的に `module load` していない。実行前に TSUBAME の module policy と CUDA compiler/toolkit availability を確認し、必要な場合は管理された recipe revision で明示する。未確認の module 操作を別環境へそのまま適用しない。

現時点の TSUBAME canonical path に MatGL LAMMPS source checkout、build tree、または `$MATGL_LMP` 実行ファイルがあるとは確認できていない。また、source revision/commit の指定も recipe から確認できない。そのため本書は build 手順を記録するものであり、「GPU LAMMPS 構築済み」「GPU benchmark 済み」とは扱わない。build 前に source URL と commit、適用 patch を固定・記録する必要がある。

## SevenNet 用 GPU LAMMPS

構築レシピは [`build_sevennet_parallel_gpu.sh`](../../hpc/tsubame_26icp/build/build_sevennet_parallel_gpu.sh)。

| 項目 | build recipe の値 |
|---|---|
| Compiler | GCC 14.2.0 |
| CUDA toolkit | CUDA 12.8.0 |
| MPI | OpenMPI 5.0.7-gcc |
| LAMMPS source | `stable_2Aug2023_update3` branch の patched LAMMPS |
| SevenNet backend | `e3gnn/parallel`（ML-IAP とは別 backend） |
| Python/Torch linkage | canonical `SEVENNET_ENV` の Python、Torch CMake prefix、Torch shared libraries |
| Install target | `$ENGINES_ROOT/lammps/sevennet/install/bin/lmp` |

本レシピは Python archive の展開とは別工程である。LAMMPS source は `stable_2Aug2023_update3` branch の shallow clone で取得するが、branch 名だけでは immutable commit が特定されない。TSUBAME canonical path に SevenNet LAMMPS source checkout と install target があるとは確認できていないため、実行ファイルの構築・GPU run は未確認である。別環境では source commit、compiler、CUDA toolkit、MPI ABI、GPU architecture と driver を記録して再構築する。

## 別計算機で環境を再構築する方法

### 共通の事前確認

1. OS、CPU architecture、glibc、GPU、NVIDIA driver と CUDA runtime compatibility を記録する。
2. Python minor version と社内 package mirror／proxy の利用条件を確認する。
3. 対象 GPU node 上で PyTorch の CUDA tensor smoke test を行う。
4. LAMMPS を利用する場合は、GPU toolkit、compiler、MPI、LAMMPS source revision と pair-style/backend を別途固定する。
5. MatGL/SevenNet の model weight、入手元、version、SHA-256、license を別途記録する。

### MatGL／M3GNet

TSUBAME snapshot を基準に別 host で再構築する場合は、対応する YAML から Python と pip package snapshot を導入する。

```bash
conda env create -f docs/engineering/shared/environment-matgl-m3gnet.yml
conda activate matgl_env
# TSUBAME と同じ MatGL source commit を使い、他の依存版は lock に合わせる。
python -m pip install --no-deps 'matgl @ git+https://github.com/materialyzeai/matgl.git@25b3a291b0cba570fbda75f4922fb51f004208ae'
python -m pip check
```

CUDA 12.8 PyTorch wheel が当該 Python／platform で提供されているかを確認し、環境構築後に GPU job smoke test を行う。異なる host で snapshot 全件をそのまま pip install することは互換性を保証しない。

### SevenNet lock からの再構築

異なる環境向けに再構築する場合は、Python 3.9.25 の Conda YAML を使う。TSUBAME と異なる Python／CUDA／OS なら、単に lock を適用して終わりにせず、解決された package list を新しい環境用 lock として記録し直す。

```bash
conda env create -f docs/engineering/shared/environment-sevennet.yml
conda activate sevennet_env
python -m pip check
python -c 'import torch; print(torch.__version__, torch.version.cuda); assert torch.version.cuda == "12.4"'
```

### 別ホストでの SevenNet 補足

同系統 TSUBAME host には archive 展開・checksum 検査を優先し、import、`sevenn` CLI、GPU tensor を確認する。異なる OS や Python 3.9 base が使えない環境では、archive を移植せず [`requirements-sevennet-py39-cu124.lock.txt`](shared/requirements-sevennet-py39-cu124.lock.txt) を参照して対象環境で再構築する。CUDA 12.4 PyTorch wheel が利用できない場合、PyTorch/CUDA と SevenNet package compatibility を再評価して、新しい lock と動作記録を作る。

## 段階的な検証

| 段階 | 確認内容 | 判定できること／できないこと |
|---|---|---|
| Python package | import、`pip check`、version snapshot | 依存関係と import。GPU 計算の成功は示さない |
| PyTorch GPU | GPU job 内で `torch.cuda.is_available()`、簡単な CUDA tensor 演算 | GPU runtime の基本動作。モデル精度や LAMMPS pair style は示さない |
| Pair style | LAMMPS `-h`、短い固定構造 energy/force test | style 登録と連携。長時間 MD の再現性は示さない |
| Parity | 同一 configuration の Python model と LAMMPS の energy/force 比較 | interface と単位の整合性 |
| Short MD | NVE energy drift、NVT 温度・potential/total energy、RDF | 基本的な数値安定性。輸送係数の収束は示さない |
| Production | 事前に定義した ensemble/時間/解析で複数温度を評価 | 対象条件下の輸送結果。実験再現性は参照データとの比較で別途判断 |

## 運用上の注意

- Python environment archive と LAMMPS binary は異なる配布物。CUDA driver はどちらにも内包されない。
- SevenNet archive は 3.1 GB。Git に追加せず、アクセス制御・容量・license を満たすファイル共有で渡す。
- Conda package list／pip freeze は version 記録であって、全 artifact と channel metadata を含む再現用 lock ではない。MatGL の厳密な再構築が必要なら、採取環境で Conda explicit export（`conda list --explicit`）と pip snapshot を追加保存する。
- Build recipe 中の absolute path、module name、GPU architecture、OpenMPI ABI は移行先に合わせて再設定する。
- MatGL recipe は source tree に `sed` による局所変更を行う。build 前に source revision と差分を保存し、クリーンな source に対して実施する。
- Model weight や入力構造を共有する際は、利用権限、機密情報、配布条件、SHA-256 を確認する。

## 関連資料

- [MACE Python 環境の再現手順](shared/mace_environment_reproduction_ja.md)
- [TSUBAME 構築・会社環境移行ガイド](mace_tsubame_company_migration_ja.md)
- [TSUBAME canonical path configuration](../../hpc/tsubame_26icp/config/yang_paths.sh)
- [MatGL/M3GNet GPU LAMMPS build recipe](../../hpc/tsubame_26icp/build/build_matgl_m3gnet_gpu.sh)
- [SevenNet GPU LAMMPS build recipe](../../hpc/tsubame_26icp/build/build_sevennet_parallel_gpu.sh)
