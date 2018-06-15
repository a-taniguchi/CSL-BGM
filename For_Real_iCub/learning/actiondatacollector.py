#coding:utf-8

##############################################
# iCub data collecting 
# datadumper files -> an action data file
# Akira Taniguchi 2016/06/14-
##############################################

#[1465866469.732024] /icubSim/head/state:o [connected]
#[1465866474.010252] /icubSim/head/state:o [disconnected]
#[1465866486.252840] /icubSim/head/state:o [connected]
#[1465866524.599823] /icubSim/head/state:o [disconnected]

#import glob
#import codecs
#import re
import os
#import sys
import random
#import string
import collections
import itertools
import numpy as np
import scipy as sp
#import matplotlib.pyplot as plt
#from numpy.random import multinomial,uniform,dirichlet
#from scipy.stats import multivariate_normal,invwishart,rv_discrete
from math import pi as PI
from math import cos,sin,sqrt,exp,log,fabs,fsum,degrees,radians,atan2
#from sklearn.cluster import KMeans
from __init__ import *

def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass


def data_collect(trialname,sn,en,Data):
    foldername = datafolder + trialname
    
    
    #datadumpフォルダを1試行ずつ読み込み
    for d in xrange(Data):
      gyo = 0
      fp = open( foldername +str(d+sn).zfill(3)+'/action.csv', 'w')
      
      #info.log読み込み
      #for line in open(foldername+str(d+sn).zfill(3)+'/head/head/info.log','r'):
      #  itemList = line[:-1].split(' ')
      #  for j in xrange(len(itemList)):
      #    itemList[j] = itemList[j].replace("[", "")
      #    itemList[j] = itemList[j].replace("]", "")
      #    
      #  if ("disconnected" == itemList[2]):
      #    datatime = int(itemList[0])
      #  
      #data.log読み込み
      #head読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/head/head/data.log','r'):
        itemList = line[:-1].split(' ')
        #if datatime == int(itemList[1]):
        head = [float(itemList[2]),float(itemList[3]),float(itemList[4]),float(itemList[5]),float(itemList[6]),float(itemList[7])]
      print "head",len(head),head
      fp.write("head,"+ repr(len(head))+"\n")
      for i in range(len(head)):
        fp.write(repr(head[i])+",")
      fp.write("\n\n")
      
      #left_arm読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/left_arm/left_arm/data.log','r'):
        itemList = line[:-1].split(' ')
        #if datatime >= int(itemList[1]):
        left_arm = []
        for i in range(16):
          left_arm = left_arm + [float(itemList[i+2])]
      print "left_arm",len(left_arm),left_arm
      fp.write("left_arm,"+ repr(len(left_arm))+"\n")
      for i in range(len(left_arm)):
        fp.write(repr(left_arm[i])+",")
      fp.write("\n\n")
      
      #right_arm読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/right_arm/right_arm/data.log','r'):
        itemList = line[:-1].split(' ')
        #if datatime >= int(itemList[1]):
        right_arm = []
        for i in range(16):
          right_arm = right_arm + [float(itemList[i+2])]
      print "right_arm",len(right_arm),right_arm
      fp.write("right_arm,"+ repr(len(right_arm))+"\n")
      for i in range(len(right_arm)):
        fp.write(repr(right_arm[i])+",")
      fp.write("\n\n")
      
      #torso読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/torso/torso/data.log','r'):
        itemList = line[:-1].split(' ')
        #if datatime >= int(itemList[1]):
        torso= []
        for i in range(3):
          torso = torso + [float(itemList[i+2])]
      print "torso",len(torso),torso
      fp.write("torso,"+ repr(len(torso))+"\n")
      for i in range(len(torso)):
        fp.write(repr(torso[i])+",")
      fp.write("\n\n")
      
      #skin読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/skin/right_hand/data.log','r'):
        itemList = line[:-1].split(' ')
        #if datatime >= int(itemList[1]):
        right_hand = []
        for i in range(5*12):
          right_hand = right_hand + [float(itemList[i+2])]
        for i in range(4*12):
          right_hand = right_hand + [float(itemList[(i+2) + 8*12])]
      print "right_hand",len(right_hand),right_hand
      fp.write("right_hand,"+ repr(len(right_hand))+"\n")
      for i in range(len(right_hand)):
        fp.write(repr(right_hand[i])+",")
      fp.write("\n\n")
      
      fp.write( repr(len(head)+len(left_arm)+len(right_arm)+len(torso)+len(right_hand)) )
      
      fp.close()
    """
    
      
      ##物体数M[d]の読み込み
      for line in open(foldername+str(d+sn).zfill(3)+'/object_center.txt','r'):
        
          M[d] = int(line)
          o_dm[d] = [ [ 0 for k in xrange(k_sift) ] for m in xrange(M[d]) ]
          c_dm[d] = [ [ 0 for k in xrange(k_rgb)  ] for m in xrange(M[d]) ]
          p_dm[d] = [ [ 0 for k in xrange(3)      ] for m in xrange(M[d]) ]
        elif gyo == 1:
          Ad[d] = int(line)-1 #物体番号1からMを0からM-1にする
        else:
          itemList = line[:-1].split(',')
          #for i in xrange(len(itemList)):
          if itemList[0] != '':
            p_dm[d][int(itemList[0])-1] = [float(itemList[1]),float(itemList[2]),float(itemList[3])]
        gyo = gyo + 1
      
      for m in xrange(M[d]):
        ##物体情報 BoF(SIFT)の読み込み
        for line in open(foldername+str(d+sn).zfill(3)+'/image/object_SIFT_BoF_'+str(m+1).zfill(2)+'.csv', 'r'):
          itemList = line[:-1].split(',')
          #print c
          #W_index = W_index + [itemList]
          for i in xrange(len(itemList)):
            if itemList[i] != '':
              #print c,i,itemList[i]
              o_dm[d][m][i] = float(itemList[i])
              
              #print itemList
              
        ##色情報 BoF(RGB)の読み込み
        for line in open(foldername+str(d+sn).zfill(3)+'/image/object_RGB_BoF_'+str(m+1).zfill(2)+'.csv', 'r'):
          itemList = line[:-1].split(',')
          #print c
          #W_index = W_index + [itemList]
          for i in xrange(len(itemList)):
            if itemList[i] != '':
              #print c,i,itemList[i]
              c_dm[d][m][i] = float(itemList[i])
    
    
    a_d  = [ basyo[1] , basyo[2] , basyo[3] , basyo[1] , basyo[2] , basyo[3] , basyo[1] , basyo[2] , basyo[3] , basyo[1]]
    """
    




if __name__ == '__main__':
    import sys
    import shutil
    #import os.path
    from __init__ import *
    #from JuliusLattice_gmm import *
    #import time
    
    
    #filename = sys.argv[1]
    #print filename
    
    #出力ファイル名を要求
    #filename = raw_input("trialname?(folder) >")
    
    trialname = raw_input("trialname?(folder) >")
    start = raw_input("start number?>")
    end   = raw_input("end number?>")
    
    sn = int(start)
    en = int(end)
    Data = int(en) - int(sn) +1
    
    
    
    
    data_collect(trialname,sn,en,Data)


