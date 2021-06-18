from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PyQt5 import QtGui
from PyQt5.QtGui import QResizeEvent
from Settings.settings import *
import numpy as np

def d3_interface(self):

    grid = QGridLayout(self)

    # grid.setRowStretch(0, 20)
    # grid.setColumnStretch(0, 30)
    self.setLayout(grid)
    self.a = QPushButton('Turn View')
    self.a.clicked.connect(self.turn_to_turn_vew)
    self.a.setFixedWidth(60)
    self.a.setFixedHeight(30)
    grid.addWidget(self.a, 0, 0, Qt.AlignTop | Qt.AlignLeft)
