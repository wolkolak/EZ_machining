import math
import numpy as np

def R_from_ijk(v_i, n_h, n_v, n_p, last_significant_line):
    print('3333 n_h = ', n_h)
    print('last_significant_line[n_h] = ', last_significant_line[n_h])
    c_h = v_i[n_h+6] #+ last_significant_line[n_h]#
    c_v = v_i[n_v+6] #+ last_significant_line[n_v]#

    h2 = v_i[n_h]
    v2 = v_i[n_v]
    c_const_i = n_p + 6
    c_const_from_main_point_i = n_p
    if np.isnan(v_i[c_const_i]):
        v_i[c_const_i] = v_i[n_p]
    #else:
    #    if v_i[c_const_i] != v_i[c_const_from_main_point_i]:
    #        pass
    #        #print('ARK problem with G{}X{}Y{}Z{}I{}J{}K{}'.format(*v_i[3:7], *v_i[10:13]))
    print('here it is: ', c_h, c_v, h2, v2)
    R = math.sqrt((h2 - c_h)**2 + (v2 - c_v)**2)
    #v_i[11] = R
    return R

def centre_R_ARK(turn_direction, plane, v_iA, v_iC, n_h, n_v, n_p):
    print(f'plane = {plane}, type = {type(plane)}')
    print('turn_direction = {}, plane = {}, v_iA = {}, v_iC = {}, n_h = {}, n_v = {}, n_p = {}'.format(turn_direction, plane, v_iA, v_iC, n_h, n_v, n_p))
    R = v_iC[13]
    print('R = ', v_iC[13])
    V_A = v_iA[n_v]
    V_C = v_iC[n_v]
    H_A = v_iA[n_h]
    H_C = v_iC[n_h]
    d = math.sqrt((H_A - H_C) ** 2 + (V_A - V_C) ** 2)
    print('||d = ', d)
    for_sqrt = R ** 2 - (d / 2) ** 2
    if for_sqrt < 0:
        h = - math.sqrt(-for_sqrt)
    else:
        h = math.sqrt(for_sqrt)
    #print('H_C = {}, H_A = {}, V_C = {}, V_A = {}, d = {}'.format(H_C, H_A, V_C, V_A, d))
    H1 = H_A + (H_C - H_A) / 2 + h * (V_C - V_A) / d
    V1 = V_A + (V_C - V_A) / 2 - h * (H_C - H_A) / d
    H2 = H_A + (H_C - H_A) / 2 - h * (V_C - V_A) / d
    V2 = V_A + (V_C - V_A) / 2 + h * (H_C - H_A) / d
    #https://www.sql.ru/forum/158538/vychislenie-centra-okruzhnosti
    #Оба     решения     лежат     в     квадрате
    #min(X1, X2) - R <= X <= max(X1, X2) = R
    #min(Y1, Y2) - R <= Y <= max(Y1, Y2) = R

    #print('X = {}, Z = {}'.format(V1, H1))

    vector_cross1 = (H_C - H_A) * (V1 - V_A) - (V_C - V_A) * (H1 - H_A)
    #vector_cross2 = (H_C - H_A) * (V2 - V_A) - (V_C - V_A) * (H2 - H_A)
    #print('|||| vector_cross1 |||| = ', vector_cross1)
    k1 = -1 if vector_cross1 > 0 else 1
    gARK = -1 if turn_direction == 3 else 1
    if k1 * gARK * R > 0:#AHTUNG - remember G3 or G2 needed
        var1 = H1
        var2 = V1
    else:
        var1 = H2
        var2 = V2
    #print('plane in ark solving', type(plane))
    #if 2*R >= d:
    #    possible = True
    #else:
    #    possible = False
    possible = False if 2*abs(R) < d else True#todo check for min step
    if plane == '18':
        print('plan 18')
        return var2, v_iA[n_p], var1, possible #added last
    elif plane == '17':
        print('plan 17')
        return var1, var2, v_iA[n_p], possible #added last
    else:#19
        print('plan 19')
        return v_iA[n_p], var1, var2, possible #added last


def aroud_AXIS_ARK(X, Y, Z, A, B, C, machine):#todo допилить под вращающуюся башку
    """
    1 Goal - find where new dot laid
    2 Goal - make an ark there
    :return:
    """
    L_A = 100.; L_B = 200.; L_C = 300.

    pass