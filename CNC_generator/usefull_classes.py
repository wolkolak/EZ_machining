import math
from CNC_generator.usefull_funcs import transfer, k_multiplayer, move_ax_along
from PyQt5.QtWidgets import QDialog, QCheckBox, QGridLayout, QComboBox, QFrame, QLabel, QTabWidget, QWidget, QLineEdit, QPushButton, QPlainTextEdit
from PyQt5 import QtGui, QtCore
from Gui.little_gui_classes import simple_warning
from CNC_generator.usefull_funcs import move_ax_along

class RTurnTool(QFrame):
    def __init__(self, father, op_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.father = father
        self.op_type = op_type
        self.R_lbl = QLabel('R')
        #self.R_lbl.setFixedWidth(10)
        self.grid.addWidget(self.R_lbl, 0, 0)
        self.R = QLineEdit('5')
        self.grid.addWidget(self.R, 0, 1)
        #self.Bind_lbl = QLabel('Bind')
        #grid.addWidget(self.Bind_lbl, 0, 1)
        self.Bind = QComboBox()

        self.Bind.setFixedSize(70, 100)
        self.Bind.setIconSize(QtCore.QSize(50, 100))
        self.grid.addWidget(self.Bind, 0, 4, 2, 1)
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind1.png'), '')#addItem(QtGui.QIcon('icons/turn_r.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind2.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind3.png'), '')
        #self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind4.png'), '')
        #self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind5.png'), '')
        if self.op_type == 'rough':
            self.RX_step_lbl = QLabel('rX step')
            self.grid.addWidget(self.RX_step_lbl, 0, 2)
            self.RX_step = QLineEdit('10')
            self.grid.addWidget(self.RX_step, 0, 3)
            self.ZX_step_lbl = QLabel('Lap min')
            self.grid.addWidget(self.ZX_step_lbl, 1, 2)
            self.ZX_step = QLineEdit('1')
            self.grid.addWidget(self.ZX_step, 1, 3)


class CutTurnTool(QFrame):
    def __init__(self, father, op_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.father = father
        self.op_type = op_type
        self.R_lbl = QLabel('R')
        self.grid.addWidget(self.R_lbl, 0, 0)
        self.R = QLineEdit('0.2')
        self.grid.addWidget(self.R, 0, 1)
        #self.Bind_lbl = QLabel('Bind')
        #grid.addWidget(self.Bind_lbl, 0, 1)
        self.B_lbl = QLabel('B')
        self.grid.addWidget(self.B_lbl, 1, 0)
        self.B = QLineEdit('4')
        self.grid.addWidget(self.B, 1, 1)
        self.Bind = QComboBox()
        #self.setStyleSheet('margin-top: -10; margin-bottom: 0;')#margin-bottom: 10; margin-top: -1;'border: 0px'
        #self.Bind.setStyleSheet ("QComboBox::drop-down {border-width: 0px;} ")#QComboBox::down-arrow {border-width: 0px;image: url(noimg)};
        #self.B.setStyleSheet('QComboBox::down-arrow {border-width: 0px}')
        self.Bind.setFixedSize(70, 100)
        self.Bind.setIconSize(QtCore.QSize(50, 100))
        self.grid.addWidget(self.Bind, 0, 4, 2, 1)
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind1.png'), '')  # addItem(QtGui.QIcon('icons/turn_r.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind2.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind3.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind4.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/cut_off_bind5.png'), '')
        if self.op_type == 'rough':
            self.RX_step_lbl = QLabel('rX step')
            self.grid.addWidget(self.RX_step_lbl, 0, 2)
            self.RX_step = QLineEdit('10')
            self.grid.addWidget(self.RX_step, 0, 3)
            self.ZX_overlap = QLabel('overlap')
            self.grid.addWidget(self.ZX_overlap, 1, 2)
            self.ZX_step = QLineEdit('1')
            self.grid.addWidget(self.ZX_step, 1, 3)


class SharpTurnTool(QFrame):
    def __init__(self, father, op_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.father = father

        self.op_type = op_type
        self.R_lbl = QLabel('R')
        #self.R_lbl.setStyleSheet('border-width: 0px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 0px;')
        self.grid.addWidget(self.R_lbl, 0, 0)
        self.R = QLineEdit('0.8')
        #self.R.setStyleSheet('border-width: 0px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 0px;')
        self.grid.addWidget(self.R, 0, 1)
        #self.Bind_lbl = QLabel('Bind')
        #grid.addWidget(self.Bind_lbl, 0, 1)
        self.Angle_lbl = QLabel('Angle')
        self.grid.addWidget(self.Angle_lbl, 1, 0)
        self.Angle = QLineEdit('15')
        self.grid.addWidget(self.Angle, 1, 1)
        self.Bind = QComboBox()
        self.Bind.setFixedSize(70, 100)
        self.Bind.setIconSize(QtCore.QSize(50, 100))
        self.grid.addWidget(self.Bind, 0, 3, 2, 1)
        self.Bind.addItem(QtGui.QIcon('icons/sharp_cut_b1.png'), '')#addItem(QtGui.QIcon('icons/turn_r.png'), '')
        self.Bind.addItem(QtGui.QIcon('icons/sharp_cut_b3.png'), '')
        self.RX_step_lbl = QLabel('rX step')
        # self.RX_step_lbl.setStyleSheet('border-width: 0px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 0px;')
        self.grid.addWidget(self.RX_step_lbl, 2, 0)
        self.RX_step = QLineEdit('2')
        # self.RX_step.setStyleSheet('border-width: 0px; margin-top: 0px; margin-bottom: 0px; padding-top: 0px; padding-bottom: 0px;')
        self.grid.addWidget(self.RX_step, 2, 1)
        self.RX_step.setToolTip('Relative stock rX allowance\nlayer to cut')
        #if self.op_type == 'rough':
        #    #self.setStyleSheet('font-size: 10px;')
        #else:
        #    self.rXallowance = QLineEdit('1')
        #    self.grid.addWidget(self.rXallowance, 2, 1)
        #    self.rXallowance.setToolTip('Relative stock rX allowance\nlayer to cut')
        #    self.rXallowance_lbl = QLabel("Stock rX'")
        #    self.grid.addWidget(self.rXallowance_lbl, 2, 0)



class Turn45Tool(QFrame):
    def __init__(self, father, op_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hide()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.father = father
        self.op_type = op_type
        self.R_lbl = QLabel('R')
        self.grid.addWidget(self.R_lbl, 0, 0)
        self.R = QLineEdit('5')
        self.grid.addWidget(self.R, 0, 1)
        self.tool_panel = ToolRoughPanel2(self)
        self.setStyleSheet('font-size: 10px; border-width: 0px; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-left: 0px; padding-right: 0px')
        if self.op_type == 'rough':
            self.RX_step_lbl = QLabel('rX step')
            self.grid.addWidget(self.RX_step_lbl, 1, 0)
            self.RX_step = QLineEdit('2')
            self.grid.addWidget(self.RX_step, 1, 1)
        self.grid.addWidget(self.tool_panel, 0, 4, 2, 1)


class ToolFinishPanel(QFrame):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.GrooveTool = father
        grid = QGridLayout()
        self.grid = grid
        self.setLayout(grid)
        self.name_lbl = QLabel('Finish')
        grid.addWidget(self.name_lbl, 0, 0, 1, 2)
        self.tool_chooser = QComboBox()
        self.tool_chooser.setFixedSize(70, 100)
        self.tool_chooser.setIconSize(QtCore.QSize(50, 100))
        grid.addWidget(self.tool_chooser, 1, 0)
        self.tool_chooser.addItem(QtGui.QIcon('icons/turn_cutoff.png'), '')
        self.tool_chooser.addItem(QtGui.QIcon('icons/turn_r.png'), '')
        self.tool_chooser.addItem(QtGui.QIcon('icons/sharp_cut.png'), '')
        self.tools_list = [CutTurnTool(self, 'finish'), RTurnTool(self, 'finish'), SharpTurnTool(self, 'finish')]
        self.tools_list[0].show()
        for el in self.tools_list:
            grid.addWidget(el, 1, 1, alignment=QtCore.Qt.AlignTop)
        self.tool_chooser.currentIndexChanged.connect(self.choose_tool_param)

    def choose_tool_param(self):
        i = self.tool_chooser.currentIndex()
        for index in range(len(self.tools_list)):
            if index == i:
                self.tools_list[index].show()
            else:
                self.tools_list[index].hide()

class ToolRoughPanel2(ToolFinishPanel):
    def __init__(self, father, *args, **kwargs):
        super().__init__(father, *args, **kwargs)
        self.tool_chooser.addItem(QtGui.QIcon('icons/turn_passing'), '')
        #self.tools_list.append(Turn45Tool(self, 'rough'))
        self.tools_list[0].hide()
        self.name_lbl.setText('Rough')
        self.name_lbl.hide()
        self.tools_list = [CutTurnTool(self, 'rough'), RTurnTool(self, 'rough'), SharpTurnTool(self, 'rough')]
        self.tool_chooser.removeItem(3)
        self.tool_chooser.setFixedSize(35, 50)
        self.tool_chooser.setIconSize(QtCore.QSize(25, 50))
        #self.setStyleSheet('font-size: 10px; border-width: 0px; margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-left: 0px; padding-right: 0px')
        self.tools_list[0].show()
        for el in self.tools_list:
            #el.setStyleSheet('background-color: red')
            el.Bind.setFixedSize(35, 50)
            el.Bind.setIconSize(QtCore.QSize(25, 50))
            #el.grid.removeWidget(el.Bind)
            #el.grid.addWidget(el.Bind, 0, 1)
            self.grid.addWidget(el, 1, 1)