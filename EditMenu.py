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




