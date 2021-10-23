from PyQt5.QtWidgets import QDialog, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
import re
from left_zone.D3_interface import restore_zero_position_shell
import math


class draft_dialog(QDialog):
    def __init__(self, main_inteface, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.main_inteface = main_inteface
        self.scene0 = self.main_inteface.centre.left.left_tab.b.openGL
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(518, 318)
        self.LeftTop = toolsFrameDisplace(self)
        self.setWindowTitle('Move, Rotate or Scale your draft')
        self.LeftBottom = toolsFrameRotate(self)
        self.RightTop = ToolsFrameAutoLineMeasure(self)
        self.RightBottom = toolsFrameScale(self)
        grid.addWidget(self.LeftTop, 0, 0)
        grid.addWidget(self.RightTop, 0, 1)
        grid.addWidget(self.LeftBottom, 1, 0)
        grid.addWidget(self.RightBottom, 1, 1)

    def done(self, a0: int) -> None:
        print('happining')
        self.scene0.refresh()
        QDialog.done(self, a0)

class toolsFrameDisplace(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setFixedSize(250, 150)
        validate_text_digit(self)
        self.setStyleSheet('background-color: rgb(200, 200, 200); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.setRowMinimumHeight(3, 70)
        #self.grid.setColumnMinimumWidth()
        self.displace_label = QLabel()
        self.addQlabel(self.displace_label, 'Displace', 'background-color: rgb(100, 255, 255)', 60, 25, 0, 0)
        self.horizontal_label = QLabel()
        self.addQlabel(self.horizontal_label, 'Horiz', 'background-color: rgb(100, 255, 255)', 50, 25, 1, 0)
        self.vertical_label = QLabel()
        self.addQlabel(self.vertical_label, 'Vert', 'background-color: rgb(100, 255, 255)', 50, 25, 2, 0)
        self.horizontal_field = QLineEdit()
        self.horizontal_field.setValidator(self.onlyInt)
        self.addQlabel(self.horizontal_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 1, 1)
        self.vertical_field = QLineEdit()
        self.vertical_field.setValidator(self.onlyInt)
        self.addQlabel(self.vertical_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 2, 1)
        self.choose_draft_zero = QPushButton()
        self.choose_draft_zero.setToolTip('Followed by RIGHT CLICK on the draft')
        self.choose_draft_zero.clicked.connect(self.choose_draft_zero_point)
        #self.draft_cursor = QPixmap('icons/choose_point.png')
        self.choose_draft_zero.setIcon(QIcon("icons/choose_point.png"))
        self.choose_draft_zero.setIconSize(QtCore.QSize(100, 100))
        self.addQlabel(self.choose_draft_zero, '', 'background-color: rgb(200, 200, 200)', 100, 100, 0, 3, 1, 3)

        self.OK_draft_zero = QPushButton()
        self.OK_draft_zero.clicked.connect(self.displace_draft)
        self.vertical_field.returnPressed.connect(self.displace_draft)
        self.horizontal_field.returnPressed.connect(self.displace_draft)
        self.addQlabel(self.OK_draft_zero, 'OK', 'background-color: rgb(255, 255, 255); border-radius: 10px', 50, 35, 0, 1, 1, 1)

    def choose_draft_zero_point(self):
        print('zero point')
        self.father.scene0.behavior_mode = 'draft_point'
        print('main_inteface = ', self.father.main_inteface.width())
        self.father.move(self.father.main_inteface.width() + self.father.main_inteface.pos().x() - self.father.width(),
                         self.father.main_inteface.height() + self.father.main_inteface.pos().y() - self.father.height())
        self.father.scene0.render_text_preparation('Choose new ZERO \n point on the draft ', text_size=200, name_png='ZERO draft dot', k=0.35)
        self.father.scene0.setCursor(QtGui.QCursor(Qt.CrossCursor))


    def displace_draft(self):
        delta_horiz = re.sub(',', '.', self.horizontal_field.text())
        delta_vert = re.sub(',', '.', self.vertical_field.text())
        if delta_horiz == '':
            delta_horiz = '0'
        if delta_vert == '':
            delta_vert = '0'
        k = self.father.scene0.draft_scale
        #angle = -(self.father.scene0.alpha * 2 * math.pi / 360)
        delta_horiz = float(delta_horiz)
        delta_vert = float(delta_vert)

        _horiz = delta_horiz #* math.cos(angle) - delta_vert * math.sin(angle)
        _vert = delta_vert #* math.cos(angle) + delta_horiz * math.sin(angle)
        #display_h_mm
        self.father.scene0.draft_zero_horiz = self.father.scene0.draft_zero_horiz + _horiz * k/787#/self.father.scene0.h
        self.father.scene0.draft_zero_vert = self.father.scene0.draft_zero_vert + _vert * k/787#/self.father.scene0.h
        print('self.father.scene0.h === ', self.father.scene0.h)

    def addQlabel(self, label, text, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        label.setText(text)
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        #label.setAlignment(Qt.AlignLeft)

class toolsFrameRotate(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setFixedSize(250, 150)
        validate_text_digit(self)
        self.setStyleSheet(
            'background-color: rgb(200, 200, 200); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.rotate_label = QLabel()
        self.addQlabel(self.rotate_label, 'Rotate', 'background-color: rgb(100, 255, 255)', 60, 25, 0, 0)
        self.grad_field = QLineEdit()
        self.grad_field.setValidator(self.onlyInt)
        self.addQlabel(self.grad_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 1, 0)
        self.minute_field = QLineEdit()
        self.minute_field.setValidator(self.onlyInt)
        self.addQlabel(self.minute_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 2, 0)
        self.grad_label = QLabel()
        self.addQlabel(self.grad_label, 'GRAD', 'background-color: rgb(100, 255, 255)', 50, 25, 1, 1)
        self.min_label = QLabel()
        self.addQlabel(self.min_label, 'MIN', 'background-color: rgb(100, 255, 255)', 50, 25, 2, 1)
        self.OK_rotate_draft = QPushButton()
        self.OK_rotate_draft.clicked.connect(lambda: self.absolute_rotate(self.father.scene0))
        self.grad_field.returnPressed.connect(lambda: self.absolute_rotate(self.father.scene0))
        self.minute_field.returnPressed.connect(lambda: self.absolute_rotate(self.father.scene0))
        self.addQlabel(self.OK_rotate_draft, 'OK', 'background-color: rgb(255, 255, 255); border-radius: 10px', 50, 35, 3, 0, 1, 1)
        self.angle_label = QLabel()
        ang_im = QPixmap('icons/angle_grad.png')
        self.angle_label.setPixmap(ang_im)
        self.addQlabel(self.angle_label, '', 'background-color: rgb(100, 255, 255)', 120, 120, 0, 2, 1, 3)

    #@restore_zero_position_shell

    def absolute_rotate(self, scene):

        print('1: cam_hori = {}, cam_vert = {}'.format(scene.cam_horizontal, scene.cam_height))
        print('1: draft_horizont = {}, draft_vert = {}'.format(scene.draft_zero_horiz, scene.draft_zero_vert))

        new_rotate_g = self.grad_field.text()
        new_rotate_m = self.minute_field.text()
        if new_rotate_g == '':
            new_rotate_g = '0'
        if new_rotate_m == '':
            new_rotate_m = '0'
        new_rotate_g = float(re.sub(',', '.', new_rotate_g))
        new_rotate_m = float(re.sub(',', '.', new_rotate_m))
        new_rotate = new_rotate_g + new_rotate_m/60
        print('scene.draft_zero_horiz = ', scene.draft_zero_horiz)

        old_alpha = (scene.alpha * 2 * math.pi / 360)
        #
        delta = -(new_rotate - scene.alpha) * 2 * math.pi / 360

        #куда в кривой СК проецируется XYZ0
        h = scene.cam_horizontal * math.cos(-old_alpha) - scene.cam_height * math.sin(-old_alpha)
        v = scene.cam_height * math.cos(-old_alpha) + scene.cam_horizontal * math.sin(-old_alpha)

        NEW_Centre_x = scene.draft_zero_horiz * math.cos(delta) - scene.draft_zero_vert * math.sin(delta)######
        NEW_Centre_y = scene.draft_zero_vert * math.cos(delta) + scene.draft_zero_horiz * math.sin(delta)

        scene.alpha = new_rotate#                                         ПОВОРОТ

        Sc_X_old = h - scene.draft_zero_horiz#Смотрит в точку предыдущего ЧПУ СК
        Sc_Y_old= v - scene.draft_zero_vert

        SC_X_new = Sc_X_old * math.cos(delta) - Sc_Y_old * math.sin(delta)#Смотрит в точку нового ЧПУ СК
        SC_Y_new = Sc_Y_old * math.cos(delta) + Sc_X_old * math.sin(delta)

        vector_X = Sc_X_old - SC_X_new
        vector_Y = Sc_Y_old - SC_Y_new

        scene.draft_zero_horiz = NEW_Centre_x - vector_X
        scene.draft_zero_vert = NEW_Centre_y - vector_Y

    def addQlabel(self, label, text, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        label.setText(text)
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

class ToolsFrameAutoLineMeasure(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setFixedSize(250, 150)
        #validate_text_digit(self)
        self.setStyleSheet('background-color: rgb(200, 200, 200); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.auto_label = QLabel()
        self.addQlabel(self.auto_label, 'Auto', 'background-color: rgb(100, 255, 255)', 80, 40, 0, 0)

        self.choose_distance_button = QPushButton()
        self.choose_distance_button.setToolTip('Followed by 2 RIGHT CLICK on the draft\n You should know distance between')
        self.addQlabel(self.choose_distance_button, 'Choose distance\n<----------------->', 'background-color: rgb(100, 255, 255)', 120, 50, 1, 0)
        self.choose_distance_button.clicked.connect(self.draft_size_from_distance)

    def draft_size_from_distance(self):
        print('draft_size_from_distance')
        self.father.scene0.behavior_mode = 'choose distance'
        self.father.move(self.father.main_inteface.width() + self.father.main_inteface.pos().x() - self.father.width(),
                         self.father.main_inteface.height() + self.father.main_inteface.pos().y() - self.father.height())
        self.father.scene0.setCursor(QtGui.QCursor(Qt.CrossCursor))
        self.father.scene0.render_text_preparation("RClick to choose \n 1'st coordinat dot ", text_size=200, name_png='1st draft dot', k=0.35)

    def addQlabel(self, label, text, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        label.setText(text)
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)


class toolsFrameScale(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setFixedSize(250, 150)

        validate_text_digit(self)

        self.setStyleSheet(
            'background-color: rgb(200, 200, 200); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;')
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.scale_label = QLabel()
        self.addQlabel(self.scale_label, 'Scale', 'background-color: rgb(100, 255, 255)', 60, 25, 0, 0)
        self.absolute_label = QLabel()
        self.addQlabel(self.absolute_label, 'Absolute', 'background-color: rgb(100, 255, 255)', 65, 25, 1, 0)
        self.relative_label = QLabel()
        self.addQlabel(self.relative_label, 'Relative', 'background-color: rgb(100, 255, 255)', 65, 25, 1, 1)
        self.absolute_field = QLineEdit()
        self.absolute_field.setValidator(self.onlyInt)

        self.addQlabel(self.absolute_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 2, 0)

        self.addQlabel(self.absolute_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 2, 0)
        self.relative_field = QLineEdit()
        self.relative_field.setValidator(self.onlyInt)
        self.addQlabel(self.relative_field, '', 'background-color: rgb(255, 255, 255); border-style: outset; '
                                                  'border-width: 2px; border-color: black;', 50, 25, 2, 1)
        self.OK_absolute_button = QPushButton()
        self.OK_absolute_button.clicked.connect(self.absolute_scaling)
        self.addQlabel(self.OK_absolute_button, 'OK', 'background-color: rgb(255, 255, 255); border-radius: 10px', 50, 35, 3, 0, 1, 1)

        self.OK_relative_button = QPushButton()
        self.OK_relative_button.clicked.connect(lambda: self.relative_scaling(self.father.scene0))
        self.absolute_field.returnPressed.connect(self.absolute_scaling)
        self.relative_field.returnPressed.connect(lambda: self.relative_scaling(self.father.scene0))
        self.addQlabel(self.OK_relative_button, 'OK', 'background-color: rgb(255, 255, 255); border-radius: 10px', 50, 35, 3, 1, 1, 1)

    def absolute_scaling(self):
        new_scale = self.absolute_field.text()
        if new_scale == '':
            return
        #прицепил декоратор
        self.exactly_absolut_scaling(self.father.scene0, new_scale)

    @restore_zero_position_shell
    def exactly_absolut_scaling(self, scene, new_scale):
       scene.draft_scale = scene.k_rapprochement * scene.scaling_draft_prime * float(new_scale)

    @restore_zero_position_shell
    def relative_scaling(self, scene):
        new_scale = self.relative_field.text()
        new_scale = re.sub(',', '.', new_scale)
        scene.draft_scale = scene.draft_scale * float(new_scale)

    def addQlabel(self, label, text, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        label.setText(text)
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

def validate_text_digit(self):
    self.onlyInt = QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)
