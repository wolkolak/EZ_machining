import math, copy
from mathematic.geometry import find_center, which_closer, move_the_dot_V_H, make_closer_to_center, lines_intersection_angles, angle_from_dot_2d
from mathematic.tragectory import Tragectory_3D_one_direction
from CNC_generator.usefull_funcs import center_from_tragectory, k_multiplayer, finish_groove_func




def new__top_dot_for_45(old_angle, new_angle, dotC, dot_main):#direction можно убрать
    print('new__top_dot_for_45')
    print('old_angle = {}, new_angle = {}, dotC = {}, dot_main = {}'.format(old_angle, new_angle, dotC, dot_main))
    #old_angle = math.radians(old_angle)
    #new_angle = math.radians(new_angle)
    delta_angle = (new_angle - old_angle) / 2
    print('delta_angle = ', delta_angle)
    result_angle = angle_from_dot_2d(dot_main, dotC)
    print('result_angle = ', result_angle)
    result_angle = result_angle + delta_angle #* direction
    print('dotC = {}, 0 = {}, dot_main = {}, result_angle = {}'.format(dotC, 0, dot_main, result_angle))
    intersection = lines_intersection_angles(dotC, 0, dot_main, result_angle)
    print('intersection = ', intersection)
    return intersection




def make_geometry_from_tragectory(new_45_tragectory, param, tool45):
    # geometry_45 = copy.copy(new_45_tragectory)
    # geometry_45 = new
    tool_allow = param['Thick'] + tool45['tool_R']
    print('tool_allow = ', tool_allow)
    print('param = ', param)
    print("param['TopFRr'][1] = ", param['TopFRr'][1])
    R_r_top45 = param['TopFRr'][1] + tool_allow if param['TopFRr'][0] != '-' else tool_allow   # param['TopFRr'][1] is not None or
    R_l_top45 = param['TopFRl'][1] + tool_allow if param['TopFRl'][0] != '-' else tool_allow   # param['TopFRl'][1] is not None or
    R_r_bot45 = param['BotFRr'][1] - tool_allow if param['BotFRr'][0] != '-' else tool_allow   # param['BotFRr'][1] is not None or
    R_l_bot45 = param['BotFRl'][1] - tool_allow if param['BotFRl'][0] != '-' else tool_allow   # param['BotFRl'][1] is not None or
    print(R_r_top45)
    print(R_l_top45)
    print(R_r_bot45)
    print(R_l_bot45)
    print('new_45_tragectory in make_geometry', new_45_tragectory)
    #param  =  {'TopFRr': ['R', 30.0], 'TopFRl': ['R', 30.0], 'BotFRr': ['R', 20.0], 'BotFRl': ['R', 20.0], 'Xa': 0.0, 'Za': 0.0, 'accurate': True, 'Thick': 0, 'corrector': False}

    top_r = [[new_45_tragectory[0][0][0], new_45_tragectory[0][0][1]],
             [new_45_tragectory[0][1][0], new_45_tragectory[0][1][1]],
             [new_45_tragectory[0][2][0], new_45_tragectory[0][2][1]]]
    top_l = [[new_45_tragectory[3][0][0], new_45_tragectory[3][0][1]],
             [new_45_tragectory[3][1][0], new_45_tragectory[3][1][1]],
             [new_45_tragectory[3][2][0], new_45_tragectory[3][2][1]]]
    bot_r = [[new_45_tragectory[1][0][0], new_45_tragectory[1][0][1]], [new_45_tragectory[1][1][0], new_45_tragectory[1][1][1]], [new_45_tragectory[1][2][0], new_45_tragectory[1][2][1]]]
    bot_l = [[new_45_tragectory[2][0][0], new_45_tragectory[2][0][1]], [new_45_tragectory[2][1][0], new_45_tragectory[2][1][1]], [new_45_tragectory[2][2][0], new_45_tragectory[2][2][1]]]
    #zdes dumaem
    print('___|___')
    print('top_r = ', top_r)# работает для скругления/фаски/угла
    print('bot_r = ', bot_r)
    print('top_l = ', top_l)
    print('bot_l = ', bot_l)
    if param['TopFRr'][0] == 'R':
        C_Rtop = center_from_tragectory(top_r, R_r_top45)
        top_r_new = make_closer_to_center(top_r, C_Rtop, R_r_top45, tool_allow)
    #elif param['TopFRr'][0] == 'Chamfer':
    else:
        top_r_new1 = move_the_dot_V_H(top_r[1], -45, tool_allow)
        top_r_new2 = move_the_dot_V_H(top_r[2], -45, tool_allow)
        top_r_new0 = lines_intersection_angles(top_r_new1, 180, top_r_new2, 45)
        top_r_new = [top_r_new0, top_r_new1, top_r_new2]
        print('особое top_r_new = ', top_r_new)
    if param['TopFRl'][0] == 'R':
        C_Ltop = center_from_tragectory(top_l, R_l_top45)
        top_l_new = make_closer_to_center(top_l, C_Ltop, R_l_top45, tool_allow)
    else:
        top_l_new1 = move_the_dot_V_H(top_l[1], -135, tool_allow)
        top_l_new2 = move_the_dot_V_H(top_l[2], -135, tool_allow)
        top_l_new0 = lines_intersection_angles(top_l_new1, 180, top_l_new2, 135)
        top_l_new = [top_l_new0, top_l_new1, top_l_new2]
        print('особое top_l_new = ', top_l_new)

    if param['BotFRr'][0] == 'R':
        if bot_r[1][0] > bot_r[2][0]:
            print('lolo1')
            print('bot_r = {}, R_r_bot45 = {}'.format(bot_r, R_r_bot45))
            C_Rbot = center_from_tragectory(bot_r, R_r_bot45)
            print('C_Rbot = ', C_Rbot)
            bot_r_new = make_closer_to_center(bot_r, C_Rbot, R_r_bot45, -tool_allow)
        else:
            print('lolo2')
            bot_r_new1 = move_the_dot_V_H(bot_r[1], -45, tool_allow)  # верхняя точка работает.
            bot_r_new2 = move_the_dot_V_H(bot_r[2], -90, tool_allow)
            bot_r_new0 = lines_intersection_angles(bot_r_new1, 225, bot_r_new2, 0)
            bot_r_new = [bot_r_new0, bot_r_new1, bot_r_new2]
    else:
        print('lolo3')
        bot_r_new1 = move_the_dot_V_H(bot_r[1], -45, tool_allow)#верхняя точка работает.
        bot_r_new2 = move_the_dot_V_H(bot_r[2], -90, tool_allow)
        bot_r_new0 = lines_intersection_angles(bot_r_new1, 180, bot_r_new2, 45)
        bot_r_new = [bot_r_new0, bot_r_new1, bot_r_new2]
    print('особое bot_r_new = ', bot_r_new)

    if param['BotFRl'][0] == 'R':
        if bot_l[1][0] > bot_l[2][0]:
            C_Lbot = center_from_tragectory(bot_l, R_l_bot45)
            bot_l_new = make_closer_to_center(bot_l, C_Lbot, R_l_bot45, -tool_allow)
        else:
            bot_l_new1 = move_the_dot_V_H(bot_l[1], -135, tool_allow)  # верхняя точка работает.
            bot_l_new2 = move_the_dot_V_H(bot_l[2], -90, tool_allow)
            bot_l_new0 = lines_intersection_angles(bot_l_new1, 180, bot_l_new2, 135)
            bot_l_new = [bot_l_new0, bot_l_new1, bot_l_new2]
    else:
        bot_l_new1 = move_the_dot_V_H(bot_l[1], -135, tool_allow)#верхняя точка работает.
        bot_l_new2 = move_the_dot_V_H(bot_l[2], -90, tool_allow)
        bot_l_new0 = lines_intersection_angles(bot_l_new1, 0, bot_l_new2, -45)
        bot_l_new = [bot_l_new0, bot_l_new1, bot_l_new2]
    print('особое bot_l_new = ', bot_l_new)
    new_tr = [top_r_new, bot_r_new, bot_l_new, top_l_new]
    print('new_geometry_45_AAAA = ', new_tr)
    #выше не верно
    return new_tr

def Make_tragectory_for45(geometry, tragectory45, tragectory_2, tool2, tool45, param):
    print('Make_tragectory_for45')

    for i in range(len(geometry)):
        geometry[i] = k_multiplayer(geometry[i], 0, 0.5)
    print('geometry: ', geometry)
    for i in range(len(tragectory45)):
        tragectory45[i] = k_multiplayer(tragectory45[i], 0, 0.5)
    t45_copy = copy.deepcopy(tragectory45)
    print('tragectory45: ', tragectory45)
    for i in range(len(tragectory_2)):
        tragectory_2[i] = k_multiplayer(tragectory_2[i], 0, 0.5)
    print('tragectory_2 = ', tragectory_2)

    angl_good_r = True if tragectory45[0][0][0] - tragectory45[1][0][0] > tragectory45[0][0][1] - tragectory45[1][0][1] else False # for 45 degrees.
    RrBot = abs(param['BotFRr'][1] - (param['Thick'] + tool45['tool_R'])) if param['BotFRr'][1] != 0 else 0
    angl_good_l = True if tragectory45[3][0][0] - tragectory45[2][0][0] > tragectory45[2][0][1] - tragectory45[3][0][1] else False
    RlTop = abs(param['TopFRl'][1] + (param['Thick'] + tool45['tool_R'])) if param['TopFRl'][1] != 0 else 0
    RlBot = abs(param['BotFRl'][1] - (param['Thick'] + tool45['tool_R'])) if param['BotFRl'][1] != 0 else 0

    if param['TopFRr'][0] == 'R':#Ищу нижнюю точку верхней части
        TopR = t45_copy[0][1]
        if angl_good_r:
            R_r_top45 = param['TopFRr'][1] + param['Thick'] + tool45['tool_R']
            C_R1top, C_R2top = find_center([tragectory45[0][1][0], tragectory45[0][1][1]],
                                           [tragectory45[0][2][0], tragectory45[0][2][1]], R_r_top45)
            C_Rtop = C_R1top if C_R1top[0] < C_R2top[0] else C_R2top
            delta = R_r_top45 / math.sqrt(2)
            # новая точка пересечения
            Rdot = [C_Rtop[0] + delta, C_Rtop[1] - delta]  # точка посчитанная под 45 градусов на окружности R+r_45.
        else:
            Rdot = tragectory45[0][2]
    elif param['TopFRr'][0] == 'Chamfer':
        print('chamfer tragectory45 = ', tragectory45)
        Rdot = tragectory45[0][2]
        TopR = t45_copy[0][1]
        print('Rdot = {}, TopR = {}'.format(Rdot, TopR))
        if TopR[1] <= t45_copy[0][0][1]:#обратное для L
            print('угол стенки слишком большой для 45градусной фаски')
            return None, None
        #Rdot = TopR
    else:   # Угол
        #Rdot = tragectory45[0][0] #Точка центра от 50 градусов.
        #sdfsdf
        #TopR = Rdot
        old_angle = angle_from_dot_2d(geometry[1][0], geometry[0][0]) - 180
        intersection = new__top_dot_for_45(old_angle=old_angle, new_angle=45, dotC=t45_copy[0][0], dot_main=geometry[0][0])
        print('here intersecton = ', intersection)
        Rdot = intersection
        TopR = Rdot
        interrsec_r = Rdot
        print('4||| Rdot Top = ', Rdot)
    #tragectory45[0][2] = Rdot

    delta_rbot = Rdot[0] - geometry[1][0][0]#tragectory45[1][0][0]  # todo не работает без скруглений. теперь должно
    #old_angle = angle_from_dot_2d(geometry[1][0], geometry[0][0]) - 180
    #intersection = new__top_dot_for_45(old_angle=old_angle, new_angle=45, dotC=t45_copy[0][0], dot_main=geometry[0][0])
    Rdot_bot = [geometry[1][0][0], Rdot[1] - delta_rbot] #crossing the bottom line of the groove
    print('TopR =|= ', TopR)
    Z_r = t45_copy[1][2][1] - 100 if t45_copy[1][2][1] is not None else None

    #                   X                       Y       Z                       R           Direction
    r_list_small = [[t45_copy[1][1][0],     None,     t45_copy[1][1][1],        None,       None],
                    [t45_copy[1][2][0],     None,     t45_copy[1][2][1],        RrBot,      'G2'],
                    [t45_copy[1][2][0],     None,     Z_r,    None,       None]
                    ]

    if r_list_small[0][0] is None:
        r_list_small[0][0] = t45_copy[1][0][0];  r_list_small[0][2] = t45_copy[1][0][1]
        r_list_small[1][0] = t45_copy[1][0][0];  r_list_small[1][2] = t45_copy[1][0][1]
        r_list_small[2][0] = t45_copy[1][0][0];  r_list_small[2][2] = r_list_small[1][2] - 100# ,буду заменять на l_list_small[1][2]
    print('r_list_small  полуфабрикат = ', r_list_small)

    if param['TopFRl'][0] == 'R':
        TopL = t45_copy[3][1]
        if angl_good_l:
            R_l_top45 = param['TopFRl'][1] + param['Thick'] + tool45['tool_R']
            C_L1top, C_L2top = find_center([tragectory45[3][1][0], tragectory45[3][1][1]], [tragectory45[3][2][0], tragectory45[3][2][1]], R_l_top45)
            C_Ltop = C_L1top if C_L1top[0] < C_L2top[0] else C_L2top
            delta = R_l_top45 / math.sqrt(2)
            Ldot = [C_Ltop[0] + delta, C_Ltop[1] + delta]
        else:
            Ldot = tragectory45[3][2]
    elif param['TopFRl'][0] == 'Chamfer':
        Ldot = tragectory45[3][2]
        TopL = t45_copy[3][1]
        if TopL[1] >= t45_copy[3][0][1]:  # обратное для R
            return None, None
    else:
        #Ldot = tragectory45[3][0] #Точка центра от 50 градусов.
        old_angle = angle_from_dot_2d(geometry[3][0], geometry[2][0]) - 180
        print('old_angle 333 = ', old_angle)
        intersection = new__top_dot_for_45(old_angle=old_angle, new_angle=135, dotC=t45_copy[3][0], dot_main=geometry[3][0])
        Ldot = intersection
        TopL = Ldot
    #tragectory45[3][2] = Ldot
    #Попадаем в дно
    delta_lbot = Ldot[0] - geometry[2][0][0]#tragectory45[2][0][0]
    Ldot_bot = [geometry[2][0][0], Ldot[1] + delta_lbot]

    Z_l = t45_copy[2][2][1] + 100 if t45_copy[2][2][1] is not None else None
    #                   X                       Y       Z                       R           Direction
    l_list_small = [[t45_copy[2][1][0],     None,     t45_copy[2][1][1],        None,       None],
                    [t45_copy[2][2][0],     None,     t45_copy[2][2][1],        RlBot,      'G3'],
                    [t45_copy[2][2][0],     None,     Z_l,                      None,       None]
                    ]
    if l_list_small[0][0] is None:
        l_list_small[0][0] = t45_copy[2][0][0];  l_list_small[0][2] = t45_copy[2][0][1]
        l_list_small[1][0] = t45_copy[2][0][0];  l_list_small[1][2] = t45_copy[2][0][1]
        l_list_small[2][0] = t45_copy[2][0][0];  l_list_small[2][2] = l_list_small[1][2] + 100

    print('предварительный  r_list_small = ', r_list_small)
    print('предварительный  l_list_small = ', l_list_small)    # верх центр под 45 градусов
    track_r_new1 = Tragectory_3D_one_direction(r_list_small, 'G18')
    intersection1, intersection2 = track_r_new1.line_cross_tragectory_([Rdot[0], None, Rdot[1]],
                                                                       [Rdot_bot[0], None, Rdot_bot[1]],
                                                                       plane='G18')
    intersection_r = intersection1 if intersection1 is not None else intersection2
    dot_cross_r = Rdot_bot if intersection_r is None else intersection_r

    track_l_new1 = Tragectory_3D_one_direction(l_list_small, 'G18')
    intersection1, intersection2 = track_l_new1.line_cross_tragectory_([Ldot[0], None, Ldot[1]],
                                                                       [Ldot_bot[0], None, Ldot_bot[1]],
                                                                       plane='G18')
    intersection_l = intersection1 if intersection1 is not None else intersection2
    dot_cross_l = Ldot_bot if intersection_l is None else intersection_l
    dot_cross_r[0] = round(dot_cross_r[0], 10); dot_cross_r[1] = round(dot_cross_r[1], 10)
    dot_cross_l[0] = round(dot_cross_l[0], 10); dot_cross_l[1] = round(dot_cross_l[1], 10)

    print('Пересечение')
    print('dot_cross_r = ', dot_cross_r)
    print('dot_cross_l = ', dot_cross_l)

    #здесь
    #собираю tragectory Заново.
    print('|//222| tragectory45 = ', tragectory45)
    #tragectory_for_tool45 = copy.deepcopy(tragectory45)

    nya = TopR if TopR[0] == Rdot[0] and TopR[1] == Rdot[1] else lines_intersection_angles(Rdot, 45, TopR, 0)
    tragectory45_0 = [nya, TopR, Rdot]#tragectory45[0][0]
    nya = dot_cross_r if tragectory45[1][2][0] is None or dot_cross_r[0] <= tragectory45[1][2][0] else tragectory45[1][2]
    tragectory45_1 = [tragectory45[1][0], dot_cross_r, nya]
    nya = dot_cross_l if tragectory45[2][2][0] is None or dot_cross_l[0] <= tragectory45[2][2][0] else tragectory45[2][2]
    tragectory45_2 = [tragectory45[2][0], dot_cross_l, nya]
    nya = TopL if TopL[0] == Ldot[0] and TopL[1] == Ldot[1] else lines_intersection_angles(Ldot, 135, TopL, 180)
    tragectory45_3 = [nya, TopL, Ldot]
    tragectory_for_tool45 = [tragectory45_0, tragectory45_1, tragectory45_2, tragectory45_3]
    print('tragectory_for_tool45 = ', tragectory_for_tool45)#верх работает безупречно

    print('Rdot = ', Rdot)
    #tragectory45[0][2] = Rdot#todo ЗДЕСЬ был 0
    #if tragectory45[0][1][0] is None:
    #    tragectory45[0][1] = copy.deepcopy(Rdot)
    #tragectory45[3][2] = Ldot
    #if tragectory45[3][1][0] is None:
    #    tragectory45[3][1] = copy.deepcopy(Ldot)
#
    #print('|//| tragectory45 = ', tragectory45)
    #tragectory45[1][1] = dot_cross_r
    #if tragectory45[1][2][0] is None or dot_cross_r[0] <= tragectory45[1][2][0]:
    #    print('Boom1')
    #    tragectory45[1][2] = dot_cross_r
    #tragectory45[2][1] = dot_cross_l
    #if tragectory45[2][2][0] is None or dot_cross_l[0] <= tragectory45[2][2][0]:
    #    print('Boom2')
    #    tragectory45[2][2] = dot_cross_l
    #print('2222 new_45_tragectory === ', tragectory45)#not for angle
    #приводим траекторию в геометрию
    geometry_45 = make_geometry_from_tragectory(tragectory_for_tool45, param, tool45)#tragectory45
    print('|geometry_45| = ', geometry_45)
    #приводим обычную геометрию в траекторию второго инструмента
    for i in range(len(geometry_45)):
        geometry_45[i] = k_multiplayer(geometry_45[i], 0, 2)
    new_rough_trajectory = finish_groove_func(geometry=geometry_45, allowanceX=param['Xa'],     #allowanceX починить
                                              allowanceZ=param['Za'], allowanceThickness=tool2['tool_R'] + param['Thick'],
                                              top_r_value=param['TopFRr'][1], top_l_value=param['TopFRl'][1],
                                              bot_r_value=5000, bot_l_value=5000, top_type_r=param['TopFRr'][0],#5000, 5000
                                              top_type_l=param['TopFRl'][0], bot_type_r='R', bot_type_l='R')
    for i in range(len(geometry_45)):
        geometry_45[i] = k_multiplayer(geometry_45[i], 0, 0.5)
    for i in range(len(new_rough_trajectory)):
        new_rough_trajectory[i] = k_multiplayer(new_rough_trajectory[i], 0, 0.5)
    print('||| new_rough_trajectory = ', new_rough_trajectory)
    return tragectory_for_tool45, new_rough_trajectory # = tragectory_prev_limit