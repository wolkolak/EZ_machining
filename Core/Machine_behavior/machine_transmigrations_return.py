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







def fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк

    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] =  math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] =  math.cos(c)

    b = math.radians(b)
    B_rotTabl[0, 0] =  math.cos(b);  B_rotTabl[0, 2] = -math.sin(b)
    B_rotTabl[2, 0] =  math.sin(b);  B_rotTabl[2, 2] =  math.cos(b)

    a = math.radians(a)
    A_rotTabl[1, 1] =  math.cos(a);  A_rotTabl[1, 2] =  math.sin(a)
    A_rotTabl[2, 1] = -math.sin(a);  A_rotTabl[2, 2] =  math.cos(a)

    total0 = total.dot(C_rotTabl)
    total0 = total0.dot(B_rotTabl)
    total0 = total0.dot(A_rotTabl)

    return total0


def fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):  # наверное тут косяк
    c = math.radians(c)
    C_rotTabl[0, 0] = math.cos(c);    C_rotTabl[0, 1] = math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);    C_rotTabl[1, 1] = math.cos(c)
    b = math.radians(b)
    B_rotTabl[0, 0] = math.cos(b);    B_rotTabl[0, 2] = -math.sin(b)
    B_rotTabl[2, 0] = math.sin(b);    B_rotTabl[2, 2] = math.cos(b)
    total0 = total.dot(C_rotTabl)
    total0 = total0.dot(B_rotTabl)
    return total0




def fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк

    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] =  math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] =  math.cos(c)

    a = math.radians(a)
    A_rotTabl[1, 1] =  math.cos(a);  A_rotTabl[1, 2] =  math.sin(a)
    A_rotTabl[2, 1] = -math.sin(a);  A_rotTabl[2, 2] =  math.cos(a)

    total0 = total.dot(C_rotTabl)
    total0 = total0.dot(A_rotTabl)

    return total0


def fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, a, b, c, total):#наверное тут косяк
    c = math.radians(c)
    C_rotTabl[0, 0] =  math.cos(c);  C_rotTabl[0, 1] =  math.sin(c)
    C_rotTabl[1, 0] = -math.sin(c);  C_rotTabl[1, 1] =  math.cos(c)
    total0 = total.dot(C_rotTabl)
    return total0












def returnPass_cba(param_list, X, Y, Z):
    return X, Y, Z


def return_TR_CBA(param_list, X, Y, Z):#Здесь C

    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_TR_CB(param_list, X, Y, Z):#Здесь C
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_TR_CA(param_list, X, Y, Z):#Здесь C
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def return_TR_C(param_list, X, Y, Z):#Здесь C

    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]






def return_TR_inverse_CBA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_TR_inverse_CB(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_TR_inverse_CA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def return_TR_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total[0][0] = total[0][0] + param_list[0]
    total[0][1] = total[0][1] + param_list[1]
    total[0][2] = total[0][2] + param_list[2]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]






def return_RT_CBA(param_list, X, Y, Z):
    #print('return_RT_CBA')
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def return_RT_CB(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def return_RT_CA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def return_RT_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]







def return_RT_inverse_CBA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def return_RT_inverse_CB(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def return_RT_inverse_CA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]


def return_RT_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    #total0 = return_rotate_func(total)
    total0[0][0] = total0[0][0] + param_list[0]
    total0[0][1] = total0[0][1] + param_list[1]
    total0[0][2] = total0[0][2] + param_list[2]
    return total0[0][0], total0[0][1], total0[0][2]

def return_R_CBA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_R_CB(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def return_R_CA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]


def return_R_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]




def return_R_inverse_CBA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CBA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]




def return_R_inverse_CB(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CB(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]



def return_R_inverse_CA(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_CA(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]

def return_R_inverse_C(param_list, X, Y, Z):
    total[0] = [X, Y, Z, 1]
    total0 = fillRotTabs_C(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], -param_list[8], total)
    return total0[0][0], total0[0][1], total0[0][2]



def return_T_cba(param_list, X, Y, Z):# todo заменить на единую операцию сложения numpy
    #todo - и то ближе результат даёт. хз почему
    X += param_list[0]
    Y += param_list[1]
    Z += param_list[2]
    return X, Y, Z





#glRotate(smallSC[2][0], 1, 0, 0)  # A
#            glRotate(smallSC[2][1], 0, 1, 0)  # B
#            glRotate(smallSC[2][2], 0, 0, 1)  # C


#def order_rotation(order:str, A, B, C):
#    pass


if __name__ == "__main__":
    import time
    from scipy.spatial.transform import Rotation

    #g54_g59_AXIS_Delta = {'G54': [0.0, 0.0, 0.0, 0.0, 0, 0], 'G55': [500.0, 0.0, 400.0, 0.0, 0.0, 0.0], 'G56': [1000.0, 0.0, 500.0, 0.0, 0.0, 0.0],
    # 'G57': [1000.0, 0.0, 500.0, 0.0, 0.0, 0.0], 'G58': [1000.0, 0.0, 500.0, 0.0, 0.0, 90.0], 'G59': [1000.0, 0.0, 500.0, 0.0, 0.0, 0.0]}

    G549shift = [500.0, 0.0, 400.0, 0.0, 0.0, 0.0]
    k = 1
    #[dx, dy, dz, 0, 0, 0, -self.main_G549['A'], -self.main_G549['B'], -self.main_G549['C']]
    param_list = [k*G549shift[0], k*G549shift[1], k*G549shift[2], None, None, None, 0, 90, 90]
    v_i = np.zeros((19, 1), float)
    v_i[16] = np.nan
    v_i[4] = 4.
    v_i[5] = 5.
    v_i[6] = 6.
    v_i[7] = 7.
    v_i[8] = 8.
    v_i[9] = 9.





    ff = 10000
    t0 = time.time()
    while ff > 0:
        v_i[4], v_i[5], v_i[6] = return_R_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
        ff -=1

    t1 = time.time()

    total_time = t1 - t0
    print(f'2 v_i = {v_i}, time_time  = {total_time }')



    euler_angles = np.array([90., 90, 90.])

    ff = 10000
    t0 = time.time()
    while ff > 0:
        rotation = Rotation.from_euler('xyz', euler_angles)
        ff -=1
    t1 = time.time()
    total_time = t1 - t0
    print(f'3 v_i = {v_i}, time_time  = {total_time }')