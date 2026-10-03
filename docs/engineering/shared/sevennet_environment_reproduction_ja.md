# SevenNet Python 環境の再現手順

## 目的と適用範囲

本書は、TSUBAME の SevenNet 0.13.0 Python 環境を配布・再構築する手順である。Conda 環境定義は [`environment-sevennet.yml`](environment-sevennet.yml)、採取した package version は [`requirements-sevennet-py39-cu124.lock.txt`](requirements-sevennet-py39-cu124.lock.txt) に記録した。GPU LAMMPS は Python venv とは別成果物であり、build 条件は[GPU LAMMPS 構築ガイド](../matgl_sevennet_environment_reproduction_ja.md)を参照する。

## TSUBAME 基準環境

| 項目 | 確認値 |
|---|---|
| Environment variable | `SEVENNET_ENV` |
| Environment type | Python venv |
| Python | 3.9.25、base interpreter `/usr/bin/python3.9` |
| OS | Linux x86_64、RHEL 9 系、glibc 2.34 |
| SevenNet | 0.13.0 |
| PyTorch | 2.6.0+cu124、CUDA runtime 12.4 |
| 主要 package | e3nn 0.6.0、NumPy 2.0.2、PyG 2.6.1 |
| Snapshot | 2026-10-02、53 package entries |

## TSUBAME archive

TSUBAME group share: `/gs/fs/tgj-26ICP/uf03782/yang/envs/share/`。

| ファイル | サイズ | SHA-256 |
|---|---:|---|
| `sevennet_env_tsubame_rhel9_x86_64_py39_cuda124_20261002.tar.gz` | 約3.1 GB | `4608190f19fe44543a58046d088fe12ecec9333caf4729841da7fdaea825fd94` |

同名の `.sha256` sidecar も共有先にある。archive は `/usr/bin/python3` を base interpreter とする同系統 TSUBAME host 向けに作成し、新しい TSUBAME path へ展開して Python、Torch、SevenNet の import と CLI module を確認した。

### 同系統 TSUBAME host での展開

```bash
ARCHIVE=sevennet_env_tsubame_rhel9_x86_64_py39_cuda124_20261002.tar.gz
sha256sum -c "$ARCHIVE.sha256"
SEVENNET_ENV="$HOME/envs/sevennet_env"
mkdir -p "$SEVENNET_ENV"
tar -xzf "$ARCHIVE" -C "$SEVENNET_ENV"

# Relocated venv は activation より interpreter の直接指定を推奨。
"$SEVENNET_ENV/bin/python" - <<'PY'
import sys, platform, torch, sevenn
print("Python:", sys.version.split()[0], "prefix:", sys.prefix)
print("Platform:", platform.platform())
print("PyTorch:", torch.__version__, "CUDA runtime:", torch.version.cuda)
print("SevenNet import:", sevenn.__file__)
assert torch.__version__ == "2.6.0+cu124"
PY
"$SEVENNET_ENV/bin/python" -m sevenn.main.sevenn --help
```

`sevenn` などの console-script wrapper は元の絶対 path を shebang に持つ場合がある。直接呼び出す前に shebang を確認し、必要な場合は `#!/usr/bin/env python` ではなく移行後 venv の Python を指すよう修正する。現行 build script にも同じ wrapper 修正がある。

### 別 host での再構築

別 OS、別 CPU architecture、異なる base Python では TSUBAME venv archive を流用せず、Conda YAML から Python 3.9.25 環境を再構築する。YAML は同じ directory の package snapshot と公式 CUDA 12.4 wheel source を参照する。

```bash
conda env create -f docs/engineering/shared/environment-sevennet.yml
conda activate sevennet_env
python -m pip check
python -c 'import torch; print(torch.__version__, torch.version.cuda); assert torch.version.cuda == "12.4"'
```

環境構築後、対象 GPU job 上で CUDA tensor smoke test を実行し、`torch.cuda.is_available()`、GPU 名、driver、`torch.version.cuda` を保存する。package import は GPU runtime test や計算精度検証の代わりにならない。

## GPU LAMMPS との境界

- archive は SevenNet Python package と依存 library をまとめたもので、LAMMPS binary、CUDA driver/toolkit、MPI compiler、model weights は含まない。
- SevenNet GPU LAMMPS は patched LAMMPS の `e3gnn/parallel` backend を使用する。ML-IAP backend とは別の接続方式である。
- build recipe は GCC 14.2.0、CUDA toolkit 12.8.0、OpenMPI 5.0.7-gcc を指定する一方、Python PyTorch runtime は CUDA 12.4。実際の build・GPU job で ABI/linkage と動作を検証する。
- TSUBAME の指定 install path に SevenNet LAMMPS binary/source checkout は確認できていない。build recipe が存在することを「build 済み」と表現しない。

## 関連資料

- [MatGL／M3GNet Python 環境の再現手順](matgl_m3gnet_environment_reproduction_ja.md)
- [MatGL／M3GNet・SevenNet GPU LAMMPS 構築ガイド](../matgl_sevennet_environment_reproduction_ja.md)
- [MACE Python 環境の再現手順](mace_environment_reproduction_ja.md)
