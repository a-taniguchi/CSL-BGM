# -*- coding: utf-8 -*-
#action and attention
#python ./learning/action.py '$folder' '$bun' '$trial' '$action
#Akira Taniguchi 2016/06/22-2017/03/17

import cv2
import os
import sys
import collections
import itertools
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from numpy.random import multinomial,uniform,dirichlet
from scipy.stats import multivariate_normal,invwishart,rv_discrete
from math import pi as PI
from math import cos,sin,sqrt,exp,log,fabs,fsum,degrees,radians,atan2
from __init__ import *

def explain_keypoint(kp):
    print 'angle:', kp.angle
    print 'class_id:', kp.class_id
    print 'octave (image scale where feature is strongest):', kp.octave
    print 'pt (x,y):', kp.pt
    print 'response:', kp.response
    print 'size:', kp.size

def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass

#param = sys.argv
#datafolder =  "/home/akira/Dropbox/iCub/datadump/" #"./../datadump/"#
trialname = "testss" #raw_input("trialname?(folder) >")#param[1] #"testss"#
start = "1"#raw_input("start number?>")
end   = raw_input("end number?>")
sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1
if Data == 20:
  DATAnum = 0     #ファイル名にデータ数が入るバージョン「データ数20以外」(1),入らない旧版「データ数20」（０）
else:
  DATAnum = 1     #ファイル名にデータ数が入るバージョン「データ数20以外」(1),入らない旧版「データ数20」（０）
if DATAnum == 0:
    Descriptor = "CNN_PCA"
elif DATAnum == 1: 
    Descriptor = "CNN_PCA_"+str(Data)  #データ数が入るバージョン

foldername = datafolder + trialname + "("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")" #datafolder + param[2] #
print foldername
learningname = raw_input("learning trial name?>")
descriptionname = raw_input("description trial name?>")#"001"#
#actionname = param[4]

filename = datafolder + descriptionname + '/'




####学習済みデータの読み込み
W_list = []
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_W_list.csv', 'r'):
  line = line.replace("'", "")
  itemList = line[:-1].split(',')
  for i in xrange(len(itemList)):
    if itemList[i] != '':
      W_list = W_list + [itemList[i]]

#cw = collections.Counter(w_dn)
#W_list = list(cw)  ##単語のリスト
print W_list
W = len(W_list)  ##単語の種類数のカウント
theta = [ [0.0 for w in xrange(W)] for i in xrange(L) ] #indexと各モダリティーの対応付けはdictionary形式で呼び出す
i = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_theta.csv', 'r'):
  itemList = line[:-1].split(',')
  for w in xrange(len(theta[i])):
    theta[i][w] = float(itemList[w])
  i = i + 1

Mu_a  = [ np.array([0.0 for i in xrange(dim_a)]) for k in xrange(Ka) ]
Sig_a = [ np.eye(dim_a)*sig_a_init for k in xrange(Ka) ]
k = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Mu_a.csv', 'r'):
  itemList = line[:-1].split(',')
  for dim in xrange(len(Mu_a[k])):
    Mu_a[k][dim] = float(itemList[dim])
  k = k + 1
k = 0
dim1 = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Sig_a.csv', 'r'):
  itemList = line[:-1].split(',')
  if dim1 != dim_a:
    for dim2 in xrange(len(Sig_a[k][dim1])):
      Sig_a[k][dim1][dim2] = float(itemList[dim2])
    dim1 = dim1 + 1
  else:
    dim1 = 0
    k = k + 1

Mu_p  = [ np.array([0.0 for i in xrange(dim_p)]) for k in xrange(Kp) ]
Sig_p = [ np.eye(dim_p)*sig_p_init for k in xrange(Kp) ]
k = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Mu_p.csv', 'r'):
  itemList = line[:-1].split(',')
  for dim in xrange(len(Mu_p[k])):
    Mu_p[k][dim] = float(itemList[dim])
  k = k + 1
k = 0
dim1 = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Sig_p.csv', 'r'):
  itemList = line[:-1].split(',')
  if dim1 != dim_p:
    for dim2 in xrange(dim_p):
      Sig_p[k][dim1][dim2] = float(itemList[dim2])
    dim1 = dim1 + 1
  else:
    dim1 = 0
    k = k + 1

Mu_o  = [ np.array([0.0 for i in xrange(dim_o)]) for k in xrange(Ko) ]
Sig_o = [ np.eye(dim_o)*sig_o_init for k in xrange(Ko) ]
k = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Mu_o.csv', 'r'):
  itemList = line[:-1].split(',')
  for dim in xrange(len(Mu_o[k])):
    Mu_o[k][dim] = float(itemList[dim])
  k = k + 1
k = 0
dim1 = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Sig_o.csv', 'r'):
  itemList = line[:-1].split(',')
  if dim1 != dim_o:
    for dim2 in xrange(len(Sig_o[k][dim1])):
      Sig_o[k][dim1][dim2] = float(itemList[dim2])
    dim1 = dim1 + 1
  else:
    dim1 = 0
    k = k + 1

Mu_c  = [ np.array([0.0 for i in xrange(dim_c)]) for k in xrange(Kc) ]
Sig_c = [ np.eye(dim_c)*sig_c_init for k in xrange(Kc) ]
k = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Mu_c.csv', 'r'):
  itemList = line[:-1].split(',')
  for dim in xrange(len(Mu_c[k])):
    Mu_c[k][dim] = float(itemList[dim])
  k = k + 1
k = 0
dim1 = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_Sig_c.csv', 'r'):
  itemList = line[:-1].split(',')
  if dim1 != dim_c:
    for dim2 in xrange(len(Sig_c[k][dim1])):
      Sig_c[k][dim1][dim2] = float(itemList[dim2])
    dim1 = dim1 + 1
  else:
    dim1 = 0
    k = k + 1

pi_a = [ alpha_a for c in xrange(Ka)] #stick_breaking(gamma, L)#
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_pi_a.csv', 'r'):
  itemList = line[:-1].split(',')
  for k in xrange(Ka):
    pi_a[k] = float(itemList[k])
  
pi_p = [ alpha_p for c in xrange(Kp)] #stick_breaking(gamma, L)#
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_pi_p.csv', 'r'):
  itemList = line[:-1].split(',')
  for k in xrange(Kp):
    pi_p[k] = float(itemList[k])

pi_o = [ alpha_o for c in xrange(Ko)] #stick_breaking(gamma, L)#
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_pi_o.csv', 'r'):
  itemList = line[:-1].split(',')
  for k in xrange(Ko):
    pi_o[k] = float(itemList[k])

pi_c = [ alpha_c for c in xrange(Kc)] #stick_breaking(gamma, L)#
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_pi_c.csv', 'r'):
  itemList = line[:-1].split(',')
  for k in xrange(Kc):
    pi_c[k] = float(itemList[k])




####物体データの読み込み
M = 0
Ad = 0

a_d  = []
o_dm = []
c_dm = []
p_dm = []

min_a = [10,10,10]   #仮の初期値
max_a = [-10,-10,-10]  #仮の初期値
min_o = 10000
max_o = -10000

gyo = 0
##物体数Mの読み込み
for line in open(filename + 'object_center.txt','r'):
  if gyo == 0:
    M = int(line)
    o_dm = [ [ 0.0 for k in xrange(k_sift) ] for m in xrange(M) ]
    c_dm = [ [ 0.0 for k in xrange(k_rgb)  ] for m in xrange(M) ]
    p_dm = [ [ 0.0 for k in xrange(dim_p)  ] for m in xrange(M) ]
    #elif gyo == 1:
    #  Ad[d] = int(line)-1 #物体番号1からMを0からM-1にする
  elif gyo == 1:
    dummy = 0
    #print "if random_obj was changed, but no problem."
  else:
    itemList = line[:-1].split(',')
    #for i in xrange(len(itemList)):
    if itemList[0] != '':
      #物体座標p_dmの読み込み
      p_dm[int(itemList[0])-1] = [float(itemList[1]),float(itemList[2])]#,float(itemList[3])]
  gyo = gyo + 1


#動作データ読み込み
gyo = 0
#対象物体の座標、手先座標読み込み
for line in open(filename+'target_object.txt','r'):
        if gyo == 0:
          Ad = int(line)-1
        elif gyo == 1:
          itemList = line[:-1].split(',')
          obj_pos = np.array([float(itemList[0]),float(itemList[1]),float(itemList[2])])
        elif gyo == 2:
          itemList = line[:-1].split(',')
          enf_pos = np.array([float(itemList[0]),float(itemList[1]),float(itemList[2])])
        elif gyo == 4:
          randomove = float(line)
        gyo = gyo + 1
        
tmp = enf_pos - obj_pos #obj_pos - enf_pos
#if (d == 0):
gyo = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_data.csv', 'r'):
  itemList = line[:-1].split(',')
  if (gyo == 0):
    min_a = [float(itemList[0]),float(itemList[1]),float(itemList[2])]
  if (gyo == 1):
    max_a = [float(itemList[0]),float(itemList[1]),float(itemList[2])]
  gyo = gyo + 1

#min_a = #list(tmp)         
#max_a = #list(tmp)
print min_a,max_a
#for i in xrange(3):
#        if (min_a[i] > tmp[i]):
#           min_a[i]= tmp[i]
#        if (max_a[i] < tmp[i]):
#           max_a[i] = tmp[i]
a_d = list(tmp) + [randomove] #相対3次元位置、指の曲げ具合

gyo = 0
for line in open(filename+'action.csv','r'):
        itemList = line[:-1].split(',')
        
        if ("" in itemList):
          itemList.pop(itemList.index(""))
        #関節箇所ごとに最小値と最大値で正規化
        if(gyo == 1 or gyo == 7 or gyo == 10):
          for i in xrange(len(itemList)):
            if gyo == 1: #head
              min = [-40,-70,-55,-35,-50, 0]
              max = [ 30, 60, 55, 15, 50,90]
            elif gyo == 7: #right_arm
              min = [-95,    0,-37,15.5,-90,-90,-20,  0,9.6,  0,  0,  0,  0,  0,   0,  0]
              max = [ 10,160.8, 80, 106, 90,  0, 40, 60, 90, 90,180, 90, 180, 90,180,270]
            elif gyo == 10: #torso
              min = [-50,-30,-10]
              max = [ 50, 30, 70]
            if itemList[i] != '':
              #print d,itemList[i]
              a_d = a_d + [ (float(itemList[i])-min[i])/float(max[i]-min[i]) ]  #正規化して配列に加える	
        if(gyo == 13):
          tactile = [0.0 for i in xrange(len(itemList)/12)]
          for i in xrange(len(itemList)/12):
            #for j in xrange(12):
            #  print i*12+j
            tactile[i] = sum([float(itemList[i*12+j]) for j in xrange(12)])/float(255*12)  #正規化して12個の平均
        
        gyo = gyo + 1
a_d = a_d + tactile

print "a_d", a_d

####物体特徴量抽出
for m in xrange(M):
  ##物体情報 BoF(SIFT)orCNN特徴の読み込み
  for line in open(filename + 'image/object_' + Descriptor + '_'+str(m+1).zfill(2)+'.csv', 'r'):
    print filename + 'image/object_' + Descriptor + '_'+str(m+1).zfill(2)+'.csv'
    itemList = line[:-1].split(',')
    #print c
    #W_index = W_index + [itemList]
    for i in xrange(len(itemList)):
      if itemList[i] != '':
        #print c,i,itemList[i]
        o_dm[m][i] = float(itemList[i])
        if min_o > o_dm[m][i]:
          min_o = o_dm[m][i]
        if max_o < o_dm[m][i]:
          max_o = o_dm[m][i]
        
  if (CNNmode == 0) or (CNNmode == -1):
    #BoFのカウント数を正規化
    sum_o_dm = sum(o_dm[m])
    if sum_o_dm != 0:
      for i in xrange(len(o_dm[m])):
        o_dm[m][i] = o_dm[m][i] / sum_o_dm
  print o_dm[m], sum(o_dm[m])
  
  ##色情報 BoF(RGB)の読み込み
  if DATAnum == 0:
    for line in open(filename + 'image/object_RGB_BoF_'+str(m+1).zfill(2)+'.csv', 'r'):
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        if itemList[i] != '':
          #print c,i,itemList[i]
          c_dm[m][i] = float(itemList[i])
  elif DATAnum == 1:
    for line in open(filename + 'image/object_RGB_BoF_'+str(Data)+'_'+str(m+1).zfill(2)+'.csv', 'r'):
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        if itemList[i] != '':
          #print c,i,itemList[i]
          c_dm[m][i] = float(itemList[i])
  
  #BoFのカウント数を正規化
  sum_c_dm = sum(c_dm[m])
  if sum_c_dm != 0:
    for i in xrange(len(c_dm[m])):
      c_dm[m][i] = c_dm[m][i] / sum_c_dm
  #print c_dm[m], sum(c_dm[m])

##アクションデータの相対座標を正規化RuntimeWarning: invalid value encountered in double_scalars

a_d[0] = (a_d[0] - min_a[0]) / (max_a[0] - min_a[0])
a_d[1] = (a_d[1] - min_a[1]) / (max_a[1] - min_a[1])
a_d[2] = (a_d[2] - min_a[2]) / (max_a[2] - min_a[2])

#CNN特徴の正規化
if CNNmode == 1:
        for m in xrange(M):
          for i in xrange(dim_o):
            o_dm[m][i] = (o_dm[m][i] - min_o) / (max_o - min_o)


N = 4
argmax_w_dn = ["" for n in range(4)]
Fd = ["a","p","c","o"] #[ Sample_Frame(N[d]) for d in xrange(D)] 

####モダリティごとの単語選択の計算(Calculator of selection of words for each modality)
za_candidate = [k for k in xrange(Ka)]
zp_candidate = [k for k in xrange(Kp)]
zo_candidate = [k for k in xrange(Ko)]
zc_candidate = [k for k in xrange(Kc)]
CDPa = [0.0 for w in xrange(len(W_list))] #candidate propbability
CDPp = [0.0 for w in xrange(len(W_list))] #candidate propbability
CDPo = [0.0 for w in xrange(len(W_list))] #candidate propbability
CDPc = [0.0 for w in xrange(len(W_list))] #candidate propbability
#F_temp = [f for f in itertools.permutations(modality,N)]  ##モダリティの順列組み合わせ

for w in range(len(W_list)):
  #w_a_prob = 0.0
  logpdf = []
  for c in za_candidate:
    logpdf += [multivariate_normal.logpdf(a_d,      mean=Mu_a[c], cov=Sig_a[c])]
  print logpdf
  max_log = np.max(logpdf)
  print max_log
  for c in za_candidate:
    CDPa[w] += exp( multivariate_normal.logpdf(a_d,      mean=Mu_a[c], cov=Sig_a[c]) - max_log + log(pi_a[c]) + log(theta[c + dict["a"]][w]))
    #print "----------"
    #print multivariate_normal.logpdf(a_d,      mean=Mu_a[c], cov=Sig_a[c])
    #print log(pi_a[c]), log(theta[c + dict["a"]][w])
    #print "----------"
  for c in zp_candidate:
    CDPp[w] += multivariate_normal.pdf(p_dm[Ad], mean=Mu_p[c], cov=Sig_p[c]) * pi_p[c] * theta[c + dict["p"]][w]
  logpdf = []
  for c in zo_candidate:
    logpdf += [multivariate_normal.logpdf(o_dm[Ad], mean=Mu_o[c], cov=Sig_o[c])]
  print logpdf
  max_log = np.max(logpdf)
  print max_log
  for c in zo_candidate:
    CDPo[w] += exp( multivariate_normal.logpdf(o_dm[Ad], mean=Mu_o[c], cov=Sig_o[c]) - max_log + log(pi_o[c]) + log(theta[c + dict["o"]][w]) )
  for c in zc_candidate:
    CDPc[w] += multivariate_normal.pdf(c_dm[Ad], mean=Mu_c[c], cov=Sig_c[c]) * pi_c[c] * theta[c + dict["c"]][w]
  

####計算したすべての候補(Ad,za)の値を保存
fp = open(filename + 'Word_description_probability_'+ learningname +'.csv', 'w')
for w in xrange(len(W_list)):
    fp.write(W_list[w]+',')
fp.write('\n')
fp.write('a\n')
for w in xrange(len(W_list)):
    fp.write(repr(CDPa[w])+',')
fp.write('\n')
fp.write('p\n')
for w in xrange(len(W_list)):
    fp.write(repr(CDPp[w])+',')
fp.write('\n')
fp.write('o\n')
for w in xrange(len(W_list)):
    fp.write(repr(CDPo[w])+',')
fp.write('\n')
fp.write('c\n')
for w in xrange(len(W_list)):
    fp.write(repr(CDPc[w])+',')
fp.write('\n')
fp.close()

print "a",CDPa
print "p",CDPp
print "o",CDPo
print "c",CDPc

###最大の要素を探す ########Fd = ["a","p","c","o"] 
max_a = np.array(CDPa).max()
max_p = np.array(CDPp).max()
max_o = np.array(CDPo).max()
max_c = np.array(CDPc).max()
for w in xrange(len(W_list)):
    if max_a == CDPa[w]:
      argmax_w_dn[0] = W_list[w]
    if max_p == CDPp[w]:
      argmax_w_dn[1] = W_list[w]
    if max_c == CDPc[w]:
      argmax_w_dn[2] = W_list[w]
    if max_o == CDPo[w]:
      argmax_w_dn[3] = W_list[w]
print argmax_w_dn

####ファイル出力
fp = open(filename + 'argmax_w_dn_' + str(Data) + "_" + learningname +'.csv', 'w')
for n in xrange(len(argmax_w_dn)):
  fp.write(argmax_w_dn[n] + ',')
fp.write('\n')
fp.close()

p = os.popen( "cat " + filename + "argmax_w_dn_" + str(Data) + "_" + learningname + ".csv | text2wave -o " + filename + "speech_" + str(Data) + "_" + learningname + ".wav" )
p.close()



