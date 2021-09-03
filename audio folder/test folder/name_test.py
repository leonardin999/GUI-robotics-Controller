# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 09:44:19 2021

@author: Leonard
"""

import pyttsx3
engine = pyttsx3.init() # object creation
import numpy as np
""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
# print (rate)                        #printing current voice rate
engine.setProperty('rate', 150)     # setting up new voice rate
voices = engine.getProperty('voices')
name = []
actual_name =[]
for voice in voices:
    name =np.append(name,voice.name)

for data in name:
    config = data.split()
    actual_name = np.append(actual_name,config[1])