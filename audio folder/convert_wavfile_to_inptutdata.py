# -*- coding: utf-8 -*-
"""
Created on Fri May 28 09:06:44 2021

@author: Leonard
"""

from module_function import *
from feature_extraction import *
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
# (rate,sig) = wav.read("0ea0e2f4_nohash_1.wav")
# [mfcc_feat,feat] = mfcc(sig, rate)

# plt.plot(np.linspace(0, len(mfcc_feat), num=len(mfcc_feat)), mfcc_feat)    
data_dir = pathlib.Path('mini_speech_commands')
if not data_dir.exists():
    print('direction not found!')
commands = np.array(os.listdir(str(data_dir)))
commands = commands[commands != 'README.md']
filenames = glob.glob(str(data_dir)+'/*/*')
pathfiles = glob.glob(str(data_dir)+'/*')
num_samples = len(filenames)
print('Number of total examples:', num_samples)
print('Number of examples per label:',
      len(os.listdir(str(data_dir/commands[0]))))
print('Example file:', filenames[0])
def get_label(file_path):
    parts=[]
    for i in range(np.size(file_path)):
        parts_take = np.array([file_path[i].split('\\')])
        parts =np.append(parts,parts_take[0,1])                                
    return parts
## create folder to save file
dirName = 'input_data'
if not os.path.exists(dirName):
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ")
else:    
    print("Directory " , dirName ,  " already exists")  
        
# data__input_dir = pathlib.Path('input_data')
# mfcc_1=[]
# for i in range(len(pathfiles)):
#     mfcc_1[i] = mutiple_file(pathfiles[i])
# #savemat(str(data__input_dir)+"\\"+commands[0]+'.mat',{str(commands[0]):mfcc_down})
mfcc_result=[]
#folder = str(folder).strip('\u202a')
listname = os.listdir(pathfiles[0]) # dir is your directory path
number_files = len(listname)

data_dir = pathlib.Path('mini_speech_commands')
if not data_dir.exists():
    print('direction not found!')
commands = np.array(os.listdir(str(data_dir)))
commands = commands[commands != 'README.md']
filenames = glob.glob(str(data_dir)+'/*/*')
pathfiles = glob.glob(str(data_dir)+'/*')
#filenames = random.shuffle(filenames)
num_samples = len(filenames)
print('Number of total examples:', num_samples)
print('Number of examples per label:',
      len(os.listdir(str(data_dir/commands[0]))))
print('Example file:', filenames[0])
def get_label(file_path):
    parts=[]
    for i in range(np.size(file_path)):
        parts_take = np.array([file_path[i].split('\\')])
        parts =np.append(parts,parts_take[0,1])                                
    return parts
label = get_label(filenames)
signal={}
mfcc_feat={}
for i in range(len(filenames)):  
    (sr,signal[i]) = read_wavfile(filenames[i])
for i in range(len(signal)):
    mfcc_feat[i] = feature_extract(signal.get(i), sr)

data = list(mfcc_feat.values())

savemat('input_data\label.mat',{'label':label})
savemat('input_data\data.mat',{'mfcc':data})
