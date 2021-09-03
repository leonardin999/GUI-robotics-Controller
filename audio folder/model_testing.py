# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 08:58:56 2020

@author: Leonard
"""

import time 
from module_function import *
## from the input:
data_dir = pathlib.Path('mini_speech_commands')
if not data_dir.exists():
    print('direction not found!')
label = np.array(os.listdir(str(data_dir)))
## from the model:
data_dir_model = pathlib.Path('model_saved')
if not data_dir_model.exists():
    print('direction not found!')
filenames = glob.glob(str(data_dir_model)+'/*')

while True:
    weights = model_load(filenames[1])
    Lambda = model_load(filenames[0],'lambda')
    [command,percent] = record(weights,Lambda,label) 
    print(command)
    
    if input('try Again? (Y/N)').strip().upper()!='Y':
        break          