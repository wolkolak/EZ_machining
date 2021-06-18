import sys
import time

import numpy as np
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QRegExp, QRegularExpression, pyqtSignal, QEventLoop
from PyQt5.QtWidgets import *
#from HLSyntax.PostProcessors_revers import *
from HLSyntax.PostProcessors_revers.Fanuc_NT import Fanuc_NT
#HLSyntax.PostProcessors_revers.

def format(color, style=''):
    """ Верните QTextCharFormat с указанными атрибутами. """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)
    return _format

# Синтаксические стили, которые могут использоваться
STYLES = {
    'axis': format('blue'),
    'g_cod_X': format('rgba(201,33,30,255)'),
    'g_cod_Y': format('rgba(0,132,209,255)'),
    'g_cod_Z': format('rgba(70,138,26,255)'),
    'g_cod_C': format('rgba(255,84,41,255)'),
    'g_cod_A': format('rgba(101,9,83,255)'),
    'g_cod_B': format('rgba(129,55,9,255)'),
    'comment_brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


STYLES_list_G0 = [
    #, 'italic' это перебор
    format('blue'), #'axis':
    format('#c9211e'),#'g_cod_X':
    format('#0084d1'),#'g_cod_Y':
    format('#468a1a'),#'g_cod_Z':
    format('#ff5429'),#'g_cod_C':
    format('#650953'),#'g_cod_A':
    format('#813709'),#'g_cod_B':
    format('blue'),  #R
    format('blue'),  #F
]

STYLES_list_G1 = [
    format('blue', 'bold'), #'axis':
    format('#c9211e', 'bold'),#'g_cod_X':
    format('#0084d1', 'bold'),#'g_cod_Y':
    format('#468a1a', 'bold'),#'g_cod_Z':
    format('#ff5429', 'bold'),#'g_cod_C':
    format('#650953', 'bold'),#'g_cod_A':
    format('#813709', 'bold' ),#'g_cod_B':
    format('blue', 'bold'), #R
    format('blue', 'bold'), #F
]

stile_g1 = [
    format('bold')
]
class GMHighlighter(QSyntaxHighlighter):

    """Синтаксические маркеры для языка. """
    # G-func
    #g_cod = ['G0', 'G1', 'G2', 'G3']
    # axises
    axises0 = ['X', 'Y', 'Z', 'C', 'B', 'A']
    axises = ['X', 'Y', 'Z', 'C', 'B', 'A', 'R']#- , 'G', 'F'
    g_prefix = r'(G0?([0123])\s*)?'
    f_postfix = r'(F(\d+.\d*))?\s*'
    r_postfix = r'(R(\d+.\d*))?\s*'
    # most strings look like 'main_rule'

    sorted_axis_rule = ''
    for letter in axises:
        sorted_axis_rule += r'((?:{})(-?\d+\.\d*)\s*)?'.format(letter)
        #sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)

    sorted_axis_rule = '^' + g_prefix + sorted_axis_rule + f_postfix +'$' #'(?:G0?\d)?\s*'   + f_postfix
    #print('nabor XYZ:', sorted_axis_rule)

    #sorted_axis_rule = r'^(?:X)(\d)$'  # UDALIT

    axises_str = ''.join(axises0)
    axises_coord = r'(([{}])\s*(-?\d+\.\d*)\s*)?'.format(axises_str)


    #unsorted_axis_rule = r'(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)#r'^\d((?:X)(-?\d+\.\d*)\s*)$'

    unsorted_axis_rule = axises_coord * 6
    unsorted_axis_rule = g_prefix + unsorted_axis_rule + r_postfix + f_postfix
    unsorted_axis_rule = '^' + unsorted_axis_rule +'$'

    def __init__(self, document, base):
        QSyntaxHighlighter.__init__(self, document)
        self.list_number_captured_1 = [i * 2 for i in range(1, 12)]
        self.previous_block_g = 0
        self.base = base
        self.count = 0
        self.count_in_step = 0
        self.const_step = 1000
        self.standart_step = self.const_step
        self.reversal_post_processor = Fanuc_NT()

        self.main_rule_regular_expression = QRegularExpression(self.sorted_axis_rule)
        self.simple_format = STYLES['axis']#self.first_rule[2]
        self.second_rule_regular_expression = QRegularExpression(self.unsorted_axis_rule)#self.rules[0][0]
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
                self.recount2(text)
                print('ERROR LINE')

    def recount_empty_line(self):
        self.base.current_g_cod_pool[self.count][0] = self.previous_block_g
        self.base.current_g_cod_pool[self.count][10] = 9999
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def recount2(self, text):
        self.base.current_g_cod_pool[self.count][0] = self.previous_block_g
        self.special_rare_case(text, self.count)
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
        return

    def special_rare_case(self, text, count):
        #print('self.base.current_g_cod_pool[self.count] ', self.base.current_g_cod_pool[self.count])
        #G28 U0. V0.
        self.reversal_post_processor.check_command(text, self.base.current_g_cod_pool[count], self.base.editor.g_modal)
        #print('self.start_pointXYZ = ', self.reversal_post_processor.start_pointXYZ)
        print('text = ', text)

    def recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        #print('self.list_number_captured_1 shape = ', len(self.list_number_captured_1))
        #print('self.base.current_g_cod_pool shape = ', self.base.current_g_cod_pool.shape)
        self.base.current_g_cod_pool[self.count] = [nya.captured(i) or None for i in self.list_number_captured_1]
        #G0-G3
        if np.isnan(self.base.current_g_cod_pool[self.count][0]):
            self.base.current_g_cod_pool[self.count][0] = self.previous_block_g
        else:
            self.base.current_g_cod_pool[self.count][9] = self.base.current_g_cod_pool[self.count][0]
            self.previous_block_g = self.base.current_g_cod_pool[self.count][0]
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        #colors
        # простая подсветка одним цветом
        # self.setFormat(index, len_match, self.simple_format)
        #альтернативная подсветка
        i = 0
        ax = len(nya.captured(i * 2 + 1))
        start = 0
        while i < 9:
            if ax != 0:
                self.setFormat(start, ax, stile[i])
            start = start + ax
            i = i + 1
            ax = len(nya.captured(i * 2 + 1))
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
        self.base.current_g_cod_pool[self.count][0] = nya.captured(2) or None
        if np.isnan(self.base.current_g_cod_pool[self.count][0]):
            self.base.current_g_cod_pool[self.count][0] = self.previous_block_g
        else:
            self.base.current_g_cod_pool[self.count][9] = self.base.current_g_cod_pool[self.count][0]
            self.previous_block_g = self.base.current_g_cod_pool[self.count][0]
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        ax = len(nya.captured(1))
        if ax != 0:
            self.setFormat(start, ax, stile[0])
            start = start + ax
        ax = len(nya.captured(3))
        #Альтернативно
        n = 4
        while nya.captured(n) != '' and n < 21 :#вероятно, избыточное условие
            self.nesting(n, nya, start, ax, stile)
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))
        ax = len(nya.captured(21))
        if ax != 0:
            self.setFormat(start, ax, stile[7])
            start = start + ax
        self.base.current_g_cod_pool[self.count][7] = nya.captured(22) or None
        ax = len(nya.captured(23))
        if ax != 0:
            self.setFormat(start, ax, stile[8])
            #start = start + ax
        self.base.current_g_cod_pool[self.count][8] = nya.captured(24) or None
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