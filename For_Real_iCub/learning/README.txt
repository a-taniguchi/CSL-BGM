//////////////////////////////////////
real iCub data用プログラム群に関するREADME
learning program
Akira Taniguchi 2016/08/21(for simulator)->2016/11/30(変更・対応付け未確認)
//////////////////////////////////////

[folder]
/data/
テスト実行用の学習データを保存していた。
現在は不使用。

/sankou/
プログラム作成時に参考にした他プログラム

/torioki/
学習用プログラムの別バージョン（比較用の別手法）を保存

[file]

__init__.py：学習用のパラメータの初期値を設定するファイル
action.py：アクション実験用プログラム（学習済みファイルと単語データから行動を生成する）
actiondatacollector.py：learn.pyを実行する前に、iCub_SIMのdaumpファイルからアクションデータを学習用データとして抽出するプログラム。
ARI.py：学習されたデータの要素ごとのカテゴリ結果と真の（人間の）カテゴリ結果のARIを計算する
ARI_Fd.py:
ARI_attention.py：Attentionした物体のみに関するARIを計算する
CNN_feature.py：物体画像ファイルからCNN特徴量を取り出すプログラム
CNNPCA_action.py：アクション生成タスク用のCNN-PCA特徴を抽出するプログラム
dsift.py：DSIFTを抽出するプログラム
learn.py：学習用プログラム。ギブスサンプリングを実行する。
meanARI.py：各試行ごとのARIを読み込み、平均値を出す
mearnARI_attention.py：Attention 物体のみのARIの平均を出す
PCA.py：CNN特徴をPCAで低次元化する（使用しているsklearn.decompositionの都合上、指定した次元数より少ない次元数になる場合がある）
PCA_rename.py:(データ数ごとにファイル名が異なるバージョン)
plot_gmm.py：位置カテゴリのガウス分布をプロットするプログラム
sift.py：SIFTとRGB特徴を抽出する
sift_action.py：アクション生成タスク用SIFT抽出し、k-meansでBOWを得るプログラム（？）
sift_read_kmeans.py：画像からSIFT→k-meansしてBOWを得るブログラム（？）

actionSelectObject_real.py : 物体選択だけのためのプログラム


[実験実行手順]
1.datadumpフォルダにデータを用意する
2.__init__.pyファイルのパラメータを設定する
3.画像特徴を抽出する。（CNN_feature.py and sift_rename.py）
4.CNN4096次元データの場合、PCAで低次元化する。（PCA_rename.py）
5.動作データの変換処理を行う。（actiondatacollector.py）
6.単語データを用意する。改行コードはLinux用のLFのみにしておくこと。（ts_words.csv）
6.学習（learn.py）

[物体選択(actionSelectObject_real.py)]
python ./learning/action_real.py $folder $bun $trial $action
folder="ts"
bun="${folder}(${sn}-${en})"
trial="cnnpca006"
