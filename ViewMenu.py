from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
import gui_classes

def view_opt(self):
    self.viewMenu = self.menubar.addMenu('&View')
    self.splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
    self.splitterMove.triggered.connect(self.close_half)

    self.change_font = QAction(QIcon('icons\open.png'), 'Font', self)
    self.change_font.triggered.connect(gui_classes.my_font_diag)

    self.viewMenu.addAction(self.splitterMove)
    self.viewMenu.addAction(self.change_font)