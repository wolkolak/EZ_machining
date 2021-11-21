from PyQt5.QtWidgets import QGridLayout,  QWidget, QTreeWidget, \
    QTreeWidgetItem, QFrame, QLabel, QSizePolicy, QListWidget, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from os import walk
from Gui.gui_classes import simple_warning
from Settings.change_setting import change_settins

class OptionsQTWItem(QTreeWidgetItem):
    def __init__(self, text, widget_to_show):
        super().__init__(text)
        self.widget_to_show = widget_to_show





class MyTree(QTreeWidget):
    def __init__(self, main):
        super().__init__()
        self.setFixedWidth(170)
        self.setMinimumHeight(380)

        #l1 = QTreeWidgetItem(["String A", "String B"])

        #l11 = QTreeWidgetItem(["Podstring A", "Podstring B"])
        #l1.addChild(l11)

        self.simulation = OptionsQTWItem(["Simulation"], main.simulation_panel_item)#???
        self.machine = OptionsQTWItem(["Machine"], main.machine_panel_item)
        self.processor = OptionsQTWItem(["Processor"], main.processor_panel_item)



        #self.addTopLevelItem(l1)

        self.addTopLevelItem(self.simulation)
        self.simulation.addChild(self.machine)
        self.simulation.addChild(self.processor)


class Father_Panel(QFrame):
    def __init__(self):
        super().__init__()
        #self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        #self.setMinimumSize(300, 300)
        self.grid = QGridLayout()

        self.setLayout(self.grid)


class MachinePanel(Father_Panel):
    def __init__(self):
        super().__init__()

        self.lbl = QLabel('another')
        self.grid.addWidget(self.lbl, 0, 0)
        self.lbl1 = QLabel('another')
        self.grid.addWidget(self.lbl1, 0, 1)
        self.hide()

def what_is_here(folder):
    file_names = []
    dir_names = []
    #path_names = []
    for (dirpath, dirnames, filenames) in walk(folder):
        file_names.extend(filenames)
        dir_names.extend(dirnames)
        #path_names.extend(dirpath)
        break
    return file_names, dir_names#, path_names

class TreeProcessor(QTreeWidget):
    def __init__(self, main, sim_panel):
        super().__init__()
        print('ПРоизошёл TreeProcessor init')
        self.currentItemChanged.connect(self.accept_blinking)
        self.sim_panel = sim_panel
        self.setMinimumSize(200, 300)
        self.setHeaderLabel('Processors')
        self.main_interface = main
        self.processor_folder = "Modelling_clay\Processors"
        tree = walk(self.processor_folder)
        self.dir_dict = {}
        for tre in tree:
            adress = tre[0]
            if adress.endswith('__pycache__'):
                continue
            for tr in tre[1]:   # folders
                if tr == '__pycache__':
                    continue
                cur_item = OptionsQTWItem([tr], None)
                cur_item.adress = adress + '\\' + tr
                self.top_or_child(cur_item, self.processor_folder, adress)
                cur_item.my_type = 'dir'
                self.dir_dict[adress + '\\' + tr] = cur_item
            for tr in tre[2]:   # files
                if tr == '__init__.py':
                    continue
                cur_item = OptionsQTWItem([tr], None)
                cur_item.setIcon(0, QtGui.QIcon('icons/processor.png'))
                cur_item.adress = adress + '\\' + tr
                self.top_or_child(cur_item, self.processor_folder, adress)
                cur_item.my_type = 'file'
                cur_item.setBackground(0, QtGui.QBrush(QtGui.QColor(224,255,255)))
                self.dir_dict[adress + '\\' + tr] = cur_item



    def accept_blinking(self, new, previous):
        if new.my_type == 'file':
            self.sim_panel.accept_proc_but.setEnabled(True)
        else:
            self.sim_panel.accept_proc_but.setEnabled(False)

    def processor_accepted(self):
        i = self.selectedItems()
        if i:
            item = i[0]
            if item.my_type == 'file':
                ad = item.adress
                print('ad = ', ad)
                ad_dot = ad.replace('\\', '.')
                new_adress_slash = ad.replace('\\', '/')  # 'Modelling_clay/Processors/Fanuc_NT'
                names = [['default_processor ', " '{}'".format(new_adress_slash)]]

                if self.main_interface.centre.note.currentIndex() == -1:
                    if self.sim_panel.use_by_default_processor.isChecked() is True:
                        change_settins(names)
                        self.main_interface.centre.note.default_processor = ad.replace("\\", "/")
                    else:
                        simple_warning('warning', "Doc for connecting not opened \n and box not checked")
                else:

                    if self.main_interface.centre.note.currentWidget().set_syntax(adress=ad_dot):



                        if self.sim_panel.use_by_default_processor.isChecked() is True:
                            change_settins(names)
                            self.main_interface.centre.note.default_processor = ad.replace("\\", "/")

                    else:
                        simple_warning('warning', "The {} \n is not a processor!".format(ad))

    def after_set_syntax(self):
        self.main_interface.centre.note.currentWidget().refresh_reading_reading_lines_number()
        self.main_interface.centre.note.currentWidget().np_box.__init__(
            self.main_interface.centre.note.currentWidget())
        self.main_interface.centre.note.currentWidget().editor.creating_np_pool()
        self.main_interface.centre.note.currentWidget().editor.arithmetic_ones()
        self.main_interface.centre.note.currentWidget().np_box.start_point()
        print('bigCast: Обнулил ', self.main_interface.centre.note.currentWidget().np_box.visible_np)

    def top_or_child(self, item, mother_adress, new_adress):
        if mother_adress == new_adress:
            self.addTopLevelItem(item)
        else:
            #print('top_or_child has adress ', self.dir_dict)
            self.dir_dict[new_adress].addChild(item)








class TreeMachine(QTreeWidget):
    def __init__(self, main, sim_panel):
        super().__init__()
        print('ПРоизошёл TreeMachine init')
        self.currentItemChanged.connect(self.accept_blinking)
        self.sim_panel = sim_panel
        self.setMinimumSize(200, 300)
        self.setHeaderLabel('Machines')
        self.main_interface = main
        self.processor_folder = "Modelling_clay\machines"
        tree = walk(self.processor_folder)
        self.dir_dict = {}
        print(' tree ==== ',  tree)

        for tre in tree:
            print('tre ====', tre)
            adress = tre[0]
            print('adress = ', adress)
            if adress.endswith('__pycache__'):
                continue
            print('tre[1] = ', tre[1])
            for tr in tre[1]:   # folders
                print('tr here: ', tr)
                if tr == '__pycache__':
                    print('leave __pycache__')
                    continue
                cur_item = OptionsQTWItem([tr], None)

                print('cur_item = ', tr)
                cur_item.adress = adress + '\\' + tr
                self.top_or_child(cur_item, self.processor_folder, adress)
                cur_item.my_type = 'dir'
                cur_item.two_file = 0
                self.dir_dict[adress + '\\' + tr] = cur_item
            print('разделитель')

            for tr in tre[2]:   # files
                if adress == self.processor_folder:
                    continue
                if tr == '__init__.py':
                    continue
                if tr == 'REAL_MACHINE.py':
                    self.dir_dict[adress].two_file = self.dir_dict[adress].two_file + 1
                if tr == 'machine_settings.py':
                    self.dir_dict[adress].two_file = self.dir_dict[adress].two_file + 1

                if self.dir_dict[adress].two_file == 2:
                    cur_item = self.dir_dict[adress]
                    cur_item.my_type = 'machine'
                    cur_item.setIcon(0, QtGui.QIcon('icons/machine_.png'))
                    cur_item.setBackground(0, QtGui.QBrush(QtGui.QColor(224, 255, 255)))


    def machine_accepted(self):
        i = self.selectedItems()
        if i:
            item = i[0]
            if item.my_type == 'machine':

                ad = item.adress
                print('ad = ', ad)
                ad_dot = ad.replace('\\', '.')
                new_adress_slash = ad.replace('\\', '/')  # 'Modelling_clay/Processors/Fanuc_NT'
                names = [['default_machine ', " '{}'".format(new_adress_slash)]]

                if self.main_interface.centre.note.currentIndex() == -1:
                    if self.sim_panel.use_by_default_machine.isChecked():# is True
                        change_settins(names)
                    else:
                       simple_warning('warning', "Doc for connecting not opened \n and box not checked")
                else:
                    if self.main_interface.centre.note.currentWidget().set_machine(address=ad_dot):
                        saved_processor_address = self.main_interface.centre.note.currentWidget().current_processor_address
                        self.main_interface.centre.note.currentWidget().set_syntax(saved_processor_address)
                        self.sim_panel.choose_processor_item.after_set_syntax()
                        if self.sim_panel.use_by_default_machine.isChecked():
                            change_settins(names)



    def accept_blinking(self, new, previous):
        if new.my_type == 'machine':
            self.sim_panel.accept_machine_but.setEnabled(True)
        else:
            self.sim_panel.accept_machine_but.setEnabled(False)


    def top_or_child(self, item, mother_adress, new_adress):
        if mother_adress == new_adress:
            self.addTopLevelItem(item)
        else:
            self.dir_dict[new_adress].addChild(item)



class SimulationPanel(Father_Panel):
    def __init__(self, main):
        super().__init__()

        self.choose_machine_item = TreeMachine(main, self)
        self.grid.addWidget(self.choose_machine_item, 0, 0, 1, 2)

        self.accept_machine_but = QPushButton('Accept \n Machine')
        self.accept_machine_but.setEnabled(False)
        self.accept_machine_but.setMinimumWidth(110)
        self.accept_machine_but.clicked.connect(self.choose_machine_item.machine_accepted)
        self.grid.addWidget(self.accept_machine_but, 1, 0)

        self.use_by_default_machine = QCheckBox('Use by\n default')
        self.use_by_default_machine.setFixedWidth(80)
        self.grid.addWidget(self.use_by_default_machine, 1, 1)


        self.choose_processor_item = TreeProcessor(main, self)
        self.grid.addWidget(self.choose_processor_item, 0, 2, 1, 2)

        self.accept_proc_but = QPushButton('Accept \n Processor')
        self.accept_proc_but.setEnabled(False)
        self.accept_proc_but.setMinimumWidth(110)
        self.accept_proc_but.clicked.connect(self.choose_processor_item.processor_accepted)
        self.grid.addWidget(self.accept_proc_but, 1, 2)

        self.use_by_default_processor = QCheckBox('Use by\n default')
        self.use_by_default_processor.setFixedWidth(80)
        self.grid.addWidget(self.use_by_default_processor, 1, 3)

        #self.lbl.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))

class ProcessorPanel(Father_Panel):
    def __init__(self):
        super().__init__()
        self.lbl = QLabel('processor panel')
        self.grid.addWidget(self.lbl, 0, 0)
        self.hide()


class BigCustomizer(QWidget):
    def __init__(self, main):
        super().__init__()
        self.resize(800, 400)
        self.current_element = None

        self.setWindowTitle('Options')
        grid = QGridLayout()
        self.setLayout(grid)
        self._main = main

        self.machine_panel_item = MachinePanel()
        self.processor_panel_item = ProcessorPanel()
        self.simulation_panel_item = SimulationPanel(main)
#
        self.SettingsTree = MyTree(self)

        self.setStyleSheet(
            'background-color: rgb(55, 255 255); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;')
        self.SettingsTree.itemSelectionChanged.connect(lambda: self.show_options(self.SettingsTree.currentItem().widget_to_show))
        #grid.addWidget(self.options_field, 0, 1, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        grid.addWidget(self.SettingsTree, 0, 0)
        grid.addWidget(self.processor_panel_item, 0, 1)
        grid.addWidget(self.machine_panel_item, 0, 1)
        grid.addWidget(self.simulation_panel_item, 0, 1)


        #self.test = QFrame()
        #grid.addWidget(self.test, 0, 0)

    def show_options(self, point):
        if self.current_element:
            self.current_element.hide()
        else:
            print('loh')
        self.current_element = point
        print('self = ', self)
        if self.current_element is not None:
            self.current_element.show()



