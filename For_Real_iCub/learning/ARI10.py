#coding:utf-8
#ARI
#Akira Taniguchi 2016/06/19
#!/usr/bin/env python
#調整ランド指数を計算するプログラム
import sys
import string
from sklearn.metrics.cluster import adjusted_rand_score
from __init__ import *
#import matplotlib.pyplot as plt
#import numpy as np
#import math

#param = sys.argv

trialname = "ts"#raw_input("trialname?(folder) >")
start = "1"#raw_input("start number?>")
end   = raw_input("data end number?>")
filename1 = raw_input("learning trial name(**00?)?>")#param[1]#"001"#

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"



#data_name = raw_input("data_name? > ")
#data_num1 = raw_input("data_start_num? > ")
#data_num2 = raw_input("data_end_num? > ")
#N = int(data_num2) - int(data_num1) +1
#filename = raw_input("Read_Ct_filename?(.csv) >")
#S = int(data_num1)

for d in range(10):
  filename = filename1 + str(d+1).zfill(3)
  za_c = []#[ int(uniform(0,Ko)) for d in xrange(D) ] #正解の分類結果
  zp_c = []#[ [ int(uniform(0,Kp)) for m in xrange(M[d]) ] for d in xrange(D) ]
  zo_c = []#[ [ int(uniform(0,Ko)) for m in xrange(M[d]) ] for d in xrange(D) ]
  zc_c = []#[ [ int(uniform(0,Kc)) for m in xrange(M[d]) ] for d in xrange(D) ]
  
  za = []#[ int(uniform(0,Ko)) for d in xrange(D) ]
  zp = []#[ [ int(uniform(0,Kp)) for m in xrange(M[d]) ] for d in xrange(D) ]
  zo = []#[ [ int(uniform(0,Ko)) for m in xrange(M[d]) ] for d in xrange(D) ]
  zc = []#[ [ int(uniform(0,Kc)) for m in xrange(M[d]) ] for d in xrange(D) ]  
  
  ARI_a = 0.0
  ARI_p = 0.0
  ARI_o = 0.0
  ARI_c = 0.0
  
  for line in open(foldername +'/za_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      itemList[i] = itemList[i].replace("\r", "")
      itemList[i] = itemList[i].replace("\n", "")
      if itemList[i] != '':
        za_c = za_c + [int(itemList[i])]
  
  for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_za.csv', 'r'):
    itemList = line[:-1].split(',')
    for i in range(len(itemList)):
      if itemList[i] != '':
        za = za + [int(itemList[i])]
  
  #print len(za_c),len(za)
  ARI_a = adjusted_rand_score(za_c, za)
  print ARI_a
  
  
  for line in open(foldername +'/zp_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      itemList[i] = itemList[i].replace("\r", "")
      itemList[i] = itemList[i].replace("\n", "")
      if itemList[i] != '':
           #if itemList[i] != "":        
           #print itemList[i]
           zp_c = zp_c + [itemList[i]]
  
  for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zp.csv', 'r'):
    itemList = line[:-1].split(',')
    for i in range(len(itemList)):
      if itemList[i] != '':
        zp = zp + [int(itemList[i])]
  
  
  ARI_p = adjusted_rand_score(zp_c, zp)
  print ARI_p
  
  
  for line in open(foldername +'/zo_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      itemList[i] = itemList[i].replace("\r", "")
      itemList[i] = itemList[i].replace("\n", "")
      if itemList[i] != '':
        zo_c = zo_c + [itemList[i]]
  
  for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zo.csv', 'r'):
    itemList = line[:-1].split(',')
    for i in range(len(itemList)):
      if itemList[i] != '':
        zo = zo + [int(itemList[i])]
  
  
  ARI_o = adjusted_rand_score(zo_c, zo)
  print ARI_o
  
  
  
  for line in open(foldername +'/zc_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      itemList[i] = itemList[i].replace("\r", "")
      itemList[i] = itemList[i].replace("\n", "")
      if itemList[i] != '':
        zc_c = zc_c + [itemList[i]]
  
  for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zc.csv', 'r'):
    itemList = line[:-1].split(',')
    for i in range(len(itemList)):
      if itemList[i] != '':
        zc = zc + [int(itemList[i])] 
  
  
  ARI_c = adjusted_rand_score(zc_c, zc)
  print ARI_c
  
  
  fp = open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_ARI.csv', 'w')
  #fp.write('pi_c'+',')
  fp.write('ARI_a,ARI_p,ARI_o,ARI_c\n')
  fp.write(repr(ARI_a)+','+repr(ARI_p)+','+repr(ARI_o)+','+repr(ARI_c)+'\n')
  fp.write('\n')
  fp.close()
