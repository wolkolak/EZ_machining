from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT
import numpy as np



def helper_for_GOTO_N(np_box, info, i_str, lbl, mod):
    """
    look for Nline in main_g_cod_pool
    :return: newi_str
    """


    if mod == 0 or mod == 3:
        print('lbl[1:] = ', lbl[1:])
        Nlines = np.where(np_box.main_g_cod_pool[i_str:, 0] == int(lbl[1:]))
        print('1 Nlines = ', Nlines)
        Nline = None
        if len(Nlines[0]) != 0:
            Nline = Nlines[0][0] + i_str
        else:#backward
            Nlines = np.where(np_box.main_g_cod_pool[:i_str, 0] == int(lbl[1:]))
            print('2 Nlines = ', Nlines)
            if len(Nlines[0]) != 0:
                Nline = Nlines[0][-1]
        if Nline is None:
            if mod == 0:
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Stopped\n'
                return None
            else:
                np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Continued\n'
                return i_str + 1

    elif mod == 1:
        Nline = np.where(np_box.main_g_cod_pool[i_str:, 0] == int(lbl[1:]))#todo
        if len(Nline[0]) == 0:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Stopped\n'
            return None
        Nline = Nline[0][0]
    elif mod == 2:
        Nline = np.where(np_box.main_g_cod_pool[:i_str, 0] == int(lbl[1:]))
        if len(Nline[0]) == 0:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Stopped\n'
            return None
        Nline = Nline[0][-1]
    print('по итогу Nline = ', Nline)
    return Nline


def fanuc_helper_for_GOTO_N(np_box, info, i_str, lbl):
    """
    look for Nline in main_g_cod_pool
    :return: newi_str
    """


    #if mod == 0 or mod == 3:
    #print('lbl[1:] = ', lbl[1:])
    Nlines = np.where(np_box.main_g_cod_pool[i_str:, 0] == int(lbl))
    print('1 Nlines = ', Nlines)
    Nline = None
    if len(Nlines[0]) != 0:
        Nline = Nlines[0][0] + i_str
    else:#backward
        Nlines = np.where(np_box.main_g_cod_pool[:i_str, 0] == int(lbl))
        print('2 Nlines = ', Nlines)
        if len(Nlines[0]) != 0:
            Nline = Nlines[0][-1]
    if Nline is None:
        #if mod == 0:
        #    np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Stopped\n'
        #    return None
        #else:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} indirect line for GOTO was not found. Continued\n'
        return i_str + 1

    print('по итогу Nline = ', Nline)
    return Nline



def helper_for_GOTO_LBL(np_box, info, i_str, lbl, mod):
    #Nlines = np.where(np_box.SHIFTcontainer.np_for_vars[:, 2] == 41)
    print('helper_for_GOTO_LBL')
    print(f' info = {info}')
    local_line = info[2]
    print('new indo = ', info)
    print('local_line = ', local_line)
    print('mod = ', mod)
    #проблема в том что я хватаю local_line репита. жопа

    Nline = None
    if mod == 0 or mod == 3:#todo да так нельзя. Для mod 0 И mod 3 нужно поставить универсальный поиск
        Nlines = np.where(np_box.SHIFTcontainer.np_for_vars[local_line:, 1] == DICTshiftsINT['LABEL'])
        if len(Nlines[0]) != 0:#forward try
            print('1 problems with Nlines = ', Nlines)
            for NL in Nlines[0]:
                key_ = np_box.SHIFTcontainer.np_for_vars[NL+local_line, 3]
                if np_box.SHIFTcontainer.base_dict[key_][0] == lbl:
                    Nline = np_box.SHIFTcontainer.np_for_vars[NL+local_line, 0]
                    break

        if Nline is None:#backward try
            Nlines = np.where(np_box.SHIFTcontainer.np_for_vars[:local_line, 1] == DICTshiftsINT['LABEL'])
            print('problems with Nlines = ', Nlines)
            if len(Nlines[0]) == 0:
                if mod == 0:
                    return None
                else:
                    return i_str + 1
            for NL in reversed(Nlines[0]):
                key_ = np_box.SHIFTcontainer.np_for_vars[NL, 3]
                if np_box.SHIFTcontainer.base_dict[key_][0] == lbl:
                    Nline = np_box.SHIFTcontainer.np_for_vars[NL, 0]
                    break
    elif mod == 1:
        Nlines = np.where(np_box.SHIFTcontainer.np_for_vars[local_line:, 1] == DICTshiftsINT['LABEL'])
        print(f'ffffggg {Nlines}')

        if len(Nlines[0]) != 0:#forward try
            print('1 problems with Nlines = ', Nlines)
            for NL in Nlines[0]:
                print(f'iii NL = {NL}')
                key_ = np_box.SHIFTcontainer.np_for_vars[NL+local_line, 3]
                print(f'ddd {np_box.SHIFTcontainer.base_dict[key_][0]} vs {lbl}')
                if np_box.SHIFTcontainer.base_dict[key_][0] == lbl:
                    Nline = np_box.SHIFTcontainer.np_for_vars[NL+local_line, 0]
                    break
    elif mod == 2:
        Nlines = np.where(np_box.SHIFTcontainer.np_for_vars[:local_line, 1] == DICTshiftsINT['LABEL'])
        print('problems with Nlines = ', Nlines)
        if len(Nlines[0]) == 0:
            np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} label_ for GOTO was not found. Stopped\n'
            return None
        for NL in reversed(Nlines[0]):
            key_ = np_box.SHIFTcontainer.np_for_vars[NL, 3]
            if np_box.SHIFTcontainer.base_dict[key_][0] == lbl:
                Nline = np_box.SHIFTcontainer.np_for_vars[NL, 0]
                break
    if Nline == None:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][0]} label_ for GOTO was not found. Stopped\n'
        print(f'len(np_box.visible_np) = {len(np_box.visible_np)}')
        Nline = len(np_box.visible_np)-1
    print('taak1 Nline: ', Nline)
    #Nline = np_box.SHIFTcontainer.np_for_vars[Nline][0]
    print('taak Nline: ', Nline)

    return Nline
