# -*- coding: utf-8 -*-
"""
Created on Sun Jun 20 04:54:22 2021

@author: Leonard
"""

from ui_styles import *
from main_GUI import *
import fnmatch
import time
from module_function_GUI import *
from feature_extraction_GUI import *
import numpy as np
from pydub import AudioSegment
import math as m
import pyttsx3
import glob


class UIFunctions(MainWindow):
    def set_up_voice(self):
        self.engine = pyttsx3.init() # object creation
        self.rate = self.engine.getProperty('rate')   # getting details of current speaking rate
        self.engine.setProperty('rate', 150)     # setting up new voice rate
        self.voices = self.engine.getProperty('voices')
        self.volume = self.engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
        self.engine.setProperty('volume',1)    # setting up volume level  between 0 and 1
        self.ui.engine.setProperty('voice','HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
        self.engine.say("Activating The Voice Command controller system. Welcome back")
        self.engine.runAndWait()
        self.engine.stop()
    def Record_Fcn(self):
        data_dir = pathlib.Path('audio folder/mini_speech_commands')
        if not data_dir.exists():
            print('direction not found!')
        self.label = np.array(os.listdir(str(data_dir)))
        ## from the model:
        data_dir_model = pathlib.Path('audio folder/model_saved')
        if not data_dir_model.exists():
            print('direction not found!')
        filenames = glob.glob(str(data_dir_model)+'/*')
        self.weights = model_load(filenames[1])
        self.Lambda = model_load(filenames[0],'lambda')

        time.sleep(0.1)
        [self.command,self.percent] = record(self.weights,self.Lambda,self.label)
        self.accurate.setText(str(self.percent))
        self.commandline.setText(self.command)
        if self.command.strip() == 'khởi động':
            theta_start = np.array(['0','53','43','0','0','0'])
            x,y,z = UIFunctions.forward_kinemtic(theta_start)
            self.xposvalue.setText(str(x))
            self.yposvalue.setText(str(y))
            self.zposvalue.setText(str(z))
        elif self.command.strip() == 'trái':
            UIFunctions.left_signal(self)
        elif self.command.strip() == 'tiến':
            UIFunctions.forward_signal(self) 
        elif self.command.strip() == 'lùi':
            UIFunctions.backward_signal(self)
        elif self.command.strip() == 'phải':
            UIFunctions.right_signal(self)
        elif self.command.strip() == 'lên':
            UIFunctions.up_signal(self)
        elif self.command.strip() == 'xuống':
            UIFunctions.down_signal(self)
        elif self.command.strip() == '__unknown_voices__':
            self.engine.say("The voice Signal lost. pLease try again")
            self.engine.runAndWait()
            self.engine.stop()
    
    def Serial_connect(self,comm,baud):
        self.ser.port = comm
        self.ser.baudrate =  baud
        self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
        self.ser.parity = serial.PARITY_NONE #set parity check: no parity
        self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits            #timeout block read
        self.ser.xonxoff = False     #disable software flow control
        self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
        self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
        self.ser.writeTimeout = 0    #timeout for write
        self.ser.open()
        
        
    def list_port(self):
        self.port.clear()
        ports = serial.tools.list_ports.comports()
        self.commPort =([comport.device for comport in serial.tools.list_ports.comports()])
        self.numConnection = len(self.commPort)
        if  self.numConnection == 0 :
            pass
        elif self.numConnection == 1 :
            self.port.addItem(str(self.commPort[0]))
        else:
            self.port.addItem(str(self.commPort[0]))
            self.port.addItem(str(self.commPort[1]))

    def connect_clicked(self):
        comport = self.port.currentText()
        baurate = self.baud.currentText()
        UIFunctions.Serial_connect(self,comport,baurate)
        self.engine.say("Connected to"+ comport)
        self.engine.runAndWait()
        self.engine.stop()
        if not self.ser.isOpen():
            self.ser.open()
            self.btnconnect.setStyleSheet('QPushButton {background-color:#1eff1e; color: white;}')                 
            self.btn_disconnect.setStyleSheet('QPushButton {background-color:#343b48; color: white;}') 
            print("connected Arduino")
        else:  
            self.btnconnect.setStyleSheet('QPushButton {background-color:#1eff1e; color: white;}') 
            self.btn_disconnect.setStyleSheet('QPushButton {background-color:#343b48; color: white;}') 
            print("connected Arduino")
                        
    def disconnect_clicked(self):
         if not self.ser.isOpen():
            self.btnconnect.setStyleSheet('QPushButton {background-color:#343b48; color: white;}') 
            self.btn_disconnect.setStyleSheet('QPushButton {background-color:#ff1e00; color: white;}') 
            print("disconnected")
         else: 
            self.ser.close()
            self.engine.say("Disconnected")
            self.engine.runAndWait()
            self.engine.stop()
            self.btnconnect.setStyleSheet('QPushButton {background-color:#343b48; color: white;}') 
            self.btn_disconnect.setStyleSheet('QPushButton {background-color:#ff1e00; color: white;}')
            print("disconnected")
            self.xposvalue.clear()
            self.yposvalue.clear()
            self.zposvalue.clear()
            self.valuethe1.clear()
            self.valuethe2.clear()
            self.valuethe3.clear()
            self.valuethe4.clear()
            self.valuethe5.clear()
            self.valuethe6.clear()

    def inverse_kinematic(Px,Py,Pz):
        d0 = 14.5 
        d1 = 2.87
        d2 = 25.5
        d3 = 1.8
        d4 = 7.2
        d5 = 17.7
        d6=  0
        d7= 6.5
        Pz = Pz + d6+d7;
        r11=  -1 ;  r12= 0;  r13= 0   ;    
        r21= 0  ; r22=1;   r23=0   ;     
        r31=0 ;  r32= 0;  r33=-1 ;
        r41=0 ; r42=0 ;r43=0 ; r44=1;
        T1 =np.empty(10, dtype=object)
        T2 =np.empty(10, dtype=object)
        T3 =np.empty(10, dtype=object)
        T4 =np.empty(10, dtype=object)
        T5 =np.empty(10, dtype=object)
        T6 =np.empty(10, dtype=object)
        T1[0] = m.atan2(-Py,-Px)
        
        a3 = 2*d2*d3
        b3 = -2*(d4+d5)*d2
        c3 = Px*Px + Py*Py + Pz*Pz + d1*d1 + 2*Px*m.cos(T1[0])*d1 + 2*Py*m.sin(T1[0])*d1 - d2*d2 - d3*d3 -(d4+d5)*(d4+d5)
        m1 = m.sqrt(a3*a3+b3*b3-c3*c3)
        T3[0]= m.atan2(b3,a3) + m.atan2(m1,c3)
        the1 = np.rad2deg(T1[0])
        the3 = np.rad2deg(T3[0])
        
        a= d2 -(d4+d5)*np.sind(the3) + d3*np.cosd(the3)
        b = d3*np.sind(the3) + (d4+d5)*np.cosd(the3)
        c = np.cosd(the1)*Px + np.sind(the1)*Py + d1
        d = Pz;
        T2[0]= m.atan2(a*d-b*c,a*c+b*d);
        the2 = np.rad2deg(T2[0]);
        
        T_03 = np.matrix([[np.cosd(the2 + the3)*np.cosd(the1)  ,   -np.sind(the2 + the3)*np.cosd(the1) ,    np.sind(the1)   ,  -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                           [np.cosd(the2 + the3)*np.sind(the1)  ,   -np.sind(the2 + the3)*np.sind(the1) ,   -np.cosd(the1)   ,  -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                           [np.sind(the2 + the3)              ,    np.cosd(the2 + the3)             ,  0               ,       d2*np.sind(the2)               ],
                           [                0               ,                0                  ,  0               ,                   1]])
        T_03_inv =np.linalg.inv(T_03)
        
        
        a5= T_03_inv[1,0]*r13+T_03_inv[1,1]*r23+T_03_inv[1,2]*r33+T_03_inv[1,3]*r43;
        T5[0]=m.atan2(m.sqrt(1-a5*a5),a5)
        the5 = np.rad2deg(T5[0])
        
        a4= (T_03_inv[2,0]*r13+T_03_inv[2,1]*r23+T_03_inv[2,2]*r33+T_03_inv[2,3]*r43)/np.sind(the5)
        b4= -(T_03_inv[0,0]*r13+T_03_inv[0,1]*r23+T_03_inv[0,2]*r33+T_03_inv[0,3]*r43)/np.sind(the5)
        T4[0]= m.atan2(a4,b4)
        the4= np.rad2deg(T4[0])
        
        T_05 =np.matrix( [[-np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,     np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))       ,   d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))   ,     -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))   ,     -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5) ,                                                                                                                              np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)   ,                                                                            np.sind(the2 + the3)*np.sind(the4)                                   ,           np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                               ,                                                                                                          0       ,                                                                                          0        ,                                                                                                   1]])                                                                                                                                                                                                                                                                                                                   
                 
        T_05_inv = np.linalg.inv(T_05) 
        a6=T_05_inv[0,0]*r11+T_05_inv[0,1]*r21+T_05_inv[0,2]*r31+T_05_inv[0,3]*r41
        b6=-(T_05_inv[2,0]*r11+T_05_inv[2,1]*r21+T_05_inv[2,2]*r31+T_05_inv[2,3]*r41)
        T6[0]=m.atan2(b6,a6)
        the6= np.rad2deg(T6[0])
        sum2 = np.array([the1,the2,the3,
                         the4,the5,the6]) 
        return sum2
    
    def forward_kinemtic_draw(the):
        d0 = 14.5 
        d1 = 2.87
        d2 = 25.5
        d3 = 1.8
        d4 = 7.2
        d5 = 17.7
        d6=  0
        d7= 6.5
        the1=float(the[0])
        the2=float(the[1])
        the3=float(the[2])
        the4=float(the[3])
        the5=float(the[4])
        the6=float(the[5])
        np.cosd = lambda x : np.cos( np.deg2rad(x) )
        np.sind = lambda x : np.sin( np.deg2rad(x) )
        T_01 = np.array([[np.cosd(the1) , -np.sind(the1) , 0 , 0],
                          [np.sind(the1) ,  np.cosd(the1) , 0 , 0],
                          [0     ,      0  ,  1 , 0],
                          [0     ,      0  ,  0 , 1]])
                   
        T_02 = np.array([[ np.cosd(the1)*np.cosd(the2),  -np.cosd(the1)*np.sind(the2)  ,   np.sind(the1)  , -d1*np.cosd(the1)],
                          [np.cosd(the2)*np.sind(the1),  -np.sind(the1)*np.sind(the2)   , -np.cosd(the1)  , -d1*np.sind(the1)],
                          [np.sind(the2),              np.cosd(the2)     ,        0     ,           0],
                          [          0,                       0         ,    0        ,      1]])
                                 
        T_03 = np.array([[ np.cosd(the2 + the3)*np.cosd(the1)  ,  -np.sind(the2 + the3)*np.cosd(the1)  ,   np.sind(the1)  ,   -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.cosd(the2 + the3)*np.sind(the1)  ,  -np.sind(the2 + the3)*np.sind(the1)  ,  -np.cosd(the1)  ,   -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.sind(the2 + the3)        ,        np.cosd(the2 + the3)   ,          0        ,              d2*np.sind(the2)],
                          [                   0         ,                      0         ,     0             ,                     1]])
        
        T_04 = np.array([[ -np.sind(the1)*np.sind(the4)-np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the1)*np.cosd(the2)*np.cosd(the3))  ,      np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))-np.cosd(the4)*np.sind(the1)   ,    -np.sind(the2 + the3)*np.cosd(the1)   ,     d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5) - d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,     np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,   -np.sind(the2 + the3)*np.sind(the1)    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5) - d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.sind(the2 + the3)*np.cosd(the4)                      ,                                                              -np.sind(the2 + the3)*np.sind(the4)           ,       np.cosd(the2 + the3)                               ,                      np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2+the3)+d2*np.sind(the2)],
                          [0                                                       ,                                                         0           ,                      0               ,                                                                                                    1]])
         
          
        T_05 = np.array([[ -np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))    ,      d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))     ,   -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))    ,    -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))   ,     d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5)          ,                                                                                                                     np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)    ,                                                                           np.sind(the2 + the3)*np.sind(the4)              ,                                np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0            ,                                                                                     0                                      ,                                                                     1]])
                          
        T_06 = np.array([[-np.sind(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))  ,      np.sind(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))-np.cosd(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))          ,       d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.sind(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))+np.cosd(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,       np.cosd(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,    -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))         ,       d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.sind(the4)*np.sind(the6)           ,                                                                                                                                                                                 -np.sind(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.cosd(the6)*np.sind(the4)                               ,                                                                                                               np.cosd(the2 + the3)*np.cosd(the5)-np.sind(the2 + the3)*np.cosd(the4)*np.sind(the5)                        ,                                     np.cosd(the2 + the3)*(d4 + d5)+d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0        ,                                                                                         0        ,                                                                                                   1]])
        P1_1org = np.array([0,0,0])
        P2_2org = np.array([0,0,0])
        P3_3org = np.array([0,0,0])
        P3_ee=    np.array([d3,0,0])
        P4_4org = np.array([0,0,-d5])
        P5_5org = np.array([0,0,0])
        P6_ee = np.array([0,0,d6+d7])
        P_0_1_EX = np.dot(T_01,np.append(P1_1org,1))
        P_0_2_EX = np.dot(T_02,np.append(P2_2org,1))
        P_0_3_EX = np.dot(T_03,np.append(P3_3org,1))
        P_0_3ee  = np.dot(T_03,np.append(P3_ee,1))
        P_0_4_EX = np.dot(T_04,np.append(P4_4org,1))
        P_0_5_EX = np.dot(T_05,np.append(P5_5org,1))
        P_0_6_EX = np.dot(T_06,np.append(P6_ee,1))
        
        
        
    
        X=np.array([P_0_1_EX[0],P_0_2_EX[0],P_0_3_EX[0],P_0_3ee[0],P_0_4_EX[0],P_0_5_EX[0],P_0_6_EX[0]])
        Y=np.array([P_0_1_EX[1],P_0_2_EX[1],P_0_3_EX[1],P_0_3ee[1], P_0_4_EX[1],P_0_5_EX[1],P_0_6_EX[1]])
        Z=np.array([P_0_1_EX[2],P_0_2_EX[2],P_0_3_EX[2],P_0_3ee[2], P_0_4_EX[2],P_0_5_EX[2],P_0_6_EX[2]])
        return X,Y,Z
    def forward_kinemtic(the):
        d0 = 14.5 
        d1 = 2.87
        d2 = 25.5
        d3 = 1.8
        d4 = 7.2
        d5 = 17.7
        d6=  0
        d7= 6.5
        the1=float(the[0])
        the2=float(the[1])
        the3=float(the[2])
        the4=float(the[3])
        the5=float(the[4])
        the6=float(the[5])
        np.cosd = lambda x : np.cos( np.deg2rad(x) )
        np.sind = lambda x : np.sin( np.deg2rad(x) )
        T_01 = np.array([[np.cosd(the1) , -np.sind(the1) , 0 , 0],
                          [np.sind(the1) ,  np.cosd(the1) , 0 , 0],
                          [0     ,      0  ,  1 , 0],
                          [0     ,      0  ,  0 , 1]])
                   
        T_02 = np.array([[ np.cosd(the1)*np.cosd(the2),  -np.cosd(the1)*np.sind(the2)  ,   np.sind(the1)  , -d1*np.cosd(the1)],
                          [np.cosd(the2)*np.sind(the1),  -np.sind(the1)*np.sind(the2)   , -np.cosd(the1)  , -d1*np.sind(the1)],
                          [np.sind(the2),              np.cosd(the2)     ,        0     ,           0],
                          [          0,                       0         ,    0        ,      1]])
                                 
        T_03 = np.array([[ np.cosd(the2 + the3)*np.cosd(the1)  ,  -np.sind(the2 + the3)*np.cosd(the1)  ,   np.sind(the1)  ,   -np.cosd(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.cosd(the2 + the3)*np.sind(the1)  ,  -np.sind(the2 + the3)*np.sind(the1)  ,  -np.cosd(the1)  ,   -np.sind(the1)*(d1 - d2*np.cosd(the2))],
                          [ np.sind(the2 + the3)        ,        np.cosd(the2 + the3)   ,          0        ,              d2*np.sind(the2)],
                          [                   0         ,                      0         ,     0             ,                     1]])
        
        T_04 = np.array([[ -np.sind(the1)*np.sind(the4)-np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the1)*np.cosd(the2)*np.cosd(the3))  ,      np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))-np.cosd(the4)*np.sind(the1)   ,    -np.sind(the2 + the3)*np.cosd(the1)   ,     d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5) - d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3) - np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,     np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))    ,   -np.sind(the2 + the3)*np.sind(the1)    ,    d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5) - d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.sind(the2 + the3)*np.cosd(the4)                      ,                                                              -np.sind(the2 + the3)*np.sind(the4)           ,       np.cosd(the2 + the3)                               ,                      np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2+the3)+d2*np.sind(the2)],
                          [0                                                       ,                                                         0           ,                      0               ,                                                                                                    1]])
         
          
        T_05 = np.array([[ -np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))   ,    np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3))    ,      d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))     ,   -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))    ,    -np.cosd(the1)*np.cosd(the4)-np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1))   ,     d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2+the3)*np.cosd(the4)*np.cosd(the5)          ,                                                                                                                     np.cosd(the2+the3)*np.cosd(the5)-np.sind(the2+the3)*np.cosd(the4)*np.sind(the5)    ,                                                                           np.sind(the2 + the3)*np.sind(the4)              ,                                np.cosd(the2 + the3)*(d4 + d5) + d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0            ,                                                                                     0                                      ,                                                                     1]])
                          
        T_06 = np.array([[-np.sind(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))  ,      np.sind(the6)*(np.cosd(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))+np.sind(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2)))-np.cosd(the6)*(np.cosd(the4)*np.sind(the1)-np.sind(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))    ,    np.sind(the5)*(np.sind(the1)*np.sind(the4)+np.cosd(the4)*(np.cosd(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the1)*np.cosd(the2)*np.cosd(the3)))-np.cosd(the5)*(np.cosd(the1)*np.cosd(the2)*np.sind(the3)+np.cosd(the1)*np.cosd(the3)*np.sind(the2))          ,       d3*np.cosd(the2 + the3)*np.cosd(the1)-np.sind(the2 + the3)*np.cosd(the1)*(d4 + d5)-d1*np.cosd(the1)+d2*np.cosd(the1)*np.cosd(the2)],
                          [np.sind(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))+np.cosd(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,       np.cosd(the6)*(np.cosd(the1)*np.cosd(the4)+np.sind(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the6)*(np.cosd(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.sind(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2)))   ,    -np.sind(the5)*(np.cosd(the1)*np.sind(the4)-np.cosd(the4)*(np.sind(the1)*np.sind(the2)*np.sind(the3)-np.cosd(the2)*np.cosd(the3)*np.sind(the1)))-np.cosd(the5)*(np.cosd(the2)*np.sind(the1)*np.sind(the3)+np.cosd(the3)*np.sind(the1)*np.sind(the2))         ,       d3*np.cosd(the2 + the3)*np.sind(the1)-np.sind(the2 + the3)*np.sind(the1)*(d4 + d5)-d1*np.sind(the1)+d2*np.cosd(the2)*np.sind(the1)],
                          [np.cosd(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.sind(the4)*np.sind(the6)           ,                                                                                                                                                                                 -np.sind(the6)*(np.cosd(the2 + the3)*np.sind(the5)+np.sind(the2 + the3)*np.cosd(the4)*np.cosd(the5))-np.sind(the2 + the3)*np.cosd(the6)*np.sind(the4)                               ,                                                                                                               np.cosd(the2 + the3)*np.cosd(the5)-np.sind(the2 + the3)*np.cosd(the4)*np.sind(the5)                        ,                                     np.cosd(the2 + the3)*(d4 + d5)+d3*np.sind(the2 + the3)+d2*np.sind(the2)],
                          [0                                                                                          ,                                                                                               0        ,                                                                                         0        ,                                                                                                   1]])

    
        p6_EE = (np.matrix([0.0,0.0,float(d6+d7),1.0])).T
        p_0_6_EX =np.dot(T_06,p6_EE)
        X = str(p_0_6_EX[0][0]).strip("[]")
        Y = str(p_0_6_EX[1][0]).strip("[]")
        Z = str(p_0_6_EX[2][0]).strip("[]")
        return float(X),float(Y),float(Z)

    def send(self,x,y,z):
       self.time = str(6)
       self.xposvalue.setText(str(x))
       self.yposvalue.setText(str(y))
       self.zposvalue.setText(str(z))
       self.setthe = np.round_(UIFunctions.inverse_kinematic(x,y,z),1)
       self.sum = np.array([self.setthe[0],self.setthe[1],self.setthe[2],
                               self.setthe[3],self.setthe[4],self.setthe[5],self.time])
       if(self.ser.isOpen()):
            self.ser.write('{},{},{},{},{},{},{}'.format(*self.sum).encode())
            Data_send =str('{},{},{},{},{},{},{}'.format(*self.sum))
            self.ser.flushInput()  #flush input buffer, discarding all its contents
            self.ser.flushOutput()
            print(Data_send)

    def forward_signal(self):
        set_x = float(self.xposvalue.text()) - 10.0
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text())
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def backward_signal(self):
        set_x = float(self.xposvalue.text()) + 10.0
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text())
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def left_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) - 10.0
        set_z = float(self.zposvalue.text())
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def right_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) + 10.0
        set_z = float(self.zposvalue.text())
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def up_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text()) 
        set_z = float(self.zposvalue.text()) + 10.0
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def down_signal(self):
        set_x = float(self.xposvalue.text())
        set_y = float(self.yposvalue.text())
        set_z = float(self.zposvalue.text()) - 10.0
        UIFunctions.send(self,set_x,set_y,set_z)
        
    def uiDefinitions(self):
        UIFunctions.list_port(self)
        UIFunctions.set_up_voice(self)
     
