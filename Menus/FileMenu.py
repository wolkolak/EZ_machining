from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar
from PyQt5.QtGui import QIcon

def file_open(self):
    self.openAction = QAction(QIcon('icons/open.png'), 'Open', self)
    self.openAction.setStatusTip('Open GM File')
    self.openAction.triggered.connect(self.centre.note.open_file)

    self.newTabAction = QAction(QIcon('icons/new_tab.png'), 'New', self)
    self.newTabAction.setShortcut('Ctrl+N')
    self.newTabAction.setStatusTip('New File')
    self.newTabAction.triggered.connect(self.centre.note.new_tab)

    self.saveAction = QAction(QIcon('icons/save.png'), 'Save', self)
    self.saveAction.setShortcut('Ctrl+S')
    self.saveAction.setStatusTip('Save current File')
    self.saveAction.triggered.connect(self.centre.note.save_file)
    self.centre.note.save_tab_button.clicked.connect(self.centre.note.save_file)


    self.saveAsAction = QAction(QIcon('icons/save_as.png'), 'Save As', self)
    self.saveAsAction.setStatusTip('Save File As')
    self.saveAsAction.triggered.connect(self.centre.note.save_file_as)

    self.closeTab = QAction(QIcon('icons/save_as.png'), 'Close Tab', self)
    self.closeTab.setStatusTip('Close Current')
    self.closeTab.triggered.connect(self.centre.note.close_current)

    self.closeAll = QAction(QIcon('icons/save_as.png'), 'Close All', self)
    self.closeAll.setStatusTip('Close All Tabs')
    self.closeAll.triggered.connect(self.centre.note.close_all)

    self.exitAction = QAction(QIcon('icons/exit24.png'), 'Exit', self)
    self.exitAction.setShortcut('Ctrl+Q')
    self.exitAction.setStatusTip('Exit application')
    self.exitAction.triggered.connect(self.super_out)#qApp.quit Но пока тоже что и Close All

    self.lastAllAction = QAction(QIcon('icons/exit24.png'), 'All', self)
    self.lastAllAction.setStatusTip('All previous files')
    self.lastAllAction.triggered.connect(self.return_files)

    self.fileMenu = self.menubar.addMenu('&File')
    self.fileMenu.addAction(self.newTabAction)
    self.fileMenu.addAction(self.openAction)
    self.fileMenu.addAction(self.saveAction)
    self.fileMenu.addAction(self.saveAsAction)
    self.last = self.fileMenu.addMenu('&Previous')
    self.last.addAction(self.lastAllAction)

    self.fileMenu.addAction(self.closeTab)
    self.fileMenu.addAction(self.closeAll)
    self.fileMenu.addAction(self.exitAction)
