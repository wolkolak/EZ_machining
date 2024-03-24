from PyQt5.QtWidgets import QGridLayout,  QWidget, QTreeWidget, \
    QTreeWidgetItem, QFrame, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui
from os import walk
from Gui.gui_classes import simple_warning
from Gui.machine_options.tools_machine import MachineTab
from Settings.change_setting import change_file_vars

class OptionsQTWItem(QTreeWidgetItem):
    def __init__(self, text, widget_to_show):
        super().__init__(text)
        self.widget_to_show = widget_to_show

class MyTree(QTreeWidget):
    def __init__(self, main):
        super().__init__()
        self.setFixedWidth(170)
        self.setMinimumHeight(380)
        self.setHeaderHidden(True)
        self.bigcustom = main
        self.simulation = OptionsQTWItem(["Simulation"], main.simulation_panel_item)#???
        self.machine = OptionsQTWItem(["Machine"], main.machine_panel_item)
        self.processor = OptionsQTWItem(["Processor"], main.processor_panel_item)
        self.addTopLevelItem(self.simulation)
        self.simulation.addChild(self.machine)
        self.simulation.addChild(self.processor)
        self.expandAll()

    def refresh_tree_bot_levels(self):
        #следующий вопрос - проверить всегда ли изменения куда надо записываются
        self.simulation.removeChild(self.machine)
        self.simulation.removeChild(self.processor)

        self.bigcustom.machine_panel_item = MachinePanel(main_interface=self.bigcustom._main, bigcustom=self.bigcustom)
        self.bigcustom.grid.addWidget(self.bigcustom.machine_panel_item, 0, 1)

        self.bigcustom.processor_panel_item = ProcessorPanel(main_interface=self.bigcustom._main, bigcustom=self.bigcustom)
        self.bigcustom.grid.addWidget(self.bigcustom.processor_panel_item, 0, 1)

        self.machine = OptionsQTWItem(["Machine"], self.bigcustom.machine_panel_item)
        self.processor = OptionsQTWItem(["Processor"], self.bigcustom.processor_panel_item)#todo Не пересобирал ещё

        self.simulation.addChild(self.machine)
        self.simulation.addChild(self.processor)





class Father_Panel(QFrame):
    def __init__(self):
        super().__init__()
        self.grid = QGridLayout()
        self.setLayout(self.grid)


class MachinePanel(Father_Panel):
    def __init__(self, main_interface, bigcustom):#, *args, **kwargs
        super().__init__()
        print('Creating machine dialog')
        self.bigcustom = bigcustom
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_interface = main_interface
        self.machine = self.take_machine()
        self.scene0 = self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL
        self.machine_options = MachineTab(self)
        self.grid.addWidget(self.machine_options, 0, 0)
        self.hide()

    def take_machine(self):
        if self.main_interface.centre.note.currentIndex() == -1:
            print('default_machine_item = ', self.main_interface.centre.note.default_machine_item)
            machine = self.main_interface.centre.note.default_machine_item
        else:
            print('||| current_machine = ', self.main_interface.centre.note.currentWidget().current_machine)
            machine = self.main_interface.centre.note.currentWidget().current_machine
        return machine


def what_is_here(folder):
    file_names = []
    dir_names = []
    for (dirpath, dirnames, filenames) in walk(folder):
        file_names.extend(filenames)
        dir_names.extend(dirnames)
        break
    return file_names, dir_names#, path_names

class TreeProcessor(QTreeWidget):
    def __init__(self, main, sim_panel):
        super().__init__()
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
                cur_item.setBackground(0, QtGui.QBrush(QtGui.QColor(224, 255, 255)))
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
                ad = item.adress                #dsfs
                ad_dot = ad.replace('\\', '/')
                new_adress_slash = ad.replace('\\', '/')  # 'Modelling_clay/Processors/Fanuc_NT'
                names = [['default_processor ', " '{}'".format(new_adress_slash)]]

                if self.main_interface.centre.note.currentIndex() == -1:
                    if self.sim_panel.use_by_default_processor.isChecked() is True:
                        change_file_vars('Settings\settings.py', names)
                        self.main_interface.st_bar.set_permanent_part()
                    else:
                        simple_warning('warning', "Doc for connecting not opened \n and box not checked")
                else:
                    if self.main_interface.centre.note.currentWidget().set_syntax(adress=ad_dot):#, l = 'change proc'     ad_dot
                        #self.main_interface.centre.note.currentWidget().editor.processor_change_toggle = True
                        self.main_interface.centre.note.currentWidget().after_set_syntax()
                        print('processor_accepted')
                        if self.sim_panel.use_by_default_processor.isChecked() is True:
                            change_file_vars('Settings\settings.py', names)
                            #print('self.main_interface.centre.note.default_processor_address = ', self.main_interface.centre.note.default_processor_address)
                            #print('ad = ', ad.replace("\\", "/"))
                            print('default_processor_address = ', self.main_interface.centre.note.default_processor_address)
                            #у текущего сделать обновление данных
                            #self.main_interface.centre.note.default_processor_address = ad.replace("\\", "/")#default_processor_address - property.
                    else:
                        simple_warning('warning', "The {} \n is not a processor!".format(ad))
                    print('хайлайты позже')

    def top_or_child(self, item, mother_adress, new_adress):
        if mother_adress == new_adress:
            self.addTopLevelItem(item)
        else:
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
        self.machine_folder = "Modelling_clay\machines"
        tree = walk(self.machine_folder)#todo processor&&&???!!
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
                self.top_or_child(cur_item, self.machine_folder, adress)
                cur_item.my_type = 'dir'
                cur_item.two_file = 0
                self.dir_dict[adress + '\\' + tr] = cur_item
            print('разделитель')

            for tr in tre[2]:   # files
                if adress == self.machine_folder:
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
        print('Start machine accepted')
        #print(self.main_interface.custom)
        #machine_panel_item = self.main_interface.custom.machine_panel_item
        #print('machine panel === 1', machine_panel_item)
        #print('before main g cod in text: \n', self.main_interface.centre.note.currentWidget().np_box.main_g_cod_pool)
        #print('before main visible_np_left: \n', self.main_interface.centre.note.currentWidget().np_box.visible_np)
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
                        change_file_vars('Settings\settings.py', names)
                        #self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.machine_model_parts()
                        #self.main_interface.st_bar.set_permanent_part()
                        bigcustom = self.sim_panel.bigcustom
                        bigcustom.SettingsTree.refresh_tree_bot_levels()
                        #bigcustom.update_scene_machine()
                        self.main_interface.centre.note.after_setting_machine()#
                    else:
                       simple_warning('warning', "Doc for connecting not opened \n and box not checked")
                else:
                    print('set_machine_in_DOC from bigCustomizer')
                    if self.main_interface.centre.note.set_machine_in_DOC(machine_address=ad_dot):
                        self.main_interface.centre.note.after_setting_machine()
                        if self.sim_panel.use_by_default_machine.isChecked():#todo Тут иногда вышиабет, говорит что объект удален уже
                            change_file_vars('Settings\settings.py', names)
                            self.main_interface.st_bar.set_permanent_part()
                    bigcustom = self.sim_panel.bigcustom
                    bigcustom.SettingsTree.refresh_tree_bot_levels()
                    #bigcustom.update_scene_machine()
                print('в какой момент')
                #self.main_interface.centre.note.currentWidget().editor.after_rehighlight = False#TODO True
                #machine_panel_item = self.sim_panel.bigcustom
                #print('machine panel 2=== ', machine_panel_item)

                #self.sim_panel.bigcustom.grid.addWidget(self.sim_panel.bigcustom.machine_panel_item, 0, 1)

                #todo поднят в  условие


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
    def __init__(self, main, bigcustom):
        super().__init__()
        #print('Simulation panel:', Father_Panel)
        self.bigcustom = bigcustom
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


class ProcessorPanel(Father_Panel):
    def __init__(self, main_interface, bigcustom):
        super().__init__()
        self.main_interface = main_interface
        self.bigcustom = bigcustom
        self.lbl = QLabel('processor panel')
        self.grid.addWidget(self.lbl, 0, 0)
        self.hide()



class BigCustomizer(QWidget):
    def __init__(self, main):
        super().__init__()
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.resize(800, 400)
        self.current_element = None

        self.setWindowTitle('Options')
        self.grid = QGridLayout()
        self.setLayout( self.grid)
        self._main = main

        self.machine_panel_item = MachinePanel(main_interface=main, bigcustom=self)#а себя???
        self.processor_panel_item = ProcessorPanel(main_interface=main, bigcustom=self)
        self.simulation_panel_item = SimulationPanel(main, self)
#
        self.SettingsTree = MyTree(self)

        self.setStyleSheet(
            'background-color: rgb(55, 255 255); border-width: 2px; border-color: black; font-size: 15px;')
        #'background-color: rgb(55, 255 255); border-style: outset; border-width: 2px; border-color: black; font-size: 15px;'

        self.SettingsTree.itemSelectionChanged.connect(lambda: self.show_options(self.SettingsTree.currentItem().widget_to_show))
        self.grid.addWidget(self.SettingsTree, 0, 0)
        self.grid.addWidget(self.processor_panel_item, 0, 1)
        self.grid.addWidget(self.machine_panel_item, 0, 1)
        self.grid.addWidget(self.simulation_panel_item, 0, 1)
        if self._main.centre.note.currentIndex() == -1:
            print('self._main.st_bar.current_machine_address looks like that: ',
                  self._main.centre.note.default_machine_item.last_name)
            print('self._main.st_bar.current_processor_address = ', self._main.st_bar.current_processor_address)
            self.chooser_machine_and_processor(self._main.st_bar.current_machine_address, self._main.st_bar.current_processor_address)
        else:
            print('self._main.st_bar.current_machine_address looks like that: ', self._main.centre.note.currentWidget().current_machine.last_name)
            print('self._main.st_bar.current_processor_address = ', self._main.st_bar.current_processor_address)
            #############

            #self.current_processor_address = address_processor.replace('/', '\\')  # FINE
            #dot = self.current_processor_address.rfind('.')
            #last_sep = self.current_processor_address.rfind('\\')
            ## print('self.current_processor_address[last_sep+1:dot] = ', self.current_processor_address[last_sep+1:])
            #self.current_processor_viewed.setText('P default: ' + self.current_processor_address[last_sep + 1:])  # do

            #############
            self.chooser_machine_and_processor(self._main.st_bar.current_machine_address, self._main.st_bar.current_processor_address)
        self.current_element = self.simulation_panel_item
#
    #def update_scene_machine_params(self):
    #    print('update_scene_machine_params')
    #    self.update_scene_machine()

    def update_scene_machine(self):
        print('update_scene_machine')
        no_tab_opened = True if self._main.centre.note.currentIndex() == -1 else False
        if no_tab_opened:
            m = self._main.centre.note.default_machine_item
            redactor = None
        else:
            m = self._main.centre.note.currentWidget().current_machine
            redactor = self._main.centre.note.currentWidget()
        m.__init__(father=redactor)
        note = self._main.centre.note
        count = note.count()
        for i in range(count):
            mach = note.widget(i).current_machine
            if mach.full_name == m.full_name:
                note.widget(i).current_machine = m
        #todo если при перелистывании станок собирается заново то достаточно
        self._main.centre.note.after_setting_machine()


    def chooser_machine_and_processor(self, machine_address:str, processor_address:str):
        #try:

        #main_directory = str(os.getcwdb())
        #main_directory = main_directory[2:-1]
#
        #machine_address = machine_address[1:]
        #machine_address = machine_address.replace('\\', '\\\\')
        #index = machine_address.rfind('\\')
        #machine_address = machine_address[len(main_directory) + 1: index-1]

        #print('parents dir: ', main_directory)
#
        #print('machine_address in chooser = ', machine_address)
        print('self.simulation_panel_item.choose_machine_item.dir_dict = ', self.simulation_panel_item.choose_machine_item.dir_dict)
        machine_current_item = self.simulation_panel_item.choose_machine_item.dir_dict[machine_address]
        machine_current_item.setSelected(True)
        print('DICT = ', self.simulation_panel_item.choose_processor_item.dir_dict)
        if not processor_address.endswith('.py'):
            processor_address = processor_address + '.py'
        print('HERE 55555: ', self.simulation_panel_item.choose_processor_item.dir_dict)
        print('HERE 55556: ', processor_address)
        processor_current_item = self.simulation_panel_item.choose_processor_item.dir_dict[processor_address]
        processor_current_item.setSelected(True)
        #processor_address = processor_address[3:]

        #print('processor_address =', processor_address)

        #except:
        #    print('Log: remembered machine or processor is not found')

    def show_options(self, point):
        print('show correspond widget')
        print('previous = ', self.current_element)
        print('new = ', point)

        if self.current_element:
            self.current_element.hide()
        else:
            print('loh')
        self.current_element = point
        print('self = ', self)
        if self.current_element is not None:
            self.current_element.show()



