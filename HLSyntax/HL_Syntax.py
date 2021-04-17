import sys
import time
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QRegExp, QRegularExpression, pyqtSignal, QEventLoop
from PyQt5.QtWidgets import *

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
    'g_cod': format('red'),
    'comment_brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class GMHighlighter(QSyntaxHighlighter):


    """Синтаксические маркеры для языка. """
    # G-func
    g_cod = ['G0', 'G1', 'G2', 'G3']
    # axises
    axises = ['X', 'Y', 'Z', 'C', 'B', 'A', 'R']
    # most strings look like 'main_rule'

    sorted_axis_rule = ''
    for letter in axises:
        sorted_axis_rule += r'((?:{})(-?\d+\.\d*)\s*)?'.format(letter)
        #sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)
    sorted_axis_rule = '^' + '(?:G\d+)?\s*' + sorted_axis_rule + '$'
    #print('nabor XYZ:', sorted_axis_rule)

    main_rule = sorted_axis_rule

    axises_str = ''.join(axises)
    axises_coord = r'([{}]\s*(-)?(\d+\.\d*)\s*)'.format(axises_str)
    second_rule = r'^(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)
    #condition operators
    condition_operators = ['WHILE', 'IF']

    # comment braces
    comment_braces = ['\([\w.]*\)']

    #condition braces
    logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']
    #condition_braces = ['\([\w.]*\)']

    #rehighlightBlock.connect

    #countChanged = pyqtSignal(int)

    def __init__(self, document, base):
        QSyntaxHighlighter.__init__(self, document)
        self.max_number_ax = [i*2 for i in range(1, 8)]
        self.base = base
        self.count = 0
        self.count_in_step = 0
        self.const_step = 1000
        self.standart_step = self.const_step
        rules = []
        # Keyword, operator, and brace rules
        # main rule
        #rules += [(r'{}'.format(GMHighlighter.axises), 0, STYLES['axis'])]#r'{}(-)?(\d+.(\d*))'
        #rules += [(r'{}'.format(GMHighlighter.main_rule), 0, STYLES['axis'])]
        rules += [(r'{}'.format(GMHighlighter.second_rule), 0, STYLES['axis'])]
        #rules += [(r'{}'.format(g), 1, STYLES['g_cod'])
        #          for g in GMHighlighter.g_cod]

        #rules += [(r'({})(-)?(\d+.(\d*))'.format(a), 0, STYLES['axis'])#r'{}(-)?(\d+.(\d*))'
        #         for a in GMHighlighter.axises]

        #rules += [(r'([XYZCAB])(-)?(\d+.(\d*))', 0, STYLES['axis'])]

        # comment rules
        rules += [(r'{}'.format(GMHighlighter.comment_braces[0]), 2, STYLES['comment_brace'])]#rules += [(r'\([\w.]*\)', 0, STYLES['string'])]


        # Создайте QRegExp для каждого шаблона
        self.first_rule = [QRegularExpression(self.main_rule), 0, STYLES['axis']]
        self.rules = [(QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules]
        self.main_rule_regular_expression = self.first_rule[0]
        self.main_format = self.first_rule[2]
        self.second_rule_regular_expression = self.rules[0][0]
        self.second_format = self.rules[0][2]

        self.too_little_number_check()

    def too_little_number_check(self):
        if self.base.delta_number_of_lines < self.const_step:
            self.standart_step = self.base.delta_number_of_lines

    def highlightBlock(self, text):
        """Применить выделение синтаксиса к данному блоку текста. """

        #if self.base.editor._document.isModified():
        #print('waiting')
        #print('delta_number_of_lines', self.base.delta_number_of_lines)
        #time.sleep(5)

        common_length = 0

        nya = self.main_rule_regular_expression.match(text, 0)
        #print('nya0 = ', nya.captured(0))
        index = nya.capturedStart()
        len_match = nya.capturedLength()
        if len_match != 0:
            self.setFormat(index, len_match, self.main_format)
            #print('self.base.current_g_cod_pool[0]  = ', self.base.current_g_cod_pool[0])
            #print('nya = ', nya.captured())
            self.recount(nya, text)
            #print('main rule! index = {}, string = {}'.format(index, text))
        elif index == 0:#empty string
            self.recount2(nya)
            #print('index = {}, string = {}, запуск дополнительных правил'.format(index, text))
        else:
            self.recount(nya, text)
        #nya = self.second_rule_regular_expression.match(text, 0)
        #index = nya.capturedStart()
        #if index != -1:
        #    self.setFormat(index, nya.capturedLength(), self.second_format)
        #    self.recount(nya)
        #    return

        #for expression, nth, format in self.rules:
        #    nya = expression.match(text, 0)
        #    index = nya.capturedStart()
        #    print('index = nya.capturedStart() = ', index)
        #    while index >= 0:
        #        end = nya.capturedEnd()
        #        length = end - index
        #        self.setFormat(index, length, format)
        #        common_length += length
        #        #print('captured string: {}, GROUP: {}'.format(nya.captured(), nth))#capturedTexts()
        #        nya = expression.match(text, end)
        #        index = nya.capturedStart()



        #self.setCurrentBlockState(0)
        #print('здесь')
        #self.recount(nya)#нужен отдельный реконт

    def recount2(self, nya):
        #print('recount start2, count = {}, nya = {}'.format(self.count, nya.captured(0)))
        # print('recount поместил в self.base.current_g_cod_pool[{}]: {}'.format(self.count, self.base.current_g_cod_pool[self.count]))
        self.count_in_step += 1
        self.count += 1

        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar

        return

    def recount(self, nya, self_block):
        #print('recount start, count = {}, nya = {}, self.standart_step={}'.format(self.count, nya.captured(0), self.standart_step))
        self.base.current_g_cod_pool[self.count] = [nya.captured(i) or None for i in self.max_number_ax]
        #print('type  self_block', type(self_block))
        #self_block.setUserData('ff')
        #print('recount поместил в self.base.current_g_cod_pool[{}]: {}'.format(self.count, self.base.current_g_cod_pool[self.count]))
        self.count_in_step += 1
        self.count += 1

        if self.count_in_step == self.standart_step:
            #print('count step = standart step, self.count = {}, bar.maximum = {}'.format(self.count, self.base.progress_bar.maximum()))
            self.base.on_count_changed(self.count)  # progressBar
            #QApplication.processEvents(QEventLoop.WaitForMoreEvents)
        return

    def to_the_start(self):
        self.standart_step = 1
        self.count = 0
        self.base.progress_bar.setMaximum(1)
        print("the end")