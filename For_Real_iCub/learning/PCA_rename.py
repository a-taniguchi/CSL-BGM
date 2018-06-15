#! /usr/bin/env python
# -*- coding: utf-8 -*-
#CNN特徴量4096次元をPCAで次元圧縮するプログラム(データ数ごとにファイル名が異なるバージョン)
#http://kensuke-mi.xyz/kensuke-mi_diary/2014/09/pca.html
#データはnumpy.array
#Akira Taniguchi 2016/07/24-2016/10/26-
import sys, os, os.path
import numpy as np
from sklearn.decomposition import PCA
from __init__ import *

def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass

trialname = raw_input("trialname?(folder) >")
start = raw_input("start number?>")
end   = raw_input("end number?>")

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname
#フォルダ作成
Makedir( foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")" )


dim=k_img
data = []

for trial in range(Data):
  filename = foldername+str(trial+sn).zfill(3)+'/'
  
  #物体数の読み込み
  gyo = 0
  for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1    
  
  #Read CNN_fc6 data for each object
  for object in range(object_num):
    for line in open(filename+'image/object_CNN_fc6_'+str(object+1).zfill(2)+'.csv','r'):
      itemList = line[:-1].split(',')
      item = []
      for i in xrange(len(itemList)):
        item = item + [float(itemList[i])]
      data = data + [item]
    

data = np.array(data)
print data
print "PCA run dim=",dim
pca=PCA(n_components=dim)
pca.fit(data)
result=pca.transform(data)

print result
print pca.components_.shape

min = np.min(result)
max = np.max(result)

#正規化する
for i in xrange(len(result)):
  for j in xrange(len(result[i])):
    result[i][j] = (result[i][j] - min) / (max - min)

print result

#Write PCA data for each object
i = 0
for trial in range(Data):
  filename = foldername+str(trial+sn).zfill(3)+'/'
  #物体数の読み込み
  gyo = 0
  for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1  

  for object in range(object_num):
    fp = open(filename+'image/object_CNN_PCA_'+str(Data)+'_'+str(object+1).zfill(2)+'.csv','w')
    for j in xrange(dim):
      fp.write(str(result[i][j])+",")
    fp.close()
    i = i + 1
    


#Write PCA data
fp = open(foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"+'/PCA'+str(Data)+'.csv','w')
fp.write(repr(min)+'\n')
fp.write(repr(max)+'\n')
#for i in range(len(cluster)):
#  fp.write(repr(i)+',')
#  for j in range(len(cluster[i])):
#    fp.write(repr(cluster[i][j])+',')
#  fp.write('\n')
fp.close()



#data=np.loadtxt("data.csv", delimiter=",")

#np.savetxt("result.csv", result, delimiter=",")
