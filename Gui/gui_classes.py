from PyQt5.QtWidgets import  QSplitter, QTabWidget, QHBoxLayout, QVBoxLayout, \
    QFrame, QTabBar,  QMessageBox, QFileDialog, QFontDialog, QPushButton, QWidget, QGridLayout, QCheckBox, QSlider, QScrollArea, QLabel, QToolTip
from PyQt5.QtCore import Qt, QPoint
from PyQt5.Qt import QButtonGroup
from left_zone import left_part
from Redactor import redactor
from Settings import change_setting
import Settings.settings as st
from PyQt5 import QtGui
from Gui.little_gui_classes import simple_warning
import numpy as np
import importlib
import sys
from PyQt5 import QtCore




class My_Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(st.font3)

class coloredTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(st.font2)




class MyOpenDialog(QWidget):
    """В данный момент не используется - можно выкинуть или допилить, заменив окно открцытия файлов"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.options = QFileDialog.DontUseNativeDialog
        self.remember_directory = QCheckBox('Remember that directory')
        #self.setMaximumSize(1111,1111)
        grid = QGridLayout()
        self.setLayout(grid)

        #self.self.layout().addWidget(self.remember_directory)
        #print('niheraaaaaaaaaaa', self.layout)
        #grid = QGridLayout()
        #grid.addWidget(self.remember_directory, 5, 5)
        #self.setLayout(grid)
        #self.remember_directory.setParent(self)
        #self.remember_directory.show()


class Tabs(QTabWidget):
    current_files = []
    filter_files = "Text files (*.txt);;MasterCAM legacy (*.nc);;Siemens Main (*.mpf);;Siemens Sub (*.spf);;Fanuc (*.p-1);;All files (*.*)"
    file_formats = [filter_files.split(';;')]
    ff = file_formats[0][0]
    ff = ff[ff.rindex('*') + 1:-1]
    print('format are :', ff)
    quantity = 15
    tabs = [["File" + str(i), None] for i in range(0, quantity)]

    def __init__(self, center_widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('self.default_processor in tabs: ', self.default_processor_address)
        self.colored_tabbar = coloredTabBar()
        self.setTabBar(self.colored_tabbar)
        self.setTabsClosable(True)
        self.setMovable(True)
        self.center_widget = center_widget
        self.little_widget = QFrame()

        little_layout = QHBoxLayout()
        self.little_widget.setLayout(little_layout)
        self.setCornerWidget(self.little_widget)

        self.new_tab_button = My_Button("NEW")
        little_layout.addWidget(self.new_tab_button)
        self.new_tab_button.setStyleSheet("background-color: {}".format(st.color1))
        self.new_tab_button.clicked.connect(self.new_tab)

        self.save_tab_button = My_Button("SAVE")
        little_layout.addWidget(self.save_tab_button )
        self.save_tab_button.setStyleSheet("background-color: {}".format(st.color1))

        self.cornerWidget().setMinimumSize(20, 40)
        self.tabCloseRequested.connect(self.delete_tab)

        #todo унаследовать нормально
        stylesheet = """ 
               QTabBar::tab:selected {background: rgb(145,191,204)}
               QTabWidget>QWidget>QWidget{background: gray;}
               """

        self.setStyleSheet(stylesheet)

    @property
    def default_processor_address(self):
        s = 'Settings.settings'
        if s in sys.modules:
            module = importlib.reload(sys.modules[s])
        else:
            module = importlib.import_module(s)
        print('module.default_processor = ', module.default_processor)
        return module.default_processor


    @property
    def default_machine_item(self):
        s = 'Settings.settings'
        if s in sys.modules:
            print('s in sys.modules')
            module_settings = importlib.reload(sys.modules[s])
            #print('sys.modules[ ] = ', sys.modules)
        #else:
        #    print('s not in sys.modules')
        #    module_settings = importlib.import_module(s)

        default_machine_address = module_settings.default_machine

        #print('default_machine_address = ', default_machine_address)

        str1 = default_machine_address.replace('/', '.') + '.REAL_MACHINE'
        #print('str1 = ', str1)
        if str1 in sys.modules:
            print('ветка обновления')
            module_real = importlib.reload(sys.modules[str1]) #todo ПОМЕНЯТЬ НАЗАД
            #import Modelling_clay.machines.NT6000_Table_C_Head_BA.REAL_MACHINE as module_real
        else:
            print('Ветка импорта')
            print('{{{{{{{{{{{{{ str1 = ', str1)
            module_real = importlib.import_module(str1)
            print('туточки')
            #import Modelling_clay.machines.NT6000_Table_C_Head_BA.REAL_MACHINE as module_real
        #f = open('Modelling_clay/machines/NT6000_Table_C_Head_BA/machine_settings.py')
        #for l in f:
        #    print('fffff = ', l)
        #f.close()

        default_machine_item = module_real.REAL_MACHINE(None)   #None is the father for super().__init__
        #print('default_machine_item dots = ', default_machine_item.machine_zero_variant)
        print('6g54_g59_AXIS = ', default_machine_item.g54_g59_AXIS)
        return default_machine_item

    def after_setting_machine(self):
        #self.main_interface.centre.left.update_visible_np_left()
        #print('after main g cod in text: \n', self.main_interface.centre.note.currentWidget().np_box.main_g_cod_pool)
        #print('after main visible_np_left: \n', self.main_interface.centre.note.currentWidget().np_box.visible_np)

        self.update_machine_processor()

        self.center_widget.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()  # initializeGL()

    #def set_machine_in_default(self, redactor=None, machine_address=None):
    #
    #    if redactor is None:
    #        redactor = self.currentWidget()
    #    if machine_address is None:# не успел собраться
    #        redactor.current_machine = self.default_machine_item
    #    else:



    def set_machine_in_DOC(self, redactor=None, machine_address=None):
        # это может быть запущено только при открытом документе

        print('machine_address - ', machine_address)
        #if redactor is False:
        #    print('redactor is False, return')
        #    return
        #if self.tab_.center_widget.
        if redactor is None:
            redactor = self.currentWidget()
        if machine_address is None:# не успел собраться
            #print('machine_address is None????')
            redactor.current_machine = self.default_machine_item
        else:
            str1 = machine_address.replace('/', '.') + '.REAL_MACHINE'
            module_real = importlib.import_module(str1)
            redactor.current_machine = module_real.REAL_MACHINE(None)
        #self.tab_.center_widget.left.left_tab.b.openGL.machine_model_parts()
        return True

    def delete_tab(self, n):
        name = self.widget(n).editor.existing or self.tabText(n)
        print('tab delete:', name)
        if self.widget(n).editor.changed:
            res = simple_2_dialog(self.save_file, lambda: self.close_only(n), "Save changes in {}?".format(self.tabText(n)))
            if res:
                name = self.widget(n).editor.existing or self.tabText(n)
                self.removeTab(n)
                self.remove_new_name(name)
            else:
                print('tab delete CANCEL')
        else:
            print('111111111')
            self.close_only(n)
            print('222222222222')
            self.removeTab(n)
            if name:
                self.remove_new_name(name)
            print('333333333333333333')

    def close_only(self, n):
        #time.sleep(8)
        if self.widget(n).editor.existing is False:
            for i in range(1, self.quantity - 1):
                if self.tabs[i][0] == self.tabText(n):
                    self.tabs[i][1] = None
                    break
        return True

    def new_tab(self):
        print('tab create')
        i = 1
        while (i < self.quantity-1) & (self.tabs[i][1] is not None):
            i += 1
        if self.tabs[i][1] is None:
            self.tabs[i][1] = True
            print('new tab0')
            self.insertTab(self.currentIndex() + 1, redactor.ParentOfMyEdit(None, existing=False, tab_=self), self.tabs[i][0])
            #gbplf
            #print('self.currentWidget().main_g_cod_pool', self.currentWidget().main_g_cod_pool)
            #self.currentWidget().editor.set_syntax()
            self.setCurrentIndex(self.currentIndex()+1)
            #self.currentWidget().np_box.main_g_cod_pool = np.insert(self.currentWidget().np_box.main_g_cod_pool, 0,
            #                                                 self.currentWidget().np_box.main_g_cod_pool, axis=0)
            self.currentWidget().np_box.propagate_np_box_starting_points()
            self.center_widget.left.update_visible_np_left()
            self.add_new_name(self.tabs[i][0])
            self.currentWidget().np_box.add_line_in_new_tab()
            print('new tab1')
        else:
            simple_warning('warning', "Притормози \n ¯\_(ツ)_/¯")

    def update_machine_processor(self):
        if self.currentIndex() == -1:
            pass
            #saved_processor_address = self.default_processor_address
        else:
            #что то тут почнить
            saved_processor_address = self.currentWidget().current_processor_address
            print('saved_processor_address = ', saved_processor_address)
            self.currentWidget().set_syntax(saved_processor_address)
            #.center_widget.app.centre.note
            self.currentWidget().after_set_syntax()
        #self.center_widget.app. sim_panel.choose_processor_item.after_set_syntax()
        #centre

    def close_all(self):
        i = -1 #we don't want endless close cycle, aren't we?
        while self.currentIndex() != -1 and self.currentIndex() != i:
            i = self.currentIndex()
            self.close_current()

    def close_current(self):
        self.tabCloseRequested.emit(self.currentIndex())
        #self.delete_tab(self.currentIndex())

    def open_file(self):
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        print('QFileDialog.DontUseNativeDialog')
        path, _ = QFileDialog.getOpenFileName(None, "Open file", st.g_programs_folder, self.filter_files)
        if path:
            self.make_open_DRY(path)
            directory_to_remember = path[: path.rindex('/')]
            print('||||| directory_to_remember = ', directory_to_remember)
            names = [['g_programs_folder ', " '{}'".format(directory_to_remember)]]
            #change_setting.change_settins(names)
            address = "Settings/settings.py"
            change_setting.change_file_vars(address, names)


    def save_file_as(self):
        if self.currentIndex() == -1:
            return
        print('saving as')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name_old = st.g_programs_folder + '/' + self.tabText(self.currentIndex())
        name_old_to_remove = self.currentWidget().editor.existing
        if self.currentWidget().editor.existing is False:
            name_old += str(self.ff)
            name_old_to_remove = self.tabText(self.currentIndex())
        path, _ = QFileDialog.getSaveFileName(None, "Save As", name_old, self.filter_files, options=options)
        if _ == '':
            return False
        print('save_file_as, path = {}\n_ = {}'.format(path, _))
        if path in self.current_files:
            simple_warning('Nope, not recommended!', 'File name already \ntaking part in the session')
            return
        if path:
            text = self.currentWidget().editor.toPlainText()
            with open(path, 'w') as file:
                file.write(text)
            self.currentWidget().editor.changed = False
            self.currentWidget().editor.existing = path
            try:
                name_open_file = path[path.rindex('/') + 1:]
            except ValueError:
                name_open_file = path
            self.setTabText(self.currentIndex(), name_open_file)
            self.window().setWindowTitle(path)
            self.remove_new_name(name_old_to_remove) #todo need or not
            self.add_new_name(path)

            directory_to_remember = path[: path.rindex('/')]
            names = [['g_programs_folder ', " '{}'".format(directory_to_remember)]]
            address = "Settings/settings.py"
            change_setting.change_file_vars(address, names)
            return True

    def save_file(self):
        if self.currentWidget() is not None:
            print('||| save_file')
            name_old = st.g_programs_folder + '/' + self.tabText(self.currentIndex())
            print('||| name_old = ', name_old)
            print(self.currentWidget().editor.existing)
            if self.currentWidget().editor.existing is False:
                return self.save_file_as()

            path = self.currentWidget().editor.existing
            if path:
                text = self.currentWidget().editor.toPlainText()
                with open(path, 'w') as file:
                    file.write(text)
                self.currentWidget().editor.changed = False
                print(path)



    def make_open_DRY(self, path):
        if path in self.current_files:
            simple_warning('Nope, not recommended!', 'File name already taking part in session')
            return
        try:
            text = open(path).read()
            try:
                name_open_file = path[path.rindex('/') + 1:]
            except ValueError:
                name_open_file = path

            self.insertTab(self.currentIndex() + 1, redactor.ParentOfMyEdit(text, tab_=self, existing=path), name_open_file)
            #self.currentWidget().editor.set_syntax()
            self.setCurrentIndex(self.currentIndex()+1)
            self.currentWidget().editor.existing = path
            print('|||Open path: ', path)
            self.add_new_name(path)
        except BaseException:
            simple_warning('warning', "У файла формат не тот \n ¯\_(ツ)_/¯ ")




    def add_new_name(self, name):
        self.current_files.append(name)
        print('current_files', self.current_files)

    def remove_new_name(self, name):
        print('11current_files', self.current_files)
        print('name = ', name)
        self.current_files.remove(name)
        print('22current_files', self.current_files)

class right2(QWidget):
    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base = base
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(st.color2))
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        # self.addItem(e.mimeData().text())
        nya = e.mimeData().text()
        nya = nya[8:]
        print(nya)

        self.base.note.make_open_DRY(nya)


class CenterWindow(QWidget):

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        centr_grid = QGridLayout()
        self.setLayout(centr_grid)
        self.setStyleSheet("background-color: gray")

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet('background-color:green')

        centr_grid.addWidget(self.splitter)
        self.note = Tabs(center_widget=self)
        self.left = left_part.left1(self)
        self.splitter.addWidget(self.left)
        self.right = right2(self)
        self.splitter.addWidget(self.right)

        grid_right = QGridLayout()
        self.right.setLayout(grid_right)
        grid_right.addWidget(self.note, 0, 0)

        self.splitter.setSizes([st.splitter_parameters['lefty'], st.splitter_parameters['righty']])

        #self.setAcceptDrops(True)

        #print('drop:', self.acceptDrops())



class m_f_d(QFontDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def my_font_diag():
    pass

def stop_calculations(self):
    print('stop_calculations')
    tabs = self.centre.note
    if tabs.currentIndex() != -1:
        np_box = self.centre.note.currentWidget().np_box
        np_box.visible_np = np_box.main_g_cod_pool.copy()
        if np_box.calcs_ON:
            np_box.calcs_ON = False
            self.calculations_stop.setIcon(QtGui.QIcon('icons/OFF.png'))
            self.view_f.animationMode.edit_panel.Calc_ON_OFF.setIcon(QtGui.QIcon('icons/OFFmin'))#eee type =
        else:
            np_box.calcs_ON = True
            self.calculations_stop.setIcon(QtGui.QIcon('icons/ON.png'))
            self.view_f.animationMode.edit_panel.Calc_ON_OFF.setIcon(QtGui.QIcon('icons/ONmin'))#my_window
            #np_box.redactor.editor.after_rehighlight = True
            #if np_box.after_rehighlight:
            np_box.special_options_applying()
            #np_box.after_rehighlight = True
        np_box.redactor.tab_.center_widget.left.update_visible_np_left()



def simple_2_dialog(func1, func2, title):
   print('simple_2_dialog')
   save_or_throw = QMessageBox()
   save_or_throw.setWindowTitle(title)
   save_or_throw.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
   rez = save_or_throw.exec()
   if rez == QMessageBox.Yes:
       print('false there')
       return func1()
   elif rez == QMessageBox.No:
       print('false here')
       return func2()
   else:
       print('that false')
       return False


class ModeButton(QPushButton):
    def __init__(self, modeWidget, name, number, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.number = number
        self.setCheckable(True)
        self.modeWidget = modeWidget
        #self.function = function
        self.clicked.connect(self.clicked_function)
        self.setStyleSheet("\
                QPushButton { color:white; font-size: 15px;}   \
                QPushButton:checked{ background-color: rgb(60, 180, 60);   border: none;}\
                QPushButton:hover{ background-color: rgb(60, 160, 60); } ")
                #border-color: white; border-style: outset; border-width: 1px
    def clicked_function(self):
        for but in self.modeWidget.box_list:
            but.setChecked(False)
        self.setChecked(True)
        self.modeWidget.active_button = self.number


class ModeButton2(QPushButton):
    def __init__(self, modeWidget, name, number, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.number = number
        self.setCheckable(True)
        self.modeWidget = modeWidget
        self.clicked.connect(self.clicked_function)
        self.setStyleSheet("\
                QPushButton { color:white; font-size: 15px;}   \
                QPushButton:checked{ background-color: rgb(200, 80, 80);  border: none;}\
                QPushButton:hover{ background-color: rgb(160, 80, 80); } ")
    def clicked_function(self):
        for but in self.modeWidget.box_list:
            but.setChecked(False)
        self.setChecked(True)
        self.modeWidget.active_button = self.number

class Button3(ModeButton):
    def __init__(self, modeWidget, name, number, *args, **kwargs):
        super().__init__(modeWidget, name, number, *args, **kwargs)
        self.setStyleSheet("\
                QPushButton { color:white; font-size: 15px;}   \
                QPushButton:checked{ background-color: rgb(80, 80, 80);  border-width: 1px; border-color: white;})")
                #QPushButton:hover{ background-color: grey; border-style: outset; } ")

    def clicked_function(self):
        aim = self.modeWidget.papa_tool_bar.my_window.centre.left.left_tab.parent_of_3d_widget.openGL
        aim.show_intermediate_dots = True if self.isChecked() else False
        print('trakc mode = ', aim.show_intermediate_dots)

class TrackMode(QFrame):
    def __init__(self, tool_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papa_tool_bar = tool_bar
        print('self.papa_tool_bar = ', self.papa_tool_bar)
        self.active_button = 0
        self.box_list = []
        self.all_track_b = self.add_mode('All', 'All tracking\n parts visible', 0)
        #self.all_track_b.clicked(self.all_point_on_off)
        self.dotted_track_b = self.add_mode('Dot', 'Future lines\n are dotted', 1)
        self.from_start_b = self.add_mode('St', 'Future lines\n invisible', 2)
        self.Intermediate_dots = self.add_button('Ark\ndots', 'Intermediate dots', 3)
        #self.Intermediate_dots.clicked.connect(self.all_point_on_off)
        self.layout_ = QGridLayout()
        self.setLayout(self.layout_)
        self.refresh_layout()
        self.all_track_b.setChecked(True)

    #def all_point_on_off(self):
    #    scene = self.papa_tool_bar.my_window.centre.left.left_tab.parent_of_3d_widget.openGL
    #    if self.Intermediate_dots.isChecked():
    #        print('All dots')
    #        scene.draw_points = scene.draw_all_points
    #    else:
    #        print('not all')
    #        scene.draw_points = scene.draw_not_all_points

    def refresh_layout(self):
        list1 = [0, 1, 2, 3]
        list2 = [0, 0, 0, 0]

        if self.papa_tool_bar.orientation() == 2:
            print('refresh_layout22 2 ')
            h = list2; v = list1
            self.layout_.setContentsMargins(0, 10, 0, 10)  # left, top, right, bottom
        else:
            print('refresh_layout11 1')
            #self.setFixedSize(300, 50)
            v = list2; h = list1
            self.layout_.setContentsMargins(10, 0, 10, 0)

        self.layout_.addWidget(self.all_track_b,        v[0], h[0], alignment=QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.dotted_track_b,     v[1], h[1], alignment=QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.from_start_b,       v[2], h[2], alignment=QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.Intermediate_dots,  v[3], h[3], alignment=QtCore.Qt.AlignHCenter)
        #self.field_mode.refresh_ModeField()

    def add_mode(self, name, tip, H):
        foo = ModeButton2(self, name, number=H)
        foo.setFixedSize(40, 25)
        foo.setToolTip(tip)
        self.box_list.append(foo)
        return foo

    def add_button(self, name, tip, H):
        foo = Button3(self, name, number=H)
        foo.setFixedSize(40, 40)
        foo.setToolTip(tip)
        return foo


class VelocitySlider(QSlider):#QSlider
    def __init__(self, Mode_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Mode_bar = Mode_bar
        self.setRange(0, 300)
        self.setValue(100)
        #self.setStyleSheet('QSlider::handle { background: green; height: %1px; width: %1px; margin: 0 -%2px; }')
        self.sliderPressed.connect(lambda: self.value_changed(self.value()))
        self.valueChanged.connect(self.value_changed)

    def value_changed(self, value):
        s = self.mapToGlobal(self.pos())
        my_point = self.moveToolTip(s)
        QToolTip.showText(my_point, '{}%'.format(value))#,self



    def moveToolTip(self, s):
        x, y = s.x(), s.y()
        if self.orientation() == 2:
            x = x - 40
            print('self.maximumHeight = ', self.maximumHeight())
            dY = self.height() * self.value() / self.maximum() - self.height()/2 - 20
            y = y - dY
        else:
            y = y - 10
            dX = self.width() * self.value() / self.maximum() - self.width() / 2 + 20
            x = x + dX
        s2 = QPoint(x, y)
        return s2





class ModeField(QFrame):
    def __init__(self, Mode_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Mode_bar = Mode_bar
        self.k_velocity = VelocitySlider(Mode_bar=Mode_bar)
        self.move_button = QPushButton('M')
        self.move_button.setToolTip('Move')
        self.move_button.setFixedSize(25, 25)
        self.delete_button = QPushButton('D')
        self.delete_button.setToolTip('Delete')
        self.delete_button.setFixedSize(25, 25)
        self.measure_button = QPushButton('Me')
        self.measure_button.setToolTip('Measure')
        self.measure_button.setFixedSize(25, 25)
        #добавить кнопки
        self.mylayout = QGridLayout()
        self.setLayout(self.mylayout)
        self.refresh_ModeField()


    def refresh_ModeField(self):
        if self.Mode_bar.papa_tool_bar.orientation() == 2:
            print('refresh_ModeField = 2')
            self.setFixedSize(40, 200)
            self.k_velocity.setOrientation(Qt.Orientation.Vertical)
            self.mylayout.setHorizontalSpacing(0)
            self.mylayout.setVerticalSpacing(10)
            self.mylayout.setContentsMargins(0, 10, 0, 10)
            self.mylayout.addWidget(self.k_velocity, 0, 0, 3, 1)
            self.mylayout.addWidget(self.move_button, 0, 1, alignment=QtCore.Qt.AlignLeft)
            self.mylayout.addWidget(self.delete_button, 1, 1, alignment=QtCore.Qt.AlignLeft)
            self.mylayout.addWidget(self.measure_button, 2, 1, alignment=QtCore.Qt.AlignLeft)
            #self.mylayout.addWidget(self.track_chooser, 3, )
        else:
            print('refresh_ModeField = 1')
            self.setFixedSize(200, 40)
            self.k_velocity.setOrientation(Qt.Orientation.Horizontal)
            self.mylayout.setHorizontalSpacing(10)
            self.mylayout.setVerticalSpacing(0)
            self.mylayout.setContentsMargins(10, 0, 10, 0)
            self.mylayout.addWidget(self.k_velocity,        1, 0, 1, 3)
            self.mylayout.addWidget(self.move_button,       0, 0, alignment=QtCore.Qt.AlignTop)
            self.mylayout.addWidget(self.delete_button,     0, 1, alignment=QtCore.Qt.AlignTop)
            self.mylayout.addWidget(self.measure_button,    0, 2, alignment=QtCore.Qt.AlignTop)



class ResetButton(QPushButton):
    def __init__(self, tool_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papa_tool_bar = tool_bar
        self.setToolTip('Reset animation')
        self.setIcon(QtGui.QIcon('icons/reset_play.png'))
        self.setStyleSheet("QPushButton { background-color: rgba(255, 255, 255, 0); font-size: 15px;}}")
        self.setFixedSize(40, 40)
        ff = QtCore.QSize(40, 40)
        self.setIconSize(ff)


class PlayButton(QPushButton):
    def __init__(self, tool_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papa_tool_bar = tool_bar
        self.setToolTip('Play/Pause')
        self.setCheckable(True)#QPushButton:checked{ background-color: rgb(80, 80, 80);#background-color: rgba(255, 255, 255, 0);
        self.setStyleSheet("\
                QPushButton { background-color: rgba(255, 255, 255, 0); font-size: 15px;}   \
                QPushButton:checked{ background-color: rgb(80, 80, 80);  border-width: 1px; border-color: white;}\
                QPushButton:hover{ background-color: grey; border-style: outset; } ")
        self.setIcon(QtGui.QIcon('icons/play.png'))
        self.clicked.connect(self.play_click)
        ff = QtCore.QSize(40, 40)
        self.setIconSize(ff)
        self.setFixedSize(40, 40)

    def play_click(self):
        QPushButton.checkStateSet(self)
        if self.isChecked():
            print('isChecked')
            self.setIcon(QtGui.QIcon('icons/pause.png'))
        else:
            print('not Checked')
            self.setIcon(QtGui.QIcon('icons/play.png'))

class EditPanel(QFrame):
    def __init__(self, modes, *args, **kwargs):
        super().__init__(modes, *args, **kwargs)
        self.modes = modes
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        #self.Calc_ON_OFF = self.modes.papa_tool_bar.my_window.calculations_stop


        self.Calc_ON_OFF = QPushButton()
        self.Calc_ON_OFF.setStyleSheet("background-image: url('image.jpg'); border: none;")
        size = QtCore.QSize(40, 40)
        self.Calc_ON_OFF.setIconSize(size)
        #self.Calc_ON_OFF.state = True
        self.Calc_ON_OFF.setIcon(QtGui.QIcon('icons/ONmin'))
        self.Calc_ON_OFF.clicked.connect(self.Calc_ON_OFF_tap)


    def Calc_ON_OFF_tap(self):
        stop_calculations(self.modes.papa_tool_bar.my_window)



class VisualPanel(QFrame):
    def __init__(self, modes, *args, **kwargs):
        super().__init__(modes, *args, **kwargs)
        self.modes = modes
        self.grid = QGridLayout()
        self.setLayout(self.grid)


class AnimationModes(QFrame):
    def __init__(self, tool_bar, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papa_tool_bar = tool_bar
        self.active_button = 0
        self.box_list = []
        self.field_mode = ModeField(self)
        self.edit_mode = self.add_mode('E', 'Edit mode', 0)
        self.edit_mode.clicked.connect(self.edit_mode_on)
        self.verification_mode = self.add_mode('V', 'Verification mode', 2)

        #self.setFixedHeight(1111)
        self.verification_mode.clicked.connect(self.animation_mode_on)
        self.track_chooser = TrackMode(self.papa_tool_bar)
        self.play_simulation = PlayButton(tool_bar=self.papa_tool_bar)
        self.reset_simulation = ResetButton(tool_bar=self.papa_tool_bar)
        self.layout_ = QGridLayout()
        self.edit_panel = EditPanel(self)
        self.visual_panel = VisualPanel(self)
        #self.edit_layout = QGridLayout()

        self.setLayout(self.layout_)

        self.edit_mode.setChecked(True)
        #self.refresh_layout()
        self.edit_mode_on()

    def edit_mode_on(self):#0
        print('edit_mode_on')
        print('active_button = ', self.active_button)
        self.edit_panel.show()
        self.visual_panel.hide()
        self.refresh_layout()

    def animation_mode_on(self):#2
        print('edit_mode_on')
        print('active_button = ', self.active_button)
        self.edit_panel.hide()
        self.visual_panel.show()
        self.refresh_layout()


    def refresh_layout(self):

        print('JJJJ self.papa_tool_bar.orientation() = ', self.papa_tool_bar.orientation())
        list1 = [0, 1, 2, 3, 4, 5]
        list2 = [0, 0, 0, 0, 0, 0]
        if self.papa_tool_bar.orientation() == 2:
            print('refresh_layout 2 ')
            self.setFixedSize(50, 570)
            self.edit_panel.setFixedSize(50, 150)
            self.visual_panel.setFixedSize(50, 150)
            h = list2; v = list1
            self.layout_.setContentsMargins(0, 10, 0, 10)  # left, top, right, bottom
            self.visual_panel.grid.setContentsMargins(0, 10, 0, 10)
            self.edit_panel.grid.setContentsMargins(0, 10, 0, 10)
        else:
            print('refresh_layout 1')
            self.setFixedSize(600, 50)
            self.edit_panel.setFixedSize(150, 50)
            self.visual_panel.setFixedSize(150, 50)
            v = list2; h = list1
            self.layout_.setContentsMargins(10, 0, 10, 0)
            self.visual_panel.grid.setContentsMargins(10, 0, 10, 0)
            self.edit_panel.grid.setContentsMargins(10, 0, 10, 0)
        self.layout_.addWidget(self.edit_mode,          v[0], h[0], alignment=QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.verification_mode,  v[1], h[1], alignment=QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.field_mode,         v[2], h[2], alignment=QtCore.Qt.AlignHCenter)
        #print('self.active_button = ', self.active_button)


        self.layout_.addWidget(self.track_chooser,    v[3], h[3], alignment=QtCore.Qt.AlignHCenter)

        if self.active_button == 2:
            self.layout_.addWidget(self.visual_panel, v[4], h[4], alignment=QtCore.Qt.AlignHCenter)
        elif self.active_button == 0:
            self.layout_.addWidget(self.edit_panel, v[4], h[4], alignment=QtCore.Qt.AlignHCenter)

        self.visual_panel.grid.addWidget(self.play_simulation,  v[0], h[0], alignment=QtCore.Qt.AlignHCenter)
        self.visual_panel.grid.addWidget(self.reset_simulation, v[1], h[1], alignment=QtCore.Qt.AlignHCenter)

        self.edit_panel.grid.addWidget(self.edit_panel.Calc_ON_OFF, v[0], h[0], alignment=QtCore.Qt.AlignHCenter)

        self.field_mode.refresh_ModeField()
        self.track_chooser.refresh_layout()

    def add_mode(self, name, tip, H):
        foo = ModeButton(self, name, number=H)
        foo.setFixedSize(30, 30)
        foo.setToolTip(tip)
        self.box_list.append(foo)
        return foo






