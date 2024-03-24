from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QLabel, QHBoxLayout
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
        #self.frame = MyFrame()
        #grid.addWidget(self.frame, 1, 0)

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

#class ShortcutToProcessorAndMachine(QFrame):
#    def __init__(self, parent, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        #self.setFixedSize(100, 100)
#        self.setFixedHeight(50)
#        self.setStyleSheet("background-color: {}".format(color2))


class leftTab(QTabWidget):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = parent
        #self.processor_at_corner = ShortcutToProcessorAndMachine(self)
        #little_layout = QHBoxLayout()
        #self.processor_at_corner.setLayout(little_layout)
        #fff = QLabel('AAAA')
        #little_layout.addWidget(fff)
        #self.setCornerWidget(self.processor_at_corner)
        self.whole_array = NumpyPrint(self)
        self.addTab(self.whole_array, 'whole array')
        self.parent_of_3d_widget = SomeInTab(left_tab=self, np_arr=self.parent.visible_np_left)
        self.addTab(self.parent_of_3d_widget, 'visual')
        self.visual_rot = NumpyPrint(self)
        self.addTab(self.visual_rot, 'ax rotated array')
        self.setCurrentIndex(1)
        #self.a.setStyleSheet('background-color:green')

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
        self.visible_np_left = self.visible_np_empty#todo переключение при смене вкладки сделать
        #self.visible_rot_np_empty = np.zeros((1, 3), float)
        #self.visible_rot = self.visible_rot_np_empty
        #self.visible_np[1][:] = 1.
        grid = QGridLayout()
        self.setLayout(grid)
        self.left_tab = leftTab(self)
        grid.addWidget(self.left_tab, 0, 0)



        #print('shape of visible_np = ', self.visible_np.shape)
        #print('np.array2string(visible_np):', np.array2string(visible_np))

    def update_visible_np_left(self):
        print('update_visible_np_left ')
        #np.set_printoptions( formatter={'float': lambda x: format(x, ' 2f')}, floatmode='fixed')
        if self.central_widget.note.currentIndex() != -1:
            np_box = self.central_widget.note.currentWidget().np_box
            self.visible_np_left = np_box.visible_np.copy()#main_g_cod_pool.copy() now fine
            main_g_cod_pool = np_box.main_g_cod_pool
            #np_while = self.central_widget.note.currentWidget().np_box.SHIFTcontainer.np_for_vars.copy()
            #dict_while = self.central_widget.note.currentWidget().np_box.SHIFTcontainer.base_dict.copy()

            vars_container_avatar = np_box.SHIFTcontainer#.my_copy()
            XYZvars_avatar = np_box.XYZvars_container
            frame_box = np_box.frame_address_in_visible_pool
            GM_avatar = np_box.GM_modal_container
        else:
            self.visible_np_left = self.visible_np_empty
            XYZvars_avatar = {}
            GM_avatar = {}
            line_numbers = 1
            #np_while = np.zeros((line_numbers, 4), int)
            #dict_while = {0: [None, None, None, None]}
            vars_container_avatar = np.zeros((line_numbers, 4), int)
            frame_box = np.zeros((1, 2), int)
            main_g_cod_pool = []
        #vars_container_avatar = [np_while, dict_while]
        vars_dict_end = str(np_box.current_vars_dict)
        self.reset_np_array_in_left_field(self.visible_np_left, frame_box, main_g_cod_pool, vars_container_avatar, vars_dict_end, XYZvars_avatar, GM_avatar)

    def reset_np_array_in_left_field(self, v, frame_box, main_g_cod_pool, vars_container_avatar, vars_dict_end, XYZvars_avatar, GM_avatar):#in self.np_box.current_vars_dict:#
        """
        here we explain how to display numpy arrays
        """
        mapper = lambda x: np.format_float_positional(x, precision=2)
        np.set_printoptions(
             linewidth=350, floatmode='fixed', threshold=sys.maxsize,
            suppress=False, formatter={'float': mapper}
        )

        self.left_tab.whole_array.setPlainText(np.array2string(v))
        #self.left_tab.visual_rot.setPlainText(np.array2string(vars_container_avatar[0]) )#+ vars_container_avatar[0]


        self.left_tab.visual_rot.setPlainText(vars_container_avatar.__str__() + '\n\n\n\n' + vars_dict_end + '\n\n\n\n' + XYZvars_avatar.__str__() + GM_avatar.__str__() + 'frame_box:\n' + str(frame_box) + '\n' + str(main_g_cod_pool))
        #print('frame_box = ', frame_box)
        #self.left_tab.visual_rot.setPlainText(np.array2string(self.central_widget.note.currentWidget().np_box.visible_np_rot))
        self.left_tab.parent_of_3d_widget.openGL.gcod = v
        self.left_tab.parent_of_3d_widget.openGL.frame_address_in_visible_pool = frame_box
        #print('self.left_tab.b.openGL.gcod.shape = ', self.left_tab.parent_of_3d_widget.openGL.gcod.shape)
        #print('Итоговый: ', self.left_tab.parent_of_3d_widget.openGL.gcod)
