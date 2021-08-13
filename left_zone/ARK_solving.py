import math
import numpy as np

def centre_ijk_ARK(v_i, n_h, n_v, n_p):
    c_h = v_i[n_h+6]
    c_v = v_i[n_v+6]
    h2 = v_i[n_h]
    v2 = v_i[n_v]
    c_const_i = n_p + 6
    c_const_from_main_point_i = n_p
    if np.isnan(v_i[c_const_i]):
        v_i[c_const_i] = v_i[c_const_i - 6]
    else:
        if v_i[c_const_i] != v_i[c_const_from_main_point_i]:
            pass
            #print('ARK problem with G{}X{}Y{}Z{}I{}J{}K{}'.format(*v_i[3:7], *v_i[10:13]))
    R = math.sqrt((h2 - c_h)**2 + (v2 - c_v)**2)
    #v_i[11] = R
    return R

def centre_R_ARK(turn_direction, plane, v_iA, v_iC, n_h, n_v, n_p):
    R = v_iC[13]
    V_A = v_iA[n_v]
    V_C = v_iC[n_v]
    H_A = v_iA[n_h]
    H_C = v_iC[n_h]
    d = math.sqrt((H_A - H_C) **2 + (V_A - V_C) **2)
    for_sqrt = R **2 - (d / 2) **2
    if for_sqrt < 0:
        h = - math.sqrt(-for_sqrt)
    else:
        h = math.sqrt(for_sqrt)
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

    k1 = -1 if vector_cross1 > 0 else 1
    gARK = -1 if turn_direction == 3 else 1
    if k1 * gARK * R > 0:#todo here might be a problem
        var1 = H1
        var2 = V1
    else:
        var1 = H2
        var2 = V2
    #print('plane in ark solving', type(plane))
    if plane == '18':
        #print('plan 18')
        return var2, v_iA[n_p], var1
    elif plane == '17':
        #print('plan 17')
        return var1, var2, v_iA[n_p]
    else:#19
        #print('plan 19')
        return v_iA[n_p], var1, var2
