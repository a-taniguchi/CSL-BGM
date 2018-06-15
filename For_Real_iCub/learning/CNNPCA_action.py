#! /usr/bin/env python
# -*- coding: utf-8 -*-
#画像からCNN特徴を抽出し、学習用データでトレーニングしたPCAで次元圧縮、正規化する
#画像からRGBを抽出し、学習済みk-meansでBoF化するプログラム
#http://kensuke-mi.xyz/kensuke-mi_diary/2014/09/pca.html
#Akira Taniguchi 2016/07/25-

import sys, os, os.path, caffe
import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from __init__ import *

def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass

#FULL PATH
MEAN_FILE = '/home/akira/Caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy'
MODEL_FILE = '/home/akira/Caffe/examples/imagenet/imagenet_feature.prototxt'
PRETRAINED = '/home/akira/Caffe/examples/imagenet/caffe_reference_imagenet_model'
LAYER = 'fc6wi'
INDEX = 4


param = sys.argv

trialname = param[1] #raw_input("trialname?(folder) >")
start = param[2] #raw_input("start number?>")
end   = param[3] #raw_input("end number?>")

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

learningname = param[4]
actionname = param[5]

foldername = datafolder + trialname + "("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"
filename = foldername + '/' + learningname + '/' + actionname + '/'

descriptors = []
descriptors_bgr = []
#object_feature = []
object_color   = []
object_feature = [ [] for j in range(Data) ]


#物体数の読み込み
gyo = 0
for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1    

for object in range(object_num):
    imgname = filename + 'image/object_' + str(object+1).zfill(2) + '.ppm' 
    print imgname  
    
    net = caffe.Classifier(MODEL_FILE, PRETRAINED)
    #caffe.set_phase_test()
    caffe.set_mode_cpu()
    net.transformer.set_mean('data', np.load(MEAN_FILE))
    #net.set_mean
    #net.set_raw_scale
    net.transformer.set_raw_scale('data', 255)
    net.transformer.set_channel_swap('data', (2,1,0))

    image = caffe.io.load_image(imgname)
    net.predict([ image ])
    feat = net.blobs[LAYER].data[INDEX].flatten().tolist()
    #print(','.join(map(str, feat)))
    fp = open(filename+'image/object_CNN_fc6_'+str(object+1).zfill(2)+'.csv','w')
    fp.write(','.join(map(str, feat)))
    fp.close()

    imgname_color = filename + 'image/obj_mask_' + str(object+1).zfill(2) + '.ppm' 
    print imgname_color  
    img_color = cv2.imread(imgname_color)

    ###color###
    img_bgr = cv2.split(img_color)
    print img_bgr
    # 複数色のチャンネルを分割して配列で取得
    # img_bgr[0] に青, img_bgr[1]に緑,img_bgr[2]に赤が入る。
    #fp = open(filename+'image/object_RGB_0'+repr(object+1)+'.csv','w')
    print len(img_bgr[0]),len(img_bgr[0][0])
    BGR = []
    for i in range(len(img_bgr[0])):
      for j in range(len(img_bgr[0][0])):
        bgr = [np.float32(img_bgr[0][i][j]),np.float32(img_bgr[1][i][j]),np.float32(img_bgr[2][i][j])]
        #print bgr
        if (bgr != [0,0,0]):
          BGR = BGR + [np.array(bgr)]
    #print BG
    #fp.write('\n')
    #fp.close()
    descriptors_bgr = descriptors_bgr + BGR
    #print descriptors_bgr
    object_color = object_color + [BGR]



#des = np.array(descriptors)
des_bgr = np.array(descriptors_bgr)

#学習データのCNN特徴を読み込んで、PCAにかける
foldername2 = datafolder + trialname

dim=k_img
data = []

for trial in range(Data):
  filename2 = foldername2+str(trial+sn).zfill(3)+'/'
  
  #物体数の読み込み
  gyo = 0
  for line in open(filename2 + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1    
  
  #Read CNN_fc6 data for each object
  for object in range(object_num):
    for line in open(filename2+'image/object_CNN_fc6_'+str(object+1).zfill(2)+'.csv','r'):
      itemList = line[:-1].split(',')
      item = []
      #print len(itemList)#,itemList
      for i in xrange(len(itemList)):
        item = item + [float(itemList[i])]
      data = data + [item]
    
data = np.array(data)
print data
print "PCA run dim=",dim
pca=PCA(n_components=dim)
pca.fit(data)
#result=pca.transform()


#正規化用の最大値と最小値の読み込み
min = 0.0
max = 0.0
#cluster = [[] for k in range(k_sift)]
i = 0
for line in open(foldername +'/PCA.csv','r'):
  if i == 0:
    min = float(line)
    i = i + 1
  if i == 1:
    max = float(line)
  #itemList = line[:-1].split(',')
  #for i in range(len(itemList)):
    #if i != 0 and itemList[i] != "":
    #  cluster[int(itemList[0])] = cluster[int(itemList[0])] + [float(itemList[i])]
print min
print max
cluster_bgr = [[] for k in range(k_rgb)]
for line in open(foldername +'/RGB_kmeans.csv','r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if i != 0 and itemList[i] != "":
      cluster_bgr[int(itemList[0])] = cluster_bgr[int(itemList[0])] + [float(itemList[i])]
      

#物体数の読み込み
gyo = 0
for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1   


data2 = []
for object in range(object_num):
    fp  = open(filename+'image/object_' + str(Descriptor) + '_'+str(object+1).zfill(2)+'.csv','w')
    if DATAnum == 0:
      fp2 = open(filename+'image/object_RGB_BoF_'+str(object+1).zfill(2)+'.csv','w')
    elif DATAnum == 1:
      fp2 = open(filename+'image/object_RGB_BoF_'+str(D)+"_"+str(object+1).zfill(2)+'.csv','w')
    #CNN特徴の読み込み
    for line in open(filename+'image/object_CNN_fc6_'+str(object+1).zfill(2)+'.csv','r'):
      item = []
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        item = item + [float(itemList[i])]
      data2 = [item]
    
    data2 = np.array(data2)
    print len(data2[0])
    print data2
    result=pca.transform(data2)
    print result
    
    #正規化する
    #for i in xrange(len(result)):
    print len(result[0])
    for j in xrange(len(result[0])):
      result[0][j] = (result[0][j] - min) / (max - min)
    
    for j in xrange(dim):
      fp.write(str(result[0][j])+",")
    fp.close()
    #i = i + 1
    
    
    BoF2 = [0 for i in range(k_rgb)]
    for f in range(len(object_color[object])):
      min = 0  #saveing nearest class
      min_value = 0.0
      for i in range(len(cluster_bgr)):
        #dist = 0
        #for j in range(len(cluster_bgr[i])):
        #  tmp = cluster_bgr[i][j] - object_color[object][f][j]
        #  dist = dist + (tmp * tmp)
        dist = sum([(cluster_bgr[i][j] - object_color[object][f][j])**2 for j in range(len(cluster_bgr[i]))])
        if(i == 0):
          min_value = dist
        elif(min_value > dist):
          min_value = dist
          min = i
      BoF2[min] = BoF2[min] + 1
    
    for i in range(k_rgb):
      fp2.write(repr(BoF2[i])+',')
    fp2.write('\n')
    
    fp.close()
    fp2.close()


