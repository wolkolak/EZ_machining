from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main import settings
import gui_classes


class MyMainWindow(QMainWindow):



    #path[path.rindex('/') + 1:-1]
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.splitter_flag = 1

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings['main_width'], settings['main_height'])
        self.centre = gui_classes.CenterWindow()
        self.setCentralWidget(self.centre)
        self.statusBar()


        openAction = QAction(QIcon('icons\open.png'), 'Open', self)
        openAction.setStatusTip('Open GM File')
        openAction.triggered.connect(self.centre.note.open_file)

        newTabAction = QAction(QIcon(r'icons\new_tab.png'), 'New', self)
        newTabAction.setShortcut('Ctrl+N')
        newTabAction.setStatusTip('New File')
        newTabAction.triggered.connect(self.centre.note.new_tab)

        saveAction = QAction(QIcon('icons\save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current File')
        saveAction.triggered.connect(self.centre.note.save_file)
        self.centre.note.save_tab_button.clicked.connect(self.centre.note.save_file)

        saveAsAction = QAction(QIcon('icons\save_as.png'), 'Save As', self)
        saveAsAction.setStatusTip('Save File As')
        saveAsAction.triggered.connect(self.centre.note.save_file_as)

        closeTab = QAction(QIcon('icons\save_as.png'), 'Close Tab', self)
        closeTab.setStatusTip('Close Current')
        closeTab.triggered.connect(self.centre.note.close_current)

        closeAll = QAction(QIcon('icons\save_as.png'), 'Close All', self)
        closeAll.setStatusTip('Close All Tabs')
        closeAll.triggered.connect(self.centre.note.close_all)

        exitAction = QAction(QIcon('icons\exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        splitterMove.triggered.connect(self.close_half)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newTabAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeTab)
        fileMenu.addAction(closeAll)
        fileMenu.addAction(exitAction)


        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(splitterMove)

        toolsMenu = menubar.addMenu('&Tools')
        inportMenu = menubar.addMenu('&Import')
        optionsMenu = menubar.addMenu('&Options')




        toolbar1 = QToolBar(self)
        self.addToolBar( Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(gui_classes.color3))
        toolbar1.addAction(exitAction)

        txt_tools = QToolBar(self)
        self.addToolBar( Qt.RightToolBarArea, txt_tools)
        txt_tools.setStyleSheet("background-color: {}".format(gui_classes.color3))
        txt_tools.addAction(splitterMove)


        
    def close_half(self):

        if self.splitter_flag == 1:
            self.centre.splitter.setSizes([100, 0])
            self.splitter_flag = self.splitter_flag + 1
        elif self.splitter_flag == 2:
            self.centre.splitter.setSizes([100, 100])
            self.splitter_flag = self.splitter_flag + 1
        else:
            self.centre.splitter.setSizes([0, 100])
            self.splitter_flag = 1
        print(self.splitter_flag )