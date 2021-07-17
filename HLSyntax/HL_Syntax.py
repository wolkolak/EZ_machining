import sys
import time

import numpy as np
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QRegExp, QRegularExpression, pyqtSignal, QEventLoop
#from PyQt5.QtWidgets import *
#from HLSyntax.PostProcessors_revers import *
#from HLSyntax.ReversPostProcessor_0 import
from HLSyntax.PostProcessors_revers.Fanuc_NT import Fanuc_NT, STYLES, STYLES_list_G0, STYLES_list_G1
#HLSyntax.PostProcessors_revers.




class GMHighlighter(QSyntaxHighlighter):

    def __init__(self, document, base):
        QSyntaxHighlighter.__init__(self, document)
        self.list_number_captured_1 = [i * 2 for i in range(1, 13)]#todo добавь ijk
        self.previous_block_g = 0
        self.base = base
        self.count = 0
        self.count_in_step = 0
        self.const_step = 1000
        self.standart_step = self.const_step
        self.reversal_post_processor = Fanuc_NT(base)
        self.remember_np_box_parts()  # todo Нужна ли отдельная функция вообще? потребуется ли она

        self.main_rule_regular_expression = QRegularExpression(self.reversal_post_processor.sorted_axis_rule)
        self.simple_format = STYLES['axis']#self.first_rule[2]
        self.second_rule_regular_expression = QRegularExpression(self.reversal_post_processor.unsorted_axis_rule)#self.rules[0][0]
        self.too_little_number_check()


    def remember_np_box_parts(self):
        self.current_g_cod_pool = self.base.np_box.current_g_cod_pool


    def too_little_number_check(self):
        print('too_little_number_check')
        if self.base.reading_lines_number < self.const_step:
            self.standart_step = self.base.reading_lines_number


    def highlightBlock(self, text):
        """Применить выделение синтаксиса к данному блоку текста. """

        nya = self.main_rule_regular_expression.match(text, 0)
        #print('nya0 = ', nya.captured(0))
        start = nya.capturedStart()
        len_match = nya.capturedLength()
        if len_match != 0:
            #print('nya = ', nya.captured())
            self.recount(nya, STYLES_list_G0, STYLES_list_G1)

        elif start == 0:
            print('empty string')
            self.recount_empty_line()
            #print('index = {}, string = {}, запуск дополнительных правил'.format(index, text))
        else:
            nya = self.second_rule_regular_expression.match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                self.unsorted_recount(nya, STYLES_list_G0, STYLES_list_G1)
            else:
                if not self.recount_special_rules(text):
                    print('ERROR LINE')

    def recount_empty_line(self):
        self.current_g_cod_pool[self.count][0] = self.previous_block_g
        self.current_g_cod_pool[self.count][14] = 9999#type
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def recount_special_rules(self, text):
        self.current_g_cod_pool[self.count][1] = self.previous_block_g
        result = self.special_rare_case(text, self.count)
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return result

    def special_rare_case(self, text, count):
        #print('self.base.current_g_cod_pool[self.count] ', self.base.current_g_cod_pool[self.count])
        #G28 U0. V0.
        print('text = ', text)
        if self.reversal_post_processor.check_command(self, text, self.current_g_cod_pool[count], count, self.base.g_modal):#todo это не тот g_modal
            return True
        else:
            return False

        #print('self.start_pointXYZ = ', self.reversal_post_processor.start_pointXYZ)


    def recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        self.current_g_cod_pool[self.count, np.r_[1:13]] = [nya.captured(i) or None for i in self.list_number_captured_1]
        #Заполнения здесь не происходит, так как оно только между numpy массивами
        #print('current_g_cod_pool == ', self.base.current_g_cod_pool[self.count])
        #G0-G3
        if np.isnan(self.current_g_cod_pool[self.count][1]):
            self.current_g_cod_pool[self.count][1] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][1]
            self.current_g_cod_pool[self.count, 0] = self.previous_block_g
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        #colors
        # простая подсветка одним цветом
        # self.setFormat(index, len_match, self.simple_format)
        #полноценная подсветка
        i = 0
        ax = len(nya.captured(i * 2 + 1))
        start = 0
        while i < 13:
            if ax != 0:
                self.setFormat(start, ax, stile[i])
                #print('i = ', i)
                #print('stile[i] = ', stile[i])
            start = start + ax
            i = i + 1
            ax = len(nya.captured(i * 2 + 1))


        print('recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)
            #QApplication.processEvents()
        #print('Count')
        return

    def unsorted_recount(self, nya, STYLES_list_G0, STYLES_list_G1):

        #for i in range(35):
        #    print('nya.captured({}) = {}'.format(i, nya.captured(i)))
        # G0-G3
        self.current_g_cod_pool[self.count][1] = nya.captured(2) or None
        if np.isnan(self.current_g_cod_pool[self.count][1]):
            self.current_g_cod_pool[self.count][1] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][1]
            self.current_g_cod_pool[self.count][0] = self.previous_block_g

        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        ax = len(nya.captured(1))
        if ax != 0:
            self.setFormat(start, ax, stile[0])
            start = start + ax
        ax = len(nya.captured(3))
        #Альтернативно
        n = 4
        while nya.captured(n) != '' and n < 22 :#вероятно, избыточное условие
            self.nesting(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))
        n = 22
        ax = len(nya.captured(21))
        while nya.captured(n) != '' and n < 29 :#вероятно, избыточное условие
            self.nestingIJK(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))
        #print('n = {}, ax = {}'.format(n, ax))


        #for i in range (33):
        #    print('nya.captured({}) = {}'.format(i, nya.captured(i)))

        ax = len(nya.captured(30))
        if ax != 0:
            self.setFormat(start, ax, stile[10])
            start = start + ax
        self.current_g_cod_pool[self.count][11] = nya.captured(31) or None#R - nya.captured(22)
        #ax = len(nya.captured(29))

        ax = len(nya.captured(32))
        if ax != 0:
            self.setFormat(start, ax, stile[11])
            #start = start + ax
        self.current_g_cod_pool[self.count][11] = nya.captured(31) or None#F
        print('unsorted recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
            # QApplication.processEvents()
        return

    def nestingIJK(self, n, nya, start, ax, stile):
        print('nestingIJK')
        symbol = nya.captured(n)
        if symbol == 'I':
            i = 7
        elif symbol == 'J':
            i = 8
        elif symbol == 'K':
            i = 9
        else:
            print('Ты не должен сюда попасть, но вдруг')
            return
        self.setFormat(start, ax, stile[i])
        self.current_g_cod_pool[self.count][i+1] = nya.captured(n+1)


    def nesting(self, n, nya, start, ax, stile):
        symbol = nya.captured(n)
        if symbol == 'X':
            i = 1
        elif symbol == 'Y':
            i = 2
        elif symbol == 'Z':
            i = 3
        elif symbol == 'C':
            i = 6
        elif symbol == 'A':
            i = 4
        elif symbol == 'B':
            i = 5

        else:
            print('Ты не должен сюда попасть, но вдруг')
            return
        self.setFormat(start, ax, stile[i])
        self.current_g_cod_pool[self.count][i+1] = nya.captured(n+1)


    def to_the_start(self):
        self.standart_step = 1
        self.count = 0
        self.base.progress_bar.setMaximum(1)
        print("the end1")