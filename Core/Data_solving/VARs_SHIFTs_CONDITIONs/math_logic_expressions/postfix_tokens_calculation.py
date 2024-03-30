from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.avaliable_math_logic_operators import \
    OPERATORs_DICT_func_1, \
    OPERATORs_PRECEDENCE_DICT, \
    OPERATORs_DICT_binary_between, \
    OPERATORs_DICT_math_U

o1 = OPERATORs_DICT_func_1
o2 = OPERATORs_PRECEDENCE_DICT
o3 = OPERATORs_DICT_binary_between
o4 = OPERATORs_DICT_math_U



def postfixTokenCalc(tokens: tuple, DICT_VARS=None, proc=None):
    """
    returns calculation result
    :param tokens: floats, vars, operators, functions
    :param DICT_VARS:
    :return: number
    """
    if proc is not None:
        print(f"proc is not None!!!!!")
        OPERATORs_DICT_func_1 =         proc.OPERATORs_DICT_func_1
        OPERATORs_PRECEDENCE_DICT =     proc.OPERATORs_PRECEDENCE_DICT
        OPERATORs_DICT_binary_between = proc.OPERATORs_DICT_binary_between
        OPERATORs_DICT_math_U =         proc.OPERATORs_DICT_math_U
    else:
        OPERATORs_DICT_func_1 =         o1
        OPERATORs_PRECEDENCE_DICT =     o2
        OPERATORs_DICT_binary_between = o3
        OPERATORs_DICT_math_U =         o4
    print(f'postfixTokenCalc tuple = {tokens}')
    if DICT_VARS is None:
        DICT_VARS = {}
    stack_l = []
    if tokens is None:
        return None
    for t in tokens:
        print('t in tokens: ', t)
        if type(t) is float or type(t) is int or type(t) is complex: # todo int and complex not needed in CNC
            stack_l.append(t)
        elif t in OPERATORs_PRECEDENCE_DICT:
            if len(stack_l) == 0:
                return None
            right = stack_l.pop(-1)
            if t in OPERATORs_DICT_binary_between:
                if len(stack_l) == 0 and (t == '-' or t == '+'):
                    stack_l.append(right) if t == '+' else stack_l.append(-right)
                else:
                    if len(stack_l) == 0:
                        if t == '=':
                            return right
                        else:
                            return None
                    left = stack_l.pop(-1)
                    if left is not None and right is not None:
                        print(f'left = {left}')
                        stack_l.append(OPERATORs_DICT_binary_between[t](left, right))
                    else:
                        print('None in {} or {}'.format(left, right))
                        return None
            elif t in OPERATORs_DICT_math_U:
                stack_l.append(OPERATORs_DICT_math_U[t](right))
            else:
                stack_l.append(OPERATORs_DICT_func_1[t](right))
        elif t in DICT_VARS:
            stack_l.append(DICT_VARS[t])
        else:
            print('{} was not found in VARs'.format(t))
            return None
    if len(stack_l) != 1:
        print('Error stack ', stack_l)
        return None

    return stack_l[0]






if __name__ == "__main__":
    from postfix4tokens import string2postfix_tuple, tokenize, tokensPostfixing

    import math


    class Retard:
        pass
    proc = Retard()

    proc.OPERATORs_DICT_func_1 = OPERATORs_DICT_func_1
    proc.OPERATORs_PRECEDENCE_DICT = OPERATORs_PRECEDENCE_DICT
    proc.OPERATORs_DICT_binary_between = OPERATORs_DICT_binary_between
    proc.OPERATORs_DICT_math_U = OPERATORs_DICT_math_U

    #DICT_VARS = {'R2': 5., 'pi': math.pi}
    #nya2 = tokenize('2^3 + 3^(1+1)')
    #print('nya22= ', nya2)
    #res = tokensPostfixing(nya2)
    #solve = postfixTokenCalc(res, DICT_VARS)
    #print('RESULT2 = ', solve)

    print('complex?: ', postfixTokenCalc((5, 3j, '-',), proc=proc))
    print('complex?: ', postfixTokenCalc((5, 3j, '-',)))
