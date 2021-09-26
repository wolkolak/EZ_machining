from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget
from PyQt5.QtGui import QPixmap

from Settings.settings import *
import numpy as np
from left_zone.Scene import Window3D
import sys

class SomeInTab(QFrame):
    def __init__(self, left_tab, np_arr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_tab = left_tab
        self.np_arr = np_arr
        """Используй пока что этот numpy(xyzcbar) и словарь с модальными ключами"""

        #modal coomnds
        self.g_modal2 = {'G0': [0, 5, 8], 'G1': [3, 6], 'G2': [], 'G3': []}

        self.openGL = Window3D(frame=self, gcod=self.np_arr, gmodal=self.g_modal2)
        #print('np_arr size ', self.np_arr.shape)
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.openGL, 0, 0)
        self.frame = MyFrame()
        grid.addWidget(self.frame, 1, 0)

        #imagem = QPixmap('373ун34.0402.128_14400696_2735.tif')#todo
        #img_tiff_map = imagem.scaled(500, 500)
        #self.setPixmap(img_tiff_map)



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
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        self.a = NumpyPrint(self)
        self.addTab(self.a, 'whole array')
        self.b = SomeInTab(left_tab=self, np_arr=self.parent.visible_np_left)
        self.addTab(self.b, 'visual')
        self.setCurrentIndex(1)

class NumpyPrint(QPlainTextEdit):
    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base = base
        self.setFont(font1)

        # нам нужно постучаться в конкретную вкладку

        #self.setPlainText(np.array2string(self.test_pool2))






class left1(QWidget):
    def __init__(self, central_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.central_widget = central_widget
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(color1))
        #axis
        self.visible_np_empty = np.zeros((1, axises), float)
        self.visible_np_left = self.visible_np_empty
        #self.visible_np[1][:] = 1.
        grid = QGridLayout()
        self.setLayout(grid)
        self.left_tab = leftTab(self)
        grid.addWidget(self.left_tab, 0, 0)



        #print('shape of visible_np = ', self.visible_np.shape)
        #print('np.array2string(visible_np):', np.array2string(visible_np))

    def update_visible_np_left(self):

        #np.set_printoptions( formatter={'float': lambda x: format(x, ' 2f')}, floatmode='fixed')

        if self.central_widget.note.currentIndex() != -1:
            self.visible_np_left = self.central_widget.note.currentWidget().np_box.visible_np.copy()
        else:
            self.visible_np_left = self.visible_np_empty
        #self.left_tab.a.setPlainText(np.array2string(self.visible_np_left))
        #self.left_tab.b.openGL.gcod = self.visible_np_left
        self.reset_np_array_in_left_field(self.visible_np_left)

    def reset_np_array_in_left_field(self, v):
        mapper = lambda x: np.format_float_positional(x, precision=2)
        np.set_printoptions(
             linewidth=350, floatmode='fixed', threshold=sys.maxsize,
            suppress=False, formatter={'float': mapper}
        )
        self.left_tab.a.setPlainText(np.array2string(v))
        self.left_tab.b.openGL.gcod = v
        print('self.left_tab.b.openGL.gcod.shape = ', self.left_tab.b.openGL.gcod.shape)
