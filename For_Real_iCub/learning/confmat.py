#coding:utf-8
#!/usr/bin/env python
#
#from pylab import *
import math
import itertools
import numpy as np
import pandas as pd
import seaborn as sn
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
from __init__ import *
#from sklearn import svm, datasets
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import confusion_matrix

sn.set_style("whitegrid", {'grid.linestyle': ' '})
current_palette = sn.color_palette()
#sn.set_palette("muted")

trialname = "ts" #param[1] #raw_input("trialname?(folder) >")
start = "001" #param[2] #raw_input("start number?>")
end   = raw_input("end number?(learned data)>") #param[3] #

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname + "("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"
learningname = raw_input("learning trial name?>")
"""
def print_cmx(y_true, y_pred):
    labels = ['grasp', 'touch', 'reach', 'look-at', 'front', 'left', 'right', 'red', 'green', 'blue', 'ball', 'box', 'cup']
#reach", \touch",\grasp", \lookat", \front", \left", \right", \far",green", \red", \blue", \box", \cup", \ball"
#sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred)#, labels=labels)
    
    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)

    plt.figure(figsize = (10,7))
    sn.heatmap(df_cmx, annot=True, cmap='Blues')
    tick_marks = np.arange(len(labels))
    plt.ylabel('True word')
    plt.xlabel('Predicted word')
    #plt.xticks(tick_marks, labels)
    plt.yticks()#rotation=90)
    plt.show()
"""
def plot_confusion_matrix(#cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    # Compute confusion matrix
    #cnf_matrix
    labels = ['grasp', 'touch', 'reach', 'look-at', 'front', 'far', 'right', 'red', 'green', 'blue', 'yellow', 'ball', 'car', 'cup', 'star']#sorted(list(set(y_true)))
    print labels
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    np.set_printoptions(precision=2)
    #classes = sorted(list(set(y_true)))
    
    
    #plt.title(title)
    
    
    #print(cm)
    if normalize:
        #cmsum = max([sum(cm[i]) for i in range(len(cm))])
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.figure(figsize = (9,7))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    """
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, cm[i, j],
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    """

    plt.colorbar()
    tick_marks = np.arange(len(labels))
    plt.xticks(tick_marks, labels)#, rotation=45)
    plt.yticks(tick_marks, labels)
    plt.tight_layout()
    plt.ylabel('True word')
    plt.xlabel('Predicted word')
    #plt.show()
    return cm



y_true = [] #["cat", "ant", "cat", "cat", "ant", "bird"]
y_pred = [] #["ant", "ant", "cat", "cat", "ant", "cat"]

#全１２文、全１０学習結果に対して
for d in xrange(1,10+1):
  filename = datafolder + "s/s" + str(d).zfill(3) + '/'
  for trial in xrange(1,10+1):
    #正解データの読み込み
    for line in open(filename + "argmax_w_dn_true.csv", 'r'):
      line = line.replace("\r", "")
      line = line.replace("look at", "look-at")
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        if (itemList[i] != ""):
          y_true += [itemList[i]]

    #推定されたデータの読み込み
    for line in open(filename + "argmax_w_dn_" + str(Data) + "_" + learningname + str(trial).zfill(3) + ".csv", 'r'):
      line = line.replace("\r", "")
      line = line.replace("look at", "look-at")
      itemList = line[:-1].split(',')
      for i in xrange(len(itemList)):
        if (itemList[i] != ""):
          y_pred += [itemList[i]]

print y_true
print y_pred

# Plot non-normalized confusion matrix
#plt.figure()
#plot_confusion_matrix(cnf_matrix, classes=class_names,
#                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
#cnf_matrix, classes=class_names, 
cm = plot_confusion_matrix(normalize=True)#,
#                      title='Normalized confusion matrix')
#print_cmx(y_true,y_pred)

######type 1 font#####
plt.rcParams['ps.useafm'] = True
plt.rcParams['pdf.use14corefonts'] = True
#plt.rcParams['text.usetex'] = True 

plt.savefig(foldername+'/'+ learningname + '_confmap.eps', dpi=300)
plt.savefig(foldername+'/'+ learningname + '_confmap.pdf', dpi=300)
plt.savefig(foldername+'/'+ learningname + '_confmap.png', dpi=300)

EARmat = np.diag(cm)
print EARmat
print sum(EARmat)/float(len(EARmat))

labels = ['grasp', 'touch', 'reach', 'look-at', 'front', 'far', 'right', 'red', 'green', 'blue', 'yellow', 'ball', 'car', 'cup', 'star']
####ファイル出力
fp = open(foldername+'/'+ learningname + '_confmap.csv', 'w')
for n in xrange(len(EARmat)):
  fp.write(labels[n] + ',')
fp.write('\n')
for n in xrange(len(EARmat)):
  fp.write(str(EARmat[n]) + ',')
fp.write('\n')
fp.write(str(sum(EARmat)/float(len(EARmat))))
fp.close()

plt.show()

"""
plt.subplots_adjust(left=0.11, bottom=0.15, right=0.95, top=0.95, wspace=None, hspace=None)

#print C
plt.xlim([0,L]);
plt.ylim([N,0]);

ind = np.arange(L) # the x locations for the groups 
width = 0.5

plt.xticks(ind+width, ('1', '2', '3', '4'), fontsize=22)
plt.yticks(fontsize=22)
c = plt.pcolor(C,cmap=plt.cm.gray)
#title('')
#xlabel('Location Concepts ID', fontsize=24)
plt.xlabel('$C_t$', fontsize=32)
plt.ylabel('data', fontsize=32)

plt.savefig('./dataJSAI/verJSAIgs.eps', dpi=150)
plt.savefig('./dataJSAI/verJSAIgs.png', dpi=150)
plt.show()
"""
