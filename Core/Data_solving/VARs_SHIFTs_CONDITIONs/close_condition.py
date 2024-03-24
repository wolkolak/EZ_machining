import numpy as np


#Шифровка
#0 - WHILE, 1 - ENDWHILE, 2 - IF, 3 - ENDIF, 4 - FOR, 5 - ENDFOR, 6 - DOWHILE, 7 - ENDDOWHILE


#                                    номер строки   код условия   key_generator
M_L_container_np_box = np.asarray( [    [10,            0,           1,],    #Ok
                                        [15,            2,           2,],
                                        [20,            1,           3,],
                                        [25,            4,           4,]])


M_L_container_np_box2 = np.asarray( [   [10,            0,           1,],    #not Ok
                                        [15,            2,           2,],
                                        [17,            3,           5,],
                                        [20,            1,           3,],
                                        [25,            4,           4,]])




#todo Всё это не надооо

condition_op_dict_OPEN =  dict(zip(range(0, 12, 2), [x+1 for x in range(0, 12, 2)]))
condition_op_dict_CLOSE = dict(zip([x+1 for x in range(0, 12, 2)], range(0, 12, 2)))

#def SearchDawn(np_container=M_L_container.np_box, start='while':int, end='end_while':int, condition_op_dict:в парном виде int, curr_int):

def SearchConditionDawn(np_container=M_L_container_np_box2, start=0, end=1, condition_op_dictO=condition_op_dict_OPEN, condition_op_dictC=condition_op_dict_CLOSE, curr_int=1):
    i = curr_int + 1
    stack = []
    L = len(np_container)
    while i < L:# and np_container[i][0] != end and True
        np_line = np_container[i]
        if np_line[1] == end and len(stack) == 0:
            document_line = np_line[0]
            return document_line
        key_ = np_line[2]
        if key_ in condition_op_dictO:
            stack.append(condition_op_dictO[key_])
        elif key_ in condition_op_dictC:
            if stack[-1] == key_:
                stack.__delitem__(-1)
            else:
                #print('Не фурычит: np_line = ', np_line)
                # Ничто не совпало. Вероятно, последовательность нарушена
                return -1
        i = i + 1
        #print('stack в итоге {}\n'.format(stack))
    return -1


#nya = SearchConditionDawn(start=0, end=1, curr_int=0)
#print('Переход к строке № ', nya)


def SearchConditionUp(np_container=M_L_container_np_box, start=0, end=1, condition_op_dictO=condition_op_dict_OPEN, condition_op_dictC=condition_op_dict_CLOSE, curr_int=1):
    i = curr_int - 1
    stack = []
    #L = len(np_container)
    #print('Высота = ', L)
    while i > -1:# and np_container[i][0] != end and True
        np_line = np_container[i]
        #print('np_line[0] = {}, end  = {}'.format(np_line[0], start))
        #print('stack = ', stack)
        #if np_line[0] == start and len(stack) == 0:
        if np_line[1] == start and len(stack) == 0:
            #document_line = np_line[2]
            document_line = np_line[0]
            return document_line
        #key_ = str(np_line[0])
        #key_ = np_line[0]
        key_ = np_line[2]
        if key_ in condition_op_dictC:
            stack.append(condition_op_dictC[key_])
        #elif key_ in condition_op_dictC and stack[-1] in condition_op_dictO:.
        elif key_ in condition_op_dictO:
            #print('udali')
            print('stack = ', stack)
            if stack[-1] == key_:
                stack.__delitem__(-1)
            else:
                print('Не фурычит: np_line = ', np_line)
                # Ничто не совпало. Вероятно, последовательность нарушена
                return -1
        i = i - 1
        #print('stack в итоге {}\n'.format(stack))
    return -1

if __name__ == '__main__':
    nya = SearchConditionUp(start=0, end=1, curr_int=3)
    print('Переход к строке № ', nya)