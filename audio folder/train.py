# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 22:51:24 2020

@author: Leonard
"""
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import numpy as np
import os
import random
import glob
import pathlib
from IPython import display
from scipy.io import loadmat,savemat
import pandas as pd
from scipy import sparse

def sigmoid(x,Lambda):
    return 1/(1+np.exp(-Lambda*x))
    
        
def convert_labels(y, C):
    Y = sparse.coo_matrix((np.ones_like(y),
        (y, np.arange(len(y)))), shape = (C, len(y))).toarray()
    return Y    

def softmax_stable(Z):
    e_Z=Z
    A=e_Z/e_Z.sum(axis=0)
    return A

def to_classlabel(z):
    return z.argmax(axis = 0),z

def LGU_network(xi,w,Lambda):
    ## network Function:
    net = np.dot(w.T,xi)
    ## Activation Function for Logsig:
    ah1 = sigmoid(net[0],Lambda[0])
    ah2 = sigmoid(net[1],Lambda[1])
    ah3 = sigmoid(net[2],Lambda[2])
    ah4 = sigmoid(net[3],Lambda[3])
    ah5 = sigmoid(net[4],Lambda[4])
    ah6 = sigmoid(net[5],Lambda[5])
    ah = np.asarray([ah1,ah2,ah3,ah4,ah5,ah6])
    ## Softmax Function: 
    result = softmax_stable(ah)
    return net,ah,result



def model_load(path,keywork = 'w'):
    w = loadmat(path)   
    weight = w[keywork]
    return weight

## data from the wav file :
data_dir_mother = pathlib.Path('mini_speech_commands')
if not data_dir_mother.exists():
    print('direction not found!')
commands = np.array(os.listdir(str(data_dir_mother)))
## data from the wav file after processing :
data_dir = pathlib.Path('input_data')
if not data_dir.exists():
    print('direction not found!')
filenames = glob.glob(str(data_dir)+'/*')    
listname = os.listdir(data_dir) # dir is your directory path
data  = loadmat(filenames[0])
label = loadmat(filenames[1])
mfcc = data['mfcc']
auto_label = label['label']
index1 = [i for i, name in enumerate(auto_label) if name.strip() == commands[0]]
index2 = [i for i, name in enumerate(auto_label) if name.strip() == commands[1]]
index3 = [i for i, name in enumerate(auto_label) if name.strip() == commands[2]]
index4 = [i for i, name in enumerate(auto_label) if name.strip() == commands[3]]
index5 = [i for i, name in enumerate(auto_label) if name.strip() == commands[4]]
index6 = [i for i, name in enumerate(auto_label) if name.strip() == commands[5]]



input1 = mfcc[index1,:]
input2 = mfcc[index2,:]
input3 = mfcc[index3,:]
input4 = mfcc[index4,:]
input5 = mfcc[index5,:]
input6 = mfcc[index6,:]


Class = len(commands)
# initialize FeedForward For Neural Network:
nuy_w = 0.001 
nuy_lam = 5
E = 1
E_store = E
E_stop = 0.0001 # stopping criteria
epod_max = 35000 #Maximun number of Training round
epod = 0 #start Epod
## initialize the Input Layer:
original_label = np.asarray([0]*len(input1) + [1]*len(input2)+ [2]*len(input3)+ [3]*len(input4)+ [4]*len(input5)+ [5]*len(input6)).T
x = np.concatenate((input1,input2,input3,input4,input5,input6), axis = 0).T
x = np.concatenate((x,np.ones((1,len(mfcc)))), axis = 0)
## Initialize the Labels 
## initialize Original Weight:
w_init = 0.1*np.ones((x.shape[0],Class),order='C')
w =  w_init
d = x.shape[0]
C = w.shape[1]
y = convert_labels(original_label,Class)
Lambda= 12*np.ones((Class,1),order='C')
Lam_store = Lambda[0]
d = x.shape[0]
## Initialize the Labels outputL
C = w_init.shape[1]
w1 = w_init[:,0].reshape(d,1)
w2 = w_init[:,1].reshape(d,1)
w3 = w_init[:,2].reshape(d,1)
w4 = w_init[:,3].reshape(d,1)
w5 = w_init[:,4].reshape(d,1)
w6 = w_init[:,5].reshape(d,1)

lam1 = Lambda[0]
lam2 = Lambda[1]
lam3 = Lambda[2]
lam4 = Lambda[3]
lam5 = Lambda[4]
lam6 = Lambda[5]

while (E>E_stop) and (epod<epod_max): ## initialize the Stopping Condition
        epod = epod + 1
        E = 0
        #w =np.asarray([w1,w2,w3,w4,w5,w6]).T.reshape(d,C)
        for i in range(x.shape[1]):
            xi = x[:,i].reshape(d,1)
            yi = y[:,i].reshape(C,1)
            [net,ah,s]= LGU_network(xi,w,Lambda)
            e = s.reshape(Class,1) - yi            
            ## Back-Propagation                
            dE_de1     = e[0]   
            dE_de2     = e[1]
            dE_de3     = e[2]
            dE_de4     = e[3]   
            dE_de5     = e[4]
            dE_de6     = e[5]
            de1_da1    = de2_da2 = de3_da3 = de4_da4 = de5_da5 = de6_da6 = 1
            da1_dah1   =  (sum(ah)-ah[0])/(sum(ah))**2
            da2_dah1   = -(ah[1])/(sum(ah))**2 
            da3_dah1   = -(ah[2])/(sum(ah))**2 
            da4_dah1   = -(ah[3])/(sum(ah))**2 
            da5_dah1   = -(ah[4])/(sum(ah))**2 
            da6_dah1   = -(ah[5])/(sum(ah))**2 
            dah1_dnet1 = Lambda[0]*np.exp(np.dot(-Lambda[0],net[0]))/(1 + np.exp(np.dot(-Lambda[0],net[0])))**2
            dah1_dlam1 = net[0]*np.exp(np.dot(-Lambda[0],net[0]))/(1 + np.exp(np.dot(-Lambda[0],net[0])))**2
            dnet1_dw = xi.T
            dE_dw_1 = (dE_de1*de1_da1*da1_dah1 + 
                        dE_de2*de2_da2*da2_dah1 +
                        dE_de3*de3_da3*da3_dah1 +
                        dE_de4*de4_da4*da4_dah1 + 
                        dE_de5*de5_da5*da5_dah1 +
                        dE_de6*de6_da6*da6_dah1 )*dah1_dnet1*dnet1_dw
            
            dE_dlam_1 =(dE_de1*de1_da1*da1_dah1 + 
                        dE_de2*de2_da2*da2_dah1 +
                        dE_de3*de3_da3*da3_dah1 +
                        dE_de4*de4_da4*da4_dah1 + 
                        dE_de5*de5_da5*da5_dah1 +
                        dE_de6*de6_da6*da6_dah1 )*dah1_dlam1
            da2_dah2   = (sum(ah)-ah[1])/(sum(ah))**2
            da1_dah2   =-(ah[0])/(sum(ah))**2               
            da3_dah2   =-(ah[2])/(sum(ah))**2 
            da4_dah2   = -(ah[3])/(sum(ah))**2 
            da5_dah2   = -(ah[4])/(sum(ah))**2 
            da6_dah2   = -(ah[5])/(sum(ah))**2 
            dah2_dnet2 = Lambda[1]*np.exp(np.dot(-Lambda[1],net[1]))/(1 + np.exp(np.dot(-Lambda[1],net[1])))**2
            dah2_dlam2 = net[1]*np.exp(np.dot(-Lambda[1],net[1]))/(1 + np.exp(np.dot(-Lambda[1],net[1])))**2
            dE_dlam_2 = (dE_de1*de1_da1*da1_dah2 + 
                        dE_de2*de2_da2*da2_dah2 +
                        dE_de3*de3_da3*da3_dah2 +
                        dE_de4*de4_da4*da4_dah2 + 
                        dE_de5*de5_da5*da5_dah2 +
                        dE_de6*de6_da6*da6_dah2 )*dah2_dlam2 
            dnet2_dw = xi.T
            dE_dw_2 = (dE_de1*de1_da1*da1_dah2 + 
                        dE_de2*de2_da2*da2_dah2 +
                        dE_de3*de3_da3*da3_dah2 +
                        dE_de4*de4_da4*da4_dah2 + 
                        dE_de5*de5_da5*da5_dah2 +
                        dE_de6*de6_da6*da6_dah2 )*dah2_dnet2*dnet2_dw
            
            da3_dah3   = (sum(ah)-ah[2])/(sum(ah))**2
            da1_dah3   =-(ah[0])/(sum(ah))**2    
            da2_dah3   =-(ah[1])/(sum(ah))**2 
            da4_dah3   = -(ah[3])/(sum(ah))**2 
            da5_dah3   = -(ah[4])/(sum(ah))**2 
            da6_dah3   = -(ah[5])/(sum(ah))**2 
            dah3_dnet3 = Lambda[2]*np.exp(np.dot(-Lambda[2],net[2]))/(1 + np.exp(np.dot(-Lambda[2],net[2])))**2
            dah3_dlam3 = net[2]*np.exp(np.dot(-Lambda[2],net[2]))/(1 + np.exp(np.dot(-Lambda[2],net[2])))**2

            dnet3_dw = xi.T
            dE_dw_3 = (dE_de1*de1_da1*da1_dah3 + 
                        dE_de2*de2_da2*da2_dah3 +
                        dE_de3*de3_da3*da3_dah3 +
                        dE_de4*de4_da4*da4_dah3 + 
                        dE_de5*de5_da5*da5_dah3 +
                        dE_de6*de6_da6*da6_dah3 )*(dah3_dnet3*dnet3_dw)
            dE_dlam_3 = (dE_de1*de1_da1*da1_dah3 + 
                        dE_de2*de2_da2*da2_dah3 +
                        dE_de3*de3_da3*da3_dah3 +
                        dE_de4*de4_da4*da4_dah3 + 
                        dE_de5*de5_da5*da5_dah3 +
                        dE_de6*de6_da6*da6_dah3 )*dah3_dlam3
            
            da4_dah4   = (sum(ah)-ah[3])/(sum(ah))**2
            da1_dah4   =-(ah[0])/(sum(ah))**2    
            da2_dah4   =-(ah[1])/(sum(ah))**2 
            da3_dah4   = -(ah[2])/(sum(ah))**2 
            da5_dah4   = -(ah[4])/(sum(ah))**2 
            da6_dah4   = -(ah[5])/(sum(ah))**2 
            dah4_dnet4 = Lambda[3]*np.exp(np.dot(-Lambda[3],net[3]))/(1 + np.exp(np.dot(-Lambda[3],net[3])))**2
            dah4_dlam4 = net[3]*np.exp(np.dot(-Lambda[3],net[3]))/(1 + np.exp(np.dot(-Lambda[3],net[3])))**2

            dnet4_dw = xi.T
            dE_dw_4 = (dE_de1*de1_da1*da1_dah4 + 
                        dE_de2*de2_da2*da2_dah4 +
                        dE_de3*de3_da3*da3_dah4 +
                        dE_de4*de4_da4*da4_dah4 + 
                        dE_de5*de5_da5*da5_dah4 +
                        dE_de6*de6_da6*da6_dah4 )*dah4_dnet4*dnet4_dw
            dE_dlam_4 =(dE_de1*de1_da1*da1_dah4 + 
                        dE_de2*de2_da2*da2_dah4 +
                        dE_de3*de3_da3*da3_dah4 +
                        dE_de4*de4_da4*da4_dah4 + 
                        dE_de5*de5_da5*da5_dah4 +
                        dE_de6*de6_da6*da6_dah4 )*dah4_dlam4
            da5_dah5   = (sum(ah)-ah[4])/(sum(ah))**2
            da1_dah5   =-(ah[0])/(sum(ah))**2    
            da2_dah5   =-(ah[1])/(sum(ah))**2 
            da3_dah5   = -(ah[2])/(sum(ah))**2 
            da4_dah5   = -(ah[3])/(sum(ah))**2 
            da6_dah5   = -(ah[5])/(sum(ah))**2 
            dah5_dnet5 = Lambda[4]*np.exp(np.dot(-Lambda[4],net[4]))/(1 + np.exp(np.dot(-Lambda[4],net[4])))**2
            dah5_dlam5 = net[4]*np.exp(np.dot(-Lambda[4],net[4]))/(1 + np.exp(np.dot(-Lambda[4],net[4])))**2

            dnet5_dw = xi.T
            dE_dw_5 = (dE_de1*de1_da1*da1_dah5 + 
                        dE_de2*de2_da2*da2_dah5 +
                        dE_de3*de3_da3*da3_dah5 +
                        dE_de4*de4_da4*da4_dah5 + 
                        dE_de5*de5_da5*da5_dah5 +
                        dE_de6*de6_da6*da6_dah5 )*dah5_dnet5*dnet5_dw
            dE_dlam_5 =(dE_de1*de1_da1*da1_dah5 + 
                        dE_de2*de2_da2*da2_dah5 +
                        dE_de3*de3_da3*da3_dah5 +
                        dE_de4*de4_da4*da4_dah5 + 
                        dE_de5*de5_da5*da5_dah5 +
                        dE_de6*de6_da6*da6_dah5 )*dah5_dlam5
            da6_dah6  = (sum(ah)-ah[5])/(sum(ah))**2
            da1_dah6   =-(ah[0])/(sum(ah))**2    
            da2_dah6   =-(ah[1])/(sum(ah))**2 
            da3_dah6   = -(ah[2])/(sum(ah))**2 
            da4_dah6   = -(ah[3])/(sum(ah))**2 
            da5_dah6   = -(ah[4])/(sum(ah))**2 
            dah6_dnet6 = Lambda[5]*np.exp(np.dot(-Lambda[5],net[5]))/(1 + np.exp(np.dot(-Lambda[5],net[5])))**2
            dah6_dlam6 = net[5]*np.exp(np.dot(-Lambda[5],net[5]))/(1 + np.exp(np.dot(-Lambda[5],net[5])))**2

            dnet6_dw = xi.T
            dE_dw_6 = (dE_de1*de1_da1*da1_dah6 + 
                        dE_de2*de2_da2*da2_dah6 +
                        dE_de3*de3_da3*da3_dah6 +
                        dE_de4*de4_da4*da4_dah6 + 
                        dE_de5*de5_da5*da5_dah6 +
                        dE_de6*de6_da6*da6_dah6 )*dah6_dnet6*dnet6_dw
            dE_dlam_6 = (dE_de1*de1_da1*da1_dah6 + 
                        dE_de2*de2_da2*da2_dah6 +
                        dE_de3*de3_da3*da3_dah6 +
                        dE_de4*de4_da4*da4_dah6 + 
                        dE_de5*de5_da5*da5_dah6 +
                        dE_de6*de6_da6*da6_dah6 )*dah6_dlam6
            ## Weight Updated
            w1 = w1 - nuy_w*dE_dw_1.T
            w2 = w2 - nuy_w*dE_dw_2.T
            w3 = w3 - nuy_w*dE_dw_3.T
            w4 = w4 - nuy_w*dE_dw_4.T
            w5 = w5 - nuy_w*dE_dw_5.T
            w6 = w6 - nuy_w*dE_dw_6.T
            
            lam1 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam1 - nuy_lam*dE_dlam_1
            lam2 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam2 - nuy_lam*dE_dlam_2
            lam3 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam3 - nuy_lam*dE_dlam_3
            lam4 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam4 - nuy_lam*dE_dlam_4
            lam5 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam5 - nuy_lam*dE_dlam_5
            lam6 = (1-0.001*(np.dot(e.T,e))/(np.dot(e.T,e)+1))*lam6 - nuy_lam*dE_dlam_6
            ## Error Update
            w =np.array([w1,w2,w3,w4,w5,w6]).T.reshape(d,C)  
            Lambda = np.array([lam1,lam2,lam3,lam4,lam5,lam6]).reshape(Class,1) 
            ## Error Update      
            E = E + 0.5*((e[0])**2 + (e[1])**2 + (e[2])**2 +(e[3])**2 + (e[4])**2 + (e[5])**2) 
            #E = E + 0.5*((e[0])**2 + (e[1])**2 + (e[2])**2 ) 
        E_store = np.append(E_store,E)
      #Lambda = Lambda.reshape(10,)
        Lam_store = np.append(Lam_store,Lambda[0])
fig = plt.figure(figsize=(15,10))
plt.plot(E_store)
plt.grid(True)          
savemat('model_saved\weight_6_class.mat', mdict={'w': w})
savemat('model_saved\Lambda_6_class.mat', mdict={'lambda': Lambda})