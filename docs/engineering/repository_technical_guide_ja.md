# Li Research リポジトリ技術ガイド

このガイドは、結晶 benchmark から非晶質材料の MD・輸送解析までを支えるコード、環境、データ経路を一か所に整理した技術入口である。科学的な結果と文献比較は[日本語 Material Review](../materials/materials_overview_ja.md)を正とし、本書では「計算をどのコード・環境で実行し、結果をどう再確認するか」を説明する。

## 1. 対象範囲と読み方

このリポジトリは単一の Python 製品ではなく、再利用ライブラリ、材料別スクリプト、HPC 構築・投入設定、入力構造、計算結果、企業向け説明資料から成る研究コード群である。TSUBAME にしか存在しない大容量軌跡・モデル重み・実行バイナリは Git に含まれない。したがって、この文書はコードの入口と再現手順を示すが、TSUBAME 上の現在のキュー状態や外部ファイルの存在を保証しない。

読む順序：

1. [リポジトリのトップ README](../../README.md)：プロジェクトの概要と入口。
2. [MACE／TSUBAME／会社環境への移行](mace_tsubame_company_migration_ja.md)：MACE-MD 実行環境。
3. [MatGL／M3GNet Python 環境の再現](matgl_m3gnet_environment_reproduction_ja.md)：MatGL 用 lock、環境 archive、source bundle。
4. [SevenNet Python 環境の再現](sevennet_environment_reproduction_ja.md)：SevenNet 用 lock と環境 archive。
5. [MatGL／M3GNet・SevenNet GPU LAMMPS 構築](matgl_sevennet_environment_reproduction_ja.md)：モデル別 GPU LAMMPS build 条件と移行境界。
6. [DFT データ作成と MACE fine-tuning](dft_and_finetuning_ja.md)：将来の材料専用モデル構築案。
7. [Material Review](../materials/materials_overview_ja.md)：材料ごとの計算条件、結果、文献対比。

## 2. ディレクトリと責務

| パス | 内容 |
|---|---|
| `src/li_research/` | 結晶構造作製、形式変換、MSD／拡散解析、RDF、作図などの再利用可能な Python コード |
| `scripts/structures/` | 材料別の準備、入力生成、解析、作図、証拠パッケージ作成スクリプト |
| `hpc/tsubame_26icp/` | TSUBAME のパス設定、エンジンビルド、benchmark、LAMMPS／GPUMD 入力、AGE job script、事前確認 |
| `hpc/shared/nep89_gpumd/` | 共有 GPUMD／NEP89 環境向けの実行補助。MACE 環境とは独立 |
| `simulation/` | エンジン別の LAMMPS 入力と補助資料 |
| `structures/` | 参照 CIF と計算用の結晶構造 |
| `materials/candidates/` | 非晶質候補の作製、検査、provenance、候補別 README |
| `materials/evidence/` | 報告図を確認するための命名済み構造・抽出フレームと manifest |
| `materials/references/` | 文献から取得した構造・補足ファイルと出典情報 |
| `results/` | CSV／JSON、生成図、解析スナップショット、履歴結果 |
| `docs/materials/` | 維持対象の材料レビュー、共通定義、主図、figure manifest |
| `docs/presentations/` | 中間・最終発表用 Markdown |
| `tests/` | 数値処理、構造、ファイル契約、図表、レポート規約のテスト |

スクリプト間で同じディレクトリの別スクリプトを import する実装があるため、ファイル移動・一括改名の前に参照先とテストを確認する。

## 3. 環境と依存関係

### 3.1 既知の実行環境

| 環境 | 主用途 | 注意点 |
|---|---|---|
| 開発用 macOS／Linux | Markdown、軽量 Python 解析、pytest | リポジトリに完全固定した Python lock file はない。ローカル版数は TSUBAME の版数ではない |
| TSUBAME `tgj-26ICP` | GPU MD、エンジン構築、production、軌跡後処理 | アカウント、quota、queue、module、モデル、実行状態は集群へ接続して都度確認 |
| 共有 NEP／GPUMD | 既存の NEP89 検証ルート | MACE＋LAMMPS のインストールとは別管理。環境を混合しない |

TSUBAME の MACE、MatGL／M3GNet、SevenNet は、それぞれ専用の環境説明 Markdown と package lock `.txt` を対にして管理する。GPU LAMMPS は Python 環境とは別に構築するため、[GPU LAMMPS 構築ガイド](matgl_sevennet_environment_reproduction_ja.md)を参照する。Python package 環境の存在は対応する LAMMPS binary の build／動作確認を意味しない。

#### MLIP 実行環境の横断一覧

3つの MLIP は同じ計算環境の中で切り替えるのではなく、依存関係と LAMMPS backend の組ごとに環境を分離する。比較・移行時は Python package だけでなく、推論方式、GPU runtime、LAMMPS interface、build toolchain を一組として確認する。

| 環境 | 用途・モデル | Python／主要 runtime | MD 接続・GPU backend | 環境の受け渡し |
|---|---|---|---|---|
| `MACE_ENV` (`mace_env`) | MACE foundation potential の推論、結晶 benchmark、ML-IAP MD | Python 3.10.19、MACE 0.3.15、PyTorch 2.10.0、CUDA runtime 12.8 | 別 build の LAMMPS ML-IAP／Kokkos CUDA。compiler・MPI・CUDA toolkit を Python 環境に混ぜない | [環境説明 Markdown](mace_environment_reproduction_ja.md) ＋ [package lock `.txt`](../../hpc/tsubame_26icp/requirements-mace-py310-cu128.lock.txt) |
| `MATGL_ENV` (`matgl_env`) | MatGL 4.0.3 を介した M3GNet 系モデルの推論・材料計算 | Python 3.12.12、PyTorch 2.10.0、CUDA runtime 12.8、MatGL source は commit 固定 | recipe 上は native／Kokkos `ML-MATGL`。指定 install binary は未確認 | [環境説明 Markdown](matgl_m3gnet_environment_reproduction_ja.md) ＋ [package lock `.txt`](../../hpc/tsubame_26icp/requirements-matgl-py312-cu128.lock.txt) |
| `SEVENNET_ENV` (`sevennet_env`) | SevenNet 0.13.0 モデルの推論・MD | Python 3.9.25、PyTorch 2.6.0+cu124、CUDA runtime 12.4 | recipe 上は patched LAMMPS `e3gnn/parallel`。build recipe の CUDA toolkit は 12.8.0、指定 install binary は未確認 | [環境説明 Markdown](sevennet_environment_reproduction_ja.md) ＋ [package lock `.txt`](../../hpc/tsubame_26icp/requirements-sevennet-py39-cu124.lock.txt) |

MatGL/M3GNet と SevenNet の package snapshot、archive、SHA-256、展開／再構築手順は各環境の専用説明に記載し、GPU LAMMPS build 条件は[共通 build ガイド](matgl_sevennet_environment_reproduction_ja.md)にまとめる。MACE の詳細は [MACE 環境ガイド](mace_environment_reproduction_ja.md)を参照する。environment archive は model weights、NVIDIA driver、GPU 対応 LAMMPS binary を含まない。

#### なぜ環境を分けるか

- Python の minor version と依存 package の版が異なるため、1つの venv/Conda env に混ぜると resolver による上書きや import/API の衝突が起こり得る。
- PyTorch の CUDA runtime（MACE/MatGL は 12.8、SevenNet は 12.4）と、LAMMPS を compile する CUDA toolkit/module は別物。driver はさらに別のホスト側要件であり、3つの版を同じ値として扱わない。
- LAMMPS 接続方式も異なる。MACE は ML-IAP、MatGL は ML-MATGL pair style、SevenNet は `e3gnn/parallel` backend を使うため、pair style、CMake package、MPI/GPU linkage をそれぞれ構築・検証する。
- Python の `import` 成功、LAMMPS の pair style 登録、energy/force parity、GPU smoke test、長時間 MD の妥当性は別々の確認段階である。

#### 実行前に表示・保存する環境情報

```bash
source hpc/tsubame_26icp/config/yang_paths.sh
for env_name in MACE_ENV MATGL_ENV SEVENNET_ENV; do
  env_path="${!env_name}"
  echo "[$env_name] $env_path"
  if [[ -x "$env_path/bin/python" ]]; then
    "$env_path/bin/python" -c 'import sys,platform; print(sys.version.split()[0], platform.platform())'
    "$env_path/bin/python" -m pip list --format=freeze
  fi
done
```

GPU job ではさらに `nvidia-smi` と `torch.version.cuda`／`torch.cuda.is_available()` を記録する。別 account や会社環境へ移すときは、`yang_paths.sh` の絶対 path を転記せず、各 environment root、model path、LAMMPS binary、module 名を移行先に合わせて設定し直す。

リポジトリに `pyproject.toml`、`requirements.txt`、Conda lock、Dockerfile はなく、「pip install 一つで全計算が再現できる」とは言えない。一般的な解析 import は ASE、NumPy、SciPy、Matplotlib を中心とし、データ診断の一部に MDAnalysis／OpenPyXL、テストに pytest を使う。MACE／PyTorch、LAMMPS、CUDA、MPI は別のエンジン環境として扱う。

### 3.2 TSUBAME パス設定

基準ファイルは [`yang_paths.sh`](../../hpc/tsubame_26icp/config/yang_paths.sh)。主要変数は `YANG_ROOT`、`PROJECT_ROOT`、`ENV_ROOT`、`STRUCTURES_ROOT`、`MODELS_ROOT`、`ENGINES_ROOT`、`RUNS_ROOT`、`RESULTS_ROOT`、`MACE_ENV`、`MACE_LMP_MLIAP` である。現在の既定値は個人の tgj-26ICP 作業場所を指す。会社や別アカウントでそのまま利用せず、移行時に必ず置き換える。

この repo の MACE ML-IAP/Kokkos 構築 recipe は、Python 3.10 の既存 `mace_env`、GCC 14.2.0、CUDA 12.8.0、OpenMPI 5.0.7-gcc、Kokkos Hopper90／SM90 を記録する。これは現行の構築レシピに記載された組合せであり、第三者の環境での動作保証やソフトウェア全体の固定 lock ではない。CUDA driver と toolkit の互換性、GPU 型、PyTorch の CUDA build、cuEquivariance 系 wheel、CuPy、LAMMPS のビルド設定を一体で検証する。

SevenNet、MatGL、GPUMD はそれぞれ別 Python／MPI／CUDA／コンパイル構成を持つ。例えば GPUMD build recipe に CUDA 13.1 が現れる一方、MACE LAMMPS は CUDA 12.8 の構成である。これらを同じ環境だとみなさない。

## 4. TSUBAME でのデプロイと実行手順

TSUBAME の公式利用説明は[システム開始ガイド](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/start/)、[job／scheduler](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/jobs/)、[software／module](https://helpdesk.t3.gsic.titech.ac.jp/t4docs_preview/master/handbook.ja/software/)を確認する。TSUBAME4.0 の scheduler は AGE（Altair Grid Engine）である。job option や GPU resource の指定は更新される可能性があるため、投入時点の公式 handbook を優先する。

1. checkout と branch、作業ディレクトリ、入力ファイル、モデルファイルを読み取り専用確認する。
2. `yang_paths.sh` の値を確認し、アカウント依存パスを作業用設定に反映する。
3. 対象 MACE checkpoint の出所・version・利用条件を確認する。
4. Python／PyTorch／CUDA と GPU への可視性を GPU job 内で事前確認する。
5. 対象 checkpoint を ML-IAP 形式へ変換し、変換前後のエネルギー／力が一致するか小さい周期構造でテストする。
6. LAMMPS の ML-IAP、Python bridge、Kokkos/CUDA、MPI を同じビルド設定で起動できることを確認する。
7. 最小 smoke test、短い benchmark の順に実行し、その後に限り本番 MD の投入を検討する。
8. 生成物、stdout/stderr、入力、module list、環境情報、モデルと構造の SHA-256 を run directory に保存する。

重い Python import、モデル変換、LAMMPS／GPUMD 計算は login node 上で実行しない。必要な GPU／CPU／memory／walltime を明示した job script を使い、GPU preflight も scheduler 経由で行う。job が exit したことはソフトウェア起動の確認にすぎず、構造・拡散・文献再現性を証明しない。

repo 内の参考入口：

| 用途 | ファイル |
|---|---|
| canonical MACE ML-IAP/Kokkos LAMMPS build | [`build_mace_mliap_gpu_maceenv.sh`](../../hpc/tsubame_26icp/build/build_mace_mliap_gpu_maceenv.sh) |
| GPU 環境事前検査 | [`check_mace_env_gpu.sh`](../../hpc/tsubame_26icp/validation/check_mace_env_gpu.sh) |
| LAMMPS MACE 入力と checkpoint 変換 | [`inputs/mace_mliap/`](../../hpc/tsubame_26icp/inputs/mace_mliap/README.md) |
| TSUBAME 全体のパス | [`yang_paths.sh`](../../hpc/tsubame_26icp/config/yang_paths.sh) |
| project と依存の cluster-side check | [`validate_project.sh`](../../hpc/tsubame_26icp/validation/validate_project.sh) |

古い root-level build script には移行前の個人パスを含むものがある。新規作業では `build/`、`benchmark/`、`production/`、`validation/` の現行入口を優先し、root-level の旧 script を利用する場合は内容と参照先を確認する。

## 5. コアコードと分析コード

### 5.1 再利用モジュール：`src/li_research/`

| 領域 | 主ファイル | 役割 |
|---|---|---|
| 結晶構造作製 | `structures/build_2x2x2.py`、`build_li3ycl6_ordered.py`、`make_li3ycl6_2x2x4.py`、`make_linboocl4_2x2x3.py` | 有序構造・supercell の作製と幾何確認 |
| 形式変換 | `conversion/prepare_data.py`、`lammps_data_to_extxyz.py`、`relaxed_lammps_dump_to_extxyz.py` | CIF／LAMMPS data／dump／extxyz 間の変換。部分占有を未検証で MD に投入しない |
| LAMMPS 輸送 | `analysis/lammps/msd_diffusion.py`、`analyze_li_jumps.py` | MSD、自己拡散、Li hop の統計 |
| GPUMD／GPUMDkit | `analysis/gpumd/prepare_gpumdkit_unwrapped.py`、`analyze_gpumdkit_windows.py`、`analyze_300K_2x2x4.py` | unwrapped 座標準備と MSD 後処理 |
| RDF／Arrhenius | `analysis/rdf/recompute_li3ycl6_rdf_all_trajectories.py`、`analysis/arrhenius/plot_li3ycl6_arrhenius_midterm.py`、`plot_linboocl4_arrhenius.py` | 取得可能な全trajectoryからの構造統計と輸送の温度依存図 |

### 5.2 材料別スクリプト：`scripts/structures/`

| 作業 | 代表入口 |
|---|---|
| 結晶・非晶質構造準備 | `prepare_hussain2024.py`、`build_lzoc_reference.py`、`prepare_lszc_272.py`、`prepare_lszc_nep.py`、`prepare_lips_nep.py`、`prepare_lipon_nep.py`、`pack_lszc.py` |
| 構造・作製検査 | `build_material_evidence_package.py`、`structure_followup.py`、`validate_amorphous_trials.py`、`check_lzoc_equilibration.py`、`compare_lzoc_candidates.py` |
| 輸送と反復解析 | `analyze_lzoc_production.py`、`analyze_lzoc_seed_repeats.py`、`analyze_lszc_matched_repeats.py`、`analyze_lszc_endpoints.py`、`analyze_lips_transport.py`、`analyze_lipon_transport.py`、`analyze_lipon_repeats.py` |
| 文献データ・集計 | `extract_tang_transport.py`、`extract_chen_source.py`、`complete_amorphous_comparisons.py`、`finish_materials_transport.py` |
| 図と evidence | `li_diffusion_style.py`、`plot_amorphous_arrhenius_comparisons.py`、`plot_literature_correspondence.py`、`curate_overview_figures.py`、`build_material_evidence_package.py` |

`hpc/tsubame_26icp/production/` の shell script は scheduler job の起動入口、同フォルダの `.lmp` は LAMMPS 入力、Python は個別の確認／処理である。名前に production とあっても、実行前に job resource、入力、出力先、構造・モデル checksum、time step、温度と ensemble を読む。投入用 script の実行は外部計算を開始する操作である。

## 6. 計算から報告までのデータフロー

```text
論文・実験構造／値
    ↓ 出典・組成・占有状態の確認
結晶モデル または 非晶質候補と作製履歴
    ↓ 組成・最小距離・cell・provenance 検査
形式変換 → engine／potential preflight → relaxation／equilibration
    ↓ 条件を固定した温度別 production MD
完全な raw trajectory（通常 TSUBAME／ローカル保管）
    ↓ 全対象 trajectory を同じ解析規約へ投入
MSD、D、Arrhenius、RDF、配位、角度、骨格運動、安定性
    ↓ 同じ定義・単位の実験／文献結果と比較
CSV／JSON、図、hash／manifest
    ↓
日本語・英語 Material Review と evidence package
```

解析規約：

- MSD は周期境界・座標 unwrap、COM 補正、粒子集合、時間原点平均の有無、単位、fit protocol を記録する。
- 独立速度 seed が複数ある場合、各温度の全 trajectory を同じ規則で処理する。値の良否や文献一致度で replica を除外しない。平均と標本 SD は、異なる amorphous glass 間の不確かさを表すものではない。
- fit window は事前に共通設定し、全温度・全 replica に同じものを適用する。窓の感度が必要なら補足診断として全条件を開示し、最終値に都合のよい区間を事後採用しない。
- Arrhenius fit は入力物理量に合わせる。実験が室温 conductivity と活性化エネルギーだけを報告するとき、実験 tracer-D(T) を創作しない。
- RDF／配位数／角度は局所環境の指標である。weighted PDF や EXAFS の物理量と同一視しない。
- 代表フレームの抽出は可視化用の bounded sampling に限り、輸送統計の母集団選別とは分ける。

### 6.1 MLP-MD の数値安定性と物理的妥当性の確認

「計算が最後まで終了した」「温度が設定値付近にある」だけでは、MLP trajectory が安定・妥当だとは判断できない。少なくとも、(1) potential の実装・入力整合、(2) 数値積分の安定性、(3) 構造・熱力学の定常性、(4) 文献に対応する物理量、を別々に確認する。数値的に安定な trajectory でも、その MLP が DFT／実験を正しく再現する保証はない。

| 検査 | 見る量・方法 | 正常と判断する目安／読み違え防止 |
|---|---|---|
| potential と backend の整合 | 同じ snapshot を MACE reference backend と LAMMPS ML-IAP に与え、energy と atomic force を比較。element mapping、atom order、units、PBC、cell も照合 | 事前に定めた許容差で一致すること。変換成功や `import` 成功だけでは不十分 |
| 初期構造・力 | minimization 前後の最小原子間距離、最大力、energy、cell、組成 | 異常な重なり・NaN・極端な force がないこと。最小距離の基準は元素対・組成・温度に応じて定め、全材料共通の閾値を機械的に適用しない |
| NVE energy conservation | 平衡化 snapshot から thermostat/barostat を外し、固定 cell・固定粒子数で NVE を短時間実行。`pe`、`ke`、`etotal = pe + ke` を追跡し、etotal の時系列傾向、block 平均、時間刻み依存性を確認 | PE と KE は相互変換して振動するのが通常で、PE 単独の上下はエネルギー保存失敗を意味しない。`etotal` に持続的な一方向 drift、急増、飛びがないかを見る。許容 drift は系・時間刻み・精度・用途ごとに決め、短い NVE test と時間刻みを変えた比較で確認する。普遍的な単一閾値はない |
| NVT production の熱力学量 | `temp`、`pe`、`ke`、`etotal`、必要に応じ `econserve`、pressure、density／cell を出力 | thermostat 下で `etotal` は thermostat との熱交換により揺らぐため、NVE のような一定値を要求しない。初期過渡後の平均・分散・block 平均が定常で、温度や体積に一方向の長期 drift がないか確認する。`econserve` は LAMMPS の対象 fix が記録する coupling energy を含む量で、利用 fix の定義も確認する |
| NPT equilibration | `temp`、pressure、`vol`、`density`、`lx/ly/lz`、`pe` を時系列と区間別統計で確認 | 圧力瞬時値は有限系で大きく揺らぐので target 圧力との瞬間一致を要求しない。体積・密度・cell の block 平均が plateau に近づき、持続的膨張／収縮が残っていないかを見て、平衡後の平均 cell を production 条件に使う。barostat 下の `etotal` を保存量と誤認しない |
| RDF と配位数 | 複数の部分 RDF (g_{\alpha\beta}(r))、第一ピーク位置・幅、第一極小までの積分配位数、温度・block・repeat ごとの変化を確認 | RDF は局所構造の統計であり、単独で拡散や熱力学安定性を証明しない。距離 bin、cutoff、密度規格化、元素 pair、集計 frame 範囲を全比較で揃える。結晶なら既知の配位・格子、ガラスなら実験／文献の対応する partial RDF や PDF と比較する |
| 時間方向の構造・局所異常 | 最小距離分布、配位分布、cell/density、bond/coordination の時間推移、代表 snapshot の可視化 | 物理的に不合理な短接触、組成・ネットワークの破綻、局所環境の急激な偏りがないかを調べる。代表 frame は診断・可視化用であり、trajectory 全体の統計を置き換えない |
| 輸送解析へ進む前 | Li MSD、線形領域、time-origin/block 安定性、温度系列、全 repeat | MSD が十分な時間範囲で拡散挙動を示すか確認する。fit protocol を事前固定し、全温度・全 repeat に一律適用する。安定性検査を通っても、統計が不十分なら (D) や (E_a) を確定値として扱わない |

LAMMPS では、production と診断の目的に合わせ、少なくとも `step/time, temp, pe, ke, etotal, press, vol, density, lx, ly, lz` の必要項目を出力する。NVE 診断では、対象 LAMMPS version／fix で利用できる場合に `econserve` も記録する。現在の repo の入力例でも `temp pe ke etotal press vol lx ly lz` を使用している。NVT/NPT の `etotal` 揺らぎを即座に不安定と見なしたり、PE が単調でないことを異常と見なしたりしない。逆に、滑らかな energy 曲線だけでモデルの物理精度を主張しない。

**推奨ゲート順：** backend parity と構造検査 → 短い NVE 時間刻み診断 → NVT/NPT の温度・cell・energy stationarity → RDF／配位と局所異常 → 全 trajectory の輸送解析 → 同じ定義の文献・実験比較。問題があれば該当ゲートへ戻り、温度・時間刻み・ensemble・cell を一度に変えず、変更要因が追跡できるようにする。

LAMMPS の [`compute rdf`](https://docs.lammps.org/compute_rdf.html) は RDF と累積配位数を定義し、[`thermo_style`](https://docs.lammps.org/thermo_style.html) は `pe`、`ke`、`etotal`、`econserve` などの出力定義を説明する。Nose–Hoover 系の [`fix nvt/npt`](https://docs.lammps.org/fix_nh.html) は thermostat/barostat の挙動・設定を確認する一次資料として参照する。具体的な設定は実行中の LAMMPS version のマニュアルと入力 script に合わせる。

## 7. データ、再現性、報告

| 場所 | 内容 |
|---|---|
| `structures/raw/`、`structures/reference/` | 入手・再構成した基準構造 |
| `structures/ordered/` | 明示的に占有を解決した計算用結晶構造 |
| `materials/candidates/<material>/` | 非晶質候補、作製条件、検査、provenance |
| `materials/evidence/` | 命名済み構造・可視化用 frame・manifest |
| `results/amorphous_review_20260915/` | 2026-09-15 系の材料別 source／analysis／summary |
| `results/publication_all_materials/` | 発表図・表と source data |
| `docs/materials/figures/` | 主 Material Review の図と manifest |
| `runs/` | Git 管理外のローカル production／分析出力 |

`.gitignore` により model weights、巨大 trajectory、restart、build output が除外される場合がある。したがって、必要な解析コード・入力条件・軽量な CSV／JSON・checksum・figure manifest は repo に保存し、元 trajectory が外部にある場合は保管先を明記する。完了印や checksum は provenance を補助するが、科学的妥当性の判定を代替しない。

## 8. テストと確認

通常のローカル検査：

```bash
python -m pytest -q
```

pytest、ASE、NumPy、SciPy、Matplotlib などが必要。これは構造・数値・データ契約・図のファイル検査であり、CUDA、モデル重み、LAMMPS backend、HPC scheduler や物理的な文献再現性を検証しない。TSUBAME の `validation/` は集群環境の入口であり、実 MD の構造・熱力学・輸送解析は別途行う。

テスト群は LZOC／LSZC／Li₃PS₄／LiPON、structure preparation、figure/export、Markdown 数式、Material Review、evidence manifest に分かれる。テストが使えない場合は、欠けた依存と実行できた検査を区別して報告する。

## 9. 維持ルール

1. 科学的主報告は日本語・英語 Material Review にまとめ、工程詳細はこの技術ガイドとリンク先の二つの運用ガイドにまとめる。
2. software version や module version は実ファイル・実行ログで確認できる場合のみ固定値として記す。
3. 研究計算の入力・出力・モデル・構造 hash を保存し、再解析時にどの source か再現できるようにする。
4. 複数 trajectory が存在するときは全件を同一条件で解析する。事後的な replica 選択、文献一致度による選別、特定モデル曲線の振幅補正をしない。
5. 図を更新した際は日英 Material Review、figure manifest、source CSV、provenance を合わせて確認する。
6. 旧結果は履歴として識別し、新解析の結果と混同しない。原始データや履歴記録を整理のためだけに破棄しない。

## 10. 現行 code の詳細索引

以下は本ガイド作成時の `rg --files` による repository inventory である。ファイルがあることは、現在の production 入口・実行可能環境・科学的有効性を保証しない。**実行前に README、source、input、model、output path、provenance を確認する。** trajectory の統計解析・図は全ての対象軌跡を扱う実装を優先し、古い選択結果 JSON を新しい報告へ流用しない。

### `src/li_research/`

```text
structures/
  build_2x2x2.py
  build_li3ycl6_ordered.py
  make_li3ycl6_2x2x4.py
  make_linboocl4_2x2x3.py
conversion/
  prepare_data.py
  lammps_data_to_extxyz.py
  relaxed_lammps_dump_to_extxyz.py
analysis/lammps/
  msd_diffusion.py
  analyze_li_jumps.py
  plot_li3ycl6_msd_three_models.py
  plot_linboocl4_msd_three_models.py
analysis/gpumd/
  prepare_gpumdkit_unwrapped.py
  analyze_gpumdkit_windows.py
  analyze_300K_2x2x4.py
analysis/rdf/
  recompute_li3ycl6_rdf_all_trajectories.py
analysis/arrhenius/
  plot_li3ycl6_arrhenius_midterm.py
  plot_linboocl4_arrhenius.py
```

### `scripts/structures/`

```text
Structure/preparation:
  prepare_hussain2024.py, build_lzoc_reference.py, prepare_lszc_272.py,
  prepare_lszc_nep.py, prepare_lszc_production.py,
  prepare_lszc_split_followup.py, prepare_lips_nep.py, prepare_lipon_nep.py,
  pack_lszc.py, extract_lszc_clusters.py
Structure/evidence/checks:
  build_material_evidence_package.py, structure_followup.py,
  compare_lzoc_candidates.py, check_lzoc_candidate3.py,
  check_lzoc_equilibration.py, validate_amorphous_trials.py,
  review_release_trials.py, refresh_legacy_rdf.py, summarize_legacy_highT.py,
  lzoc_order_motion.py, lzoc300_structure_motion.py
Transport/analysis:
  analyze_lzoc_production.py, analyze_lzoc_seed_repeats.py,
  analyze_followup300.py, analyze_lszc_endpoints.py,
  analyze_lszc_matched_repeats.py, analyze_lips_transport.py,
  analyze_lips_r1_remote.py, analyze_lipon_transport.py,
  analyze_lipon_repeats.py, analyze_lipon_600k_long.py,
  analyze_lipon_precontact.py, analyze_targeted_diagnostics.py
Reference/summary:
  extract_tang_transport.py, extract_chen_source.py,
  complete_amorphous_comparisons.py, finish_amorphous_analysis.py,
  finish_materials_transport.py, paper_aligned_analysis.py,
  legacy_paper_alignment.py, portfolio_supplement.py, lzoc_table4_comparison.py
Plot/report:
  plot_amorphous_arrhenius_comparisons.py, plot_lips_r1_report.py,
  plot_literature_correspondence.py, plot_lzoc_preparation.py,
  plot_targeted_diagnostics.py, plot_legacy_lzoc_comparison.py,
  curate_overview_figures.py, li_diffusion_style.py
TSUBAME submission wrappers (submission may start remote computation):
  submit_lips_r1_analysis.sh, submit_lps_r1_transport.sh,
  submit_lszc_endpoint_npt150.sh, submit_lszc_matched4t.sh,
  submit_lszc_production300.sh, submit_lszc_split50.sh,
  submit_lzoc_nhc300.sh, submit_lzoc_seed300.sh,
  submit_preparation_repeats.sh
```

`selected` という単語は元素 pair、数値 interval、表示用 frame 抽出にも使われるため、単語検索だけでコードを削除しない。ここで廃止するのは、文献との近さ・数値の良さ・trajectory 指標で独立 trajectory を事後選択する動作である。

### `hpc/tsubame_26icp/` build／benchmark／production／validation

```text
build:
  build_allegro_lammps.sh, build_gpumd.sh,
  build_mace_mliap_gpu_maceenv.sh, build_matgl_m3gnet_gpu.sh,
  build_sevennet_parallel_gpu.sh, compile_allegro_model.sh
benchmark:
  gpumd_nep89_300K_2x2x4.sh, gpumd_nep89_400K.sh, gpumd_nep89_smoke.sh,
  mace_mp0b2_small_mliap_benchmark.sh,
  mace_mp0b3_medium_mliap_canonical_benchmark.sh,
  mace_mpa0_medium_mliap_canonical_benchmark.sh,
  matgl_m3gnet_cpu_benchmark.sh, matgl_m3gnet_gpu_benchmark.sh,
  sevennet_nano_serial_benchmark.sh, sevennet_parallel_benchmark.sh
validation:
  check_mace_env_gpu.sh, validate_project.sh
production:
  amorphous_compare_20260915.sh, amorphous_lzoc_4t.sh/.lmp,
  amorphous_lzoc_candidate.sh/.lmp, amorphous_lzoc_equilibrate.sh/.lmp,
  amorphous_lzoc_high_temperature.sh/.lmp, amorphous_lzoc_pilot.sh/.py,
  amorphous_lzoc_reference.sh/.lmp, amorphous_targeted_diagnostics.sh,
  check_lzoc_virial.sh/.py, lipon_600K_600ps_repeats.sh,
  lipon_600K_600ps_repeats_R6_R7.sh, lipon_nep89_release.sh,
  lipon_nep89_trial.sh, lipon_transport_bulk.sh, lipon_transport_repeats.sh,
  lips_nep89_trial.sh, lips_transport_control.sh, lszc_272_npt.sh,
  lszc_272_release.sh, lszc_nep89_preflight.sh, lszc_packed272_smoke.sh,
  lszc_paper_temperatures.sh, lzoc192_hold300.sh, lzoc_aimd_aligned_80ps.sh,
  lzoc_hussain192_cool.sh, lzoc_hussain192_heat.sh,
  lzoc_hussain192_trial.sh, lzoc_nep89.sh, nep89_npt_extension.sh,
  md_m3gnet_gpu_li3ycl6_03_400K_3rep_50ps_eq_500ps_prod.sh,
  md_mace_mpa0_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh,
  md_sevennet_nano_li3ycl6_03_5T_3rep_50ps_eq_500ps_prod.sh,
  portfolio_followup.sh
```

TSUBAME build/production script は計算や file 作成などの副作用を持つ。本文の技術索引・構築例を確認するだけでは job submission の許可を意味しない。
