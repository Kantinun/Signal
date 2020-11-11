import vxi11
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image
import io
import datetime
import time

class Channel():
    def __init__(self, channel):
        self.indexVol = 0
        self.indexTime = 0
        self.indexcoupling = 0
        self.start_trig_lv = 0
        self.indexTrigSweep = 0
        self.indexTrigSl = 0
        self.vertiPos = 0
        self.horiPos = 0
        self.probeRatio = "1"
        self.channel = str(channel)

class Osci ():
    def __init__(self , ip):
        self.os =  vxi11.Instrument(str(ip))
        self.sweepList = ["AUTO", "NORM", "SING"]
        self.coupList = ["DC", "AC", "GND"]
        self.slopeList = ["POS", "NEG", "RFAL"]

        self.chanList = []
        for i in range(1,5):
            self.chanList.append(Channel(i))

        self.indCh = 0
    
    def run (self): # run
        self.os.write(':RUN')

    def stop (self): # run
        self.os.write(':STOP')
    
    def auto (self):
        self.os.write(':AUToscale')

    def ch_display (self, status): #display ch 
        if status=="on":
            self.os.write(f"CHAN{self.chanList[self.indCh].channel}:DISP ON")
            self.os.write(f':CHANnel{self.chanList[self.indCh].channel}:PROBe {self.chanList[self.indCh].probeRatio}')
            self.chanList[self.indCh].ch_on = False
        elif status == "off":
            self.os.write(f"CHAN{self.chanList[self.indCh].channel}:DISP OFF")
            self.chanList[self.indCh].ch_on = True

    def set_vol_scale (self, direction):
        volList = [str(0.001*int(self.chanList[self.indCh].probeRatio)), str(0.002*int(self.chanList[self.indCh].probeRatio)), str(0.005*int(self.chanList[self.indCh].probeRatio)), str(0.01*int(self.chanList[self.indCh].probeRatio)), str(0.02*int(self.chanList[self.indCh].probeRatio)), str(0.05*int(self.chanList[self.indCh].probeRatio)), str(0.1*int(self.chanList[self.indCh].probeRatio)), str(0.2*int(self.chanList[self.indCh].probeRatio)), str(0.5*int(self.chanList[self.indCh].probeRatio)), str(1*int(self.chanList[self.indCh].probeRatio)), str(2*int(self.chanList[self.indCh].probeRatio)), str(5*int(self.chanList[self.indCh].probeRatio))]
        if self.chanList[self.indCh].indexVol==len(volList):
            self.chanList[self.indCh].indexVol=0
        self.os.write(f"CHAN{self.chanList[self.indCh].channel}:SCAL {volList[self.chanList[self.indCh].indexVol]}")
        if direction == "up":
            self.chanList[self.indCh].indexVol +=1
        elif direction == "down":
            self.chanList[self.indCh].indexVol -=1

    def set_time_scale (self , direction):
        timeList = [str(0.001*int(self.chanList[self.indCh].probeRatio)), str(0.002*int(self.chanList[self.indCh].probeRatio)), str(0.005*int(self.chanList[self.indCh].probeRatio)), str(0.01*int(self.chanList[self.indCh].probeRatio)), str(0.02*int(self.chanList[self.indCh].probeRatio)), str(0.05*int(self.chanList[self.indCh].probeRatio)), str(0.1*int(self.chanList[self.indCh].probeRatio)), str(0.2*int(self.chanList[self.indCh].probeRatio)), str(0.5*int(self.chanList[self.indCh].probeRatio)), str(1*int(self.chanList[self.indCh].probeRatio)), str(2*int(self.chanList[self.indCh].probeRatio)), str(5*int(self.chanList[self.indCh].probeRatio))]
        if self.chanList[self.indCh].indexTime == len(timeList):
            self.chanList[self.indCh].indexTime=0
        self.os.write(f":TIM:MAIN:SCAL {timeList[self.chanList[self.indCh]]}")
        if direction == "up":
            self.chanList[self.indCh].indexTime +=1
        elif direction == "down":
            self.chanList[self.indCh].indexTime -=1

    def tg_lv(self, direction):
        if direction == "up":
            self.chanList[self.indCh].start_trig_lv += 20e-3
        elif direction == "down":
            self.chanList[self.indCh].start_trig_lv -= 20e-3
        print(type(self.chanList[self.indCh].start_trig_lv))
        self.os.write(f':TRIGger:EDGe:LEV {str(self.chanList[self.indCh].start_trig_lv)}')
    
    def setProbeRatio(self, value):
        self.os.write(f':CHANnel{self.chanList[self.indCh].channel}:PROBe {str(value)}')
        self.chanList[self.indCh].probeRatio = value

    def setCoupling(self):
        self.os.write(f':CHANnel{self.chanList[self.indCh].channel}:COUPling {self.coupList[self.chanList[self.indCh].indexcoupling]}')
        self.chanList[self.indCh].indexcoupling +=1
        if self.chanList[self.indCh].indexcoupling==len(self.coupList):
            self.chanList[self.indCh].indexcoupling=0
    
    def setTrigSweep(self):
        self.os.write(f":TRIGger:SWEep {self.sweepList[self.chanList[self.indCh].indexTrigSweep]}")
        self.chanList[self.indCh].indexTrigSweep += 1
        if self.chanList[self.indCh].indexTrigSweep==len(self.sweepList):
            self.chanList[self.indCh].indexTrigSweep=0

    def setTrigSource(self):
        self.os.write(f":TRIGger:EDGe:SOURce CHAN{self.chanList[self.indCh].channel}")

    def setTrigSlope(self):
        self.os.write(f":TRIGger:EDGe:SLOPe {self.slopeList[self.chanList[self.indCh].indexTrigSl]}")
        self.chanList[self.indCh].indexTrigSl += 1
        if self.chanList[self.indCh].indexTrigSl==len(self.slopeList):
            self.chanList[self.indCh].indexTrigSl=0
        
    def setVerticalPosition(self, direction):
        if direction == "up":
            self.chanList[self.indCh].vertiPos += 20e-6
        elif direction == "down":
            self.chanList[self.indCh].vertiPos -= 20e-6
        self.os.write(f":CHANnel1:OFFSet {self.chanList[self.indCh].vertiPos}")
    
    def setHorizontalPosition(self, direction):
        if direction == "up":
            self.chanList[self.indCh].horiPos += 20e-6
        elif direction == "down":
            self.chanList[self.indCh].horiPos -= 20e-6
        self.os.write(f":TIMebase:MAIN:OFFSet {self.chanList[self.indCh].horiPos}")

    def selectCh(self, index):
        self.indCh = index
        self.os.write(f":TRIGger:EDGe:SOURce {self.chanList[self.indCh].channel}")

    def write_screen_capture(self, filename=''):
        self.os.write(':DISP:DATA? ON,OFF,PNG')
        raw_data = self.os.read_raw()[11:] # strip off first 11 bytes
        # save image file
        if (filename == ''):
            filename = "rigol_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".png"
        fid = open(filename, 'wb')
        fid.write(raw_data)
        fid.close()
        return filename