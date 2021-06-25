from PyQt5.QtCore import QRegExp, QRegularExpression
from abc import ABC, abstractmethod
from PyQt5.QtGui import QColor, QTextCharFormat, QFont

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


STYLES_list_G0 = [#todo По-хорошему это бы тоже перенести в постпроцессор
    #, 'italic' это перебор
    format('blue'), #'axis':
    format('#c9211e'),#'g_cod_X':
    format('#0084d1'),#'g_cod_Y':
    format('#468a1a'),#'g_cod_Z':
    format('#650953'),#'g_cod_A':
    format('#813709'),#'g_cod_B':
    format('#ff5429'),#'g_cod_C':
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

class ReversalPostProcessor0(ABC):#metaclass=ABCMeta
    """ this is abstract ZERO simulator. If u writing simulator different from any, use it as parent and do your best.
    u need override special_commands list then.
    To add command, create behavior function; add to special_commands list string, color, style.
    Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as part,
    order matters.
    """


    def __init__(self):
        self.update_rules()
        self.start_pointXYZ = [500., 0., 50., 0., 0., 0]
        self.k_XYZABC = {'X': 1.,
                         'Y': 1.,
                         'Z': 1.,
                         'C': 1.,
                         'A': 1.,
                         'B': 1.,
                         }
        self.k_XYZABC_list = []
        self.update_options_postprocessor()

        self.condition_operators = ['WHILE', 'IF']

        # comment braces
        self.comment_braces = ['\([\w.]*\)']

        # condition braces
        self.logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']
        self.condition_braces = ['\([\w.]*\)']

    def update_options_postprocessor(self):
        self.update_rules()
        self.k_XYZABC_list = []
        for i in 'XYZABC':
            #print('k_XYZABC_list = ', self.k_XYZABC_list)
            self.k_XYZABC_list.append(self.k_XYZABC[i])

        #EXAMPLE
   #     self.special_commands = [['G28 U0. V0.', self.G28_U0_V0, format('#468a1a', 'bold')]]
   #     for i in range(0, len(self.special_commands)):
   #         self.special_commands[i][0] = [QRegularExpression('^' + self.special_commands[i][0] + '$')]
   #         # look Perl RegularExpressions if u need
   #     print('self.special_commands = ', self.special_commands)
   #
   # def G28_U0_V0(self, nya, np_line):
   #     print('G28_U0_V0')

    def k_appliying(self, visible_np):
        visible_np[:, 2] = visible_np[:, 2] * self.k_XYZABC['X']
        #visible_np[:, 11] = visible_np[:, 1] * self.k_XYZCAB['X']

    def check_command(self, lineBlock, text, np_line, g_modal):
        print("type(lineBlock) = ", type(lineBlock))
        print('CHECK COMMAND START')
        for i in range(len(self.special_commands)):
            #print('i[0] = ', i[0])
            nya = self.special_commands[i][0].match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                self.special_commands[i][1](lineBlock, nya, np_line, g_modal, i)
                return
        if len_match == 0:
            np_line[14] = 9999
        print('CHECK COMMAND END')

    def update_rules(self):
        """Синтаксические маркеры для языка. """
        # G-func
        # g_cod = ['G0', 'G1', 'G2', 'G3']
        # axises
        # todo perl выражения должны заимствоваться из псведопостпроцессора
        axises0 = ['X', 'Y', 'Z', 'A', 'B', 'C']
        I, J, K, R = 'I', 'J', 'K', 'R'  # R_how_it_look = 'CR='
        axises = ['X', 'Y', 'Z', 'A', 'B', 'C', I, J, K, R]  # - , 'G', 'F'
        g_prefix = r'(G0?([0123])\s*)?'
        f_postfix = r'(F(\d+.\d*))?\s*'
        i_postfix = '(' + I + r'(\d+.\d*))?\s*'
        j_postfix = '(' + J + r'(\d+.\d*))?\s*'
        k_postfix = '(' + K + r'(\d+.\d*))?\s*'
        r_postfix = '(' + R + r'(\d+.\d*))?\s*'
        # most strings look like 'main_rule'

        sorted_axis_rule = ''
        for letter in axises:
            sorted_axis_rule += r'((?:{})(-?\d+\.\d*)\s*)?'.format(letter)
            # sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)

        self.sorted_axis_rule = '^' + g_prefix + sorted_axis_rule + f_postfix + '$'  # '(?:G0?\d)?\s*'   + f_postfix

        # sorted_axis_rule = r'^(?:X)(\d)$'  # UDALIT

        axises_str = ''.join(axises0)
        axises_coord = r'(([{}])\s*(-?\d+\.\d*)\s*)?'.format(axises_str)

        # unsorted_axis_rule = r'(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)#r'^\d((?:X)(-?\d+\.\d*)\s*)$'

        unsorted_axis_rule = axises_coord * 6
        unsorted_axis_rule = g_prefix + unsorted_axis_rule + i_postfix + j_postfix + k_postfix + r_postfix + f_postfix
        self.unsorted_axis_rule = '^' + unsorted_axis_rule + '$'
