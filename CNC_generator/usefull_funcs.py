import math, copy
from mathematic.geometry import find_center, which_closer
from mathematic.arithmetic import max_None, min_None
from mathematic.turn_helpers import takeZl_Zr_from_groove1, takeXl_from_groove1, takeXR_from_groove1

def lines_intersection_dots(x1, z1, x2, z2, x3, z3, x4, z4):
    print('lines_intersection_dots')
    t2_up = (x3 - x1) * (z2 - z1) - (x2 - x1) * (z3 - z1)
    t2_bot = (x2 - x1) * (z4 - z3) - (x4 - x3) * (z2 - z1)
    t2 = t2_up / t2_bot
    x = x3 + (x4 - x3) * t2
    z = z3 + (z4 - z3) * t2
    return x, z

def transfer(direction, l, x1, z1, x2, z2):
    #direction = 'left'
    #l=5
    #x1=30
    #x2=10
    #z1=43.753
    #z2=15.19
    print('in transfer: direction = ', direction)
    print('x1 = {}, z1 = {}, x2 = {}, z2 = {}'.format(x1, z1, x2, z2))

    d_x = x2 - x1
    d_z = z2 - z1
    print('d_x = {}, d_z = {}'.format(d_x, d_z))
    k = d_x/d_z
    first = math.sqrt(l * l / (k * k + 1))
    second = k * first
    if direction == 'left':
        second = - second
    else:
        first = - first

    if d_x <= 0:
        first = - first
    if d_z <= 0:
        second = - second
    print('first = {}, second = {}'.format(first, second))
    print('in func x1 = {}, z1={}, x2={}, z2 = {}'.format(x1+first, z1+second, x2+first, z2+second))
    return x1+first, z1+second, x2+first, z2+second

def move_ax_along(result, index, add):
    #result = [[x1, z1], [x2, z2]]
    for r in result:
        if r[index] is not None:
            r[index] = r[index] + add
    return result

def k_multiplayer(result, index, k):
    # result = [[x1, z1], [x2, z2], [x3, z3]]
    for r in range(len(result)):
        if result[r][index] is not None:
            result[r][index] = result[r][index] * k
    return result


def DrawGrooveGcode45Rough(r_, l_, param, tool, DCurr):
    print('DrawGrooveGcode45Rough')
    #
    r_ = move_ax_along(r_, 0, -tool['tool_R'] * 2)
    l_ = move_ax_along(l_, 0, -tool['tool_R'] * 2)
    DCurr = DCurr - tool['tool_R'] * 2
    print('r_ = ', r_)
    print('l_ = ', l_)
    print('DCurr = ', DCurr)
    T_step = tool['rX step'] * 2
    Dmax = max_None(r_[0][0], l_[0][0])
    Radd = tool['tool_R'] + param['Thick']
    Gcode = ''
    G2_G3_normal = True
    if G2_G3_normal:
        clock = 'G2'
        reverseclock = 'G3'
    else:
        clock = 'G3'
        reverseclock = 'G2'
    Add_part = 2
    nya = True
    new_startX, new_startZ, new_endZ = r_[0][0], r_[0][1], l_[0][1]

    while DCurr - T_step > r_[3][0] or nya:
        DCurr = DCurr - T_step
        if DCurr <= r_[3][0]:
            DCurr = r_[3][0]; nya = False
        Zl, Zr = takeZl_Zr_from_groove1(DCurr=DCurr, l_1=l_, r_1=r_, param=param, tool=tool, Radd=Radd)
        Add_part_str_r = 'G0 Z{}\r\nX{}\r\nG1X{}\r\n'.format(round(new_startZ, 3), round(new_startX + Add_part, 3), round(new_startX, 3))
        Gcode = Gcode + ';RIGHT SIDE45\r\n'
        Gcode = Gcode + Add_part_str_r
        if new_startX > r_[1][0]:#
            if DCurr <= r_[1][0]:
                if r_[0][0] != r_[1][0]:
                    if param['TopFRr'][0] == 'R':#                                         zdes
                        Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, round(r_[1][0], 3), round(r_[1][1], 3), round(param['TopFRr'][1]+Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(r_[1][0], 3), round(r_[1][1], 3))
            else:
                if r_[0][0] != r_[1][0]:
                    if param['TopFRr'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(reverseclock, round(DCurr, 3), round(Zr, 3), round(param['TopFRr'][1]+Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(DCurr, 3), round(Zr, 3))
        if new_startX > r_[2][0] and DCurr < r_[1][0]:
            if DCurr <= r_[2][0]:
                Gcode = Gcode + 'X{} Z{}\r\n'.format(round(r_[2][0], 3), round(r_[2][1], 3))
            else:
                Gcode = Gcode + 'X{} Z{}\r\n'.format(round(DCurr, 3), round(Zr, 3)) #if Bottom_r is False else Gcode

        if DCurr < r_[2][0]:#r_[3][0]: #вот с таким строками проблемы
            if DCurr == r_[3][0]:
                if r_[2][0] != r_[3][0]:
                    if param['BotFRr'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(clock, round(r_[3][0], 3), round(r_[3][1], 3), round(param['BotFRr'][1]-Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(r_[3][0], 3), round(r_[3][1], 3))
            else:
                if r_[2][0] != r_[3][0]:
                    if param['BotFRr'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(clock, round(DCurr, 3), round(Zr, 3),  round(param['BotFRr'][1] - Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(r_[3][0], 3), round(r_[3][1], 3)) #if Bottom_r is False else Gcode
        Gcode = Gcode + ';LEFT SIDE45\r\n'
        Gcode = Gcode + 'G1 Z{}\r\n'.format(round(Zl, 3))
        if DCurr <= l_[2][0]:
            if new_startX > l_[2][0]:# + T_step:
                if l_[2][0] != l_[3][0]:
                    if param['BotFRl'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(clock, round(l_[2][0], 3), round(l_[2][1], 3), round(param['BotFRl'][1]-Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(l_[2][0]), round(l_[2][1]))
            else:
                if l_[2][0] != l_[3][0]:
                    if param['BotFRl'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(clock, round(new_startX, 3), round(new_endZ, 3), round(param['BotFRl'][1] - Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(new_startX, 3), round(new_endZ, 3))

        if new_startX > l_[2][0] and DCurr < l_[1][0]:# + T_step:
            if DCurr <= l_[1][0]:
                if new_startX >= l_[1][0]: #+ T_step:
                    Gcode = Gcode + 'X{} Z{}\r\n'.format(round(l_[1][0], 3), round(l_[1][1], 3)) #if DCurr <= l_[1][0]
                else:
                    Gcode =  Gcode + 'X{} Z{}\r\n'.format(round(new_startX, 3), round(new_endZ, 3))
        if new_startX > l_[1][0]:# + T_step:
            if DCurr == l_[0][0]:
                if l_[0][0] != l_[1][0]:
                    if param['TopFRl'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, round(l_[0][0], 3), round(l_[0][1], 3), round(param['TopFRl'][1]+Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(l_[0][0], 3), round(l_[0][1], 3))
            else:
                if l_[0][0] != l_[1][0]:
                    if param['TopFRl'][0] == 'R':
                        Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, round(new_startX, 3), round(new_endZ, 3), round(param['TopFRl'][1] + Radd, 3))
                    else:
                        Gcode = Gcode + 'X{} Z{}\r\n'.format(round(new_startX, 3), round(new_endZ, 3))

        Gcode = Gcode + 'X{}\r\n'.format(round(new_startX + Add_part, 3))
        new_startX = DCurr
        new_startZ = Zr
        new_endZ = Zl
    Gcode = Gcode + 'G0 X{}\r\n'.format(round(Dmax + Add_part, 3))
    return Gcode




def DrawGrooveGcodeFinish(tool:dict, trajectory_dots:list, param, _45 = False):
    print('DrawGrooveGcodeFinish trajectory_dots = ', trajectory_dots)
    if _45:
        print('555 DrawGrooveGcodeFinish trajectory_dots = ', trajectory_dots)
    #tool = {type:R/A; B:10; angle:35; tool_R: 5; bind_place: 'bind1/2/3/4/5'}
    #trajectory_dots = [[   [rX, rZ],           [r1X, r1Z],         [r2X, r2Z]],
    #                    [[r_B_X, r_B_Z],   [r_B_1X, r_B_1Z],   [r_B_2X, r_B_2Z]]
    #                    [[l_B_X, l_B_Z],   [l_B_1X, l_B_1Z],   [l_B_2X, l_B_2Z]]
    #                    [  [lX, lZ],           [l1X, l1Z],         [l2X, l2Z]]
    #param = {'TopFRr': ['R', 5],'TopFRl': ['R', 5],'BotFRr': ['R', 5],'BotFRl': ['R', 5], Xa: 0.5, Za: 0.5, corrector=False, 'rXstock': 1.}

    Angle_r = math.degrees(math.atan((trajectory_dots[0][0][1] - trajectory_dots[1][0][1]) / (trajectory_dots[0][0][0] - trajectory_dots[1][0][0]) * 2))
    Angle_l = math.degrees(math.atan((trajectory_dots[3][0][1] - trajectory_dots[2][0][1]) / (trajectory_dots[2][0][0] - trajectory_dots[3][0][0]) * 2))
    Gcode_groove_param = ';Groove_D = {}, Zleft = {}, Groove_d = {}, B_Groove = {}, Angle_r = {}, Angle_l = {}\r\n'.\
    format(round(trajectory_dots[0][0][0] - tool['tool_R']*2, 3), round(trajectory_dots[3][0][1], 3), round(trajectory_dots[1][0][0], 3),
           round(trajectory_dots[1][0][1]-trajectory_dots[2][0][1], 3), round(Angle_r, 2), round(Angle_l, 2))
    Gcode_groove_param = Gcode_groove_param + ';Allowance: rX = {}, Z = {}, Thickness = {}\r\n'.format(param['Xa'], param['Za'], param['Thick'])
    Gcode_groove_param = Gcode_groove_param + ';Tool = {}, ToolR = {}, Bind place = {}, Corrector = {}\r\n'.format(tool['type'], tool['tool_R'], tool['bind_place'], param['corrector'])
    #B
    if tool['type'] == 'A':
        Gcode_groove_param = Gcode_groove_param + ';layer to cut = {}\r\n'.format(tool['rX step'])
    else:
        Gcode_groove_param = Gcode_groove_param + ';Tool B = {}\r\n'.format(tool['B'])
        if tool['type'] == 'B' and param['corrector']:
            Gcode_groove_param = Gcode_groove_param + ";Warning: CUTOff tool with Corrector. Tool can't be changed\r\n"
            Gcode_groove_param = Gcode_groove_param + ";But you can manipulate allowance by changing corrector R at will\r\n"
    if trajectory_dots[0][1][0] is None:                            #RIGHT TOP
        top_rX1 = trajectory_dots[0][0][0]; top_rZ1 = trajectory_dots[0][0][1]
        top_rX2 = trajectory_dots[0][0][0]; top_rZ2 = trajectory_dots[0][0][1]
    else:
        top_rX1 = trajectory_dots[0][1][0]; top_rZ1 = trajectory_dots[0][1][1]
        top_rX2 = trajectory_dots[0][2][0]; top_rZ2 = trajectory_dots[0][2][1]

    if trajectory_dots[1][1][0] is None:                            #RIGHT BOT
        bot_rX1 = trajectory_dots[1][0][0]; bot_rZ1 = trajectory_dots[1][0][1]
        bot_rX2 = trajectory_dots[1][0][0]; bot_rZ2 = trajectory_dots[1][0][1]
    else:
        bot_rX1 = trajectory_dots[1][1][0]; bot_rZ1 = trajectory_dots[1][1][1]
        bot_rX2 = trajectory_dots[1][2][0]; bot_rZ2 = trajectory_dots[1][2][1]

    if trajectory_dots[2][1][0] is None:                            #LEFT BOT
        bot_lX1 = trajectory_dots[2][0][0]; bot_lZ1 = trajectory_dots[2][0][1]
        bot_lX2 = trajectory_dots[2][0][0]; bot_lZ2 = trajectory_dots[2][0][1]
    else:
        bot_lX1 = trajectory_dots[2][1][0]; bot_lZ1 = trajectory_dots[2][1][1]
        bot_lX2 = trajectory_dots[2][2][0]; bot_lZ2 = trajectory_dots[2][2][1]

    if trajectory_dots[3][1][0] is None:                           #LEFT TOP
        top_lX1 = trajectory_dots[3][0][0]; top_lZ1 = trajectory_dots[3][0][1]
        top_lX2 = trajectory_dots[3][0][0]; top_lZ2 = trajectory_dots[3][0][1]
    else:
        top_lX1 = trajectory_dots[3][1][0]; top_lZ1 = trajectory_dots[3][1][1]
        top_lX2 = trajectory_dots[3][2][0]; top_lZ2 = trajectory_dots[3][2][1]

    XcenterbOT = bot_rX2
    Zcenter = (bot_rZ2 + bot_lZ2) / 2
    print('bot_rZ2 = {}, bot_lZ2 = {}'.format(bot_rZ2, bot_lZ2))
    print('Zcenter = ', Zcenter)
    r_side_track = []
    l_side_track = []
    if tool['type'] == 'A':
        r_side_track.append([XcenterbOT+tool['rX step']*2, Zcenter-tool['rX step']/math.tan(tool['angle'])])
        r_side_track.append([XcenterbOT, Zcenter])
        r_side_track.append([bot_rX2, bot_rZ2])
        r_side_track.append([bot_rX1, bot_rZ1])
        r_side_track.append([top_rX2, top_rZ2])
        r_side_track.append([top_rX1, top_rZ1])
        l_side_track.append([XcenterbOT+tool['rX step']*2, Zcenter+tool['rX step']/math.tan(tool['angle'])])
        l_side_track.append([XcenterbOT, Zcenter])
        l_side_track.append([bot_lX2, bot_lZ2])
        l_side_track.append([bot_lX1, bot_lZ1])
        l_side_track.append([top_lX2, top_lZ2])
        l_side_track.append([top_lX1, top_lZ1])
        if _45:
            print('this is r_side_track = ', r_side_track)
        if tool['bind_place'] == 1:
            for p in r_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] + tool['tool_R']
            for p in l_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] - tool['tool_R']
    else:
        r_side_track.append([top_rX1, top_rZ1])
        r_side_track.append([top_rX2, top_rZ2])
        r_side_track.append([bot_rX1, bot_rZ1])
        r_side_track.append([bot_rX2, bot_rZ2])

        l_side_track.append([top_lX1, top_lZ1])
        l_side_track.append([top_lX2, top_lZ2])
        l_side_track.append([bot_lX1, bot_lZ1])
        l_side_track.append([bot_lX2, bot_lZ2])

        if tool['bind_place'] == 1:
            for p in r_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] + tool['tool_R'] - tool['B']
            for p in l_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] - tool['tool_R']
        elif tool['bind_place'] == 2:
            for p in r_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] + tool['tool_R']
            for p in l_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
                p[1] = p[1] - tool['tool_R'] + tool['B']
        elif tool['bind_place'] == 3:
            for p in r_side_track:
                p[1] = p[1] + tool['tool_R'] * 2 - tool['B']
        elif tool['bind_place'] == 4:
            for p in l_side_track:
                p[1] = p[1] - tool['tool_R'] * 2 + tool['B']
        else:#5
            for p in r_side_track:
                p[0] = p[0] - tool['tool_R'] * 2
            for p in l_side_track:
                p[0] = p[0] - tool['tool_R'] * 2

    Radd = tool['tool_R'] + param['Thick']
    if tool['type'] == 'A':
        MinD = r_side_track[1][0]
        if tool['bind_place'] == 1:
            if r_side_track[5][1] - l_side_track[5][1] < 2 * tool['tool_R']:
                print('Инструмент не влез вообще')
                return 'Tool is too big', r_side_track, l_side_track
            l_side_track = l_side_track[-1::-1]
            r_side_track = r_side_track[-1::-1]
            if _45:
                print('||h|| r_side_track = ', r_side_track)
        else:
            if r_side_track[5][1] < l_side_track[5][1]:
                return 'Tool is too big', r_side_track, l_side_track
            l_side_track = l_side_track[-1::-1]
            r_side_track = r_side_track[-1::-1]
    else:#
        MinD = r_side_track[3][0]
        print('MinD = ', MinD)
        if r_side_track[0][1] < l_side_track[0][1]:
            print('Инструмент не влез вообще')
            return 'Tool is too big', r_side_track, l_side_track
    DCurr = MinD
    threshold1 = r_side_track[0][0]
    threshold2 = r_side_track[3][0]

    step = 20
    good = False
    s_tool = 0

    while step > 0 or good is False:
        save_D = DCurr#copy.copy(DCurr)
        print('DCurr = {}, l_side_track = {}, r_side_track = {}, param = {}, tool = {}, Radd = {}'.format(DCurr, l_side_track, r_side_track, param, tool, Radd))
        Z_l, Z_r = takeZl_Zr_from_groove1(DCurr, l_side_track, r_side_track, param, tool, Radd)
        print('l_side_track = {}, r_side_track = {}'.format(l_side_track, r_side_track))
        print('In while')
        print('threshold1 = {}, threshold2 = {}, DCurr = {}'.format(threshold1, threshold2, DCurr))
        print('Z_l = {}, Z_r = {}'.format(Z_l, Z_r))
        print('Z_l new = {}, Z_r = {}'.format(Z_l + s_tool, Z_r))
        #Z_l, Z_r = takeZl_Zr(DCurr, l_side_track, r_side_track, param, f_angles, Radd, Angle_r_tan, Angle_l_tan)
        if Z_l <= Z_r:  # влезло
            good = True
            threshold1 = DCurr
            if DCurr == MinD:
                print('BREACK MinD')
                break
        else:
            good = False
            threshold2 = DCurr
        DCurr = (threshold1 + threshold2) / 2
        step = step - 1

    DCurr = save_D
    if DCurr != r_side_track[0][0] and tool['type'] != 'A':
        if r_side_track[3][0] < DCurr:
            r_side_track[3][0] = DCurr; r_side_track[3][1] = Z_r
        if r_side_track[2][0] < DCurr:
            r_side_track[2][0] = DCurr; r_side_track[2][1] = Z_r
        if r_side_track[1][0] < DCurr:
            r_side_track[1][0] = DCurr; r_side_track[1][1] = Z_r

        if l_side_track[3][0] < DCurr:
            l_side_track[3][0] = DCurr; l_side_track[3][1] = Z_l
        if l_side_track[2][0] < DCurr:
            l_side_track[2][0] = DCurr; l_side_track[2][1] = Z_l
        if l_side_track[1][0] < DCurr:
            l_side_track[1][0] = DCurr; l_side_track[1][1] = Z_l

    l_side_track_round = l_side_track.copy()
    r_side_track_round = r_side_track.copy()
    for p in r_side_track:
        p[0] = round(p[0], 3)
        p[1] = round(p[1], 3)
    for p in l_side_track:
        p[0] = round(p[0], 3)
        p[1] = round(p[1], 3)
    if tool['type'] == 'A':
        print('here r_side_track_round = ', r_side_track_round)
        Gcode = DrawSharpCutter(r_side_track_round, l_side_track_round, param, tool)
    else:
        Gcode = DrawOffCutter(r_side_track_round, l_side_track_round, param, tool)
    result_str = Gcode_groove_param + Gcode
    return result_str, r_side_track, l_side_track


def DrawOffCutter(r_, l_, param, tool):
    # param = {'TopFRr': ['R', 5],'TopFRl': ['R', 5],'BotFRr': ['R', 5],'BotFRl': ['R', 5], Xa: 0.5, Za: 0.5, corrector=False, 'rXstock': 1., 'Thick': thick }
    # tool = {type:R/A; B:10; angle:35; tool_R: 5; bind_place: 'bind1/2/3/4/5'}
    Gcode = ''
    Add_part = 2
    Radd = tool['tool_R'] + param['Thick']
    if param['corrector'] is True:
        Add_part = 1 + Radd*2
        Radd = 0
        Add_part_str_r = 'G0 Z{}\r\nX{}\r\nG1 G42 X{}\r\n'.format(round(r_[0][1], 3), round(r_[0][0] + Add_part, 3), round(r_[0][0], 3))
        Add_part_str_l = 'G0 Z{}\r\nX{}\r\nG1 G41 X{}\r\n'.format(round(l_[0][1], 3), round(l_[0][0] + Add_part, 3), round(l_[0][0], 3))
        Add_part_str_r_end = 'G40 G0X{}\r\n'.format(round(l_[0][0] + Add_part, 3))
        Add_part_str_l_end = 'G40 G0X{}\r\n'.format(round(r_[0][0] + Add_part, 3))
    else:
        Add_part_str_r = 'G0 Z{}\r\nX{}\r\nG1X{}\r\n'.format(round(r_[0][1], 3), round(r_[0][0] + Add_part, 3), round(r_[0][0], 3))
        Add_part_str_l = 'G0 Z{}\r\nX{}\r\nG1X{}\r\n'.format(round(l_[0][1], 3), round(l_[0][0] + Add_part, 3), round(l_[0][0], 3))
        Add_part_str_r_end = 'G0 X{}\r\n'.format(round(l_[0][0] + Add_part, 3))
        Add_part_str_l_end = 'G0 X{}\r\n'.format(round(r_[0][0] + Add_part, 3))

    G2_G3_normal = True
    if G2_G3_normal:
       clock = 'G2'
       reverseclock = 'G3'
    else:
       clock = 'G3'
       reverseclock = 'G2'

    Gcode = Gcode + ';RIGHT SIDE\r\n'
    Gcode = Gcode + Add_part_str_r

    if r_[0][0] != r_[1][0]:
        if param['TopFRr'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, r_[1][0], r_[1][1], round(param['TopFRr'][1]+Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[1][0], r_[1][1])
    Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[2][0], r_[2][1])
    if r_[2][0] != r_[3][0]:
        if param['BotFRr'][0] == 'R':
            print('Bot FR = ', param['BotFRr'][1])
            print('tool r = ', tool['tool_R'])
            print('thick = ', param['Thick'])
            Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(clock, r_[3][0], r_[3][1], round(param['BotFRr'][1]-Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[3][0], r_[3][1])
    Gcode = Gcode + Add_part_str_r_end
    Gcode = Gcode + ';LEFT SIDE\r\n'
    Gcode = Gcode + Add_part_str_l
    if l_[0][0] != l_[1][0]:
        if param['TopFRl'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(clock, l_[1][0], l_[1][1], round(param['TopFRl'][1]+Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(l_[1][0], l_[1][1])
    Gcode = Gcode + 'X{} Z{}\r\n'.format(l_[2][0], l_[2][1])
    if l_[2][0] != l_[3][0]:
        if param['BotFRl'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, l_[3][0], l_[3][1], round(param['BotFRl'][1]-Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(l_[3][0], l_[3][1])
    Gcode = Gcode + 'Z{}\r\n'.format(r_[3][1])
    Gcode = Gcode + Add_part_str_l_end
    return Gcode


def DrawSharpCutterRough(r_, l_, param, tool, DCurr, Z_l, Z_r, Z_l_Up, Z_r_Up, zl_start = None, zr_start = None):
    # param = {'TopFRr': ['R', 5],'TopFRl': ['R', 5],'BotFRr': ['R', 5],'BotFRl': ['R', 5], Xa: 0.5, Za: 0.5, corrector=False, 'rXstock': 1., 'Thick': thick }
    # tool = {type:R/A; B:10; angle:35; tool_R: 5; bind_place: 'bind1/2/3/4/5'}
    print('DrawSharpCutterRough Start')
    R_3 = ''; R_5 = ''
    Add_part = 2
    Radd = tool['tool_R'] + param['Thick']

    if zr_start is None:
        r_part = 'G0 Z{}\r\nX{}\r\nG1X{} Z{}\r\nZ{}\r\n'.format(round(r_[5][1], 3), round(DCurr + tool['rX step']), DCurr, round(r_[4][1], 3), round(Z_r, 3))
        l_part = 'G0 Z{}\r\nX{}\r\nG1X{} Z{}\r\nZ{}\r\n'.format(round(l_[5][1], 3), round(DCurr + tool['rX step']), DCurr, round(l_[4][1], 3), round(Z_l, 3))
    else:
        r_part = 'G0 Z{}\r\nX{}\r\nG1X{} Z{}\r\nZ{}\r\n'.format(round(zr_start-(2+tool['tool_R']), 3), round(DCurr + tool['rX step'], 3), DCurr, round(zr_start, 3), round(Z_r, 3))
        l_part = 'G0 Z{}\r\nX{}\r\nG1X{} Z{}\r\nZ{}\r\n'.format(round(zl_start + (2+tool['tool_R']), 3), round(DCurr + tool['rX step'], 3), DCurr, round(zl_start, 3), round(Z_l, 3))
    DCurrUp = DCurr + tool['rX step']*2
    if param['BotFRl'][0] == 'R':
            mod3 = 'G2'
            R_3 = abs(param['BotFRl'][1] - Radd)
            move3l = 'X{} Z{} R{}\r\n'.format(round(l_[2][0], 3), round(l_[2][1], 3), R_3)
    else:
            mod3 = 'G1'
            move3l = 'X{} Z{}\r\n'.format(round(l_[2][0], 3), round(l_[2][1], 3))

    mod4 = 'G1'
    move4l = 'X{} Z{}\r\n'.format(round(l_[1][0], 3), round(l_[1][1], 3))

    if param['TopFRl'][0] == 'R':
        mod5 = 'G3'
        R_5 = abs(param['TopFRl'][1] + Radd)
        move5l = 'X{} Z{} R{}\r\n'.format(round(l_[0][0], 3), round(l_[0][1], 3), R_5)
    else:
        mod5 = 'G1'
        move5l = 'X{} Z{}\r\n'.format(round(l_[0][0], 3), round(l_[0][1], 3))

    mod3 = '' if mod3 == 'G1' else mod3
    mod4 = '' if mod4 == mod3 else mod4
    mod5 = '' if mod5 == mod4 else mod5
    mod6 = 'G1' if mod5 != 'G1' else ''
    lastx = None
    if DCurrUp > l_[0][0]:
        modCurD = mod6
    if DCurrUp <= l_[0][0]:
        modCurD = mod5
    if DCurrUp <= l_[1][0]:
        modCurD = mod4
    if DCurrUp <= l_[2][0]:
        modCurD = mod3

    l_part = l_part + ';ZL = {}\r\n'.format(round(Z_l, 3))
    if DCurrUp > l_[2][0] >= DCurr:
        l_part = l_part + mod3 + move3l
        lastx = l_[2][0]
    if DCurrUp > l_[1][0] >= DCurr:
        l_part = l_part + mod4 + move4l
        lastx = l_[1][0]
    if DCurrUp > l_[0][0] >= DCurr:
        l_part = l_part + mod5 + move5l
        lastx = l_[0][0]
    if DCurrUp != lastx:
        R_value = R_3 if l_[3][0] < DCurrUp <= l_[2][0] else R_5
        a = '' if modCurD == 'G1' or modCurD == '' else 'R{}'.format(R_value)
        print('here L')
        l_part = l_part + modCurD + 'X{} Z{} {}\r\n'.format(round(DCurrUp, 3), round(Z_l_Up, 3), a)
    l_part = l_part + 'G1 X{}\r\n' .format(round(DCurrUp + Add_part, 3))

    DCurrUp = DCurr + tool['rX step']*2
    if param['BotFRr'][0] == 'R':
        mod3 = 'G3'
        R_3 = abs(param['BotFRr'][1] - Radd)
        move3l = 'X{} Z{} R{}\r\n'.format(round(r_[2][0], 3), round(r_[2][1], 3), R_3)
    else:
        mod3 = 'G1'
        move3l = 'X{} Z{}\r\n'.format(round(r_[2][0], 3), round(r_[2][1], 3))

    mod4 = 'G1'
    move4l = 'X{} Z{}\r\n'.format(round(r_[1][0], 3), round(r_[1][1], 3))

    if param['TopFRr'][0] == 'R':
        mod5 = 'G2'
        R_5 = abs(param['TopFRr'][1] + Radd)
        move5l = 'X{} Z{} R{}\r\n'.format(round(r_[0][0], 3), round(r_[0][1], 3), R_5)
    else:
        mod5 = 'G1'
        move5l = 'X{} Z{}\r\n'.format(round(r_[0][0], 3), round(r_[0][1], 3))

    mod3 = '' if mod3 == 'G1' else mod3
    mod4 = '' if mod4 == mod3 else mod4
    mod5 = '' if mod5 == mod4 else mod5
    mod6 = 'G1' if mod5 != 'G1' else ''
    lastx = None
    if DCurrUp > r_[0][0]:
        modCurD = mod6
    if DCurrUp <= r_[0][0]:
        modCurD = mod5
    if DCurrUp <= r_[1][0]:
        modCurD = mod4
    if DCurrUp <= r_[2][0]:
        modCurD = mod3

    if DCurrUp > r_[2][0] >= DCurr:
        r_part = r_part + mod3 + move3l
        lastx = r_[2][0]
    if DCurrUp > r_[1][0] >= DCurr:
        r_part = r_part + mod4 + move4l
        lastx = r_[1][0]
    if DCurrUp > r_[0][0] >= DCurr:
        r_part = r_part + mod5 + move5l
        lastx = r_[0][0]
    if DCurrUp != lastx:
        R_value = R_3 if r_[3][0] < DCurrUp <= r_[2][0] else R_5
        a = '' if modCurD == 'G1' or modCurD == '' else 'R{}'.format(R_value)
        r_part = r_part + modCurD + 'X{} Z{} {}\r\n'.format(round(DCurrUp, 3), round(Z_r_Up, 3), a)
    r_part = r_part + 'G1 X{}\r\n' .format(round(DCurrUp + Add_part, 3))
    return r_part, l_part



def DrawGrooveGcodeRough(tool:dict, r_:list, l_:list, param,  limit_trajectory, _45=False):#todo меняю тут second_tool_dict:dict,
    print('DrawGrooveGcodeRough')
    Radd = tool['tool_R'] + param['Thick']
    Dmax = r_[0][0] if r_[0][0] > l_[0][0] else l_[0][0]
    tool_step_X = tool['rX step'] * 2
    DCurr = Dmax - tool_step_X
    Gcode = ''
    #        tool = {'type': 'B', 'B': float(tool_l[0].B.text()), 'tool_R': tool_r,
    #            'bind_place': tool_l[0].Bind.currentIndex() + 1, 'rX step': float(tool_l[0].RX_step.text()),
    #            'Lap min': float(tool_l[0].RX_step.text())}
    #param = {'TopFRr': [top_type_R, top_Rvalue], 'TopFRl': [top_type_L, top_Lvalue], 'BotFRr': [bot_type_R, bot_Rvalue],
    #         'BotFRl': [bot_type_L, bot_Lvalue], 'Xa': allowanceX, 'Za': allowanceZ, 'accurate': rough_.accurate.isChecked(),
    #         'rXstock': float(tool_l[2].rXallowance.text()), 'Thick': thick, 'corrector': False}
    if tool['type'] == 'A':
        result_lim_str1, r_side_lim, l_side_lim = DrawGrooveGcodeFinish(tool, trajectory_dots=limit_trajectory, param=param, _45 = True)
        # todo Radius may be is not right. it depends on whenether 45tool had the space for ark making
        Dmax = tool['rX step'] * 2 + r_[0][0]
        DCurr = Dmax
        Gcode_r = ''; Gcode_l = ''
        limitZl = None; limitZr = None
        import os
        clear = lambda: os.system('cls')
        clear()
        while True:
            newDcurr = DCurr - tool_step_X
            if newDcurr > r_[3][0]:
                DCurr = newDcurr
            else:
                DCurr = r_[3][0]
            Z_l, Z_r = takeZl_Zr_from_groove1(DCurr, l_, r_, param, tool, Radd)
            Z_l_Up, Z_r_Up = takeZl_Zr_from_groove1(DCurr + tool_step_X, l_, r_, param, tool, Radd)#tool['rX step']
            if _45:
                limitZl, limitZr = takeZl_Zr_from_groove1(DCurr=DCurr, l_1=l_side_lim, r_1=r_side_lim, param=param, tool=tool, Radd=Radd)
            Gr, Gl = DrawSharpCutterRough(r_, l_, param, tool, DCurr, Z_l, Z_r, Z_l_Up, Z_r_Up, zl_start=limitZl, zr_start=limitZr)
            Gcode_r = Gcode_r + Gr
            Gcode_l = Gcode_l + Gl
            if DCurr == r_[3][0]:
                break
        Gcode = Gcode_r + 'G0 X{}\r\n'.format(Dmax) + Gcode_l
    elif tool['type'] == 'B' or tool['type'] == 'R':
        result_lim_str1, r_side_lim, l_side_lim = DrawGrooveGcodeFinish(tool, trajectory_dots=limit_trajectory, param=param)
        if r_side_lim[-1][0] > r_[-1][0]:
            r_side_lim.append([r_[-1][0], l_[0][1]])
            l_side_lim.append([l_[-1][0], r_[0][1]])
        print('B check r_side_lim = ', r_side_lim)
        # todo Radius may be is not right. it depends on whenether 45tool had the space for ark making
        Z_l_prev = l_[0][1]
        Z_r_prev = r_[0][1]
        print('DCURR in while: ', DCurr)
        while DCurr >= r_[3][0]:
            Do = DCurr + tool_step_X + 2
            Z_l, Z_r = takeZl_Zr_from_groove1(DCurr, l_, r_, param, tool, Radd)
            if _45:
                limitZl, limitZr = takeZl_Zr_from_groove1(DCurr=DCurr, l_1=l_side_lim, r_1=r_side_lim, param=param, tool=tool, Radd=Radd)
                print('B limitZr = ', limitZr)
                #посчитать takeZl_Zr_from_groove1
                Gcode = Gcode + DrawOffCutterRough(Z_l, Z_r, DCurr, b=tool['B'], ov=tool['Lap min'], Do=Do,
                Z_l_prev=Z_l_prev, Z_r_prev=Z_r_prev, r_=r_, l_=l_, param=param, tool=tool, limitZr=limitZr, limitZl=limitZl)
            else:
                Gcode = Gcode + DrawOffCutterRough(Z_l, Z_r, DCurr, b=tool['B'], ov=tool['Lap min'], Do=Do, Z_l_prev=Z_l_prev, Z_r_prev=Z_r_prev, r_=r_, l_=l_, param=param, tool=tool)
            Z_l_prev, Z_r_prev = Z_l, Z_r
            if r_[3][0] - tool_step_X < DCurr - tool_step_X < r_[3][0]:
                DCurr = r_[3][0]
            else:
                DCurr = DCurr - tool_step_X
                print('tool_step_X = ', tool_step_X)
                print('AAAAAAAAAAAAAAAAAAAAAAA: ', DCurr)
        Gcode = Gcode + 'G0 X{}\r\n'.format(Dmax)
        print('new_rough_trajectory = ', limit_trajectory)
    else:#todo 45
        print('new_rough_trajectory 45 = ', limit_trajectory)
        print('1|||  r_ = ', r_)
        print('1|||  l_ = ', l_)
        r_ = k_multiplayer(result=r_, index=0, k=2)
        l_ = k_multiplayer(result=l_, index=0, k=2)
        print('|||  r_ = ', r_)
        print('|||  l_ = ', l_)
        print('RRR DCurr = ', DCurr)
        Gcode = Gcode + DrawGrooveGcode45Rough(r_, l_, param, tool, DCurr=Dmax*2)
    return Gcode


def DrawSharpCutter(r_, l_, param, tool):
    # param = {'TopFRr': ['R', 5],'TopFRl': ['R', 5],'BotFRr': ['R', 5],'BotFRl': ['R', 5], Xa: 0.5, Za: 0.5, corrector=False, 'rXstock': 1., 'Thick': thick }
    # tool = {type:R/A; B:10; angle:35; tool_R: 5; bind_place: 'bind1/2/3/4/5'}
    print('work with r_ = ', r_)
    Gcode = ''
    Add_part = 2
    Radd = tool['tool_R'] + param['Thick']
    if param['corrector'] is True:
        Add_part = 1 + Radd*2
        Radd = 0
        Add_part_str_r = 'G0 Z{}\r\nX{}\r\nG1 G41 X{}\r\n'.format(round(r_[5][1], 3), round(r_[5][0] + Add_part + tool['rX step'], 3), round(r_[5][0], 3))
        Add_part_str_l = 'G0 Z{}\r\nX{}\r\nG1 G42 X{}\r\n'.format(round(l_[5][1], 3), round(l_[5][0] + Add_part + tool['rX step'], 3), round(l_[5][0], 3))
        Add_part_str_r_end = 'G40 G0X{}\r\n'.format(round(l_[0][0] + Add_part, 3))
        Add_part_str_l_end = 'G40 G0X{}\r\n'.format(round(r_[0][0] + Add_part, 3))
    else:
        Add_part_str_r = 'G0 Z{}\r\nX{}\r\nG1X{}\r\n'.format(r_[5][1], round(r_[5][0] + Add_part + tool['rX step']), round(r_[5][0], 3))
        Add_part_str_l = 'G0 Z{}\r\nX{}\r\nG1X{}\r\n'.format(l_[5][1], round(l_[5][0] + Add_part + tool['rX step']), round(l_[5][0], 3))
        print('l_ = ', l_)
        Add_part_str_r_end = 'G0 X{}\r\n'.format(round(l_[0][0] + Add_part, 3))#todo Add_part_str_r_end  useless
        Add_part_str_l_end = 'G0 X{}\r\n'.format(round(r_[0][0] + Add_part, 3))
    G2_G3_normal = True
    if G2_G3_normal:
       clock = 'G2'
       reverseclock = 'G3'
    else:
       clock = 'G3'
       reverseclock = 'G2'


    Gcode = Gcode + ';RIGHT SIDE\r\n'
    Gcode = Gcode + Add_part_str_r
    Gcode = Gcode + 'X{} Z{}\r\nZ{}\r\n'.format(r_[4][0], r_[4][1], r_[3][1])
    if r_[3][0] != r_[2][0]:
        if param['BotFRr'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(reverseclock, r_[2][0], r_[2][1], round(param['BotFRr'][1]-Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[2][0], r_[2][1])
    Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[1][0], r_[1][1])
    if r_[1][0] != r_[0][0]:
        if param['TopFRr'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(clock, r_[0][0], r_[0][1], round(param['TopFRr'][1]+Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[0][0], r_[0][1])
    Gcode = Gcode + Add_part_str_r_end

    overlap = 1
    Gcode = Gcode + ';LEFT SIDE\r\n'
    Gcode = Gcode + Add_part_str_l
    Gcode = Gcode + 'X{} Z{}\r\nX{}Z{}\r\n'.format(l_[4][0], round(l_[4][1]+overlap, 3), l_[3][0], round(l_[3][1], 3))
    if l_[3][0] != l_[2][0]:
        if param['BotFRl'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\nG1'.format(clock, l_[2][0], l_[2][1], round(param['BotFRl'][1]-Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(l_[2][0], l_[2][1])
    Gcode = Gcode + 'X{} Z{}\r\n'.format(l_[1][0], l_[1][1])
    if r_[1][0] != r_[0][0]:
        if param['TopFRl'][0] == 'R':
            Gcode = Gcode + '{} X{} Z{} R{}\r\n'.format(reverseclock, l_[0][0], l_[0][1], round(param['TopFRl'][1]+Radd, 3))
        else:
            Gcode = Gcode + 'X{} Z{}\r\n'.format(r_[0][0], l_[0][1])
    #Gcode = Gcode + 'G0 X{}\r\n'.format(l_[5][0]+10)
    Gcode = Gcode + Add_part_str_l_end
    return Gcode

def DrawOffCutterRough(Z_l, Z_r, D, b, ov, Do, Z_l_prev, Z_r_prev, r_, l_, param, tool, limitZl=None, limitZr=None):
    # tool = {type:R/A; B:10; angle:35; tool_R: 5; bind_place: 'bind1/2/3/4/5'}
    #param = {'TopFRr': [top_type_R, top_Rvalue], 'TopFRl': [top_type_L, top_Lvalue], 'BotFRr': [bot_type_R, bot_Rvalue],
    #         'BotFRl': [bot_type_L, bot_Lvalue], 'Xa': allowanceX, 'Za': allowanceZ, 'accurate': self.accurate.isChecked(),
    #         'rXstep': float(self.RX_step.text()), 'Lap min': float(self.ZX_step.text()),
    #         'Thick': thick}
    #Angle_r = math.degrees(math.atan((r_[0][1] - (r_[1][1])) / (r_[0][0] - (r_[1][0]) * 2)))
    #Angle_l = math.degrees(math.atan((l_[1][1] - (l_[0][1])) / (l_[1][0] - (l_[0][0]) * 2)))
    #Dmax = max_None(r_[0][0], l_[0][0])
    Lz = Z_r - Z_l
    step = b - ov
    D_add = 2
    n = Lz / step - 1
    n = int(n - n%1)
    Gcode = ''
    print('ov = {}, b = {}'.format(ov, b))
    Gcode = Gcode + ';block start\r\n'
    Radd = tool['tool_R'] + param['Thick']

    print('Z_r_prev = ', Z_r_prev)
    Z_r_const = copy.copy(Z_r)
    print('Z_r == ', Z_r)
    Gcode = Gcode + 'G0'
    if Z_r_prev > Z_r:
        Z_r_prev = Z_r_prev - step
        while Z_r_prev - ov*0.3 > Z_r: #for veeery gentle slope. If Z step too big for X step and we need a few more plungs
            X_R = takeXR_from_groove1(Z_r_prev, r_, param, Radd)
            print("Z_r_prev равно {}, X_R = {}".format(Z_r_prev, X_R))
            Gcode = Gcode + 'Z{}\r\nG1 X{}\r\nG0 X{}\r\n'.format(round(Z_r_prev, 3), round(X_R, 3), round(D+D_add+tool['rX step']*2, 3))
            Z_r_prev = Z_r_prev - step
    Z_r = Z_r_const
    for k in range(n+2):
        newZ = Z_r - k * step
        if limitZr is not None and limitZl is not None and limitZl+ov < newZ < limitZr-ov:
            continue
        if newZ != round(newZ, 1) and k != 0:
            if newZ - round(newZ, 1) < 0.1:# * ov
                newZ = round(newZ, 1)
        if newZ - Z_l > ov*0.3:
            Gcode = Gcode + 'Z{}\r\nG1 X{}\r\nG0 X{}\r\n'.format(round(newZ, 3), round(D, 3), round(Do, 3))
    Gcode = Gcode + 'Z{}\r\nG1 X{}\r\n'.format(round(Z_l, 3), round(D, 3))

    print("Z_l_prev === ", Z_l_prev)
    print("Z_l = ", Z_l)
    print('l_ ===== ', l_)

    Gcode = Gcode + 'G0'
    if Z_l_prev < Z_l:
        Gcode = Gcode + 'X{}\r\n'.format(round(Do, 3))
        Z_l = Z_l - step
        while Z_l_prev + ov*0.3 < Z_l:
            X_L = takeXl_from_groove1(Z_l, l_, param, Radd)
            Gcode = Gcode + 'Z{}\r\nG1 X{}\r\nG0 X{}\r\n'.format(round(Z_l, 3), round(X_L, 3), round(D+D_add+tool['rX step']*2, 3))
            Gcode = Gcode + ';Z_l_prev = {}, Z_l = {}\r\n'.format(round(Z_l_prev, 3), round(Z_l, 3))
            Z_l = Z_l - step
    else:
        Gcode = Gcode + 'X{}\r\n'.format(round(D + 2, 3))
    Gcode = Gcode + ';Z_l = {} Z_r = {} \r\n'.format(Z_l, Z_r)
    Gcode = Gcode + 'X{}\r\n'.format(Do + D_add)
    Gcode = Gcode + ';block end\r\n'
    return Gcode


def groove_dot(R_Chamfer, R_ChamferValue, TB, len_, LeftRight, dot1, dot, dot2):
    """
    find center R for a new tool.
    :param R_Chamfer:
    :param R_ChamferValue:
    :param TB:
    :param len_:
    :param LeftRight:
    :param dot1:
    :param dot:
    :param dot2:
    :return:
    """
    #dot1 = [x1, z1]
    #dot = [[x00, z00], [x11, z11], [x22, z22]]
    #dot2 = [x2, z2]
    G_code = ''
    #result =   [[x, z],      [x1, z1],     [x2, z2]]
    result = [[None, None], [None, None], [None, None]]
    if R_Chamfer == 'R':
        n_x1, n_z1, n_x2, n_z2 = transfer(LeftRight, len_, dot1[0], dot1[1], dot[1][0], dot[1][1])
        m_x1, m_z1, m_x2, m_z2 = transfer(LeftRight, len_, dot[2][0], dot[2][1], dot2[0], dot2[1])
        print('m_x1 = {}, m_z1 = {}, m_x2 = {}, m_z2 = {}'.format(m_x1, m_z1, m_x2, m_z2))
        result[0][0], result[0][1] = lines_intersection_dots(n_x1, n_z1, n_x2, n_z2, m_x1, m_z1, m_x2, m_z2)
        print('|||| result == ', result)
        if TB != 'Bot' or R_ChamferValue >= len_:
            result[1][0], result[1][1], result[2][0], result[2][1] = n_x2, n_z2, m_x1, m_z1
            print('|||| new result = ', result)
        return result

    elif R_Chamfer == 'Chamfer':
        n_x1, n_z1, n_x2, n_z2 = transfer('right', len_, dot1[0], dot1[1], dot[0][0], dot[0][1])#смещение верха
        m_x1, m_z1, m_x2, m_z2 = transfer('right', len_, dot[2][0], dot[2][1], dot2[0], dot2[1])#смещение низа
        x1, z1 = lines_intersection_dots(n_x1, n_z1, n_x2, n_z2, m_x1, m_z1, m_x2, m_z2)#точка угла
        k_x1, k_z1, k_x2, k_z2 = transfer('right', len_, dot[1][0], dot[1][1], dot[2][0], dot[2][1])#смещение фаски
        x2, z2 = lines_intersection_dots(m_x1, m_z1, m_x2, m_z2, k_x1, k_z1, k_x2, k_z2)
        #print('||| TB = {}, n_x1 = {}, n_z1 = {}, n_x2 = {}, n_z2 = {}, k_x1 = {}, k_z1 = {}, k_x2 = {}, k_z2 = {}'.format(TB, n_x1, n_z1, n_x2, n_z2, k_x1, k_z1, k_x2, k_z2))
        x_c, z_c = lines_intersection_dots(n_x1, n_z1, n_x2, n_z2, k_x1, k_z1, k_x2, k_z2)#верхняя точка центр
        result[0][0], result[0][1] = x1, z1  # check?

        if TB != 'Bot' or (z_c < z1 and x_c >= x2):
            result[1], result[2] = [x_c, z_c], [x2, z2]
        else:#
            result[1], result[2] = [x_c, z_c], [x2, z2]
        return result

    else:
        #print('Problem place:  len_ = {}, dot1[0] = {}, dot1[1] = {}, dot[0][0] = {}, dot[0][1] = {}'.format(len_, dot1[0], dot1[1], dot[0][0], dot[0][1]))
        n_x1, n_z1, n_x2, n_z2 = transfer('right', len_, dot1[0], dot1[1], dot[0][0], dot[0][1])
        m_x1, m_z1, m_x2, m_z2 = transfer('right', len_, dot[0][0], dot[0][1], dot2[0], dot2[1])
        x_c, z_c = lines_intersection_dots(n_x1, n_z1, n_x2, n_z2, m_x1, m_z1, m_x2, m_z2)
        result[0][0], result[0][1] = x_c, z_c
        return result


def draw_45_tragectory(tragectory45, tragectory_prev_limit, geometry, tool45, tool, param):#здесь черновой второй инструмент
    print('draw_45_tragectory')
    #import os
    #clear = lambda: os.system('cls')
    #clear()
    for i in range(len(geometry)):
        geometry[i] = k_multiplayer(result=geometry[i], index=0, k=2)
    result_str1, r_side_track, l_side_track = DrawGrooveGcodeFinish(tool, trajectory_dots=geometry, param=param)
    for i in range(len(tragectory_prev_limit)):
        tragectory_prev_limit[i] = k_multiplayer(result=tragectory_prev_limit[i], index=0, k=2)
    Gcode2 = DrawGrooveGcodeRough(tool=tool, r_=r_side_track, l_=l_side_track, limit_trajectory=tragectory_prev_limit, param=param, _45=True)#
    pseudo45tool = {'type': 'R', 'B': 10.0, 'tool_R': tool45['tool_R'], 'bind_place': 3}
    result_str1, r_45, l_45 = DrawGrooveGcodeFinish(pseudo45tool, trajectory_dots=tragectory45, param=param)#должен получить 45
    Gcode1 = DrawGrooveGcodeRough(tool=tool45, r_=r_45, l_=l_45, limit_trajectory=tragectory45, param=param)# + 'Gcode1 end\n'
    Gcode = Gcode1 + Gcode2
    return Gcode



def center_from_tragectory(dot3, R):#внимание, может быть не по касательной
    print('center_from_tragectory')
    print('R = ', R)
    print('dot3 = ', dot3)
    # точка пересечений окружностей
    a, b = find_center(dot_in1=dot3[1], dot_in2=dot3[2], r=R)
    print('__?__\n a = {}, b = {}'.format(a, b))
    new_center = which_closer(a, b, dot3[0], 'farther')
    print('new_center = ', new_center)
    print('if dot3 changed = ', dot3)
    return new_center


def finish_groove_func(geometry, allowanceX, allowanceZ, allowanceThickness,
                  top_r_value, top_l_value, bot_r_value, bot_l_value,
                  top_type_r, top_type_l, bot_type_r, bot_type_l):
    #не даёт привязку
    #finish_trajectory = [[[Top_r_x, Top_r_z], [Top_r_x_1, Top_r_z_1], [Top_r_x_2, Top_r_z_2]],
    #                     [[Bot_r_x, Bot_r_z], [Bot_r_x_1, Bot_r_z_1], [Bot_r_x_2, Bot_r_z_2]],
    #                     [[Bot_l_x, Bot_l_z], [Bot_l_x_1, Bot_l_z_1], [Bot_l_x_2, Bot_l_z_2]],
    #                     [[Top_l_x, Top_l_z], [Top_l_x_1, Top_l_z_1], [Top_l_x_2, Top_l_z_2]]]

    print("finish_groove_func")
    print('geometry = ', geometry)
    first = geometry[0]
    Top_r_x, Top_r_z, Top_r_x_1, Top_r_z_1, Top_r_x_2, Top_r_z_2 = first[0][0], first[0][1], first[1][0], first[1][1], first[2][0], first[2][1]

    second = geometry[1]
    Bot_r_x, Bot_r_z, Bot_r_x_1, Bot_r_z_1, Bot_r_x_2, Bot_r_z_2 = second[0][0], second[0][1], second[1][0], second[1][1], second[2][0], second[2][1]

    third = geometry[2]
    Bot_l_x, Bot_l_z, Bot_l_x_1, Bot_l_z_1, Bot_l_x_2, Bot_l_z_2 = third[0][0], third[0][1], third[1][0], third[1][1], third[2][0], third[2][1]

    fourth = geometry[3]
    Top_l_x, Top_l_z, Top_l_x_1, Top_l_z_1, Top_l_x_2, Top_l_z_2 = fourth[0][0], fourth[0][1], fourth[1][0], fourth[1][1], fourth[2][0], fourth[2][1]
    print('top_type_r = ', top_type_r)
    len_ = allowanceThickness

    if Top_r_x_1 is None:
        dot1 = [Top_r_x/2, Top_r_z+100]
    else:
        dot1 = [Top_r_x_1/2, Top_r_z_1+100]
    if Bot_r_x_1 is None:
        dot2 = [Bot_r_x / 2, Bot_r_z]
        print('1dot2 in finish_groove_func: ', dot2)
    else:
        dot2 = [Bot_r_x_1 / 2, Bot_r_z_1]
        print('2dot2 in finish_groove_func: ', dot2)

    dot = k_multiplayer([[Top_r_x, Top_r_z], [Top_r_x_1, Top_r_z_1], [Top_r_x_2, Top_r_z_2]], 0, 0.5)
    print('||| top_type_r = {}, top_r_value = {}, dot1 = {}, dot = {}, dot2 = {}'.format(top_type_r, top_r_value, dot1, dot, dot2))

    result_top_r = groove_dot(R_Chamfer=top_type_r, R_ChamferValue=top_r_value, TB='Top', len_=len_, LeftRight='right', dot1=dot1, dot=dot, dot2=dot2)
    print('|||| result_top_r == ', result_top_r)
    if Top_l_x_1 is None:
        dot1 = [Top_l_x / 2, -Top_l_z + 100]
    else:
        dot1 = [Top_l_x_1 / 2, -Top_l_z_1 + 100]
    if Bot_l_x_1 is None:
        dot2 = [Bot_l_x / 2, -Bot_l_z]
    else:
        dot2 = [Bot_l_x_1 / 2, -Bot_l_z_1]
    dot = k_multiplayer([[Top_l_x, Top_l_z], [Top_l_x_1, Top_l_z_1], [Top_l_x_2, Top_l_z_2]], 0, 0.5)
    dot = k_multiplayer(dot, 1, -1)
    result_top_l = groove_dot(R_Chamfer=top_type_l, R_ChamferValue=top_l_value, TB='Top', len_=len_, LeftRight='right', dot1=dot1, dot=dot, dot2=dot2)

    if Top_r_x_1 is None:
        dot1 = [Top_r_x / 2, Top_r_z]
    else:
        dot1 = [Top_r_x_2 / 2, Top_r_z_2]
    if Bot_r_x_1 is None:
        print('yy1')
        dot2 = [Bot_r_x / 2, Bot_r_z + 100]# отсюда ноги растут наверное
    else:
        print('yy2')
        dot2 = [Bot_r_x_2 / 2, Bot_r_z_2 + 100]
    dot = k_multiplayer([[Bot_r_x, Bot_r_z], [Bot_r_x_1, Bot_r_z_1], [Bot_r_x_2, Bot_r_z_2]], 0, 0.5)
    #што то тут чинить
    print('|||| bot_type_r = {}, bot_r_value = {}'.format(bot_type_r, bot_r_value))
    print('mda1 dot1 = {}, dot2 = {}'.format(dot1, dot2))
    print('mda2 dot = ', dot)
    result_bot_r = groove_dot(R_Chamfer=bot_type_r, R_ChamferValue=bot_r_value, TB='Bot', len_=len_, LeftRight='right', dot1=dot1, dot=dot, dot2=dot2)
    print('особое result_bot_r = ', result_bot_r)
    if Top_l_x_1 is None:
        dot1 = [Top_l_x / 2, -Top_l_z]
    else:
        dot1 = [Top_l_x_2 / 2, -Top_l_z_2]
    if Bot_l_x_1 is None:
        dot2 = [Bot_l_x / 2, -Bot_l_z + 100]
    else:
        dot2 = [Bot_l_x_2 / 2, -Bot_l_z_2 + 100]
    dot = k_multiplayer([[Bot_l_x, Bot_l_z], [Bot_l_x_1, Bot_l_z_1], [Bot_l_x_2, Bot_l_z_2]], 0, 0.5)
    dot = k_multiplayer(dot, 1, -1)
    result_bot_l = groove_dot(R_Chamfer=bot_type_l, R_ChamferValue=bot_l_value, TB='Bot', len_=len_, LeftRight='right', dot1=dot1, dot=dot, dot2=dot2)

    result_top_r = k_multiplayer(result_top_r, 0, 2)
    result_top_l = k_multiplayer(result_top_l, 0, 2)
    result_bot_r = k_multiplayer(result_bot_r, 0, 2)
    result_bot_l = k_multiplayer(result_bot_l, 0, 2)
    result_top_l = k_multiplayer(result_top_l, 1, -1)
    result_bot_l = k_multiplayer(result_bot_l, 1, -1)

    result_top_r = move_ax_along(result=result_top_r, index=0, add=allowanceX*2)
    result_top_l = move_ax_along(result=result_top_l, index=0, add=allowanceX*2)
    result_bot_r = move_ax_along(result=result_bot_r, index=0, add=allowanceX*2)
    result_bot_l = move_ax_along(result=result_bot_l, index=0, add=allowanceX*2)

    result_top_r = move_ax_along(result=result_top_r, index=1, add=-allowanceZ)
    result_top_l = move_ax_along(result=result_top_l, index=1, add=allowanceZ)
    result_bot_r = move_ax_along(result=result_bot_r, index=1, add=-allowanceZ)
    result_bot_l = move_ax_along(result=result_bot_l, index=1, add=allowanceZ)

    new_geometry = [result_top_r, result_bot_r, result_bot_l, result_top_l]
    print('geometry in find = ', geometry)
    print('new geometry in find = ', new_geometry)
    return new_geometry
