import numpy as np
import copy

from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.exp_tokenization import tokenize
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.postfix4tokens import string2postfix_tuple, tokensPostfixing
import math
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTconstructionsF, DICTconstructionsB, DICTconstrucionINTERIM, DICTshiftsINT
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.close_condition import SearchConditionDawn, SearchConditionUp

not_count = [DICTshiftsINT['R = '], DICTshiftsINT['LABEL'], DICTshiftsINT['POLAR'], DICTshiftsINT['CYCLE800']]#, 41


class PAPAcontainer():
    def __init__(self, np_box, columns, i, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.np_box = np_box
        self.give_num = (i for i in range(1, 99999999))
        line_numbers = 1#todo ?
        self.np_for_vars = np.zeros((line_numbers, columns), int)
        self.index = i
        self.np_for_vars[0, 0] = -1
        self.np_for_vars[0, i] = 0
        self.base_dict = {0: None}  # keys - str(number: int) values - list
        self.brackets = self.np_box.brackets

    def finish_inserting(self, min_line, n_new_lines, new_slice):
        """
        This function insert your new_slice in correct way
        :param min_line:       min line from np_box
        :param n_new_lines:    amount of inserted lines
        :param new_slice:      inserted block
        """
        print('finish_inserting')
        min_line_inOP = np.searchsorted(self.np_for_vars[:, 0], min_line)
        add = n_new_lines - 1
        self.np_for_vars[min_line_inOP:, 0] = self.np_for_vars[min_line_inOP:, 0] + add
        self.np_for_vars = np.insert(self.np_for_vars, min_line_inOP, new_slice, axis=0)
        print(f'999self.np_for_vars = {self.np_for_vars}')

    def delete_slice(self, n_min:int, n_max:int):
        """
        :param n_min: line number in Gcode file
        :param n_max:
        :return: self.np_for_vars and self.base_dict shrink
        """
        print('delete_slice22')
        min_line = np.searchsorted(self.np_for_vars[0:, 0], n_min)
        max_line = np.searchsorted(self.np_for_vars[0:, 0], n_max)
        if len(self.np_for_vars) > max_line and n_max == self.np_for_vars[max_line][0]:
            max_line = max_line + 1
        else:
            max_line = max_line
        pp = self.index
        for i in range(min_line, max_line):
            n_key = self.np_for_vars[i, pp]
            self.base_dict.pop(n_key)
        d = n_max - n_min
        self.np_for_vars[max_line:, 0] = self.np_for_vars[max_line:, 0] - d
        self.np_for_vars = np.delete(self.np_for_vars, np.s_[min_line:max_line], axis=0)

    def return_info(self, line):
        print(f'999 self.np_for_vars = {self.np_for_vars}')
        local_line = np.searchsorted(self.np_for_vars[0:, 0], line)
        print(f'local_line = {local_line}')
        print(f'3434 self.np_for_vars[local_line] = {self.np_for_vars[local_line]}')
        return self.base_dict[self.np_for_vars[local_line][self.index]], local_line





class XYZ_vars_container(PAPAcontainer):
    """
    np int: [[line N, Label1, WHILE cipher, dict key], ...]
    dict:   {dict key: param list, ...}
    """
    def __init__(self, np_box, *args, **kwargs):
        super().__init__(np_box, columns=2, i=1, *args, **kwargs)
        self.base_dict = {0: None}  # keys - str(number: int) values - list

    def condition_inserter(self, XYexps:dict, min_line:int, n_new_lines):
        print('condition_inserter')
        """
        :param XYexps: {n_line: regularExpResult}
        :param min_line:
        :return:
        """
        L = len(XYexps)
        new_slice = np.zeros((L, 2), int)
        i = 0
        #np int: [[line N, dict key], ...]
        #dict:   {dict key: {'X': tuple(,,,,), 'Y': tuple(,,,,)...}}

        for el in XYexps:
            axises = {'X': None, 'Y': None, 'Z': None, 'A': None, 'B': None, 'C': None, 'R': None, 'I': None, 'J': None, 'K': None, 'F': None, 'AR': None, 'AP': None, 'RP': None }
            n = 10
            while XYexps[el].captured(n) != '':#n < 61 and
                axises[XYexps[el].captured(n)] = string2postfix_tuple(XYexps[el].captured(n+1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if XYexps[el].captured(n+1) != '=' else None
                n = n + 6
            n = 46
            while XYexps[el].captured(n) != '' and n < 69:
                axises[XYexps[el].captured(n)] = string2postfix_tuple(XYexps[el].captured(n+1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor ) if XYexps[el].captured(n+1) != '=' else None
                n = n + 6
            n = 64
            if XYexps[el].captured(n) != '':#CR
                #print(f'CR or AR = |{XYexps[el].captured(n)}|')
                axises['R'] = string2postfix_tuple(XYexps[el].captured(n + 1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if XYexps[el].captured(n+1) != '=' else None
                #print(f"condition_inserter R = {axises['R']}")
            n = 70
            if XYexps[el].captured(n) != '':#AR
                print(f'CR or AR = |{XYexps[el].captured(n)}|')
                axises['AR'] = string2postfix_tuple(XYexps[el].captured(n + 1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if XYexps[el].captured(n+1) != '=' else None
                #print(f"condition_inserter R = {axises['R']}")
            n = 76
            if XYexps[el].captured(n) != '':#AP/AR
                print(f'CR or AR = |{XYexps[el].captured(n)}|')
                axises[XYexps[el].captured(n).replace(' ', '')[:-1]] = string2postfix_tuple(XYexps[el].captured(n + 1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) #if XYexps[el].captured(n+1) != '=' else None
            n = 82
            if XYexps[el].captured(n) != '':#AP/RP
                print(f'CR or AR = |{XYexps[el].captured(n)}|')
                axises[XYexps[el].captured(n).replace(' ', '')[:-1]] = string2postfix_tuple(XYexps[el].captured(n + 1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) #if XYexps[el].captured(n+1) != '=' else None

            n=87
            if XYexps[el].captured(n) != '':
                axises['F'] = string2postfix_tuple(XYexps[el].captured(n + 1), self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if XYexps[el].captured(n+1) != '=' else None
            new_slice[i][0] = el + min_line
            new_slice[i][1] = next(self.give_num)
            self.base_dict[new_slice[i][1]] = axises
            i = i + 1
        self.finish_inserting(min_line=min_line, n_new_lines=n_new_lines, new_slice=new_slice)

    def __str__(self):
        a = 'XYZ vars:\n'
        for el in self.np_for_vars:
            a = a + 'N:{},                 {}\n'.format(el[0], self.base_dict[el[1]])
        a = a + '\n\n\n'
        #    + self.vars.__str__()
        return a

class GM_modal_container(PAPAcontainer):
    """
    np int: [[line N, Label1, WHILE cipher, dict key], ...]
    dict:   {dict key: param list, ...}
    """
    def __init__(self, np_box, *args, **kwargs):
        super().__init__(np_box, columns=2, i=1, *args, **kwargs)
        self.base_dict = {0: None}  # keys - str(number: int) values - list

    def condition_inserter(self, GMexps:dict, min_line:int, n_new_lines:int):
        print('condition_inserter 150 ')
        """
        :param GMexps: [{n_line, {key: value} }, ...]
        :param min_line:
        :return:
        """
        L = len(GMexps)
        new_slice = np.zeros((L, 2), int)
        i = 0
        #np int: [[line N, dict key], ...]
        #dict:   {dict key: {'X': tuple(,,,,), 'Y': tuple(,,,,)...}}
        for el in GMexps:
            new_slice[i][0] = el[0] + min_line
            kk = next(self.give_num)
            new_slice[i][1] = kk
            self.base_dict[kk] = el[1]
            i = i + 1
        self.finish_inserting(min_line=min_line, n_new_lines=n_new_lines, new_slice=new_slice)


    def __str__(self):
        a = 'GM_modal_container:\n'
        for el in self.np_for_vars:
            a = a + f'N:{el[0]}|: {self.base_dict[el[1]]}\n'
        a = a + '\n\n\n'
        return a



class ShiftContainer(PAPAcontainer):
    """
    np int: [[line N, Label1, WHILE cipher, dict key], ...]
    dict:   {dict key: param list, ...}
    """
    def __init__(self, np_box, *args, **kwargs):
        super().__init__(np_box, columns=4, i=3, *args, **kwargs)
        self.VARs = self.np_box.VARs
        self.conditionOPs = [DICTshiftsINT['WHILE'], DICTshiftsINT['IF'], DICTshiftsINT['ELIF'], DICTshiftsINT['CASE'], DICTshiftsINT['OF']]
        #self.OPENS = [DICTshiftsINT['WHILE'], DICTshiftsINT['IF'], DICTshiftsINT['ELIF'], DICTshiftsINT['CASE'], DICTshiftsINT['OF'], DICTshiftsINT['ELSE']]
        self.CLOSES = []
        self.AfterJump = False
        self.base_dict = {0: [None, None, None, None, None]}  # keys - str(number: int) values - list
        self.label_correct = self.np_box.redactor.highlight.reversal_post_processor.correct_lbl
        self.OPs_with_different_rules = self.np_box.redactor.highlight.reversal_post_processor.OPs_with_different_rules
        self.save_vars_as_local_global_func = self.np_box.redactor.highlight.reversal_post_processor.save_vars_as_local_global
        #self.LogButton = self.np_box.redactor.Logs



    def condition_inserter(self, commands:list, min_line, n_new_lines:int ):
        print('condition_inserter 200')
        """
        :param commands: [[cur I, OP_int, REGcontent], ...]
        :param min_line:
        :return:
        """
        L = len(commands)
        new_slice = np.zeros((L, 4), int)
        i = 0
        #np int: [[line N, Label1, WHILE cipher, dict key], ...]
        #dict:   {dict key: [param list1, param list2, param list3], ...}
        for el in commands:#todo 41????
            print('command = ', el)
            new_slice[i][0] = el[0] + min_line
            new_slice[i][1] = 41 if el[2].captured(4) != '' else -1
            new_slice[i][2] = el[1]
            new_slice[i][3] = next(self.give_num)
            fourth_tokens = None
            third_standart = True
            if el[1] in self.OPs_with_different_rules:
                print('self.OPs_with_different_rules[1] = ', self.OPs_with_different_rules)
                first_tokens, second_tokens, third_tokens, fourth_tokens, new_slice = self.OPs_with_different_rules[el[1]][1](self,  el, i, min_line, new_slice, self.np_box.CUR_PROC)#
                #
            else:

                #todo Дальше словарь. CASE_OF не стал включать
                if new_slice[i][2] == 30:
                    first = el[2].captured(7)#7
                    second = el[2].captured(10)
                    third = el[2].captured(6) if el[2].captured(6) != '' else 'REAL'
                    #self.save_vars_as_local_global_func(self, el, new_slice[i])
                    #i = i + 1
                    #continue
                #elif new_slice[i][2] == DICTshiftsINT['SUB_PROG_START']:
                #    first = el[2].captured(5)#7
                #    second = el[2].captured(6).lower()


                elif new_slice[i][2] == DICTshiftsINT['SUB_PROGRAM']:
                    first = el[2].captured(5)#7
                    second = el[2].captured(6).lower()
                    content: str = el[2].captured(7)
                    third_standart = False
                    if content == '':
                        third_tokens = None
                    else:
                        print('123 content = ', content)
                        if content[0] in ('[', '(') and content[-1] in (']', ')'):
                            content = content[1:-1]#обрезаю скобки

                        content_list = content.split(',')

                        third = []
                        fourth = []
                        for var_equalution in content_list:
                            print(f'1 var_equalution = {var_equalution}')
                            third.append(None)
                            fourth.append(string2postfix_tuple(var_equalution, self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor))
                            #ve_list = var_equalution.split('=')
                            #if len(ve_list) > 1:
                            #    third.append(ve_list[0])
                            #    print(f've_list[1] = {ve_list[1]}')
                            #    fourth.append(string2postfix_tuple(ve_list[1], self.brackets))
                            #else:
                            #    third.append(None)
                            #    print(f've_list[0] = {ve_list[0]}')
                            #    fourth.append(string2postfix_tuple(ve_list[0], self.brackets))
                        third_tokens = [*third]
                        fourth_tokens = [*fourth]
                    #if new_slice[i][2] == DICTshiftsINT['SUB_PROGRAM']:
                    self.np_box.add_sub_programs(second)


                elif new_slice[i][2] == DICTshiftsINT['SUB_PROG_START']:
                    first = el[2].captured(5)#7
                    second = el[2].captured(6).lower()
                    content: str = el[2].captured(7)
                    third_standart = False
                    if content == '':
                        third_tokens = None
                    else:
                        content = content[1:-1]
                        content_list = content.split(',')
                        third = []
                        fourth = []
                        for var_equalution in content_list:
                            ve_list = var_equalution.split('=')
                            third.append(string2postfix_tuple(ve_list[0], self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor))
                            if len(ve_list) > 1:
                                fourth.append(string2postfix_tuple(ve_list[1], self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor))
                            else:
                                fourth.append(None)
                        third_tokens = [*third]
                        fourth_tokens = [*fourth]
                else:
                    first = el[2].captured(6)
                    second = el[2].captured(8)
                    third = el[2].captured(10)
                first_tokens = string2postfix_tuple(first, self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if first != '' else None
                print(f'second6565 = {second}')
                second_tokens = string2postfix_tuple(second, self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if second != '' else None
                if third_standart:
                    third_tokens = string2postfix_tuple(third, self.brackets, proc=self.np_box.redactor.highlight.reversal_post_processor) if third != '' else None
                else:
                    #f = ('ABC',)

                    second_tokens = (second,)

            #if (first_tokens is None and first not in [None, '', ' ']) or \
            #        (second_tokens is None and first not in [None, '', ' ']) or \
            #        (third_tokens is None and first not in [None, '', ' ']):
            #    self.LogButton.text_logs = self.LogButton.text_logs.append(new_slice[i][0])



            print(f'first_tokens = {first_tokens}, second_tokens = {second_tokens}, third_tokens = {third_tokens}')
            #dict:   {dict key: [param list1, param list2, param list3], ...}

            Lbl = el[2].captured(4)
            Lbl = self.label_correct(Lbl) if Lbl != '' else ''
            self.base_dict[new_slice[i][3]] = [Lbl, first_tokens, second_tokens, third_tokens, fourth_tokens]
            i = i + 1

        self.finish_inserting(min_line=min_line, n_new_lines=n_new_lines, new_slice=new_slice)

    def return_info(self, line):
        #print('return_info: ', self.np_for_vars)
        local_line = np.searchsorted(self.np_for_vars[:, 0], line)
        print('line = ', line)
        #print('TYTYT local_line  = ', local_line )
        #print('self.np_for_vars = ', self.np_for_vars)
        return self.np_for_vars[local_line], self.base_dict[self.np_for_vars[local_line][self.index]], local_line#todo тут вышибло

    def nextSHIFT(self, i_str, len_v):#, lbl_name=None, auto_return=-1
        print('nextSHIFT')
        print('i_str start = ', i_str)
        #if len_v == 51:
        #    2/0
        print('len_v = ', len_v)
        print('111 np_box.redactor.Logs.math_logs = ', self.np_box.redactor.Logs.math_logs)
        cur_instruction = self.np_box.special_instructions[-1] if len(self.np_box.special_instructions) > 0 else None
        #может, вообще применить инструкцию ко всему что ниже
        #if i_str +1 >= len_v:
        #    print(f' ушёл на дешевых {len_v-1}')
        #    return len_v-1
        local_line = np.searchsorted(self.np_for_vars[:, 0], i_str+1)
        print(f' Искал я {i_str+1}')


        #AAAAAAAA
        print('local_line = ', local_line)
        print('999 self.np_for_vars = ', self.np_for_vars)
        L = len(self.np_for_vars)
        print('cur_instruction = ', cur_instruction)
        if cur_instruction is None:
            while local_line < L and (self.np_for_vars[local_line][2] in not_count):#[30, 40, 41]):
                local_line = local_line + 1
            if local_line == L:
                return len_v - 1
            i_str = self.np_for_vars[local_line][0]
            print(f'222 nextSHIFT: i_str = {i_str}')
        else:#here we are looking for special labels.with is all for REPEAT
            if len(self.np_for_vars) > local_line:
                print('222 np_box.redactor.Logs.math_logs = ', self.np_box.redactor.Logs.math_logs)
                i_str = cur_instruction(self.np_box, local_line, i_str)
                print('333 np_box.redactor.Logs.math_logs = ', self.np_box.redactor.Logs.math_logs)
            else:
                i_str = -1
            print(f'3333 nextSHIFT: i_str = {i_str}')

        if i_str == -1:
            i_str = len_v - 1
        print(f'nextSHIFT: i_str = {i_str}')
        return i_str



    def SearchConditionUp(self, curr_int, start=0, end=1):#, condition_op_dictO=DICTconstructionsF, condition_op_dictC=DICTconstructionsB

        np_container = self.np_for_vars
        i = curr_int - 1
        stack = []
        # L = len(np_container)
        # print('Высота = ', L)
        while i > -1:  # and np_container[i][0] != end and True
            #print('111 stack = ', stack)

            np_line = np_container[i]
            #print(f'np_line = {np_line}, start = {start}')
            if np_line[2] == start and len(stack) == 0:
                # document_line = np_line[2]
                document_line = np_line[0]
                return document_line
            key_ = np_line[2]
            if key_ in DICTconstructionsB:
                stack.append(DICTconstructionsB[key_])
            elif key_ in DICTconstructionsF:
                # print('udali')
                #print('stack = ', stack)
                #print('key_  = ', key_ )
                if stack.__len__() != 0 and stack[-1] == key_:
                    stack.__delitem__(-1)
                else:
                    print('Не фурычит: np_line = ', np_line)
                    # Ничто не совпало. Вероятно, последовательность нарушена
                    return -1
            i = i - 1
            # print('stack в итоге {}\n'.format(stack))
        return -1

    def SearchConditionDawn(self, curr_int=1, start=0, end=[1]):
        print('my SearchConditionDawn')
        #2/0
        i = curr_int + 1
        stack = []
        np_container = self.np_for_vars
        L = len(np_container)
        print(f'i = {i}, L = {L}')
        while i < L:  # and np_container[i][0] != end and True
            #print('222 stack = ', stack)
            np_line = np_container[i]
            print(f'тут какая то дичь = {np_line}')
            print('end = ', end)
            if np_line[2] in end and len(stack) == 0:
                document_line = np_line[0]
                print(f'return {document_line}')
                return document_line
            key_ = np_line[2]
            if key_ in DICTconstructionsF:
                stack.append(DICTconstructionsF[key_])
            elif key_ in DICTconstrucionINTERIM:#раньше в DICTconstrucionINTERIM value = None было, навреное, новый вариант правильнее
                if stack.__len__() != 0 and stack[-1] != DICTconstrucionINTERIM[key_]:
                    stack.append(DICTconstructionsF[key_])
            elif key_ in DICTconstructionsB:
                print(f'555 5 {key_} in {DICTconstructionsB}')
                print('Дичь номер 2: stack = ', stack)
                print('stack.__len__() = ', stack.__len__())
                if stack.__len__() != 0 and stack[-1] == key_:
                    stack.__delitem__(-1)
                else:
                    print('Не фурычит: np_line = ', np_line)
                    # Ничто не совпало. Вероятно, последовательность нарушена
                    print(f'1return {-1}')
                    return -1
            i = i + 1
            # print('stack в итоге {}\n'.format(stack))
        print(f'2return {-1}')
        return -1






    def __str__(self):
        a = 'SHIFT container\n'
        print('self.base_dict = ', self.base_dict)
        #print('self.np_for_vars = ', self.np_for_vars)
        for el in self.np_for_vars:
            a = a + 'N:{},      Label:{},      OP cipher:{},      dict conditions: {}\n'.format(el[0], el[1], el[2], self.base_dict[el[3]])
        a = a + '\n\n\n'
        i = 1
        for v in self.VARs:
            if i == 3:
                i = 0
                a = a + str(v) + ':' + str(self.VARs[v]) + '\n'
            else:
                new_a = str(v) + ':' + str(self.VARs[v])
                addL = 60 - len(new_a)
                a = a + new_a + '|' + ' '*addL + '|'
            i = i + 1
        return a
