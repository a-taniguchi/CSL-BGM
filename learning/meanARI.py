#coding:utf-8
#ARI
#Akira Taniguchi 2016/06/20
#!/usr/bin/env python
import sys
import string
#from sklearn.metrics.cluster import adjusted_rand_score
#import matplotlib.pyplot as plt
import numpy as np
from __init__ import *
#import matplotlib.pyplot as plt
#import numpy as np
#import math

trialname = "testss"
trial_se = "(001-040)"#raw_input("trialname?(folder) >")
start = raw_input("start number?>")
end   = raw_input("end number?>")
filename1 = raw_input("learning trial name?(before)>")#"001"#
filename2 = raw_input("learning trial name?(after)>")#"001"#

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname + trial_se#+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"


#MI_M = [[] for c in xrange(N)]
ARI_a_M = [[] for c in xrange(Data)]
ARI_p_M = [[] for c in xrange(Data)]
ARI_o_M = [[] for c in xrange(Data)]
ARI_c_M = [[] for c in xrange(Data)]
#PARs_M = [[] for c in xrange(N)]
#PARw_M = [[] for c in xrange(N)]
#MM = [ np.array([[] for m in xrange(10) ]) for n in xrange(N)]
#MM_M = 

fp = open(foldername + '/' + filename1 + str(sn).zfill(3) + "-" + str(en).zfill(3) + filename2 + '_avgARI.csv', 'w')
#fp.write('MI,ARI,PARs,PARw\n')

#i = 0
#MI_MAX = [[0,0]] 
#ARI_MAX = [[0,0]]
#PARs_MAX = [[0,0]]
#PARw_MAX = [[0,0]]

for s in range(Data):
  i = 0
  filename = filename1 + str(s+sn).zfill(3) + filename2
  for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_ARI.csv', 'r'):
    itemList = line[:-1].split(',')
    if (i != 0) and (itemList[0] != ''):
      #print i,itemList
      #MI_M[s] = MI_M[s] + [float(itemList[0])]
      ARI_a_M[s] = ARI_a_M[s] + [float(itemList[0])]
      ARI_p_M[s] = ARI_p_M[s] + [float(itemList[1])]
      ARI_o_M[s] = ARI_o_M[s] + [float(itemList[2])]
      ARI_c_M[s] = ARI_c_M[s] + [float(itemList[3])]
      #PARs_M[s] = PARs_M[s] + [float(itemList[2])]
      #PARw_M[s] = PARw_M[s] + [float(itemList[3])]
      #if (float(itemList[0]) > MI_MAX[0][1]):
      #    MI_MAX = [[s+1,float(itemList[0])]] + MI_MAX
      #if (float(itemList[1]) > ARI_MAX[0][1]):
      #    ARI_MAX = [[s+1,float(itemList[1])]] + ARI_MAX
      #if (float(itemList[3]) > PARw_MAX[0][1]):
      #    PARw_MAX = [[s+1,float(itemList[3])]] + PARw_MAX
    i = i + 1
    #print MI_M[s]
    #for i in xrange(len(itemList)):
    #   if itemList[i] != '':
         
    #MM[s] = MM[s] + [[float(itemList[0]),float(itemList[1]),float(itemList[2]),float(itemList[3])]]
    #ARI = adjusted_rand_score(CtC, Ct)
    #print str(ARI)
    #ARI_M = ARI_M + ARI
  #MI_M[s] = np.array(MI_M[s])
  ARI_a_M[s] = np.array(ARI_a_M[s])
  ARI_p_M[s] = np.array(ARI_p_M[s])
  ARI_o_M[s] = np.array(ARI_o_M[s])
  ARI_c_M[s] = np.array(ARI_c_M[s])
  #PARs_M[s] = np.array(PARs_M[s])
  #PARw_M[s] = np.array(PARw_M[s])
  #if (MI_M[s][-1] > MI_MAX[0][1]):
  #        MI_MAX = [[s+1,MI_M[s][-1]]] + MI_MAX
  #if (ARI_M[s][-1] > ARI_MAX[0][1]):
  #        ARI_MAX = [[s+1,ARI_M[s][-1]]] + ARI_MAX
  #if (PARw_M[s][-1] > PARw_MAX[0][1]):
  #        PARw_MAX = [[s+1,PARw_M[s][-1]]] + PARw_MAX
  #if (PARs_M[s][-1] > PARs_MAX[0][1]):
  #        PARs_MAX = [[s+1,PARs_M[s][-1]]] + PARs_MAX

#print "MI_MAX:",MI_MAX
#print "ARI_MAX:",ARI_MAX
#print "PARw_MAX:",PARw_MAX
#print "PARs_MAX:",PARs_MAX
#print MI_M
#MM_M = sum(MM)/N
#MI_MM = sum(MI_M)/N
ARI_a_MM = sum(ARI_a_M)/Data
ARI_p_MM = sum(ARI_p_M)/Data
ARI_o_MM = sum(ARI_o_M)/Data
ARI_c_MM = sum(ARI_c_M)/Data
#PARw_MM = sum(PARw_M)/N
#PARs_MM = sum(PARs_M)/N
#print MI_MM
#MI,ARI,PARs,PARw,

fp.write('ARI_a,ARI_p,ARI_o,ARI_c\n')
fp.write(repr(ARI_a_MM[0])+','+repr(ARI_p_MM[0])+','+repr(ARI_o_MM[0])+','+repr(ARI_c_MM[0])+'\n')
fp.write( str(np.std(ARI_a_M, ddof=1))+','+ str(np.std(ARI_p_M, ddof=1))+','+ str(np.std(ARI_o_M, ddof=1))+','+str(np.std(ARI_c_M, ddof=1)) )
fp.write('\n')

print('ARI_a,ARI_p,ARI_o,ARI_c\n')
print(repr(ARI_a_MM[0])+'\n'+repr(ARI_p_MM[0])+'\n'+repr(ARI_o_MM[0])+'\n'+repr(ARI_c_MM[0])+'\n')
print( str(np.std(ARI_a_M, ddof=1))+'\n'+ str(np.std(ARI_p_M, ddof=1))+'\n'+ str(np.std(ARI_o_M, ddof=1))+'\n'+str(np.std(ARI_c_M, ddof=1)) )


#for iteration in xrange(len(MI_MM)):
#  fp.write( str(MI_MM[iteration])+','+ str(ARI_MM[iteration])+','+ str(PARs_MM[iteration])+','+str(PARw_MM[iteration]) )
#  fp.write('\n')
#fp.write('\n')

#for iteration in xrange(10):
#  MI_MS = np.array([MI_M[s][iteration] for s in xrange(N)])
#  MI_std = np.std(MI_MS, ddof=1)
#  #print MI_std

#for iteration in xrange(len(MI_MM)):
#  MI_MS = np.array([MI_M[s][iteration] for s in xrange(N)])
#  ARI_MS = np.array([ARI_M[s][iteration] for s in xrange(N)])
#  PARs_MS = np.array([PARs_M[s][iteration] for s in xrange(N)])
#  PARw_MS = np.array([PARw_M[s][iteration] for s in xrange(N)])
#  #print iteration,np.std(MI_MS, ddof=1)
#  fp.write( str(np.std(MI_MS, ddof=1))+','+ str(np.std(ARI_MS, ddof=1))+','+ str(np.std(PARs_MS, ddof=1))+','+str(np.std(PARw_MS, ddof=1)) )
#  fp.write('\n')
#np.std
#float(ARI_M / N)
#print "ARI mean"
#print str(ARI_M)
print "close."

fp.close()
