#coding:utf-8
#File for setting parameters
#Akira Taniguchi 2016/05/31-2018/12/01-2020/07/15

#https://en.wikipedia.org/wiki/Conjugate_prior
#Multivariate normal μ (mean vector) and Σ (covariance matrix), normal-inverse-Wishart
import numpy as np

####################Parameter settings####################
D = 20             # The number of traning sentences (it should be chainged for each trial)
num_iter = 200     # Iteration number of Gibbs sampling

CNNmode = 2        # Switching image features: (0)SIFT; (1)CNN fc6 layer; (2)CNN->PCA; (-1)DSIFT

#if CNNmode == 0:
#  Descriptor = "SIFT_BoF"
#  k_img = 100
#elif CNNmode == -1:
#  Descriptor = "DSIFT_BoF"
#  k_img = 100
#elif CNNmode == 1:
#  Descriptor = "CNN_fc6"
#  k_img = 4096  ## The huge dimension-GMM is not work.
if CNNmode == 2:
  Descriptor = "CNN_PCA"
  k_img = 30 #65 # The number of dimensions

k_sift = k_img   # k value of ｋ−means
k_rgb  = 10      # The number of dimensions for color feature


nonpara = 1        # Nonparametric Bayes method (ON:1, OFF:0)
if nonpara == 1:
  Ka = 10                   # the number of action categories (the upper limit value)
  Kp = 10                   # the number of position categories (the upper limit value)
  Ko = 10                   # the number of object categories (the upper limit value)
  Kc = 10                   # the number of color categories (the upper limit value)
  alpha_a = 1.0             # Hyperparameter of the Dirichlet distibution of action categories 
  alpha_p = 1.0             # Hyperparameter of the Dirichlet distibution of position categories
  alpha_o = 1.0             # Hyperparameter of the Dirichlet distibution of object categories
  alpha_c = 1.0             # Hyperparameter of the Dirichlet distibution of color categories
elif nonpara == 0:
  Ka = 5                    # the number of action categories
  Kp = 5                    # the number of position categories
  Ko = 5                    # the number of object categories
  Kc = 5                    # the number of color categories
  alpha_a = 1.0             # Hyperparameter of the Dirichlet distibution of action categories 
  alpha_p = 1.0             # Hyperparameter of the Dirichlet distibution of position categories
  alpha_o = 1.0             # Hyperparameter of the Dirichlet distibution of object categories
  alpha_c = 1.0             # Hyperparameter of the Dirichlet distibution of color categories
L = Ka + Kp + Ko + Kc   # the number of word distributions

modality = ["a","p","o","c"]
dict = {"a":0, "p":Ka, "o":Ka+Kp, "c":Ka+Kp+Ko}   # First index number of theta for each modality

gamma = 0.1             # Hyperparameter of the word distribution

## action category
dim_a = 4+34                       #Number of dimensions of Gaussian distribution
k0a = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0a = np.zeros(dim_a)              #Hyperparameter of mean vector of the Gaussian distribution
V0a = np.eye(dim_a)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0a = dim_a + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution(>=dim_a)
#beta_a = [k0a, m0a, V0a, n0a]     

## position category
dim_p = 2#3                        #Number of dimensions of Gaussian distribution
k0p = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0p = np.zeros(dim_p)              #Hyperparameter of mean vector of the Gaussian distribution
V0p = np.eye(dim_p)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0p = dim_p + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution(>=dim_p)
#beta_p = [k0p, m0p, V0p, n0p]     

## image feature category
dim_o = k_sift                     #Number of dimensions of Gaussian distribution
k0o = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0o = np.zeros(dim_o)              #Hyperparameter of mean vector of the Gaussian distribution
V0o = np.eye(dim_o)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0o = dim_o + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution(>=dim_o)
#beta_o = [k0o, m0o, V0o, n0o]     

## color category
dim_c = k_rgb                      #Number of dimensions of Gaussian distribution
k0c = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0c = np.zeros(dim_c)              #Hyperparameter of mean vector of the Gaussian distribution
V0c = np.eye(dim_c)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0c = dim_c + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution(>=dim_c)
#beta_c = [k0c, m0c, V0c, n0c]     

# Range of initial values of Gaussian distribution
mu_a_init  = [0,1]      # [min,max] of mean vector
sig_a_init = 0.05       # Initial variance

mu_p_init  = [-0.5,0.5] # [min,max] of mean vector
sig_p_init = 0.05       # Initial variance

mu_o_init  = [0,1]      # [min,max] of mean vector
sig_o_init = 0.05       # Initial variance 

mu_c_init  = [0,1]      # [min,max] of mean vector
sig_c_init = 0.05       # Initial variance


Plot = 1000  #Plot number of position category for visulalization (2000)


#################### Setting of path of folder ####################
datafolder =  "/home/iCub/datadump/" #"./../datadump/"   #Folder name of traning data

