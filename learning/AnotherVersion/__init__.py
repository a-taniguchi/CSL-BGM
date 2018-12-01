#coding:utf-8
#Akira Taniguchi 2017/03/23-26
import numpy as np

####################Parameter settings#################### 
M = 1#60             # The number of traning sentences 
num_iter = 10     #Iteration number of Gibbs sampling

K  = 10            # The number of categories in POS tag state
Ka = 10            # The number of categories in action
Kc = 5             # The number of categories in object color
Ks = 10            # The number of categories in spatial layout
Kg = 5             # The number of categories in object geometry
Kt = 1             # The number of categories in Trash
L = Ka + Kc + Ks + Kg + Kt   # The number of word distributions (Theta) #16

modality = ["a", "c", "s","g","t"] # "a" denotes action, "c" denotes color, "s" denotes spatial layout, "g" denotes object geometry, "t" denotes trash
dict = {"a":0, "c":Ka, "s":Ka+Kc, "g":Ka+Kc+Ks, "t":Ka+Kc+Ks+Kg}  #First index number of theta for each modality

alpha_a = 0.10      # Hyperparameter of the Dirichlet distribution pi_a
alpha_c = 0.10      # Hyperparameter of the Dirichlet distribution pi_c
alpha_s = 0.10      # Hyperparameter of the Dirichlet distribution pi_s
alpha_g = 0.10      # Hyperparameter of the Dirichlet distribution pi_g
gamma = 0.010        # Hyperparameter of the Dirichlet distribution theta
lambda0 = 10.0      # Hyperparameter of the Categorical distribution m
delta = 0.01        # Hyperparameter of the Categorical distribution pi

#beta_a = [k0a, m0a, V0a, n0a]
dim_a = 3                          #Number of dimensions of action                       [[Amir: It is not possible to define it in advance as it changes from action to another, see learn.py file]] 
#[[Akira: It is defined as a global variable. Assigned value is temporary. It is changed by learn.py.]]
k0a = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0a = np.zeros(dim_a)              #Hyperparameter of mean vector of the Gaussian distribution
V0a = np.eye(dim_a)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0a = dim_a + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_a)

#beta_c = [k0c, m0c, V0c, n0c]
dim_c = 3                          #Number of dimensions of object color                [[Amir: Not possible to define it as it depends on the number of the pixels of each object, see learn.py file]]
k0c = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0c = np.zeros(dim_c)              #Hyperparameter of mean vector of the Gaussian distribution
V0c = np.eye(dim_c)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0c = dim_c + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_c)

#beta_s = [k0s, m0s, V0s, n0s]
dim_s = 3                          #Number of dimensions of centroid (x,y,z)
k0s = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0s = np.zeros(dim_s)              #Hyperparameter of mean vector of the Gaussian distribution
V0s = np.eye(dim_s)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0s = dim_s + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_s)

#beta_g = [k0g, m0g, V0g, n0g]
dim_g = 308                        #Number of dimensions of object geometry
k0g = 1e-3                         #Hyperparameter of mean vector of the Gaussian distribution
m0g = np.zeros(dim_g)              #Hyperparameter of mean vector of the Gaussian distribution
V0g = np.eye(dim_g)*0.01           #Hyperparameter of covariance matrix of the Gaussian distribution
n0g = dim_g + 2.0                  #Hyperparameter of covariance matrix of the Gaussian distribution (>=dim_g)


#initial valeus of Gauss distribution

mu_a_init  = [0,1]      #[min,max]    [[Amir:  how to define this value?]]
sig_a_init = 0.05 

mu_c_init  = [0,1]      #[min,max]    [[Amir:  how to define this value?]]
sig_c_init = 0.05 

mu_s_init  = [-1,1]      #[min,max]
sig_s_init = 0.05 

mu_g_init  = [0,10]      #[min,max]
sig_g_init = 0.05


###################Setting of path of folder####################
datafolder =  "/home/akira/For_Akira/Multimodal_Data/"  #Folder name of traning data
Learningfolder = "Learning_Data/"
Sentences = "POS-Tagging-files/Corpus.txt"   
POS_tags = "POS-Tagging-files/Output-POS.txt"  
Object_geometry = "Point-Cloud-PCD-files/Geometry/"               #Object_features
Object_color = "Point-Cloud-PCD-files/RGB/"
Centroids = "Point-Cloud-PCD-files/Centroids/"       
Action="Skeleton-Tracking files/Action/"
Test_folder = "Test/" 
Sentence = "POS-Tagging-files/Sentence.txt"   #Folder,file name of Sentence data (datafolder + Sentence)
POS_tag = "POS-Tagging-files/Sentence_Labels.txt"  #Folder,file name of POS_tag data (datafolder + POS_tag)
