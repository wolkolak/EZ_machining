xA, yA, zA, xB, yB, zB, xC, yC, zC, R
l_chord = 0.01
polyglobal_center = ....
polyglobal_R = ....
np_mini_array = ....
poluglobal_i = -1

Vx = xB - xA
Vy = yB - yA
Vz = zB - zA


# l_chord_max = max(Vx, Vy, Vz)/100
# if l_chord < l_chord_max:
#    l_chord = l_chord_max

def middle_chord_devide(xA, yA, zA, xC, yC, zC, l_current):
    if l_current > l_chord:
        i + +
        xB, yB, zB = find_xB_yB_zB(xA, yA, zA, xC, yC,
                                   polyglobal_center, polyglobal_R)

        l_current = l_current / 2

        middle_chord_devide(xA, yA, zA, xB, yB, zB, l_current)

        np_mini_array[i] = xB, yB, zB

        middle_chord_devide(xB, yB, zB, xC, yC, zC, l_current)


def find_xB_yB_zB(xA, yA, zA, xC, yC, zC, polyglobal_center, polyglobal_R):
    xB = (xA + xC) / 2
    yB = (yA + yC) / 2
    zB = (zA + zC) / 2

    r = math.dist(Center_X, Center_Y, Center_Z, xC, yC, zC)
    d = R - r
    Vx = xB - Center_X
    Vy = yB - Center_Y
    Vz = zB - Center_Z

    k = d / r
    xB = xB + k * Vx
    yB = yB + k * Vy
    zB = zB + k * Vz
    return xB, yB, zC
