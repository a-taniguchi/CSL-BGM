#coding:utf-8
#gaussian plot (position category)
#Akira Taniguchi 2016/06/16
import itertools
import numpy as np
from scipy import linalg
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn import mixture
from __init__ import *
from numpy.random import multinomial,uniform,dirichlet
from scipy.stats import multivariate_normal,invwishart,rv_discrete

trialname = "ts"#raw_input("trialname?(folder) >")
start = "1"#raw_input("start number?>")
end   = "25"#raw_input("end number?>")
filename = raw_input("learning trial name?>")#"001"#

Kp = 5

sn = int(start)
en = int(end)
Data = int(en) - int(sn) +1

foldername = datafolder + trialname+"("+str(sn).zfill(3)+"-"+str(en).zfill(3)+")"

Mu_p  = [ np.array([0 for i in xrange(dim_p)]) for k in xrange(Kp) ]
Sig_p = [ np.eye(dim_p)*sig_p_init for k in xrange(Kp) ]

#p_dm = [[[-0.3945, 0.0165]], [[-0.3555, -0.006], [-0.336, 0.18]], [[-0.438, -0.0315], [-0.315, 0.0225], [-0.2355, 0.18]], [[-0.453, -0.018], [-0.3, -0.1005], [-0.258, -0.0255]], [[-0.438, 0.036], [-0.318, 0.1875], [-0.3, 0.0795]], [[-0.5535, 0.0675], [-0.336, -0.0465]], [[-0.3885, 0.0555], [-0.3465, -0.126]], [[-0.3555, -0.1425], [-0.324, -0.039], [-0.273, 0.0825]], [[-0.3885, 0.135]], [[-0.285, -0.0135]], [[-0.5265, 0.045], [-0.33, 0.18], [-0.2685, 0.0165]], [[-0.453, 0.015], [-0.3795, 0.231]], [[-0.3825, -0.231]], [[-0.327, -0.18], [-0.309, -0.0075]], [[-0.3735, -0.1455]], [[-0.2685, -0.0135]], [[-0.438, 0.033], [-0.36, 0.204], [-0.2955, 0.0855]], [[-0.45, 0.048]], [[-0.447, -0.006], [-0.3735, 0.1785]], [[-0.4005, 0.1755], [-0.2655, -0.0705]]]
p_temp = []
#for d in xrange(D):
#  p_temp = p_temp + p_dm[d]

#[[-0.319936213,	0.117489433],[-0.345566772,	-0.00810185],[-0.362990185,	-0.042447971],[-0.277759177,	0.083363745]]

#Sig_p = [[] , [], [] ,[]]

#Sig_p[0] = [[0.010389635,	0.001709343],[0.001709343,	0.018386732]]
#[[0.005423979,	0.000652657],[0.000652657,	0.001134736]]
#Sig_p[1] = [[0.001920786,	-0.001210214],[-0.001210214,	0.002644612]]
#Sig_p[2] = [[0.003648299,	-0.000312398],[-0.000312398,	0.001518234]]
#Sig_p[3] = [[0.001851727,	-0.000656013],[-0.000656013,	0.004825636]]

k=0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_Mu_p.csv', 'r'):
  itemList = line[:-1].split(',')
  #for i in xrange(len(itemList)):
  Mu_p[k] = [float(itemList[0]),float(itemList[1])]
  k = k + 1 

k=0
i=0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_Sig_p.csv', 'r'):
  itemList = line[:-1].split(',')
  if k < Kp:
    if (i == 0):
      #for i in xrange(len(itemList)):
      print itemList
      Sig_p[k][0][0] = float(itemList[0])
      Sig_p[k][0][1] = float(itemList[1])
      i = i + 1
    elif (i == 1):
      #for i in xrange(len(itemList)):
      print itemList
      Sig_p[k][1][0] = float(itemList[0])
      Sig_p[k][1][1] = float(itemList[1])
      i = i + 1
    elif (i == 2):
      i = 0
      k = k + 1

zp = []
pi_p = [0.0 for k in range(Kp)] #[0.017826621173443864,0.28554229470170217,0.041570976925928926,0.1265347852145472,0.52852532198437785]

dm = 0
for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_zp.csv', 'r'):
  itemList = line[:-1].split(',')
  for i in range(len(itemList)):
    if itemList[i] != '':
      #print dm,itemList[i]
      zp = zp + [int(itemList[i])]
      
      dm = dm + 1

for line in open(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_pi_p.csv', 'r'):
  itemList = line[:-1].split(',')
  for i in range(len(pi_p)):
    pi_p[i] = float(itemList[i])

colors = ['b', 'g', 'm', 'r', 'c', 'y', 'k', 'orange', 'purple', 'brown']
color_iter = itertools.cycle(colors)
splot = plt.subplot(1, 1,1)

for k,(mean,covar,color) in enumerate(zip(Mu_p,Sig_p,color_iter)):
        v, w = linalg.eigh(covar)
        u = w[0] / linalg.norm(w[0])
        angle = np.arctan(u[1] / u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse([mean[1],mean[0]], v[0], v[1], 180 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        #splot.add_artist(ell)
        #ガウス分布から大量にサンプリングしてプロットする場合
        for i in range(int(5000*2*pi_p[k])):#)):#
          X = multivariate_normal.rvs(mean=mean, cov=covar)
          plt.scatter(X[1],X[0], s=5, marker='.', color=color, alpha=0.2)

#データをクラスごとに色分けしてプロットする場合
#for i in range(len(p_temp)):
#  plt.scatter(p_temp[i][1],p_temp[i][0], marker='x', c=colors[zp[i]])





"""
# Number of samples per component
n_samples = 500

# Generate random sample, two components
np.random.seed(0)
C = np.array([[0., -0.1], [1.7, .4]])
X = np.r_[np.dot(np.random.randn(n_samples, 2), C),
          .7 * np.random.randn(n_samples, 2) + np.array([-6, 3])]

# Fit a mixture of Gaussians with EM using five components
#gmm = mixture.GMM(n_components=5, covariance_type='full')
#gmm.fit(X)

# Fit a Dirichlet process mixture of Gaussians using five components
dpgmm = mixture.DPGMM(n_components=5, covariance_type='full')
dpgmm.fit(X)



#for i, (clf, title) in enumerate([#(gmm, 'GMM'),
#                                  (dpgmm, 'Dirichlet Process GMM')]):
"""
#clf=dpgmm
title = 'Position category'#data'
#Y_ = clf.predict(X)
#print Y_
"""
for i, (mean, covar, color) in enumerate(zip(
            clf.means_, clf._get_covars(), color_iter)):
        v, w = linalg.eigh(covar)
        print covar
        u = w[0] / linalg.norm(w[0])
        # as the DP will not use every component it has access to
        # unless it needs it, we shouldn't plot the redundant
        # components.
        #if not np.any(Y_ == i):
        #    continue
        #plt.scatter(X[Y_ == i, 0], X[Y_ == i, 1], .8, color=color)

        # Plot an ellipse to show the Gaussian component
        angle = np.arctan(u[1] / u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        ell = mpl.patches.Ellipse(mean, v[0], v[1], 180 + angle, color=color)
        ell.set_clip_box(splot.bbox)
        ell.set_alpha(0.5)
        splot.add_artist(ell)
"""
plt.ylim(-0.2, -0.8)
plt.xlim(-0.3, 0.3)
#plt.xticks([-0.8+0.1*i for i in range(7)])
#plt.yticks([-0.3+0.1*i for i in range(7)])
plt.title(title)

#w, h = plt.get_figwidth(), plt.get_figheight()
#ax = plt.add_axes((0.5 - 0.5 * 0.8 * h / w, 0.1, 0.8 * h / w, 0.8))
#aspect = (ax.get_xlim()[1] - ax.get_xlim()[0]) / (ax.get_ylim()[1] - ax.get_ylim()[0])                     
#ax.set_aspect(aspect)
plt.gca().set_aspect('equal', adjustable='box')

plt.savefig(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_position_data_plot_p1nd.eps', dpi=150)
plt.savefig(foldername +'/' + filename + '/' + trialname + '_'+ filename +'_position_data_plot_p1nd.png', dpi=150)

plt.show()
