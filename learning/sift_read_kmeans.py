# -*- coding: utf-8 -*-
#画像からSIFTとRGBを抽出し、k-meansでBoF化するプログラム
#参考：http://qiita.com/umekichinano/items/5e10e6b97b27f9575d6a#opencv3%E3%81%AE%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB--%E7%92%B0%E5%A2%83%E6%A7%8B%E7%AF%89
#Akira Taniguchi 2016/06/13-

import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
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

##########
print 'OpenCV Version (should be 3.1.0, with nonfree packages installed, for this tutorial):'
print cv2.__version__
##########



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
Makedir( foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")" )

for trial in range(Data):
  filename = foldername+str(trial+sn).zfill(3)+'/'

  #物体数の読み込み
  gyo = 0
  for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1    
    #    for i in xrange(len(itemList)):
    #      if itemList[i] != '':
    #        Ct = Ct + [int(itemList[i])]

  

  for object in range(object_num):
    imgname = filename + 'image/object_' + str(object+1).zfill(2) + '.ppm' 
    print imgname  
    img = cv2.imread(imgname)

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
    #print BGR
    #fp.write('\n')
    #fp.close()
    descriptors_bgr = descriptors_bgr + BGR
    #print descriptors_bgr
    object_color[trial] = object_color[trial] + [BGR]

    ###SIFT###
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
 
    sift = cv2.xfeatures2d.SIFT_create(contrastThreshold = 0.04, edgeThreshold = 10, sigma = 1.6-0.8)
    #nfeatures = 0, nOctaveLayers = 3,
    #kp = sift.detect(gray,None)
 
    kp, dsc = sift.detectAndCompute(gray,None)

    print len(dsc)#,sum(dsc)
    print dsc
    object_feature[trial] = object_feature[trial] + [dsc]
    for i in range(len(dsc)):
      descriptors = descriptors + [dsc[i]]

    #descriptors = descriptors + [dsc]

    #descriptors.append(dsc)
    #print descriptors 
    #print 'this is an example of a single SIFT keypoint:\n* * *'
    #explain_keypoint(kp[0])
    img = cv2.drawKeypoints(gray, kp, img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
    #cv2.imshow("img", img)
    imgname = filename + 'image/sift_0' + repr(object+1) + '.png'
    cv2.imwrite(imgname,img)

des = np.array(descriptors)
des_bgr = np.array(descriptors_bgr)

#print kp
print 'SIFT descriptors are vectors of shape', des[0].shape
  
#print len(des)
#print des

#print len(des_bgr)
#print des_bgr

#print sum(des[0][0])
#k=10
print "k-means(SIFT), K =",k_sift
print "k-means(RGB), K =",k_rgb

cluster = [[] for k in range(k_sift)]
for line in open(foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"+'/SIFT_kmeans.csv','r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if i != 0 and itemList[i] != "":
      cluster[int(itemList[0])] = cluster[int(itemList[0])] + [float(itemList[i])]

cluster_bgr = [[] for k in range(k_rgb)]
for line in open(foldername+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"+'/RGB_kmeans.csv','r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if i != 0 and itemList[i] != "":
      cluster_bgr[int(itemList[0])] = cluster_bgr[int(itemList[0])] + [float(itemList[i])]
      


#print k,len(cluster)
#print bow
print cluster

print np.sum(des),np.sum(cluster)


for trial in range(Data):
  filename = foldername+str(trial+sn).zfill(3)+'/'

  #物体数の読み込み
  gyo = 0
  for line in open(filename + 'object_center.txt', 'r'):
    #itemList = line[:-1].split(',')
    if gyo == 0:
      object_num = int(line)
    gyo = gyo + 1    
    #    for i in xrange(len(itemList)):
    #      if itemList[i] != '':
    #        Ct = Ct + [int(itemList[i])]

  for object in range(object_num):
    fp  = open(filename+'image/object_SIFT_BoF_'+str(object+1).zfill(2)+'.csv','w')
    fp2 = open(filename+'image/object_RGB_BoF_'+str(object+1).zfill(2)+'.csv','w')
    #min = 0
    BoF  = [0 for i in range(k_sift)]
    BoF2 = [0 for i in range(k_rgb)]
    for f in range(len(object_feature[trial][object])):
      min = 0  #saveing nearest class
      min_value = 0.0
      for i in range(len(cluster)):
        dist = 0
        for j in range(len(cluster[i])):
          tmp = cluster[i][j] - object_feature[trial][object][f][j]
          dist = dist + (tmp * tmp)
        if(i == 0):
          min_value = dist
        elif(min_value > dist):
          min_value = dist
          min = i
      BoF[min] = BoF[min] + 1
  
    for i in range(k_sift):
      fp.write(repr(BoF[i])+',')
    fp.write('\n')
  
    for f in range(len(object_color[trial][object])):
      min = 0  #saveing nearest class
      min_value = 0.0
      for i in range(len(cluster_bgr)):
        dist = 0
        for j in range(len(cluster_bgr[i])):
          tmp = cluster_bgr[i][j] - object_color[trial][object][f][j]
          dist = dist + (tmp * tmp)
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




#k = cv2.waitKey(0)
#if k & 0xff == 27:
#    cv2.destroyAllWindows()
