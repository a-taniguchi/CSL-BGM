# -*- coding: utf-8 -*-
# Multimodal Learning of spatial prepositions and object categories (For test)
# Akira Taniguchi 2017/03/27

import os
import sys
import collections
import itertools
import numpy as np
import scipy as sp
#import matplotlib.pyplot as plt
from numpy.random import multinomial,uniform,dirichlet
from scipy.stats import multivariate_normal,invwishart,rv_discrete
from math import pi as PI
from math import cos,sin,sqrt,exp,log,fabs,fsum,degrees,radians,atan2
from __init__ import *



def Makedir(dir):
    try:
        os.mkdir( dir )
    except:
        pass


def data_read(Test_folder):
    #foldername = datafolder + filename
    O = 0
    N = 0
    w_i =  []  # the set of sentences # The sentence is the set of words.
    zt_i = []  # the set of POS tags
    d_c =  []  # the set of dyadic spatial configurations (e.g., centroid A - centroid B)
    f_c =  []  # the set of object features
    centroid = []
    
    ##reading the set of the number of objects and centroids for each sentences
    #Read current centroids data
    o_count = 0
    while (os.path.exists( datafolder+Centroids+Test_folder+"/Centroid_Object_" +str(o_count)+".txt" ) == True):
        o_count += 1
    O = int(o_count)
    
    #o = 0  # object index in d-th sentence
    for o in xrange(O):
        for line in open(datafolder+Centroids+Test_folder+"/Centroid_Object_" +str(o)+".txt",'r'):
          itemList = line[:-1].split('  ')
          if itemList[0] != '':
            #Reading centroid
            centroid += [[float(itemList[0]),float(itemList[1]),float(itemList[2])]]  #(x,y,z)
        print o,centroid[o]
        #o = o + 1
    #O[d] = int(o)
    
    f_c = [ [ 0 for k in xrange(dim_f) ] for m in xrange(O) ]
    d_c = [ [ [ 0 for k in xrange(dim_d) ] for o2 in xrange(O) ] for o1 in xrange(O) ]
    
    #From centroids to d_c
    for o1 in xrange(O):
        for o2 in xrange(O):
          if o1 != o2:
            d_c[o1][o2] = np.array(centroid[o1]) - np.array(centroid[o2])  #o1(reference)->o2(landmark)
    
    
    ##reading the set of object features for each sentences
    o = 0  # object index in d-th sentence
    #for m in xrange(O[d]):
    ##reading object features
    dim = 0
    for line in open(datafolder+Object_features+Test_folder+"/VFH_Object_Descriptor_" + str(o) + ".txt", 'r'):
          itemList = line#[:-1].split(',')
          #for i in xrange(len(itemList)):
          if itemList != '':
              #print c,i,itemList[i]
              f_c[o][dim] = float(itemList)
              dim += 1
    #Normalization of object feature histograms
    """
    sum_f_c = sum(f_c[o])
    for i in xrange(len(f_c[o])):
            f_c[o][i] = f_c[o][i] / float(sum_f_c)
    """
    
    #reading training sentences (words)
    #d = 0
    for line in open(datafolder+Sentence, 'r'):
        itemList = line[:-1].split(' ')
        for i in xrange(len(itemList)):
            if (itemList[i] != ''):
              w_i = w_i + [str(itemList[i])]
              N = N + 1
        #d = d + 1
    print w_i
    
    
    #reading POS tag data
    #d = 0
    for line in open(datafolder+POS_tag, 'r'):
        itemList = line[:-1].split(' ')
        for i in xrange(len(itemList)):
            if (itemList[i] != ''): #and (d < M):
              zt_i = zt_i + [int(itemList[i])]
        #d = d + 1
    print zt_i
    
    
    ###################
    return O, N, w_i, d_c, f_c, zt_i
    

def para_read(foldername,filename):
    foldername = foldername + "/" + filename
    W_list = []
    for line in open(foldername +'/' + filename +'_W_list.csv', 'r'):
      line = line.replace("'", "")
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        if itemList[i] != '':
          W_list = W_list + [itemList[i]]
    
    print W_list
    W = len(W_list)  ##単語の種類数のカウント
    theta = [ [0.0 for w in xrange(W)] for i in xrange(L) ] #indexと各モダリティーの対応付けはdictionary形式で呼び出す
    
    i = 0
    for line in open(foldername +'/' + filename +'_theta.csv', 'r'):
      itemList = line[:-1].split(',')
      for w in xrange(len(theta[i])):
        theta[i][w] = float(itemList[w])
      i = i + 1
      
    Mu_d  = [ np.array([0.0 for i in xrange(dim_d)]) for k in xrange(Kd) ]
    Sig_d = [ np.eye(dim_d) for k in xrange(Kd) ]
    k = 0
    for line in open(foldername +'/' + filename +'_Mu_d.csv', 'r'):
      itemList = line[:-1].split(',')
      for dim in xrange(len(Mu_d[k])):
        Mu_d[k][dim] = float(itemList[dim])
      k = k + 1
    k = 0
    dim1 = 0
    for line in open(foldername +'/' + filename +'_Sig_d.csv', 'r'):
      itemList = line[:-1].split(',')
      if dim1 != dim_d:
        for dim2 in xrange(len(Sig_d[k][dim1])):
          Sig_d[k][dim1][dim2] = float(itemList[dim2])
        dim1 = dim1 + 1
      else:
        dim1 = 0
        k = k + 1
    
    Mu_f  = [ np.array([0.0 for i in xrange(dim_f)]) for k in xrange(Kf) ]
    Sig_f = [ np.eye(dim_f) for k in xrange(Kf) ]
    k = 0
    for line in open(foldername +'/' + filename +'_Mu_f.csv', 'r'):
      itemList = line[:-1].split(',')
      for dim in xrange(len(Mu_f[k])):
        Mu_f[k][dim] = float(itemList[dim])
      k = k + 1
    k = 0
    dim1 = 0
    for line in open(foldername +'/' + filename +'_Sig_f.csv', 'r'):
      itemList = line[:-1].split(',')
      if dim1 != dim_f:
        for dim2 in xrange(len(Sig_f[k][dim1])):
          Sig_f[k][dim1][dim2] = float(itemList[dim2])*dim_f
        dim1 = dim1 + 1
      else:
        dim1 = 0
        k = k + 1
    
    pi_d = [ alpha_d for c in xrange(Kd)] 
    for line in open(foldername +'/' + filename +'_pi_d.csv', 'r'):
      itemList = line[:-1].split(',')
      for k in xrange(Kd):
        pi_d[k] = float(itemList[k])
      
    pi_f = [ alpha_f for c in xrange(Kf)] 
    for line in open(foldername +'/' + filename +'_pi_f.csv', 'r'):
      itemList = line[:-1].split(',')
      for k in xrange(Kf):
        pi_f[k] = float(itemList[k])
    
    pi_t = [ sum(dirichlet([ lambda0 for mod in xrange(len(modality))],1))/1.0 for t in xrange(K) ]
    k = 0
    for line in open(foldername +'/' + filename +'_pi_t.csv', 'r'):
      itemList = line[:-1].split(',')
      for mod in xrange(len(modality)):
          #print itemList[mod]
          pi_t[k][mod] = float(itemList[mod])
      k += 1
    
    return theta,W_list,Mu_d,Sig_d,Mu_f,Sig_f,pi_d,pi_f,pi_t
    

filename = "trial13_60"#str(M)    ###raw_input("Raading folder name in Learning_Data?(60) >") #M=60 ## it will be trial number

foldername = datafolder + Learningfolder


Read_folder = "Test_2"  #raw_input("testdata_folder? >") "Test1_"
#Reading data files
O, N, w_i, d_c, f_c, zt_c = data_read(Read_folder)
theta,W_list,Mu_d,Sig_d,Mu_f,Sig_f,pi_d,pi_f,pi_t = para_read(foldername,filename)



argmax_ci = [[-1,-1] for n in range(N)]
argmax_mi = ["" for n in range(N)]
#referent -1

prob_ci_mi = [ [ [0.0 for o in xrange( O*O )] for m in xrange(len(modality)) ] for i in xrange(N) ] 
prob_i = [0.0 for i in xrange(N)]

print "Estimate mi and ci"
######Estimate argmax_{ci,mi} P(ci,mi| zt_c,pi_t,theta, pi_d,pi_f,d_c,f_c,phi_d,phi_f)
for i in xrange(N):
  for mod in xrange(len(modality)):
    modal_name = modality[mod]
    for ci in xrange(O*O):
      o1 = ci / O
      o2 = ci % O
      if o1 != o2: #O*(O-1)
        prob_ci_mi[i][mod][ci] = pi_t[zt_c[i]][mod]
        if   modal_name == "d":
          logtemp = [1.0 for k in xrange(Kd)]
          for zd in xrange(Kd):
            Zc = zd
            temp = theta[Zc + dict[modal_name]][W_list.index(w_i[i])]
            logtemp[zd] = log(temp) + log(pi_d[zd]) + multivariate_normal.logpdf(d_c[o1][o2], mean=Mu_d[zd], cov=Sig_d[zd])
          prob_ci_mi[i][mod][ci] *= sum(np.exp(logtemp)) 
          #print o1,o2,sum(np.exp(logtemp)) 
        elif modal_name == "f":
          logtemp2 = [1.0 for k in xrange(Kf)]
          #max_logtemp = 0.0
          for zf in xrange(Kf):
            Zc = zf
            temp = theta[Zc + dict[modal_name]][W_list.index(w_i[i])]
            logtemp2[zf] = log(temp) + log(pi_f[zf]) + multivariate_normal.logpdf(f_c[o1], mean=Mu_f[zf], cov=Sig_f[zf]) /dim_f 
          prob_ci_mi[i][mod][ci] *= sum(np.exp(logtemp2)) 
        else: #"g"
          Zc = 0
          temp = theta[Zc + dict[modal_name]][W_list.index(w_i[i])]
          prob_ci_mi[i][mod][ci] *= temp
          
    if (modal_name == "d"):
      prob_i[i] = sum(prob_ci_mi[i][mod])
  
  print i,prob_ci_mi[i]
  ###最大の要素を探す ########
  max_ci_mi = np.array(prob_ci_mi[i]).max()
  #print "max_ci_mi", max_ci_mi
  for mod in xrange(len(modality)):
    for ci in xrange(O*O):
      if max_ci_mi == prob_ci_mi[i][mod][ci]:
         argmax_ci[i] = [ci / O, ci % O]
         argmax_mi[i] = mod
  
  print i,argmax_mi[i]
  print i,argmax_ci[i]

max_i = np.array(prob_i).max()
argmax_i = prob_i.index(max_i)
print "argmax_i",argmax_i

#make folder
Makedir( datafolder + Test_folder )
Makedir( datafolder + Test_folder + Read_folder)

####File output
fp = open(datafolder + Test_folder + Read_folder + '/argmax_mi.csv', 'w')
for n in xrange(len(argmax_mi)):
  fp.write(repr(modality[argmax_mi[n]]) + ',')
fp.write('\n')
fp.close()

####File output
fp = open(datafolder + Test_folder + Read_folder + '/argmax_mi_value.csv', 'w')
for n in xrange(len(argmax_mi)):
  fp.write(repr(argmax_mi[n]) + ',')
fp.write('\n')
fp.close()

####File output
fp = open(datafolder + Test_folder + Read_folder + '/argmax_ci.csv', 'w')
for n in xrange(len(argmax_ci)):
  for i in xrange(len(argmax_ci[n])):
    fp.write(repr(argmax_ci[n][i]) + ',')
  fp.write('\n')
fp.close()

####File output
fp = open(datafolder + Test_folder + Read_folder + '/argmax_referent.csv', 'w')
fp.write(repr(argmax_i))
fp.write('\n')
fp.close()

####File output
fp = open(datafolder + Test_folder + Read_folder + '/prob_referent.csv', 'w')
for n in xrange(len(prob_i)):
  fp.write(repr(prob_i[n]) + ',')
fp.write('\n')
fp.close()
