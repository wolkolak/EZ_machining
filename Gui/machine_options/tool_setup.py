from PyQt5.QtWidgets import QGridLayout, QFrame, QPushButton, QComboBox
from os import walk
from PyQt5 import QtCore
from Gui.tool_register_edit import RegisterToolDialog
from Settings.change_setting import change_file_vars


class ToolSetup(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        grid = QGridLayout()
        grid.setRowStretch(3, 1)
        self.setLayout(grid)
        self.machine_tab = father
        self.setStyleSheet(' font-size: 20px;')#background-color: rgb(200, 200, 200);
        self.tool_registers = QComboBox(self)#ToolRegister
        self.tool_registers.setStyleSheet('background-color: white')
        grid.addWidget(self.tool_registers, 0, 0, 1, 2)

        self.new_register = QPushButton('New register')
        self.new_register.setFixedSize(155, 50)
        grid.addWidget(self.new_register, 1, 0, QtCore.Qt.AlignLeft)

        self.edit_register = QPushButton('Edit register')
        self.edit_register.setFixedSize(155, 50)
        self.edit_register.clicked.connect(self.edit_register_func)
        grid.addWidget(self.edit_register, 1, 1, alignment=QtCore.Qt.AlignRight)

        self.connect_to_machine = QPushButton('Accept')
        self.connect_to_machine.setToolTip('Connect to \n current machine')
        self.connect_to_machine.setFixedSize(75, 50)
        self.connect_to_machine.clicked.connect(self.update_tool_setup)
        #функции то нету((()))
        grid.addWidget(self.connect_to_machine, 1, 2, alignment=QtCore.Qt.AlignRight)
        self.update_registers()

    def edit_register_func(self):
        print('LYAAA')
        fff = RegisterToolDialog(self)
        fff.exec()

    def update_tool_setup(self):
        names = [['bound_register', "'{}'".format(self.tool_registers.currentText())]]
        if self.machine_tab.dialog.main_interface.centre.note.currentIndex() == -1:
            m = self.machine_tab.dialog.main_interface.centre.note.default_machine_item
        else:
            m = self.machine_tab.dialog.main_interface.centre.note.currentWidget().current_machine
        address = m.machine_settings_open
        change_file_vars(address, names, '=')
        self.machine_tab.dialog.bigcustom.update_scene_machine()

    def update_registers(self, catalog="Modelling_clay\\tool_registers"):
        tree = walk(catalog)
        second_ = next(tree)[2]
        for tr in second_:
            if tr != '__init__.py':
                self.tool_registers.addItem(tr)

