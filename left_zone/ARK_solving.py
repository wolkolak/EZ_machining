import math

#xA, yA, zA, xB, yB, zB, xC, yC, zC, R
#l_chord = 0.01
#polyglobal_center = ....
#polyglobal_R = ....
#np_mini_array = ....
#poluglobal_i = -1
#
#Vx = xB - xA
#Vy = yB - yA
#Vz = zB - zA


# l_chord_max = max(Vx, Vy, Vz)/100
# if l_chord < l_chord_max:
#    l_chord = l_chord_max


def centre_R_ARK(turn_direction, plane, R, xA, yA, zA, xC, yC, zC,):
    print('xC = ', xC)
    if plane == 18:
        V_A = xA
        V_C = xC
        H_A = zA
        H_C = zC
    elif plane == 17:
        V_A = yA
        V_C = yC
        H_A = xA
        H_C = xC
    else:#19
        V_A = zA
        V_C = zC
        H_A = yA
        H_C = yC

    d = math.sqrt((H_A - H_C) **2 + (V_A - V_C) **2)
    for_sqrt = R **2 - (d / 2) **2
    if for_sqrt < 0:
        h = - math.sqrt(-for_sqrt)
    else:
        h = math.sqrt(for_sqrt)
    H1 = H_A + (H_C - H_A) / 2 + h * (V_C - V_A) / d
    V1 = V_A + (V_C - V_A ) / 2 - h * (H_C - H_A) / d
    H2 = H_A + (H_C - H_A) / 2 - h * (V_C - V_A ) / d
    V2 = V_A + (V_C - V_A ) / 2 + h * (H_C - H_A) / d
    #https://www.sql.ru/forum/158538/vychislenie-centra-okruzhnosti
    #Оба     решения     лежат     в     квадрате
    #min(X1, X2) - R <= X <= max(X1, X2) = R
    #min(Y1, Y2) - R <= Y <= max(Y1, Y2) = R



    #a = math.atan((H_C-H_A) / (V_A-V_C))
    #for_asin = math.sqrt((V_C-V_A)**2 + (H_C-H_A)**2) / (2*R)
    #leftother = for_asin % 1
    #if leftother != 0:
    #    for_asin = leftother
    #b = math.asin(for_asin)
    #H1 = H_A - R * math.cos(a+b)
    #V1 = V_A - R * math.sin(a+b)
    #H2 = H_A - R * math.cos(a+b)
    #V2 = V_A - R * math.sin(a+b)
    print('X = {}, Z = {}'.format(V1, H1))

    vector_cross1 = (H_C - H_A) * (V1 - V_A) - (V_C - V_A) * (H1 - H_A)
    #vector_cross2 = (H_C - H_A) * (V2 - V_A) - (V_C - V_A) * (H2 - H_A)

    k1 = -1 if vector_cross1 > 0 else 1
    gARK = -1 if turn_direction == 3 else 2
    if k1 * gARK * R > 0:
        var1 = H1
        var2 = V1
    else:
        var1 = H2
        var2 = V2
    if plane == 18:
        return var2, yA, var1
    elif plane == 17:
        return var1, var2, zA
    else:
        return xA, var1, var2




#def middle_chord_devide(xA, yA, zA, xC, yC, zC, l_current):
#    if l_current > l_chord:
#        i + +
#        xB, yB, zB = find_xB_yB_zB(xA, yA, zA, xC, yC,
#                                   polyglobal_center, polyglobal_R)
#
#        l_current = l_current / 2
#
#        middle_chord_devide(xA, yA, zA, xB, yB, zB, l_current)
#
#        np_mini_array[i] = xB, yB, zB
#
#        middle_chord_devide(xB, yB, zB, xC, yC, zC, l_current)
#
#
#def find_xB_yB_zB(xA, yA, zA, xC, yC, zC, polyglobal_center, polyglobal_R):
#    xB = (xA + xC) / 2
#    yB = (yA + yC) / 2
#    zB = (zA + zC) / 2
#
#    r = math.dist(Center_X, Center_Y, Center_Z, xC, yC, zC)
#    d = R - r
#    Vx = xB - Center_X
#    Vy = yB - Center_Y
#    Vz = zB - Center_Z

#    k = d / r
#    xB = xB + k * Vx
#    yB = yB + k * Vy
#    zB = zB + k * Vz
#    return xB, yB, zC
