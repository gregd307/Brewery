import sys
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from Process_Control import *
from temprature import sent_temp
global s3,h3,m3,time1,time2


time1 = 0
time2 = 0
s3 = 0
m3 = 0
h3 = 0
def Alarm(self):
        global alarm1,alarm2,time1,time2
        
        for x, y in alarm1.iteritems():
            
            if x.isChecked():
                a = y.time()
                h = a.hour()
                m = a.minute()
                s = a.second()
                
                time4 = ("{0}:{1}:{2}".format(h,m,s))
                if time4 == time1:
                     print "ALARM 1 ACTIVE"
                     os.system('sh -c "echo high > /sys/class/gpio/gpio18/direction"')
                     
                        
        for x, y in alarm2.iteritems():
            if x.isChecked():
                a = y.time()
                h = a.hour()
                m = a.minute()
                s = a.second()
                
                time4 = ("{0}:{1}:{2}".format(h,m,s))
                if time4 == time2:
                     print "ALARM 2 ACTIVE"
                     os.system('sh -c "echo high > /sys/class/gpio/gpio18/direction"')
                     
                       










class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.get_temp = Get_Temp()
        self.timer = QtCore.QTimer(self)
        self.connect(self.get_temp, SIGNAL("display_temp()"),self.display_temp,Qt.DirectConnection)

        self.get_temp.start()
        self.timer.timeout.connect(self.Time)
        self.HTL_Start.clicked.connect(self.Set)
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.Time2)
        self.BOIL_TIMER_START.clicked.connect(self.Set2)
        self.timer3 = QtCore.QTimer(self)
        self.timer3.timeout.connect(self.Time3)
        self.START_TIMER.clicked.connect(self.Start)
        self.STOP_TIMER.clicked.connect(lambda: self.timer3.stop())
        self.RESET_TIMER.clicked.connect(self.Reset)
        self.pushButton.clicked.connect(self.Alarm_Reset)
        global alarm1,alarm2
        alarm1 = {self.HLT_alarm_set1:self.ALARM_HLT_1,self.HLT_alarm_set1_2:self.ALARM_HLT_2,self.HLT_alarm_set1_3:self.ALARM_HLT_3,self.HLT_alarm_set1_4:self.ALARM_HLT_4,self.HLT_alarm_set1_5:self.ALARM_HLT_5}
        alarm2 = {self.Boil_alarm_set1:self.ALARM_BOIL_1,self.Boil_alarm_set1_2:self.ALARM_BOIL_2,self.Boil_alarm_set1_3:self.ALARM_BOIL_3,self.Boil_alarm_set1_4:self.ALARM_BOIL_4,self.Boil_alarm_set1_5:self.ALARM_BOIL_5}    
        
        
         
    
    def Alarm_Reset(self):
        os.system('sh -c "echo low > /sys/class/gpio/gpio18/direction"')
                       

       
                    

    def Reset(self):
        global s3,m3,h3
        self.timer3.stop()
        
        s3=0
        m3=0
        h3=0
        
        time = "{0}:{1}:{2}".format(h3,m3,s3)
        self.TIMER_DISPLAY.setDigitCount(len(time))
        self.TIMER_DISPLAY.display(time)

    def Start(self):
        global s3,m3,h3
        self.timer3.start(1000)
    
    def Time3(self):
        global s3,m3,h3
        
        if s3<59:
            s3 += 1
        else:
            if m3 < 59:
                s3 = 0
                m3 += 1
            elif m3 == 59 and h3 < 24:
                h3 += 1
                m3 = 0
                s3= 0
            else:
                self.timer3.stop()
        time = "{0}:{1}:{2}".format(h3,m3,s3)

        self.TIMER_DISPLAY.setDigitCount(len(time))
        self.TIMER_DISPLAY.display(time)
        

    def Set(self):
        global t,h,m,s
        t = self.HLT_TIMER_SET.time()
        self.HLT_Timer_DISPLAY.display(t.toString())
        self.timer.start(1000)
        
        h = t.hour()
        m = t.minute()
        s = t.second()
        
        
    
    def Time(self):
        global t,h,m,s,time1
        
        
        if s > 0:
            s -= 1
        else:
            if m > 0:
                m -= 1
                s = 59
            elif m == 0 and h > 0:
                h -= 1
                m = 59
                s = 59
            else:
                self.timer.stop()
        time1 = ("{0}:{1}:{2}".format(h,m,s))
        Alarm(self)
        self.HLT_Timer_DISPLAY.setDigitCount(len(time1))
        self.HLT_Timer_DISPLAY.display(time1)
        
    def Set2(self):
        global t2,h2,m2,s2
        t2 = self.BOIL_TIMER_SET.time()
        self.BOIL_TIMER_DISPLAY.display(t2.toString())
        self.timer2.start(1000)
        
        h2 = t2.hour()
        m2 = t2.minute()
        s2 = t2.second()
        
        
    
    def Time2(self):
        global t2,h2,m2,s2,time2
        
        
        if s2 > 0:
            s2 -= 1
        else:
            if m2 > 0:
                m2 -= 1
                s2 = 59
            elif m2 == 0 and h2 > 0:
                h2 -= 1
                m2 = 59
                s2 = 59
            else:
                self.timer2.stop()
        time2 = ("{0}:{1}:{2}".format(h2,m2,s2))
        Alarm(self)
        self.BOIL_TIMER_DISPLAY.setDigitCount(len(time2))
        self.BOIL_TIMER_DISPLAY.display(time2)

 





    def display_temp(self):
            temp = sent_temp()
            self.HLT_TEMP.display(temp[0])
            self.MASH_TEMP.display(temp[1])
            self.Boil_TEMP.display(temp[2])

class Get_Temp(QThread):
    def __init__(self, parent = None):
        super(Get_Temp,self).__init__(parent)

    def run(self):
        while True:
            self.emit(SIGNAL("display_temp()"))
            
    