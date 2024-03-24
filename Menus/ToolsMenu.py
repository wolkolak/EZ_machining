from PyQt5.QtWidgets import QAction, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QFont
from Menus.EditMenu import add_action

from Gui.tools_draft import draft_dialog
#from Gui.tools_machine import machine_dialog
from Gui.tools_JOG import JOG_dialog
from Gui.tools_Cut import Cut_tools_dialog
from CNC_generator.main_generator import CNC_GeneratorDialog


def tools_menu_opt(self):
    self.toolsMenu = self.menubar.addMenu('&Tools')

    self.changePointAndScaleAction = QAction(QIcon('icons/open.png'), 'Draft property', self)
    add_action(self.toolsMenu, self.changePointAndScaleAction, 'Change draft property', lambda: empty_draft_property(self), 'Ctrl+D')
    self.changePointAndScaleAction.setStatusTip('All options regarding draft')

    #self.changeMachineProperty = QAction(QIcon('icons/open.png'), 'Machine property', self)#todo убрать
    #add_action(self.toolsMenu, self.changeMachineProperty, 'Change draft property',
    #           lambda: empty_machine_property(self), 'Ctrl+M')
    #self.changeMachineProperty.setStatusTip('Machine options')

    self.JOG_action = QAction(QIcon('icons/open.png'), 'JOG', self)
    add_action(self.toolsMenu, self.JOG_action, 'Try JOG',
               lambda: JOG_tool(self), 'Ctrl+J')
    self.JOG_action.setStatusTip("JOG. For familiarization only")

    self.CutTools = QAction(QIcon('icons/open.png'), 'Cut tools', self)
    add_action(self.toolsMenu, self.CutTools, 'All tools for machining', lambda: open_dialog_tools(self), 'Ctrl+T')
    self.CutTools.setStatusTip('All tools for machining')

    self.CNC_generator_action = QAction(QIcon('icons/open.png'), 'CNC Generator', self)
    add_action(self.toolsMenu, self.CNC_generator_action, 'Generate G-cod',
               lambda: draft_call_CNC_generator(self), 'Ctrl+C+N')
    self.CNC_generator_action.setStatusTip('Easy Machining will try generate\nsome G-cod for you')

def open_dialog_tools(self):
    Cut_tools_dialog(self).show()


def JOG_tool(self):
    JOG_dialog(self).show()

#def empty_machine_property(self):
#    print('Machine property')
#    self.machine_prop = machine_dialog(self).show()

def empty_draft_property(self):
    print('Change draft property')
    self.draft_prop = draft_dialog(self).show()

def draft_call_CNC_generator(self):
    print('ща буду генерить')
    self.CNC_generator_item = CNC_GeneratorDialog(self).show()





class DraftItem(QListWidgetItem):
    def __init__(self, text, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self. width = width
        self.height = height













