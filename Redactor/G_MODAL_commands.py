from PyQt5.QtCore import QRegExp, QRegularExpression
from abc import ABC, abstractmethod
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
import copy

class G_MODAL_DICT(dict):#dict of lists of lists.
    def __init__(self):
        super().__init__()
        self['plane'] = [[0, '18'], ]
        self['absolute_or_incremental'] = [[0, '90'], ]
        self.base_g_modal = self.create_base_g_modal()
        self.current_g_modal = self.create_current_from_g_modal(0)
        print('1base_dict = ', self.base_g_modal)
        #self.insert_in_main_gmodal('plane', 2, 18)


    def create_base_g_modal(self):
        base_dict = {}
        for i in self:
            base_dict[i] = self.get(i)[0][1]
        #print('base_dict = ', base_dict)
        return base_dict

    def create_current_from_g_modal(self, line_number_start):#по очереди, хотя можно и х2 идти

        new_g_modal_dict = self.base_g_modal.copy()#todo должен быть базовый g_modal_dict

        for i in self:#dict search
            i_current = 0
            for j in self.get(i):#search for tuple in list
                i_current = j[1]
                if j[0] > line_number_start:
                    break
            new_g_modal_dict[i] = i_current
        return new_g_modal_dict

    def del_all_modal_commands_in_range(self, n_start, n_end, doc_end, delta_lines):
        #del and change nuer lines
        for i in self:
            list1 = self.get(i)
            j = 0
            list_len = len(list1)
            while j < list_len:
                if n_start <= list1[j][0]:
                    if list1[j][0] <= n_end:
                        list1.pop(j)
                        list_len -= 1
                        j -= 1
                        #continue
                    else:
                        list1[j][0] = list1[j][0] + delta_lines
                j += 1
            #for j in range(len(list1)):
            #    if n_start <= list1[j][0]:
            #        if list1[j][0] <= n_end:
            #            list1.pop(j)
            #        else:
            #            list1[j][0] = list1[j][0] + delta_lines

    def insert_in_main_gmodal(self, key, line_number, value):
        print('insert_in_main_gmodal')
        list1 = self.get(key)
        print('list1 = ', list1)
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