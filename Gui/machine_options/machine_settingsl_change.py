from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QFrame, QLabel, \
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTabWidget, QHBoxLayout, QCheckBox, QComboBox, QScrollArea, QPlainTextEdit
from os import walk
import importlib
from PyQt5 import QtCore, QtGui, Qt
from Settings.change_setting import change_file_vars


class AxisOffsetFrame(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QGridLayout()
        #self.grid.setRowStretch(3, 1)
        #self.grid.set
        #self.grid.setColumnStretch()
        #style =
        self.setLayout(self.grid)
        self.machine_tab = father
        self.setStyleSheet('QCheckBox::indicator:unchecked {background-color : white;})')
        self.__X = LabelPlusText('X', 'X offset:', father)
        self.__Y = LabelPlusText('Y', 'Y offset:', father)
        self.__Z = LabelPlusText('Z', 'Z offset:', father)
        if self.machine_tab.dialog.main_interface.centre.note.currentIndex() == -1:
            m = self.machine_tab.dialog.main_interface.centre.note.default_machine_item
        else:
            m = self.machine_tab.dialog.main_interface.centre.note.currentWidget().current_machine
        self.__X.text_field.setText(str(m.offset_pointXYZ[0]))#todo ХЗ что это вообще
        self.__Y.text_field.setText(str(m.offset_pointXYZ[1]))
        self.__Z.text_field.setText(str(m.offset_pointXYZ[2]))

        self.make_button(self.grid)


        self.grid.addWidget(self.__X, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.__Y, 1, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)
        self.grid.addWidget(self.__Z, 2, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)

        #self.current_machine = QLabel('super machine')
        #self.my_add_widget(self.current_machine, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 360, 80, 0, 1, 1, 2)

        self.__X_box = QCheckBox('X usable')
        self.__X_box.setChecked(m.axles_DICT['X'])
        self.my_add_widget(self.__X_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 0, 1)
        self.__Y_box = QCheckBox('Y usable')
        self.__Y_box.setChecked(m.axles_DICT['Y'])
        self.my_add_widget(self.__Y_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 1, 1)
        self.__Z_box = QCheckBox('Z usable')
        self.__Z_box.setChecked(m.axles_DICT['Z'])#todo Nope. не факт. может, наоборот снять надо. Нужно импортировать из файла AAAAAAAAAAAAAAAAAAA!!!!!!!!!!!!
        self.my_add_widget(self.__Z_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 2, 1)

        self.__A_box = QCheckBox('A usable')
        self.__A_box.setChecked(m.axles_DICT['A'])
        self.my_add_widget(self.__A_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 0, 2)
        self.__B_box = QCheckBox('B usable')
        self.__B_box.setChecked(m.axles_DICT['B'])
        self.my_add_widget(self.__B_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 1, 2)
        self.__C_box = QCheckBox('C usable')
        self.my_add_widget(self.__C_box, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 160, 40, 2, 2)
        self.__C_box.setChecked(m.axles_DICT['C'])



    def my_add_widget(self, label, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        print('my_add_widget start')
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignCenter)
        print('my_add_widget end')

    def make_button(self, grid):
        self.accept_axles_chage_point = QPushButton('Accept')
        self.accept_axles_chage_point.setFixedSize(100, 40)
        self.accept_axles_chage_point.setStyleSheet(' background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;')
        self.accept_axles_chage_point.clicked.connect(self.save_axles_change_point)
        grid.addWidget(self.accept_axles_chage_point, 4, 2, 1, 1, alignment=QtCore.Qt.AlignRight)

    def save_axles_change_point(self):
        a1 = "axles_DICT"
        a2 = "{{'X': {}, 'Y': {}, 'Z': {}, 'A': {}, 'B': {}, 'C': {}}}".format(
            self.__X_box.isChecked(), self.__Y_box.isChecked(), self.__Z_box.isChecked(),
            self.__A_box.isChecked(), self.__B_box.isChecked(), self.__C_box.isChecked(),
        )
        b1 = "offset_pointXYZ"#todo ЭТО НА ПОМОЙКУ
        b2 = "[{}, {}, {}, 0., 0., 0]".format(self.__X.text_field.text(), self.__Y.text_field.text(), self.__Z.text_field.text())

        #c1 = "current_g54_g59"
        #c2 = 'G54'
        #print(' Ищем: ', self.)

        names = [[a1, a2], [b1, b2]]
        no_tab_opened = True if self.machine_tab.dialog.main_interface.centre.note.currentIndex() == -1 else False
        if no_tab_opened:
            m = self.machine_tab.dialog.main_interface.centre.note.default_machine_item
        else:
            m = self.machine_tab.dialog.main_interface.centre.note.currentWidget().current_machine
        change_file_vars(m.machine_settings_open, names)
        #if not no_tab_opened:
        #    self.machine_tab.dialog.main_interface.centre.note.set_machine_in_DOC()
        #self.machine_tab.dialog.main_interface.centre.note.after_setting_machine()
        #self.machine_tab.dialog.scene0.machine_model_parts()
        self.machine_tab.dialog.bigcustom.update_scene_machine()

class LabelPlusText(QFrame):
    def __init__(self, ax, lbl_text, machine_tab, *args, **kwargs):
        super().__init__(*args, **kwargs)
        validate_text_digit(self)
        grid = QGridLayout()
        self.machine_tab = machine_tab
        self.setLayout(grid)
        self.setStyleSheet('background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;')
        #self.setStyleSheet('background-color: rgb(55, 55, 255); border-style: outset; spacing: 3px;')
        self.setFixedSize(160, 40)
        self.ax = ax
        self.lbl_text = lbl_text
        self.lbl_ = QLabel(lbl_text)
        self.text_field = QLineEdit()
        self.text_field.setValidator(self.onlyInt)
        #self.text_field.setText(self.)
        #self.ax_field.setText(self.machine_tab.dialog.main_interface.    )
        #self.text_field.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.text_field.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.lbl_, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.text_field, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

def validate_text_digit(self):
    self.onlyInt = QtGui.QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)