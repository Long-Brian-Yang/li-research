# 日報：方向 2 の構造・ポテンシャル・MD workflow

**日付：** 2026-08-19  
**対象：** 高 Li⁺ 伝導性ハライド／オキシハライド固体電解質（方向 2）  
**今回の判断：** まずは汎用機械学習ポテンシャルで、二つの代表構造の安定性と輸送解析 workflow を確立する。

## 1. 今回選択する二つの構造

| 材料 | 文献上の位置づけ | 今回の計算モデル | 原子数 | 選択理由 |
|---|---|---:|---:|---|
| Li₃YCl₆ | Asano et al., *Advanced Materials* (2018) の高電圧ハライド SSE benchmark | (2\times2\times4) | 480 | ハライド骨格、Li disorder、4 V 正極適合性を調べる基準構造 |
| LiNbOCl₄ | Tanaka et al., *Angewandte Chemie* (2023) の mixed-anion oxyhalide | (2\times2\times3) を新規 follow-up として作成 | 336 | O/Cl mixed-anion 環境、柔らかい polyanion framework、高伝導候補を調べる構造 |

### Li₃YCl₆

三つの Li/Y ordering model を (2\times2\times4) に拡大した。各モデルは

\[
\mathrm{Li_{144}Y_{48}Cl_{288}}
\]

であり、縮約すると Li₃YCl₆ となる。最短原子間距離は約 2.39–2.46 Å で、
幾何学的には MD 入力として使用可能である。ただし、(2\times2\times2) の
relaxed cell を c 軸方向に繰り返したモデルなので、最終的な production MD の前に
超胞全体の relaxation を行うのが望ましい。

### LiNbOCl₄

スクリーンショットから再構成した conventional cell を明示的な full-occupancy
ordered model として (2\times2\times3) に拡大した。組成は

\[
\mathrm{Li_{48}Nb_{48}O_{48}Cl_{192}}
\]

であり、縮約すると LiNbOCl₄ となる。現在の直接反復モデルは 336 atoms である。
文献で報告される 168-atom cell は異なる crystallographic setting に基づくため、
原子数を直接比較してはいけない。LiNbOCl₄ は最短距離が約 1.91 Å であるため、
必ず relaxation 後に局所構造が妥当か確認する。

## 2. M3GNet から MACE へ変更する理由

### M3GNet の位置づけ

M3GNet は Materials Project の構造 relaxation データを基盤とする汎用 graph
interatomic potential であり、構造 relaxation や材料スクリーニングに適している。
ただし、今回の長時間 ionic transport MD では、Python/ASE を介した計算よりも、
GPU 上で効率よく force を評価できる実装が重要になる。

### MACE-MPA-0 のデータセットと元素範囲

今回使用する MACE-MPA-0 は、公式情報では 89 元素をカバーし、主に

- MPTrj（Materials Project の relaxation trajectory）
- subsampled Alexandria dataset（sAlex）

を用いて学習された汎用材料ポテンシャルである。したがって Li、Y、Cl、Nb、O は
元素範囲内に含まれる。

ただし、MACE-MPA-0 は Li₃YCl₆ や LiNbOCl₄ 専用に fine-tune されたモデルではない。
そのため、今回の結果はまず workflow 検証と定性的な比較に用い、実験値との厳密な
一致や論文レベルの定量性を主張しない。必要であれば、後で DFT/AIMD データを用いた
fine-tuning または Δ-learning を検討する。

### MACE を選ぶ実務上の理由

1. MACE は equivariant message-passing により、局所環境の方向性と多体相互作用を
   表現しやすい。
2. MACE-MPA-0 は MACE-MP-0 より広い材料データを用いた後続 foundation model で、
   材料系の安定性と高圧領域の改善を目的としている。
3. MACE は LAMMPS の ML-IAP interface と Kokkos GPU backend に接続できるため、
   長時間 MD の計算効率を上げやすい。
4. 同じ model を relaxation、短時間 stability test、production MD に連続して使用
   でき、計算 workflow を一貫させやすい。

MACE 公式資料では、ML-IAP interface は GPU 用に最適化され、旧来の MACE LAMMPS
interface より高い性能を目指した実装と説明されている。モデル変換は GPU ノード上で
行い、実行時の GPU architecture と合わせる必要がある。

参考：

- [MACE foundation models](https://github.com/ACEsuit/mace-foundations)
- [MACE official documentation: ML-IAP and LAMMPS](https://mace-docs.readthedocs.io/_/downloads/en/latest/pdf/)
- [M3GNet original paper](https://doi.org/10.1038/s43588-022-00349-3)

## 3. ASE-MD から LAMMPS へ変更する理由

### ASE-MD を残す用途

ASE-MD は、構造の読み込み、短時間 relaxation、少数ステップの sanity check に便利で
ある。したがって、完全に削除するのではなく、次の用途に限定する。

- CIF からの構造読み込みと変換確認
- 100–1000 step の短時間 test
- 初期構造、原子種、単位、速度初期化の検証

### production MD を LAMMPS に移す理由

1. LAMMPS はコンパイル済みの MD engine であり、Python 主体の ASE loop より長時間
   trajectory に適している。
2. Kokkos GPU backend を使用でき、TSUBAME の NVIDIA GPU を直接利用できる。
3. NVT、thermo output、restart、LAMMPS trajectory dump を標準形式で保存できる。
4. (2\times2\times4) Li₃YCl₆ と (2\times2\times3) LiNbOCl₄ のような大きめの
   supercell で、MSD、Li diffusion、構造安定性を同じ engine で比較できる。
5. 後で GPUMD/NEP89、DFT/AIMD、他の MLIP と比較しやすい。

dump は削除しない。production 中は 1000 step ごとに

```lammps
dump traj all custom 1000 output.lammpstrj id type xu yu zu vx vy vz
```

を保存し、MSD、Li の unwrapped trajectory、拡散経路、構造崩壊の有無を解析する。
thermo output も削除しない。`thermo 1000` と `thermo_style` により、温度、ポテンシャル
エネルギー、運動エネルギー、全エネルギー、圧力、体積、セル長を 1000 step ごとに
保存し、`lammps.log` に記録する。dump と thermo は、trajectory の MSD 解析と同時に
温度安定性・エネルギー安定性を確認するために必要である。不要な頻繁出力による I/O
overhead だけを避ける。

## 4. 現時点の MD protocol

| 項目 | 設定 |
|---|---|
| Engine | LAMMPS + MACE ML-IAP/Kokkos |
| Ensemble | NVT |
| 温度 | 400 K（初期 workflow test） |
| timestep | 1 fs |
| equilibration | 10 ps（10,000 steps） |
| production | 100 ps（100,000 steps） |
| trajectory dump | 1,000 stepsごと（Li の MSD・経路解析用） |
| thermo output | 1,000 stepsごと（温度・エネルギー・圧力・体積・セル長） |
| log | `lammps.log` として保存 |
| GPU | 原則 1 job : 1 GPU |
| 解析 | 温度、エネルギー、最短距離、MSD、(D_{Li})、Nernst–Einstein 推定値 |

400 K は室温の直接再現ではなく、Li motion を観測するための初期検証温度である。
最終的な実験比較では 300 K を基準にし、温度依存性と block uncertainty を別途評価する。

## 5. TSUBAME での次の作業

1. GPU node 上で MACE-MPA-0 を ML-IAP 形式に変換する。
2. `PKG_ML-IAP`、`PKG_KOKKOS`、Python support を有効にした LAMMPS を構築する。
3. まず 1,000 step の benchmark を実行し、`timesteps/s` と GPU memory を記録する。
4. 旧 `pair_style mace` と ML-IAP/Kokkos のエネルギー、温度、短時間 trajectory を比較する。
5. 問題がなければ 10 ps equilibration + 100 ps production を実行する。
6. LiNbOCl₄ については、(2\times2\times3) ordered model を relaxation してから
   production MD に進める。

## 6. 今回の結論

今回の目的は、最初から専用 MLIP を新規学習することではない。まずは MACE-MPA-0 と
LAMMPS を用いて、二つの代表構造について、

\[
\text{structure} \rightarrow \text{relaxation} \rightarrow \text{stability test}
\rightarrow \text{MD} \rightarrow \text{MSD / diffusion analysis}
\]

という再現可能な workflow を完成させる。その後、汎用モデルの適用限界が明らかに
なった場合に限り、対象構造の DFT/AIMD データを追加して fine-tuning を検討する。
