# NEP89 + GPUMD：TSUBAME 共同利用

既存の GPUMD 実行ファイルと NEP89 ポテンシャルを Brian のパスから参照します。環境のコピー・再コンパイル・conda activate は不要です。MACE/LAMMPS とは別の実行エンジンです。

## 1. 自分の作業ディレクトリを作る

```bash
mkdir -p /gs/fs/tgj-26ICP/team3/nep89_gpumd/work/$USER/test_1ps
cd /gs/fs/tgj-26ICP/team3/nep89_gpumd/work/$USER/test_1ps
cp /gs/fs/tgj-26ICP/team3/nep89_gpumd/example_model.xyz model.xyz
cp /gs/fs/tgj-26ICP/team3/nep89_gpumd/run_1ps.in run.in
```

example_model.xyz は Li42 Zr24 O12 Cl114、192 原子の LZOC 接続確認用構造です。科学的妥当性を保証する汎用初期構造ではありません。別材料では自分の周期境界・元素名・晶胞を含む GPUMD extended XYZ の model.xyz に交換してください。LAMMPS data や CIF はそのまま読み込めません。

## 2. 1 ps 動作確認

```bash
qsub -g tgj-26ICP /gs/fs/tgj-26ICP/team3/nep89_gpumd/run_gpumd.sh
qstat -u "$USER"
```

gpu_1 を一つ使用し、300 K NVT、0.5 fs × 2000 steps = 1 ps を実行します。初期構造の最適化や本計算の平衡化を代替するテストではありません。既定の計算時間上限は 15 分です。

結果は **qsub を実行した作業ディレクトリ/results/ユーザー名_ジョブ番号/** に保存されます。共有プログラム・モデルの場所には保存されません。同じ作業場所から再提出しても結果フォルダはジョブごとに分離されます。ただし入力はジョブ開始時にコピーされるため、待機中は model.xyz と run.in を変更しないでください。複数条件は別の作業ディレクトリに置いてください。

主な出力：stdout.txt、stderr.txt、thermo.out、dump.xyz、restart.xyz、provenance.sha256、completed.txt。completed.txt はプログラム終了と基本数値チェックのみを示し、構造・密度・拡散の妥当性を保証しません。

## 3. 自分の MD 計算

自分の run.in の温度・ステップ数・平衡化プロトコルを編集します。GPUMD は run.in にシェル変数を展開しないため potential 行には上記の絶対パスを記入してください。時間を延ばす場合：

```bash
qsub -g tgj-26ICP -l h_rt=1:00:00 /gs/fs/tgj-26ICP/team3/nep89_gpumd/run_gpumd.sh
```

入力が他のファイルを参照する高度な計算では、自分用にジョブスクリプトをコピーし、そのファイルも結果フォルダへコピーするよう変更してください。共有スクリプトは model.xyz と run.in の二つをコピーします。

## 4. 自分のジョブスクリプトから直接利用

GPU を割り当てた計算ノード上で：

```bash
source /gs/fs/tgj-26ICP/team3/nep89_gpumd/paths.sh
cd /自分の計算ディレクトリ
"$GPUMD_BIN" > stdout.txt 2> stderr.txt
```

ログインノードで MD を実行しないでください。paths.sh は gcc/14.2.0 と cuda/12.8.0 をロードします。GPUMD は現在のディレクトリの run.in と model.xyz を読みます。

## 5. 共用ファイルと権限

- GPUMD: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/engines/gpumd/source/src/gpumd`
- NEP89: `/gs/fs/tgj-26ICP/uf03782/yang/li-research/models/nep89/nep/nep89_20250409/nep89_20250409.txt`
- 同じ tgj-26ICP group のアカウントが対象です。他 group のアカウントにはアクセスを保証しません。
- 共用バイナリとモデルは参照専用です。変更・削除・上書きしないでください。提供側パスを移動/削除すると利用できなくなります。
- 元素を扱えることと、その材料・高温・非晶状態でモデル精度が検証されていることは異なります。
