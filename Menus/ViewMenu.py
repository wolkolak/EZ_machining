from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
from Gui import gui_classes


def view_opt(self):
    self.viewMenu = self.menubar.addMenu('&View')
    self.splitterMove = QAction(QIcon('icons/splitter.png'), 'shift', self)
    self.splitterMove.triggered.connect(self.close_half)

    self.change_font = QAction(QIcon('icons/open.png'), 'Font', self)
    self.change_font.triggered.connect(gui_classes.my_font_diag)

    self.viewMenu.addAction(self.splitterMove)
    self.viewMenu.addAction(self.change_font)

    self.BackplotView = self.viewMenu.addMenu('&Backplot VieW')
    self.placeStartAction = QAction(QIcon('icons/scrap1.png'), 'Begin here', self)
    self.placeStartAction.setShortcut('Ctrl+B')
    self.placeStartAction.triggered.connect(self.remeber_start_point)
    self.BackplotView.addAction(self.placeStartAction)

    self.unPlaceStartAction = QAction(QIcon('icons/open.png'), 'Discard Beginning Point', self)
    self.unPlaceStartAction .setShortcut('Ctrl+E')
    self.unPlaceStartAction.triggered.connect(self.drop_point)
    self.BackplotView.addAction(self.unPlaceStartAction)