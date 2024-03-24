

from Core.Machine_behavior.machine_transmigrations_return import *
from Core.Machine_behavior.machine_transmigrations_forward import *


#abc = [1, 2, 3]

def return_TR(abc):
    if abc[0] != 0 and abc[1] != 0:#CBA
        f = return_TR_CBA
        f2 = RT_ABC
    elif abc[0] != 0 and abc[1] == 0:#CA
        f = return_TR_CA
        f2 = RT_AC
    elif abc[0] == 0 and abc[1] != 0:#CB
        f = return_TR_CB
        f2 = RT_BC
    else:#C
        f = return_TR_C
        f2 = RT_C
    return f, f2

def return_TR_inverse(abc):
    if abc[0] != 0 and abc[1] != 0:  # CBA
        f = return_TR_inverse_CBA
        f2 = RT_inverse_ABC
    elif abc[0] != 0 and abc[1] == 0:  # CA
        f = return_TR_inverse_CA
        f2 = RT_inverse_AC
    elif abc[0] == 0 and abc[1] != 0:  # CB
        f = return_TR_inverse_CB
        f2 = RT_inverse_BC
    else:  # C
        f = return_TR_inverse_C
        f2 = RT_inverse_C
    return f, f2


def return_RT(abc):
    if abc[0] != 0 and abc[1] != 0:  # CBA
        f = return_RT_CBA
        f2 = TR_ABC
    elif abc[0] != 0 and abc[1] == 0:  # CA
        f = return_RT_CA
        f2 = TR_AC
    elif abc[0] == 0 and abc[1] != 0:  # CB
        f = return_RT_CB
        f2 = TR_BC
    else:  # C
        f = return_RT_C
        f2 = TR_C
    return f, f2




def return_RT_inverse(abc):
    if abc[0] != 0 and abc[1] != 0:  # CBA
        f = return_RT_inverse_CBA
        f2 = TR_inverse_ABC
    elif abc[0] != 0 and abc[1] == 0:  # CA
        f = return_RT_inverse_CA
        f2 = TR_inverse_AC
    elif abc[0] == 0 and abc[1] != 0:  # CB
        f = return_RT_inverse_CB
        f2 = TR_inverse_BC
    else:  # C
        f = return_RT_inverse_C
        f2 = TR_inverse_C
    return f, f2




def return_R(abc):
    #return returnPass_cba, returnPass_cba
    if abc[0] != 0 and abc[1] != 0:  # CBA
        f = return_R_CBA
        f2 = R_ABC
    elif abc[0] != 0 and abc[1] == 0:  # CA
        f = return_R_CA
        f2 = R_AC
    elif abc[0] == 0 and abc[1] != 0:  # CB
        f = return_R_CB
        f2 = R_BC
    else:  # C
        f = return_R_C
        f2 = R_C
    return f, f2



def return_R_inverse(abc):
    if abc[0] != 0 and abc[1] != 0:  # CBA
        f = return_R_inverse_CBA
        f2 = R_inverse_ABC
    elif abc[0] != 0 and abc[1] == 0:  # CA
        f = return_R_inverse_CA
        f2 = R_inverse_AC
    elif abc[0] == 0 and abc[1] != 0:  # CB
        f = return_R_inverse_CB
        f2 = R_inverse_BC
    else:  # C
        f = return_R_inverse_C
        f2 = R_inverse_C
    return f, f2

def returnPass(abc):
    return returnPass_cba, Pass_abc

def return_T(abc):
    return return_T_cba, T_abc
