from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import settings


def edit_opt(self):
    self.findAction = QAction(QIcon('icons\open.png'), 'Find', self)
    self.findAction.setStatusTip('find in current text')
    self.findAction.triggered.connect(self.find_obertka)
    self.findAction.setShortcut('Ctrl+F')

    self.undoAction = QAction(QIcon('icons\open.png'), 'Undo', self)
    self.undoAction.setStatusTip('Cancel previous change')
    self.undoAction.triggered.connect(self.undo_obertka)
    self.undoAction.setShortcut('Ctrl+Z')



    self.editMenu = self.menubar.addMenu('&Edit')
    self.editMenu.addAction(self.findAction)
    self.editMenu.addAction(self.undoAction)




