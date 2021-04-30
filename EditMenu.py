from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import settings


def edit_opt(self):
    self.findAction = QAction(QIcon('icons\open.png'), 'Find', self)
    self.findAction.setStatusTip('find in current text')
    self.findAction.triggered.connect(self.find_obertka)
    self.findAction.setShortcut('Ctrl+F')

    self.editMenu = self.menubar.addMenu('&Edit')
    self.editMenu.addAction(self.findAction)

    self.undoAction = QAction('Undo', self)
    self.redoAction = QAction("Redo", self)
    self.cutAction = QAction('Cut', self)
    self.copyAction = QAction('Copy', self)
    self.select_allAction = QAction('Select all', self)
    self.delAction = QAction('Delete', self)
    self.pasteAction = QAction('Paste', self)

    self.editMenu.addSeparator()
    add_action(self.editMenu, self.undoAction, 'Cancel previous change', self.undo_obertka, 'Ctrl+Z')
    add_action(self.editMenu, self.redoAction, 'Rewriting undone changes', self.redo_obertka, 'Ctrl+Y')
    self.editMenu.addSeparator()
    add_action(self.editMenu, self.cutAction, 'Cut text', self.cut_obertka, 'Ctrl+X')
    add_action(self.editMenu, self.copyAction, 'Copy text', self.copy_obertka, 'Ctrl+C')
    add_action(self.editMenu, self.pasteAction, 'Paste text', self.paste_obertka, 'Ctrl+V')
    add_action(self.editMenu, self.delAction, 'Delete text', self.del_obertka, 'Delete')
    self.editMenu.addSeparator()
    add_action(self.editMenu, self.select_allAction, 'Select all text', self.select_all_obertka, 'Ctrl+A')



def add_action(menu, nameaction, tip, my_slot, short_cut):
    nameaction.setStatusTip(tip)
    nameaction.triggered.connect(my_slot)
    nameaction.setShortcut(short_cut)
    menu.addAction(nameaction)

