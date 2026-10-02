# MACE Python 環境の再現手順

## 目的と適用範囲

この手順は、TSUBAME の `mace_env` で記録した Python パッケージ構成を、別の Linux GPU 計算機で再構築するためのものです。環境一式のコピーではなく、バージョン固定リストから各計算機上でインストールします。

記録した基準環境は **RHEL 9 系／x86_64、CPython 3.10.19、PyTorch 2.10.0（CUDA 12.8 build）、MACE 0.3.15** です。完全な Python package snapshot は [`requirements-mace-py310-cu128.lock.txt`](../../hpc/tsubame_26icp/requirements-mace-py310-cu128.lock.txt) にあります。これは Linux x86_64 向けの version lock であり、任意の OS・GPU に対するバイナリ互換性を保証するものではありません。

対象外：TSUBAME の NVIDIA kernel driver、CUDA toolkit/module、MPI/GCC/CMake module、独自ビルドした GPU LAMMPS 実行ファイル、MACE checkpoint／重み、入力構造、trajectory、ジョブスクリプト。特に LAMMPS ML-IAP/Kokkos/CUDA は Python 環境とは別に移行先でビルドします。

## 基準環境の主要バージョン

| 項目 | 記録値 |
|---|---|
| OS / architecture | Linux x86_64、RHEL 9 系（TSUBAME login node の報告値） |
| glibc | 2.34 |
| Python | 3.10.19 |
| PyTorch | `torch==2.10.0`、runtime reported by `torch.version.cuda`: 12.8 |
| MACE | `mace-torch==0.3.15` |
| GPU kernel libraries | CUDA 12 系 NVIDIA Python packages、CuPy 14.2.0、cuEquivariance 0.10.0 |
| Atomistic Python packages | ASE 3.28.0、e3nn 0.4.4、matscipy 1.2.0、NumPy 2.2.6、SciPy 1.15.3 |
| Snapshot date | 2026-10-02 |

## 移行先の前提確認

インストール前に管理者へ確認し、次の情報を記録します。

1. Linux distribution、CPU architecture、glibc version。
2. GPU model と compute capability、NVIDIA driver version。
3. 対象 driver が CUDA 12.8 runtime を実行できること。
4. Python 3.10 が利用可能であること。
5. PyPI と PyTorch wheel index への接続可否、proxy／内部 mirror の指定。
6. CUDA toolkit が必要な追加 build（LAMMPS/Kokkos 等）の有無。
7. MACE model/checkpoint と計算コードを社内利用・再配布できるライセンス。

macOS、Windows、ARM64 では、この Linux wheel lock をそのまま使わないでください。別の Linux distribution でも glibc、GPU driver、利用可能な wheel が異なる場合は、対象機向けに PyTorch と CUDA の組合せを選び直し、その環境で version lock と動作試験を更新します。ホストの NVIDIA driver は Python wheel に含まれません。

## Linux x86_64 での再構築

以下は Python 3.10 と CUDA 12.8 対応 NVIDIA driver が利用可能な Linux x86_64 を想定します。社内 mirror を使う場合は index URL を管理者指定のものに置換します。

```bash
python3.10 --version
nvidia-smi

python3.10 -m venv mace_env
source mace_env/bin/activate
python -m pip install --upgrade pip

# PyTorch CUDA 12.8 build を先に固定する。
python -m pip install --index-url https://download.pytorch.org/whl/cu128 \
  'torch==2.10.0'

# TSUBAME で採取した Python package versions。
python -m pip install -r hpc/tsubame_26icp/requirements-mace-py310-cu128.lock.txt

python -m pip check
```

PyTorch を先に CUDA 12.8 index から導入するのは、通常の PyPI 版で上書きされ CPU-only build になるのを防ぐためです。lock 内の `torch==2.10.0` は public version を照合します。導入後に `torch.version.cuda` が `12.8` であることを必ず検査します。

## 動作確認

### CPU/login node での package import

```bash
python - <<'PY'
import sys, platform, torch, mace, ase, cupy
import cuequivariance_torch, cuequivariance_ops_torch

print('Python:', sys.version.split()[0])
print('Platform:', platform.platform())
print('PyTorch:', torch.__version__)
print('PyTorch CUDA runtime:', torch.version.cuda)
print('CUDA available on this node:', torch.cuda.is_available())
print('MACE:', mace.__version__)
print('ASE:', ase.__version__)
print('CuPy:', cupy.__version__)
print('cuEquivariance imports: OK')
assert torch.version.cuda == '12.8'
PY
```

`torch.cuda.is_available() == False` は login node に GPU driver/device がない場合には想定されます。GPU 動作の合否は、移行先の正式な GPU queue/job 上で判定します。

### GPU node での最低限の確認

GPU job 内で次を実行し、出力を保存します。

```bash
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
python - <<'PY'
import torch
assert torch.cuda.is_available(), 'CUDA GPU is not visible to this job'
x = torch.randn((1024, 1024), device='cuda')
y = x @ x
torch.cuda.synchronize()
print('GPU:', torch.cuda.get_device_name(0))
print('CUDA runtime:', torch.version.cuda)
print('CUDA tensor smoke test: OK', y.shape)
PY
```

これは PyTorch CUDA の基本動作試験です。対象 MACE checkpoint による短い推論、ASE/LAMMPS parity、MACE-MD の energy/force 検証の代替ではありません。

## 移行先で追加構築するもの

LAMMPS を利用する workflow では、Python package 導入とは別に、移行先に合わせて GCC、CMake、MPI、CUDA toolkit、LAMMPS revision、ML-IAP、Kokkos backend を選び再構築します。TSUBAME の Hopper90/SM90 build flags や absolute paths を別 GPU／別 scheduler に流用しません。既存の build recipe と移行注意点は[TSUBAME 構築・会社環境移行ガイド](mace_tsubame_company_migration_ja.md)を参照します。

導入した MACE checkpoint は、コード version と別に model 名、入手元、version、SHA-256、利用ライセンスを記録します。チェックポイント自体がこの lock や環境アーカイブに含まれることはありません。

## 再現性と限界

- この lock は TSUBAME 環境の package version snapshot です。hash を含む完全な wheel artifact lock ではありません。
- Package version が同一でも、GPU architecture、driver、compiler、MPI、CUDA libraries、BLAS/thread settings によって挙動や性能が変わることがあります。
- 初回構築後に `pip list --format=freeze` を保存し、この lock との差分を確認します。意図しない version drift があれば計算開始前に解消します。
- インストール成功、import 成功、CUDA tensor smoke test 成功、LAMMPS parity、短時間 MD 妥当性は別々の検証段階です。
- Foundation model と全依存 package のライセンスを、会社内利用・fine-tuning・再配布のそれぞれについて個別に確認します。
