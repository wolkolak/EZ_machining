from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog, QMessageBox, QDialog, QPlainTextEdit,\
    QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QTextDocument
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
        print('main window started')
        self.splitter_flag = splitter_parameters['flag']

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, interface_settings['main_width'], interface_settings['main_height'])
        self.centre = gui_classes.CenterWindow()
        self.setCentralWidget(self.centre)
        self.statusBar()
        self.menubar = self.menuBar()

        #file
        self.openAction = QAction(QIcon('icons\open.png'), 'Open', self)
        self.openAction.setStatusTip('Open GM File')
        self.openAction.triggered.connect(self.centre.note.open_file)

        self.newTabAction = QAction(QIcon(r'icons\new_tab.png'), 'New', self)
        self.newTabAction.setShortcut('Ctrl+N')
        self.newTabAction.setStatusTip('New File')
        self.newTabAction.triggered.connect(self.centre.note.new_tab)

        self.saveAction = QAction(QIcon('icons\save.png'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save current File')
        self.saveAction.triggered.connect(self.centre.note.save_file)
        self.centre.note.save_tab_button.clicked.connect(self.centre.note.save_file)


        self.saveAsAction = QAction(QIcon('icons\save_as.png'), 'Save As', self)
        self.saveAsAction.setStatusTip('Save File As')
        self.saveAsAction.triggered.connect(self.centre.note.save_file_as)

        self.closeTab = QAction(QIcon('icons\save_as.png'), 'Close Tab', self)
        self.closeTab.setStatusTip('Close Current')
        self.closeTab.triggered.connect(self.centre.note.close_current)

        self.closeAll = QAction(QIcon('icons\save_as.png'), 'Close All', self)
        self.closeAll.setStatusTip('Close All Tabs')
        self.closeAll.triggered.connect(self.centre.note.close_all)

        self.exitAction = QAction(QIcon('icons\exit24.png'), 'Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.super_out)#qApp.quit


        fileMenu = self.menubar.addMenu('&File')
        fileMenu.addAction(self.newTabAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addAction(self.closeTab)
        fileMenu.addAction(self.closeAll)
        fileMenu.addAction(self.exitAction)

        #Edit
        self.findAction = QAction(QIcon('icons\open.png'), 'Find', self)
        self.findAction.setStatusTip('find in current text')
        self.findAction.triggered.connect(self.find_obertka)
        self.findAction.setShortcut('Ctrl+F')
        self.editMenu = self.menubar.addMenu('&Edit')
        self.editMenu.addAction(self.findAction)

        #View
        self.viewMenu = self.menubar.addMenu('&View')
        self.splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        self.splitterMove.triggered.connect(self.close_half)
        self.viewMenu.addAction(self.splitterMove)



        

        toolsMenu = self.menubar.addMenu('&Tools')
        inportMenu = self.menubar.addMenu('&Import')

        #options

        self.saveOptionsAction = QAction(QIcon('icons\open.png'), 'Save Options', self)
        self.saveOptionsAction.setStatusTip('save options')
        self.saveOptionsAction.triggered.connect(self.save_options)

        self.restoreOptionsAction = QAction(QIcon('icons\open.png'), 'Restore Default', self)
        self.restoreOptionsAction.setStatusTip('restore default options')
        self.restoreOptionsAction.triggered.connect(self.restore_all_options)

        self.optionsMenu = self.menubar.addMenu('&Options')
        self.optionsMenu.addAction(self.saveOptionsAction)
        self.optionsMenu.addAction(self.restoreOptionsAction)



        toolbar1 = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(gui_classes.color3))
        toolbar1.addAction(self.exitAction)

        txt_tools = QToolBar(self)
        self.addToolBar(Qt.RightToolBarArea, txt_tools)
        txt_tools.setStyleSheet("background-color: {}".format(gui_classes.color3))
        txt_tools.addAction(self.splitterMove)

        self.centre.note.currentChanged.connect(self.change_title)

        self.light_out(False)

    def super_out(self):
        self.centre.note.close_all()

    def find_obertka(self):
        self.centre.note.currentWidget().find_in_text()

    def change_title(self, n):
        print('tab change')

        if self.centre.note.currentIndex() != -1:
            if self.centre.note.currentWidget().existing is False:
                title2 = self.centre.note.tabText(n)
            else:
                title2 = self.centre.note.currentWidget().existing
            self.setWindowTitle('EZ machining:  {}'.format(title2))
            self.light_out(True)
        else:
            self.setWindowTitle('EZ machining')
            self.light_out(False)

    def light_out(self, gamlet):
        self.saveAction.setEnabled(gamlet)
        self.saveAsAction.setEnabled(gamlet)
        self.centre.note.save_tab_button.setEnabled(gamlet)
        self.findAction.setEnabled(gamlet)
        self.editMenu.setEnabled(gamlet)



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
