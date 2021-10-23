from PyQt5.QtWidgets import QAction, QApplication, QDialog, QGridLayout, QFrame, QLabel, \
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTabWidget


from PyQt5 import QtCore, QtGui

class AxisFrame(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = father



class G54SmallClass(QFrame):
    def __init__(self, father,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        self.setLayout(grid)
        self.g54_window = father
        self.ax_label = QLabel()
        grid.addWidget(self.ax_label, 0, 0, 1, 1, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ax_field = QLineEdit()
        #self.ax_field.setText(letter)
        self.ax_field.setValidator(self.g54_window.onlyInt)
        self.ax_field.setStyleSheet('background-color: rgb(255, 255, 255); border-style: outset;')
        self.ax_field.setAlignment(QtCore.Qt.AlignRight)
        grid.addWidget(self.ax_field, 0, 1, 1, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


class G54_G55(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        validate_text_digit(self)
        self.dialog = father
        #self.setFixedWidth(150)

        i = 0
        for letter in 'XYZABC':#нужен какой то
            name = letter + '_small_frame'
            setattr(self, name, G54SmallClass)
            #exec(foo + " = 'something else'")
            #print(self.__dir__())
            #print('getattr(self, name) == ', getattr(self, name))
            new_small_frame = getattr(self, name)(self)
            new_small_frame.ax_label.setText(letter)
            new_small_frame.ax_field.setText('0.')
            self.my_add_widget(new_small_frame, 'background-color: rgb(200, 200, 100); border-style: outset; ', 100, 50, i, 0)
            i = i + 1
        self.grid.setAlignment(QtCore.Qt.AlignLeft)
        self.accept = QPushButton('Accept')
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
        self.g54_g55 = G54_G55(self.dialog)
        self.addTab(self.g54_g55, 'G54')



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
        self.work_pieces = Workpieces_frame(self)
        self.addTab(self.work_pieces, 'Workpices: G54, G55')


class machine_dialog(QDialog):
    def __init__(self, main_inteface, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_inteface = main_inteface
        self.scene0 = self.main_inteface.centre.left.left_tab.b.openGL
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