from PyQt5.QtWidgets import QDialog, QCheckBox, QGridLayout, QComboBox, QFrame, QLabel, QTabWidget, QWidget, QLineEdit, QPushButton, QPlainTextEdit
from PyQt5 import QtGui, QtCore
import math
from CNC_generator.groove_cylinder import TurnGroove



class CNC_GeneratorDialog(QDialog):
    def __init__(self, main_interface, *args, **kwargs):
        super().__init__(main_interface, *args, **kwargs)
        self.operations_dict = {'Turn groove': TurnGroove(self), }#'Turn Thread': TurnThread(self)
        #self.current_line = 'Turn groove'
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(800, 670)
        self.grid = QGridLayout()
        self.grid.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        #self.grid.setRowStretch(0, 1)
        self.setLayout(self.grid)
        self.choose_operation = OperationChooser(self)
        self.grid.addWidget(self.choose_operation, 0, 0)


class TurnThread(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(590, 355)
        self.hide()
        grid = QGridLayout()
        self.setLayout(grid)
        #self.setStyleSheet(' font-size: 15px;')
        self.father = father
        self.was_bin_ich = QLabel('резьба')
        grid.addWidget(self.was_bin_ich, 1, 0)


class OperationChooser(QComboBox):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.father = father
        self.setFixedSize(150, 40)
        for key_ in self.father.operations_dict:
            self.addItem(key_)
            self.father.grid.addWidget(self.father.operations_dict[key_], 1, 0)
        self.setCurrentIndex(0)
        self.father.operations_dict[self.currentText()].show()
        self.current_str = self.currentText()
        self.currentIndexChanged.connect(self.show_corresponding_form)

    def show_corresponding_form(self):
        self.father.operations_dict[self.current_str].hide()
        self.father.operations_dict[self.currentText()].show()
        self.current_str = self.currentText()