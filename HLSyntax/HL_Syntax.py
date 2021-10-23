import numpy as np
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtCore import QRegularExpression
#from PyQt5.QtWidgets import *
#from HLSyntax.PostProcessors_revers import *
#from HLSyntax.ReversPostProcessor_0 import
from Modelling_clay.PostProcessors_revers.Fanuc_NT import Fanuc_NT
from Modelling_clay.ReversPostProcessor_0 import STYLES, STYLES_list_G0, STYLES_list_G1
#HLSyntax.PostProcessors_revers.




class GMHighlighter(QSyntaxHighlighter):

    def __init__(self, document, base):
        QSyntaxHighlighter.__init__(self, document)
        self.list_number_captured_1 = [i * 2 for i in range(1, 15)]#todo добавь ijk
        self.list_number_captured_1.insert(3, 6)
        print('self.list_number_captured_1 = ', self.list_number_captured_1)
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
        self.current_g_cod_pool[self.count][2] = self.previous_block_g
        self.current_g_cod_pool[self.count][16] = 9999#type
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def recount_special_rules(self, text):
        self.current_g_cod_pool[self.count][3] = self.previous_block_g
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

        self.current_g_cod_pool[self.count, np.r_[0:15]] = [nya.captured(i) or None for i in self.list_number_captured_1]
        print('uuuu nya.captured(6) = ',nya.captured(6))
        #Заполнения здесь не происходит, так как оно только между numpy массивами
        #print('current_g_cod_pool == ', self.base.current_g_cod_pool[self.count])
        #G0-G3
        if np.isnan(self.current_g_cod_pool[self.count][3]):
            self.current_g_cod_pool[self.count][3] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][3]
            self.current_g_cod_pool[self.count, 2] = self.previous_block_g
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        #colors
        # простая подсветка одним цветом
        # self.setFormat(index, len_match, self.simple_format)
        #полноценная подсветка
        i = 0
        ax = len(nya.captured(i * 2 + 1))
        start = 0
        #if ax != 0:
        #    self.setFormat(start, ax, stile[i])
        #start = start + ax
        #i = i + 1
        print('i equal ', i)
        #for k in range(40):
        #    print('recount: ||||nya.captured({}) = {}'.format(k, nya.captured(k)))

        while i < 14:#todo надо подумать. По идее надо добавлять +1 строку в style, но работало, вроде...
            if ax != 0:
                self.setFormat(start, ax, stile[i])
                #print('i = ', i)
                #print('stile[i] = ', stile[i])
            start = start + ax
            i = i + 1
            ax = len(nya.captured(i * 2 + 1))


        #print('recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)
            #QApplication.processEvents()
        #print('Count')
        return

    def unsorted_recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        print('unsorted_recount start')

        #for i in range(35):
        #    print('nya.captured({}) = {}'.format(i, nya.captured(i)))
        # G0-G3
        self.current_g_cod_pool[self.count][0] = nya.captured(2) or None
        self.current_g_cod_pool[self.count][1] = nya.captured(4) or None
        self.current_g_cod_pool[self.count][2] = nya.captured(6) or None
        if np.isnan(self.current_g_cod_pool[self.count][2]):
            self.current_g_cod_pool[self.count][3] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][2]
            self.current_g_cod_pool[self.count][3] = self.previous_block_g

        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        n = 1#N
        ax = len(nya.captured(n))

        #print('n === ', n)
        #print('nya.captured(n) = ', nya.captured(n))
        #print(' ax  == ', ax )
        #print('start === ', start)


        if ax != 0:
            self.setFormat(start, ax, stile[0])#N
            start = start + ax
        n = n + 2
        ax = len(nya.captured(n))



        if ax != 0:
            self.setFormat(start, ax, stile[1])#G40
            start = start + ax
        n = n + 2
        ax = len(nya.captured(n))
        if ax != 0:
            self.setFormat(start, ax, stile[2])#G1
            start = start + ax
        n = n + 2
        ax = len(nya.captured(n))

        #if ax != 0:
        #    self.setFormat(start, ax, stile[n-1])
        #    start = start + ax
        #n = n + 2
        #ax = len(nya.captured(n))
        n = n + 1
        print('n === ', n)
        for k in range(40):
            print('||||nya.captured({}) = {}'.format(k, nya.captured(k)))

        #n = 4
        while nya.captured(n) != '' and n < 26 :#вероятно, избыточное условие
            self.nesting(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))
        #n = 26
        #ax = len(nya.captured(n))#todo нужно будет разделить координаты точки и IJK или уже?

        while nya.captured(n) != '' and n < 33 :#ijk
            self.nestingIJK(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))
        #print('n = {}, ax = {}'.format(n, ax))


        #for i in range (33):
        #    print('nya.captured({}) = {}'.format(i, nya.captured(i)))
        n = 35
        ax = len(nya.captured(n - 1))
        print('n 2=== ', n)
        #ax = len(nya.captured(34))
        if ax != 0:
            self.setFormat(start, ax, stile[12])
            start = start + ax
        self.current_g_cod_pool[self.count][13] = nya.captured(35) or None#R
        #ax = len(nya.captured(29))

        n = 37
        ax = len(nya.captured(n - 1))
        if ax != 0:
            self.setFormat(start, ax, stile[13])
            #start = start + ax
        self.current_g_cod_pool[self.count][14] = nya.captured(37) or None#F
        print('unsorted recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
            # QApplication.processEvents()
        return

    def nestingIJK(self, n, nya, start, ax, stile):
        print('nestingIJK')
        add = 2
        symbol = nya.captured(n)
        if symbol == 'I':
            i = 7 + add
        elif symbol == 'J':
            i = 8 + add
        elif symbol == 'K':
            i = 9 + add
        else:
            print('Ты не должен сюда попасть, но вдруг 1')
            return
        self.setFormat(start, ax, stile[i])
        self.current_g_cod_pool[self.count][i+1] = nya.captured(n+1)


    def nesting(self, n, nya, start, ax, stile):
        print('nesting s')
        add = 2
        symbol = nya.captured(n)
        if symbol == 'X':
            i = 1 + add
        elif symbol == 'Y':
            i = 2 + add
        elif symbol == 'Z':
            i = 3 + add
        elif symbol == 'C':
            i = 6 + add
        elif symbol == 'A':
            i = 4 + add
        elif symbol == 'B':
            i = 5 + add

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