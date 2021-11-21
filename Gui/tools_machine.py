from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QFrame, QLabel, \
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTabWidget


from PyQt5 import QtCore, QtGui

class AxisFrame(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = father



class G54SmallClass(QFrame):
    def __init__(self, father, G_Number54_59, letter,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('G_Number54_59 = ', G_Number54_59)
        #self.letter = letter
        grid = QGridLayout()
        self.setLayout(grid)
        self.g54_window = father
        self.ax_label = QLabel()
        self.ax_label.setText(letter)
        grid.addWidget(self.ax_label, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ax_field = QLineEdit()
        #self.ax_field.setText('0.0')

        #value = str(self.g54_window.dialog.scene0.current_machine.g54_g59_AXIS[G_Number54_59][letter])
        print('self.g54_window.dialog.main_inteface.centre.note.current = ', self.g54_window.dialog.main_interface.centre.note.currentIndex())
        if self.g54_window.dialog.main_interface.centre.note.currentIndex() == -1:

            value = str(self.g54_window.dialog.main_interface.default_reference.default_machine.g54_g59_AXIS[G_Number54_59][letter])

        else:
            value = str(self.g54_window.dialog.main_interface.centre.note.currentWidget().current_machine.g54_g59_AXIS[G_Number54_59][letter])
        print('value = ', value)

        self.ax_field.setText(value)#todo G55

        self.ax_field.setValidator(self.g54_window.onlyInt)
        self.ax_field.setStyleSheet('background-color: rgb(255, 255, 255); border-style: outset;')
        self.ax_field.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.ax_field, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


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
            self.my_add_widget(self.dict_of_XYZABC[letter], 'background-color: rgb(200, 200, 100); border-style: outset; ', 100, 50, i, 0)
            i = i + 1
        self.grid.setAlignment(QtCore.Qt.AlignLeft)
        self.accept = QPushButton('Accept')
        list_of_XYZABC = ['X', 'Y', 'Z', 'A', 'B', 'C']
        #G_list = [self.dict_of_XYZABC[key].ax_field.text() for key in list_of_XYZABC]

        #self.accept.clicked.connect(lambda: self.dialog.scene0.current_machine.save_line_in_machine_settings_py(self.Gnumber,
        #                                    [str(float(self.dict_of_XYZABC[key].ax_field.text())) for key in list_of_XYZABC]))
        if self.dialog.main_interface.centre.note.currentIndex() == -1:
            self.accept.clicked.connect(lambda: self.dialog.main_interface.default_reference.default_machine.save_line_in_machine_settings_py(self.Gnumber,
                                    [str(float(self.dict_of_XYZABC[key].ax_field.text())) for key in list_of_XYZABC]))
        else:
            self.accept.clicked.connect(lambda: self.dialog.main_interface.centre.note.currentWidget().current_machine.save_line_in_machine_settings_py(self.Gnumber,
                                    [str(float(self.dict_of_XYZABC[key].ax_field.text())) for key in list_of_XYZABC]))

        self.my_add_widget(self.accept, 'background-color: rgb(255, 255, 255); border-style: outset; Text-align:Center', 100, 50, 5, 1)



    def my_add_widget(self, label, backgroud_style, w, h, pos1, pos2, width=1, height=1):
        label.setStyleSheet(backgroud_style)
        label.setFixedSize(w, h)
        self.grid.addWidget(label, pos1, pos2, width, height, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

class TabWorkpieces(QTabWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(
            'background-color: rgb(200, 200, 200); border-style: outset;  font-size: 20px;')
        self.dialog = father
        G_Numbers = ['G5' + str(_n) for _n in range(4, 10)]
        print('G_Numbers ====== ', G_Numbers)
        [self.add_G_number(G_Number) for G_Number in G_Numbers]

    def add_G_number(self, G_Number):
        print('G_Number in add_G_number: ', G_Number)
        self.g54_g55 = G54_G55(self.dialog, G_Number)
        self.addTab(self.g54_g55, G_Number)



class Workpieces_frame(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.dialog = father
        self.workpieces_tab = TabWorkpieces(self.dialog)

        grid.addWidget(self.workpieces_tab, 0, 0)



class MachineTab(QTabWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = father
        self.ax_frame = AxisFrame(self)
        self.addTab(self.ax_frame, 'Axis On/Off')
        self.setStyleSheet(
            'background-color: rgb(200, 200, 200); border-style: outset;  font-size: 15px;')
        self.work_pieces = Workpieces_frame(self.dialog)
        self.addTab(self.work_pieces, 'Workpices: G54, G55')


class machine_dialog(QDialog):
    def __init__(self, main_inteface, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_interface = main_inteface
        self.scene0 = self.main_interface.centre.left.left_tab.b.openGL
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(518, 318)
        self.machine_options = MachineTab(self)
        self.setWindowTitle('Machine options')
        grid.addWidget(self.machine_options, 0, 0)

def validate_text_digit(self):
    self.onlyInt = QtGui.QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)