import vxi11
import matplotlib
import matplotlib.pyplot as plt

class Osci ():

    def __init__(self , ip):
        self.os =  vxi11.Instrument(str(ip))
        self.indexVol = 0
        self.indexTime = 0
        self.indexcoupling = 0
        self.start_trig_lv = 0
        self.indexTrigSweep = 0
        self.probeRatio = "1"
        self.channel = "1"
        self.ch_on = True

    def run (self): # run
        self.os.write(':RUN')
    
    def auto (self):
        self.os.write(':AUToscale')
    def ch_display (self,ch): #display ch 
        if (self.ch_on):
            self.os.write(f"CHAN{str(ch)}:DISP ON")
            self.os.write(f':CHANnel{str(ch)}:PROBe {self.probeRatio}')
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

    def set_time_scale (self , scale):
        self.os.write(':TIM:MAIN:SCAL ' + str(scale))

    def tg_lv(self, value):
        self.start_trig_lv = self.start_trig_lv + value
        self.os.write(f':TRIGger:EDGe:LEV {str(self.start_trig_lv)}')
    
    def setProbeRatio(self, channel,value):
        self.os.write(f':CHANnel{str(channel)}:PROBe {str(value)}')
        self.probeRatio = value
        self.set_vol_scale()

    def setCoupling(self):
        coupList = ["DC, AC, GND"]
        if self.indexcoupling<0:
            self.indexVol = 0
            self.os.write(f':CHANnel{self.channel}:COUPling {coupList[self.indexcoupling]}')
        if self.indexcoupling>len(coupList):
            self.indexVol=len(coupList)
            self.os.write(f':CHANnel{self.channel}:COUPling {coupList[self.indexcoupling]}')
        self.os.write(f':CHANnel{self.channel}:COUPling {coupList[self.indexcoupling]}')
        self.indexcoupling +=1
    
    def setTrigSweep(self):
        sweepList = ["AUTO", "NORM", "SING"]
        if self.indexTrigSweep<0:
            self.indexVol = 0
            self.os.write(f":TRIGger:SWEep {sweepList[self.indexTrigSweep]}")
        if self.indexTrigSweep>len(sweepList):
            self.indexVol=len(volLsweepListist)
            self.os.write(f":TRIGger:SWEep {sweepList[self.indexTrigSweep]}")
        self.os.write(f":TRIGger:SWEep {sweepList[self.indexTrigSweep]}")
        self.indexTrigSweep += 1

    def setTrigSource(self):
        self.os.write(f":TRIGger:EDGe:SOURce {self.channel}")

    


