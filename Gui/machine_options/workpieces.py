from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QFrame, QLabel, \
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTabWidget, QHBoxLayout, QCheckBox, QComboBox, QScrollArea, QPlainTextEdit
from os import walk
import importlib
from PyQt5 import QtCore, QtGui, Qt
from Settings.change_setting import change_file_vars


class Workpieces_frame(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.dialog = father
        self.workpieces_tab = TabWorkpieces(self.dialog)
        grid.addWidget(self.workpieces_tab, 0, 0)

class TabWorkpieces(QTabWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('background-color: rgb(200, 200, 200); font-size: 20px;')
        self.dialog = father
        G_Numbers = ['G5' + str(_n) for _n in range(4, 10)]
        print('G_Numbers ====== ', G_Numbers)
        [self.add_G_number(G_Number) for G_Number in G_Numbers]

    def add_G_number(self, G_Number):
        print('G_Number in add_G_number: ', G_Number)
        g54_g55 = G54_G55(self.dialog, G_Number)
        self.addTab(g54_g55, G_Number)

class G54_G55(QFrame):
    def __init__(self, father, Gnumber, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        validate_text_digit(self)
        self.Gnumber = Gnumber
        print('Gnumber in g54_g55 is ', Gnumber)
        self.dialog = father
        #self.setFixedWidth(150)
        self.dict_of_XYZABC = {'X': None, 'Y': None, 'Z': None,
                               'A': None, 'B': None, 'C': None}
        i = 0
        for letter in self.dict_of_XYZABC:#нужен какой то
            self.dict_of_XYZABC[letter] = G54SmallClass(self, Gnumber, letter)
            print('self.dict_of_XYZABC[] = ', self.dict_of_XYZABC['X'])
            self.my_add_widget(self.dict_of_XYZABC[letter], '', 150, 50, i, 0)#background-color: rgb(200, 200, 100);
            i = i + 1
        self.grid.setAlignment(QtCore.Qt.AlignLeft)
        self.accept_G549_coord = QPushButton('Accept')
        self.g549_default_tick = QCheckBox('Use from\nthe start')

        #if self.dialog.main_interface.centre.note.currentIndex() == -1:
        #    machine = self.dialog.main_interface.centre.note.default_machine_item
        #else:
        #    machine = self.dialog.main_interface.centre.note.currentWidget().current_machine

        self.rotate_type_warning = QLabel('Warning. It is Euler angle. \n 1 Around X\n 2 Around Y\n 3 Around Z\n Order has meaning')
        #todo from Core.Machine_behavior.G549_coords
        #todo g54_g59_AXIS_Delta[key_][0], g54_g59_AXIS_Delta[key_][1], g54_g59_AXIS_Delta[key_][2] = TR_ABC change

        self.grid.addWidget(self.rotate_type_warning, 2, 2, 2, 1, alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        if self.Gnumber == self.dialog.machine.current_g54_g59:
            self.g549_default_tick.setCheckState(True)
        self.my_add_widget(self.g549_default_tick,
                        'background-color: rgb(240, 240, 240); Text-align:Center', 100, 60, 3, 1)

        self.accept_G549_coord.clicked.connect(self.accepting_machine_g549_coordinates)
        self.my_add_widget(self.accept_G549_coord, 'background-color: rgb(240, 240, 240); Text-align:Center', 100, 40, 5, 1)
        if self.dialog.main_interface.centre.note.currentIndex() == -1:
            m = self.dialog.main_interface.centre.note.default_machine_item
        else:
            m = self.dialog.main_interface.centre.note.currentWidget().current_machine

        self.current_machine = QLabel(m.last_name)
        print('|||\\\\ self.current_machine.txt = ', self.current_machine.text())
        self.my_add_widget(self.current_machine, 'background-color: rgb(240, 240, 240); Text-align:Center; font-size: 20px;', 350, 55, 0, 2, 2, 1)
        self.current_machine.setAlignment(QtCore.Qt.AlignCenter)  #
        #print('pppassed thrugh')


    def accepting_machine_g549_coordinates(self):
        #todo это не то
        #1 определить по вкладке или по дефолту
        if self.dialog.main_interface.centre.note.currentIndex() == -1:
            #print('shit happens')
            m = self.dialog.main_interface.centre.note.default_machine_item
        else:
            print('then wtf')
            m = self.dialog.main_interface.centre.note.currentWidget().current_machine
            print('m = ', m)
        a = "'{}'".format(self.Gnumber)
        b = "{{'X': {}, 'Y': {}, 'Z': {}, 'A': {}, 'B': {}, 'C': {}}},".\
            format(str(self.dict_of_XYZABC['X'].ax_field.text()),
                   str(self.dict_of_XYZABC['Y'].ax_field.text()),
                   str(self.dict_of_XYZABC['Z'].ax_field.text()),
                   str(self.dict_of_XYZABC['A'].ax_field.text()),
                   str(self.dict_of_XYZABC['B'].ax_field.text()),
                   str(self.dict_of_XYZABC['C'].ax_field.text()))
        names = [[a, b]]
        change_file_vars(m.machine_settings_open, names, split=':')
        print('Записываем ', self.Gnumber)
        print('g549_default_tick = ', self.g549_default_tick.checkStateSet())
        if self.g549_default_tick.checkState():
            print('checkStateSet()')
            names = [['current_g54_g59', "'" + self.Gnumber + "'"]]
            change_file_vars(m.machine_settings_open, names)
        # переписать станку данные

        #считать это всё заново
        self.dialog.bigcustom.update_scene_machine()


        #добавить кнопку для переназначения СК базовой
        #self.dialog.scene0.machine_model_parts()
        #self.dialog.bigcustom.update_scene_machine_params()


    def my_add_widget(self, label, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        print('my_add_widget start')
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        print('my_add_widget end')


class G54SmallClass(QFrame):
    def __init__(self, father, G_Number54_59, letter,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('G_Number54_59 = ', G_Number54_59)
        grid = QGridLayout()
        self.setLayout(grid)
        self.g54_window = father
        self.ax_label = QLabel()


        self.ax_label.setText(letter)
        grid.addWidget(self.ax_label, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ax_field = QLineEdit()
        print('self.g54_window.dialog.main_inteface.centre.note.current = ', self.g54_window.dialog.main_interface.centre.note.currentIndex())
        if self.g54_window.dialog.main_interface.centre.note.currentIndex() == -1:
            value = str(self.g54_window.dialog.main_interface.centre.note.default_machine_item.g54_g59_AXIS[G_Number54_59][letter])
        else:
            value = str(self.g54_window.dialog.main_interface.centre.note.currentWidget().current_machine.g54_g59_AXIS[G_Number54_59][letter])

        self.ax_field.setText(value)#todo G55
        self.ax_field.setValidator(self.g54_window.onlyInt)
        self.ax_field.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.ax_field.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.ax_field, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

def validate_text_digit(self):
    self.onlyInt = QtGui.QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)