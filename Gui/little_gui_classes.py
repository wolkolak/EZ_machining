from PyQt5.QtWidgets import QMessageBox
from Settings.settings import *


def simple_warning(title, text):
    warning = QMessageBox()
    warning.setFont(QFont("Helvetica [Cronyx]", 12))
    warning.setWindowTitle(title)
    warning.setText(text)
    warning.exec()