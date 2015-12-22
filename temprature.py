import os
import time
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

prob1 = '/sys/bus/w1/devices/28-00000627c414/w1_slave'
prob2 = '/sys/bus/w1/devices/28-000006282488/w1_slave'
prob3 = '/sys/bus/w1/devices/28-000006285167/w1_slave'


def temp_raw(sensor):
    f = open(sensor,'r')
    lines = f.readlines()
    f.close()
    return lines



def read_temp(sensor):
    lines = temp_raw(sensor)
    while lines[0].strip()[-3:] != 'YES':
       # time.sleep(0.2)
        lines = temp_raw(sensor)

    temp_output = lines[1].find('t=')
    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string)/ 1000.0
        temp_f = temp_c*9.0 /5.0 + 32.0
        return temp_f

def sent_temp():
    temp = [read_temp(prob1),read_temp(prob2),read_temp(prob3)]
    print temp
    return temp



sent_temp()

