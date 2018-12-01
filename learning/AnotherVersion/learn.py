#coding:utf-8

import os
import random
import collections
import itertools
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from numpy.random import multinomial,uniform,dirichlet,randint
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

def data_read(filename):
    foldername = datafolder + filename
    
    O = [0 for d in xrange(M)]   # the set of the number of objects
    N = [0 for d in xrange(M)]   # the set of the number of words
    w_i =  [ [] for d in xrange(M) ]  # the set of sentences # The sentence is the set of words.
    zt_i = [ [] for d in xrange(M) ]  # the set of POS tags
    a_p =  [ [] for d in xrange(M) ]  # the set of actions
    c_p =  [ [] for d in xrange(M) ]  # the set of object color
    s_p =  [ [] for d in xrange(M) ]  # the set of spatial configurations (e.g., centroid A - centroid B)
    g_p =  [ [] for d in xrange(M) ]  # the set of object geometry
    centroid_Before = centroid_After = [ [] for d in xrange(M) ]     

    ##reading the set of the number of objects and centroids for each sentences
    for d in xrange(M):
      #Read current centroids data
      o_count = 0
      while (os.path.exists(datafolder+Centroids+ "Experiment_" + str(d+1) + "/Centroid_Object_" + str(o_count) + "_Before" +".txt" ) == True):
        o_count += 1
      O[d] = int(o_count)
      
      #o = 0  # object index in d-th sentence  
      for o in xrange(O[d]):
        for line in open(datafolder+Centroids+ "Experiment_" + str(d+1) + "/Centroid_Object_" + str(o) + "_Before" + ".txt",'r'): 
          itemList = line[:-1].split('  ')
          if itemList[0] != '':
            #Reading centroid
            centroid_Before[d] += [[float(itemList[0]),float(itemList[1]),float(itemList[2])]]  #(x,y,z)   [[Amir: centroid [d] or centroid [d][o]]]?? (before it was [d] and i made it [d][o])
            # [[Akira: If Array = [o1,o2], Array += [o3]  ->  Array is [o1,o2,o3]. ]]
        """
        for line in open(datafolder+Centroids+ "Experiment_" + str(d+1) + "/Centroid_Object_" + str(o) + "_After" + ".txt",'r'): 
          itemList = line[:-1].split('  ')
          if itemList[0] != '':
            #Reading centroid
            centroid_After [d] += [[float(itemList[0]),float(itemList[1]),float(itemList[2])]]  #(x,y,z)                         [[Amir: I change it to centroid [d][o]]]??
        """

        print d,o,centroid_Before [d] #, centroid_After [d]                                                                                          

    for d in xrange(M):  
      g_p[d] = [ [ 0 for k in xrange(dim_g) ] for m in xrange(O[d]) ]
      s_p[d] = [ [ [ 0 for k in xrange(dim_s) ] for o2 in xrange(O[d]) ] for o1 in xrange(O[d]) ]  # [[Amir:I added 1 to consider the relationship between objects AFTER manipulation]]                  
      #[[Akira:I deleted after manipulation. ]]
    
    #From centroids to s_p
    for d in xrange(M):
      for o1 in xrange(O[d]):
        for o2 in xrange(O[d]):
          if (o1 != o2) : #& (o2 != O[d]):
            s_p[d][o1][o2] = np.array(centroid_Before[d][o1]) - np.array(centroid_Before[d][o2])  #o1(reference)->o2(landmark) 
          #elif (o2 == O[d]):   
          #  s_p[d][o1][o2] = np.array(centroid_After[d][o1])  - np.array(centroid_After[d][o2])   #o1(reference)->o2(landmark) 
    
    print d, s_p[d] 
    ## ************* Reading Color Data ***************************************
     
    for d in xrange(M):      
      if (os.path.exists(datafolder + Object_color + "Experiment_"+str(d+1) + "/RGB_Object_0" + ".txt") ):
           RGB_File = datafolder + Object_color + "Experiment_"+str(d+1) + "/RGB_Object_0" + ".txt"
           Object_index=0
      else: 
           RGB_File = datafolder + Object_color + "Experiment_"+str(d+1) + "/RGB_Object_1" + ".txt"
           Object_index=1

      RGB_values = sum(np.loadtxt (RGB_File, dtype='float')) 
      dim_c= len( RGB_values )  #[[Akira: It is 3 dim. ([R,G,B])]]
      #************************
      k0c = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
      m0c = np.zeros(dim_c)              #Hyperparameter of mean vector of the Gaussian distribution
      V0c = np.eye(dim_c)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
      n0c = dim_c + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_c)
      #************************
      c_p[d] = [ [ 0 for k in xrange(dim_c) ] for m in xrange(O[d]) ]  
      
      if  Object_index == 0:                 
        c_p[d][Object_index]=  RGB_values / float(sum(RGB_values))  #Normalization of RGB histograms
        c_p[d][Object_index+1]=  [-1,-1,-1]  ##[[Akira : If It is an empty array, This code becomes error.]]
      else:        
        c_p[d][Object_index]=  RGB_values / float(sum(RGB_values))  #Normalization of RGB histograms
        c_p[d][Object_index-1]=  [-1,-1,-1]


      print d, c_p[d] 

    ## **************Reading Action Data **************************************
       
    for d in xrange(M):

      #Shoulder_values = np.loadtxt (datafolder+Action+"Experiment_"+str(d+1)+"/Trial_1"+"Left_shoulder.txt", dtype='float') 
      #Elbow_values = np.loadtxt (datafolder+Action+"Experiment_"+str(d+1)+"/Trial_1"+"Left_elbow.txt", dtype='float') 
      #Hand_values = np.loadtxt (datafolder+Action+"Experiment_"+str(d+1)+"/Trial_1"+"Left_elbow.txt", dtype='float')  #[[Akira: Please change to states of HMM.]]
      Test_states = [0,0,1,1,1,2,2,2,2]
      cc_a = collections.Counter(Test_states)
      
      global dim_a  ##[Akira : Here is in "data_read" function. It needs to "global". ]]
      global k0a 
      global m0a
      global V0a
      global n0a
      
      dim_a = len( cc_a ) #  #[[Akira: Please change to the number of categories in action states of HMM. (like a POS tag states)]]
      #************************      
      k0a = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
      m0a = np.zeros(dim_a)              #Hyperparameter of mean vector of the Gaussian distribution
      V0a = np.eye(dim_a)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
      n0a = dim_a + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_a)
      #************************
      a_p[d]= [ cc_a[k] for k in xrange(dim_a) ] # a_p[d] is dim_a dimensional vector. (one-dimensional array of the number of elements dim_a)
      #Normalization of action state histograms
      sum_a_p = sum(a_p[d]) 
      for i in xrange(len(a_p[d])):
         a_p[d][i] = a_p[d][i] / float(sum_a_p)
      
      #a_p[d][0]=Shoulder_values 
      #a_p[d][1]= Elbow_values 
      #a_p[d][2]=Hand_values        
      print d, a_p[d] 

    ## ************************************************************************

    ##reading the set of object features for each sentences
    for d in xrange(M):
      o = 0  # object index in d-th sentence
      for o in xrange(O[d]):        
        dim = 0
        for line in open(datafolder+Object_geometry+"Experiment_"+str(d+1)+"/VFH_Object_" + str(o) + ".txt", 'r'):
          itemList = line          
          if itemList != '':              
              g_p[d][o][dim] = float(itemList)
              dim += 1
        #Normalization of object feature histograms
        normalize_fc = 0
        if (normalize_fc == 1):
          sum_g_p = max(g_p[d][o]) 
          for i in xrange(len(g_p[d][o])):
            g_p[d][o][i] = g_p[d][o][i] / float(sum_g_p)
      print d, g_p[d]  
    
    #reading training sentences (words)
    d = 0
    for line in open(datafolder+Sentences, 'r'):
        itemList = line[:-1].split(' ')
        for i in xrange(len(itemList)):
            if (itemList[i] != '') and (d < M):
              w_i[d] = w_i[d] + [str(itemList[i])]
              N[d] = N[d] + 1
        d = d + 1
    print w_i    
    
    #reading POS tag data
    d = 0
    for line in open(datafolder+POS_tags, 'r'):
        itemList = line[:-1].split(' ')
        for i in xrange(len(itemList)):
            if (itemList[i] != '') and (d < M):
              zt_i[d] = zt_i[d] + [int(itemList[i])]
        d = d + 1
    print zt_i        
    ###################
    return O, N, w_i, a_p, c_p, s_p, g_p, zt_i

def para_save(foldername,filename,za,zc,zs,zg,mi,theta,W_list,Mu_a,Sig_a,Mu_c,Sig_c,Mu_s,Sig_s,Mu_g,Sig_g,pi_a,pi_c,pi_s,pi_g,p_i,pi_t):
        
    #Saving each parameter
    fp = open(foldername +'/' + filename +'_za.csv', 'w')
    for d in xrange(M):
      #for m in xrange(len(za[d])):
      fp.write(repr(za[d])+',')                             #[[Amir: This writes the x,y,z paramters of the shoulder, elbow, hand concatenated??!!NOT SURE if this is correct]] #[[Akira: za is a latent state of action information]]
      fp.write('\n')
    fp.close()

    fp = open(foldername +'/' + filename +'_zc.csv', 'w')
    for d in xrange(M):
      for m in xrange(len(zc[d])):
        fp.write(repr(zc[d][m])+',')
      fp.write('\n')
    fp.close()

    fp = open(foldername +'/' + filename +'_zs.csv', 'w')
    for d in xrange(M):
      for o1 in xrange(len(zs[d])):
        for o2 in xrange(len(zs[d][o1])):
          fp.write(repr(zs[d][o1][o2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_zg.csv', 'w')
    for d in xrange(M):
      for m in xrange(len(zg[d])):
        fp.write(repr(zg[d][m])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_mi.csv', 'w')
    #fp.write('mi\n')
    for d in xrange(M):
      for f in xrange(len(mi[d])):
        fp.write(repr(mi[d][f])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_mi_value.csv', 'w')
    #fp.write('mi\n')
    for d in xrange(M):
      for f in xrange(len(mi[d])):
        fp.write(repr(modality.index(mi[d][f]))+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_theta.csv', 'w')
    #fp.write('theta\n')
    for i in xrange(L):
      for w in xrange(len(W_list)):
        fp.write(repr(theta[i][w])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_W_list.csv', 'w')
    for w in xrange(len(W_list)):
      fp.write(repr(W_list[w])+',')
    fp.write('\n')
    fp.close()
    
    
    fp = open(foldername +'/' + filename +'_Mu_a.csv', 'w')
    for k in xrange(Ka):     
      for dim in xrange(dim_a):
        fp.write(repr(Mu_a[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_Sig_a.csv', 'w')    
    for k in xrange(Ka):      
      for dim in xrange(dim_a):
        for dim2 in xrange(dim_a):
          fp.write(repr(Sig_a[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()

    fp = open(foldername +'/' + filename +'_Mu_c.csv', 'w')
    for k in xrange(Kc):     
      for dim in xrange(dim_c):
        fp.write(repr(Mu_c[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_Sig_c.csv', 'w')    
    for k in xrange(Kc):      
      for dim in xrange(dim_c):
        for dim2 in xrange(dim_c):
          fp.write(repr(Sig_c[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()

    fp = open(foldername +'/' + filename +'_Mu_s.csv', 'w')
    for k in xrange(Ks):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_s):
        fp.write(repr(Mu_s[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_Sig_s.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Ks):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_s):
        for dim2 in xrange(dim_s):
          fp.write(repr(Sig_s[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_Mu_g.csv', 'w')
    for k in xrange(Kg):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_g):
        fp.write(repr(Mu_g[k][dim])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_Sig_g.csv', 'w')
    #fp.write('Sig\n')
    for k in xrange(Kg):
      #fp.write(repr(k)+',')
      for dim in xrange(dim_g):
        for dim2 in xrange(dim_g):
          fp.write(repr(Sig_g[k][dim][dim2])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
   
    fp = open(foldername +'/' + filename +'_pi_a.csv', 'w')    
    for k in xrange(Ka):
      fp.write(repr(pi_a[k])+',')
    fp.write('\n')
    fp.close()

    fp = open(foldername +'/' + filename +'_pi_c.csv', 'w')   
    for k in xrange(Kc):
      fp.write(repr(pi_c[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_pi_s.csv', 'w')
    #fp.write('pi_s'+',')
    for k in xrange(Ks):
      fp.write(repr(pi_s[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_pi_g.csv', 'w')
    #fp.write('pi_g'+',')
    for k in xrange(Kg):
      fp.write(repr(pi_g[k])+',')
    fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_pi_t.csv', 'w')
    for i in xrange(K):
      for m in xrange(len(modality)):
        fp.write(repr(pi_t[i][m])+',')
      fp.write('\n')
    fp.close()
    
    fp = open(foldername +'/' + filename +'_pi.csv', 'w')
    for d in xrange(M):
      for n in xrange(len(p_i[d])):
        for o in xrange(len(p_i[d][n])):
          fp.write(repr(p_i[d][n][o])+',')
        fp.write('\n')
      fp.write('\n')
    fp.close()
    #if object0 is referent and object1 is landmark, p_i[d][n]=[0,1] 
    
    print 'File Output Successful!(filename:'+foldername+')\n'    
    

# Simulation
def simulate(foldername,filename, O, N, w_i, a_p, c_p, s_p, g_p, zt_p): 
      np.random.seed()
      #print w_i
      print u"Initialize Parameters..."
      za = [ [ int(uniform(0,Ka)) for o in xrange(3)] for d in xrange(M) ] #random initialzation       [[Amir: 3 articulations]] # [[Akira: How do you represent feature vector of action information?]]
      zc = [ [ int(uniform(0,Kc)) for o in xrange(O[d]) ] for d in xrange(M) ] #random initialzation
      zs = [ [ [ int(uniform(0,Ks))*int(o1!=o2)-int(o1==o2) for o2 in xrange(O[d]) ] for o1 in xrange(O[d]) ] for d in xrange(M) ] #random initialzation  # if(o1 == o2): zs[d][o1][o2] = -1 (Exception)
      zg = [ [ int(uniform(0,Kg)) for o in xrange(O[d]) ] for d in xrange(M) ] #random initialzation
      
      mi = [ Sample_Frame_Random(N[d]) for d in xrange(M)] #random initialzation ("a", "c", "s","g","t")
      pi_list = [list(c) for c in itertools.permutations(range(O[d]),2)] 
      #p_i = [ [ [int(uniform(0,O[d])), int(uniform(0,O[d]))] for i in xrange(N[d]) ] for d in xrange(M) ]  
      p_i = [ [pi_list[randint(0,len(pi_list))] for i in xrange(N[d]) ] for d in xrange(M) ]  #the set of object dyadic-layout selection # A->B is [0,1] # A is a regerent object, B is a landmark
      
      cw = np.sum([collections.Counter(w_i[d]) for d in xrange(M)])
      W_list = list(cw)  ##List of words
      W = len(cw)  ##Length of word list
      theta = [ sum(dirichlet(np.array([gamma for w in xrange(W)]),1))/1.0 for i in xrange(L) ] 
      #[ dirichlet(np.array([gamma for w in xrange(W)])) for i in xrange(L) ] 
      ka_temp = Ka
      kc_temp = Kc
      Ks_temp = Ks
      Kg_temp = Kg

      #*********************************
      a_temp = []
      for d in xrange(M):
        #for o in xrange(3):                        # [[Amir: 3 articulations?? Please have a look on how the Shoulder,Elbow,Hand data are read]] # [[Akira: How do you represent feature vector of action information?]] 
        a_temp.append(a_p[d])
      if (len(a_temp) <= Ka): 
        Ka_temp = len(a_temp)
      a_temp = np.array(a_temp)     
      Mu_a  = KMeans(n_clusters=Ka_temp, init='k-means++').fit(a_temp).cluster_centers_ 
      for k in xrange(Ka):
        if (len(Mu_a) < Ka):
          Mu_a = np.append(Mu_a,np.array([[uniform(mu_a_init[0],mu_a_init[1]) for i in xrange(dim_a)]]), axis=0)
      Sig_a = [ np.eye(dim_a)*sig_a_init for k in xrange(Ka) ]
      #*********************************
      c_temp = []
      for d in xrange(M):
        for o in xrange(O[d]):
          if (c_p[d][o][0] != -1 and c_p[d][o][1] != -1 and c_p[d][o][2] != -1):
            c_temp.append(c_p[d][o])
      if (len(c_temp) <= Kc): 
        Kc_temp = len(c_temp)
      c_temp = np.array(c_temp)     
      Mu_c  = KMeans(n_clusters=Kc_temp, init='k-means++').fit(c_temp).cluster_centers_ 
      for k in xrange(Kc):
        if (len(Mu_c) < Kc):
          Mu_c = np.append(Mu_c,np.array([[uniform(mu_c_init[0],mu_c_init[1]) for i in xrange(dim_c)]]), axis=0)
      Sig_c = [ np.eye(dim_c)*sig_c_init for k in xrange(Kc) ]
      #*********************************

      s_temp = []
      for d in xrange(M):
        for o1 in xrange(len(s_p[d])):
          for o2 in xrange(len(s_p[d][o1])):
            s_temp.append(s_p[d][o1][o2])
      if (len(s_temp) <= Ks): 
        Ks_temp = len(s_temp)
      s_temp = np.array(s_temp)
      #print Ks_temp,s_temp
      Mu_s  = KMeans(n_clusters=Ks_temp, init='k-means++').fit(s_temp).cluster_centers_
      #Mu_s = []
      for k in xrange(Ks):
        if (len(Mu_s) < Ks):
          Mu_s= np.append(Mu_s,np.array([[uniform(mu_s_init[0],mu_s_init[1]) for i in xrange(dim_s)]]), axis=0)
        #print len(Mu_s),Mu_s
      Sig_s = [ np.eye(dim_s)*sig_s_init for k in xrange(Ks) ]
      
      g_temp = []
      for d in xrange(M):
        for o in xrange(O[d]):
          g_temp.append(g_p[d][o])
      if (len(g_temp) <= Kg): 
        Kg_temp = len(g_temp)
      g_temp = np.array(g_temp)     
      Mu_g  = KMeans(n_clusters=Kg_temp, init='k-means++').fit(g_temp).cluster_centers_ #[np.array([uniform(mu_g_init[0],mu_g_init[1]) for i in xrange(dim_g)]) for k in xrange(Kg)] #
      for k in xrange(Kg):
        if (len(Mu_g) < Kg):
          Mu_g= np.append(Mu_g,np.array([[uniform(mu_g_init[0],mu_g_init[1]) for i in xrange(dim_g)]]), axis=0)
      Sig_g = [ np.eye(dim_g)*sig_g_init for k in xrange(Kg) ]
      
      pi_a = sum(dirichlet([ alpha_a for c in xrange(Ka)],1))/1.0 #stick_breaking(gamma, L)# 
      pi_c = sum(dirichlet([ alpha_c for c in xrange(Kc)],1))/1.0 #stick_breaking(gamma, L)#
      pi_s = sum(dirichlet([ alpha_s for c in xrange(Ks)],1))/1.0 #stick_breaking(gamma, L)#
      pi_g = sum(dirichlet([ alpha_g for c in xrange(Kg)],1))/1.0 #stick_breaking(gamma, L)#
      
      cc_zt = np.sum([collections.Counter(zt_p[d]) for d in range(M)])
      #K = len(cc_zt)   # the number of tag states
      pi_t = [ sum(dirichlet([ lambda0 for mod in xrange(len(modality))],1))/1.0 for t in xrange(K) ]
      
      print za
      print zc
      print zs
      print zg
      print theta
      print pi_a
      print pi_c
      print pi_s
      print pi_g
      print Mu_a
      print Mu_c
      print Mu_s
      print Mu_g
      print mi
      print p_i      
      
      ######################################################################
      ####                       ↓Learning↓                           ####
      ######################################################################
      print u"- <START> Multimodal Learning of spatial prepositions and object categories -"
      
      for iter in xrange(num_iter):   #Iteration of Gibbs sampling
        print '----- Iter. '+repr(iter+1)+' -----'
        
        ########## ↓ ##### Sampling zs ##### ↓ ##########ok
        print u"Sampling zs..."
        for d in xrange(M):          #for each sentence
          for o1 in xrange(O[d]):    #for each obect (referent)
            for o2 in xrange(O[d]):   #for each obect (landmark)
              temp = np.array(pi_s)
              if o1 != o2:   #O*(O-1)
                for k in xrange(Ks):      #for each index of category
                  for n in xrange(N[d]):  #for each word in a sentence
                    if (mi[d][n] == "s") and (p_i[d][n][0] == o1) and (p_i[d][n][1] == o2):  #
                      temp[k] *= theta[k + dict["s"]][W_list.index(w_i[d][n])]
                  #print k,d,o1,o2,len(s_p[d][o1][o2]),len(Mu_s[k]),s_p[d][o1][o2],Mu_s[k]
                  temp[k] *= multivariate_normal.pdf(s_p[d][o1][o2], mean=Mu_s[k], cov=Sig_s[k])
                
                temp = temp / np.sum(temp)  
                zs[d][o1][o2] = list(multinomial(1,temp)).index(1)
        print zs
        ########## ↑ ##### Sampling zs ##### ↑ ##########
        
        ########## ↓ ##### Sampling zg ##### ↓ ##########
        print u"Sampling zg..."
        for d in xrange(M):         #for each sentence
          for o1 in xrange(O[d]):    #for each obect
            #temp = np.array(pi_g)
            logtemp = np.array([log(pi_g[k]) for k in xrange(Kg)])
            for k in xrange(Kg):      #for each index of category
              for n in xrange(N[d]):  #for each word in a sentence
                if (mi[d][n] == "g") and (p_i[d][n][0] == o1): 
                  logtemp[k] += log(theta[k + dict["g"]][W_list.index(w_i[d][n])])
              logtemp[k] += multivariate_normal.logpdf(g_p[d][o1], mean=Mu_g[k], cov=Sig_g[k]) 
            
            logtemp = logtemp - np.max(logtemp)
            logtemp = logtemp - sp.misc.logsumexp(logtemp)
            zg[d][o1] = list( multinomial(1,np.exp(logtemp)) ).index(1)
        print zg
        ########## ↑ ##### Sampling zg ##### ↑ ##########        
        
        #[[Akira: I added sampling code of z_c.]]
        ########## ↓ ##### Sampling zc ##### ↓ ##########
        print u"Sampling zc..."
        for d in xrange(M):         #for each sentence
          for o1 in xrange(O[d]):    #for each obect
            logtemp = np.array([log(pi_c[k]) for k in xrange(Kc)])
            for k in xrange(Kc):      #for each index of category
              for n in xrange(N[d]):  #for each word in a sentence
                if (mi[d][n] == "c") and (p_i[d][n][0] == o1):  #
                  logtemp[k] += log(theta[k + dict["c"]][W_list.index(w_i[d][n])])
              if (c_p[d][o1][0] != -1 and c_p[d][o1][1] != -1 and c_p[d][o1][2] != -1):
                logtemp[k] += multivariate_normal.logpdf(c_p[d][o1], mean=Mu_c[k], cov=Sig_c[k]) 
            
            logtemp = logtemp - np.max(logtemp)
            logtemp = logtemp - sp.misc.logsumexp(logtemp)
            zc[d][o1] = list( multinomial(1,np.exp(logtemp)) ).index(1)
        print zc
        ########## ↑ ##### Sampling zc ##### ↑ ##########        
        
        #[[Akira: I added sampling code of z_a.]]
        ########## ↓ ##### Sampling za ##### ↓ ##########
        print u"Sampling za..."
        for d in xrange(M):         #for each sentence
            logtemp = np.array([log(pi_a[k]) for k in xrange(Ka)])
            for k in xrange(Ka):      #for each index of category
              for n in xrange(N[d]):  #for each word in a sentence
                if (mi[d][n] == "a"): # and (p_i[d][n][0] == o1): 
                  logtemp[k] += log(theta[k + dict["a"]][W_list.index(w_i[d][n])])
              logtemp[k] += multivariate_normal.logpdf(a_p[d], mean=Mu_a[k], cov=Sig_a[k]) 
            
            logtemp = logtemp - np.max(logtemp)
            logtemp = logtemp - sp.misc.logsumexp(logtemp)
            za[d] = list( multinomial(1,np.exp(logtemp)) ).index(1)
        print za
        ########## ↑ ##### Sampling zc ##### ↑ ##########        
        
        ########## ↓ ##### Sampling π_s ##### ↓ ##########
        print u"Sampling PI_s..."
        cc_zs = np.sum([ np.sum([collections.Counter(zs[d][o1]) for o1 in xrange(O[d])]) for d in range(M) ])
        temp = np.array([cc_zs[k] + alpha_s for k in xrange(Ks)])
        
        #Sampling of pi_s from the posterior distribution calculated by the added data and hyperparameter
        pi_s = dirichlet(temp)
        print pi_s
        ########## ↑ ##### Sampling π_s ##### ↑ ##########
        
        ########## ↓ ##### Sampling π_g ##### ↓ ##########
        print u"Sampling PI_g..."
        cc_zg = np.sum([collections.Counter(zg[d]) for d in range(M)])
        temp = np.array([cc_zg[k] + alpha_g for k in xrange(Kg)])
        
        #Sampling of pi_g from the posterior distribution calculated by the added data and hyperparameter
        pi_g = dirichlet(temp)
        print pi_g
        ########## ↑ ##### Sampling π_g ##### ↑ ############       
        
        #[[Akira: I added sampling code of pi_c.]]
        ########## ↓ ##### Sampling π_c ##### ↓ ##########
        print u"Sampling PI_c..."
        cc_zc = np.sum([collections.Counter(zc[d]) for d in range(M)])
        temp = np.array([cc_zc[k] + alpha_c for k in xrange(Kc)])
        
        #Sampling of pi_g from the posterior distribution calculated by the added data and hyperparameter
        pi_c = dirichlet(temp)
        print pi_c
        ########## ↑ ##### Sampling π_c ##### ↑ ############       
        
        #[[Akira: I added sampling code of pi_a.]]
        ########## ↓ ##### Sampling π_a ##### ↓ ##########
        print u"Sampling PI_a..."
        
        cc = collections.Counter(za)
        temp = np.array([cc[k] + alpha_a for k in xrange(Ka)])
        
        #加算したデータとパラメータから事後分布を計算しサンプリング
        pi_a = dirichlet(temp)
        print pi_a
        ########## ↑ ##### Sampling π_a ##### ↑ ##########
        
        ########## ↓ ##### Sampling μd,Σd ##### ↓ ##########
        print u"Sampling mu_s,Sigma_s..."
        #cc = np.sum([collections.Counter(zg[d]) for d in range(M)])
        for k in xrange(Ks): 
          nk = cc_zs[k]
          xt = []
          m_ML = np.zeros(dim_s)
          if nk != 0 : 
            for d in xrange(M) : 
              for o1 in xrange(O[d]):
                for o2 in xrange(O[d]):
                  if (zs[d][o1][o2] == k) and (o1 != o2): 
                    xt = xt + [ np.array(s_p[d][o1][o2]) ]
            
            m_ML = sum(xt) / float(nk) 
            print "p%d n:%d m_ML:%s" % (k,nk,str(m_ML))
            
            #Hyperparameter of the posterior distribution
            kN = k0s + nk
            mN = ( k0s*m0s + nk*m_ML ) / kN  
            nN = n0s + nk
            VN = V0s + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0s*nk/kN)*np.dot(np.array([m_ML-m0s]).T,np.array([m_ML-m0s]))
            
            ##3.1##Sampling Σ from Inverse-Wishart distribution
            Sig_s[k] = invwishart.rvs(df=nN, scale=VN) 
            ##3.2##Sampling μ from Gaussian distribution
            Mu_s[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_s[k]/kN) for i in xrange(10)],0) 
          else:  # if the category k is not allocated to data
            Mu_s[k]  = np.array([uniform(mu_s_init[0],mu_s_init[1]) for i in xrange(dim_s)])
            Sig_s[k] = np.eye(dim_s)*sig_s_init #invwishart.rvs(df=n0s, scale=V0s ) #np.eye(dim_s)*sig_s_init
          
          if (nk != 0): 
            print 'Mu_s'+str(k)+' : '+str(Mu_s[k])
            print 'Sig_s'+str(k)+':\n'+str(Sig_s[k])
        ########## ↑ ##### Sampling μd,Σd ##### ↑ ##########
        
        ########## ↓ ##### Sampling μf,Σf ##### ↓ ##########  
        print u"Sampling mu_g,Sigma_g..."
        #cc = np.sum([collections.Counter(zg[d]) for d in range(M)])
        for k in xrange(Kg): 
          nk = cc_zg[k]
          xt = []
          m_ML = np.zeros(dim_g)
          if nk != 0 : 
            for d in xrange(M) : 
              for m in xrange(O[d]):
                if zg[d][m] == k : 
                  xt = xt + [ np.array(g_p[d][m]) ]
            
            m_ML = sum(xt) / float(nk) 
            #print "p%d n:%d m_ML:%s" % (k,nk,str(m_ML))
            
            #Hyperparameter of the posterior distribution
            kN = k0g + nk
            mN = ( k0g*m0g + nk*m_ML ) / kN 
            nN = n0g + nk
            VN = V0g + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0g*nk/kN)*np.dot(np.array([m_ML-m0g]).T,np.array([m_ML-m0g]))
            
            ##3.1##Sampling Σ from Inverse-Wishart distribution
            Sig_g[k] = invwishart.rvs(df=nN, scale=VN) 
            ##3.2##Sampling μ from Gaussian distribution
            Mu_g[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_g[k]/kN) for i in xrange(1)],0) 
          else:  # if the category k is not allocated to data
            Mu_g[k]  = np.array([uniform(mu_g_init[0],mu_g_init[1]) for i in xrange(dim_g)])
            Sig_g[k] = np.eye(dim_g)*sig_g_init #invwishart.rvs(df=n0g, scale=V0g ) #
          
          if (nk != 0):  
            print 'Mu_g '+str(k)+' : '+str(Mu_g[k])
            print 'Sig_g'+str(k)+':\n'+str(Sig_g[k])
        ########## ↑ ##### Sampling μf,Σf ##### ↑ ##########        
        
        #[[Akira: I added sampling code of Mu_c and Sig_c.]]
        ########## ↓ ##### Sampling μc,Σc ##### ↓ ##########  
        print u"Sampling mu_c,Sigma_c..."
        #cc = np.sum([collections.Counter(zg[d]) for d in range(M)])
        for k in xrange(Kc): 
          nk = cc_zc[k]
          for d in xrange(M) : 
              for m in xrange(O[d]):
                if zc[d][m] == k : 
                  if (c_p[d][m][0] == -1 and c_p[d][m][1] == -1 and c_p[d][m][2] == -1):
                    nk= nk-1   
          xt = []
          m_ML = np.zeros(dim_c)
          if nk != 0 : 
            for d in xrange(M) : 
              for m in xrange(O[d]):
                if zc[d][m] == k : 
                  if (c_p[d][m][0] != -1 and c_p[d][m][1] != -1 and c_p[d][m][2] != -1):
                    xt = xt + [ np.array(c_p[d][m]) ]
                  
            
            m_ML = sum(xt) / float(nk) 
            print "p%d n:%d m_ML:%s" % (k,nk,str(m_ML))
            
            #Hyperparameter of the posterior distribution
            kN = k0c + nk
            #print k0c,m0c,nk,m_ML,kN
            mN = ( k0c*m0c + nk*m_ML ) / kN 
            nN = n0c + nk
            VN = V0c + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0c*nk/kN)*np.dot(np.array([m_ML-m0c]).T,np.array([m_ML-m0c]))
            
            ##3.1##Sampling Σ from Inverse-Wishart distribution
            Sig_c[k] = invwishart.rvs(df=nN, scale=VN) 
            ##3.2##Sampling μ from Gaussian distribution
            Mu_c[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_c[k]/kN) for i in xrange(1)],0) 
          else:  # if the category k is not allocated to data
            Mu_c[k]  = np.array([uniform(mu_c_init[0],mu_c_init[1]) for i in xrange(dim_c)])
            Sig_c[k] = np.eye(dim_c)*sig_c_init #invwishart.rvs(df=n0g, scale=V0g ) #
          
          if (nk != 0):  
            print 'Mu_c '+str(k)+' : '+str(Mu_c[k])
            print 'Sig_c'+str(k)+':\n'+str(Sig_c[k])
        ########## ↑ ##### Sampling μc,Σc ##### ↑ ##########        
        
        #[[Akira: I added sampling code of Mu_a and Sig_a.]]
        ########## ↓ ##### Sampling μa,Σa ##### ↓ ##########  
        print u"Sampling myu_a,Sigma_a..."
        
        cc = collections.Counter(za)
        for k in xrange(Ka) : 
          nk = cc[k]
          xt = []
          m_ML = np.zeros(dim_a)
          if nk != 0 : 
            for d in xrange(M) : 
              if za[d] == k : 
                xt = xt + [ np.array(a_p[d]) ]
            
            m_ML = sum(xt) / float(nk) 
            #print "n:%d m_ML:%s" % (nk,str(m_ML))
            print "a%d n:%d" % (k,nk)
            
            #Hyperparameter of the posterior distribution
            kN = k0a + nk
            mN = ( k0a*m0a + nk*m_ML ) / kN  
            nN = n0a + nk
            VN = V0a + sum([np.dot(np.array([xt[j]-m_ML]).T,np.array([xt[j]-m_ML])) for j in xrange(nk)]) + (k0a*nk/kN)*np.dot(np.array([m_ML-m0a]).T,np.array([m_ML-m0a]))
            
            ##3.1##Sampling Σ from Inverse-Wishart distribution
            Sig_a[k] = invwishart.rvs(df=nN, scale=VN) 
            ##3.2##Sampling μ from Gaussian distribution
            Mu_a[k] = np.mean([multivariate_normal.rvs(mean=mN, cov=Sig_a[k]/kN) for i in xrange(100)],0) 
          else:  # if the category k is not allocated to data
            Mu_a[k]  = np.array([uniform(mu_a_init[0],mu_a_init[1]) for i in xrange(dim_a)])
            Sig_a[k] = np.eye(dim_a)*sig_a_init #invwishart.rvs(df=n0a, scale=V0a )#
          
          if (nk != 0): 
            print 'Mu_a '+str(k)+' : '+str(Mu_a[k])
            print 'Sig_a'+str(k)+':\n'+str(Sig_a[k])
        ########## ↑ ##### Sampling μa,Σa ##### ↑ ##########        
        
        ########## ↓ ##### Sampling mi ##### ↓ #############
        print u"Sampling mi..."
        for d in xrange(M):
          for i in xrange(N[d]):
            temp = [1.0 for mod in xrange(len(modality))]
            for mod in range(len(modality)):
              #print d,i,N[d],mod
              modal_name = modality[mod]
              #if mi_temp[i][n] == mod:
              if   modal_name == "s":
                Zc = zs[d][p_i[d][i][0]][p_i[d][i][1]]
              elif modal_name == "g":
                Zc = zg[d][p_i[d][i][0]]
              elif modal_name == "a":   ##[[Akira: I added.]]
                Zc = za[d]
              elif modal_name == "c":   ##[[Akira: I added.]]
                Zc = zc[d][p_i[d][i][0]]
              else: #"t"
                Zc = 0
              
              temp[mod] = theta[Zc + dict[modal_name]][W_list.index(w_i[d][i])] * pi_t[zt_p[d][i]][mod]
            temp = temp / np.sum(temp)  #Normalization
            mi[d][i] = modality[list(multinomial(1,temp)).index(1)]
          print d, mi[d]
        ########## ↑ ##### Sampling mi ##### ↑ ##########
        
        ########## ↓ ##### Sampling p_i ##### ↓ ##########
        print u"Sampling p_i..."  # A->B is [0,1] # A is a regerent object, B is a landmark
        for d in xrange(M):
          for i in xrange(N[d]):
            temp = [delta for o in xrange( O[d]*O[d] )]
            #temp_referent = [delta for o in xrange( O[d] )]
            #temp_landmark = [delta for o in xrange( O[d] )]
            modal_name = mi[d][i]
            for o1 in xrange(O[d]):
              for o2 in xrange(O[d]):
                if o1 != o2: #O*(O-1)
                  if   modal_name == "s":
                    Zc = zs[d][o1][o2]
                  elif modal_name == "g":
                    Zc = zg[d][o1]
                  elif modal_name == "a":   ##[[Akira: I added.]]
                    Zc = za[d]
                  elif modal_name == "c":   ##[[Akira: I added.]]
                    Zc = zc[d][o1]
                  else: #"t"
                    Zc = 0
                  temp[o1*O[d]+o2] *= theta[Zc + dict[modal_name]][W_list.index(w_i[d][i])]
                  #temp_referent[o1] *= theta[Zc + dict[modal_name]][W_list.index(w_i[d][i])]
                  #temp_landmark[o2] *= theta[Zc + dict[modal_name]][W_list.index(w_i[d][i])]
                else: # o1 == o2
                  temp[o1*O[d]+o2] = 0.0
            temp_sum = sum(temp)
            temp = np.array(temp) / float(temp_sum)
            #print temp
            p_i_temp = list(multinomial(1,temp)).index(1)#list(multinomial(1,temp)).index(1)
            #print p_i_temp,O[d]
            p_i[d][i][0] = p_i_temp / O[d]
            p_i[d][i][1] = p_i_temp % O[d]
            #p_i[d][i][0] = multinomial(1,temp_referent)
            #p_i[d][i][1] = multinomial(1,temp_landmark)
            if modal_name == "c":
              for m in xrange(O[d]):
                if (c_p[d][m][0] != -1 and c_p[d][m][1] != -1 and c_p[d][m][2] != -1):
                  p_i[d][i][0] = m
        print p_i
        ########## ↑ ##### Sampling p_i ##### ↑ ##########
        
        ########## ↓ ##### Sampling Π_t ##### ↓ ##########
        print u"Sampling PI_t..." #Relationship of POS tags and modalities
        #cc_zt = np.sum([collections.Counter(zt[d]) for d in range(M)])
        #K = len(cc_zt)   # the number of tag states
        
        for t in xrange(K):
          temp = np.array([lambda0 for mod in xrange(len(modality))])
          for d in xrange(M):
            for i in xrange(N[d]):
              if zt_p[d][i] == t:
                temp[modality.index(mi[d][i])] += 1
          pi_t[t] = dirichlet(temp)
        
        print pi_t
        ########## ↑ ##### Sampling Π_t ##### ↑ ##########
        
        ########## ↓ ##### Sampling Θ ##### ↓ ##########
        print u"Sampling Theta..."
        temp = [np.array([gamma for w in xrange(W)]) for mz in xrange(L)]
        for d in xrange(M):
            for n in xrange(N[d]):
              modal_name = mi[d][n]
              #print d,n,p_i[d][n],modal_name
              if   modal_name == "s":
                Zc = zs[d][p_i[d][n][0]][p_i[d][n][1]]
              elif modal_name == "g":
                Zc = zg[d][p_i[d][n][0]]
              elif modal_name == "a":   ##[[Akira: I added.]]
                Zc = za[d]
              elif modal_name == "c":   ##[[Akira: I added.]]
                Zc = zc[d][p_i[d][n][0]]
              else: #"t"
                Zc = 0
              temp[Zc + dict[modal_name]][W_list.index(w_i[d][n])] += 1
        
        #Sampling from the posterior distribution calculated by the added data and hyperparameter
        theta = [sum(dirichlet(temp[i],10))/10.0 for i in xrange(L)]
        
        print theta
        ########## ↑ ##### Sampling Θ ##### ↑ ##########
        print "" 
      
      ######################################################################
      ####                       ↑Learning↑                           ####
      ######################################################################
      
      ########  ↓Files output↓  ########
      print_flag = 1
      if print_flag == 1:
        print "--------------------"        
        print u"- <COMPLETED> Multimodal Learning of spatial prepositions and object categories -"
        print 'zs: ' + str(zs)
        print 'zg: ' + str(zg)
        print 'za: ' + str(za)
        print 'zc: ' + str(zc)
        for d in xrange(M):
          print 'p_i%d: %s' % (d, str(p_i[d]))
          print 'mi%d: %s' % (d, str(mi[d]))
        for c in xrange(Ks):
          print "theta_d%d: %s" % (c,theta[c + dict["s"]])
        for c in xrange(Kg):
          print "theta_f%d: %s" % (c,theta[c + dict["g"]])
        for c in xrange(Ka):
          print "theta_a%d: %s" % (c,theta[c + dict["a"]])
        for c in xrange(Kc):
          print "theta_c%d: %s" % (c,theta[c + dict["c"]])
        for k in xrange(Ks):
          print "mu_s%d: %s" % (k, str(Mu_s[k]))
        for k in xrange(Kg):
          print "mu_g%d: %s" % (k, str(Mu_g[k]))
        for k in xrange(Ka):
          print "mu_a%d: %s" % (k, str(Mu_a[k]))
        for k in xrange(Kc):
          print "mu_c%d: %s" % (k, str(Mu_c[k]))
        print 'pi_s: ' + str(pi_s)
        print 'pi_g: ' + str(pi_g)
        print 'pi_a: ' + str(pi_a)
        print 'pi_c: ' + str(pi_c)
        
        print "--------------------"
        
      #Saving parameters to files
      para_save(foldername+filename,filename,za,zc,zs,zg,mi,theta,W_list,Mu_a,Sig_a,Mu_c,Sig_c,Mu_s,Sig_s,Mu_g,Sig_g,pi_a,pi_c,pi_s,pi_g,p_i,pi_t)
      
      ########  ↑Files output↑  ########      

if __name__ == '__main__':
    import sys
    import shutil
    from __init__ import *
    
    flag = True
    while (flag == True):  
           
      filename = raw_input("Output folder name? >")      
      foldername = datafolder + Learningfolder  
      
      #make folder
      Makedir( datafolder + Learningfolder )
      Makedir( foldername + filename )
      Makedir( foldername + filename + "/init")
      
      #Copy of init.py
      shutil.copy("./__init__.py", foldername + filename + "/init")
      
      #Reading data files
      O, N, w_i, a_p, c_p, s_p, g_p, zt_p = data_read(filename)    
      
      simulate(foldername,filename, O, N, w_i, a_p, c_p, s_p, g_p, zt_p) #Runing of Gibbs sampling
      flag = False
