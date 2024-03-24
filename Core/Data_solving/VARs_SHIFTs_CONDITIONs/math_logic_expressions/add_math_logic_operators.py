import operator
import math

def int_from_float(a):
    if a is None:
        return None
    return operator.floordiv(a, 1)

def qudric(a):
    if a is None:
        return None
    return operator.pow(a, 2)

def start_solving(something):
    print('= in expression')
    return None

def unary_minus(a):
    if a is None:
        return None
    return -a

def sin(a):
    if a is None:
        return None
    a = math.radians(a)
    return math.sin(a)

def cos(a):
    if a is None:
        return None
    a = math.radians(a)
    return math.cos(a)

def tan(a):
    if a is None:
        return None
    a = math.radians(a)
    return math.tan(a)

def atan(a):
    if a is None:
        return None
    #a = math.radians(a)
    return math.degrees(math.atan(a))

def arccos(a):
    if a is None:
        return None
    return math.degrees(math.acos(a))

def arcsin(a):
    if a is None:
        return None
    return math.degrees(math.asin(a))


def divide(a,b):
    if b != 0 and (a is not None and b is not None):
        return operator.truediv(a, b)
    else:
        print('dived by ZERO!!!')
        return None



