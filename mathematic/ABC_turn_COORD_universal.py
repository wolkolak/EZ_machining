import math
import numpy as np

def turn_around_radians1(h, v, angle):
    h_new = h * math.cos(angle) - v * math.sin(angle)
    v_new = h * math.sin(angle) + v * math.cos(angle)
    return h_new, v_new#, p, five

def turn_around_radians2(h, v, angle):
    h_new = h * math.cos(angle) - v * math.sin(angle)
    v_new = h * math.sin(angle) + v * math.cos(angle)
    return h_new, v_new, math.degrees(angle)#, p, five

def turn_around_AX(x, y, z, alpha_AX):
    alpha = math.radians(alpha_AX)
    x_new = x * math.cos(alpha) - y * math.sin(alpha)
    y_new = x * math.sin(alpha) + y * math.cos(alpha)
    return x_new, y_new, z






def table_c_turn():
    print('table_c_turn')

def table_b_turn():
    print('table_b_turn')

def table_a_turn():
    print('table_a_turn')

def head_c_turn():
    print('head_c_turn')

def head_b_turn():
    print('head_b_turn')

def head_a_turn():
    print('head_a_turn')




def turn_coord_universal_build_f(table, head, g549, ax_order):#, DICT_AX_PARAMETERS
    #Будем исходить, что именно ближе к детали может быть любая вращательная ось
    #DICT_AX_PARAMETERS = {      'A': {'Place': 'Head', 'LShoulder': 100, 'angle': 0.},  # 0 OR 45 percents
    #                            'B': {'Place': 'Head', 'LShoulder': 101, 'angle': 0.},
    #                            'C': {'Place': 'Head', 'LShoulder': 102, 'angle': 0.}}
    ax_order = 'CBA'
    table = [[None, None], [None, None], [102, 0.0]]
    head = [[60, 0.0], [501, 0.0], [None, None]]
    g549 = {'X': 0, 'Y': 0.0, 'Z': 800.0, 'A': 0.0, 'B': 0.0, 'C': 0.0}

    if table[2][0] is None:
        table_c = False
    else:
        table_c = True
    if table[1][0] is None:
        table_b = False
    else:
        table_b = True
    if table[0][0] is None:
        table_a = False
    else:
        table_a = True

    if table_a:
        turn_a = table_a_turn
    else:
        turn_a = head_a_turn
    if table_b:
        turn_b = table_b_turn
    else:
        turn_b = head_b_turn
    if table_c:
        turn_c = table_c_turn
    else:
        turn_c = head_c_turn

    turn_list = []
    for let in ax_order:
        if let == 'A':
            func = turn_a
        elif let == 'B':
            func = turn_b
        else:
            func = turn_c
        turn_list.append(func)
    #понять когда достаточно переносов без других сложных операций. может всегда?
    #вариант со столами
    #перенос координат в центр стола
    #поворот первой оси если надо.
    #перенос нас плечо 2 элемента к точке крепления
    #поворот если надо
    #перенос к точке крепления 3 элемента
    #поворот 3 го элемента


    #для включенного режима следования точка не меняет своего положения. Меняют своё положения элементы станка, причём в обратном порядке
    #или в том же, просто перенести потом. Мб так лучше ибо есть зацеп за кончик инструмента а есть за его центр
    #какая роль у нуля станка??? Вообще, наша цель - перемещение к точке вращения первого элемента. Но G549 указана относительно нуля станка.
    #Нуль станка сам по себе не двигается. Вращаться вокруг нуля станка - точно не нужно. Как до него смещаться если G549 повернута?
    #Если сначала происходят повороты, то строясь от детали мы будем сначала смещаться, потом поворачиваться.

    #[400.0, 0.0, 500.0, 0.0, 0.0, 0.0]
    func1 = turn_close_part_ax


