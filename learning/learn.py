#coding:utf-8

##############################################
# iCub learning program 
# Basically, Gibbs sampling of GMMs and LDA
# Akira Taniguchi 2016/05/31-2020/07/15
##############################################

#numpy.random.multivariate_normal
#http://docs.scipy.org/doc/numpy-1.10.0/reference/generated/numpy.random.multivariate_normal.html
#scipy.stats.multivariate_normal
#http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.stats.multivariate_normal.html
#scipy.stats.invwishart
#http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.stats.invwishart.html
#numpy.random.dirichlet
#http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.dirichlet.html
#scipy.stats.dirichlet
#http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.stats.dirichlet.html
#numpy.random.multinomial
#http://docs.scipy.org/doc/numpy-1.10.1/reference/generated/numpy.random.multinomial.html
#scipy.stats.rv_discrete
#http://docs.scipy.org/doc/scipy-0.17.0/reference/generated/scipy.stats.rv_discrete.html

import os
import random
import collections
import itertools
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from numpy.random import multinomial,uniform,dirichlet
from scipy.stats import multivariate_normal,invwishart,rv_discrete
from math import pi as PI
from math import cos,sin,sqrt,exp,log,fabs,fsum,degrees,radians,atan2
from sklearn.cluster import KMeans
from __init__ import *

def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass

def stick_breaking(alpha, k):
    betas = np.random.beta(1, alpha, k)
    remaining_pieces = np.append(1, np.cumprod(1 - betas[:-1]))
    p = betas * remaining_pieces
    return p/p.sum()

def Sample_Frame_Random(num):
    #modal = [ modality[i] for i in range(len(modality))]
    F = []
    for i in xrange(num):
      mo = int(uniform(0,len(modality)))
      F = F + [ modality[mo] ]
    return F

def Sample_Frame(num):
    modal = ["a","p","o","c"]
    other = "x"
    dis = 0
    F = []
    if (num >= len(modal)):
      #print "[Error] over modality"
      dis = num - len(modal)
      num = 4
      #return F
    for n in xrange(num):
      mo = int(uniform(0,4-n))
      F = F + [ modal[mo] ]
      modal.pop(mo)
    for i in xrange(dis):
      F.insert( int(uniform( 0, int(num+i+1) )), other )
    return F

def data_read(trialname,finename,sn,en):
    foldername = datafolder + trialname
    
    M = [0 for d in xrange(D)]   # the set of the number of objects
    N = [0 for d in xrange(D)]   # the set of the number of words
    Ad = [0 for d in xrange(D)]
    
    w_dn = [ [] for d in xrange(D) ]  # the set of sentences # The sentence is the set of words.
    a_d  = [ [] for d in xrange(D) ]  # the set of actions
    o_dm = [ [] for d in xrange(D) ]  # the set of object features
    c_dm = [ [] for d in xrange(D) ]  # the set of object colors
    p_dm = [ [] for d in xrange(D) ]  # the set of pobject positions
    
    min_a = [10,10,10]     # Temporary initial value
    max_a = [-10,-10,-10]  # Temporary initial value
    min_o = 10000
    max_o = -10000
    
    ## reading the set of the number of objects for each sentences
    for d in xrange(D):
      line_num = 0
      ## Read the number of objects M[d]
      for line in open(foldername+str(d+sn).zfill(3)+'/object_center.txt','r'):
        if line_num == 0:
          M[d] = int(line)
          o_dm[d] = [ [ 0 for k in xrange(k_sift) ] for m in xrange(M[d]) ]
          c_dm[d] = [ [ 0 for k in xrange(k_rgb)  ] for m in xrange(M[d]) ]
          p_dm[d] = [ [ 0 for k in xrange(dim_p)  ] for m in xrange(M[d]) ]
          #elif line_num == 1:
          #  Ad[d] = int(line)-1 #物体番号1からMを0からM-1にする
        elif line_num == 1:
          dummy = 0
          #print "if random_obj was changed, but no problem."
        else:
          itemList = line[:-1].split(',')
          #for i in xrange(len(itemList)):
          if itemList[0] != '':
            ## Read the position p_dm
            p_dm[d][int(itemList[0])-1] = [float(itemList[1]),float(itemList[2])]
        line_num = line_num + 1
      
      
      gyo = 0
      ## Read the target object position and end-effector position (Hand posiiton of iCub) 
      for line in open(foldername+str(d+sn).zfill(3)+'/target_object.txt','r'):
        if gyo == 0:
          Ad[d] = int(line)-1
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
      if (d == 0):
         min_a = list(tmp)
         max_a = list(tmp)
      for i in xrange(3):
        if (min_a[i] > tmp[i]):
           min_a[i]= tmp[i]
        if (max_a[i] < tmp[i]):
           max_a[i] = tmp[i]
      a_d[d] = list(tmp) + [randomove] # Relative 3D position, finger bending (相対3次元位置、指の曲げ具合)
      
      gyo = 0
      for line in open(foldername+str(d+sn).zfill(3)+'/action.csv','r'):
        itemList = line[:-1].split(',')
        
        if ("" in itemList):
          itemList.pop(itemList.index(""))
        # Normalized with minimum and maximum values for each joint location (関節箇所ごとに最小値と最大値で正規化)
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
              a_d[d] = a_d[d] + [ (float(itemList[i])-min[i])/float(max[i]-min[i]) ]  #Normalize and add to array	
        if(gyo == 13):
          tactile = [0.0 for i in xrange(len(itemList)/12)]
          for i in xrange(len(itemList)/12):
            #for j in xrange(12):
            #  print i*12+j
            tactile[i] = sum([float(itemList[i*12+j]) for j in xrange(12)])/float(255*12)  #Average of 12 data
        
        gyo = gyo + 1
      a_d[d] = a_d[d] + tactile
      
      
      for m in xrange(M[d]):
        ##物体情報 BoF(SIFT)orCNN特徴の読み込み
        for line in open(foldername+str(d+sn).zfill(3)+'/image/object_' + Descriptor + '_'+str(m+1).zfill(2)+'.csv', 'r'):
          itemList = line[:-1].split(',')
          #print c
          #W_index = W_index + [itemList]
          for i in xrange(len(itemList)):
            if itemList[i] != '':
              #print c,i,itemList[i]
              o_dm[d][m][i] = float(itemList[i])
              if min_o > o_dm[d][m][i]:
                min_o = o_dm[d][m][i]
              if max_o < o_dm[d][m][i]:
                max_o = o_dm[d][m][i]
              
        if (CNNmode == 0) or (CNNmode == -1):
          # Normalized BoF count (BoFのカウント数を正規化)
          sum_o_dm = sum(o_dm[d][m])
          for i in xrange(len(o_dm[d][m])):
            o_dm[d][m][i] = o_dm[d][m][i] / sum_o_dm
              
        ## Read color information BoF(RGB)
        for line in open(foldername+str(d+sn).zfill(3)+'/image/object_RGB_BoF_'+str(m+1).zfill(2)+'.csv', 'r'):
          itemList = line[:-1].split(',')
          #print c
          #W_index = W_index + [itemList]
          for i in xrange(len(itemList)):
            if itemList[i] != '':
              #print c,i,itemList[i]
              c_dm[d][m][i] = float(itemList[i])
        
        # Normalized BoF count (BoFのカウント数を正規化)
        sum_c_dm = sum(c_dm[d][m])
        for i in xrange(len(c_dm[d][m])):
          c_dm[d][m][i] = c_dm[d][m][i] / sum_c_dm
      
    # Get the word data
    d = 0
    for line in open(foldername +"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"+'/' + trialname +'_words.csv', 'r'):
        itemList = line[:-1].split(',')
        for i in xrange(len(itemList)):
            if itemList[i] != '':
              w_dn[d] = w_dn[d] + [str(itemList[i])]
              N[d] = N[d] + 1
        d = d + 1
    
    print w_dn
    
    ## Normalize relative coordinates of action data (アクションデータの相対座標を正規化)
    for d in xrange(D):
      a_d[d][0] = (a_d[d][0] - min_a[0]) / (max_a[0] - min_a[0])
      a_d[d][1] = (a_d[d][1] - min_a[1]) / (max_a[1] - min_a[1])
      a_d[d][2] = (a_d[d][2] - min_a[2]) / (max_a[2] - min_a[2])
      
      # CNN feature normalization (CNN特徴の正規化)
      if CNNmode == 1:
        for m in xrange(M[d]):
          for i in xrange(dim_o):
            o_dm[d][m][i] = (o_dm[d][m][i] - min_o) / (max_o - min_o)
    
    ###test data###
    #D = 10
    #M = [1 for d in xrange(D)]
    #N = [4 for d in xrange(D)]
    #Ad = [0 for d in xrange(D)]
    #basyo = [[],[-10+uniform(-1,1),-10+uniform(-1,1)], [10+uniform(-1,1),10+uniform(-1,1)], [0+uniform(-1,1),0+uniform(-1,1)]]
    #a_d  = [ basyo[1] , basyo[2] , basyo[3] , basyo[1] , basyo[2] , basyo[3] , basyo[1] , basyo[2] ]#, basyo[3] , basyo[1]]
    #p_dm = [[basyo[3]],[basyo[3]],[basyo[3]],[basyo[1]],[basyo[1]],[basyo[1]],[basyo[2]],[basyo[2]],[basyo[2]],[basyo[3]]]
    #o_dm = [[basyo[1]],[basyo[3]],[basyo[2]],[basyo[3]],[basyo[2]],[basyo[1]],[basyo[2]],[basyo[3]],[basyo[1]],[basyo[2]]]
    #c_dm = [[basyo[2]],[basyo[1]],[basyo[1]],[basyo[2]],[basyo[3]],[basyo[2]],[basyo[3]],[basyo[1]],[basyo[3]],[basyo[1]]]
    
    
    #w_dn = [["reach","front","box","green"] for i in range(1)]+[["touch","right","cup","green"] for i in range(1)]+[["touch","front","box","red"] for i in range(1)]+[["reach","front","box","blue"] for i in range(1)]+[["touch","front","box","green"] for i in range(1)]+[["lookat","front","cup","blue"] for i in range(1)]+[["lookat","left","cup","red"] for i in range(1)]+[["lookat","right","box","red"] for i in range(1)]#+[["a3a","p2p","o1o","c3c"] for i in range(1)]+[["a1a","p3p","o2o","c1c"] for i in range(1)]
    
    # Save the loaded data to one file (読み込んだデータを保存)
    fp = open( foldername +"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"+'/' + filename +'/'+ trialname + '_' + filename +'_data.csv', 'w')
    for i in xrange(3):
      fp.write(repr(min_a[i])+',')
    fp.write('\n')
    for i in xrange(3):
      fp.write(repr(max_a[i])+',')
    fp.write('\n')
    fp.write('M\n')
    fp.write(repr(M))
    fp.write('\n')
    fp.write('N\n')
    fp.write(repr(N))
    fp.write('\n')
    fp.write('a_d\n')
    for d in xrange(D):
      fp.write(repr(a_d[d])+'\n')
    fp.write('\n')
    fp.write('p_dm\n')
    fp.write(repr(p_dm))
    fp.write('\n')
    fp.write('o_dm\n')
    for d in xrange(D):
      fp.write(repr(o_dm[d])+'\n')
    fp.write('\n')
    fp.write('c_dm\n')
    fp.write(repr(c_dm))
    fp.write('\n')
    fp.write('Ad\n')
    fp.write(repr(Ad))
    fp.write('\n')
    fp.write('w_dn\n')
    fp.write(repr(w_dn))
    fp.write('\n')
    fp.close()
    
    return M, N, w_dn, a_d, p_dm, o_dm, c_dm, Ad


def para_save(foldername,trialname,filename,za,zp,zo,zc,Fd,theta,W_list,Mu_a,Sig_a,Mu_p,Sig_p,Mu_o,Sig_o,Mu_c,Sig_c,pi_a,pi_p,pi_o,pi_c):
    foldername = foldername + "/" + filename
    trialname = trialname + "_" + filename
    
    #Saving each parameter
    fp = open( foldername +'/' + trialname +'_kekka.csv', 'w')
    fp.write('sampling_data\n') 
    fp.write('za\n')
    for d in xrange(D):
      fp.write(repr(d)+',')
    fp.write('\n')
    for d in xrange(D):
      fp.write(repr(za[d])+',')
    fp.write('\n')
    
    fp.write('zp\n')
    for d in xrange(D):
      for m in xrange(len(zp[d])):
        fp.write(repr(d)+'->'+repr(m)+',')
    fp.write('\n')
    for d in xrange(D):
      for m in xrange(len(zp[d])):
        fp.write(repr(zp[d][m])+',')
    fp.write('\n')
    
    fp.write('zo\n')
    for d in xrange(D):
      for m in xrange(len(zo[d])):
        fp.write(repr(d)+'->'+repr(m)+',')
    fp.write('\n')
    for d in xrange(D):
      for m in xrange(len(zo[d])):
        fp.write(repr(zo[d][m])+',')
    fp.write('\n')
    
    fp.write('zc\n')
    for d in xrange(D):
      for m in xrange(len(zc[d])):
        fp.write(repr(d)+'->'+repr(m)+',')
    fp.write('\n')
    for d in xrange(D):
      for m in xrange(len(zc[d])):
        fp.write(repr(zc[d][m])+',')
    fp.write('\n')
    
    fp.write('Fd\n')
    for d in xrange(D):
      fp.write(repr(d)+','+repr(Fd[d])+'\n')
      
    fp.write('theta\n,,')
    for w in xrange(len(W_list)):
      fp.write(repr(W_list[w])+',')
    fp.write('\n')
    for i in xrange(Ka):
      fp.write('a '+repr(i)+','+repr(i)+',')
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i][w])+',')
      fp.write('\n')
    for i in xrange(Kp):
      fp.write('p '+repr(i)+','+repr(i+dict["p"])+',')
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i+dict["p"]][w])+',')
      fp.write('\n')
    for i in xrange(Ko):
      fp.write('o '+repr(i)+','+repr(i+dict["o"])+',')
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i+dict["o"]][w])+',')
      fp.write('\n')
    for i in xrange(Kc):
      fp.write('c '+repr(i)+','+repr(i+dict["c"])+',')
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i+dict["c"]][w])+',')
      fp.write('\n')
    
    fp.write('action category\n')
    fp.write('Mu\n')
    for k in xrange(Ka):
      fp.write(repr(k)+',')
      for dim in xrange(dim_a):
        fp.write(repr(Mu_a[k][dim])+',')
      fp.write('\n')
    fp.write('Sig\n')
    for k in xrange(Ka):
      fp.write(repr(k)+'\n')
      for dim in xrange(dim_a):
        for dim2 in xrange(dim_a):
          fp.write(repr(Sig_a[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    
    fp.write('position category\n')
    fp.write('Mu\n')
    for k in xrange(Kp):
      fp.write(repr(k)+',')
      for dim in xrange(dim_p):
        fp.write(repr(Mu_p[k][dim])+',')
      fp.write('\n')
    fp.write('Sig\n')
    for k in xrange(Kp):
      fp.write(repr(k)+'\n')
      for dim in xrange(dim_p):
        for dim2 in xrange(dim_p):
          fp.write(repr(Sig_p[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    
    fp.write('object category\n')
    fp.write('Mu\n')
    for k in xrange(Ko):
      fp.write(repr(k)+',')
      for dim in xrange(dim_o):
        fp.write(repr(Mu_o[k][dim])+',')
      fp.write('\n')
    fp.write('Sig\n')
    for k in xrange(Ko):
      fp.write(repr(k)+'\n')
      for dim in xrange(dim_o):
        for dim2 in xrange(dim_o):
          fp.write(repr(Sig_o[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    
    fp.write('color category\n')
    fp.write('Mu\n')
    for k in xrange(Kc):
      fp.write(repr(k)+',')
      for dim in xrange(dim_c):
        fp.write(repr(Mu_c[k][dim])+',')
      fp.write('\n')
    fp.write('Sig\n')
    for k in xrange(Kc):
      fp.write(repr(k)+'\n')
      for dim in xrange(dim_c):
        for dim2 in xrange(dim_c):
          fp.write(repr(Sig_c[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    
    fp.write('pi_a'+',')
    for k in xrange(Ka):
      fp.write(repr(pi_a[k])+',')
    fp.write('\n')
    fp.write('pi_p'+',')
    for k in xrange(Kp):
      fp.write(repr(pi_p[k])+',')
    fp.write('\n')
    fp.write('pi_o'+',')
    for k in xrange(Ko):
      fp.write(repr(pi_o[k])+',')
    fp.write('\n')
    fp.write('pi_c'+',')
    for k in xrange(Kc):
      fp.write(repr(pi_c[k])+',')
    fp.write('\n')
    
    fp.close()
    
    #print 'File Output Successful!(filename:'+filename+')\n'
    
    ## Output each parameter as each file (パラメータそれぞれをそれぞれのファイルとして出力)
    fp = open(foldername +'/' + trialname +'_za.csv', 'w')
    for d in xrange(D):
      fp.write(repr(za[d])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_zp.csv', 'w')
    for d in xrange(D):
      for m in xrange(len(zp[d])):
        fp.write(repr(zp[d][m])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_zo.csv', 'w')
    for d in xrange(D):
      for m in xrange(len(zo[d])):
        fp.write(repr(zo[d][m])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_zc.csv', 'w')
    for d in xrange(D):
      for m in xrange(len(zc[d])):
        fp.write(repr(zc[d][m])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Fd.csv', 'w')
    #fp.write('Fd\n')
    for d in xrange(D):
      for f in xrange(len(Fd[d])):
        fp.write(repr(Fd[d][f])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_theta.csv', 'w')
    #fp.write('theta\n')
    for i in xrange(L):
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i][w])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_W_list.csv', 'w')
    for w in xrange(len(W_list)):
      fp.write(repr(W_list[w])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Mu_a.csv', 'w')
    #fp.write('action category\n')
    #fp.write('Mu\n')
    for k in xrange(Ka):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_a):
        fp.write(repr(Mu_a[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Sig_a.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Ka):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_a):
        for dim2 in xrange(dim_a):
          fp.write(repr(Sig_a[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Mu_p.csv', 'w')
    #fp.write('position category\n')
    #fp.write('Mu\n')
    for k in xrange(Kp):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_p):
        fp.write(repr(Mu_p[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Sig_p.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Kp):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_p):
        for dim2 in xrange(dim_p):
          fp.write(repr(Sig_p[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Mu_o.csv', 'w')
    #fp.write('object category\n')
    #fp.write('Mu\n')
    for k in xrange(Ko):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_o):
        fp.write(repr(Mu_o[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Sig_o.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Ko):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_o):
        for dim2 in xrange(dim_o):
          fp.write(repr(Sig_o[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Mu_c.csv', 'w')
    #fp.write('color category\n')
    #fp.write('Mu\n')
    for k in xrange(Kc):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_c):
        fp.write(repr(Mu_c[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_Sig_c.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Kc):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_c):
        for dim2 in xrange(dim_c):
          fp.write(repr(Sig_c[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_pi_a.csv', 'w')
    #fp.write('pi_a'+',')
    for k in xrange(Ka):
      fp.write(repr(pi_a[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_pi_p.csv', 'w')
    #fp.write('pi_p'+',')
    for k in xrange(Kp):
      fp.write(repr(pi_p[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_pi_o.csv', 'w')
    #fp.write('pi_o'+',')
    for k in xrange(Ko):
      fp.write(repr(pi_o[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + trialname +'_pi_c.csv', 'w')
    #fp.write('pi_c'+',')
    for k in xrange(Kc):
      fp.write(repr(pi_c[k])+',')
    fp.write('\n')
    fp.close()
    
    print 'File Output Successful!(filename:'+foldername+')\n'
    
    

# Simulation
def simulate(foldername,trialname,filename,sn,en, M, N, w_dn, a_d, p_dm, o_dm, c_dm, Ad):
      np.random.seed()
      print w_dn
      # random initialzation
      print u"Initialize Parameters..."
      za = [ int(uniform(0,Ko)) for d in xrange(D) ]
      zp = [ [ int(uniform(0,Kp)) for m in xrange(M[d]) ] for d in xrange(D) ]
      zo = [ [ int(uniform(0,Ko)) for m in xrange(M[d]) ] for d in xrange(D) ]
      zc = [ [ int(uniform(0,Kc)) for m in xrange(M[d]) ] for d in xrange(D) ]
      
      Fd = [ Sample_Frame(N[d]) for d in xrange(D)] #random initialzation ("a","p","o","c")
      
      cw = np.sum([collections.Counter(w_dn[d]) for d in xrange(D)])
      W_list = list(cw)  ##List of words
      W = len(cw)  ##Length of word list
      theta = [ sum(dirichlet(np.array([gamma for w in xrange(W)]),100))/100.0 for i in xrange(L) ] #indexと各モダリティーの対応付けはdictionary形式で呼び出す
      
      #KMeans(n_clusters=Ka, init='k-means++').fit(a_d).cluster_centers_
      Mu_a  = KMeans(n_clusters=Ka, init='k-means++').fit(a_d).cluster_centers_#[ np.array([uniform(mu_a_init[0],mu_a_init[1]) for i in xrange(dim_a)]) for k in xrange(Ka) ]
      Sig_a = [ np.eye(dim_a)*sig_a_init for k in xrange(Ka) ]
      #print "Mu_a",Mu_a
      
      p_temp = []
      for d in xrange(D):
        p_temp = p_temp + p_dm[d]
      Mu_p  = KMeans(n_clusters=Kp, init='k-means++').fit(p_temp).cluster_centers_#[ np.array([uniform(mu_p_init[0],mu_p_init[1]) for i in xrange(dim_p)]) for k in xrange(Kp) ]
      Sig_p = [ np.eye(dim_p)*sig_p_init for k in xrange(Kp) ]
      
      o_temp = []
      for d in xrange(D):
        o_temp = o_temp + o_dm[d]
      Mu_o  = KMeans(n_clusters=Ko, init='k-means++').fit(o_temp).cluster_centers_#[ np.array([uniform(mu_o_init[0],mu_o_init[1]) for i in xrange(dim_o)]) for k in xrange(Ko) ]
      Sig_o = [ np.eye(dim_o)*sig_o_init for k in xrange(Ko) ]
      
      c_temp = []
      for d in xrange(D):
        c_temp = c_temp + c_dm[d]
      Mu_c  = KMeans(n_clusters=Kc, init='k-means++').fit(c_temp).cluster_centers_#[ np.array([uniform(mu_c_init[0],mu_c_init[1]) for i in xrange(dim_c)]) for k in xrange(Kc) ]
      Sig_c = [ np.eye(dim_c)*sig_c_init for k in xrange(Kc) ]
      
      
      if nonpara == 0 :
        pi_a = sum(dirichlet([ alpha_a for c in xrange(Ka)],100))/100.0
        pi_p = sum(dirichlet([ alpha_p for c in xrange(Kp)],100))/100.0 
        pi_o = sum(dirichlet([ alpha_o for c in xrange(Ko)],100))/100.0 
        pi_c = sum(dirichlet([ alpha_c for c in xrange(Kc)],100))/100.0 
      elif nonpara == 1:
        pi_a = stick_breaking(alpha_a, Ka)
        pi_p = stick_breaking(alpha_p, Kp) 
        pi_o = stick_breaking(alpha_o, Ko) 
        pi_c = stick_breaking(alpha_c, Kc) 
      
      print theta
      print pi_a
      print pi_p
      print pi_o
      print pi_c
      print Mu_a
      print Mu_p
      print Mu_o
      print Mu_c
      print Fd
      
      ### Copy initial values (このやり方でないと値が変わってしまう)
      za_init = [ za[d] for d in xrange(D)]
      zp_init = [ [ zp[d][m] for m in xrange(M[d]) ] for d in xrange(D) ]
      zo_init = [ [ zo[d][m] for m in xrange(M[d]) ] for d in xrange(D) ]
      zc_init = [ [ zc[d][m] for m in xrange(M[d]) ] for d in xrange(D) ]
      Fd_init = [ Fd[d] for d in xrange(D)]
      theta_init = [ np.array(theta[i]) for i in xrange(L) ] 
      Mu_a_init  = [ np.array(Mu_a[k]) for k in xrange(Ka) ]
      Sig_a_init = [ np.array(Sig_a[k]) for k in xrange(Ka) ]
      Mu_p_init  = [ np.array(Mu_p[k]) for k in xrange(Kp) ]
      Sig_p_init = [ np.array(Sig_p[k]) for k in xrange(Kp) ]
      Mu_o_init  = [ np.array(Mu_o[k]) for k in xrange(Ko) ]
      Sig_o_init = [ np.array(Sig_o[k]) for k in xrange(Ko) ]
      Mu_c_init  = [ np.array(Mu_c[k]) for k in xrange(Kc) ]
      Sig_c_init = [ np.array(Sig_c[k]) for k in xrange(Kc) ]
      pi_a_init = [pi_a[k] for k in xrange(Ka)]
      pi_p_init = [pi_p[k] for k in xrange(Kp)]
      pi_o_init = [pi_o[k] for k in xrange(Ko)]
      pi_c_init = [pi_c[k] for k in xrange(Kc)]
      
      ### save initial values 
      #filename_init = filename + "/init"
      trialname_init = "init/" + trialname 
      para_save(foldername,trialname_init,filename,za_init,zp_init,zo_init,zc_init,Fd_init,theta_init,W_list,Mu_a_init,Sig_a_init,Mu_p_init,Sig_p_init,Mu_o_init,Sig_o_init,Mu_c_init,Sig_c_init,pi_a_init,pi_p_init,pi_o_init,pi_c_init)
      
      ######################################################################
      ####                     ↓ Learning phase ↓                       ####
      ######################################################################
      print u"- <START> Learning of Lexicon and Multiple Categories ver. iCub MODEL. -"
      
      for iter in xrange(num_iter):   #Iteration of Gibbs sampling
        print '----- Iter. '+repr(iter+1)+' -----'
        
        ########## ↓ ##### Sampling za ##### ↓ ##########
        print u"Sampling za..."
        
        for d in xrange(D):         #for each sentence
          temp = np.array(pi_a)
          for k in xrange(Ka):      #for each index of category
            for n in xrange(N[d]):  #for each word in a sentence
              if Fd[d][n] == "a":
                temp[k] = temp[k] * theta[k + dict["a"]][W_list.index(w_dn[d][n])]
            temp[k] = temp[k] * multivariate_normal.pdf(a_d[d], mean=Mu_a[k], cov=Sig_a[k])
          
          temp = temp / np.sum(temp)  #正規化
          za[d] = list(multinomial(1,temp)).index(1)
        print za
        ########## ↑ ##### Sampling za ##### ↑ ##########
        
        ########## ↓ ##### Sampling zp ##### ↓ ##########
        print u"Sampling zp..."
        
        for d in xrange(D):         #for each sentence
          for m in xrange(M[d]):    #for each obect
            temp = np.array(pi_p)
            for k in xrange(Kp):      #for each index of category
              for n in xrange(N[d]):  #for each word in a sentence
                if Fd[d][n] == "p" and Ad[d] == m:
                  temp[k] = temp[k] * theta[k + dict["p"]][W_list.index(w_dn[d][n])]
              temp[k] = temp[k] * multivariate_normal.pdf(p_dm[d][m], mean=Mu_p[k], cov=Sig_p[k])
            
            temp = temp / np.sum(temp)  #正規化
            zp[d][m] = list(multinomial(1,temp)).index(1)
        print zp
        ########## ↑ ##### Sampling zp ##### ↑ ##########
        
        ########## ↓ ##### Sampling zo ##### ↓ ##########
        print u"Sampling zo..."
        
        for d in xrange(D):         #データごとに
          for m in xrange(M[d]):    #物体ごとに
            temp = np.array(pi_o)
            logtemp = np.array([log(pi_o[k]) for k in xrange(Ko)])
            for k in xrange(Ko):      #カテゴリ番号ごとに
              for n in xrange(N[d]):  #文中の単語ごとに
                if Fd[d][n] == "o" and Ad[d] == m:
                  #temp[k] = temp[k] * theta[k + dict["o"]][W_list.index(w_dn[d][n])]
                  logtemp[k] = logtemp[k] + log(theta[k + dict["o"]][W_list.index(w_dn[d][n])])
              loggauss = multivariate_normal.logpdf(o_dm[d][m], mean=Mu_o[k], cov=Sig_o[k])
              #print loggauss
              logtemp[k] = logtemp[k] + loggauss#multivariate_normal.pdf(o_dm[d][m], mean=Mu_o[k], cov=Sig_o[k])
            
            logtemp = logtemp - np.max(logtemp)
            logtemp = logtemp - sp.misc.logsumexp(logtemp)#log(np.sum(np.array([exp(logtemp[k]) for k in xrange(Ko)])))  #正規化
            #print logtemp,sp.misc.logsumexp(logtemp)
            #print np.exp(logtemp),np.sum(np.exp(logtemp))
            zo[d][m] = list( multinomial(1,np.exp(logtemp)) ).index(1)
        print zo
        ########## ↑ ##### Sampling zo ##### ↑ ##########
        
        ########## ↓ ##### Sampling zc ##### ↓ ##########
        print u"Sampling zc..."
        
        for d in xrange(D):         #データごとに
          for m in xrange(M[d]):    #物体ごとに
            temp = np.array(pi_c)
            for k in xrange(Kc):      #カテゴリ番号ごとに
              for n in xrange(N[d]):  #文中の単語ごとに
                if Fd[d][n] == "c" and Ad[d] == m:
                  #print temp
                  temp[k] = temp[k] * theta[k + dict["c"]][W_list.index(w_dn[d][n])]
                  #print temp
              temp[k] = temp[k] * multivariate_normal.pdf(c_dm[d][m], mean=Mu_c[k], cov=Sig_c[k])
              #print temp[k],multivariate_normal.pdf(c_dm[d][m], mean=Mu_c[k], cov=Sig_c[k])
            #print temp
            temp = temp / np.sum(temp)  #正規化
            #print temp
            zc[d][m] = list(multinomial(1,temp)).index(1)
        print zc
        ########## ↑ ##### Sampling zc ##### ↑ ##########
        
        ########## ↓ ##### π_aのサンプリング ##### ↓ ##########
        print u"Sampling PI_a..."
        
        cc = collections.Counter(za)
        if nonpara == 0:
          temp = np.array([cc[k] + alpha_a for k in xrange(Ka)])
        elif nonpara == 1:
          temp = np.array([cc[k] + (alpha_a / float(Ka)) for k in xrange(Ka)])
        
        #加算したデータとパラメータから事後分布を計算しサンプリング
        pi_a = dirichlet(temp)
        print pi_a
        ########## ↑ ##### π_aのサンプリング ##### ↑ ##########
        
        ########## ↓ ##### π_pのサンプリング ##### ↓ ##########
        print u"Sampling PI_p..."
        
        cc = np.sum([collections.Counter(zp[d]) for d in range(D)])
        if nonpara == 0:
          temp = np.array([cc[k] + alpha_p for k in xrange(Kp)])
        elif nonpara == 1:
          temp = np.array([cc[k] + (alpha_p / float(Kp)) for k in xrange(Ka)])
        
        #加算したデータとパラメータから事後分布を計算しサンプリング
        pi_p = dirichlet(temp)
        print pi_p
        ########## ↑ ##### π_pのサンプリング ##### ↑ ##########
        
        ########## ↓ ##### π_oのサンプリング ##### ↓ ##########
        print u"Sampling PI_o..."
        
        cc = np.sum([collections.Counter(zo[d]) for d in range(D)])
        if nonpara == 0:
          temp = np.array([cc[k] + alpha_o for k in xrange(Ko)])
        elif nonpara == 1:
          temp = np.array([cc[k] + (alpha_o / float(Ko)) for k in xrange(Ka)]) 
        
        #加算したデータとパラメータから事後分布を計算しサンプリング
        pi_o = dirichlet(temp)
        print pi_o
        ########## ↑ ##### π_oのサンプリング ##### ↑ ##########
        
        ########## ↓ ##### π_cのサンプリング ##### ↓ ##########
        print u"Sampling PI_c..."
        
        cc = np.sum([collections.Counter(zc[d]) for d in range(D)])
        if nonpara == 0:
          temp = np.array([cc[k] + alpha_c for k in xrange(Kc)])
        elif nonpara == 1:
          temp = np.array([cc[k] + (alpha_c / float(Kc)) for k in xrange(Ka)])
        
        #加算したデータとパラメータから事後分布を計算しサンプリング
        pi_c = dirichlet(temp)
        print pi_c
        ########## ↑ ##### π_cのサンプリング ##### ↑ ##########
        
        ########## ↓ ##### μa,Σa(ガウス分布の平均、共分散行列)のサンプリング ##### ↓ ##########
        print u"Sampling myu_a,Sigma_a..."
        
        cc = collections.Counter(za)
        for k in xrange(Ka) : 
          nk = cc[k]
          xt = []
          m_ML = np.zeros(dim_a)
          ###kについて、zaが同じものを集める
          if nk != 0 :  #もしzaの中にkがあれば(計算短縮処理)        ##0ワリ回避
            for d in xrange(D) : 
              if za[d] == k : 
                xt = xt + [ np.array(a_d[d]) ]
            
            m_ML = sum(xt) / float(nk) #fsumではダメ
            #print "n:%d m_ML:%s" % (nk,str(m_ML))
            print "a%d n:%d" % (k,nk)
            
            ##ハイパーパラメータ更新
            kN = k0a + nk
            mN = ( k0a*m0a + nk*m_ML ) / kN  #dim_a 次元横ベクトル
            nN = n0a + nk
            VN = V0a + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0a*nk/kN)*np.dot(np.array([m_ML-m0a]).T,np.array([m_ML-m0a]))
            
            ##3.1##Σを逆ウィシャートからサンプリング
            Sig_a[k] = invwishart.rvs(df=nN, scale=VN) #/ n0a
            ##3.2##μを多変量ガウスからサンプリング
            Mu_a[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_a[k]/kN) for i in xrange(100)],0) #サンプリングをロバストに
          else:  #データがないとき
            Mu_a[k]  = np.array([uniform(mu_a_init[0],mu_a_init[1]) for i in xrange(dim_a)])
            Sig_a[k] = invwishart.rvs(df=n0a, scale=V0a )#np.eye(dim_a)*sig_a_init
          
          
          
          if (nk != 0):  #データなしは表示しない
            print 'Mu_a '+str(k)+' : '+str(Mu_a[k])
            print 'Sig_a'+str(k)+':\n'+str(Sig_a[k])
          
          #print [(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]
          #print [np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]
          #print sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)])
          #print ( float(k0a*nk)/kN ) * np.dot(np.array([m_ML - m0a]).T,np.array([m_ML - m0a]))
          #print VN
          #samp_sig_rand = np.array([ invwishart(nuN,VN) for i in xrange(100)])    ######
          #samp_sig = np.mean(samp_sig_rand,0)
          #print samp_sig
          
          #if np.linalg.det(samp_sig) < -0.0:
          #  Sig_a[k] = np.mean(np.array([ invwishartrand(nuN,VN)]),0)
          
          #print ''
          #for k in xrange(K):
          #if (nk[k] != 0):  #データなしは表示しない
          #  print 'Sig_a'+str(k)+':'+str(Sig_a[k])
          
        ########## ↑ ##### μa,Σa(ガウス分布の平均、共分散行列)のサンプリング ##### ↑ ##########
        
        ########## ↓ ##### μp,Σp(ガウス分布の平均、共分散行列)のサンプリング ##### ↓ ##########
        print u"Sampling myu_p,Sigma_p..."
        
        cc = np.sum([collections.Counter(zp[d]) for d in range(D)])
        for k in xrange(Kp) : 
          nk = cc[k]
          xt = []
          m_ML = np.zeros(dim_p)
          ###kについて、zaが同じものを集める
          if nk != 0 :  #もしzaの中にkがあれば(計算短縮処理)        ##0ワリ回避
            for d in xrange(D) : 
              for m in xrange(M[d]):
                if zp[d][m] == k : 
                  xt = xt + [ np.array(p_dm[d][m]) ]
            
            m_ML = sum(xt) / float(nk) #fsumではダメ
            #print "n:%d m_ML:%s" % (nk,str(m_ML))
            print "p%d n:%d" % (k,nk)
            
            ##ハイパーパラメータ更新
            kN = k0p + nk
            mN = ( k0p*m0p + nk*m_ML ) / kN  #dim_a 次元横ベクトル
            nN = n0p + nk
            VN = V0p + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0p*nk/kN)*np.dot(np.array([m_ML-m0p]).T,np.array([m_ML-m0p]))
            
            ##3.1##Σを逆ウィシャートからサンプリング
            Sig_p[k] = invwishart.rvs(df=nN, scale=VN) #/ n0a
            ##3.2##μを多変量ガウスからサンプリング
            Mu_p[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_p[k]/kN) for i in xrange(100)],0) #サンプリングをロバストに
          else:  #データがないとき
            Mu_p[k]  = np.array([uniform(mu_p_init[0],mu_p_init[1]) for i in xrange(dim_p)])
            Sig_p[k] = invwishart.rvs(df=n0p, scale=V0p ) #np.eye(dim_p)*sig_p_init
          
          
          if (nk != 0):  #データなしは表示しない
            print 'Mu_p '+str(k)+' : '+str(Mu_p[k])
            print 'Sig_p'+str(k)+':\n'+str(Sig_p[k])
          
        ########## ↑ ##### μp,Σp(ガウス分布の平均、共分散行列)のサンプリング ##### ↑ ##########
        
        ########## ↓ ##### μo,Σo(ガウス分布の平均、共分散行列)のサンプリング ##### ↓ ##########
        print u"Sampling myu_o,Sigma_o..."
        
        cc = np.sum([collections.Counter(zo[d]) for d in range(D)])
        for k in xrange(Ko) : 
          nk = cc[k]
          xt = []
          m_ML = np.zeros(dim_o)
          ###kについて、zaが同じものを集める
          if nk != 0 :  #もしzaの中にkがあれば(計算短縮処理)        ##0ワリ回避
            for d in xrange(D) : 
              for m in xrange(M[d]):
                if zo[d][m] == k : 
                  xt = xt + [ np.array(o_dm[d][m]) ]
            
            m_ML = sum(xt) / float(nk) #fsumではダメ
            #print "n:%d m_ML:%s" % (nk,str(m_ML))
            print "o%d n:%d" % (k,nk)
            
            ##ハイパーパラメータ更新
            kN = k0o + nk
            mN = ( k0o*m0o + nk*m_ML ) / kN  #dim_a 次元横ベクトル
            nN = n0o + nk
            VN = V0o + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0o*nk/kN)*np.dot(np.array([m_ML-m0o]).T,np.array([m_ML-m0o]))
            
            ##3.1##Σを逆ウィシャートからサンプリング
            Sig_o[k] = invwishart.rvs(df=nN, scale=VN) #/ n0a
            ##3.2##μを多変量ガウスからサンプリング
            Mu_o[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_o[k]/kN) for i in xrange(100)],0) #サンプリングをロバストに
          else:  #データがないとき
            Mu_o[k]  = np.array([uniform(mu_o_init[0],mu_o_init[1]) for i in xrange(dim_o)])
            Sig_o[k] = invwishart.rvs(df=n0o, scale=V0o ) #np.eye(dim_o)*sig_o_init
          
          if (nk != 0):  #データなしは表示しない
            print 'Mu_o '+str(k)+' : '+str(Mu_o[k])
            print 'Sig_o'+str(k)+':\n'+str(Sig_o[k])
          
        ########## ↑ ##### μo,Σo(ガウス分布の平均、共分散行列)のサンプリング ##### ↑ ##########
        
        ########## ↓ ##### μc,Σc(ガウス分布の平均、共分散行列)のサンプリング ##### ↓ ##########
        print u"Sampling myu_c,Sigma_c..."
        
        cc = np.sum([collections.Counter(zc[d]) for d in range(D)])
        for k in xrange(Kc) : 
          nk = cc[k]
          xt = []
          m_ML = np.zeros(dim_c)
          ###kについて、zaが同じものを集める
          if nk != 0 :  #もしzaの中にkがあれば(計算短縮処理)        ##0ワリ回避
            for d in xrange(D) : 
              for m in xrange(M[d]):
                if zc[d][m] == k : 
                  xt = xt + [ np.array(c_dm[d][m]) ]
            
            m_ML = sum(xt) / float(nk) #fsumではダメ
            #print "n:%d m_ML:%s" % (nk,str(m_ML))
            print "c%d n:%d" % (k,nk)
            
            ##ハイパーパラメータ更新
            kN = k0c + nk
            mN = ( k0c*m0c + nk*m_ML ) / kN  #dim_a 次元横ベクトル
            nN = n0c + nk
            VN = V0c + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0c*nk/kN)*np.dot(np.array([m_ML-m0c]).T,np.array([m_ML-m0c]))
            
            ##3.1##Σを逆ウィシャートからサンプリング
            Sig_c[k] = invwishart.rvs(df=nN, scale=VN) #/ n0a
            ##3.2##μを多変量ガウスからサンプリング
            Mu_c[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_c[k]/kN) for i in xrange(100)],0) #サンプリングをロバストに
          else:  #データがないとき
            Mu_c[k]  = np.array([uniform(mu_c_init[0],mu_c_init[1]) for i in xrange(dim_c)])
            Sig_c[k] = invwishart.rvs(df=n0c, scale=V0c ) #np.eye(dim_c)*sig_c_init
          
          if (nk != 0):  #データなしは表示しない
            print 'Mu_c '+str(k)+' : '+str(Mu_c[k])
            print 'Sig_c'+str(k)+':\n'+str(Sig_c[k])
          
        ########## ↑ ##### μc,Σc(ガウス分布の平均、共分散行列)のサンプリング ##### ↑ ##########
        
        ########## ↓ ##### Fdのサンプリング ##### ↓ ##########
        print u"Sampling Fd..."
        #基本的にデータごとの単語数におけるモダリティの組み合わせ全探索する
        
        for d in xrange(D):
          F_temp = [f for f in itertools.permutations(modality,N[d])]  ##モダリティの順列組み合わせ
          temp = [1.0 for i in xrange(len(F_temp))]  ##フレームの組み合わせ数分の要素を用意する
          for i in xrange(len(F_temp)):
            for n in xrange(N[d]):
              #print i,n,N[d],M[d]
              if F_temp[i][n] == "a":
                temp[i] = temp[i] * theta[za[d]                   ][W_list.index(w_dn[d][n])]
              if F_temp[i][n] == "p":
                temp[i] = temp[i] * theta[zp[d][Ad[d]] + dict["p"]][W_list.index(w_dn[d][n])]
              if F_temp[i][n] == "o":
                temp[i] = temp[i] * theta[zo[d][Ad[d]] + dict["o"]][W_list.index(w_dn[d][n])]
              if F_temp[i][n] == "c":
                temp[i] = temp[i] * theta[zc[d][Ad[d]] + dict["c"]][W_list.index(w_dn[d][n])]
          temp = temp / np.sum(temp)  #正規化
          Fd[d] = F_temp[list(multinomial(1,temp)).index(1)]
          print d, Fd[d]
        
        ########## ↑ ##### Fdのサンプリング ##### ↑ ##########
        
        ########## ↓ ##### Sampling Θ ##### ↓ ##########
        print u"Sampling Theta..."
        #dict = {"a":0, "p":Ka, "o":Ka+Kp, "c":Ka+Kp+Ko}   #各モダリティのindexにキーを足すとΘのindexになる
        
        temp = [np.array([gamma for w in xrange(W)]) for i in xrange(L)]
        for d in xrange(D):
            for n in xrange(N[d]):
              if (Fd[d][n] == "a"):
                temp[za[d]]                   [W_list.index(w_dn[d][n])] = temp[za[d]]                   [W_list.index(w_dn[d][n])] + 1
              if (Fd[d][n] == "p"):
                temp[zp[d][Ad[d]] + dict["p"]][W_list.index(w_dn[d][n])] = temp[zp[d][Ad[d]] + dict["p"]][W_list.index(w_dn[d][n])] + 1
              if (Fd[d][n] == "o"):
                temp[zo[d][Ad[d]] + dict["o"]][W_list.index(w_dn[d][n])] = temp[zo[d][Ad[d]] + dict["o"]][W_list.index(w_dn[d][n])] + 1
              if (Fd[d][n] == "c"):
                temp[zc[d][Ad[d]] + dict["c"]][W_list.index(w_dn[d][n])] = temp[zc[d][Ad[d]] + dict["c"]][W_list.index(w_dn[d][n])] + 1
          
        #Sampling from the posterior distribution calculated by the added data and hyperparameter
        theta = [sum(dirichlet(temp[i],100))/100.0 for i in xrange(L)] ##ロバストネスを上げる100
        
        print theta
        ########## ↑ ##### Sampling Θ ##### ↑ ##########
        print "" 
      
      ######################################################################
      ####                     ↑ Learning phase ↑                       ####
      ######################################################################
      
      
      loop = 1
      ########  ↓Files output↓  ########
      if loop == 1:
        print "--------------------"
        #最終学習結果を出力
        print u"- <COMPLETED> Learning of Lexicon and Multiple Categories ver. iCub MODEL. -"
        #print 'Sample: ' + str(sample)
        print 'za: ' + str(za)
        print 'zp: ' + str(zp)
        print 'zo: ' + str(zo)
        print 'zc: ' + str(zc)
        for d in xrange(D):
          print 'Fd%d: %s' % (d, str(Fd[d]))
        for c in xrange(Ka):
          print "theta_a%d: %s" % (c,theta[c + dict["a"]])
        for c in xrange(Kp):
          print "theta_p%d: %s" % (c,theta[c + dict["p"]])
        for c in xrange(Ko):
          print "theta_o%d: %s" % (c,theta[c + dict["o"]])
        for c in xrange(Kc):
          print "theta_c%d: %s" % (c,theta[c + dict["c"]])
        for k in xrange(Ka):
          print "mu_a%d: %s" % (k, str(Mu_a[k]))
        for k in xrange(Kp):
          print "mu_p%d: %s" % (k, str(Mu_p[k]))
        for k in xrange(Ko):
          print "mu_o%d: %s" % (k, str(Mu_o[k]))
        for k in xrange(Kc):
          print "mu_c%d: %s" % (k, str(Mu_c[k]))
        #for k in xrange(K):
        #  print "sig%d: \n%s" % (k, str(Sig_a[k]))
        print 'pi_a: ' + str(pi_a)
        print 'pi_p: ' + str(pi_p)
        print 'pi_o: ' + str(pi_o)
        print 'pi_c: ' + str(pi_c)
        
        print "--------------------"
        
        #Saving parameters to files
        para_save(foldername,trialname,filename,za,zp,zo,zc,Fd,theta,W_list,Mu_a,Sig_a,Mu_p,Sig_p,Mu_o,Sig_o,Mu_c,Sig_c,pi_a,pi_p,pi_o,pi_c)
        
      ########  ↑Files output↑  ######## 
      

if __name__ == '__main__':
    import sys
    import shutil
    from __init__ import *
    
    #filename = sys.argv[1]
    #print filename
    
    #出力ファイル名を要求
    #filename = raw_input("trialname?(folder) >")
    
    trialname = raw_input("trialname?(folder) >")
    start = raw_input("start number?>")
    end   = raw_input("end number?>")
    filename = raw_input("learning trial name?>")
    
    sn = int(start)
    en = int(end)
    Data = int(en) - int(sn) +1
    
    if D != Data:
      print "data number error.",D,Data
      exit()
    
    foldername = datafolder + trialname+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"
    
    #make folder
    Makedir( foldername + "/" + filename )
    Makedir( foldername + "/" + filename + "/init")
    
    #Copy of init.py
    shutil.copy("./__init__.py", foldername + "/" + filename + "/init")
    
    #Reading data files (単語、切り出した物体特徴と色と位置、姿勢と触覚と手先位置)
    M, N, w_dn, a_d, p_dm, o_dm, c_dm, Ad = data_read(trialname,filename,sn,en)
    #print w_dn
    
    #Gibbs sampling
    simulate(foldername,trialname,filename,sn,en, M, N, w_dn, a_d, p_dm, o_dm, c_dm, Ad)
    

########################################
