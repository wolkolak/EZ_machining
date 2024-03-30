import  math
import numpy as np
import copy

from typing import List

from Core.Data_solving.added_special_instructions_in_solving import turn_around_C

def matrixis_return(ox, oy, oz, ax, ay, az):

    rotation_matrix_x = np.array([[1, 0, 0, 0],
                                  [0, np.cos(ax), -np.sin(ax), 0],
                                  [0, np.sin(ax), np.cos(ax), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_y = np.array([[np.cos(ay), 0, np.sin(ay), 0],
                                  [0, 1, 0, 0],
                                  [-np.sin(ay), 0, np.cos(ay), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_z = np.array([[np.cos(az), -np.sin(az), 0, 0],
                                  [np.sin(az), np.cos(az), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

    #transformation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)
    transformation_matrix = np.dot(np.dot(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)

    transformation_matrix = np.linalg.inv(transformation_matrix)
    #transformation_matrix[3,:] = ox, oy, oz, 1
    transformation_matrix[:, 3] = ox, oy, oz, 1
    return transformation_matrix#translation_matrix, rotation_matrix_x, rotation_matrix_y, rotation_matrix_z


def matrixis_returnCBA(ox, oy, oz, ax, ay, az):

    rotation_matrix_x = np.array([[1, 0, 0, 0],
                                  [0, np.cos(ax), -np.sin(ax), 0],
                                  [0, np.sin(ax), np.cos(ax), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_y = np.array([[np.cos(ay), 0, np.sin(ay), 0],
                                  [0, 1, 0, 0],
                                  [-np.sin(ay), 0, np.cos(ay), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_z = np.array([[np.cos(az), -np.sin(az), 0, 0],
                                  [np.sin(az), np.cos(az), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

    #transformation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)
    #transformation_matrix = np.dot(np.dot(rotation_matrix_x, rotation_matrix_y), rotation_matrix_z)
    transformation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)

    transformation_matrix = np.linalg.inv(transformation_matrix)
    #transformation_matrix[3,:] = ox, oy, oz, 1
    transformation_matrix[:, 3] = ox, oy, oz, 1
    return transformation_matrix


def vinoska_vremennaya_pod_CYCLE800(v_i, current_g_modal):
    print('solving CYCLE800')
    print(current_g_modal['CYCLE800'])
    v_i[4] = v_i[4] + current_g_modal['CYCLE800'][2][0]
    v_i[5] = v_i[5] + current_g_modal['CYCLE800'][2][1]
    v_i[6] = v_i[6] + current_g_modal['CYCLE800'][2][2]
    v_i[4:7] = np.dot([v_i[4:7]], current_g_modal['CYCLE800'][1])  # + translation_vector
    v_i[4] = v_i[4] + current_g_modal['CYCLE800'][0][0]
    v_i[5] = v_i[5] + current_g_modal['CYCLE800'][0][1]
    v_i[6] = v_i[6] + current_g_modal['CYCLE800'][0][2]

#def curentSC_4_many_dots(dots: np.ndarray, CYCLE800):#Отрабатываю вариант без цикла 800
#    print(f'curentSC_4_many_dots = {CYCLE800}')
#    uu = np.array([CYCLE800[3:6]])
#    print('uu = ', uu)
#    print(f'dots[:, 17:20] = {dots[:, 17:20]}')
#    #dots[:, 17:20] = np.dot(dots[:, 17:20], uu)  # + translation_vector
#    #dots[:, 17:20] = np.dot(dots[:, 17:20], CYCLE800[3:][np.newaxis, :])
#    param_list = [CYCLE800[0], CYCLE800[1], CYCLE800[2], 0, 0, 0, CYCLE800[3], CYCLE800[4], CYCLE800[5]]  # ABC были
    #    с -
#    total[0] = [dots[:, 17], dots[:, 18], dots[:, 19]]
#    points = np.hstack((points, np.ones((points.shape[0], 1))))
#
#    total0 = fillRotTabs_ABC(A_rotTabl, B_rotTabl, C_rotTabl, param_list[6], param_list[7], param_list[8], total)
#
    #dots[:, 17] += CYCLE800[0]
    #dots[:, 18] += CYCLE800[1]
    #dots[:, 19] += CYCLE800[2]


def CYCLE800_4_many_dots(dots: np.ndarray, CYCLE800):
    print(f'CYCLE800_4_many_dots = {CYCLE800}')
    #CYCLE800_4_many_dots =
    # [[-56.75, 0.0, -18.0], - XYZ

    # array([
    # [0.00, -1., 0.00],
    # [0., 0.00, 1.],
    # [-1., -0.00, 0.]]),

    # [0.0, 0.0, 0.0] - XYZ после
    # ]
    # Данные по факту предобработаны
    dots[:, 17] = dots[:, 17] + CYCLE800[2][0]
    dots[:, 18] = dots[:, 18] + CYCLE800[2][1]
    dots[:, 19] = dots[:, 19] + CYCLE800[2][2]
    dots[:, 17:] = np.dot([dots[:, 17:]], CYCLE800[1])  # + translation_vector
    dots[:, 17] = dots[:, 17] + CYCLE800[0][0]
    dots[:, 18] = dots[:, 18] + CYCLE800[0][1]
    dots[:, 19] = dots[:, 19] + CYCLE800[0][2]





def trans_matrix_from_SC(G549, C800):
    """
    I will use rot matrix, not transformation. because this will be faster. Ill move cords beforehand in old matrix to compensate dX, dY, dZ
    :param G549:
    :param C800:
    :return: summirize matrix
    """
    transformation_matrixC800: np.ndarray = np.eye(4)
    # C800 =
    # [[-56.75, 0.0, -18.0], - XYZ
    # array([
    # [0.00, -1., 0.00],
    # [0., 0.00, 1.],
    # [-1., -0.00, 0.]]),
    # [0.0, 0.0, 0.0] - XYZ после
    # ]
    if C800 is not None:
        rotC800: np.ndarray = C800[1]
        rotC800 = np.append(rotC800, [[0], [0], [0]], axis=1)
        rotC800 = np.append(rotC800, [[0, 0, 0, 1]], axis=0)
        #rotC800 = rotC800 + [0, 0, 0, 1]
        print(f'rotC800 = {rotC800}')
        if any(C800[2]):
            ox, oy, oz = C800[2][0:3]
            #C800. добавить сюда столбец и строку с конца
            translation_matrix = np.array([[1, 0, 0, ox],
                                           [0, 1, 0, oy],
                                           [0, 0, 1, oz],
                                           [0, 0, 0, 1]])
            transformation_matrixC800 = translation_matrix.dot(rotC800)
            #assert transformation_matrixC800[3, 3]
        else:
            transformation_matrixC800 = rotC800
            print(f'transformation_matrixC800[3, 3] = {transformation_matrixC800[3, 3]}')
            #assert transformation_matrixC800[3, 3]#TODO ПОМЕНЯТЬ


        #transformation_matrixC800 = np.linalg.inv(transformation_matrixC800)
        ox, oy, oz = C800[0][0:3]
        transformation_matrixC800[3, 0] = transformation_matrixC800[3, 0] + ox
        transformation_matrixC800[3, 1] = transformation_matrixC800[3, 1] + oy
        transformation_matrixC800[3, 2] = transformation_matrixC800[3, 2] + oz

    #CYCLE800 закончен
    if any(G549):  # G549 = [500.0, 0.0, 400.0, 20.0, 45.0, 0.0]
        ox, oy, oz = G549[0:3]
        ax, ay, az = G549[3:]
        ax = math.radians(ax)
        ay = math.radians(ay)
        az = math.radians(az)
        trans_matr_sum = matrixis_return(ox, oy, oz, ax, ay, az)
    else:
        trans_matr_sum = np.eye(4)
    trans_matr_sum = transformation_matrixC800.dot(trans_matr_sum)



    #two_matrixs_Ccenter = [None, None]
    #print(f'kinematics0 = {kinematics.}')
    #if trans_matr_sum is not None and kinematics is not None:
    #    two_matrixs_Ccenter[0] = np.zeros((4, 4), float)
    #    two_matrixs_Ccenter[1] = np.zeros((4, 4), float)
    #    print(f'kinematics = {kinematics}')

    return trans_matr_sum#, two_matrixs_Ccenter


def matrixMorty(dots_transformation_matrix, machine):
    """
    :param dots_transformation_matrix: Это матрица переноса точек из виртуальной текущей СК в СК построений (G54 main)
    :param machine:
    :param table:
    :param head:
    :return:
    """
    print('matrixMorty_C')
    #transf_matrix,
    #print(f'transf_matrix = \n{transf_matrix}')
    print(f'machine = {machine}')
    ax_order = machine.ax_order #'CBA'
    XYZABC_ADD = machine.XYZABC_ADD
    for_45grad_angles = machine.for_45grad_angles
    animation_line_ax_order = machine.animation_line_ax_order
    collet = machine.collet
    print(f'Базовая ск в координатах {machine.g54_g59_AXIS[machine.current_g54_g59]}')

    #{'X': -1000.0, 'Y': 0.0, 'Z': 500.0, 'A': 0.0, 'B': 0, 'C': 0}
    M1 = dots_transformation_matrix # FIXME Перенос в базовую СК
    #trans_matrix_from_SC(G549, C800)
    #coords_line = [-machine.g54_g59_AXIS[machine.current_g54_g59][key] for key in 'XYZABC']
    #ox, oy, oz = G549[0:3]
    #ax, ay, az = G549[3:]
    #ax = math.radians(ax)
    #ay = math.radians(ay)
    #az = math.radians(az)
    #M1 = matrixis_return(ox, oy, oz, ax, ay, az)

    coords_line = [machine.g54_g59_AXIS[machine.current_g54_g59][key] for key in 'XYZABC']
    print(f'M2 coords = {coords_line}')
    coords_line[3:] = map(np.radians, coords_line[3:])
    print(f'M2 coords_02 = {coords_line}')
    M2 = matrixis_return(*coords_line)  # FIXME Добавляю сюда матрицу переноса координат из базовой G54 в Машинный Ноль
    #M2 = np.linalg.inv(M2)
    print('M2 = ', M2)
    #TODO Раньше я работал с 't_angle' вот так
    #euler_angles_rad = shoulder_dict['t_angle']
    #rotation = Rotation.from_euler('xyz', euler_angles_rad)
    #fff = rotation.apply(np.array([from_SC[0], from_SC[1], from_SC[2]])) где from_SC это координаты XYZ
    #Мда
    #_________________________________

    coords_line = XYZABC_ADD# FIXME Добавляю сюда матрицу переноса координат из Машинного Ноля в точку 1 [C]
    coords_line = [-x for x in coords_line]
    coords_line[3:] = map(np.radians, coords_line[3:])
    M3 = matrixis_return(*coords_line)  # TODO С минусом всё сейчас




    shoulder_dict = machine.DICT_AX_PARAMETERS[ax_order[1]] # FIXME Добавляю сюда матрицу переноса координат из точки 1 [C] в точку 2 [B]
    coords_line = [0., -shoulder_dict['LShoulder'], 0., *[- x for x in shoulder_dict['t_angle']]]
    M4 = matrixis_return(*coords_line)

    shoulder_dict = machine.DICT_AX_PARAMETERS[ax_order[2]] # FIXME Добавляю сюда матрицу переноса координат из точки 2 [B] в точку 3 [A]
    coords_line = [0., -shoulder_dict['LShoulder'], 0., *[- x for x in shoulder_dict['t_angle']]]
    M5 = matrixis_return(*coords_line)

    h = collet['h']  # FIXME Добавляю сюда матрицу переноса координат из точки 3 [A] в точку 5 [Кончик инструмента???]
    coords_line = [0., 0., h, -collet['angle'], 0., 0.]  # h = Y OR Z
    M6 = matrixis_return(*coords_line)


    # todo Подглядывая в order, нужно сформировать для каждой оси список матриц преобразования
    # todo Например, для C: [M1], 'B': [M1, M2] - где M2 - это матрица прехода от элемента 1 к элементу 2 и тд.
    #if

    matrixis4Morty = [M1, M2, M3,]  #  M4, M5, M6
    print(f'Motry to return: \n {matrixis4Morty}')
    return matrixis4Morty



def Morty_matrix_use(coords: np.ndarray, some_matrx: List[np.ndarray]):
    # [nan nan nan 0. 100. 0. 100. 0. 0. 1.57 nan nan nan nan nan 11. nan 600. 34.20 406.03]
    print(f'99 9 coords = {coords}')
    print(f'some_matrix = {some_matrx}')
    #todo переходим


    coords[17:] = coords[4:7]

    M1 = some_matrx[0]
    #M1 = np.linalg.inv(M1)

    #M1[0, 2] = 0
    M1[1, 1] = 0
    print('888885 M1 = ', M1)
    coords[17:] = coords[17:] + M1[:3, 3]
    coords[17:] = coords[17:].dot(M1[:3, :3])

    M2 = some_matrx[1] # Машинный ноль #FIXME Нет не фикси. Вроде верно.
    coords[17:] = coords[17:].dot(M2[:3, :3])
    coords[17:] = coords[17:] + M2[:3, 3]
    print(f'taak552 = {coords[17:]}')

    M3 = some_matrx[2]
    coords[17:] = coords[17:] + M3[:3, 3]
    coords[17:] = coords[17:].dot(M3[:3, :3])
    AAAA
    print(f'taak551 = {coords[17:]}')


    print(f'taak553 = {coords[17:]}')
    #coords[17:] = 600, 0, 600
    coords[17:] = turn_around_C(coords[17], coords[18], coords[19], coords[9])
    #todo переходим назад

    #TODO А это не надо, мы же в базовую переносим
    #invert_M1 = np.linalg.inv(M1[:3, :3])
    #coords[17:] = coords[17:].dot(invert_M1)
    #coords[17:] = coords[17:] + M1[:3, 3]


    invert_M3 = np.linalg.inv(M3[:3, :3])

    coords[17:] = coords[17:].dot(invert_M3)
    coords[17:] = coords[17:] - M3[:3, 3]


    invert_M2 = np.linalg.inv(M2[:3, :3])  #FIXME Нет не фикси. Вроде верно.
    coords[17:] = coords[17:] - M2[:3, 3]
    coords[17:] = coords[17:].dot(invert_M2)





def G549_4_many_dots_NEW(dots: np.ndarray, trans_matx):
    print(f'trans_matx_4_many_dots = {trans_matx}')
    # Данные по факту предобработаны
    print(f'here trans_matx = {trans_matx}')
    print(trans_matx[3,0])
    print(trans_matx[3, 2])
    dots[:, 17:] = np.dot([dots[:, 17:]], trans_matx[:3, :3])  # + translation_vector
    dots[:, 17] = dots[:, 17] + trans_matx[3, 0]
    dots[:, 18] = dots[:, 18] + trans_matx[3, 1]
    dots[:, 19] = dots[:, 19] + trans_matx[3, 2]

def G549_4_1_dot(dot: np.ndarray, trans_matx):
    print(f'G549_4_1_dot')
    dot[17:20] = np.dot([dot[4:7]], trans_matx[:3, :3])  # + translation_vector
    dot[17] = dot[17] + trans_matx[0, 3]
    dot[18] = dot[18] + trans_matx[1, 3]
    dot[19] = dot[19] + trans_matx[2, 3]



# Матрица масштабирования
# matrix_scale = np.array([
#    [x_scale, 0, 0, 0],
#    [0, y_scale, 0, 0],
#    [0, 0, z_scale, 0],
#    [0, 0, 0, 1]
# ])