# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 04:38:33 2021

@author: Leonard
"""

import sys
import matplotlib
import serial.tools.list_ports
import serial
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import numpy as np
import sounddevice as sd

import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from function_realtime import *

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_facecolor('#343b48')
        plt.style.use("seaborn-notebook")
        self.axes = fig.add_subplot(111,projection='3d')
        self.axes.set_facecolor('#343b48')

        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()
        
class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi('main.ui',self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons\24x24\cil-microphone.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        #self.threadpool = QtCore.QThreadPool()
        
        self.canvas = MplCanvas(self, width=25, height=25, dpi=70)
        self.ui.formLayout.addWidget(self.canvas)
        self.reference_plot = None
        self.ser =  serial.Serial()
        UIFunctions.uiDefinitions(self)
        self.read()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(100) #msec
        self.timer.timeout.connect(self.read)
        self.timer.start()

        self.btnconnect.clicked.connect(lambda: UIFunctions.connect_clicked(self))
        self.btn_disconnect.clicked.connect(lambda: UIFunctions.disconnect_clicked(self))
        self.btn_record.clicked.connect(lambda: UIFunctions.Record_Fcn(self))
        self.btn_up.clicked.connect(lambda: UIFunctions.forward_signal(self))
        self.btn_down.clicked.connect(lambda: UIFunctions.backward_signal(self))
        self.btn_right.clicked.connect(lambda: UIFunctions.right_signal(self))
        self.btn_left.clicked.connect(lambda: UIFunctions.left_signal(self)) 
        self.btn_z_down.clicked.connect(lambda: UIFunctions.down_signal(self))         
        self.btn_z_up.clicked.connect(lambda: UIFunctions.up_signal(self))
    def keyPressEvent(self, event): # doesnt work when app is in background
        if event.key() == Qt.Key_R:
            UIFunctions.Record_Fcn(self)
            
    def read(self):
        if self.ser.isOpen():
            strdata = self.ser.readline().decode()
            
            self.ser.flushInput()
            self.ser.flushOutput()
            time.sleep(0.1)
            self.theta = strdata.split()
            x,y,z = UIFunctions.forward_kinemtic_draw(self.theta)
            self.canvas.axes.clear()
            self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=10)
            self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=10)
            self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=10)
            self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=10)
            self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=10)
            self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linewidth=10)
        
        
            self.canvas.axes.scatter(x[0], y[0], z[0], marker="H", color='black',linewidth=10)
            self.canvas.axes.scatter(x[1], y[1], z[1], color='black',linewidth=5)
            self.canvas.axes.scatter(x[2], y[2], z[2], color='black',linewidth=10)
            self.canvas.axes.scatter(x[3], y[3], z[3], color='black',linewidth=10)
            self.canvas.axes.scatter(x[4], y[4], z[4], color='black',linewidth=10)
            self.canvas.axes.scatter(x[5], y[5], z[5], color='black',linewidth=10)
            self.canvas.axes.scatter(x[6], y[6],z[6],  marker="v",color='red',linewidth=3)
            
            
            label = '  (%d, %d, %d)' % (x[6], y[6],z[6])
            self.canvas.axes.text(x[6],y[6],z[6],label,fontsize=10,color='red')
            self.canvas.axes.set_xlim(-40, 15)
            self.canvas.axes.set_ylim(-25, 15)
            self.canvas.axes.set_zlim(-5, 20)
            self.canvas.draw()
                
            if len(self.theta) == 6:
                self.valuethe1.setText(self.theta[0])
                self.valuethe2.setText(self.theta[1])
                self.valuethe3.setText(self.theta[2])
                self.valuethe4.setText(self.theta[3])
                self.valuethe5.setText(self.theta[4])
                self.valuethe6.setText(self.theta[5])
                
    def start_worker(self):
        worker = Worker(self.update_plot, )
        self.threadpool.start(worker)
        
    def update_plot(self):
            while self.ser.isOpen():
                theta1 = self.theta
                x,y,z = UIFunctions.forward_kinemtic_draw(theta1)
                self.canvas.axes.clear()
                self.canvas.axes.plot([x[0],x[1]],[y[0],y[1]],[z[0],z[1]], linewidth=5)
                self.canvas.axes.plot([x[1],x[2]],[y[1],y[2]],[z[1],z[2]],linewidth=5)
                self.canvas.axes.plot([x[2],x[3]],[y[2],y[3]],[z[2],z[3]],linewidth=5)
                self.canvas.axes.plot([x[3],x[4]],[y[3],y[4]],[z[3],z[4]],linewidth=5)
                self.canvas.axes.plot([x[4],x[5]],[y[4],y[5]],[z[4],z[5]],linewidth=5)
                self.canvas.axes.plot([x[5],x[6]],[y[5],y[6]],[z[5],z[6]],linewidth=5)
            
            
                self.canvas.axes.scatter(x[0], y[0], z[0], marker="H", color='black',linewidth=10)
                self.canvas.axes.scatter(x[1], y[1], z[1], color='black',linewidth=10)
                self.canvas.axes.scatter(x[2], y[2], z[2], color='black',linewidth=10)
                self.canvas.axes.scatter(x[3], y[3], z[3], color='black',linewidth=10)
                self.canvas.axes.scatter(x[4], y[4], z[4], color='black',linewidth=10)
                self.canvas.axes.scatter(x[5], y[5], z[5], color='black',linewidth=10)
                self.canvas.axes.scatter(x[6], y[6],z[6],  marker="v",color='red',linewidth=2)
                
                
                label = '  (%d, %d, %d)' % (x[6], y[6],z[6])
                self.canvas.axes.text(x[6],y[6],z[6],label,fontsize=7,color='red')
                self.canvas.axes.get_zorder().set_visible(False)
                self.canvas.axes.get_xaxis().set_visible(True)
                self.canvas.axes.get_yaxis().set_visible(True)
                self.canvas.axes.set_xlim(-40, 15)
                self.canvas.axes.set_ylim(-15, 15)
                self.canvas.axes.set_zlim(-1, 20)
                self.canvas.draw()

class Worker(QtCore.QRunnable):

    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):

        self.function(*self.args, **self.kwargs)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle('Manual By Voice:: Applications')
    window.show()
    sys.exit(app.exec_())
