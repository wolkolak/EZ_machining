from PyQt5.QtCore import QRegExp, QRegularExpression
from abc import ABC, abstractmethod
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
import copy

todo Всё это удалять
sdfsf
class G_MODAL_DICT(dict):#dict of lists of lists.
    def __init__(self, redactor):
        fdfgdf
        super().__init__()
        print('G_MODAL_DICT')
        self.redactor = redactor
        self['plane'] = [[0, '18'], ]
        self['absolute_or_incremental'] = [[0, '90'], ]
        self['polar_coord'] = [[0, '113'],]
        self['SC'] = [[0, '54'], ]
        self.base_g_modal = self.create_base_g_modal()
        self.current_g_modal = self.create_current_from_g_modal(0)
        print('1base_dict = ', self.base_g_modal)

    def create_base_g_modal(self):
        base_dict = {}
        for i in self:
            base_dict[i] = self.get(i)[0][1]
        #print('base_dict = ', base_dict)
        return base_dict

    def create_current_from_g_modal(self, line_number_start):#по очереди, хотя можно и х2 идти
        #print('||| create_current_from_g_modal')
        new_g_modal_dict = self.base_g_modal.copy()#todo должен быть базовый g_modal_dict

        for i in self:#dict search
            i_current = 0
            for j in self.get(i):#search for tuple in list
                if j[0] > line_number_start:
                    break
                i_current = j[1]
            new_g_modal_dict[i] = i_current
        return new_g_modal_dict

    #def del_all_modal_commands_in_range(self, n_start, n_end, doc_end, delta_lines):
    #    #del and change nuer lines
    #    for i in self:
    #        list1 = self.get(i)
    #        j = 0
    #        list_len = len(list1)
    #        while j < list_len:
    #            if n_start <= list1[j][0]:
    #                if list1[j][0] <= n_end:
    #                    list1.pop(j)
    #                    list_len -= 1
    #                    j -= 1
    #                    #continue
    #                else:
    #                    list1[j][0] = list1[j][0] + delta_lines
    #            j += 1
    #        if i == 'SC':
    #            #print('888 list1 = ', list1)
    #            True54 = True55 = True56 = True54 = True57 = True58 = True59 = False
    #            for i2 in list1:
    #                #print('list1 = ', list1)
    #                if i2[1] == '54':
    #                    True54 = True
    #                elif i2[1] == '55':
    #                    True55 = True
    #                elif i2[1] == '56':
    #                    True56 = True
    #                elif i2[1] == '57':
    #                    True57 = True
    #                elif i2[1] == '58':
    #                    True58 = True
    #                elif i2[1] == '59':
    #                    True59 = True
    #                else:
    #                    # А G68.1 напрямую выкидываем на помоечку
    #                    # Прям удаляем.
    #                    g54_g59_AXIS_Display = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.g54_g59_AXIS_Display
    #                    g54_g59_AXIS_Display.pop(i2[1])
#
    #            g54_g59_AXIS_Display = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.g54_g59_AXIS_Display
#
    #            g54_g59_AXIS_Display['G54'][6] = True54
    #            g54_g59_AXIS_Display['G55'][6] = True55
    #            g54_g59_AXIS_Display['G56'][6] = True56
    #            g54_g59_AXIS_Display['G57'][6] = True57
    #            g54_g59_AXIS_Display['G58'][6] = True58
    #            g54_g59_AXIS_Display['G59'][6] = True59

    def insert_in_main_gmodal(self, key, line_number, value):
        #'polar_coord', count + self.redactor.editor.min_line_np, POLAR_ON_OFF
        print('insert_in_main_gmodal')
        list1 = self.get(key)
        print('key = ', key)
        print('22 list1 = ', list1)
        if key == 'SC':
            self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.g54_g59_AXIS_Display['G' + str(value)][6] = True
        print('line_number = ',line_number)
        for j in range(len(list1)):#-1 ? nope
            print('j=',j)
            print('list1[j][0] = ', list1[j][0])
            if line_number < list1[j][0]:#todo А если закончатся значения, куда добавлять?
                position = j
                break
        new_line_value = [line_number, value]
        if 'position' in locals():
            print('position in locals')
            list1.insert(position, new_line_value)
        else:
            print('position None')
            list1.append(new_line_value)
        #self.current_g_modal[key] = value
        print('self.current_g_modal = ', self.current_g_modal)
        print('G MODAL = ', self)
        #todo обновить create_current_from_g_modal

    def slide_in_main_gmodal(self, start_slide, n):
        for i in self:
            list1 = self.get(i)
            for j in range(len(list1)):
                if start_slide < list1[j][0]:
                    list1[j][0] = list1[j][0] + n