#! /usr/bin/env python
# -*- coding: utf-8 -*-
#CNNの特徴量4096次元そのまま.k-meansはデータ数が稼げないのでしても不毛
#Akira Taniguchi 2016/06/21-07/25
import sys, os, os.path, caffe
import cv2
import numpy as np
#from sklearn.cluster import KMeans
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


trialname = raw_input("trialname?(folder) >")
start = raw_input("start number?>")
end   = raw_input("end number?>")

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

descriptors = []
descriptors_bgr = []
object_feature = [ [] for j in range(Data) ]
object_color   = [ [] for j in range(Data) ]

foldername = datafolder + trialname
#フォルダ作成
#Makedir( foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")" )


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



