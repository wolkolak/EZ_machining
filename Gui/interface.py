from PyQt5.QtWidgets import QMainWindow, QToolBar
from PyQt5.QtCore import Qt
from Gui import gui_classes, MyViewToolBar, MyTxtToolBar, test_button
#MyTxtToolBar, MyViewToolBar,gui_classes
import shutil
import sys
from Menus import EditMenu, FileMenu, ViewMenu, OptionsMenu, ToolsMenu
from Settings import bigCustomizer, change_setting, settings
#from Gui import test_button

class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        print('main window started')
        self.splitter_flag = settings.splitter_parameters['flag']

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings.interface_settings['main_width'], settings.interface_settings['main_height'])
        self.centre = gui_classes.CenterWindow(self)
        self.setCentralWidget(self.centre)
        self.statusBar()
        self.menubar = self.menuBar()

        #file
        FileMenu.file_open(self)
        #Edit
        EditMenu.edit_opt(self)
        #View
        ViewMenu.view_opt(self)
        #Tools
        ToolsMenu.tools_menu_opt(self)
        #self.toolsMenu = self.menubar.addMenu('&Tools')

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
        self.custom = bigCustomizer.BigCustomizer(self)
        #self.light_out(False)
        EditMenu.update_edit_menu(self, self.centre.note.currentIndex())

        print('foninf:', self.fontInfo())
        self.setFont(settings.font1)
        try:
            self.restoreState(settings.saved_toolbars)
        finally:
            pass

        #Test
        test_button.test_opt(self)

    def closeEvent(self, evnt):
        self.super_out()
        evnt.ignore()

    def return_files(self):
        pass

    def super_out(self):
        self.centre.note.close_all()
        if self.centre.note.currentIndex() == -1:
            print('outta')
            sys.exit()

    def find_obertka(self):
        self.centre.note.currentWidget().editor.find_in_text()

    def replace_obertka(self):
        self.centre.note.currentWidget().editor.replace_in_text()

    def undo_obertka(self):
        self.centre.note.currentWidget().editor.my_undo()

    def redo_obertka(self):
        self.centre.note.currentWidget().editor.my_redo()

    def del_obertka(self):
        self.centre.note.currentWidget().editor.my_del()

    def paste_obertka(self):
        self.centre.note.currentWidget().editor.my_paste()

    def select_all_obertka(self):
        self.centre.note.currentWidget().editor.my_select_all()

    def copy_obertka(self):
        self.centre.note.currentWidget().editor.my_copy()

    def cut_obertka(self):
        self.centre.note.currentWidget().editor.my_cut()

    def change_tab(self, n):
        print('tab change')
        if self.centre.note.currentIndex() != -1:
            print('cur index = ', self.centre.note.currentIndex())
            #todo self.centre.note.currentWidget().current_g_cod_pool
            #self.centre.left.left_tab.a.reset_np_array_in_left_field()
            #self.centre.left.reset_np_array_in_left_field()
            self.centre.left.update_visible_np_left()
            if self.centre.note.currentWidget().editor.existing is False:
                title2 = self.centre.note.tabText(n)
            else:
                title2 = self.centre.note.currentWidget().editor.existing
            self.setWindowTitle('EZ machining:  {}'.format(title2))
            #self.light_out(True)
            EditMenu.update_edit_menu(self, self.centre.note.currentIndex())
            self.centre.note.currentWidget().editor.setFocus()
            self.centre.left.left_tab.b.openGL.processor = \
                self.centre.note.currentWidget().highlight.reversal_post_processor #update current processor

        else:
            self.setWindowTitle('EZ machining')
            EditMenu.update_edit_menu(self, self.centre.note.currentIndex())
            #self.light_out(False)

    #def light_out(self, gamlet):
    #    self.saveAction.setEnabled(gamlet)
    #    self.saveAsAction.setEnabled(gamlet)
    #    self.centre.note.save_tab_button.setEnabled(gamlet)
    #    #self.findAction.setEnabled(gamlet)
    #    self.editMenu.setEnabled(gamlet)
    #    self.BackplotView.setEnabled(gamlet)



    def save_options(self):
        """
        :return: changing exact values of exact names
        """
        name1 = "interface_settings ", " {{'main_width': {}, 'main_height':{} }}".format(self.width(), self.height())
        name2 = "splitter_parameters ", " {{'lefty': {}, 'righty': {}, 'flag': {} }}".format(self.centre.splitter.sizes()[0],
                        self.centre.splitter.sizes()[1], self.splitter_flag)
        name3 = "saved_toolbars ", " {}".format(self.saveState())
        names = [name1, name2, name3]
        print(self.centre.splitter.sizes())

        change_setting.change_settins(names)

        toolbars_plasemnt = self.saveState()
        print('tolbars:', toolbars_plasemnt)
        print('toolbasrs type', type(toolbars_plasemnt))

    def restore_all_options(self):
        shutil.copyfile('../Settings/default_settings.py', 'Settings/settings.py', follow_symlinks=True)

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

    def remeber_start_point(self):
        self.centre.note.currentWidget().editor.start_point = self.centre.note.currentWidget().editor.textCursor().blockNumber()
        #todo
        print('start point:', self.centre.note.currentWidget().editor.start_point)
        # self.centre.note.currentWidget().setMaximumBlockCount(self.max_blocks - self.cur_block)

    def drop_point(self):
        print('dropping point')
        #todo
        #self.centre.note.currentWidget().setMaximumBlockCount(0)

    def customize(self):
        self.custom.show()



