#coding:utf-8
#パラメータ設定ファイル
#Akira Taniguchi 2016/05/31-2016/11/30-
import numpy as np

####################パラメータ####################
D = 25 #40#8#10             #全データ数
num_iter = 200     #学習のイテレーション回数

CNNmode = 2     #CNN→PCA(2)・特徴抽出をCNNにする（１）・SIFTにする（０）・DSIFTのBoFにする（-1）
DATAnum = 0#1     #ファイル名にデータ数が入るバージョン「データ数４０」(1),入らない旧版「データ数２５」（０）

if CNNmode == 0:
  if DATAnum == 0:
    Descriptor = "SIFT_BoF"
  elif DATAnum == 1: 
    Descriptor = "SIFT_BoF_"+str(D)  #データ数が入るバージョン
  k_img = 100
elif CNNmode == -1:
  Descriptor = "DSIFT_BoF"
  k_img = 100
elif CNNmode == 1:
  Descriptor = "CNN_fc6"
  k_img = 4096  ##高次元すぎてGMMが動かない
elif CNNmode == 2:
  if DATAnum == 0:
    Descriptor = "CNN_PCA"
  elif DATAnum == 1: 
    Descriptor = "CNN_PCA_"+str(D)  #データ数が入るバージョン
  k_img = 65

k_sift = k_img   #ｋ−meansのkの値
#k_cnn = k_sift
k_rgb  = 10


nonpara = 1        #Nonparametric Bayes method (ON:1,OFF:0)
if nonpara == 1:
  Ka = 10 #5#4                  # the number of action categories
  Kp = 10 #5#4                  # the number of position categories
  Ko = 10 #5#3                  # the number of object categories
  Kc = 10 #5#3                  # the number of color categories
  alpha_a = 1.0#2.0 #1.0            #アクションカテゴリの混合分布のハイパーパラメータ
  alpha_p = 1.0#2.0 #1.0            #位置カテゴリの混合分布のハイパーパラメータ
  alpha_o = 1.0#2.0 #1.0            #物体カテゴリの混合分布のハイパーパラメータ
  alpha_c = 1.0#2.0 #1.0            #色カテゴリの混合分布のハイパーパラメータ
elif nonpara == 0:
  Ka = 5#4                  # the number of action categories
  Kp = 5#4                  # the number of position categories
  Ko = 5#3                  # the number of object categories
  Kc = 5#3                  # the number of color categories
  alpha_a = 1.0            #アクションカテゴリの混合分布のハイパーパラメータ
  alpha_p = 1.0            #位置カテゴリの混合分布のハイパーパラメータ
  alpha_o = 1.0            #物体カテゴリの混合分布のハイパーパラメータ
  alpha_c = 1.0            #色カテゴリの混合分布のハイパーパラメータ
L = Ka + Kp + Ko + Kc   # the number of word distributions

modality = ["a","p","o","c"]
dict = {"a":0, "p":Ka, "o":Ka+Kp, "c":Ka+Kp+Ko}   #各モダリティのindexにキーを足すとΘのindexになる

##初期(ハイパー)パラメータ
gamma = 0.1#.0             #単語分布のハイパーパラメータ
#alpha_a = 5.0 #1.0            #アクションカテゴリの混合分布のハイパーパラメータ
#alpha_p = 5.0 #1.0            #位置カテゴリの混合分布のハイパーパラメータ
#alpha_o = 5.0 #1.0            #物体カテゴリの混合分布のハイパーパラメータ
#alpha_c = 5.0 #1.0            #色カテゴリの混合分布のハイパーパラメータ

dim_a = 4+34#+#2#100                        #ガウス分布の次元数
k0a = 1e-3                         #μのパラメータ
m0a = np.zeros(dim_a)              #μのパラメータnp.array([[0.0] for dim in xrange(dim_a)])
V0a = np.eye(dim_a)*0.01#01                #Σのパラメータ(V0a=n0a*Sig0a)
n0a = dim_a + 2.0                  #Σのパラメータ(>=dim_a)
#beta_a = [k0a, m0a, V0a, n0a]             #アクションカテゴリのガウス分布のハイパーパラメータ

dim_p = 2#3                          #ガウス分布の次元数
k0p = 1e-3                         #μのパラメータ
m0p = np.zeros(dim_p)              #μのパラメータ
V0p = np.eye(dim_p)*0.01#01                #Σのパラメータ
n0p = dim_p + 2.0                  #Σのパラメータ(>=dim_p)
#beta_p = [k0p, m0p, V0p, n0p]             #位置カテゴリのガウス分布のハイパーパラメータ

dim_o = k_sift#100                        #ガウス分布の次元数
k0o = 1e-3                         #μのパラメータ
m0o = np.zeros(dim_o)              #μのパラメータ
V0o = np.eye(dim_o)*0.01#01                #Σのパラメータ
n0o = dim_o + 2.0                  #Σのパラメータ(>=dim_o)
#beta_o = [k0o, m0o, V0o, n0o]             #物体カテゴリのガウス分布のハイパーパラメータ

dim_c = k_rgb#100                        #ガウス分布の次元数
k0c = 1e-3                         #μのパラメータ
m0c = np.zeros(dim_c)              #μのパラメータ
V0c = np.eye(dim_c)*0.01#01                #Σのパラメータ
n0c = dim_c + 2.0                  #Σのパラメータ(>=dim_c)
#beta_c = [k0c, m0c, V0c, n0c]             #色カテゴリのガウス分布のハイパーパラメータ

#ガウスの初期値のスケール
mu_a_init  = [0,1]#[0,1]      #[最小値,最大値]
sig_a_init = 0.05 

mu_p_init  = [-0.5,0.5]
sig_p_init = 0.05#10.0 

mu_o_init  = [0,1]#[0,1]
sig_o_init = 0.05#1.0 

mu_c_init  = [0,1]#[0,1]
sig_c_init = 0.05#1.0 


##latticelmパラメータ
#knownn = [2,3,4] #[3]#         #言語モデルのn-gram長 (3)
#unkn = [3,4] #[3]#            #綴りモデルのn-gram長 (3),5
#annealsteps = [3,5,10]    #焼き鈍し法のステップ数 (3)
#anneallength = [5,10,15]  #各焼き鈍しステップのイタレーション数 (5)


##相互推定に関するパラメータ
#sample_num = len(knownn)*len(unkn)  #取得するサンプル数
#ITERATION = 10  #相互推定のイテレーション回数

##単語の選択の閾値
#threshold = 0.01


Plot = 2000#1000  #位置分布ごとの描画の点プロット数

#N_best_number = 1 #n-bestのnをどこまでとるか（n<=10）

####################ファイル####################
datafolder =  "/home/akira/Dropbox/iCub/iCub/datadump/" #"./../datadump/"#  ##"/home/icub/Desktop/Akira/iCub/datadump/" #
#win:相対パス、ubuntu:絶対パス

#speech_folder = "/home/*/Dropbox/Julius/directory/CC3Th2/*.wav" #*.wav" #音声の教示データフォルダ(Ubuntuフルパス)
#data_name = 'datah.csv'      # 'test000' #位置推定の教示データ(./../sampleフォルダ内)
#lang_init = 'phonemes.htkdic' #  'web.000.htkdic' #初期の単語辞書（./lang_mフォルダ内）


#map_data : ./jygame/__inti__.py 

#correct_Ct = 'Ct_correct.csv'  #データごとの正解のCt番号
#correct_data = 'TAMD1_human.txt'  #データごとの正解の文章（単語列、区切り文字つき）(./data/)
#correct_name = 'name_correct.csv'  #データごとの正解の場所の名前（音素列）

