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

    self.textEdit = self.editMenu.addMenu('&Text Edit')
    self.placeStartAction = QAction(QIcon('icons\scrap1.png'), 'Begin here', self)
    self.placeStartAction.setShortcut('Ctrl+B')
    self.placeStartAction.triggered.connect(self.start_point)
    self.textEdit.addAction(self.placeStartAction)

    self.unPlaceStartAction = QAction(QIcon('icons\open.png'), 'Discard Beginning Point', self)
    self.unPlaceStartAction .setShortcut('Ctrl+E')
    self.unPlaceStartAction.triggered.connect(self.drop_point)
    self.textEdit.addAction(self.unPlaceStartAction)


