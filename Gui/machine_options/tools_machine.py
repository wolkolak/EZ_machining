from PyQt5.QtWidgets import QGridLayout, QFrame, QLabel, QLineEdit,  QTabWidget
from PyQt5 import QtCore, QtGui
from Gui.machine_options.workpieces import Workpieces_frame
from Gui.machine_options.machine_settingsl_change import AxisOffsetFrame
from Gui.machine_options.tool_setup import ToolSetup


class MachineTab(QTabWidget):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = father
        self.setStyleSheet('font-size: 15px;')
        self.work_pieces = Workpieces_frame(self.dialog)
        self.addTab(self.work_pieces, 'Workpices: G54, G55')
        self.ax_frame = AxisOffsetFrame(self)
        self.addTab(self.ax_frame, 'Axles and Tool Change Point')
        self.tool_setup = ToolSetup(self)
        self.addTab(self.tool_setup, 'Tool setup')

    #def update_machine_in_scene(self):
    #    self.dialog.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()
    #    #self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()


def validate_text_digit(self):
    self.onlyInt = QtGui.QDoubleValidator()
    local_field = QtCore.QLocale(QtCore.QLocale.English)
    self.onlyInt.setLocale(local_field)