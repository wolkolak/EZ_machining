from PyQt5.QtCore import QRegularExpression
from abc import ABC
from PyQt5.QtGui import QColor, QTextCharFormat, QFont
#from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.avaliable_math_logic_operators import *
#from Redactor.G_MODAL_commands import G_MODAL_DICT
import importlib
import sys
from os import listdir
from os.path import isfile, join
import numpy as np
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.postfix4tokens import string2postfix_tuple, tokensPostfixing


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
    'comment': format('Gray', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
    'if_while': format('magenta', 'italic'),
    'label':    format('brown', 'italic'),
    'condition': format('darkMagenta', 'italic'),
    'R = ': format('darkGreen', 'italic')
}


STYLES_list_G0 = [
    #, 'italic' это перебор
    format('blue'),     #N100
    format('gray'),     #G40
    format('blue'),     #'interpolation':
    format('#c9211e'),  #'g_cod_X':
    format('#0084d1'),  #'g_cod_Y':
    format('#468a1a'),  #'g_cod_Z':
    format('#650953'),  #'g_cod_A':
    format('#813709'),  #'g_cod_B':
    format('#ff5429'),  #'g_cod_C':
    format('#c9211e'),  #I
    format('#0084d1'),  #J
    format('#468a1a'),  #K
    format('gray'),     #R
    format('blue'),     #F
]

STYLES_list_G1 = [
    format('blue', 'bold'),     # N100
    format('gray', 'bold'),     # G40
    format('blue', 'bold'),     #'interpolation':
    format('#c9211e', 'bold'),  #'g_cod_X':
    format('#0084d1', 'bold'),  #'g_cod_Y':
    format('#468a1a', 'bold'),  #'g_cod_Z':
    format('#650953', 'bold'),  #'g_cod_A':
    format('#813709', 'bold'),  #'g_cod_B':
    format('#ff5429', 'bold'),  #'g_cod_C':
    format('#c9211e', 'bold'),  # I
    format('#0084d1', 'bold'),  # J
    format('#468a1a', 'bold'),  # K
    format('gray', 'bold'),     #R
    format('blue', 'bold'),     #F
]

#dict_for_GOTO_inCASE = {'': DICTshiftsINT['GOTO'], 'F': DICTshiftsINT['GOTOF'], 'B': DICTshiftsINT['GOTOB'], 'C': DICTshiftsINT['GOTOC'], 'S': DICTshiftsINT['GOTOS']}







class ReversalPostProcessor0(ABC):#metaclass=ABCMeta
    """ this is abstract ZERO simulator. If u writing simulator different from any, use it as parent and do your best.
    u need override special_commands list then.
    To add command, create behavior function; add to special_commands list string, color, style.
    Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as part,
    order matters.

    Lets divide the rule type np[14] by groups: nan - ordinary line, 0 - absolute move somewhere like G28,
    9999 - empty line, 9998 - comment line, 9997 - unidentified line, 1 - G modal command, 2 - machining cycles,
    3 - creating vars, 4 - logic cycles and conditions.
    """


    def __init__(self, redactor):
        self.redactor = redactor
        self.CNC_op_type = 'Fanuc_op'
        #self.update_rules()
        #self.stright_G2_G3 = True
        #self.siemens_ijk = False
        #self.sub_programs_static = sub_programs()
        #self.
        self.ARK_modal = 3#or 0 if not
        self.brackets = ['[', ']', '(', ')']
        X = 'X';        Y = 'Y';        Z = 'Z';        A = 'A';        B = 'B';        C = 'C'
        self.AXISnames = [X, Y, Z, A, B, C]
        I, J, K, R = 'I', 'J', 'K', 'R'  # R_how_it_look = 'CR='
        self.RIJK = [R, I, J, K]

        self.G_MODAL_DICT_in_proc = {'plane': '18', 'absolute_or_incremental': '90', 'polar_coord': '113', 'SC': '54', 'polar_coord_16': '15'}
        #todo Отправить всю эту красоту в np_box

        self.condition_operators = ['WHILE', 'IF']

        # comment braces
        self.comment_braces = ['(;?\s*\(.*\))?'] #todo для анализа нужно будет добавить подсчёт открытия/закрытия скобок
        self.comment_start = '('

        # condition braces
        self.logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']
        self.condition_braces = ['\([\w.]*\)']#todo не используется
        #self.OPs_with_different_rules = {DICTshiftsINT['CASE']: [CASE_color, CASE_feed_dict], DICTshiftsINT['REPEAT_LB']: [REPEAT_LB_color, REPEAT_LB_feed_dict]}#DICTshiftsINT['REPEATu']: [REPEATu_color, REPEATu_insert],
        self.OPs_with_different_rules = {}  # DICTshiftsINT['REPEATu']: [REPEATu_color, REPEATu_insert],
        self.update_options_postprocessor()
        self.my_name()
        print('Siemens created END')

    def correct_lbl(self, lbl:str):
        print('correct_lbl')
        print(f'1 lbl={lbl}|')
        ind = lbl.find(':')
        lbl = lbl[:ind]
        print(f'2 lbl={lbl}|')
        return lbl

    def my_name(self):
        self.full_name = sys.modules[self.__module__].__file__
        index = self.full_name.rfind('\\')
        self.last_name = self.full_name[index + 1:]

    def update_options_postprocessor(self):
        #self.k_XYZABC_dict = []
        print('update_options_postprocessor')
        #for i in 'XYZABC':
        #    #print('k_XYZABC_list = ', self.k_XYZABC_list)
        #    #print('self.redactor.current_machine = ', self.redactor.current_machine)
        #    self.k_XYZABC_list.append(self.redactor.current_machine.k_XYZABC[i])
        #self.k_XYZABC_dict = self.redactor.current_machine.k_XYZABC#may be does not needed
        self.update_rules()

    def sub_programs(self):
        sub_program_names = {}
        return sub_program_names

    #def k_applying(self, visible_np):
    #    visible_np[:, 4] = visible_np[:, 4] * self.k_XYZABC_dict['X']
#
    #def k_devide_applying(self, visible_np):
    #    visible_np[:, 4] = visible_np[:, 4] / self.k_XYZABC_dict['X']


    def Rad_applying(self, visible_np):
        #pass

        visible_np[:, 7] = np.radians(visible_np[:, 7])
        visible_np[:, 8] = np.radians(visible_np[:, 8])
        visible_np[:, 9] = np.radians(visible_np[:, 9])

    def check_command(self, lineBlock, text, np_line, count, g_modal):
        # это при чтении
        # нужно в список
        # верну малый список для одной строки

        # print('CHECK COMMAND START')
        command_dict = {}
        result = False
        #нуэно список новых параметров притащить
        for i in range(len(self.special_commands)):
            nya = self.special_commands[i][0].match(text, 0)
            len_match = nya.capturedLength()
            if len_match != 0:
                key, value = self.special_commands[i][1](lineBlock, nya, np_line, count, g_modal, i)
                command_dict[key] = value
                result = True
        if result is not True:
            np_line[16] = 9999
        return result, command_dict
        #print('CHECK COMMAND END')


    #def return_form_for_sub_program_mask(self):
    #    return QRegularExpression('^' + '' + '$')

    def sub_programs_current(self, cat):
        sub_program_names = {}
        try:
            f_c = [f for f in listdir(cat) if isfile(join(cat, f))]
            print('f_c = ', f_c)
            if len(f_c) > 0:
                for f1 in f_c:
                    if f1.endswith('.spf') or f1.endswith('.mpf') or f1.endswith('.SPF') or f1.endswith('.MPF'):
                        sub_program_names[f1[:-4].lower()] = cat + '/' + f1
                        sub_program_names[f1[:-4].lower() + '_' + f1[-3:].lower()] = cat + '/' + f1
        except:
            print('Mother catalogue for current file was not found. It\'s subprograms not included' )
        print('sub_program_names current = ', sub_program_names)
        return sub_program_names







    def update_rules(self):
        """Синтаксические маркеры для языка. """
        # G-func
        # g_cod = ['G0', 'G1', 'G2', 'G3']
        # axises
        # todo perl выражения должны заимствоваться из псведопостпроцессора
        axises0 = self.AXISnames
        #axises = ['X', 'Y', 'Z', 'A', 'B', 'C']  # - , 'G', 'F'
        g_prefix = r'(\s?G0?([0123])\s*)?'
        #f_postfix = r'(F\s*(\d+(\.\d*)?\s*))?'#todo вопрос: а не должен ли "?" стоять в конце?
        f_postfix = r'(F\s*(\d+.?\d*\s*))?'
        NumberN = r'(\s?N(\d+)\s*)?'
        Corrector = r'(\s?G(4[0123]\.?\d*)\s*)?'
        i_postfix = '(' + self.RIJK[1] + r'(-?\d+\.\d*)\s*)?'#todo сейчас только R реализован для несортированного варианта
        j_postfix = '(' + self.RIJK[2] + r'(-?\d+\.\d*)\s*)?'
        k_postfix = '(' + self.RIJK[3] + r'(-?\d+\.\d*)\s*)?'
        r_postfix = '(' + self.RIJK[0] + r'(-?\d+\.\d*)\s*)?'
        # most strings look like 'main_rule'
        #ark_postfix_sort =
        #I, J, K, R = 'I', 'J', 'K', 'R'  # R_how_it_look = 'CR='
        R, I, J, K = self.RIJK
        sorted_axis_rule = ''
        for letter in axises0:
            sorted_axis_rule += r'(\s*(?:{})(-?\d+\.\d*)\s*)?'.format(letter)
            # sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)

        self.sorted_axis_rule = '^' + NumberN + Corrector + g_prefix + sorted_axis_rule + i_postfix + j_postfix + k_postfix + r_postfix + f_postfix + ';?$'  # '(?:G0?\d)?\s*'   + f_postfix

        # sorted_axis_rule = r'^(?:X)(\d)$'  # UDALIT

        #axises_str = ''.join([*self.AXISnames, I, J, K, R])
        axises_str = ''.join([*self.AXISnames])
        #ijk_str = I + J + K

        axises_coord = r'(\s*([{}])\s*(-?\d+\.\d*)\s*)?'.format(axises_str)

        #ijk_coord = r'(([{}])\s*(-?\d+\.\d*)\s*)?'.format(ijk_str)
        # unsorted_axis_rule = r'(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)#r'^\d((?:X)(-?\d+\.\d*)\s*)$'

        #unsorted_axis_rule_ = axises_coord * 10 #+ ijk_coord * 3


        ijk_str = I + J + K
        ijk_coord = r'(([{}])\s*(-?\d+\.\d*)\s*)?'.format(ijk_str)
        unsorted_axis_rule_ = axises_coord * 6 + ijk_coord * 3

        #NumberN = r'(\s?N(\d+)\s*)?'
        #NumberN = r'(\s?N(\d+)\s*)?' #-одинаково инфа сотка
        #starts = '^(\s*)' + NumberN
        #ends = '(\(.*\))?\s*$'
        #Label = '(.*:\s*)?'
        #long_starts = starts + Label

        Corrector_g_prefix_unsorted = '((\w*:\s*))?' + r'(\s*G(0?[0123]|4[012])\s*)?' * 2#(\s*) добавил вначале
        #теперь нужно починить распознавание unsorted в HL_Sntax как минимум
        unsorted_axis_rule_ = NumberN + Corrector_g_prefix_unsorted + unsorted_axis_rule_ + r_postfix + f_postfix + self.comment_braces[0]
        self.unsorted_axis_rule = '^' + unsorted_axis_rule_ + ';?$'
        #self.make_3d_big_rule()

        #ax_vars = r'(([{}])\s*(-?(\d+\.\d*)|(#\d+)|(\[.*\])\s*))?'.format(axises_str)
        # ax_vars = r'(([XYZIJKRABC])\s * (-?(\d+\.\d *) | (  # \d+)|(\[[^\]]*\]))\s*)?'
        #ax_vars = r'(([{}])\s*(-?(\d+\.\d*)|(#\d+)|(\[.*\]))\s*)?'.format(axises_str)#.*[^\[\]]


        axises_str_vars_rule = axises_str#.join(Rvars)#.join(ijk_coord * 3)
        print('555 axises_str_vars_rule = ', axises_str_vars_rule)
        #sample = r'(([{}])\s*((-?\s*\d+\.\d*)|(-?\s*#\d+)|(-?\s*\[[^\]]*\]))\s*)?'
        sample = r'(([{}])\s*((-?\s*\d+\.\d*)|(-?\s*#\d+)|(-?\s*\[.*?\]))\s*)?'
        ax_vars = sample.format(axises_str_vars_rule)#axises_str

        unsorted_rule_ax_vars_ = ax_vars * 6#r'\s*' +

        ijk = sample.format('IJK')
        equality_with_siemens_AR =  3*r'(()(()|()|()))?'#r'()()()()()()'  #
        unsorted_rule_ax_vars_ = unsorted_rule_ax_vars_ + ijk * 3 + r'(({})\s*(-?(\d+\.\d*)|(#\d+)|(\[[^\]]*\]))\s*)?'.format(R) + equality_with_siemens_AR

        #r'(({})\s*(-?(\d+\.\d*)|(#\d+)|(\[[^\]]*\]))\s*)?'.format(R)

        #add_R_AR = r'(({}\s*)\s*(-?(\d+\.?\d*)|(R\d+)|([^;]*))\s*)?'
        #add_AR = add_R_AR.format('AR\s*=')

        unsorted_rule_ax_vars_ = '^' + NumberN + Corrector_g_prefix_unsorted + unsorted_rule_ax_vars_ + f_postfix + self.comment_braces[0] + ';?$'

        self.unsorted_rule_ax_vars = unsorted_rule_ax_vars_


        self.assemble_tools_register()
        self.sub_programs_static = self.sub_programs()
        print(f'222 sub_programs_static = {self.sub_programs_static}')
        #todo Нужна функция для подхватывания и замены функций инструментов в scene0 и в вычислениях, который ещё не прописаны
        self.MATH_operators()
        self.SHIFT_operators()


    def assemble_tools_register(self):
        m = self.redactor.current_machine
        scene0 = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL
        path = m.bound_register
        path = 'Modelling_clay/tool_registers/' + path
        tool_dict = {}
        print('PATH ||| = ', path)
        with open(path, 'r', encoding='utf8') as register:
            for line in register:
                mask, address = line.split('===')
                address = address[:-1]
                print('mask = {}, address = {}'.format(mask, address))
                tools_main_catalog = 'Modelling_clay/machine_tools/'
                L = len(tools_main_catalog)
                catalog0 = address[L:]
                print('m.bound_register = ', m.bound_register)

                catalog0, _ = catalog0.split('\\', 1)
                print('catalog0 = ', catalog0)
                func_address = tools_main_catalog + catalog0 + '/' + '__init__'#.py
                #func_address = r'Modelling_clay/machine_tools/turn_cut/__init__'
                func_address = func_address.replace('/', '.')
                module = importlib.import_module(func_address)
                ToolFunction = module.init__tool
                ToolWay = module.tip_tool_way
                ToolDict = {}
                with open(address, 'r') as tool_dict_file:
                    for line2 in tool_dict_file:
                        var_, value_ = line2.split('=', 1)
                        ToolDict[var_] = value_
                tool_dict[mask] = [ToolFunction, ToolDict, ToolWay]

                #print('catalog0 = ', catalog0)
                #init_func =
        self.tool_dict = tool_dict
        print('tool list = ', tool_dict)



    def MATH_operators(self):
        print(f'MATH_operators: {self.CNC_op_type}')
        try:
            s = 'Modelling_clay.Processors.Processor_base.{}'.format(self.CNC_op_type)# as op_module
            #print('s = ', s)
            op_module = importlib.import_module(s)
            print(f'try op_module = {op_module}')
        except:
            print(f'except, грузим фанук')
            import Modelling_clay.Processors.Processor_base.Fanuc_op as op_module

        NumberN = r'(N(\d+)\s*)?'
        #print('START_EXP: ', op_module.START_EXP_var)
        #START_EXP_param  = op_module.START_EXP_param
        START_EXP_var = op_module.START_EXP_var
        #self.START_EXP_param = QRegularExpression('^' + NumberN + START_EXP_param)#+ '()'Number
        self.START_EXP_var = QRegularExpression('^' + NumberN + START_EXP_var)

        self.DICT_BRACKETS = op_module.DICT_BRACKETS
        self.OPERATORs_DICT_math = op_module.OPERATORs_DICT_math; self.OPERATORs_DICT_math_U = op_module.OPERATORs_DICT_math_U
        self.OPERATORs_DICT_compare1 = op_module.OPERATORs_DICT_compare1; self.OPERATORs_DICT_compare2 = op_module.OPERATORs_DICT_compare2
        self.OPERATORs_DICT_logic_L = op_module.OPERATORs_DICT_logic_L; self.OPERATORs_DICT_func_1 = op_module.OPERATORs_DICT_func_1
        self.OPERATORs_DICT_func_2 = op_module.OPERATORs_DICT_func_2; self.OPERATORs_PRECEDENCE_DICT = op_module.OPERATORs_PRECEDENCE_DICT
        self.OPERATORs_DICT_binary_between = op_module.OPERATORs_DICT_binary_between; self.DICT_VARS = op_module.DICT_VARS


    def SHIFT_operators(self):
        #'GOTO': 14,
        #'GOTOC': 15,  # GOTO without error
        #'GOTOS': 16,  # to start of the program
        #'GOTOB': 17,  # backward direction
        #'GOTOF': 18,  # forward direction
        ## 'REPEAT_LB':    19,
        #'R = ': 30,
        #'LABEL': 40

        #NumberN = r'(N(\d+)\s*)?'
        NumberN = r'(N(\d+)\s*)?'
        #starts = '^(\s*)' + NumberN
        starts = '^(\s*)' + NumberN
        #ends = '(\(.*\))?\s*$'#todo or ;
        ends = '(;.*)?$'  # todo or ;
        Label = '([^;\(\)]*:\s*)?'
        long_starts = starts + Label
        #todo временно для сименса
        self.label = long_starts

        #last_part = '([^\{}]*)'.format(self.brackets[2])

        p = '([^GOTO]+)'#)|(DEFAULT)

        #p = '(.*)'
        #это всё неверно конечно
        of_goto = '(' + '(\s+)' + '(\d+)' + '(\s*GOTO([FBCS])?\s*)'+ p + ')?'

        case_default_str = '(' + '(DEFAULT)' + '(\s*GOTO([FBCS])?\s*)'+ '([^;]+)'+ ')?'
        #case_default_str = '(.*)'

        #case_str = '(CASE\s*)' + '\((.*)\)'+ '(OF\s*) ' + '(.*)'# of_goto#*5 + case_default_str

        #case_str = '(CASE\s*)' + '(\(.*\))' + r'(\s*OF)' + of_goto * 7 + case_default_str#+ '(.*)'       \t*
        center_sub = '(^)?(\w*)\s*(\([^\(\)]+\))?'  # для сименса сейчас subr1 и subr2(x=2, z=8)

        SHIFT_masks = {#отдельно сделать переменные и метки
            #long_starts + '(IF)' + '(.*)' + '(THEN)' + last_part + ends: DICTshiftsINT['IF_THEN'],
            #long_starts + '(IF)' + '(.*)' + '(GOTOF)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            #long_starts + '(IF)' + '(.*)' + '(GOTOB)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            #long_starts + '(IF)' + '(.*)' + '(GOTOC)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            #long_starts + '(IF)' + '(.*)' + '(GOTOS)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            #long_starts + '(IF)'    + '(.*)' + '(GOTO)'   + last_part +     ends: DICTshiftsINT['IF_GOTO'],
            #long_starts + '(IF)' + '(.*)' +                                 ends: DICTshiftsINT['IF'],
            #long_starts + '(ELIF)'  + '(.*)' + '(GOTO)' + last_part +       ends: DICTshiftsINT['ELIF'],#todo в исменс не надо, в фанук - тоже
            #long_starts + '(ELSE)'  + '(\s*)' +                             ends: DICTshiftsINT['ELSE'],
            #long_starts + '(ENDLOOP)' +                                     ends: DICTshiftsINT['END_LOOP'],  # '(\s*)' +
            #long_starts + '(ENDIF)' + '(\s*)' +                             ends: DICTshiftsINT['ENDIF'],
            #long_starts + '(ENDFOR)' +      '(\s*)' +                       ends: DICTshiftsINT['END_FOR'],  # '(\s*)' +
            #long_starts + '(WHILE)' + '(.*)' + '(DO)' + last_part +         ends: DICTshiftsINT['WHILE'],
            #long_starts + '(END)'   +     last_part +                       ends: DICTshiftsINT['ENDWHILE'],#'(\s*)' +
            #long_starts + '(LOOP)'  +                                       ends: DICTshiftsINT['LOOP'],#+ '(\s*)'
            #long_starts + '(REPEAT\s*)' +                                      ends: DICTshiftsINT['REPEATu'],#'(\s*)' +
            #long_starts + '(UNTIL\s+)' +      '([^;]+)'           +               ends: DICTshiftsINT['UNTIL'],#'(\s*)'
            #long_starts + '(FOR)' + '(.*)' + '(TO)' + last_part +           ends: DICTshiftsINT['FOR'],
            #long_starts + case_str                  +                        ends: DICTshiftsINT['CASE'],
            #long_starts + '(GOTOC)'  + last_part +                          ends: DICTshiftsINT['GOTOC'],
            #long_starts + '(GOTOS)'  + last_part +                          ends: DICTshiftsINT['GOTOS'],
            #long_starts + '(GOTOB)'  + last_part +                          ends: DICTshiftsINT['GOTOB'],
            #long_starts + '(GOTOF)'  + last_part +                          ends: DICTshiftsINT['GOTOF'],
            #long_starts + '(GOTO)' + last_part +                            ends: DICTshiftsINT['GOTO'],
            #long_starts + '(REPEAT(B)?)' + '(\s+(\w+))?'  +'(\s+(\w+))?' + '(\s+P\s*=\s*([^;]+))?' + '(\s*)' + ends: DICTshiftsINT['REPEAT_LB'],
            #long_starts + '((\w*\d*)|(\#\d*))(\s*=\s*)(.*)' +               ends: DICTshiftsINT['R = '],
            #long_starts + '(\(.*\))' + ends: DICTshiftsINT['LABEL'],
            ##long_starts + center_sub + ends: DICTshiftsINT['SUB_PROGRAM'],
        }

        self.SUBprogram_mask = QRegularExpression(long_starts + center_sub + ends)
        self.SHIFT_masks = {}
        for k, v in SHIFT_masks.items():
            self.SHIFT_masks[QRegularExpression(k)] = v


