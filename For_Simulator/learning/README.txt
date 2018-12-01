//////////////////////////////////////
README file for learning programs
                         in simulator
Author: Akira Taniguchi 
2016/08/21 (Japanese version)
2018/12/01 (English version)
//////////////////////////////////////

[Folder]
/option/: These files are provided as options, so you do not need to use them.

[Files]
ARI.py: Calculate the ARI value of categorization result for each element of learned data and true (human) categorization result for evaluation
ARI10.py: Calculate the ARI value for 10 trials
CNNPCA_action.py: Program for extracting CNN-PCA features for action generation task
CNNPCA_description.py: Program for extracting CNN-PCA features for description task
CNN_feature.py: Program for extracting CNN feature vector from object image file
PCA.py: Reduce dimensions of CNN features with PCA (due to the sklearn.decomposition being used, there may be a smaller number of dimensions than the specified number of dimensions)
PCA_rename.py: (Version with different file names for each number of data)
README.txt: This file
__init__.py: File to set the initial values ​​of learning parameters
__init__for_action.py: File to set the initial values ​​of parameters for action generation task
action.py: Action experiment program (generate actions from learned files and word data)
actiondatacollector.py: Before executing learn.py, it extracts action data as learning data from dump file of iCub_SIM.
confmat.py: Visualization of confusion matrix between true word and estimated word
confmat_ACCF.py: accuracy_score and f1_score are given by confusion matrix
description.py: Program for action description task
description2.py: Program for action description task
description_all.sh: Shell script for action description task
learn.py: Main Learning program by Gibbs sampling.
mean ARI.py: Read ARI for each trial and give an average value
mearnEAR_Fd.py: Average of ARI of only attention object (option)
plot_gmm.py: Program for plotting Gaussian distribution of the position category (error occurs in NPB version)
plot_gmm2.py: Program for drawn Gaussian distribution of the position category elliptically (error occurs in NPB version)
plot_gmm2_nd.py: Program for drawn Gaussian distribution of the position category elliptically (weight of mixture ratio can not be considered.)
plot_gmm2_nodata.py: Program for drawn Gaussian distribution of the position category elliptically (without training data plots)
plot_gmm_nd.py: Program for plotting Gaussian distribution of the position category
sift_rename.py: extract SIFT feature and RGB features (Only use RGB features)


[Experiment execution procedure]
1. Prepare the data in the datadump folder
2. Set the parameters and PATH in the initialization file (__init__.py) 
2-1. Prepare word file (testss_word.csv)
3. Extract image features. (CNN_feature.py and sift_rename.py)
4. For CNN 4096 dimensional data, PCA reduces the dimension. (PCA_rename.py)
5. Perform conversion processing of action data. (Actiondatacollector.py)
5. Learning (learn.py)

