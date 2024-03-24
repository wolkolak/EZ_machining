import math

def equation_root(a, b, c):
    D = b**2 - 4 * a * c
    #print('equation_root: a = {}, b = {}, c = {}, D = {}'.format(a, b, c, D))
    #D = round(D, 7)
    D = abs(D)    # abs added then i received problems with 45 tool and z-100, B200 in groove
    x1 = (-b - math.sqrt(D)) / 2 / a
    x2 = (-b + math.sqrt(D)) / 2 / a
    return x1, x2


def min_None(n1, n2):
    if n1 is not None and n2 is not None:
        result = min(n1, n2)
        print('n1 = {}, n2 = {}, min n = {}'.format(n1, n2, result))
    else:
        result = n1 if n1 is not None else n2
        print('n1 = {}, n2 = {}, min n = {}'.format(n1, n2, result))
    return result

def max_None(n1, n2):
    if n1 is not None and n2 is not None:
        result = max(n1, n2)
    else:
        result = n1 if n1 is not None else n2
    return result

def between(dot_between, end1, end2):
    if end1 <= dot_between <= end2 or end1 >= dot_between >= end2:
        return True
    else:
        return False