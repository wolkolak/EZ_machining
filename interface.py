from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import gui_classes
from settings import interface_settings, default_interface_settings
import re
import fileinput
import os


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.splitter_flag = 1

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
        restoreOptionsAction.triggered.connect(lambda: self.restore_options('interface_settings', 'default_interface_settings'))
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
        pass

    def restore_options(self, name, defaultname):
        x = None
        y = None
        name = name + ' '
        defaultname = defaultname + ' '

        with open('settings.py') as settings:
            for index, line in enumerate(settings):
                if re.match(name, line):
                    x, cur_line = index, line
                if re.match(defaultname, line):
                    y, def_line = index, line
                if x and y:
                    print('x=', x, 'y=', y)
                    break
        try:
            with fileinput.FileInput('settings.py', inplace=True, backup='.bak') as settings:
                for index, line in enumerate(settings):
                    if index != x:
                        print(line, end='')
                    else:
                        print(name + def_line[len(defaultname):])
            os.unlink('settings.py' + '.bak')
        except OSError:
            gui_classes.simple_warning('Ooh', 'Something went wrong \n ¯\_(ツ)_/¯')
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
        print(self.splitter_flag)