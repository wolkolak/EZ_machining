#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Settings.check_on_start import check_it
check_it()
from PyQt5 import QtGui
import sys
from PyQt5.QtWidgets import QApplication
from Gui import interface

#sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    #sys.setswitchinterval(1000)
    #with open('Settings/settings.py')
    app = QApplication(sys.argv)
    #QApplication.setStyle(QStyleFactory.create('windows'))
    ex = interface.MyMainWindow()
    import ctypes

    myappid = 'mycompany.myproduct.subproduct.version'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    #title = QLabel('Title')

    ex.show()#иначе сохранять состояние окна нельзя будет
    sys.exit(app.exec_())
