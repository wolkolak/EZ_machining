from PyQt5.QtWidgets import QDialog, QGridLayout, QFrame, QLabel,  QSlider, QScrollBar, QDial, QPushButton,\
    QLineEdit, QTreeWidget, QTreeWidgetItem, QComboBox, QCheckBox, QSlider, QScrollArea
from PyQt5 import QtCore, QtGui
from left_zone.additional_functions import read_tool_file
from Gui.little_gui_classes import validate_text_digit
from Gui.gui_classes import simple_warning
from os import walk
from Settings.change_setting import change_file_vars
import importlib, shutil


class OptionsQTWItem(QTreeWidgetItem):
    def __init__(self, text, widget_to_show):
        print('OptionsQTWItem.text = ', text)
        super().__init__(text)
        self.widget_to_show = widget_to_show


class ToolCatalog(QComboBox):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.address = father.tool_folder
        self.setFixedSize(180, 40)
        tree = walk(self.address)
        print('tree = ', tree)
        first_ = next(tree)[1]
        for tr in first_:
            if tr != 'tool_pics' and tr != '__pycache__':
                #print('catalog = ', tr)
                self.addItem(tr)
        self.currentIndexChanged.connect(self.ololo)

    def ololo(self):
        #print('self.currentText() = ', self.currentText())
        self.father.tree.tool_folder = "Modelling_clay\machine_tools\\" + self.currentText()
        #print('FOLDER = ', self.father.tool_folder)
        self.father.tree.update_tree()




class TreeTools(QTreeWidget):
    def __init__(self, father):
        super().__init__()
        self.father = father
        print('ПРоизошёл TreeTool init')
        self.setMinimumSize(500, 300)
        self.setHeaderLabel('')
        self.tool_folder = "Modelling_clay\machine_tools\\" + self.father.tool_catalog.currentText()
        self.dir_dict = {}
        self.update_tree()
        self.currentItemChanged.connect(self.accept_blinking)


    def accept_blinking(self, new):
        if new is None or new.my_type != 'file':
            self.father.edit_tool.setEnabled(False)
        else:
            self.father.edit_tool.setEnabled(True)

    def update_tree(self):
        self.clear()
        print('self.tool_folder = ', self.tool_folder)
        tree = walk(self.tool_folder)
        self.dir_dict = {}
        for tre in tree:
            address = tre[0]
            if address.endswith('__pycache__'):
                continue
            for tr in tre[1]:  # folders
                if tr == '__pycache__':
                    continue
                cur_item = OptionsQTWItem([tr], None)
                cur_item.address = address + '\\' + tr
                self.top_or_child(cur_item, self.tool_folder, address)
                cur_item.my_type = 'dir'
                self.dir_dict[address + '\\' + tr] = cur_item
            for tr in tre[2]:  # files
                if tr == '__init__.py':
                    continue
                cur_item = OptionsQTWItem([tr], None)
                cur_item.setIcon(0, QtGui.QIcon('icons/tool.png'))
                cur_item.address = address + '\\' + tr
                self.top_or_child(cur_item, self.tool_folder, address)
                cur_item.my_type = 'file'
                cur_item.setBackground(0, QtGui.QBrush(QtGui.QColor(224, 255, 255)))
                self.dir_dict[address + '\\' + tr] = cur_item
                #print('cur_item.address = ', cur_item.address)

    def tool_accepted(self):
        print('tool_accepted')
        i = self.selectedItems()
        if i:
            item = i[0]
            if item.my_type == 'file':
                ad = item.address
                new_address_slash = ad.replace('\\', '/')  # 'Modelling_clay/Processors/Fanuc_NT'
                names = [['default_tool ', " '{}'".format(new_address_slash)]]
                if self.father.use_by_default_tool.isChecked() is True:
                    change_file_vars('Settings\settings.py', names)
                # todo изменить основной инструмент
                self.father.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.current_tool = ad
                self.father.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.create_tool()



    def top_or_child(self, item, mother_address, new_address):
        if mother_address == new_address:
            self.addTopLevelItem(item)
        else:
            self.dir_dict[new_address].addChild(item)


class Cut_tools_dialog(QDialog):
    def __init__(self, main_inteface, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        print(' Cut_tools_dialog')
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.main_interface = main_inteface
        self.tool_folder = 'Modelling_clay\machine_tools'
        self.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        #self.dir_dict = {}
        self.scene0 = self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL
        grid = QGridLayout()

        self.tool_catalog = ToolCatalog(self)
        grid.addWidget(self.tool_catalog, 0, 0)

        self.new_tool_but = QPushButton('New tool')
        self.new_tool_but.setFixedSize(200, 40)
        grid.addWidget(self.new_tool_but, 0, 2, alignment=QtCore.Qt.AlignRight)
        self.new_tool_but.clicked.connect(self.start_new_tool)

        self.tree = TreeTools(self)
        grid.addWidget(self.tree, 1, 0, 1, 3)

        self.edit_tool = QPushButton('Edit tool')
        self.edit_tool.setFixedSize(200, 40)
        grid.addWidget(self.edit_tool, 2, 0, alignment=QtCore.Qt.AlignLeft)
        self.edit_tool.setEnabled(False)
        self.edit_tool.clicked.connect(self.start_editing)

        self.use_by_default_tool = QCheckBox('Use by\n default')
        self.use_by_default_tool.setFixedWidth(90)
        grid.addWidget(self.use_by_default_tool, 2, 1, alignment=QtCore.Qt.AlignRight)

        self.accept_but = QPushButton('Accept tool')
        self.accept_but.clicked.connect(self.tree.tool_accepted)
        self.accept_but.setFixedSize(200, 40)
        grid.addWidget(self.accept_but, 2, 2, alignment=QtCore.Qt.AlignRight)

        self.setLayout(grid)
        self.setFixedSize(550, 450)
        self.setWindowTitle('Cut tools dialog')

    def start_new_tool(self):
        g = GiveToolName(self)
        g.exec()

    #todo function to change tool?
    def start_editing(self):#, ok_window=False
        g = Edit_tools_dialog(self.main_interface, self)
        g.exec()

class GiveToolName(QDialog):
    def __init__(self, mother, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mother = mother
        self.setFixedSize(195, 128)
        self.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        self.lbl = QLabel("New tool name:")
        self.lbl.setFixedSize(150, 36)
        self.new_name = QLineEdit('')
        self.new_name.setFixedSize(150, 36)
        self.but = QPushButton('Ok')
        self.but.setFixedSize(150, 36)
        grid = QGridLayout()
        grid.addWidget(self.lbl, 0, 0)
        grid.addWidget(self.new_name, 1, 0)
        grid.addWidget(self.but, 2, 0)
        self.setLayout(grid)
        self.but.clicked.connect(self.OK_func)

    def OK_func(self):
        address = self.mother.tree.tool_folder + '\\' + self.new_name.text() + '.txt'
        print('address = ', address)
        if self.mother.tree.currentItem() is None:
            example = self.mother.tree.itemAt(0, 0)#if None than message "You need at least one tool in folder"
        else:
            example = self.mother.tree.currentItem()
        print('ТААААК = ', type(example))
        shutil.copyfile(example.address, address)
        #todo обновить экран
        self.mother.tree.update_tree()
        #todo указать новый элемент
        for name in self.mother.tree.dir_dict:
            if address == name:
                self.mother.tree.setCurrentItem(self.mother.tree.dir_dict[name])
                break
        self.mother.start_editing()
        self.close()



class Edit_tools_dialog(QDialog):
    def __init__(self, main_inteface, tool_dialog, *args, **kwargs):
        super().__init__(main_inteface, *args, **kwargs)
        self.tool_dialog = tool_dialog
        self.main_interface = main_inteface
        w, h = 550, 650
        #self.setFixedSize(w*2, h)
        self.cur_tool = self.tool_dialog.tree.currentItem()
        self.dict_tool = read_tool_file(self.cur_tool.address)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        grid = QGridLayout()
        self.setLayout(grid)
        print('cur_tool == ', self.cur_tool.address)
        self.picture = QLabel()
        self.picture.setFixedSize(w, h)
        address = "Modelling_clay//machine_tools//tool_pics//" + self.dict_tool['PIC']
        self.picture.setPixmap(QtGui.QPixmap(address).scaled(w, h, QtCore.Qt.KeepAspectRatio))
        grid.addWidget(self.picture, 0, 0)

        self.r_side = R_Side(self)
        grid.addWidget(self.r_side, 0, 1, 1, 2)

        self.check_but = QPushButton('Check')
        self.check_but.setFixedSize(100, 45)
        self.check_but.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        grid.addWidget(self.check_but, 2, 1, alignment=QtCore.Qt.AlignBottom)
        self.check_but.clicked.connect(self.check_tools_param)

        self.accept_but = QPushButton('Accept')
        self.accept_but.setFixedSize(100, 45)
        self.accept_but.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        grid.addWidget(self.accept_but, 2, 2, alignment=QtCore.Qt.AlignBottom)
        self.accept_but.clicked.connect(self.accept_tool_change)

        name = self.tool_dialog.tree.currentItem().address
        name_l = name.split('\\')
        name = name_l[-1]
        self.name_lbl = QLabel(name)
        self.name_lbl.setFixedSize(400, 45)
        self.name_lbl.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        grid.addWidget(self.name_lbl, 2, 0, alignment=QtCore.Qt.AlignBottom)

    def accept_tool_change(self):
        problem_keys = self.check_tools_param()
        if len(problem_keys) == 0:
            split = "="
            replacement = ""
            for i_ in self.dict_tool:
                replacement = replacement + '{}{}{}\n'.format(i_, split, str(self.dict_tool[i_]))
            with open(self.cur_tool.address, 'w') as f:
                f.write(replacement)
            self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL.create_tool()



    def check_tools_param(self):
        str1 = "Modelling_clay.machine_tools." + self.dict_tool['TYPE'] + ".__init__"
        module_real = importlib.import_module(str1)
        tool_check_func = module_real.tool_check

        for j in self.r_side.dict_blocks:
            self.r_side.dict_blocks[j].val.setStyleSheet("color: black;")
            v = self.r_side.dict_blocks[j].val.text()
            try:
                v = float(v)
            except:
                if v is None:
                    v = 0
            self.dict_tool[j] = v
        self.dict_tool, problem_keys = tool_check_func(self.dict_tool)
        for j in self.r_side.dict_blocks:
            self.r_side.dict_blocks[j].val.setText(str(self.dict_tool[j]))
        for k in problem_keys:
            self.r_side.dict_blocks[k].val.setStyleSheet("color: red;")
        return problem_keys



class R_Side(QScrollArea):
    def __init__(self, edit_dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_dialog = edit_dialog
        self.setFixedSize(370, 600)
        grid = QGridLayout()
        self.form1 = QFrame()
        self.dict_blocks = {}
        n = 0
        for name in self.edit_dialog.dict_tool:
            value = self.edit_dialog.dict_tool[name]
            self.dict_blocks[name] = Claster_dict(name, value)
            grid.addWidget(self.dict_blocks[name], n, 1, alignment=QtCore.Qt.AlignLeft)
            n = n + 1
        self.form1.setLayout(grid)
        self.setWidget(self.form1)
        print('CHECK')



class Claster_dict(QFrame):
    def __init__(self, name, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('border-width: 2px; black; font-size: 20px;')
        self.setFixedSize(300, 45)
        self.lbl = QLabel(name)
        self.lbl.setFixedSize(150, 25)
        self.val = QLineEdit(str(value))
        self.val.setFixedSize(140, 25)
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.lbl, 0, 0)
        grid.addWidget(self.val, 0, 1)
        if name == 'OVERALL_L':# or name == 'PIC':
            self.val.setEnabled(False)
