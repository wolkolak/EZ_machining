#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QApplication, QLabel

import copy
import interface


#todo from settings
default_settings = {'main_width': 1450, 'main_height': 900, 'font_txt': "nyaa", 'txt_width': 600}
settings = copy.deepcopy(default_settings)




if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = interface.MyMainWindow()

    title = QLabel('Title')

    ex.show()#иначе сохранять состояние окна нельзя будет
    sys.exit(app.exec_())
