﻿#coding:utf-8
#ARI
#Akira Taniguchi 2016/06/19
#!/usr/bin/env python
#調整ランド指数を計算するプログラム(Attention data only)
import sys
import string
from sklearn.metrics.cluster import adjusted_rand_score
from __init__ import *
#import matplotlib.pyplot as plt
#import numpy as np
#import math

trialname = "testss"#raw_input("trialname?(folder) >")
start = "1"#raw_input("start number?>")
end   = "20"#raw_input("end number?>")
filename = raw_input("learning trial name?>")#"001"#

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"

Ad = [0, 1, 1, 2, 2, 1, 1, 2, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1]

#data_name = raw_input("data_name? > ")
#data_num1 = raw_input("data_start_num? > ")
#data_num2 = raw_input("data_end_num? > ")
#N = int(data_num2) - int(data_num1) +1
#filename = raw_input("Read_Ct_filename?(.csv) >")
#S = int(data_num1)

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

d = 0
for line in open(foldername +'/zp_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      #print d,len(Ad)
      if (itemList[i] != ''):
        #print i,d,itemList[i]
        if (i == Ad[d]):
          zp_c = zp_c + [int(itemList[i])]
   d = d + 1

d = 0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zp.csv', 'r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if itemList[i] != '' and i == Ad[d]:
      zp = zp + [int(itemList[i])]
  d = d + 1


ARI_p = adjusted_rand_score(zp_c, zp)
print ARI_p

d = 0
for line in open(foldername +'/zo_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      if itemList[i] != '' and i == Ad[d]:
        zo_c = zo_c + [int(itemList[i])]
   d = d + 1

d = 0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zo.csv', 'r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if itemList[i] != '' and i == Ad[d]:
      zo = zo + [int(itemList[i])]
  d = d + 1

ARI_o = adjusted_rand_score(zo_c, zo)
print ARI_o



d = 0
for line in open(foldername +'/zc_C.csv', 'r'):
   itemList = line[:-1].split(',')
   for i in xrange(len(itemList)):
      if itemList[i] != '' and i == Ad[d]:
        zc_c = zc_c + [int(itemList[i])]
   d = d + 1
d = 0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zc.csv', 'r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if itemList[i] != '' and i == Ad[d]:
      zc = zc + [int(itemList[i])]
  d = d + 1

ARI_c = adjusted_rand_score(zc_c, zc)
print ARI_c

#print str(ARI)
#ARI_M = ARI_M + ARI

#ARI_M = float(ARI_M / N)
#print "ARI mean"
#print str(ARI_M)


fp = open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_ARI_attention.csv', 'w')
#fp.write('pi_c'+',')
fp.write('ARI_a,ARI_p,ARI_o,ARI_c\n')
fp.write(repr(ARI_a)+','+repr(ARI_p)+','+repr(ARI_o)+','+repr(ARI_c)+'\n')
fp.write('\n')
fp.close()
