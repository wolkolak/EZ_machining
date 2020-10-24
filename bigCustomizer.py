from PyQt5.QtWidgets import  QGridLayout,  QWidget, QTreeWidget, \
    QListView, QTreeView, QTreeWidgetItem, QFrame
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import  QTextDocument, QTextCharFormat,\
    QTextFormat, QGuiApplication
from settings import *
from find_replace import finder


class OptionsQTWItem(QTreeWidgetItem):
    def __init__(self, text, widget_to_show):
        super().__init__(text)
        self.widget_to_show = widget_to_show





class MyTree(QTreeWidget):
    def __init__(self, main):
        super().__init__()
        self.setMinimumSize(300, 300)
        #l1 = QTreeWidgetItem(["String A", "String B"])

        #l11 = QTreeWidgetItem(["Podstring A", "Podstring B"])
        #l1.addChild(l11)
        self.simulation = OptionsQTWItem(["Sim & HL rules"],  main.field_simulation)

        #self.addTopLevelItem(l1)
        self.addTopLevelItem(self.simulation)




class RightPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.setMinimumSize(300, 300)
        self.hide()

class SimulationOptionsPanel(RightPanel):
    def __init__(self):
        super().__init__()





class BigCustomizer(QWidget):
    def __init__(self, main):
        super().__init__()
        self.resize(800, 400)
        self.current_element = None

        self.setWindowTitle('Options')
        grid = QGridLayout()
        self.setLayout(grid)

        self._main = main

        self.field_simulation = SimulationOptionsPanel()
        self.SettingsTree = MyTree(self)
        self.SettingsTree.itemSelectionChanged.connect(lambda: self.show_options(self.SettingsTree.currentItem().widget_to_show))


        grid.addWidget(self.SettingsTree, 0, 0)
        grid.addWidget(self.field_simulation, 0, 1)

    def show_options(self, point):
        if self.current_element:
            self.current_element.hide()
        else:
            print('loh')
        self.current_element = point
        self.current_element.show()



