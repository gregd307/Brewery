#!/usr/bin/env python
import sys
import os
#initalizes one wire sensor and gpio 18
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
os.system('sh -c "echo 18 > /sys/class/gpio/export"')

from PyQt4.QtGui import *
from Brew_control import Window





if __name__ == "__main__":







 app = QApplication(sys.argv)
 window = Window()
 #splash screen
 splash_pix = QPixmap('splash1.png')
 splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
 splash.setMask(splash_pix.mask())
 splash.show()
 app.processEvents()

 window.show()
 app.processEvents()
 sys.exit(app.exec_())
