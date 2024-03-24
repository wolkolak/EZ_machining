from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.avaliable_math_logic_operators import *
#from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT

#№НЕТ. не так.

#START_EXP_param = '\s*[R]\d+\s* = \s*$'

#START_EXP2 = '\s*\$[S]\s* = \s*'

START_EXP_var = '\s*(.*)\s* =\s*(.*)$'

#START_EXP3 = '^' + '\s*T\s* = \s*'
#Не R а любые символы включая свои переменные
#IF, WHILE и прочие условные старты



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
            "<": operator.lt,
            "=": start_solving,
            ">": operator.gt,
        }

OPERATORs_DICT_compare2 = {
            "<=": operator.le,
            "==": operator.eq,
            "<>": operator.ne,
            ">=": operator.ge,
        }

OPERATORs_DICT_logic_L = {
            'AND': 'AND',
            'NOT': 'NOT',
            'OR': 'OR',
            'XOR': 'XOR',
            #'GE': 'GE',
            #'GT': 'GT',
            #'EQ': 'EQ',
            #'NE': 'NE',
            #'LT': 'LT',
            #'LE': 'LE'
            'MOD': operator.mod
        }

def foo(a):
    return None

OPERATORs_DICT_func_1 = {

            'SQRT': math.sqrt,
            'ABC': operator.abs,
            'INT': int_from_float,
            'NEG': operator.inv,
            #'MOD': operator.mod,#
            'SIN': sin,
            'COS': cos,
            'TAN': tan,
            'ASIN': arcsin,
            'ACOS': arccos,
            'ATAN': atan,
            'EXP': math.exp,
            'IC':   foo,#it can be almost anything, it will be taken out before
            'AC':   foo,#but we need prevent using it inside expressions
        }

OPERATORs_DICT_func_2 = {
            'POW2': operator.pow
        }

before_unar_arithmetic = {**OPERATORs_DICT_compare1, **OPERATORs_DICT_logic_L, **OPERATORs_DICT_compare2}
before_unar_arithmetic['('] = None
before_unar_arithmetic['^'] = None

OPERATORs_DICT_binary_between = {**OPERATORs_DICT_math, **OPERATORs_DICT_compare1, **OPERATORs_DICT_compare2, **OPERATORs_DICT_logic_L, **OPERATORs_DICT_func_2}

OPERATORs_PRECEDENCE_DICT = {
            '_':       3,
            '^':       4,
            '-':       1,
            '+':       1,
            '*':       2,
            '/':       2,
            'IC':4,
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

import numpy as np
#$TC_DP6[$P_TOOLNO,1]>=R9
DICT_VARS = {'pi': math.pi,
             #'$TC_DP6[$P_TOOLNO,1]': True,
            #'$P_TOOLNO,1': True,
            #'$P_TOOLNO,1': 0,
            #'$TC_DP6': np.array([[0, 110],[0, 0]]),
            }




DICT_BRACKETS = ['[', ']']#TODO для массивов. не используется




























