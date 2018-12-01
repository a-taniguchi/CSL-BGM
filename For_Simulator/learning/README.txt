//////////////////////////////////////
README file for learning programs
                         in simulator
Author: Akira Taniguchi 
2016/08/21 (Japanese version)
2018/12/01 (English version)
//////////////////////////////////////

[Folder]
none.

[Files]
ARI.py: Calculate the ARI value of categorization result for each element of learned data and true (human) categorization result for evaluation
ARI10.py: Calculate the ARI value for 10 trials
ARI10_Fd.py: Calculate the ARI value between categorization results of Fd for 10 trials
ARI_Fd.py: Calculate the ARI value between categorization results of Fd (Estimated sensory-channel for each word)
CNNPCA_action.py: Program for extracting CNN-PCA features for action generation task
CNNPCA_description.py: Program for extracting CNN-PCA features for description task
CNN_feature.py: Program for extracting CNN feature vector from object image file
PCA.py: Reduce dimensions of CNN features with PCA (due to the sklearn.decomposition being used, there may be a smaller number of dimensions than the specified number of dimensions)
PCA_rename.py: (Version with different file names for each number of data)
README.txt: This file
__init__.py: File to set the initial values ​​of learning parameters
__init__for_action.py: File to set the initial values ​​of parameters for action generation task
action.py: Action experiment program (generate actions from learned files and word data)
actionSeparate.py: 
actiondatacollector.py: Before executing learn.py, it extracts action data as learning data from dump file of iCub_SIM.


dsift.py: a program to extract DSIFT
learn.py: Learning program. Perform Gibbs sampling.
mean ARI.py: Read ARI for each trial and give an average value
mearnARI_attention.py: Average of ARI of only attention object

plot_gmm.py: A program for plotting the Gaussian distribution of the position category (error occurs in NPB version)
plot_gmm2.py: Gaussian distribution of position category is elliptically drawn program (error occurs in NPB version)
plot_gmm_nd.py: Program for plotting Gaussian distribution of position category
plot_gmm2_nd.py: Gaussian distribution of position category is elliptical drawing program (weight of mixture ratio can not be considered?)
sift.py: extract SFT and RGB features
sift_action.py: SIFT for action generation task and program for obtaining BOW with k-means (?)
sift_read_kmeans.py: Program for obtaining BOW by SIFT → k-means from the image (?)

description.py: Program for Action description task. making.

[Experiment execution procedure]
1. Prepare the data in the datadump folder
2. Set the parameters and PATH in the __init__.py file
Prepare 2-1.word file (testss_word.csv)
3. Extract image features. (CNN_feature.py and sift_rename.py)
4. For CNN 4096 dimensional data, PCA reduces the dimension. (PCA_rename.py)
5. Perform conversion data conversion processing. (Actiondatacollector.py)
5. Learning (learn.py)

__init__.py：学習用のパラメータの初期値を設定するファイル
action.py：アクション実験用プログラム（学習済みファイルと単語データから行動を生成する）
actiondatacollector.py：learn.pyを実行する前に、iCub_SIMのdaumpファイルからアクションデータを学習用データとして抽出するプログラム。
ARI.py：学習されたデータの要素ごとのカテゴリ結果と真の（人間の）カテゴリ結果のARIを計算する
ARI_attention.py：Attentionした物体のみに関するARIを計算する
CNN_feature.py：物体画像ファイルからCNN特徴量を取り出すプログラム
CNNPCA_action.py：アクション生成タスク用のCNN-PCA特徴を抽出するプログラム
dsift.py：DSIFTを抽出するプログラム
learn.py：学習用プログラム。ギブスサンプリングを実行する。
meanARI.py：各試行ごとのARIを読み込み、平均値を出す
mearnARI_attention.py：Attention 物体のみのARIの平均を出す
PCA.py：CNN特徴をPCAで低次元化する（使用しているsklearn.decompositionの都合上、指定した次元数より少ない次元数になる場合がある）
PCA_rename.py:(データ数ごとにファイル名が異なるバージョン)
plot_gmm.py：位置カテゴリのガウス分布を点プロットするプログラム(NPB版だとエラーが出る)
plot_gmm2.py:位置カテゴリのガウス分布を楕円で描画プログラム(NPB版だとエラーが出る)
plot_gmm_nd.py：位置カテゴリのガウス分布を点プロットするプログラム
plot_gmm2_nd.py:位置カテゴリのガウス分布を楕円で描画プログラム(混合比の重みが考慮できていない？)
sift.py：SIFTとRGB特徴を抽出する
sift_action.py：アクション生成タスク用SIFT抽出し、k-meansでBOWを得るプログラム（？）
sift_read_kmeans.py：画像からSIFT→k-meansしてBOWを得るブログラム（？）

description.py:Action description task用プログラム。作成中。

[実験実行手順]
1.datadumpフォルダにデータを用意する
2.__init__.pyファイルのパラメータを設定する
2-1.wordファイルを用意する(testss_word.csv)
3.画像特徴を抽出する。（CNN_feature.py and sift_rename.py）
4.CNN4096次元データの場合、PCAで低次元化する。（PCA_rename.py）
5.動作データの変換処理を行う。（actiondatacollector.py）
5.学習（learn.py）




