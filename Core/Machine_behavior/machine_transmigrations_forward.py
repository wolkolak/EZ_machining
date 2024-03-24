import math
import numpy as np
from OpenGL.GL import *

#todo total = np.array([[x, y, z, 1]])



A_rotTabl = np.array([
    [1., 0., 0., 0.],
    [0., 0., 0., 0.],
    [0., 0., 0., 0.],
    [0., 0., 0., 1.]
])

B_rotTabl = np.array([
    [0., 0., 0., 0.],
    [0., 1., 0., 0.],
    [0., 0., 0., 0.],
    [0., 0., 0., 1.]
])

C_rotTabl = np.array([
        [0., 0., 0., 0.],
        [0., 0., 0., 0.],
        [0., 0., 1., 0.],
        [0., 0., 0., 1.]
])

total = np.array([[0., 0., 0., 1.]])
#total = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])







def fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк

    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] = math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] = math.cos(c)

    b = math.radians(b)
    B_rotTabl[0, 0] =  math.cos(b);  B_rotTabl[0, 2] =-math.sin(b)
    B_rotTabl[2, 0] =  math.sin(b);  B_rotTabl[2, 2] = math.cos(b)

    a = math.radians(a)
    A_rotTabl[1, 1] =  math.cos(a);  A_rotTabl[1, 2] = math.sin(a)
    A_rotTabl[2, 1] = -math.sin(a);  A_rotTabl[2, 2] = math.cos(a)


    total0 = total.dot(A_rotTabl)
    total0 = total0.dot(B_rotTabl)
    total0 = total0.dot(C_rotTabl)

    #total0 = total.dot(A_rotTabl)
    #total0 = total0.dot(B_rotTabl)
    #total0 = total0.dot(C_rotTabl)

    return total0





def fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):  # наверное тут косяк
    c = math.radians(c)
    C_rotTabl[0, 0] = math.cos(c);    C_rotTabl[0, 1] = math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);   C_rotTabl[1, 1] = math.cos(c)
    b = math.radians(b)
    B_rotTabl[0, 0] = math.cos(b);    B_rotTabl[0, 2] = -math.sin(b)
    B_rotTabl[2, 0] = math.sin(b);    B_rotTabl[2, 2] = math.cos(b)

    total0 = total.dot(B_rotTabl)
    total0 = total0.dot(C_rotTabl)

    #total0 = total.dot(B_rotTabl)
    #total0 = total0.dot(C_rotTabl)

    return total0




def fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк

    a = math.radians(a)
    A_rotTabl[1, 1] =  math.cos(a);  A_rotTabl[1, 2] = math.sin(a)
    A_rotTabl[2, 1] = -math.sin(a);  A_rotTabl[2, 2] = math.cos(a)

    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] = math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] = math.cos(c)

    total0 = total.dot(A_rotTabl)
    total0 = total0.dot(C_rotTabl)

    #total0 = total.dot(A_rotTabl)
    #total0 = total0.dot(C_rotTabl)

    return total0


def fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк
    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] = math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] = math.cos(c)
    total0 = total.dot(C_rotTabl)
    return total0












def Pass_abc(param_list, X, Y, Z):
    pass


def TR_ABC(param_list, X, Y, Z):#Здесь C

    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def TR_BC(param_list, X, Y, Z):#Здесь C
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def TR_AC(param_list, X, Y, Z):#Здесь C
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def TR_C(param_list, X, Y, Z):#Здесь C

    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]



#тут пробовать


def TR_inverse_ABC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def TR_inverse_BC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def TR_inverse_AC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def TR_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]






def RT_ABC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def RT_BC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def RT_AC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def RT_C(param_list, X, Y, Z):#todo плюс???
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]







def RT_inverse_ABC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def RT_inverse_BC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def RT_inverse_AC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def RT_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def R_ABC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def R_BC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def R_AC(param_list, X, Y, Z):
    #return  X, Y, Z
    #print('R_AC = ', param_list)
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def R_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]




def R_inverse_ABC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]




def R_inverse_BC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_BC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]



def R_inverse_AC(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_AC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def R_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def T_abc(param_list, X, Y, Z):# todo заменить на единую операцию сложения numpy
    #todo - и то ближе результат даёт. хз почему
    X += param_list[0]
    Y += param_list[1]
    Z += param_list[2]
    return X, Y, Z


