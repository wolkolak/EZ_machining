from PyQt5.QtWidgets import QSplitter, QTabWidget, QHBoxLayout,  \
    QFrame, QTabBar,  QMessageBox, QPlainTextEdit,  QWidget, QGridLayout, QGraphicsScene, QPushButton
from PyQt5.QtCore import Qt, QRect, QSize
import redactor
import OpenGL
from PyQt5.QtOpenGL import QGLWidget

from settings import *
import numpy as np

class Window3D(QGLWidget):
    """Визуализацию ты можешь разместить где то тут.
    Класс QGLWidget это 3д класс для работы с OpenGL графонием.
    Необходим ли он нам и насколько он похож на то, про что ты читал, я пока не знаю.
    https://doc.qt.io/qt-5/qglwidget.html
    """
    def __init__(self, gcod, gmodal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('start opengl')
        self.setMinimumSize(100, 100)
        self.gcod = gcod
        self.gmodal = gmodal


class SomeInTab(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        """Используй пока что этот numpy(xyzcbar) и словарь с модальными ключами"""
        self.g_cod_pool2 = np.array([[200, 0, 3, 0, 0, 0, 0],
                                   [160, 0, -5, 0, 0, 0, 0],
                                   [163, 0, 3, 0, 0, 0, 0],
                                   [155, 0, -5, 0, 0, 0, 0],
                                   [166, 0, 0, 0, 0, 0, 0],
                                   [100, 0, 200, 0, 0, 0, 0]],
                                   float)
        #modal coomnds
        self.g_modal2 = {'G0': [0, 5, 8], 'G1': [3, 6], 'G2': [], 'G3': []}

        self.openGL = Window3D(gcod=self.g_cod_pool2, gmodal=self.g_modal2)
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.openGL, 0, 0)
        self.frame = MyFrame()
        grid.addWidget(self.frame, 1, 0)

class MyFrame(QFrame):
    """тут пример кнопок"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMaximumHeight(100)
        grid = QGridLayout()
        self.setLayout(grid)
        self.a = QPushButton('кнопка 1')
        self.a.clicked.connect(self.do_something)

        self.b = QPushButton('кнопка 2')
        grid.addWidget(self.a, 0, 0)
        grid.addWidget(self.b, 0, 1)

    def do_something(self):
        print('ololo')



class leftTab(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        b = SomeInTab()
        self.addTab(b, 'visual')




class left1(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(color1))

        grid = QGridLayout()
        self.setLayout(grid)
        self.left_tab = leftTab()
        grid.addWidget(self.left_tab, 0, 0)

