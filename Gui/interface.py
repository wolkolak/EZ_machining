from PyQt5.QtWidgets import QMainWindow, QToolBar, QStatusBar, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from Gui import gui_classes, MyViewToolBar, MyTxtToolBar, test_button
#MyTxtToolBar, MyViewToolBar,gui_classes
import shutil
import sys
from Menus import EditMenu, FileMenu, ViewMenu, OptionsMenu, ToolsMenu, ImportMenu
from Settings import bigCustomizer, change_setting, settings
from Gui.Default_machine_syntax import DefaultReference
import os
#from Gui import test_button
from Gui.little_gui_classes import simple_warning

def take_between_hooks(line, hook):
    """

    :param line: line with hooks desirable
    :return: line between hooks
    """
    needed_line = False
    n_start = line.find(hook)
    if n_start != -1:
        n_start = n_start + 1
        n_end = line.find(hook, n_start)
        if n_end != -1:
            needed_line = line[n_start:n_end]
            print('needed_line = ', needed_line)
    return needed_line


class MyStatusBar(QStatusBar):
    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        self.current_processor_viewed = QPushButton()
        self.current_processor_viewed.clicked.connect(self.obertka_open_option)
        self.current_machine_viewed = QPushButton()
        self.current_machine_viewed.clicked.connect(self.obertka_open_option)
        #self.current_processor_viewed.setFixedSize(100, 100)
        self.set_permanent_part()
        self.addPermanentWidget(self.current_machine_viewed, 0)
        self.addPermanentWidget(self.current_processor_viewed, 0)


    def obertka_open_option(self):
        self.app.customize()

    def set_permanent_part(self):
        #todo сюда заложить адреса для диалога станков и процессоров but we need to choose an object(((
        #current_machine_name = 'machine100500'
        main_directory = str(os.getcwdb())
        main_directory = main_directory[2:-1]
        main_directory = main_directory.replace('\\\\', '\\')

        if self.app.centre.note.currentIndex() == -1:
            self.current_machine_viewed.setText('M default: ' + self.app.centre.note.default_machine_item.last_name)
            #machine
            address_machine:str = self.app.centre.note.default_machine_item.full_name
            address_machine = address_machine[len(main_directory)+1:]
            index = address_machine.rfind('\\')
            address_machine = address_machine[:index]
            self.current_machine_address = address_machine

            #processor
            address_processor = self.app.centre.note.default_processor_address#&&&&??????
            self.current_processor_address = address_processor.replace('/', '\\')#FINE
            dot = self.current_processor_address.rfind('.')
            last_sep = self.current_processor_address.rfind('\\')
            #print('self.current_processor_address[last_sep+1:dot] = ', self.current_processor_address[last_sep+1:])
            self.current_processor_viewed.setText('P default: ' + self.current_processor_address[last_sep+1:])#dot
        else:
            current_machine_name = self.app.centre.note.currentWidget().current_machine.last_name
            address_machine:str = self.app.centre.note.currentWidget().current_machine.full_name
            address_machine = address_machine[len(main_directory)+1:]
            index = address_machine.rfind('\\')
            address_machine = address_machine[:index]
            self.current_machine_address = address_machine
            self.current_machine_viewed.setText('M: ' + current_machine_name)

            #processor
            address_processor = self.app.centre.note.currentWidget().current_processor_address#&&&&??????
            self.current_processor_address = address_processor.replace('/', '\\')#FINE
            last_sep = self.current_processor_address.rfind('\\')
            self.current_processor_viewed.setText('P: ' + self.current_processor_address[last_sep+1:])


        print('in set_permanent_part proc: ', self.current_processor_address)
        print('in set_permanent_part machine: ', self.current_machine_address)


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        print('main window started')
        path = os.getcwd() + '\icons\main icon.png'
        self.setWindowIcon(QtGui.QIcon(path))
        #tray_icon = QtGui.Tra
        self.splitter_flag = settings.splitter_parameters['flag']
        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings.interface_settings['main_width'], settings.interface_settings['main_height'])
        self.centre = gui_classes.CenterWindow(self)
        self.setCentralWidget(self.centre)
        self.st_bar = MyStatusBar(self)
        self.setStatusBar(self.st_bar)
        self.menubar = self.menuBar()
        #self.default_reference = DefaultReference()#todo ввёл специальный класс для этого и забыл. Лежит до рефакторинга
        #file
        FileMenu.file_open(self)
        #Edit
        EditMenu.edit_opt(self)
        #View
        ViewMenu.view_opt(self)
        #Tools
        ToolsMenu.tools_menu_opt(self)
        #self.toolsMenu = self.menubar.addMenu('&Tools')

        #self.inportMenu = self.menubar.addMenu('&Import')
        ImportMenu.import_menu_opt(self)


        #options
        OptionsMenu.options(self)
        self.txt_tools = MyTxtToolBar.MyTextToolBar(self)
        self.view_f = MyViewToolBar.MyViewToolBar(self)

        self.centre.note.currentChanged.connect(self.change_tab)
        self.custom = bigCustomizer.BigCustomizer
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
        #self.centre.note.currentWidget().editor.rehighlightNextBlocks()

    def myIter_obertka(self):
        self.centre.note.currentWidget().editor.my_iter()


    def change_tab(self, n):
        print('tab change')
        #suda
        self.st_bar.set_permanent_part()
        if self.centre.note.currentIndex() != -1:
            print('cur index = ', self.centre.note.currentIndex())
            #todo self.centre.note.currentWidget().current_g_cod_pool
            #self.centre.left.left_tab.a.reset_np_array_in_left_field()
            #self.centre.left.reset_np_array_in_left_field()
            calc_ON_OFF = self.centre.note.currentWidget().np_box.calcs_ON
            if calc_ON_OFF:
                self.calculations_stop.setIcon(QtGui.QIcon('icons/ON.png'))
                self.view_f.animationMode.edit_panel.Calc_ON_OFF.setIcon(QtGui.QIcon('icons/ONmin'))#my_window
            else:
                self.calculations_stop.setIcon(QtGui.QIcon('icons/OFF.png'))
                self.view_f.animationMode.edit_panel.Calc_ON_OFF.setIcon(QtGui.QIcon('icons/OFFmin'))#my_window
            self.centre.left.update_visible_np_left()
            if self.centre.note.currentWidget().editor.existing is False:
                title2 = self.centre.note.tabText(n)
            else:
                title2 = self.centre.note.currentWidget().editor.existing
            self.setWindowTitle('EZ machining:  {}'.format(title2))
            #self.light_out(True)
            #self.
            EditMenu.update_edit_menu(self, self.centre.note.currentIndex())
            self.centre.note.currentWidget().editor.setFocus()
            self.centre.left.left_tab.parent_of_3d_widget.openGL.processor = \
                self.centre.note.currentWidget().highlight.reversal_post_processor #update current processor

            #self.centre.left.left_tab.b.openGL.initializeGL()
            #self.centre.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()
        else:
            self.setWindowTitle('EZ machining')
            EditMenu.update_edit_menu(self, self.centre.note.currentIndex())

        self.centre.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()
        #print(f'проверка 99 = {self.centre.note.currentWidget().np_box.main_g_cod_pool}')
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
        address = "Settings/settings.py"
        change_setting.change_file_vars(address, names)

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
        self.custom(self).show()
        #self.custom




