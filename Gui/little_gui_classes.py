from PyQt5.QtWidgets import QMessageBox, QDialog
from Settings.settings import *
from PyQt5.QtGui import QDoubleValidator
from PyQt5 import QtCore, QtGui

def simple_warning(title, text):
    warning = QMessageBox()
    warning.setFont(QFont("Helvetica [Cronyx]", 12))
    warning.setWindowTitle(title)
    warning.setText(text)
    warning.exec()

def validate_text_digit(self):
    self.onlyInt = QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)




