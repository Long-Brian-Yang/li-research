# MACE 計算環境：TSUBAME 構築と会社環境への移行

## 1. この文書の位置付け

ここでは、既存リポジトリの MACE-MPA-0／MACE-MP-0b3 medium と LAMMPS ML-IAP/Kokkos の構築例を出発点に、TSUBAME 上で環境を再現・確認する手順と、会社の計算環境へ移す際の確認事項を整理する。TSUBAME の値をそのまま会社の標準環境とみなすものではない。会社側の GPU、scheduler、module、利用許諾、データ管理規則が未確定なら、最初に管理者へ確認してから構成を決定する。

## 2. MACE の実行スタック

MACE MD を実行する環境は、少なくとも次の層からなる。

| 層 | 固定・確認対象 | 確認理由 |
|---|---|---|
| Hardware／driver | GPU 型、compute capability、driver、GPU memory | 対応する CUDA binary と precision を決める |
| CUDA | toolkit、runtime、NVCC、Kokkos CUDA backend | PyTorch と LAMMPS の双方が同じ GPU runtime を利用できるか |
| Compiler／MPI | GCC、CMake、OpenMPI | LAMMPS build と実行時 ABI を一致させる |
| Python | Python、PyTorch と PyTorch CUDA build | MACE checkpoint 変換・Python bridge の依存 |
| MACE backend | mace-torch、e3nn/cuequivariance、CuPy 等 | checkpoint を評価・変換する |
| LAMMPS | commit/tag、ML-IAP、Python、Kokkos、CUDA build options | `mliap_unified` inference backend を動作させる |
| Model | checkpoint 名、version、license、SHA-256 | 結果の再現、利用許諾、変更検知 |
| System input | element order、units、PBC、cell、potential file | 変換と LAMMPS 入力の物理的整合 |

どの層も単独で動けば十分というわけではない。Python から MACE を import できても、LAMMPS の embedded Python binding、`liblammps`、Kokkos/CUDA と checkpoint 変換形式の組合せが一致するとは限らない。

## 3. TSUBAME における現在の repo 構成

### 3.1 既存 repo が記録している構築値

canonical build script [`build_mace_mliap_gpu_maceenv.sh`](../../hpc/tsubame_26icp/build/build_mace_mliap_gpu_maceenv.sh) は、既存の Python 3.10 `mace_env`、GCC 14.2.0、CUDA 12.8.0、OpenMPI 5.0.7-gcc、Kokkos Hopper90／SM90、ML-IAP、LAMMPS Python package を前提にする。canonical path は [`yang_paths.sh`](../../hpc/tsubame_26icp/config/yang_paths.sh) に置かれている。

これは repo 内の recipe の内容である。実際に TSUBAME に存在する module/version、GPU 型・割当、MACE 環境と checkpoint の現在値は、作業開始日に scheduler 内で確認する。MACE 公式 installation guide も PyTorch の対応する platform/CUDA build を先に決めるよう案内しているため、無計画に pip install で PyTorch を上書きしない。

### 3.2 事前確認

ログイン node で行うのは軽いファイル確認と job script 準備までとする。GPU 検出、PyTorch CUDA、MACE import、checkpoint 変換、LAMMPS 計算は、利用規則に従う GPU job 内で確認する。

```bash
source hpc/tsubame_26icp/config/yang_paths.sh
printf 'PROJECT_ROOT=%s\nMACE_ENV=%s\nMACE_LMP_MLIAP=%s\nMODELS_ROOT=%s\n' \
  "$PROJECT_ROOT" "$MACE_ENV" "$MACE_LMP_MLIAP" "$MODELS_ROOT"
test -x "$MACE_ENV/bin/python"
test -x "$MACE_LMP_MLIAP"
test -s "$MODELS_ROOT/mace/mace-mp-0b3-medium.model"
bash -n hpc/tsubame_26icp/build/build_mace_mliap_gpu_maceenv.sh
```

これらは path/shell のみを確認し、job を投入しない。GPU 側の import 検査用 repo script は [`check_mace_env_gpu.sh`](../../hpc/tsubame_26icp/validation/check_mace_env_gpu.sh) で、AGE の GPU resource を要求する job として実行する。job の投入には現在の TSUBAME 公式 scheduler 規則を使い、ログイン node から直接 GPU 計算を始めない。

GPU job 内の最低限の出力には次を含める。

```bash
nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
"$MACE_ENV/bin/python" -c 'import torch, mace; print(torch.__version__, torch.version.cuda, torch.cuda.is_available()); print(mace.__version__)'
```

実際の recipe は cuEquivariance/CuPy も import している。使用する MACE model/backend に必要なパッケージを追加で確認し、単なる `import mace` の成功をもって完了としない。

### 3.3 構築・変換・動作確認

1. cluster policy、GPU request、walltime、module と既存 environment の利用権限を確認する。
2. Python、PyTorch、CUDA wheel、MACE、cuEquivariance 系、CuPy の exact version を採取する。既存環境を不用意に更新せず、試作環境を分離する。
3. 対応する LAMMPS source revision を決め、ML-IAP、Kokkos/CUDA、Python package、MPI を recipe の組合せで構築する。
4. MACE checkpoint を原本として保存し SHA-256 とライセンスを記録する。変換用 `.pt` は新しい出力名にし、原本を上書きしない。
5. conversion script が出す ML-IAP model を LAMMPS から読み込めることを確認する。
6. 同一の周期構造について ASE/MACE と LAMMPS のエネルギー・力を比較し、atom order、units、元素 mapping、stress sign/unit、PBC を照合する。許容誤差は dtype/backend ごとに事前に決め、検証結果に記録する。
7. 小さい構造の短い MD で finite energy/force、温度、cell、neighbor list、GPU usage を確認する。
8. その後に限り短 benchmark、続いて対象計算の投入を判断する。

checkpoint の conversion が成功しただけでは backend parity は証明されない。LAMMPS ML-IAP の実装、MACE checkpoint、ML-IAP serialization が互換かは、対象 version の公式資料と実測 parity test で検証する。

## 4. TSUBAME で特に注意すること

- **scheduler／login node：** 重い計算と GPU import test を login node で実行しない。job の GPU、CPU、memory、walltime、queue/group 指定は TSUBAME の現行 handbook に従う。
- **module 再現性：** job 中に `module list`、`which nvcc`、`nvcc --version`、`mpirun --version`、GPU/driver 情報を保存する。login session の環境継承だけを当てにしない。
- **Python ABI／shared libraries：** CUDA toolkit、PyTorch CUDA build、NVIDIA pip libraries、LAMMPS `lib`、Python wheel が衝突しやすい。script の `LD_LIBRARY_PATH` を無闇に広げず、job の実効値を記録する。
- **GPU visibility／MPI ranks：** 1 GPU job で複数 process が同一 GPU を奪い合っていないか確認する。Kokkos GPU device と MPI rank 配置は benchmark で検証する。
- **Storage／capacity：** 300–600 ps の軌跡、restart、ログは大きくなりうる。job ごとの出力先、quota、保存期間、退避先を事前確認する。重要な原始軌跡を figure 用抽出 frame で置き換えない。
- **paths：** repo には `/gs/fs/tgj-26ICP/uf03782/yang` を既定とする個人/group パスがある。別 project/account でそのまま使用しない。古い HPC root script には移行前のパスが残るものがある。
- **GPU build architecture：** `Kokkos_ARCH_HOPPER90` と CUDA architecture 90 は現行 recipe が対象とする GPU 用。別 GPU へコピーするときは compute capability に合わせ再構築する。
- **完成状態：** scheduler の exit status 0 は実行の終了であり、trajectory の物理検証ではない。温度・energy・cell・組成・短接触・MSD/RDF・文献対応を別途確認する。

TSUBAME の開始、job、software/module の最新条件は公式 [start](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/start/)、[jobs](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/jobs/)、[software](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/software/)を参照する。利用組織の契約・quota・運用ルールを、過去の job script より優先する。

## 5. 会社環境へ移行する前の確認票

| 項目 | 移行先の管理者と合意する内容 |
|---|---|
| Compute | GPU 型・数、driver/CUDA 対応範囲、GPU partition と予約規則 |
| Scheduler | Slurm/AGE/その他、GPU request syntax、walltime、array job、preemption |
| Software | OS、GCC/CMake/MPI、CUDA、Python/PyTorch、container 可否 |
| Storage | project/scratch/archive の使い分け、quota、backup、retention、転送方法 |
| Security | proprietary composition、構造、DFT data を置ける計算機・filesystem・Git remote |
| License | MACE model/checkpoint、疑似ポテンシャル、VASP/商用コード、社内利用・再配布条件 |
| Source control | 社内 Git hosting、private repository、secrets、credential、artifact policy |
| Validation | parity test の許容誤差、基準構造、承認者、計算結果のレビュー手順 |

移行時に TSUBAME の account/group ID、絶対パス、SSH key、API token、個人の `yang_paths.sh`、module load 行、compiled binary をそのまま配布しない。会社の filesystem policy で認められる repository と artifact store を選び、非公開データや checkpoint の公開 Git への push を避ける。

最低限持ち運ぶのは source code、入力テンプレート、versioned workflow、短い公開可能な regression structure、検証スクリプト、再配布可能な小さなテスト結果である。GPU binary と Python environment は移行先で構築し直し、build log、commit hash、dependency list、model SHA-256 を記録する。元の MACE model が再配布不可なら、移行先が正規に取得できる手段だけを使う。

会社環境に proprietary materials を置く許可が明示されるまで、TSUBAME や公開 Git を機密データの搬送先と仮定しない。

## 6. model と software のライセンス

MACE code と foundation checkpoint の license は同一とは限らず、モデルごとに異なる。model card、checkpoint metadata、配布元の license を使う形態（社内研究、商用評価、fine-tuning、モデル配布、成果物の公開）ごとに確認する。MACE foundation models の一覧には model ごとの license 表記があるため、単に「MACE は MIT」と一般化しない。

DFT package、pseudopotential、訓練データ、fine-tuned checkpoint にも個別条件がある。特に VASP は利用者・組織の有効ライセンスが必要であり、大学での使用権が会社へ移るとは限らない。会社の DFT 計算は会社が利用許諾を持つコード・資源で実施する。

参照：

- [MACE installation](https://mace-docs.readthedocs.io/en/latest/guide/installation.html)
- [MACE repository and current model information](https://github.com/ACEsuit/mace)
- [MACE foundation models](https://github.com/ACEsuit/mace-foundations)
- [LAMMPS ML-IAP pair style](https://docs.lammps.org/pair_mliap.html)
- [VASP: Who can license VASP?](https://www.vasp.at/info/faq/who_can_license/)
- [VASP public-domain FAQ](https://vasp.at/info/faq/public_domain/)
- [VASP Wiki](https://vasp.at/wiki/Welcome)

## 7. この repo の保守範囲

現行 build／validation recipe と相違がある設定を見つけた場合は、確認なしに「TSUBAME 標準」として本文へ固定せず、module list と実行 log を採取してから改訂する。環境が変わったときは build script、`yang_paths.sh`、preflight、README、parity test を同一変更で更新する。
