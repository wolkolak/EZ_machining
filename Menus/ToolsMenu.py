from PyQt5.QtWidgets import QAction, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap, QDoubleValidator, QFont
from Menus.EditMenu import add_action

from Gui.tools_draft import draft_dialog
from Gui.tools_machine import machine_dialog


def tools_menu_opt(self):
    self.toolsMenu = self.menubar.addMenu('&Tools')

    self.changePointAndScaleAction = QAction(QIcon('icons/open.png'), 'Draft property', self)
    add_action(self.toolsMenu, self.changePointAndScaleAction, 'Change draft property', lambda: empty_draft_property(self), 'Ctrl+D')
    self.changePointAndScaleAction.setStatusTip('All options regarding draft')

    self.changeMachineProperty = QAction(QIcon('icons/open.png'), 'Machine property', self)
    add_action(self.toolsMenu, self.changeMachineProperty, 'Change draft property',
               lambda: empty_machine_property(self), 'Ctrl+M')
    self.changeMachineProperty.setStatusTip('Machine options')

def empty_machine_property(self):
    print('Machine property')
    self.machine_prop = machine_dialog(self).show()

def empty_draft_property(self):
    print('Change draft property')
    self.draft_prop = draft_dialog(self).show()


class DraftItem(QListWidgetItem):
    def __init__(self, text, width, height, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self. width = width
        self.height = height













