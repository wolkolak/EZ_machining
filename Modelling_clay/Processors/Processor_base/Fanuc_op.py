from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.avaliable_math_logic_operators import *

#№НЕТ. не так.

#START_EXP = '\s*([#]\d+)\s* =\s*(.*)$'
#START_EXP_param = '\s*([#]\d+)\s* =\s*(.*)$'

START_EXP_var = '\s*(.*)\s* =\s*(.*)$'

#START_EXP2 = '^' + '^'#todo don't need right now

OPERATORs_DICT_math = {
            '-': operator.sub,
            '+': operator.add,
            '*': operator.mul,
            '/': divide,
            #'^': operator.pow
        }

OPERATORs_DICT_math_U = {
            '_': unary_minus,
        }

OPERATORs_DICT_compare1 = {
            #"<": operator.lt,
            "=": start_solving,
            #">": operator.gt,
        }

OPERATORs_DICT_compare2 = {
            #"<=": operator.le,
            #"==": operator.eq,
            #"<>": operator.ne,
            #">=": operator.ge,
        }

OPERATORs_DICT_logic_L = {
    'AND': operator.and_,
    'NOT': operator.not_,
    'OR': operator.or_,
    'XOR': operator.xor,
    'GE': operator.ge,
    'GT': operator.gt,
    'EQ': operator.eq,
    'NE': operator.neg,
    'LT': operator.lt,
    'LE': operator.le,
    'mod':      operator.mod,
        }

OPERATORs_DICT_func_1 = {

            'SQRT': math.sqrt,
            'ABC': operator.abs,
            'INT': int_from_float,
            'NEG': operator.inv,
            'MOD': operator.mod,
            'SIN': sin,
            'COS': cos,
            'TAN': tan,
            'ASIN': arcsin,
            'ACOS': arccos,
            'ATAN': atan,
            'EXP': math.exp
        }

OPERATORs_DICT_func_2 = {
            'POW2': operator.pow
        }

before_unar_arithmetic = {**OPERATORs_DICT_compare1, **OPERATORs_DICT_logic_L, **OPERATORs_DICT_compare2}
before_unar_arithmetic['('] = None
before_unar_arithmetic['^'] = None

OPERATORs_DICT_binary_between = {**OPERATORs_DICT_math, **OPERATORs_DICT_compare1, **OPERATORs_DICT_compare2,
                                         **OPERATORs_DICT_logic_L, **OPERATORs_DICT_func_2}

OPERATORs_PRECEDENCE_DICT = {
            '_':       3,
            '^':       4,
            '-':       1,
            '+':       1,
            '*':       2,
            '/':       2,
            'SQRT':    4,
            'POW1':    4,
            'POW2':    4,
            'ABC':     4,
            'INT':     4,
            'NEG':     4,
            'MOD':     4,
            'SIN':     4,
            'COS':     4,
            'TAN':     4,
            'ASIN':    4,
            'ACOS':    4,
            'ATAN':    4,
            "<":       0,
            "<=":      0,
            "==":      0,
            "!=":      0,
            ">=":      0,
            ">":       0,
            '=':      -5,
            'AND':    -4,
            'NOT':    -4,
            'OR':     -4,
            'XOR':    -4,
            'GE':      0,
            'GT':      0,
            'EQ':      0,
            'NE':      0,
            'LT':      0,
            'LE':      0
        }


DICT_VARS = {'pi': math.pi,
             #'#1': None,
            }


#DICT_BRACKETS = ['[', ']']#TODO: вообще не надо
DICT_BRACKETS = ['^^^', '$$$']


#DICTclassicCYCLES = {
#    'WHILE':        'ENDWHILE',
#    'ENDWHILE':     'WHILE',
#    'REPEAT':       'UNTIL',
#    'LOOP':         'END_LOOP',
#    'FOR':          'END_FOR',
#}
#
#
#
#DICTshiftsINT = {
#    'WHILE':    0,
#    'ENDWHILE': 1,
#    'IF':       2,
#    'ENDIF':    3,
#    'REPEAT':   4,
#    'UNTIL':    5,
#    'LOOP':     6,
#    'END_LOOP': 7,
#    'FOR':      8,
#    'END_FOR':  9,
#    'CASE':     10,
#    'DEFAULT':  11,
#    'IF_THEN':  12,
#    'IF_GOTO':  13,
#    'GOTO':     14,
#    'GOTOC':    15,  # GOTO without error
#    'GOTOS':    16,  # to start of the program
#    'GOTOB':    17,  # backward direction
#    'GOTOF':    18,  # forward direction
#    'LABEL':    19,
#    'R = ':     30,
#    'Label':    40
#
#}
#
#
##1 - Forward, 2 - Backward, 3 - From the start to the end, 4 - Nothing (next line)
#
## command: [1/2/3/4, [**words to look for]
## IF:   [1, [key_ELIF, key_ELSE, key_ENDIF]]
#
#DICTshift = {
#    'IF':       [1, [DICTshiftsINT['ELIF'], DICTshiftsINT['ELSE'], DICTshiftsINT['ENDIF']]],
#    'ELIF':     [1, [DICTshiftsINT['ELIF'], DICTshiftsINT['ELSE'], DICTshiftsINT['ENDIF']]],
#    'ELSE':     [1, [DICTshiftsINT['ENDIF'],]],
#    #'ENDIF':    [None],
#    'CASE':     [1, [DICTshiftsINT['OF'], DICTshiftsINT['DEFAULT']]],
#    'OF':       [1, [DICTshiftsINT['DEFAULT'],]],
#    #'DEFAULT':  [None],
#    'IF_THEN':  [3, [DICTshiftsINT['Label']]],
#    'IF_GOTO':  [3, [DICTshiftsINT['Label']]],
#    'GOTO':     [3, [DICTshiftsINT['Label']]],
#    'GOTOC':    [3, [DICTshiftsINT['Label']]],# GOTO without error
#    'GOTOS':    [3, [DICTshiftsINT['Label']]],# to start of the prog
#    'GOTOB':    [2, [DICTshiftsINT['Label']]],# backward direction
#    'GOTOF':    [1, [DICTshiftsINT['Label']]],# forward direction
#}

