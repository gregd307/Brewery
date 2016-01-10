import sys
import os
from PyQt4 import QtCore, QtGui
from Brew import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from temprature import sent_temp
global s3,h3,m3,time1,time2,M1,temp1,temp2,temp3

#initializes some varables
m3 = 0
M1 = []
temp1=[]
temp2=[]
temp3=[]
time1 = 0
time2 = 0
s3 = 0
m3 = 0
h3 = 0

#class that defines what each object does
class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
#defines thread get_temp
        self.get_temp = Get_Temp()
#defines thread get_data
        self.get_data = Get_Data()
#defines timer
        self.timer = QtCore.QTimer(self)
#signal to start threads
        self.connect(self.get_temp, SIGNAL("display_temp()"),self.display_temp,Qt.DirectConnection)
        self.connect(self.get_data, SIGNAL("plot()"),self.plot,Qt.DirectConnection)
#defines a graph and plots it in vertical layout
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.verticalLayout.addWidget(self.canvas)        
#starts get_temp thread
        self.get_temp.start()
#starts timer
        self.timer.timeout.connect(self.Time)
#HLT timer button signal
        self.HTL_Start.clicked.connect(self.Set)
#defines and starts timer2
        self.timer2 = QtCore.QTimer(self)
        self.timer2.timeout.connect(self.Time2)
#Boil timer button signal
        self.BOIL_TIMER_START_2.clicked.connect(self.Set2)
#defines and starts timer3        
        self.timer3 = QtCore.QTimer(self)
        self.timer3.timeout.connect(self.Time3)
#signals for graph timmer buttons
        self.START_TIMER.clicked.connect(self.Start)
        self.STOP_TIMER.clicked.connect(lambda: self.timer3.stop())
        self.RESET_TIMER.clicked.connect(self.Reset)
        self.ALARM_RESET.clicked.connect(self.Alarm_Reset)
#dictionaries for alarm values
        global alarm1,alarm2
        alarm1 = {self.HLT_alarm_set1:self.ALARM_HLT_1,self.HLT_alarm_set1_2:self.ALARM_HLT_2,self.HLT_alarm_set1_3:self.ALARM_HLT_3,self.HLT_alarm_set1_4:self.ALARM_HLT_4,self.HLT_alarm_set1_5:self.ALARM_HLT_5}
        alarm2 = {self.Boil_alarm_set1:self.ALARM_BOIL_1,self.Boil_alarm_set1_2:self.ALARM_BOIL_2,self.Boil_alarm_set1_3:self.ALARM_BOIL_3,self.Boil_alarm_set1_4:self.ALARM_BOIL_4,self.Boil_alarm_set1_5:self.ALARM_BOIL_5}    
#signals for file dropdown buttons
        self.actionQuit.triggered.connect(self.close_application)
        self.actionSave.triggered.connect(self.save_application)
        self.actionLoad.triggered.connect(self.load_application)
        self.actionNew.triggered.connect(self.reset_data)

#closes the application       
    def close_application(self):
        print("window close")
        sys.exit()
        
#gets data from form and saves it to a file
    def save_application(self):
        self.get_data()
        text2 = []
        name = QtGui.QFileDialog.getSaveFileName()
        file = open(name,'w')        
        for i in self.form_field:
            file.write(i + "\n")
        file.close()
        file = ""
        self.form_field = []
        print ("saved")
        
#Gets data from a file and send it to get_data
    def load_application(self):
        self.reset_data()
        temp=[]
        name = QtGui.QFileDialog.getOpenFileName()
        file = open(name,'r')
        for i in file:
            temp1 = i[:-1]
            temp.append(temp1)
        file.close()
        file = ""
            
        self.load_data(temp)    
        print ("loaded")
        
#Gets data from Receipe form
    def get_data(self):
        self.form_field = [self.Brewer_name_txt.text(),
        self.Brew_Date_txt.text(),
        self.Batch_size_txt.text(),
        self.boil_time_txt.text(),
        self.Ingredient_one.text(),
        self.Amount_one.text(),
        self.Ingredient_three.text(),
        self.Amount_three.text(),
        self.Ingredient_two.text(),
        self.Amount_two.text(),
        self.Ingredient_four.text(),
        self.Alcohol_volume_txt.text(),
        self.Amount_four.text(),
        self.Ingredient_five.text(),
        self.Amount_five.text(),
        self.Hop_one.text(),
        self.hop_amount_one.text(),
        self.hop_AA_one.text(),
        self.hop_boil_one.text(),
        self.hop_amount_two.text(),
        self.hop_boil_two.text(),
        self.hop_AA_two.text(),
        self.hop_two.text(),
        self.hop_amount_three.text(),
        self.hop_boil_three.text(),
        self.hop_AA_three.text(),
        self.hop_3.text(),
        self.hop_amount_four.text(),
        self.hop_boil_four.text(),
        self.hop_AA_four.text(),
        self.hop_4.text(),
        self.hop_amount_five.text(),
        self.hop_boil_five.text(),
        self.hop_AA_five.text(),
        self.hop_five.text(),
        self.original_gravity_txt.text(),
        self.final_gravity_txt.text(),
        self.IBU_txt.text(),
        self.SRM_txt.text(),
        self.Brewhouse_efficiency_txt.text(),
        self.Carbonation_level_txt.text(),
        self.hydrometer_preboil_date_txt.text(),
        self.hydrometer_afterboil_date_txt.text(),
        self.hydrometer_racked_date_txt.text(),
        self.hydrometer_final_date_txt.text(),
        self.hydrometer_preboil_gravity_txt.text(),
        self.hydrometer_racked_gravity_txt.text(),
        self.hydrometer_final_gravity_txt.text(),
        self.hydrometer_afterboil_gravity_txt.text(),        
        self.Recipe_name_txt.text(),
        self.beer_type_txt.text(),
        self.Batch_txt.text(),
        self.efficiency_txt.text(),
        self.infusion_one_txt.text(),
        self.infusion_temp_one_txt.text(),
        self.infusion_three_txt.text(),
        self.infusion_temp_three_txt.text(),
        self.infusion_two_txt.text(),
        self.infusion_temp_two_txt.text(),
        self.infusion_four_txt.text(),
        self.infusion_temp_four_txt.text(),
        self.infusion_five_txt.text(),
        self.infusion_temp_five_txt.text(),
        self.cost_grains_txt.text(),
        self.cost_grains_txt_2.text(),
        self.cost_yeast_txt.text(),
        self.cost_other_txt.text(),
        self.infusion_time_one_txt.text(),
        self.infusion_time_four_txt.text(),
        self.infusion_time_five_txt.text(),
        self.infusion_time_two_txt.text(),
        self.infusion_time_three_txt.text(),
        self.yeat_starter_txt.text(),
        self.yeast_attenuation_txt.text(),        
        self.yeast_type_txt.text(),       
        self.cost_total_txt.text(),
        self.Notes.toPlainText()]
        
#fills the recipe form with data from a file            
    def load_data(self,x):
        
        self.Brewer_name_txt.setText(x[0])
        self.Brew_Date_txt.setText(x[1])
        self.Batch_size_txt.setText(x[2])
        self.boil_time_txt.setText(x[3])
        self.Ingredient_one.setText(x[4])
        self.Amount_one.setText(x[5])
        self.Ingredient_three.setText(x[6])
        self.Amount_three.setText(x[7])
        self.Ingredient_two.setText(x[8])
        self.Amount_two.setText(x[9])
        self.Ingredient_four.setText(x[10])
        self.Alcohol_volume_txt.setText(x[11])
        self.Amount_four.setText(x[12])
        self.Ingredient_five.setText(x[13])
        self.Amount_five.setText(x[14])
        self.Hop_one.setText(x[15])
        self.hop_amount_one.setText(x[16])
        self.hop_AA_one.setText(x[17])
        self.hop_boil_one.setText(x[18])
        self.hop_amount_two.setText(x[19])
        self.hop_boil_two.setText(x[20])
        self.hop_AA_two.setText(x[21])
        self.hop_two.setText(x[22])
        self.hop_amount_three.setText(x[23])
        self.hop_boil_three.setText(x[24])
        self.hop_AA_three.setText(x[25])
        self.hop_3.setText(x[26])
        self.hop_amount_four.setText(x[27])
        self.hop_boil_four.setText(x[28])
        self.hop_AA_four.setText(x[29])
        self.hop_4.setText(x[30])
        self.hop_amount_five.setText(x[31])
        self.hop_boil_five.setText(x[32])
        self.hop_AA_five.setText(x[33])
        self.hop_five.setText(x[34])
        self.original_gravity_txt.setText(x[35])
        self.final_gravity_txt.setText(x[36])
        self.IBU_txt.setText(x[37])
        self.SRM_txt.setText(x[38])
        self.Brewhouse_efficiency_txt.setText(x[39])
        self.Carbonation_level_txt.setText(x[40])
        self.hydrometer_preboil_date_txt.setText(x[41])
        self.hydrometer_afterboil_date_txt.setText(x[42])
        self.hydrometer_racked_date_txt.setText(x[43])
        self.hydrometer_final_date_txt.setText(x[44])
        self.hydrometer_preboil_gravity_txt.setText(x[45])
        self.hydrometer_racked_gravity_txt.setText(x[46])
        self.hydrometer_final_gravity_txt.setText(x[47])
        self.hydrometer_afterboil_gravity_txt.setText(x[48])        
        self.Recipe_name_txt.setText(x[49])
        self.beer_type_txt.setText(x[50])
        self.Batch_txt.setText(x[51])
        self.efficiency_txt.setText(x[52])
        self.infusion_one_txt.setText(x[53])
        self.infusion_temp_one_txt.setText(x[54])
        self.infusion_three_txt.setText(x[55])
        self.infusion_temp_three_txt.setText(x[56])
        self.infusion_two_txt.setText(x[57])
        self.infusion_temp_two_txt.setText(x[58])
        self.infusion_four_txt.setText(x[59])
        self.infusion_temp_four_txt.setText(x[60])
        self.infusion_five_txt.setText(x[61])
        self.infusion_temp_five_txt.setText(x[62])
        self.cost_grains_txt.setText(x[63])
        self.cost_grains_txt_2.setText(x[64])
        self.cost_yeast_txt.setText(x[65])
        self.cost_other_txt.setText(x[66])
        self.infusion_time_one_txt.setText(x[67])
        self.infusion_time_four_txt.setText(x[68])
        self.infusion_time_five_txt.setText(x[69])
        self.infusion_time_two_txt.setText(x[70])
        self.infusion_time_three_txt.setText(x[71])
        self.yeat_starter_txt.setText(x[72])
        self.yeast_attenuation_txt.setText(x[73])        
        self.yeast_type_txt.setText(x[74]) 
        self.cost_total_txt.setText(x[75])
        for i in range(76,len(x),1):
            temp = x[i]
            temp = temp[:-1]
            self.Notes.append(temp)
            
        

#fills recipe form with blank spaces
    def reset_data(self):
        x=" "
        self.Brewer_name_txt.setText(x)
        self.Brew_Date_txt.setText(x)
        self.Batch_size_txt.setText(x)
        self.boil_time_txt.setText(x)
        self.Ingredient_one.setText(x)
        self.Amount_one.setText(x)
        self.Ingredient_three.setText(x)
        self.Amount_three.setText(x)
        self.Ingredient_two.setText(x)
        self.Amount_two.setText(x)
        self.Ingredient_four.setText(x)
        self.Alcohol_volume_txt.setText(x)
        self.Amount_four.setText(x)
        self.Ingredient_five.setText(x)
        self.Amount_five.setText(x)
        self.Hop_one.setText(x)
        self.hop_amount_one.setText(x)
        self.hop_AA_one.setText(x)
        self.hop_boil_one.setText(x)
        self.hop_amount_two.setText(x)
        self.hop_boil_two.setText(x)
        self.hop_AA_two.setText(x)
        self.hop_two.setText(x)
        self.hop_amount_three.setText(x)
        self.hop_boil_three.setText(x)
        self.hop_AA_three.setText(x)
        self.hop_3.setText(x)
        self.hop_amount_four.setText(x)
        self.hop_boil_four.setText(x)
        self.hop_AA_four.setText(x)
        self.hop_4.setText(x)
        self.hop_amount_five.setText(x)
        self.hop_boil_five.setText(x)
        self.hop_AA_five.setText(x)
        self.hop_five.setText(x)
        self.original_gravity_txt.setText(x)
        self.final_gravity_txt.setText(x)
        self.IBU_txt.setText(x)
        self.SRM_txt.setText(x)
        self.Brewhouse_efficiency_txt.setText(x)
        self.Carbonation_level_txt.setText(x)
        self.hydrometer_preboil_date_txt.setText(x)
        self.hydrometer_afterboil_date_txt.setText(x)
        self.hydrometer_racked_date_txt.setText(x)
        self.hydrometer_final_date_txt.setText(x)
        self.hydrometer_preboil_gravity_txt.setText(x)
        self.hydrometer_racked_gravity_txt.setText(x)
        self.hydrometer_final_gravity_txt.setText(x)
        self.hydrometer_afterboil_gravity_txt.setText(x)
        self.Recipe_name_txt.setText(x)
        self.beer_type_txt.setText(x)
        self.Batch_txt.setText(x)
        self.efficiency_txt.setText(x)
        self.infusion_one_txt.setText(x)
        self.infusion_temp_one_txt.setText(x)
        self.infusion_three_txt.setText(x)
        self.infusion_temp_three_txt.setText(x)
        self.infusion_two_txt.setText(x)
        self.infusion_temp_two_txt.setText(x)
        self.infusion_four_txt.setText(x)
        self.infusion_temp_four_txt.setText(x)
        self.infusion_five_txt.setText(x)
        self.infusion_temp_five_txt.setText(x)
        self.cost_grains_txt.setText(x)
        self.cost_grains_txt_2.setText(x)
        self.cost_yeast_txt.setText(x)
        self.cost_other_txt.setText(x)
        self.infusion_time_one_txt.setText(x)
        self.infusion_time_four_txt.setText(x)
        self.infusion_time_five_txt.setText(x)
        self.infusion_time_two_txt.setText(x)
        self.infusion_time_three_txt.setText(x)
        self.yeat_starter_txt.setText(x)
        self.yeast_attenuation_txt.setText(x)
        self.yeast_type_txt.setText(x) 
        self.cost_total_txt.setText(x)
        self.Notes.setText(x)

#resets the alarm and sets gpio 18 to low        
    def Alarm_Reset(self):
        os.system('sh -c "echo low > /sys/class/gpio/gpio18/direction"')
                       

       
                    
#Resets timmer for graph
    def Reset(self):
        global s3,m3,h3
        self.timer3.stop()        
        s3=0
        m3=0
        h3=0
        self.get_data.start()
        time = "{0}:{1}:{2}".format(h3,m3,s3)
        self.TIMER_DISPLAY.setDigitCount(len(time))
        self.TIMER_DISPLAY.display(time)

#starts timer for graph
    def Start(self):
        global s3,m3,h3
        self.timer3.start(1000)
        
#Timer for graph and displays time (counts up)   
    def Time3(self):
        global s3,m3,h3           
        
        if s3 == 0:
            self.get_data.start()
            s3 += 1
        if s3 == 30:
            self.get_data.start()
            s3 += 1
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
        
#Sets HLT timer
    def Set(self):
        global t,h,m,s
        t = self.HLT_TIMER_SET.time()
        self.HLT_Timer_DISPLAY.display(t.toString())
        self.timer.start(1000)
        
        h = t.hour()
        m = t.minute()
        s = t.second()
        
        
#Timer for HLT timer(counts the timer down)    
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
        
#Sets boil timer        
    def Set2(self):
        global t2,h2,m2,s2
        t2 = self.BOIL_TIMER_SET.time()
        self.BOIL_TIMER_DISPLAY.display(t2.toString())
        self.timer2.start(1000)
        
        h2 = t2.hour()
        m2 = t2.minute()
        s2 = t2.second()
        
        
#timer for boil timer(counts the timer down)    
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
        
#checks to see if alarm has been triggered and sets gpio 18 to high
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
                     os.system('sh -c "echo low > /sys/class/gpio/gpio18/direction"')
                     
                        
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






#displays temps by calling settemp from temprature.py 
    def display_temp(self):
            temp = sent_temp()
            self.HLT_TEMP.display(temp[0])
            self.MASH_TEMP.display(temp[1])
            self.Boil_TEMP.display(temp[2])
            
#creates a graph and displays it
    def plot(self):
        temp = sent_temp()
        temp1.append(temp[0])
        temp2.append(temp[1])
        temp3.append(temp[2])
        M1.append(m3)        
        XHLT= self.figure.add_subplot(111)             
        XHLT.plot(M1,temp1,'b-',label = "HLT")
        XHLT.plot(M1,temp2,'r-',label = "MASH")
        XHLT.plot(M1,temp3,'g-',label = "BOIL")
        self.canvas.draw()
        self.canvas.update()
        if m3 == 0 and h3 == 0 and s3 == 0:
            XHLT.hold(False)


#thread that gets temprature from sensor and desplays them            
class Get_Temp(QThread):
    def __init__(self, parent = None):
        super(Get_Temp,self).__init__(parent)

    def run(self):
        while True:
            self.emit(SIGNAL("display_temp()"))
            
#Gets data and plots a graph
class Get_Data(QThread):
    def __init__(self, parent = None):
        super(Get_Data,self).__init__(parent)

    def run(self):
        while True:
            self.emit(SIGNAL("plot()"))
            
