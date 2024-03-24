from PyQt5.QtWidgets import QDialog, QGridLayout, QFrame, QScrollArea, QPlainTextEdit, QTreeWidget, QTreeWidgetItem, QLabel, QPushButton, QLineEdit
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRegularExpression

from os import walk
from Settings.change_setting import change_file_vars, change_any_file_completly
from Gui.gui_classes import simple_warning
from Help.short_help import ShortHelp

class RegisterToolDialog(QDialog):
    def __init__(self, father_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(1350, 500)
        self.setWindowTitle('Tool setup')
        self.memory_structure = DontWantDatabaseDict(self)
        grid = QGridLayout()
        self.setLayout(grid)
        self.machine_tab = father_
        self.scroll_reg = MaskScroll(self)
        self.tools_tree = TreeTool(self)
        #self.tools_tree.setSelection()
        self.r_side = RightEditPanel(self)
        self.setStyleSheet('font-size: 20px;')
        self.repaint_masks()
        grid.addWidget(self.scroll_reg, 0, 0)
        grid.addWidget(self.tools_tree, 0, 1, alignment=QtCore.Qt.AlignLeft)
        grid.addWidget(self.r_side, 0, 2, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

    def repaint_masks(self):
        #dict_ = self.scroll_reg.dict_clasters
        dict_ = self.memory_structure.address_widget_dict
        for claster in dict_:
            dict_[claster].text_field.clear_claster()


class MaskScroll(QScrollArea):
    def __init__(self, edit_dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit_dialog = edit_dialog
        self.setWidgetResizable(True)
        #x_ = 560; y_ = 470
        #self.add

        self.setFixedSize(560, 470)
        #self.scr
        self.grid = GridForClasters()

        self.current_claster = None
        self.address = r"Modelling_clay\tool_registers" + "\\" + self.edit_dialog.machine_tab.tool_registers.currentText()
        n = 0

        with open(self.address) as f:
            print('address == ', self.address)
            f_l = f.readlines()
        for _l_ in f_l:
            print('_l_  = ', _l_)
            if _l_.count('===') == 1:
                mask, address = _l_.split('===')
                if address.endswith('\n'):
                    address = address[:-1]
                claster_ = ClasterToolMask(mask, address, self, n)
                self.edit_dialog.memory_structure.address_widget_dict[address] = claster_
                #self.edit_dialog.memory_structure.address_item_dict[address] = [mask, claster_, None]
                #FFFFFFFFFFF
                self.grid.addWidget(self.edit_dialog.memory_structure.address_widget_dict[address], n, 1, alignment=QtCore.Qt.AlignLeft)
                n = n + 1
        self.form1 = QtWidgets.QWidget()
        self.form1.setLayout(self.grid)
        self.setWidget(self.form1)
        #print('CHECK')


    def save_register_func(self):
        list_ = []
        for obj in self.grid.claster_list:
            print('fuck the ', obj.text_field.toPlainText())
            if obj.tool_address in self.edit_dialog.memory_structure.address_item_dict:
                print('accepted')
                obj.text_field.text_ = obj.text_field.toPlainText()
                list_.append([obj.text_field.text_, obj.tool_address])
        change_any_file_completly(address=self.address, names=list_, split='===')
        self.grid.claster_list[0].text_field.rechoose_field()


    def two_clasters_exchage_places(self, claster, direction):
        claster_place = claster.number
        if direction == 'up':
            adding = -1
        else:
            adding = 1
        another_claster_place = claster_place + adding
        another_claster = self.grid.itemAtPosition(another_claster_place, 1).widget()
        another_claster.number = another_claster.number - adding
        claster.number = claster.number + adding
        self.grid.removeWidget_exchange_places(claster)
        self.grid.removeWidget_exchange_places(another_claster)
        #print('how many after remove = ', self.grid.how_many_clasters)
        if claster_place < another_claster_place:
            self.grid.addWidget(another_claster, claster_place, 1)
            self.grid.addWidget(claster, another_claster_place, 1)
        else:
            self.grid.addWidget(claster, another_claster_place, 1)
            self.grid.addWidget(another_claster, claster_place, 1)




class GridForClasters(QGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.claster_list = []

    def addWidget(self, w, vert, *args, **kwargs) -> None:
        print('my add, type = ', type(w))
        if isinstance(w, ClasterToolMask):#"<class 'Gui.tool_register_edit.ClasterToolMask'>":
            print('***')
            self.claster_list.insert(vert, w)
            w.up_but.show()#(True)
            w.down_but.show()
            self.claster_list.index(w)

            claster_index = self.claster_list.index(w)
            if claster_index > 0:
                print('3333')
                widget_prev = self.claster_list[claster_index - 1]
                widget_prev.down_but.show()
            else:
                w.up_but.hide()
                print('444')

            if claster_index + 1 < len(self.claster_list):
                print('555')
                widget_next = self.claster_list[claster_index + 1]
                widget_next.down_but.show()
            else:
                print('666')
                w.down_but.hide()
        print('777')
        QGridLayout.addWidget(self,  w, vert, *args, **kwargs)

    def removeWidget_exchange_places(self, w, *args, **kwargs) -> None:#for exchange
        if isinstance(w, ClasterToolMask):
            self.claster_list.remove(w)
        QGridLayout.addWidget(self, w, *args, **kwargs)
        #QGridLayout.removeWidget(self, *args, **kwargs)

class ClasterToolMask(QFrame):
    def __init__(self, mask, address, father_scroll, n, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet('border-style: outset; font-size: 20px;')
        self.number = n
        self.tool_address = address
        self.father_scroll = father_scroll
        self.text_field = MyPlainText(mask, self)
        self.text_field.setFixedSize(470, 50)
        grid = QGridLayout()
        self.setLayout(grid)
        grid.addWidget(self.text_field, 0, 1, 2, 1)

        self.up_but = UpDown(r'icons\up.png')
        self.down_but = UpDown(r'icons\down.png')
        self.up_but.clicked.connect(lambda: self.father_scroll.two_clasters_exchage_places(self, 'up'))
        self.down_but.clicked.connect(lambda: self.father_scroll.two_clasters_exchage_places(self, 'down'))
        grid.addWidget(self.up_but, 0, 0)
        grid.addWidget(self.down_but, 1, 0)
        print('claster:')
        print('mask = ', self.text_field)
        print('self.tool_address = ', self.tool_address)



class UpDown(QPushButton):
    def __init__(self, icon_address, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(22, 22)
        self.setIcon(QtGui.QIcon(icon_address))

class RightEditPanel(QFrame):
    def __init__(self, papa_dialog, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papa_dialog = papa_dialog
        grid = QGridLayout()
        self.setLayout(grid)
        #self.setStyleSheet(' border-style: outset; border-width: 4px; border-color: cyan;')
        self.lbl_mask = QLabel('Text example')
        self.lbl_mask.setFixedSize(135, 35)
        grid.addWidget(self.lbl_mask, 0, 2, alignment=QtCore.Qt.AlignRight)

        self.check_field = CheckField(self)
        grid.addWidget(self.check_field, 1, 0, 1, 3)

        self.lbl_catch = QLabel('Catched tool')
        self.lbl_catch.setFixedSize(125, 35)
        grid.addWidget(self.lbl_catch, 2, 2, alignment=QtCore.Qt.AlignRight)

        self.catched_tool = QLineEdit()
        self.catched_tool.setStyleSheet('color: green')
        self.catched_tool.setReadOnly(True)
        self.catched_tool.setFixedHeight(40)
        grid.addWidget(self.catched_tool, 3, 0, 1, 3)

        self.how_to_use = QPushButton('?')
        self.how_to_use.clicked.connect(self.ask_help)
        self.how_to_use.setStyleSheet('font-size: 50px;')
        self.how_to_use.setFixedSize(90, 75)
        grid.addWidget(self.how_to_use, 4, 0, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.new_mask_for_tool = QPushButton('New mask\nfor tool')

        self.new_mask_for_tool.clicked.connect(self.papa_dialog.memory_structure.create_new_mask)
        self.new_mask_for_tool.setFixedSize(135, 75)
        grid.addWidget(self.new_mask_for_tool, 5, 1)


        self.accept_mask = ConnectMaskButton(self, 'Bond mask\nto tool')
        self.accept_mask.clicked.connect(self.papa_dialog.memory_structure.bond_tool_mask)
        self.accept_mask.setFixedSize(135, 75)
        grid.addWidget(self.accept_mask, 4, 2, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)

        self.del_field = QPushButton('Del mask\nfield')
        self.del_field.clicked.connect(self.papa_dialog.memory_structure.del_field_func)
        self.del_field.setFixedSize(90, 75)
        grid.addWidget(self.del_field, 5, 0, alignment=QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.unbond_mask = ConnectMaskButton2(self, 'Unbond mask\n from tool')
        self.unbond_mask.clicked.connect(self.papa_dialog.memory_structure.unbond_tool_mask)
        self.unbond_mask.setFixedSize(135, 75)
        grid.addWidget(self.unbond_mask, 4, 1)

        self.save_register = QPushButton('Save\nregister')
        self.save_register.clicked.connect(self.papa_dialog.scroll_reg.save_register_func)
        self.save_register.setFixedSize(135, 75)
        grid.addWidget(self.save_register, 5, 2, alignment=QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)


    def ask_help(self):
        text = r'Help/texts/Register help.txt'
        w = 600; h = 600
        a = ShortHelp(self, text, w, h)
        a.exec()

class ConnectMaskButton(QPushButton):
    def __init__(self, panel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.panel = panel
        self.update_enable()

    def update_enable(self):
        self.setEnabled(self.update_part_1())


    def update_part_1(self):# не моргает
        print('update_part_1')
        if self.panel.papa_dialog.scroll_reg.current_claster is None:
            return False
        if self.panel.papa_dialog.scroll_reg.current_claster.tool_address in self.panel.papa_dialog.memory_structure.address_item_dict:
            return False
        if len(self.panel.papa_dialog.tools_tree.selectedItems()) != 1:
            return False
        if self.panel.papa_dialog.tools_tree.selectedItems()[0].my_type != 'file':
            return False
        if self.panel.papa_dialog.tools_tree.selectedItems()[0].tool_address in self.panel.papa_dialog.memory_structure.address_widget_dict:
            return False
        return True

class ConnectMaskButton2(ConnectMaskButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_part_1(self):
        print('update_part_2')
        if self.panel.papa_dialog.scroll_reg.current_claster is None:
            return False
        if len(self.panel.papa_dialog.tools_tree.selectedItems()) != 1:
            return False
        if self.panel.papa_dialog.tools_tree.selectedItems()[0].my_type != 'file':
            return False
        if self.panel.papa_dialog.scroll_reg.current_claster.tool_address in self.panel.papa_dialog.memory_structure.address_item_dict \
                and self.panel.papa_dialog.scroll_reg.current_claster.tool_address == self.panel.papa_dialog.tools_tree.selectedItems()[0].tool_address:
            print('TRUE')
            return True
        return False


class CheckField(QPlainTextEdit):
    def __init__(self, panel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedHeight(60)
        self.panel = panel
        self.textChanged.connect(self.check_content)


    def check_content(self):
        print('checking content')
        print(self.panel.papa_dialog.memory_structure.address_item_dict)
        text = self.toPlainText()
        list = self.panel.papa_dialog.scroll_reg.grid.claster_list
        catched_tool = self.panel.catched_tool
        catched_tool.setToolTip('No tool')
        catched_tool.setText('')
        for claster in list:
            str_ = claster.text_field.toPlainText()
            expr = QRegularExpression(str_)
            nya = expr.match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                ad = claster.tool_address
                item = self.panel.papa_dialog.memory_structure.address_item_dict[ad]
                #print('item.tool_name = ', item.tool_name)
                catched_tool.setText(item.tool_name[0])
                catched_tool.setToolTip(ad)
                return







class MyPlainText(QPlainTextEdit):
    def __init__(self, text_, claster, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_ = text_
        self.claster = claster
        self.setPlainText(text_)
        self.textChanged.connect(self.select_claster)

    @property
    def text_equal_to_dict(self):
        if self.text_ == self.toPlainText():
            color = r'255, 255, 255'
        else:
            color = r'255, 200, 200'
        return color

    def mousePressEvent(self, event):
        print('mousePressEvent')
        print(type(self.claster.father_scroll))
        print(self.claster.father_scroll.edit_dialog.tools_tree.dir_dict)
        self.dive_in_tree()
        self.rechoose_field()
        QPlainTextEdit.mousePressEvent(self, event)

    def dive_in_tree(self):
        dd = self.claster.father_scroll.edit_dialog.memory_structure.address_item_dict
        if self.claster.tool_address in dd:
            self.claster.father_scroll.edit_dialog.tools_tree.clearSelection()
            dd[self.claster.tool_address].setSelected(True)
            #self.address_widget_dict = {}
            #self.address_item_dict = {}

    def rechoose_field(self):
        print('rechoose')
        if self.claster.father_scroll.current_claster is not None:
            self.claster.father_scroll.current_claster.text_field.clear_claster()
        self.select_claster()

    def clear_claster(self):
        if self.claster.tool_address in self.claster.father_scroll.edit_dialog.memory_structure.address_item_dict:
            self.setStyleSheet(
                ' border-width: 0px; border-color: cyan; background-color: rgb({});'.format(self.text_equal_to_dict))
        else:
            self.setStyleSheet(' border-width: 0px; border-color: cyan; background-color: rgb(255, 55, 55);')

    def select_claster(self):#todo
        print('select: ', self.toPlainText())
        # self.claster.father.ensureVisible(50, 50)
        self.claster.father_scroll.ensureWidgetVisible(self)
        if self.claster.tool_address in self.claster.father_scroll.edit_dialog.memory_structure.address_item_dict:
            self.setStyleSheet(
                'border-width: 4px; border-color: cyan; background-color: rgb({});'.format(self.text_equal_to_dict))
        else:
            self.setStyleSheet(' border-width: 4px; border-color: cyan; background-color: rgb(255, 55, 55);')
        # self.setPlainText('ffffffff')
        self.claster.father_scroll.current_claster = self.claster
        self.claster.father_scroll.edit_dialog.r_side.accept_mask.update_enable()
        self.claster.father_scroll.edit_dialog.r_side.unbond_mask.update_enable()
        print('end select')


class TreeTool(QTreeWidget):
    def __init__(self, dialog_):
        super().__init__()
        self.dialog = dialog_
        self.setHeaderHidden(True)
        self.setFixedWidth(350)
        #self.setFixedSize(350, 360)
        self.dir_dict = {}
        self.tools_folder = "Modelling_clay\machine_tools"
        tree = walk(self.tools_folder)
        for tre in tree:
            address = tre[0]
            if address.endswith('__pycache__') or address.endswith('tool_pics'):
                continue
            for tr in tre[1]:   # folders
                if tr == '__pycache__' or tr =='tool_pics':
                    continue
                full_address = address + '\\' + tr
                #cur_item = OptionsQTWItem([tr][0], full_address)#text2, tool_address
                cur_item = OptionsQTWItem(tool_name=[tr][0], tool_address=full_address)
                self.dir_dict[address + '\\' + tr] = cur_item
                self.top_or_child(cur_item, self.tools_folder, address)
                cur_item.my_type = 'dir'
                self.dialog.memory_structure.address_item_dict[full_address] = cur_item

            for tr in tre[2]:   # files
                if tr == '__init__.py':
                    continue
                full_address = address + '\\' + tr
                cur_item = OptionsQTWItem([tr][0], full_address) #
                self.dialog.memory_structure.address_item_dict[full_address] = cur_item

                if cur_item.tool_address in self.dialog.memory_structure.address_widget_dict:
                    cur_item.setIcon(0, QtGui.QIcon('icons/tool.png'))
                    cur_item.setBackground(0, QtGui.QBrush(QtGui.QColor(224, 255, 255)))
                #tool_address
                self.top_or_child(cur_item, self.tools_folder, address)
                cur_item.my_type = 'file'
        self.currentItemChanged.connect(self.choose_item)
        self.itemClicked.connect(self.choose_item)
        self.expandAll()


    def choose_item(self):
        print('chooose item')
        address = self.currentItem().tool_address
        if address in self.dialog.memory_structure.address_widget_dict:
            self.dialog.memory_structure.address_widget_dict[address].text_field.rechoose_field()#select_claster()
        else:
            if self.dialog.scroll_reg.current_claster is not None:# and self.dialog.scroll_reg.current_claster.tool_address != address:
                #self.dialog.scroll_reg.current_claster.text_field.clear_claster()
                self.dialog.scroll_reg.current_claster.text_field.rechoose_field()
        self.dialog.r_side.accept_mask.update_enable()
        self.dialog.r_side.unbond_mask.update_enable()

    def top_or_child(self, item, mother_address, new_address):
        if mother_address == new_address:
            self.addTopLevelItem(item)
        else:
            self.dir_dict[new_address].addChild(item)

class OptionsQTWItem(QTreeWidgetItem):
    def __init__(self, tool_name, tool_address):#todo text2? wtf??!
        print('tool name = ', tool_name)
        tool_name = [tool_name]
        super().__init__(tool_name)
        #self.mask = text2[0]
        self.tool_name = tool_name
        self.tool_address = tool_address
        #print('text2 == ', text2)
        self.setSelected(True)

    #def zeroing_tree_item(self):
    #    pass

class DontWantDatabaseDict:
    def __init__(self, papa):
        self.papa_dialog = papa
        self.list_new_address_names = []
        self.one = 'some_special_shit'
        self.tool_about_number = 1

        self.address_widget_dict = {}
        self.address_item_dict = {}# mask: widget

    def disconnect_tool_and_mask(self, scroll_w, tree_item):
        #mask = scroll_w.text_
        #mask = scroll_w.text_field.text_
        scroll_w.tool_address = self.one + str(self.tool_about_number)
        self.tool_about_number +=1
        self.address_widget_dict.pop(tree_item.tool_address)
        self.address_widget_dict[scroll_w.tool_address] = scroll_w


    def unbond_tool_mask(self):#todo нет никакого my_scroll
        item = self.papa_dialog.tools_tree.selectedItems()[0]
        claster = self.papa_dialog.scroll_reg.current_claster
        if self.address_widget_dict[item.tool_address] is claster:
        #if claster is new_item.widget_to_show:
            print('self.papa_dialog.my_scroll.current_claster is new_item.widget_to_show')
            self.disconnect_tool_and_mask(claster, item)
            item.setIcon(0, QtGui.QIcon())
            item.setBackground(0, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
            claster.text_field.rechoose_field()

    def bond_tool_mask(self):
        print('bond')
        claster = self.papa_dialog.scroll_reg.current_claster
        item = self.papa_dialog.tools_tree.currentItem()
        if item is None:
            return
        temporary_address = claster.tool_address
        new_address = item.tool_address
        self.papa_dialog.memory_structure.address_widget_dict.pop(temporary_address)
        self.papa_dialog.memory_structure.address_widget_dict[new_address] = claster
        claster.tool_address = new_address
        #покрасить и иконку прилепить
        item.setIcon(0, QtGui.QIcon('icons/tool.png'))
        item.setBackground(0, QtGui.QBrush(QtGui.QColor(224, 255, 255)))
        claster.text_field.rechoose_field()

    def create_new_mask(self):
        temporary_address = self.one+str(self.tool_about_number)
        self.tool_about_number +=1
        n = len(self.papa_dialog.scroll_reg.grid.claster_list) #- 1
        claster = ClasterToolMask(mask='mask', address=temporary_address, father_scroll=self.papa_dialog.scroll_reg, n=n)
        self.papa_dialog.memory_structure.address_widget_dict[temporary_address] = claster
        #print('1| claster_list = ', self.papa_dialog.scroll_reg.grid.claster_list)
        scroll = self.papa_dialog.scroll_reg
        scroll.grid.addWidget(claster, n, 1, alignment=QtCore.Qt.AlignLeft)
        #print('1| claster_list = ', self.papa_dialog.scroll_reg.grid.claster_list)
        for p in range(n):
            self.papa_dialog.scroll_reg.two_clasters_exchage_places(claster, direction='up')
        claster.text_field.rechoose_field()
        print('self.papa_dialog.grid.claster_list = ', self.papa_dialog.scroll_reg.grid.claster_list)

    def del_field_func(self):
        print('del bond field')
        claster = self.papa_dialog.scroll_reg.current_claster
        n = len(self.papa_dialog.scroll_reg.grid.claster_list)
        i = claster.number
        for p in range(i, n-1):
            self.papa_dialog.scroll_reg.two_clasters_exchage_places(claster, direction='down')
        self.papa_dialog.scroll_reg.grid.removeWidget(claster)
        self.papa_dialog.scroll_reg.grid.claster_list.pop(n-1)
        claster.deleteLater()
        self.papa_dialog.scroll_reg.current_claster = None

