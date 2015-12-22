#!/usr/bin/env python
import sys
import os
os.system('sudo modprobe w1-gpio')
os.system('sudo modprobe w1-therm')
os.system('sh -c "echo 18 > /sys/class/gpio/export"')

from PyQt4.QtGui import *
from window import Window





if __name__ == "__main__":







 app = QApplication(sys.argv)
 window = Window()
 #ui = Ui_MainWindow()
 #ui.setupUi(window)

 window.show()
 sys.exit(app.exec_())
