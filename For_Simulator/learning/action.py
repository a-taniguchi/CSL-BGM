# -*- coding: utf-8 -*-
#action and attention
#python ./learning/action.py '$folder' '$bun' '$trial' '$action
#Akira Taniguchi 2016/06/22-

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

param = sys.argv

#datafolder =  "/home/akira/Dropbox/iCub/datadump/" #"./../datadump/"#

trialname = param[1] #"testss"#raw_input("trialname?(folder) >")
foldername = datafolder + param[2] #datafolder + trialname+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"
#start = "1"#raw_input("start number?>")
#end   = "20"#raw_input("end number?>")
learningname = param[3] #raw_input("learning trial name?>")#"001"#
actionname = param[4]

#sn = int(start)
#en = int(end)
#Data = int(en) - int(sn) +1
Data = D

filename = foldername + '/' + learningname + '/' + actionname + '/'

#init = foldername + '/' + learningname + '/init'
#sys.path.append(init)
#from __init__ import *

####単語データの読み込み
N = 0
w_dn = []
#d = 0
for line in open(filename + 'words.txt', 'r'):
  itemList = line[:-1].split(',')
  for i in xrange(len(itemList)):
    if itemList[i] != '':
      w_dn = w_dn + [str(itemList[i])]
      N = N + 1
  #d = d + 1

#N = 4  #test
#w_dn = ["grasp", "front", "blue", "box"]  #test
print w_dn


####学習済みデータの読み込み
#za = [i for in xrange(Ka)] #[ int(uniform(0,Ko)) for d in xrange(D) ]
#zp = [ [ int(uniform(0,Kp)) for m in xrange(M[d]) ] for d in xrange(D) ]
#zo = [ [ int(uniform(0,Ko)) for m in xrange(M[d]) ] for d in xrange(D) ]
#zc = [ [ int(uniform(0,Kc)) for m in xrange(M[d]) ] for d in xrange(D) ]

#Fd = [ Sample_Frame(N[d]) for d in xrange(D)] #初期値はランダムに設定("a","p","o","c")

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
argmax_Ad = 0
argmax_zak = 0
argmax_a_d = []

#a_d  = []
o_dm = []
c_dm = []
p_dm = []


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


####物体特徴量抽出
for m in xrange(M):
  ##物体情報 BoF(SIFT)orCNN特徴の読み込み
  for line in open(filename + 'image/object_' + Descriptor + '_'+str(m+1).zfill(2)+'.csv', 'r'):
    itemList = line[:-1].split(',')
    #print c
    #W_index = W_index + [itemList]
    for i in xrange(len(itemList)):
      if itemList[i] != '':
        #print c,i,itemList[i]
        o_dm[m][i] = float(itemList[i])
        #if min_o > o_dm[m][i]:
        #  min_o = o_dm[m][i]
        #if max_o < o_dm[m][i]:
        #  max_o = o_dm[m][i]
        
  if (CNNmode == 0) or (CNNmode == -1):
    #BoFのカウント数を正規化
    sum_o_dm = sum(o_dm[m])
    if sum_o_dm != 0:
      for i in xrange(len(o_dm[m])):
        o_dm[m][i] = o_dm[m][i] / sum_o_dm
  #print o_dm[m], sum(o_dm[m])
  
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


####アクション選択の計算
Ad_candidate = [m for m in xrange(M)]
za_candidate = [k for k in xrange(Ka)]
CDP = [[pi_a[k] / float(M) for m in xrange(M)] for k in xrange(Ka)] #candidate propbability
#F_temp = [f for f in itertools.permutations(modality,N)]  ##モダリティの順列組み合わせ

for c in list(itertools.product(za_candidate, Ad_candidate)):
    #print c[0],c[1]
    temp_ocpw = 0.0
    logpdf = []
    for zok in xrange(Ko):
      logpdf += [multivariate_normal.logpdf(o_dm[c[1]], mean=Mu_o[zok], cov=Sig_o[zok])]
    #print logpdf
    max_log = np.max(logpdf)
    for zok in xrange(Ko):
      temp_cpw = 0.0
      for zck in xrange(Kc):
        temp_pw = 0.0
        for zpk in xrange(Kp):
          temp_w = 0.0
          for F_temp in itertools.permutations(modality,N):
            #print c[0],zok,zck,zpk,F_temp
            temp = 1e+1#00#1.0
            for n in xrange(N):
              #print i,n,N[d],M[d]
              if F_temp[n] == "a":
                temp = temp * theta[c[0]           ][W_list.index(w_dn[n])]
              if F_temp[n] == "p":
                temp = temp * theta[zpk + dict["p"]][W_list.index(w_dn[n])]
              if F_temp[n] == "o":
                temp = temp * theta[zok + dict["o"]][W_list.index(w_dn[n])]
              if F_temp[n] == "c":
                temp = temp * theta[zck + dict["c"]][W_list.index(w_dn[n])]
            temp_w = temp_w + temp
            #print temp,temp_w
          temp_pw = temp_pw + multivariate_normal.pdf(p_dm[c[1]], mean=Mu_p[zpk], cov=Sig_p[zpk]) * pi_p[zpk] * temp_w
          #print temp_pw,temp_w
        temp_cpw = temp_cpw + multivariate_normal.pdf(c_dm[c[1]], mean=Mu_c[zck], cov=Sig_c[zck]) * pi_c[zck] * temp_pw
      
      temp_ocpw = temp_ocpw + exp(multivariate_normal.logpdf(o_dm[c[1]], mean=Mu_o[zok], cov=Sig_o[zok]) - max_log + log(pi_o[zok]) + log(temp_cpw))
      #print "G",multivariate_normal.logpdf(o_dm[c[1]], mean=Mu_o[zok], cov=Sig_o[zok]) * pi_o[zok]
    CDP[c[0]][c[1]] = CDP[c[0]][c[1]] * temp_ocpw
    #print "b",c[0],c[1]+1,CDP[c[0]][c[1]]
    
    mnotAd = [i for i in xrange(M)]
    mnotAd.pop(c[1])
    temp = 1e+1#00#1.0
    for m2 in mnotAd:
      logpdf = []
      for zok in xrange(Ko):
        logpdf += [multivariate_normal.logpdf(o_dm[m2], mean=Mu_o[zok], cov=Sig_o[zok])]
      #print logpdf
      max_log = np.max(logpdf)
      temp_o = 0.0
      for zok in xrange(Ko):
        temp_o = temp_o + exp(multivariate_normal.logpdf(o_dm[m2], mean=Mu_o[zok], cov=Sig_o[zok]) - max_log + log(pi_o[zok]))
      temp_p = 0.0
      for zpk in xrange(Kp):
        temp_p = temp_p + multivariate_normal.pdf(p_dm[m2], mean=Mu_p[zpk], cov=Sig_p[zpk]) * pi_p[zpk]
      temp_c = 0.0
      for zck in xrange(Kc):
        temp_c = temp_c + multivariate_normal.pdf(c_dm[m2], mean=Mu_c[zck], cov=Sig_c[zck]) * pi_c[zck]
      temp = temp * temp_o * temp_p * temp_c #* float(1e+10)
      #print temp,temp_o,temp_p,temp_c
    CDP[c[0]][c[1]] = CDP[c[0]][c[1]] * temp #* float(1e+10)
    print c[0],c[1]+1,CDP[c[0]][c[1]]

"""
for c in list(itertools.product(za_candidate, Ad_candidate)):
    #print c[0],c[1]
    temp_ocpw = 0.0
    for F_temp in itertools.permutations(modality,N):
      temp_cpw = 0.0
      for zck in xrange(Kc):
        temp_pw = 0.0
        for zpk in xrange(Kp):
          temp_w = 0.0
          for zok in xrange(Ko):
            #print c[0],zok,zck,zpk,F_temp
            temp = 1.0
            for n in xrange(N):
              #print i,n,N[d],M[d]
              if F_temp[n] == "a":
                temp = temp * theta[c[0]           ][W_list.index(w_dn[n])]
              if F_temp[n] == "p":
                temp = temp * theta[zpk + dict["p"]][W_list.index(w_dn[n])]
              if F_temp[n] == "o":
                temp = temp * theta[zok + dict["o"]][W_list.index(w_dn[n])]
              if F_temp[n] == "c":
                temp = temp * theta[zck + dict["c"]][W_list.index(w_dn[n])]
            temp_w = temp_w + multivariate_normal.pdf(o_dm[c[1]], mean=Mu_o[zok], cov=Sig_o[zok]) * pi_o[zok] * temp
            #print temp,temp_w
          temp_pw = temp_pw + multivariate_normal.pdf(p_dm[c[1]], mean=Mu_p[zpk], cov=Sig_p[zpk]) * pi_p[zpk] * temp_w
          #print temp_pw,temp_w
        temp_cpw = temp_cpw + multivariate_normal.pdf(c_dm[c[1]], mean=Mu_c[zck], cov=Sig_c[zck]) * pi_c[zck] * temp_pw
      temp_ocpw = temp_ocpw + temp_cpw
    CDP[c[0]][c[1]] = CDP[c[0]][c[1]] * temp_ocpw
    print c[0],c[1],temp_ocpw
"""

####計算したすべての候補(Ad,za)の値を保存
fp = open(filename + 'candidate.csv', 'w')
#fp.write('theta\n')
for k in xrange(Ka):
  for m in xrange(M):
    fp.write(repr(CDP[k][m])+',')
  fp.write('\n')
fp.close()


###最大の要素を探す
max = np.array(CDP).max()
for k in xrange(Ka):
  for m in xrange(M):
    if max == CDP[k][m]:
      argmax_Ad = m
      argmax_zak = k

#argmax_Ad = 0
#argmax_za = 0
argmax_a_d = Mu_a[argmax_zak]
#print Mu_a

#正規化を元に戻す
min_a = [0.0, 0.0, 0.0]
max_a = [0.0, 0.0, 0.0]
i = 0
for line in open(foldername +'/' + learningname + '/' + trialname + '_' + learningname + '_data.csv', 'r'):
  itemList = line[:-1].split(',')
  if i == 0:
    min_a = [float(itemList[0]), float(itemList[1]), float(itemList[2])]
  elif i == 1:
    max_a = [float(itemList[0]), float(itemList[1]), float(itemList[2])]
  i = i + 1

for dim in xrange(3):
  argmax_a_d[dim] = argmax_a_d[dim] * (max_a[dim] - min_a[dim]) + min_a[dim]

print argmax_zak, argmax_Ad+1, argmax_a_d

####ファイル出力
fp = open(filename + 'argmax_ZAAD.csv', 'w')
fp.write(repr(argmax_zak) + ',' + repr(argmax_Ad) + '\n')
#fp.write('\n')
fp.close()

fp = open(filename + 'argmax_a_d.csv', 'w')
for dim in xrange(dim_a):
  fp.write(repr(argmax_a_d[dim]) + ',')
fp.write('\n')
fp.close()

i = 0
obj_point = []#["" for m in range(M)]
for line in open(filename + 'object_cam_point.txt', 'r'):
  #itemList = line[:-1].split(',')
  if i == 0:
    M = int(line)
  elif i <= M+1 and i != 1:
    obj_point = obj_point + [line]
  i = i + 1
    
fp = open(filename + 'object_cam_point.txt', 'w')
fp.write(repr(M)+'\n')
fp.write(repr(argmax_Ad+1)+'\n')
for m in xrange(M):
  fp.write(obj_point[m])
fp.close()

i = 0
obj_point = []#["" for m in range(M)]
for line in open(filename + 'object_center.txt', 'r'):
  #itemList = line[:-1].split(',')
  if i == 0:
    M = int(line)
  elif i <= M+1 and i != 1:
    obj_point = obj_point + [line]
  i = i + 1
    
fp = open(filename + 'object_center.txt', 'w')
fp.write(repr(M)+'\n')
fp.write(repr(argmax_Ad+1)+'\n')
for m in xrange(M):
  fp.write(obj_point[m])
fp.close()
