#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QLabel, QStyleFactory

import interface

if __name__ == '__main__':

    app = QApplication(sys.argv)
    #QApplication.setStyle(QStyleFactory.create('windows'))
    ex = interface.MyMainWindow()

    title = QLabel('Title')

    ex.show()#иначе сохранять состояние окна нельзя будет
    sys.exit(app.exec_())
