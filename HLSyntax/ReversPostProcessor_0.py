from PyQt5.QtCore import QRegExp, QRegularExpression
from abc import ABC, abstractmethod


class ReversalPostProcessor0(ABC):#metaclass=ABCMeta
    """ this is abstract ZERO simulator. If u writing simulator different from any, use it as parent and do your best.
    u need override special_commands list then.
    To add command, create behavior function; add to special_commands list string, color, style.
    Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as part,
    order matters.
    """
    #__metaclass__ = ABCMeta
    #@abstractmethod
    def __init__(self):
        self.start_pointXYZ = [500., 0., 50., 0., 0., 0]
        self.k_XYZCAB = {'X': 1.,
                         'Y': 1.,
                         'Z': 1.,
                         'C': 1.,
                         'A': 1.,
                         'B': 1.,
                         }


        self.condition_operators = ['WHILE', 'IF']

        # comment braces
        self.comment_braces = ['\([\w.]*\)']

        # condition braces
        self.logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']
        self.condition_braces = ['\([\w.]*\)']



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
        visible_np[:, 1] = visible_np[:, 1] * self.k_XYZCAB['X']

    def check_command(self, text, np_line, g_modal):
        print('CHECK COMMAND START')
        for i in range(len(self.special_commands)):
            #print('i[0] = ', i[0])
            nya = self.special_commands[i][0].match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                self.special_commands[i][1](nya, np_line, g_modal, i)
                return
        if len_match == 0:
            np_line[10] = 9999
        print('CHECK COMMAND END')