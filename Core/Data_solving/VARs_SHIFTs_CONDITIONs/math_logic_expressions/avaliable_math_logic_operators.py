#from add_math_logic_operators import *

from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.add_math_logic_operators import *


OPERATORs_DICT_math = {
    '-':        operator.sub,
    '+':        operator.add,
    '*':        operator.mul,
    '/':        divide,#operator.truediv,
    '^':        operator.pow
}

OPERATORs_DICT_math_U = {
    '_':        unary_minus,
    }


OPERATORs_DICT_compare1 = {
    "<":        operator.lt,
    "=":        start_solving,
    ">":        operator.gt,
}

OPERATORs_DICT_compare2 = {
    "<=":       operator.le,
    "==":       operator.eq,
    "<>":       operator.ne,
    ">=":       operator.ge,
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

def foo(a):
    return None

OPERATORs_DICT_func_1 = {

    'sqrt':     math.sqrt,
    'pow1':     qudric,
    'abc':      operator.abs,
    'int':      int_from_float,
    'neg':      operator.inv,
    #'mod':      operator.mod,
    'sin':      sin,
    'cos':      cos,
    'tan':      tan,
    'arcsin':   arcsin,
    'arccos':   arccos,
    'art':      atan,
    'exp':      math.exp,
    'ic':   foo,
    'ac':  foo,

}

OPERATORs_DICT_func_2 = {
'pow2':      operator.pow
}

before_unar_arithmetic = {**OPERATORs_DICT_compare1, **OPERATORs_DICT_logic_L, **OPERATORs_DICT_compare2}
before_unar_arithmetic['('] = None
before_unar_arithmetic['^'] = None

OPERATORs_DICT_binary_between = {**OPERATORs_DICT_math, **OPERATORs_DICT_compare1, **OPERATORs_DICT_compare2, **OPERATORs_DICT_logic_L, **OPERATORs_DICT_func_2}




OPERATORs_PRECEDENCE_DICT = {
    '_':        3,
    '^':        4,
    '-':        1,
    '+':        1,
    '*':        2,
    '/':        2,
    'sqrt':     4,
    'ic':       4,
    'pow1':     4,
    'pow2':     4,
    'abc':      4,
    'int':      4,
    'neg':      4,
    'mod':      4,
    'sin':      4,
    'cos':      4,
    'tan':      4,
    'arcsin':   4,
    'arccos':   4,
    'art':      4,
    "<":        0,
    "<=":       0,
    "==":       0,
    "!=":       0,
    ">=":       0,
    ">":        0,
    '=':       -5,
    'AND':     -4,
    'NOT':     -4,
    'OR':      -4,
    'XOR':     -4,
    'GE':       0,
    'GT':       0,
    'EQ':       0,
    'NE':       0,
    'LT':       0,
    'LE':       0

}

#VAR_ADDRESS_LIST = ['#', '$']