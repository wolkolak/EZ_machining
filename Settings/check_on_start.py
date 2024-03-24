import sys
from PyQt5.QtWidgets import QMessageBox, QDialog, QApplication
from PyQt5.QtGui import QFont

def check_it():
    try:
        print('checking 0%')
        from Settings import settings
        print('checking 100%')
    except:
        print('Failed')
        app = QApplication(sys.argv)
        warning = QMessageBox()
        warning.setFont(QFont("Helvetica [Cronyx]", 12))
        title = 'Oups!'
        text = "Problem with Settings/settings file.\n" \
               "Consider checking it's content\n" \
               "and save changes through python editor.\n" \
               "Non-english letters need 'utf-8'.\n" \
               "settings.py should start with '# -*- coding: utf-8 -*-'"
        warning.setWindowTitle(title)
        warning.setText(text)
        warning.exec()
        quit()
        #q = simple_warning('Oups!', text)