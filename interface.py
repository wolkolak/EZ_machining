from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar
from PyQt5.QtCore import Qt
import gui_classes
import settings
import MyTxtToolBar, MyViewToolBar
import re
import fileinput
import os
import shutil
import FileMenu, ViewMenu, OptionsMenu, EditMenu


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        print('main window started')
        self.splitter_flag = settings.splitter_parameters['flag']

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings.interface_settings['main_width'], settings.interface_settings['main_height'])
        self.centre = gui_classes.CenterWindow()
        self.setCentralWidget(self.centre)
        self.statusBar()
        self.menubar = self.menuBar()

        #file
        FileMenu.file_open(self)
        #Edit
        EditMenu.edit_opt(self)
        #View
        ViewMenu.view_opt(self)

        self.toolsMenu = self.menubar.addMenu('&Tools')
        self.inportMenu = self.menubar.addMenu('&Import')

        #options
        OptionsMenu.options(self)

        toolbar1 = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(gui_classes.color3))
        toolbar1.addAction(self.exitAction)

        self.view_f = MyViewToolBar.MyViewToolBar(self)
        self.txt_tools = MyTxtToolBar.MyTextToolBar(self)

        self.centre.note.currentChanged.connect(self.change_tab)

        self.light_out(False)

        print('foninf:', self.fontInfo())
        self.setFont(settings.font1)
        try:
            self.restoreState(settings.saved_toolbars)
        finally:
            pass

    def return_files(self):
        pass

    def super_out(self):
        self.centre.note.close_all()

    def find_obertka(self):
        self.centre.note.currentWidget().find_in_text()

    def change_tab(self, n):
        print('tab change')

        if self.centre.note.currentIndex() != -1:
            if self.centre.note.currentWidget().existing is False:
                title2 = self.centre.note.tabText(n)
            else:
                title2 = self.centre.note.currentWidget().existing
            self.setWindowTitle('EZ machining:  {}'.format(title2))
            self.light_out(True)
            self.centre.note.currentWidget().setFocus()
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
        name3 = 'saved_toolbars '
        print(self.centre.splitter.sizes())
        try:
            with fileinput.FileInput('settings.py', inplace=True, backup='.bak') as settings:
                for line in settings:
                    if re.match(name1, line):
                        print("{}= {{'main_width': {}, 'main_height':{} }}".format(name1, self.width(), self.height()))
                    elif re.match(name2, line):
                        print("{}= {{'lefty': {}, 'righty': {}, 'flag': {} }}".format(name2, self.centre.splitter.sizes()[0],
                        self.centre.splitter.sizes()[1], self.splitter_flag))
                    elif re.match(name3, line):
                        print("{}= {}".format(name3, self.saveState()))

                    else:
                        print(line, end='')
            os.unlink('settings.py' + '.bak')
        except OSError:
            gui_classes.simple_warning('Ooh', 'Something went wrong \n ¯\_(ツ)_/¯')

        toolbars_plasemnt = self.saveState()
        print('tolbars:', toolbars_plasemnt)
        print('toolbasrs type', type(toolbars_plasemnt))

    def restore_all_options(self):
        shutil.copyfile('default_settings.py', 'settings.py', follow_symlinks=True)

        self.setGeometry(100, 100, settings.interface_settings['main_width'], settings.interface_settings['main_height'])
        self.centre.splitter.setSizes([settings.splitter_parameters['lefty'], settings.splitter_parameters['righty']])
        self.splitter_flag = 2

    def close_half(self):
        print(self.splitter_flag)
        if self.splitter_flag == 1:
            self.centre.splitter.setSizes([100, 0])
            self.splitter_flag = self.splitter_flag + 1
        elif self.splitter_flag == 2:
            self.centre.splitter.setSizes([settings.splitter_parameters['lefty'], settings.splitter_parameters['righty']])
            self.splitter_flag = self.splitter_flag + 1
        else:
            self.centre.splitter.setSizes([0, 100])
            self.splitter_flag = 1
