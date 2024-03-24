from PyQt5.QtWidgets import QDialog, QGridLayout, QFrame, QLabel,  QSlider, QScrollBar, QDial, QPushButton, QLineEdit
from PyQt5 import QtCore
from Gui.little_gui_classes import validate_text_digit



class JOG_dialog(QDialog):
    def __init__(self, main_inteface, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        print('Creating JOG dialog')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_interface = main_inteface
        self.scene0 = self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(550, 450)
        self.setWindowTitle('JOG dialog')
        self.XYZABC_list = []#[JOGSmallClass(self, None, 'X'), JOGSmallClass(self, None, 'Y'), ]

        for i, k in zip(range(0, 6), [*'XYZABC']):
            self.XYZABC_list.append(JOGSmallClass(self, k))
            grid.addWidget(self.XYZABC_list[i], i, 0)


class JOGSmallClass(QFrame):
    def __init__(self, father, letter,  *args, **kwargs):#todo нужна ли ax?????
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(400, 70)
        self.dialog_interface = father
        self.letter = letter
        self.setStyleSheet('background-color: rgb(100, 200, 200); border-style: outset; font-size: 20px;')
        self.ax_label = QLabel()
        self.ax_label.setText(letter)
        grid.addWidget(self.ax_label, 0, 0, 1, 1,  alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)#,

        self.minus = QPushButton('-')
        self.minus.setStyleSheet('background-color: rgb(220, 220, 220); border-style: outset; ')
        self.minus.clicked.connect(lambda: self.move_slide_ax(-1))
        self.minus.setAutoRepeat(True)
        self.minus.setAutoRepeatInterval(500)
        self.minus.setAutoRepeatDelay(1000)
        #self.minus.toggled.connect(lambda: self.move_slide_ax(-1))
        self.minus.setFixedSize(100, 50)
        grid.addWidget(self.minus, 0, 1, 1, 1)

        self.step = QLineEdit('10.')
        validate_text_digit(self)
        self.step.setValidator(self.onlyInt)
        self.step.setStyleSheet('background-color: rgb(255, 255, 255); border-style: outset;')
        self.step.setFixedSize(100, 50)
        grid.addWidget(self.step, 0, 2, 1, 1)

        self.plus = QPushButton('+')
        self.plus.clicked.connect(lambda: self.move_slide_ax(1))
        self.plus.setAutoRepeat(True)
        self.plus.setAutoRepeatInterval(500)
        self.plus.setAutoRepeatDelay(1000)
        self.plus.setStyleSheet('background-color: rgb(220, 220, 220); border-style: outset;')
        self.plus.setFixedSize(100, 50)
        grid.addWidget(self.plus, 0, 3, 1, 1)

    def move_slide_ax(self, sign):
        machine_draw = self.dialog_interface.scene0.machine_draw_list
        after_draw = self.dialog_interface.scene0.after_draw_return_list
        print('1machine_draw = ', machine_draw)
        print('1after_draw = ', after_draw)
        sign *= -1# because storage inversed

        CurrentAXDict = self.dialog_interface.scene0.CurrentAXDict
        list_base = self.dialog_interface.scene0.BASE_XYZABC
        #Заменить list_base
        step = float(self.step.text()) * sign * (-1)
        CurrentAXDict[self.letter][0][CurrentAXDict[self.letter][1]] += step
        my_str = "XYZABC"
        i = my_str.index(self.letter)
        if i < 3:
            meters = 'mm'
        else:
            meters = 'grad'

        print('Axis {}: {} {}'.format(self.letter, CurrentAXDict[self.letter][0][CurrentAXDict[self.letter][1]] - list_base[i], meters))
        #self.machine_draw_list = []
        #self.after_draw_return_list = []

        print('2machine_draw = ', machine_draw)
        print('2after_draw = ', after_draw)
