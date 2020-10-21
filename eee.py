import vxi11
import matplotlib
import matplotlib.pyplot as plt
from PyQt5 import QtWidgets,uic
import datetime
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Osci ():

    def __init__(self , ip):
        self.os =  vxi11.Instrument(str(ip))
        self.probeRatio = "1"
        self.indexVol = 0

    def run (self): # run
        self.os.write(':RUN')
    
    def auto (self):
        self.os.write(':AUToscale')

    def ch_display (self,ch): #display ch 
        if (self.ch_on):
            self.os.write(f"CHAN{str(ch)}:DISP ON")
            self.ch_on = False
        else:
            self.os.write(f"CHAN{str(ch)}:DISP OFF")
            self.ch_on = True

    def set_vol_scale (self , ch, direction):
        volList = [str(0.001*self.probeRatio), str(0.002*self.probeRatio), str(0.005*self.probeRatio), str(0.01*self.probeRatio), str(0.02*self.probeRatio), str(0.05*self.probeRatio), str(0.1*self.probeRatio), str(0.2*self.probeRatio), str(0.5*self.probeRatio), str(1*self.probeRatio), str(2*self.probeRatio), str(5*self.probeRatio)]
        if self.indexVol<0:
            self.indexVol = 0
            self.os.write(f"CHAN{str(ch)}:SCAL {volList[self.indexVol]}")
        if self.indexVol>len(volList):
            self.indexVol=len(volList)
            self.os.write(f"CHAN{str(ch)}:SCAL {volList[self.indexVol]}")
        self.os.write(f"CHAN{str(ch)}:SCAL {volList[self.indexVol]}")
        if direction == "up":
            self.indexVol +=1
        elif direction == "down":
            self.indexVol -=1

    def set_time_scale (self , scale ):
        self.os.write(':TIM:MAIN:SCAL ' + str(scale))

    def tg_lv(self, value):
        self.start_trig_lv = self.start_trig_lv + value
        self.os.write(f':TRIGger:EDGe:LEV {str(self.start_trig_lv)}')

    def write_screen_capture(self, filename=''):
	    self.os.write(':DISP:DATA? ON,OFF,PNG')
	    raw_data = self.os.read_raw()[11:] # strip off first 11 bytes
	    # save image file
	    if (filename == ''):
	        filename = "rigol_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".png"
	    fid = open(filename, 'wb')
	    fid.write(raw_data)
	    fid.close()
        self.image = filename
	    print ("Wrote screen capture to filename " + '\"' + filename + '\"')
	    self.dialog = CaptureImage(self.image)

class CaptureImage(QDialog):

    def __init__(self,item):
        super().__init__()
        self.image = QPixmap.fromImage(item)
        self.hbox = QHBoxLayout(self)
        self.image_label = QLabel(self)
        self.image_label.setPixmap(self.image)
        self.hbox.addWidget(self.image_label)
        self.setLayout(self.hbox)

class Test ():
    def __init__(self):
        self.ip = True

    def plus (self,ch):
        if(self.ip):
            print("ON")
            self.ip = False
        else:
            print("OFF")
            self.ip = True

t = Test()
app = QtWidgets.QApplication([])
call = uic.loadUi("os.ui")
myOsci = Osci("169.254.1.5")



call.btn_run.clicked.connect(myOsci.run)
call.btn_CAP.clicked.connect(lambda : myOsci.write_screen_capture(''))
call.btn_T_slope.clicked.connect()
call.actionExit.triggered.connect(call.close)

call.show()
app.exec()
