# Cross-Situational Learning with Bayesian Generative Models for Multimodal Category and Word Learning in Robots
## Cross-Situational Learning with Bayesian Generative Model (CSL-BGM)

These source codes can be used in both iCub simulator and real iCub.  
- `/For_Real_iCub/` : The folder for a real iCub robot  
- `/For_Simulator/` : The folder for iCub simulator  
- `/learning/` :  Minimal python codes for learning.  


### Introduction
Figure 1: An overview of the cross-situational learning scenario as the focus of this study.
The robot obtains multimodal information from multiple sensory-channels in a situation and estimates the relationships between words and sensory-channels.  
<img src="https://github.com/a-taniguchi/CSL-BGM/blob/master/img/abstract.jpg" width="600x">

Figure 2: The procedure for obtaining and processing data.  
<img src="https://github.com/a-taniguchi/CSL-BGM/blob/master/img/getting_data.jpg" width="600px">

Figure 3: The graphical model of cross-situational learning for multichannel categorizations and for learning word meaning; the action, position, color, and object categories are represented by a component in Gaussian mixture models (GMMs). A word distribution is related to a category on GMMs. Gray nodes represent observed variables.
<img src="https://github.com/a-taniguchi/CSL-BGM/blob/master/img/graphicalmodel.jpg" width="520px">

## Execution PC environment  
- Ubuntu 14.04  
- iCub software and YARP  
- ODE 0.13.1 and SDL  
- Python 2.7.6 (numpy, scipy, scikit-learn)  
- OpenCV 3.1.0   
- CNN feature extracter: Caffe (Reference model: Alex-net)  

## How to install iCub softwere
Plase see these sites.  
- http://wiki.icub.org/wiki/ICub_Software_Installation  
- http://wiki.icub.org/wiki/Linux:Installation_from_binaries  


---

## Paper information  
Abstract:  
Human infants can acquire word meanings by estimating the relationships among multimodal information and words. In this paper, we propose a novel Bayesian generative model that can form multiple categories based on each sensory-channel and can associate words with any of four sensory-channels (action, position, object, and color). This paper focuses on cross-situational learning using the co-occurrence between words and information of sensory-channels in complex situations. We conducted a learning experiment using a simulator and a real humanoid iCub robot. In the experiments, a human tutor provided a sentence that describes an object of visual attention and an accompanying action to the robot. The experimental results showed that the proposed method was able to estimate the multiple categorizations and to learn the relationships between multiple sensory-channels and words accurately. In addition, we conducted an action generation task and an action description task based on word meanings learned in the cross-situational learning experiment. The experimental results showed the robot could successfully use the word meanings learned by using the proposed method.

Keywords: Bayesian model, cross-situational learning, lexical acquisition, multimodal categorization, symbol grounding, word meaning

Reference:  
Akira Taniguchi, Tadahiro Taniguchi, and Angelo Cangelosi. "Cross-Situational Learning with Bayesian Generative Models for Multimodal Category and Word Learning in Robots." Frontiers in Neurorobotics 11: 66 (2017).  
DOI: 10.3389/fnbot.2017.00066

Paper:  
https://www.frontiersin.org/articles/10.3389/fnbot.2017.00066/full

Video:  
https://youtu.be/SzyoWaj47Xc

Materials: [Slide](https://drive.google.com/file/d/1x9GInP4sed5eo-xf-lOuCjptJjcRFXaj/view?usp=sharing), [Poster](https://drive.google.com/file/d/11t1uURVSP7gjFAZyNkpEQCqk0Ojju1MK/view?usp=sharing)

