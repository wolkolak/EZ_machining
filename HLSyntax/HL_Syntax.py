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
        self.reversal_post_processor = Fanuc_NT()

        self.main_rule_regular_expression = QRegularExpression(self.reversal_post_processor.sorted_axis_rule)
        self.simple_format = STYLES['axis']#self.first_rule[2]
        self.second_rule_regular_expression = QRegularExpression(self.reversal_post_processor.unsorted_axis_rule)#self.rules[0][0]
        self.too_little_number_check()

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

        elif start == 0:#empty string
            print('special case')
            self.recount_empty_line()
            #print('index = {}, string = {}, запуск дополнительных правил'.format(index, text))
        else:
            nya = self.second_rule_regular_expression.match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                self.unsorted_recount(nya, STYLES_list_G0, STYLES_list_G1)
            else:
                self.recount_special_rules(text)
                print('ERROR LINE')

    def recount_empty_line(self):
        self.base.current_g_cod_pool[self.count][0] = self.previous_block_g
        self.base.current_g_cod_pool[self.count][14] = 9999#type
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def recount_special_rules(self, text):
        self.base.current_g_cod_pool[self.count][1] = self.previous_block_g
        self.special_rare_case(text, self.count)
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def special_rare_case(self, text, count):
        #print('self.base.current_g_cod_pool[self.count] ', self.base.current_g_cod_pool[self.count])
        #G28 U0. V0.
        self.reversal_post_processor.check_command(self, text, self.base.current_g_cod_pool[count], self.base.g_modal)
        #print('self.start_pointXYZ = ', self.reversal_post_processor.start_pointXYZ)
        print('text = ', text)

    def recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        #print('self.list_number_captured_1 shape = ', len(self.list_number_captured_1))
        #print('self.base.current_g_cod_pool shape = ', self.base.current_g_cod_pool.shape)
        #self.base.current_g_cod_pool[self.count, 0] = nya.captured(0) or None
        self.base.current_g_cod_pool[self.count, np.r_[1:13]] = [nya.captured(i) or None for i in self.list_number_captured_1]
        #G0-G3
        if np.isnan(self.base.current_g_cod_pool[self.count][1]):
            self.base.current_g_cod_pool[self.count][1] = self.previous_block_g
        else:
            self.previous_block_g = self.base.current_g_cod_pool[self.count][1]
            self.base.current_g_cod_pool[self.count, 0] = self.previous_block_g
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        #colors
        # простая подсветка одним цветом
        # self.setFormat(index, len_match, self.simple_format)
        #полноценная подсветка
        i = 0
        ax = len(nya.captured(i * 2 + 1))
        start = 0
        while i < 9:
            if ax != 0:
                self.setFormat(start, ax, stile[i])
            start = start + ax
            i = i + 1
            ax = len(nya.captured(i * 2 + 1))
        for i in range (33):
            print('nya.captured({}) = {}'.format(i, nya.captured(i)))
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)
            #QApplication.processEvents()
        return

    def unsorted_recount(self, nya, STYLES_list_G0, STYLES_list_G1):

        #for i in range(35):
        #    print('nya.captured({}) = {}'.format(i, nya.captured(i)))
        # G0-G3
        self.base.current_g_cod_pool[self.count][1] = nya.captured(2) or None
        if np.isnan(self.base.current_g_cod_pool[self.count][1]):
            self.base.current_g_cod_pool[self.count][1] = self.previous_block_g
        else:
            self.previous_block_g = self.base.current_g_cod_pool[self.count][1]
            self.base.current_g_cod_pool[self.count][0] = self.previous_block_g

        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        ax = len(nya.captured(1))
        if ax != 0:
            self.setFormat(start, ax, stile[0])
            start = start + ax
        ax = len(nya.captured(3))
        #Альтернативно
        n = 4
        while nya.captured(n) != '' and n < 27 :#вероятно, избыточное условие
            self.nesting(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))

        for i in range (33):
            print('nya.captured({}) = {}'.format(i, nya.captured(i)))

        ax = len(nya.captured(27))
        if ax != 0:
            self.setFormat(start, ax, stile[7])
            start = start + ax
        self.base.current_g_cod_pool[self.count][11] = nya.captured(28) or None#R - nya.captured(22)
        ax = len(nya.captured(29))


        if ax != 0:
            self.setFormat(start, ax, stile[8])
            #start = start + ax
        self.base.current_g_cod_pool[self.count][12] = nya.captured(30) or None#F
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
            # QApplication.processEvents()
        return

    def nesting(self, n, nya, start, ax, stile):
        symbol = nya.captured(n)
        if symbol == 'X':
            i = 1
        elif symbol == 'Y':
            i = 2
        elif symbol == 'Z':
            i = 3
        elif symbol == 'C':
            i = 4
        elif symbol == 'A':
            i = 5
        elif symbol == 'B':
            i = 6
        else:
            print('Ты не должен сюда попасть, но вдруг')
            return
        self.setFormat(start, ax, stile[i])
        self.base.current_g_cod_pool[self.count][i] = nya.captured(n+1)


    def to_the_start(self):
        self.standart_step = 1
        self.count = 0
        self.base.progress_bar.setMaximum(1)
        print("the end1")