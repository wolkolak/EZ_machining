#from avaliable_math_logic_operators import OPERATORs_DICT_logic_L, OPERATORs_DICT_math, OPERATORs_DICT_compare1, \
#    OPERATORs_PRECEDENCE_DICT

from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.avaliable_math_logic_operators import \
    OPERATORs_DICT_logic_L, OPERATORs_DICT_math, OPERATORs_DICT_compare1, OPERATORs_PRECEDENCE_DICT#, VAR_ADDRESS_LIST


def tokenize(input_string:str, brackets=None):
    if brackets is None:
        brackets = ['(', ')', '[', ']']
    cleaned = input_string
    chars = list(cleaned)
    output = []
    state = ""
    buf = ""
    space = False
    while len(chars) != 0:
        char = chars.pop(0)
        if char in [' ', brackets[2], brackets[3]]:
            output.append(buf) if buf != "" else False
            buf = ""
            state = ""
            space = True
        else:
            if space and state == 'func':
                if buf in OPERATORs_DICT_logic_L:
                    print('space = True, buf = {}'.format(buf))
                    output.append(buf)
                    buf = ''
                    state = ''
            if char.isdigit() or char == '.':
                if state != "num" and state != 'func':
                    output.append(buf) if buf != "" else False
                    buf = ""
                if state != 'func':
                    state = "num"
                buf += char
            elif char in OPERATORs_DICT_math.keys() or char in [brackets[0], brackets[1]]:
                output.append(buf) if buf != "" else False
                buf = ""
                state = 'op'
                output.append(char)
            elif char in OPERATORs_DICT_math.keys() or char in OPERATORs_DICT_compare1:
                if state == 'op2' and len(output[-1]) == 1:
                    output[-1] = output[-1] + char
                else:
                    output.append(buf) if buf != "" else False
                    buf = ""
                    state = 'op2'
                    output.append(char)
            else:
                if state != "func":
                    output.append(buf) if buf != "" else False
                    buf = ""
                state = "func"
                buf += char
            space = False
    output.append(buf) if buf != "" else False


    for i in range(len(output)):
        try:
            output[i] = float(output[i])
        except:
            #print('output = ', output)
            print('output[i] = ', output[i])
            if output[i] == ';':
                output = output[:i]
                break
            elif output[i].endswith(';'):#type(output[i]) is str and
                output[i] = output[i][:-1]
                output = output[:i + 1]
                break
    #if output[-1] == ';':
    #    output.pop(-1)
    #elif type(output[-1]) is str and output[-1].endswith(';'):
    #    output[-1] = output[-1][:-1]
    print('в итоге output = ', output)
    return output



if __name__ == "__main__":
    #g = tokenizeCNC('2<3 GE 2.0 GT A + af34d9 + sin(60)==5+pow(5,2)')#6 GE
    #brackets = ['(', ')', '[', ']']
    #g = tokenizeCNC('2<3 GE 2.0 GT A + af34d9 + sin[60]==5+pow[5,2]', brackets)  # 6 GE
    #g = tokenize('2^3 + 3^(1+1)')
    #print('g = ', g)
    g = tokenize('2^3 + 3^(1+1)')

    #g = tokenize('A[f[1]]')#DICT_BRACKETS
    print('g = ', g)
    #nya = '-2^ -[sin[5]*3]'
    #print(tokenize(nya))
