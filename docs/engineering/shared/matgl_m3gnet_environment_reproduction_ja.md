# MatGL／M3GNet Python 環境の再現手順

## 目的と適用範囲

本書は、TSUBAME で確認した MatGL 4.0.3／M3GNet 系の Python 環境を共有・再構築するための専用手順である。Conda 環境定義は [`environment-matgl-m3gnet.yml`](environment-matgl-m3gnet.yml)、全 package version は [`requirements-matgl-py312-cu128.lock.txt`](requirements-matgl-py312-cu128.lock.txt) にまとめた。GPU LAMMPS は Python 環境と別に構築するため、build 条件は[GPU LAMMPS 構築ガイド](../matgl_sevennet_environment_reproduction_ja.md)を参照する。

この環境は MatGL を通じた M3GNet 系 potential の推論・材料計算を目的とする。MatGL package、PyTorch/CUDA runtime、NVIDIA driver、CUDA toolkit、LAMMPS binary、モデル重みはそれぞれ別要素である。

## TSUBAME 基準環境

| 項目 | 確認値 |
|---|---|
| Environment variable | `MATGL_ENV` |
| Environment type | Conda |
| Python | 3.12.12、Linux x86_64、glibc 2.34 |
| MatGL | 4.0.3、editable source install |
| PyTorch | 2.10.0、CUDA runtime 12.8 |
| 主要 package | ASE 3.27.0、e3nn 0.4.4、NumPy 2.4.2 |
| Snapshot | 2026-10-02、全122 package entries |

採取時の MatGL source は upstream commit `25b3a291b0cba570fbda75f4922fb51f004208ae`。editable install の `.pth` は当初の旧作業 path を指していたため、配布時は環境 archive と source bundle を分け、移行先で source を再インストールする。

## TSUBAME archive と source bundle

共有先は `/gs/fs/tgj-26ICP/uf03782/yang/envs/share/`。

| ファイル | サイズ | SHA-256 |
|---|---:|---|
| `matgl_env_tsubame_rhel9_x86_64_py312_cuda128_20261002.tar.gz` | 約4.4 GB | `ed8b10586140747d7bc98c0d14e4deebab7cc546798491879dc68c31a7432692` |
| `matgl_source_4.0.3_25b3a29_20261002.tar.gz` | 約2.7 MB | `5dc19809d0f80da80dc9e8433da3b312b027221f9c09ca7a5c0f557d00711aa2` |

`.sha256` sidecar もそれぞれ同じ場所に置く。archive と sidecar を同じ directory に保存してから checksum を確認する。

### 同系統 Linux host での展開

本 archive は TSUBAME と同系統の RHEL 9／x86_64 環境向け。展開後に `conda-unpack` を実行して prefix を修正し、editable MatGL source を commit 固定 bundle から導入する。

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
```

確認する。

```bash
"$MATGL_ENV/bin/python" - <<'PY'
import sys, platform, torch, matgl
print("Python:", sys.version.split()[0])
print("Platform:", platform.platform())
print("PyTorch:", torch.__version__, "CUDA runtime:", torch.version.cuda)
print("MatGL:", matgl.__version__, matgl.__file__)
assert torch.__version__ == "2.10.0+cu128"
assert matgl.__version__ == "4.0.3"
PY
```

新しい TSUBAME path への展開で上記 import を確認済み。login node では CUDA device が見えないことがあるため、GPU 利用可否は GPU job 内の smoke test で確認する。

### 別 host での再構築

別 OS／CPU architecture／Python minor version に TSUBAME archive を直接持ち込まず、Conda YAML から Python 3.12.12 の環境を作る。YAML は同じ directory の package snapshot と公式 CUDA 12.8 wheel source を参照する。MatGL source は同じ commit から最後に導入する。

```bash
conda env create -f docs/engineering/shared/environment-matgl-m3gnet.yml
conda activate matgl_env
python -m pip install --no-deps \
  'matgl @ git+https://github.com/materialyzeai/matgl.git@25b3a291b0cba570fbda75f4922fb51f004208ae'
python -m pip check
python -c 'import torch; print(torch.__version__, torch.version.cuda); assert torch.version.cuda == "12.8"'
```

CUDA wheel の提供状況と driver/runtime compatibility は移行先で確認する。異なる platform で同一 lock が解決できない場合は、対象 host に合わせた新しい lock を保存する。

## GPU・LAMMPS との境界

- Python package lock／archive は NVIDIA kernel driver と GPU 対応 LAMMPS executable を含まない。
- MatGL native／Kokkos LAMMPS は `ML-MATGL` pair style と TSUBAME の GCC/OpenMPI/Kokkos/CUDA 条件で別途 compile する。
- TSUBAME の現在の canonical path では MatGL LAMMPS source checkout と install binary を確認できていない。recipe があることと build 済みであることを混同しない。
- Pair-style 登録、同一構造の energy/force parity、GPU tensor test、短時間 MD は段階を分けて検証する。
- Model weights は archive に含まれない。入手元、version、SHA-256、社内利用・再配布条件を別途記録する。

## 関連資料

- [MatGL／M3GNet・SevenNet GPU LAMMPS 構築ガイド](../matgl_sevennet_environment_reproduction_ja.md)
- [SevenNet Python 環境の再現手順](sevennet_environment_reproduction_ja.md)
- [MACE Python 環境の再現手順](mace_environment_reproduction_ja.md)
