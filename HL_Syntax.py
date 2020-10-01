import sys

from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter
from PyQt5.QtCore import QRegExp, QRegularExpression
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


class GMHighlighter (QSyntaxHighlighter):
    """Синтаксические маркеры для языка Python. """
    # Python keywords
    axises = [
        'X', 'Y', 'Z', 'C', 'A', 'B', 'F'
    ]

    #condition operators
    condition_operators = ['WHILE', 'IF']

    # comment braces
    comment_braces = ['\([\w.]*\)']

    #condition braces
    logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']
    #condition_braces = ['\([\w.]*\)']

    #G-func
    g_cod = ['G0', 'G1', 'G2', 'G3']

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)
        rules = []
        # Keyword, operator, and brace rules


        rules += [(r'{}(-)?(\d+.(\d*))'.format(a), 0, STYLES['axis'])
                  for a in GMHighlighter.axises]

        rules += [(r'{}'.format(g), 0, STYLES['g_cod'])
                  for g in GMHighlighter.g_cod]

        # comment rules
        rules += [(r'{}'.format(GMHighlighter.comment_braces[0]), 0, STYLES['comment_brace'])]#rules += [(r'\([\w.]*\)', 0, STYLES['string'])]


        # Создайте QRegExp для каждого шаблона
        self.rules = [(QRegularExpression(pat), index, fmt)
            for (pat, index, fmt) in rules]
        #for i in self.rules:
        #    print(i)


    def highlightBlock(self, text):
        """Применить выделение синтаксиса к данному блоку текста. """
        # Сделайте другое форматирование синтаксиса
        for expression, nth, format in self.rules:
            #print('for start:', expression, nth, format )
            #index = expression.indexIn(text, 0)
            nya = expression.match(text, 0)
            index = nya.capturedStart()

            while index >= 0:
                nya = expression.match(text, index)
                index = nya.capturedStart()
                length = nya.capturedEnd() - index
                self.setFormat(index, length, format)
                nya = expression.match(text, nya.capturedEnd())
                index = nya.capturedStart()

        self.setCurrentBlockState(0)

