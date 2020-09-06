from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import gui_classes
from settings import interface_settings, splitter_parameters
import re
import fileinput
import os
import shutil

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.splitter_flag = splitter_parameters['flag']

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, interface_settings['main_width'], interface_settings['main_height'])
        self.centre = gui_classes.CenterWindow()
        self.setCentralWidget(self.centre)
        self.statusBar()
        menubar = self.menuBar()

        #file
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





        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newTabAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeTab)
        fileMenu.addAction(closeAll)
        fileMenu.addAction(exitAction)


        #View
        splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        splitterMove.triggered.connect(self.close_half)
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(splitterMove)

        toolsMenu = menubar.addMenu('&Tools')
        inportMenu = menubar.addMenu('&Import')

        #options

        saveOptionsAction = QAction(QIcon('icons\open.png'), 'Save Options', self)
        saveOptionsAction.setStatusTip('save options')
        saveOptionsAction.triggered.connect(self.save_options)

        restoreOptionsAction = QAction(QIcon('icons\open.png'), 'Restore Default', self)
        restoreOptionsAction.setStatusTip('restore default options')
        restoreOptionsAction.triggered.connect(self.restore_all_options)

        optionsMenu = menubar.addMenu('&Options')
        optionsMenu.addAction(saveOptionsAction)
        optionsMenu.addAction(restoreOptionsAction)



        toolbar1 = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(gui_classes.color3))
        toolbar1.addAction(exitAction)

        txt_tools = QToolBar(self)
        self.addToolBar(Qt.RightToolBarArea, txt_tools)
        txt_tools.setStyleSheet("background-color: {}".format(gui_classes.color3))
        txt_tools.addAction(splitterMove)

    def save_options(self):
        """
        :return: changing exact values of exact names
        """
        name1 = 'interface_settings '
        name2 = 'splitter_parameters '
        print(self.centre.splitter.sizes())
        try:
            with fileinput.FileInput('settings.py', inplace=True, backup='.bak') as settings:
                for line in settings:
                    if re.match(name1, line):
                        print("interface_settings = {{'main_width': {}, 'main_height':{} }}".format(self.width(), self.height()))
                    elif re.match(name2, line):
                        print("splitter_parameters = {{'lefty': {}, 'righty': {}, 'flag': {} }}".format(self.centre.splitter.sizes()[0],
                        self.centre.splitter.sizes()[1], self.splitter_flag))
                    else:
                        print(line, end='')
            os.unlink('settings.py' + '.bak')
        except OSError:
            gui_classes.simple_warning('Ooh', 'Something went wrong \n ¯\_(ツ)_/¯')

    def restore_all_options(self):
        shutil.copyfile('default_settings.py', 'settings.py', follow_symlinks=True)
        from settings import interface_settings
        self.setGeometry(100, 100, interface_settings['main_width'], interface_settings['main_height'])
        self.centre.splitter.setSizes([splitter_parameters['lefty'], splitter_parameters['righty']])
        self.splitter_flag = 2

    def close_half(self):
        print(self.splitter_flag)
        if self.splitter_flag == 1:
            self.centre.splitter.setSizes([100, 0])
            self.splitter_flag = self.splitter_flag + 1
        elif self.splitter_flag == 2:
            self.centre.splitter.setSizes([splitter_parameters['lefty'], splitter_parameters['righty']])
            self.splitter_flag = self.splitter_flag + 1
        else:
            self.centre.splitter.setSizes([0, 100])
            self.splitter_flag = 1
