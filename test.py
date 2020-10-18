import vxi11
import matplotlib
import matplotlib.pyplot as plt

# osx =  DS1054Z('169.254.33.140')

class Osci ():

    def __init__(self , ip):
        self.os =  vxi11.Instrument(str(ip))
        self.start_vol_scale = 0
        self.start_trig_lv = 0
        self.ch_on = True

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

    def set_vol_scale (self , ch , value ):
        self.start_vol_scale = self.start_vol_scale + value
        self.os.write(f"CHAN{str(ch)}:SCAL {str(self.start_vol_scale)}")

    def set_time_scale (self , scale ):
        self.os.write(':TIM:MAIN:SCAL ' + str(scale))

    def tg_lv(self, value):
        self.start_trig_lv = self.start_trig_lv + value
        self.os.write(f':TRIGger:EDGe:LEV {str(self.start_trig_lv)}')


print('\n volkzapp')