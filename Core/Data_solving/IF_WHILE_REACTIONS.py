from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.postfix_tokens_calculation import postfixTokenCalc
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT, DICTconstructionsF, DICTconstructionsB, \
    DICTconstrucionINTERIM
# from Core.Data_solving.VARs_SHIFTs_CONDITIONs.close_condition import SearchConditionDawn, SearchConditionUp
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.GOTOhelper import helper_for_GOTO_N, helper_for_GOTO_LBL, fanuc_helper_for_GOTO_N
import numpy as np
from Core.Data_solving.added_special_instructions_in_solving import *
import time


def CNCpass(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line:
    print('CNCpass')
    print(f'info = {info}')
    jumped_here = False
    return i_str + 1, jumped_here, i+0


def if_classic(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    print('if classic')
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    print('res = ', res)
    if res is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        res = False
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)
    i__ = info[2]

    if res:
        jumped_here = False
        print(f'if направляет на строку номер {i_str + 1}')
        return i_str + 1, jumped_here, i
    else:
        jumped_here = True
        i_str2 = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['IF'],
                                                           end=[DICTshiftsINT['ELSE'], DICTshiftsINT['ENDIF']])
        if i_str2 == -1:
            return i_str + 1, False, i
        else:
            print(f'endif new i_str = {i_str2}')
            return i_str2, jumped_here, i


def else_if_classic(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    print('elseif classic')
    # 2/0
    if jumped_here:
        print('1')
        return i_str + 1, False, i
    print('1.1')
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)
    i__ = info[2]
    i_str2 = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['ELSE'], end=[DICTshiftsINT['ENDIF']])
    print('i_str2 = ', i_str2)
    print('1.2')
    if i_str2 != -1:
        print(f'elseif new i_str = {i_str2}')
        print('2')
        return i_str2, jumped_here, i
    else:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} aiming for non-existent line\n'
        print('36565')
        return i_str2, jumped_here, i


# def


def classic_while(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line todo бывают и промежуточные команды и выходы из середины цикла, но это всё для GOTO

    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    print(f'classic_while: {res} in {info}')
    if res is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        res = False
    print(f'Искомый {i_str} condition is {res}')
    # i = np_box.SHIFTcontainer.return_new_i(i_str)
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)  # Istart
    i__ = info[2]
    print('while i = ', i)
    if res:
        jumped_here = False
        return i_str + 1, jumped_here, i
    else:  # pick end_while
        i_str2 = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['WHILE'], end=[DICTshiftsINT['ENDWHILE']])
        if i_str2 != -1:
            jumped_here = True
            print(f'endwhile new i_str = {i_str2}')
            return i_str2, jumped_here, i
        else:
            jumped_here = False  # True?
            return i_str, jumped_here, i


def classic_REPAT_until(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line todo бывают и промежуточные команды и выходы из середины цикла, но это всё для GOTO
    print('classic_DOwhile')
    return i_str + 1, jumped_here, i


def classic_UNTIL_repeat(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line todo бывают и промежуточные команды и выходы из середины цикла, но это всё для GOTO
    print('classic_DO WHILE END')
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    if res is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        res = False
    print(f'Искомый {i_str} condition is {res}')
    # i = np_box.SHIFTcontainer.return_new_i(i_str)
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)  # Istart
    i__ = info[2]
    print('while i = ', i)
    if not res:
        jumped_here = False
        return i_str + 1, jumped_here, i
    else:  # pick end_while
        i_str2 = np_box.SHIFTcontainer.SearchConditionUp(curr_int=i__, start=DICTshiftsINT['REPEATu'], end=[DICTshiftsINT['UNTIL']])
        if i_str2 != -1:
            jumped_here = True
            print(f'endwhile new i_str = {i_str2}')
            return i_str2, jumped_here, i
        else:
            jumped_here = False  # True?
            return i_str, jumped_here, i


def classic_end_while(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    print('classic_endwhile')
    print('jumped_here = ', jumped_here)
    if jumped_here:
        print(f'endwhile 1 return i_str + 1 = {i_str + 1}')
        return i_str + 1, False, i
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)#Istart
    i__ = info[2]
    # pass_ = False
    print(f'i = {i}, and i_str = {i_str}')
    i_str2 = np_box.SHIFTcontainer.SearchConditionUp(curr_int=i__, start=DICTshiftsINT['WHILE'], end=DICTshiftsINT['ENDWHILE'])
    if i_str2 != -1:
        print(f'endwhile new i_str = {i_str2}')
        return i_str2, True, i
    else:
        print(f'endwhile 2 return i_str + 1 = {i_str + 1}')
        return i_str + 1, False, i


def LOOPinfinite(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line todo бывают и промежуточные команды и выходы из середины цикла, но это всё для GOTO
    print('classic_LOOPinfinite')
    return i_str + 1, jumped_here, i


def END_LOOPinfinite(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    print('classicEND_LOOPinfinite')
    # i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)#Istart
    i__ = info[2]
    i_str2 = np_box.SHIFTcontainer.SearchConditionUp(curr_int=i__, start=DICTshiftsINT['LOOP'], end=DICTshiftsINT['END_LOOP'])
    if i_str2 != -1:
        print(f'classicEND_LOOPinfinite new i_str = {i_str2}')
        return i_str2, True, i
    else:
        return i_str + 1, False, i


def siemensFOR_TO(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line todo бывают и промежуточные команды и выходы из середины цикла, но это всё для GOTO
    exp_ = info[1][1][1:-1]
    print('info moe22 = ', info)
    # info[1][1][1:-1][0] = exp_ = info[1][1][1:-1][0] + 1
    print('exp_ = ', exp_)

    res1 = postfixTokenCalc(exp_, DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    res2 = postfixTokenCalc(info[1][2], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    print(f'||| res1 = {res1}, res2 = {res1}')
    print('info[1][4] = ', info[1][4])
    if info[1][4] is None:
        print('-+-+-+-+-+-+-+-')
        current_vars[info[1][1][0]] = res1
        i__ = info[2]
        i_str3 = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['FOR'], end=[DICTshiftsINT['END_FOR']])
        print(f'taaaks i_str3 = {i_str3}')
        if i_str3 < 0:
            print(f'here66 i_str2 = {i_str3}')
            info[1][4] = None
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line: can not find pair to the operator\n'
            return i_str + 1, False, i
        info[1][4] = True
    else:
        current_vars[info[1][1][0]] = current_vars[info[1][1][0]] + 1

    if current_vars[info[1][1][0]] is None or res2 is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error:{info[1][4]} compared with {info[1][4]}\n'
        print(f'end probably0 info[1][4] = {info[1][4]}')
        return i_str + 1, False, i

    if current_vars[info[1][1][0]] > res2:

        info[1][4] = None
        i__ = info[2]
        print('i = ', i)
        i_str2 = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['FOR'], end=[DICTshiftsINT['END_FOR']])
        # здесь. и нет завуршающего оператора

        if i_str2 != -1:
            jumped_here = True
            print(f'enf FOR_TO new i_str = {i_str2}')
            print(f'end probably1 info[1][4] = {info[1][4]}')
            return i_str2, jumped_here, i
        else:
            #
            jumped_here = False  # True?
            print(f'end probably2 info[1][4] = { info[1][4] }')
            return i_str, jumped_here, i
    else:
        #if True:
        #    info[1][4] = None
        print(f'end probably3 info[1][4] = { info[1][4] }')
        return i_str + 1, False, i


def siemens_end_FOR(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    print('classic_endwhile')
    if jumped_here:
        return i_str + 1, False, i
    i__ = info[2]
    i_str2 = np_box.SHIFTcontainer.SearchConditionUp(curr_int=i__, start=DICTshiftsINT['FOR'], end=[DICTshiftsINT['END_FOR']])
    if i_str2 != -1:
        return i_str2, True, i
    else:
        return i_str + 1, False, i


def siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=0, lbl_name=None):  # todo время отслеживать ЦИКЛЫ #lbl_place=1,
    """
    1 can jump by label, by real number of line and indirect line number(N100)
    2 can't jump into conditions, but can jump outside
    3 mod: 0-GOTO, 1-GOTOF, 2-GOTOB, 3-GOTOC
    """
    print('i_str = ', i_str)
    print('lbl_name = ', lbl_name)
    print('info[1][1] = ', info[1])
    if lbl_name is None:
        lbl_name = info[1][1]  # problem for IF
    print('gotoF - ', i_str)
    # print('main info = ', info[1][1][0])
    print(f'в goto lbl_name = {lbl_name}')
    if lbl_name is None or len(lbl_name) == 0:
        print('== 0')
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} empty label for GOTO. Stopped\n'
        return None, False, i

    # print()
    if not (isinstance(lbl_name[0], float) or isinstance(lbl_name[0], int)) and len(lbl_name) == 1 and lbl_name[0] not in current_vars:
        lbl = lbl_name[0]
        if len(lbl) > 1 and lbl[0] == 'N' and lbl[1:].isdigit():  # todo for N
            Nline = helper_for_GOTO_N(np_box, info, i_str, lbl, mod)
        else:  # todo поиск по метке
            print('lbl check = ', lbl)
            print('66 i_str start = ', i_str)

            Nline = helper_for_GOTO_LBL(np_box, info, i_str, lbl, mod)
            print('после helper а Nline = ', Nline)
    else:  # todo поиск по вычислениям  т.е. по вычисленной строке
        Nline = postfixTokenCalc(lbl_name, DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
        # Nline = int(Nline)
        print('here check 333 Nline = ', Nline)

    if Nline is None or Nline < 0 or Nline > len(np_box.main_g_cod_pool):
        if mod == 3:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} labeled line for GOTO was not found. Continued\n'
            return i_str + 1, False, i
        else:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} labeled line for GOTO was not found. Stopped\n'
            return None, False, i

    stack = []
    print(f'Nline = {Nline}, i_str: = {i_str:}')
    if Nline > i_str:
        start_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)
        end_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], Nline)
        for l_param in np_box.SHIFTcontainer.np_for_vars[start_slice: end_slice + 1]:
            print('1 looking for stack: ', stack)
            if l_param[2] in DICTconstructionsF:
                stack.append(DICTconstructionsF[l_param[2]])
            elif l_param[2] in DICTconstructionsB:
                if len(stack) > 0 and stack[-1] == l_param[2]:
                    stack.pop(-1)
            elif l_param[2] in DICTconstrucionINTERIM:
                if not (len(stack) > 0 and stack[-1] == DICTconstrucionINTERIM[l_param[2]]):
                    stack.append(DICTconstrucionINTERIM[l_param[2]])
    else:  # backward check
        start_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str) - 1
        end_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], Nline) - 1
        print('Nline = ', Nline)
        print(f'start_slice = {start_slice}, end_slice = {end_slice}')
        for l_param in np_box.SHIFTcontainer.np_for_vars[start_slice: end_slice - 1: -1]:
            print('l_param = ', l_param)
            print('2 looking for stack: ', stack)
            if l_param[2] in DICTconstructionsB:
                stack.append(DICTconstructionsB[l_param[2]])
            elif l_param[2] in DICTconstructionsF:
                if len(stack) > 0 and stack[-1] == l_param[2]:
                    stack.pop(-1)
            elif l_param[2] in DICTconstrucionINTERIM:
                if not (len(stack) > 0 and stack[-1] == DICTconstructionsB[DICTconstrucionINTERIM[l_param[2]]]):
                    stack.append(DICTconstructionsB[DICTconstrucionINTERIM[l_param[2]]])
    print('goto Nline = {}'.format(Nline))
    if len(stack) != 0:
        print('alarm!!')
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line GOTO tryed to enter condition structure. Stopped\n'
        return None, False, i  # i_str+1
    return Nline, False, i  # todo check if False


def fanuc_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=0, lbl_name=None):  # todo время отслеживать ЦИКЛЫ #lbl_place=1,
    """
    1 can jump by label, by real number of line and indirect line number(N100)
    2 can't jump into conditions, but can jump outside
    3 mod: 0-GOTO, 1-GOTOF, 2-GOTOB, 3-GOTOC
    """
    print('i_str = ', i_str)
    print('lbl_name = ', lbl_name)
    print('info[1][1] = ', info[1])
    if lbl_name is None:
        lbl_name = info[1][1]  # problem for IF
    print('gotoF - ', i_str)
    # print('main info = ', info[1][1][0])
    print(f'в goto lbl_name = {lbl_name}')
    if lbl_name is None or len(lbl_name) == 0:
        print('== 0')
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} empty label for GOTO. Stopped\n'
        return None, False, i

    # print()
    if  (isinstance(lbl_name[0], float) or isinstance(lbl_name[0], int)):
        lbl = lbl_name[0]
        print(f'lbl = {lbl}')
        if True:#len(lbl) > 0 :#and lbl[:].isdigit():  # todo for N
            Nline = fanuc_helper_for_GOTO_N(np_box, info, i_str, lbl)
            if Nline is None or Nline < 0:
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} labeled line for GOTO was not found. Stopped\n'
                return None, False, i

            stack = []
            print(f'Nline = {Nline}, i_str: = {i_str:}')
            if Nline > i_str:
                start_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str)
                end_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], Nline)
                for l_param in np_box.SHIFTcontainer.np_for_vars[start_slice: end_slice + 1]:
                    print('1 looking for stack: ', stack)
                    if l_param[2] in DICTconstructionsF:
                        stack.append(DICTconstructionsF[l_param[2]])
                    elif l_param[2] in DICTconstructionsB:
                        if len(stack) > 0 and stack[-1] == l_param[2]:
                            stack.pop(-1)
                    elif l_param[2] in DICTconstrucionINTERIM:
                        if not (len(stack) > 0 and stack[-1] == DICTconstrucionINTERIM[l_param[2]]):
                            stack.append(DICTconstrucionINTERIM[l_param[2]])
            else:  # backward check
                start_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], i_str) - 1
                end_slice = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], Nline) - 1
                print('Nline = ', Nline)
                print(f'start_slice = {start_slice}, end_slice = {end_slice}')
                for l_param in np_box.SHIFTcontainer.np_for_vars[start_slice: end_slice - 1: -1]:
                    print('l_param = ', l_param)
                    print('2 looking for stack: ', stack)
                    if l_param[2] in DICTconstructionsB:
                        stack.append(DICTconstructionsB[l_param[2]])
                    elif l_param[2] in DICTconstructionsF:
                        if len(stack) > 0 and stack[-1] == l_param[2]:
                            stack.pop(-1)
                    elif l_param[2] in DICTconstrucionINTERIM:
                        if not (len(stack) > 0 and stack[-1] == DICTconstructionsB[DICTconstrucionINTERIM[l_param[2]]]):
                            stack.append(DICTconstructionsB[DICTconstrucionINTERIM[l_param[2]]])
            print('goto Nline = {}'.format(Nline))
            if len(stack) != 0:
                print('alarm!!')
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line GOTO tryed to enter condition structure. Stopped\n'
                return None, False, i  # i_str+1
            return Nline, False, i  # todo check if False

    np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} GOTO is perplexed ¯\_(ツ)_/¯. Stopped\n'
    return None, False, i

def fanuc_if_goto(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    print('fanuc_if_goto')
    print('current_vars = ', current_vars)
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    print('res = ', res)
    if res is None or info[1][2] is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        return i_str + 1, False, i
    if res:
        return fanuc_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod, lbl_name=info[1][2])
    else:
        return i_str + 1, False, i

def siemens_if_goto(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    print('siemens_if_goto')
    print('current_vars = ', current_vars)
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    print('res = ', res)
    if res is None or info[1][2] is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        return i_str + 1, False, i
    if res:
        return siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod, lbl_name=info[1][2])
    else:
        return i_str + 1, False, i


def siemens_gotoF(np_box, info, current_vars, i_str, jumped_here, i, lbl_place=1, mod=0):
    return siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=1, lbl_name=info[1][1])


def siemens_gotoB(np_box, info, current_vars, i_str, jumped_here, i, lbl_place=1, mod=0):
    return siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=2, lbl_name=info[1][1])


def siemens_gotoC(np_box, info, current_vars, i_str, jumped_here, i, lbl_place=1, mod=0):
    return siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=3, lbl_name=info[1][1])


def siemens_gotoS(np_box, info, current_vars, i_str, jumped_here, i, lbl_place=1, mod=0):
    return 0, False


def siemens_if_gotoF(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    return siemens_if_goto(np_box, info, current_vars, i_str, jumped_here, i, mod=1)


def siemens_if_gotoB(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    return siemens_if_goto(np_box, info, current_vars, i_str, jumped_here, i, mod=2)


def siemens_if_gotoC(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    return siemens_if_goto(np_box, info, current_vars, i_str, jumped_here, i, mod=3)


def siemens_if_gotoS(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    if res is None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} line expression error\n'
        return i_str + 1, False, i
    if res:
        return 0, True, i
    else:
        return i_str + 1, False


def siemens_case_of_1line(np_box, info, current_vars, i_str, jumped_here, i, mod=0):
    print('siemens_case_of_1line start')
    print('info = ', info)
    exps = info[1][1]
    res = postfixTokenCalc(info[1][1][0], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    right_GOTO = info[1][2][-1]
    right_LBL = info[1][3][-1]
    for i in range(1, len(exps) - 1):
        if res == postfixTokenCalc(exps[i], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor):
            right_GOTO = info[1][2][i - 1]
            right_LBL = info[1][3][i - 1]
    if right_GOTO == '':
        return i_str + 1, False, i
    else:
        if right_GOTO == DICTshiftsINT['GOTOS']:
            return siemens_gotoS(np_box, info, current_vars, i_str, jumped_here, i)
        else:
            if right_GOTO == DICTshiftsINT['GOTO']:
                mod = 0
            elif right_GOTO == DICTshiftsINT['GOTOF']:
                mod = 1
            elif right_GOTO == DICTshiftsINT['GOTOB']:
                mod = 2
            elif right_GOTO == DICTshiftsINT['GOTOC']:
                mod = 3
            # right_LBL
            print('siemens_case_of_1line')
            print('right_LBL= ', right_LBL)
            return siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=mod, lbl_name=right_LBL)


def siemens_REPEAT_LBL(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line
    # что то напортачил
    print('siemens_REPEAT_LB')
    print('info = ', info)
    #2/0
    #first = False
    stack_DATA = [i_str, *info[1][1:]]
    if len(np_box.return_stack) == 0 or np_box.return_stack[-1][0] != i_str:
        print(f'FIRST REPEAT')
        #first = True
        len_logs = len(np_box.redactor.Logs.math_logs)
        Nline, jumped_here, i = siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=2, lbl_name=info[1][1])
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs[:len_logs]
        if Nline is None:
            Nline, jumped_here, i = siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=1, lbl_name=info[1][1])  # np_box.return_stack[-1][1]
        len_logs2 = len(np_box.redactor.Logs.math_logs)
        # if len_logs != len_logs2:
        if Nline is None:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'"{info[1][1][0]}" 1was not found - REPEAT Stopped\n'
            print(f'11return 333')
            return None, False, i
        info2 = np_box.SHIFTcontainer.return_info(Nline)
        if info[1][4] is not None:  # REPEATB

            stack_DATA[2] = stack_DATA[1]  # tuple([Nline])
            stack_DATA[3] = int(stack_DATA[3]) if stack_DATA[3] != '' else 1
            print('REPEAT stack_DATA = ', stack_DATA)
            np_box.special_instructions.append(REPEAT_lbl_instruction)
            np_box.return_stack.append(stack_DATA)
            print(f'11return 222')
            return Nline, jumped_here, i

        if info[1][2] is not None:
            Nline__, jumped_here__, i = siemens_goto_super(np_box, info2, current_vars, Nline, jumped_here, i, mod=1, lbl_name=tuple(info[1][2]))
            len_logs3 = len(np_box.redactor.Logs.math_logs)
            if len_logs2 != len_logs3:
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'"{info[1][2][0]}" 2was not found - REPEAT Stopped\n'
                print(f'11return 444')
                return None, False, i
            else:
                if Nline__ > i_str > Nline:
                    np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'"{info[1][1][0]}" and "{info[1][2][0]}" on opposite sides - REPEAT ignored\n'
                    print(f'11return 555')
                    return i_str + 1, False, i
        else:
            Nline__, jumped_here__ = siemens_goto_super(np_box, info2, current_vars, Nline, jumped_here, i, mod=1, lbl_name=tuple(['ENDLABEL']))
            len_logs3 = len(np_box.redactor.Logs.math_logs)
            if Nline < i_str:
                if len_logs2 != len_logs3 or Nline__ > i_str:  # or Nline < i_str < Nline__
                    print('end - REPEAT itself')
                    stack_DATA[2] = tuple([stack_DATA[0]])
                    # erase the error log. not catched - not bullied
                    np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs[:len_logs2]
                else:
                    stack_DATA[2] = tuple(['ENDLABEL'])
                    print(f'stack_DATA = {stack_DATA}')
            else:  # LBL2 = None, Nline > i_str
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'REPEAT need 2 labels if first label is on the front. Stopped\n'
                print(f'11return 666')
                return None, False, i#-1

        np_box.special_instructions.append(REPEAT_lbl_instruction)
        np_box.return_stack.append(stack_DATA)
        np_box.return_stack[-1][3] = postfixTokenCalc(np_box.return_stack[-1][3], proc=np_box.redactor.highlight.reversal_post_processor) if len(np_box.return_stack[-1][3]) != 0 else 1
        print(Nline)
    else:
        last_iter = True if np_box.return_stack[-1][3] == 1 else False
        if last_iter is True:
            np_box.return_stack.pop(-1)
            np_box.special_instructions.pop(-1)
            return i_str + 1, True, i#-1#TODO
        else:
            np_box.return_stack[-1][3] = np_box.return_stack[-1][3] - 1
            Nline, jumped_here, i = siemens_goto_super(np_box, info, current_vars, i_str, jumped_here, i, mod=0, lbl_name=np_box.return_stack[-1][1])
    i = i + 1
    return Nline, jumped_here, i


def fanuc_if_then(np_box, info, current_vars, i_str, jumped_here, i):
    print('fanuc_if_then')
    res = postfixTokenCalc(info[1][1], DICT_VARS=current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    if res and info[1][2] is not None:
        current_vars[info[1][2][0]] = postfixTokenCalc(info[1][2], current_vars, proc=np_box.redactor.highlight.reversal_post_processor)
    return i_str + 1, jumped_here, i

#def END_solving(np_box, info, current_vars, i_str, jumped_here, i):
#
#    return 1111, jumped_here, i


def SUB_program_siemens(np_box, info, current_vars, i_str, jumped_here, i):#TODO: не могу улучшить дома - нужно ещё раз в учебник посомтреть
    print('SUB_program_siemens')

    p_name = info[1][2][0]
    red = np_box.sub_programs_dict[p_name]
    if len(red.np_box.main_g_cod_pool) > 1:
        np_box.redactor.tab_.currentWidget().all_subs_count = np_box.redactor.tab_.currentWidget().all_subs_count + 1
        red.np_box.visible_np = red.np_box.main_g_cod_pool.copy()
        N_ = red.np_box.visible_np[0][15]
        red.np_box.visible_np[0][:] = np_box.last_significant_line4subprograms
        red.np_box.visible_np[0][15] = N_
        np_box.redactor.current_machine.k_devide_applying2line(red.np_box.visible_np[0])  # red.np_box.visible_np[0][:] =
        red.np_box.SUB_exchange_DATA = info[2]
        np_box.SHIFTcontainer.save_vars_as_local_global_func(np_box, current_vars, red, info)
        sub_main = red.np_box.visible_np
        L = len(sub_main)
        cur_frame_address = np.zeros((L, 2), int)

        NshiftCorrect =  np_box.redactor.subNstart #np_box.frame_address_in_visible_pool[-1][1] +#+ L
        cur_frame_address[:, 0] = np.arange(i_str+1, i_str + L+1)
        cur_frame_address[:, 1] = np.arange(NshiftCorrect,  NshiftCorrect + L)
        print(f'SUB: cur_frame_address = {cur_frame_address}')
        i = i + L
        sub_start_place_frame = np.copy(np_box.frame_address_in_visible_pool[-1])
        sub_start_place_frame[0] = i + 1
        np_box.frame_address_in_visible_pool = np.concatenate([np_box.frame_address_in_visible_pool, cur_frame_address])
        np_box.frame_address_in_visible_pool = np.concatenate([np_box.frame_address_in_visible_pool, [sub_start_place_frame]])
        print('sub_main = ', sub_main)
        sub_start_place = np_box.new_v[-1]
        np_box.new_v = np.concatenate([np_box.new_v, sub_main])
        np_box.new_v = np.concatenate([np_box.new_v, [sub_start_place]])
        np_box.last_significant_line4subprograms = red.np_box.last_significant_line4subprograms
    return i_str + 1, jumped_here, i+1


def MACRO_program_fanuc(np_box, info, current_vars, i_str, jumped_here, i):#TODO: ЕЩЁ НИЧЕГО НЕ ДЕЛАЛ.
    print('SUB_program_siemens')

    p_name = info[1][2][0]
    red = np_box.sub_programs_dict[p_name]
    if len(red.np_box.main_g_cod_pool) > 1:
        np_box.redactor.tab_.currentWidget().all_subs_count = np_box.redactor.tab_.currentWidget().all_subs_count + 1
        red.np_box.visible_np = red.np_box.main_g_cod_pool.copy()
        N_ = red.np_box.visible_np[0][15]
        red.np_box.visible_np[0][:] = np_box.last_significant_line4subprograms
        red.np_box.visible_np[0][15] = N_
        np_box.redactor.current_machine.k_devide_applying2line(red.np_box.visible_np[0])  # red.np_box.visible_np[0][:] =
        red.np_box.SUB_exchange_DATA = info[2]
        np_box.SHIFTcontainer.save_vars_as_local_global_func(np_box, current_vars, red, info)
        sub_main = red.np_box.visible_np
        L = len(sub_main)
        cur_frame_address = np.zeros((L, 2), int)

        NshiftCorrect =  np_box.redactor.subNstart #np_box.frame_address_in_visible_pool[-1][1] +#+ L
        cur_frame_address[:, 0] = np.arange(i_str+1, i_str + L+1)
        cur_frame_address[:, 1] = np.arange(NshiftCorrect,  NshiftCorrect + L)
        print(f'SUB: cur_frame_address = {cur_frame_address}')
        i = i + L
        sub_start_place_frame = np.copy(np_box.frame_address_in_visible_pool[-1])
        sub_start_place_frame[0] = i + 1
        np_box.frame_address_in_visible_pool = np.concatenate([np_box.frame_address_in_visible_pool, cur_frame_address])
        np_box.frame_address_in_visible_pool = np.concatenate([np_box.frame_address_in_visible_pool, [sub_start_place_frame]])
        print('sub_main = ', sub_main)
        sub_start_place = np_box.new_v[-1]
        np_box.new_v = np.concatenate([np_box.new_v, sub_main])
        np_box.new_v = np.concatenate([np_box.new_v, [sub_start_place]])
        np_box.last_significant_line4subprograms = red.np_box.last_significant_line4subprograms
    return i_str + 1, jumped_here, i+1

def PROG_start_siemens(np_box, info, current_vars, i_str, jumped_here, i):
    vars_ = np_box.SUB_exchange_DATA
    print(f'vars_ = {vars_}')
    n = 0
    if info[1][3] is None:
        return i_str + 1, jumped_here, i  # todo+1?
    L = len(info[1][3])
    if len(vars_)>1:
        if np_box.redactor.father_np_box is not None:
            for v in vars_[1]:#info[3]:
                if n == L:
                    np_box.redactor.tab_.currentWidget().Logs.math_logs = np_box.redactor.Logs.math_logs + f'PROC {info[1][1][1]} doesn\'t have that much vars. Error!\n'
                    break
                current_vars[info[1][3][n][-1]] = postfixTokenCalc(v, np_box.redactor.father_np_box.current_vars_dict, proc=np_box.redactor.highlight.reversal_post_processor)
                n+=1
    while n < L:
        if info[1][3][n]:
            current_vars[info[1][3][n][-1]] = postfixTokenCalc(info[1][4][n], proc=np_box.redactor.highlight.reversal_post_processor)
        n += 1
    if np_box.redactor.father_np_box is not None:
        np_box.SUB_exchange_DATA = []
        for D in info[1][3]:
            if D[0] == 'VAR':
                np_box.SUB_exchange_DATA.append([True, D[-1]])
            else:
                np_box.SUB_exchange_DATA.append([False, D[-1]])
    print(f'PROG_start_siemens:\n SUB_exchange_DATA = {np_box.SUB_exchange_DATA}, \n info = {info}')
    return i_str + 1, jumped_here, i#todo+1?


functions_dict = {DICTshiftsINT['WHILE']: classic_while, DICTshiftsINT['ENDWHILE']: classic_end_while,
                  DICTshiftsINT['IF_GOTO']: siemens_if_goto, DICTshiftsINT['IF_GOTOF']: siemens_if_gotoF,
                  DICTshiftsINT['IF_GOTOB']: siemens_if_gotoB, DICTshiftsINT['IF_GOTOC']: siemens_if_gotoC,
                  DICTshiftsINT['IF_GOTOS']: siemens_if_gotoS, DICTshiftsINT['GOTOS']: siemens_gotoS,
                  DICTshiftsINT['IF']: if_classic, DICTshiftsINT['ELSE']: else_if_classic,
                  DICTshiftsINT['GOTO']: siemens_goto_super, DICTshiftsINT['GOTOF']: siemens_gotoF,
                  DICTshiftsINT['GOTOB']: siemens_gotoB, DICTshiftsINT['GOTOC']: siemens_gotoC,
                  DICTshiftsINT['LOOP']: LOOPinfinite, DICTshiftsINT['END_LOOP']: END_LOOPinfinite,
                  DICTshiftsINT['FOR']: siemensFOR_TO, DICTshiftsINT['END_FOR']: siemens_end_FOR,
                  DICTshiftsINT['REPEATu']: classic_REPAT_until, DICTshiftsINT['UNTIL']: classic_UNTIL_repeat,
                  DICTshiftsINT['REPEAT_LB']: siemens_REPEAT_LBL, DICTshiftsINT['IF_THEN']: fanuc_if_then,
                  DICTshiftsINT['CASE']: siemens_case_of_1line, DICTshiftsINT['M30']: CNCpass,
                  DICTshiftsINT['SUB_PROG_START']: PROG_start_siemens, DICTshiftsINT['SUB_PROGRAM']: SUB_program_siemens,
                  DICTshiftsINT['GOTO_FANUC']: fanuc_goto_super, DICTshiftsINT['IF_GOTO_FANUC']: fanuc_if_goto,
                  DICTshiftsINT['MACRO_PROGRAM_FANUC']: MACRO_program_fanuc,
                   }



def IF_WHILE_what2do(np_box, info, current_vars, i_str, jumped_here, i):  # , local_line

    print('IF_WHILE_what2do')
    print('info = ', info)
    try:
        foo = functions_dict[info[0][2]]
    except:
        foo = CNCpass
    new_i_str, jumped_here, i = foo(np_box, info, current_vars, i_str, jumped_here, i)  # , local_line, pass_
    print(f'new_i_str = {new_i_str}')
    if new_i_str is not None:
        new_i_str = int(new_i_str)
    return new_i_str, jumped_here, i




