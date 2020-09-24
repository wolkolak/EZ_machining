from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon


def options(self):
    self.saveOptionsAction = QAction(QIcon('icons\open.png'), 'Save Options', self)
    self.saveOptionsAction.setStatusTip('save options')
    self.saveOptionsAction.triggered.connect(self.save_options)

    self.restoreOptionsAction = QAction(QIcon('icons\open.png'), 'Restore Default', self)
    self.restoreOptionsAction.setStatusTip('restore default options')
    self.restoreOptionsAction.triggered.connect(self.restore_all_options)

    self.optionsMenu = self.menubar.addMenu('&Options')
    self.optionsMenu.addAction(self.saveOptionsAction)
    self.optionsMenu.addAction(self.restoreOptionsAction)

