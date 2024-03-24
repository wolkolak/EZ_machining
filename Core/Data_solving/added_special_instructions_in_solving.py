from left_zone.ARK_solving import *
import math
from left_zone.bring_coords_to_main_G549 import move_from_main_G549, move_to_main_G549_new, move_from_main_G549222
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.postfix_tokens_calculation import postfixTokenCalc
from scipy.spatial.transform import Rotation
import copy

places = {'X': 4, 'Y': 5, 'Z': 6, 'A': 7, 'B': 8, 'C': 9, 'I': 10, 'J': 11, 'K': 12, 'R': 13, 'F': 14}#todo CR check  'AR': 15

def siemens_SUB_helper(vars1, vars2):
    for k in vars1:
        if k[0] == 'R' and k[1:].isnumeric() or k in vars2:
            vars2[k] = vars1[k]


def REPEAT_lbl_instruction(self, local_line, i_str):
    """
    Эта функция ищет точку до которой необходимо протянуть блок строк от первой метки
    запускается и работает для nextSHIFT
    """
    #self - np_box
    print('REPEAT_lbl_instruction')
    print('i_str = ', i_str)
    print('local_line = ', local_line)
    last_place = self.return_stack[-1]
    print('last_place = ', last_place)
    if last_place[4] is not None:#REPEATB
        return i_str#last_place[0]
    if last_place[2] is None:
        print('222')
        LBL2 = 'ENDLABEL'
    elif type(last_place[2][0]) is int :
        print(f'last_place[2][0] = {last_place[2][0]}, type = {type(last_place[2][0])}')
        print(f'Тут дрянь {self.redactor.Logs.math_logs}')
        return last_place[2][0]
    else:
        LBL2 = last_place[2][0]

    L = len(self.SHIFTcontainer.np_for_vars)
    while local_line < L and self.SHIFTcontainer.np_for_vars[local_line][2] in [30, 40, 41] and \
            self.SHIFTcontainer.base_dict[self.SHIFTcontainer.np_for_vars[local_line][3]][0] != LBL2:  # todo так нельзя? внутри может быть алгоритмический цикл или даже переход GOTO

        if self.SHIFTcontainer.np_for_vars[local_line][1] == 41:  # lbl
            if self.return_stack[-1][2] is None or self.return_stack[-1][3] is None:
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{i_str} line error. Related to None in stack for REPEAT and PROC\n'
                print('или эта')
                return i_str+1
            #if self.SHIFTcontainer.base_dict[self.SHIFTcontainer.np_for_vars[local_line][3]][0] == last_place[2][0]:
            #    return i_str
        local_line = local_line + 1
    if local_line < L and self.SHIFTcontainer.base_dict[self.SHIFTcontainer.np_for_vars[local_line][3]][0] == LBL2:
        print('эта ветка')

        i_str = self.SHIFTcontainer.np_for_vars[local_line][0]
        return i_str
    elif local_line >= L:
        print('такс а тут')
        self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{i_str} line: can\'t find "{LBL2} in file"\n'
        return i_str + 1


def feed_axis_from_dict(self, v_i, current_vars, last_significant_line, current_g_modal, polar_cur, DictG549shift):#, old_v
    if self.redactor.father_np_box is None:
        n = v_i[15]
    else:
        ooo = self.redactor.subNstart
        n = v_i[15] - ooo-1#?
    print(self.XYZvars_container)
    goal, local_line = self.XYZvars_container.return_info(n)
    print(f'self.XYZvars_container.return_info(n) = {self.XYZvars_container.return_info(n)}')
    AR = goal['AR']
    AP = goal['AP']
    RP = goal['RP']
    print('here')
    print('goal = ', goal)
    #print()
    for key_n in places:
        print(f'key_n = {key_n}')
        if goal[key_n[0]] is not None and len(goal[key_n[0]]) != 0:
            if goal[key_n][0] == 'IC':
                a = goal[key_n][1:]
                v_i[places[key_n]] = postfixTokenCalc(a, DICT_VARS=current_vars,  proc=self.redactor.highlight.reversal_post_processor)
                if current_g_modal['absolute_or_incremental'] == '90':
                    v_i[places[key_n]] += last_significant_line[places[key_n]]
            elif goal[key_n][0] == 'AC':
                v_i[places[key_n]] = postfixTokenCalc(goal[key_n][1:], DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
                if current_g_modal['absolute_or_incremental'] == '91':
                    v_i[places[key_n]] -= last_significant_line[places[key_n]]
            else:
                v_i[places[key_n]]= postfixTokenCalc(goal[key_n], DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
            if np.isnan(v_i[places[key_n]]) :#None
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{int(v_i[15])} line  expression error\n'
    print('AR = ', AR)
    print(f'9999v_i = {v_i}')
    self.redactor.current_machine.k_applying1_line(v_i)
    if AR is not None and AR != ():#не 360!!!
        AR = postfixTokenCalc(AR, proc=self.redactor.highlight.reversal_post_processor)
        n_h, n_v, n_p = self.n_h, self.n_v, self.n_p
        l = math.sqrt((v_i[n_h] - last_significant_line[n_h])**2 + (v_i[n_v] - last_significant_line[n_v])**2 )/2
        v_i[places['R']] = l/math.sin(math.radians(AR/2))#goal['AR']#postfixTokenCalc(goal[key_], DICT_VARS=current_vars)
    elif AP is not None or RP is not None:
        #polar_cur
        print(f'888 RP = {RP}')
        print(f'postfixTokenCalc(RP, DICT_VARS=current_vars) = {postfixTokenCalc(RP, DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)}')
        if RP is not None:
            RP = postfixTokenCalc(RP, DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
            if RP is None:
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{v_i[15]} line  expression error]\n'
                return v_i
            self.RP = RP
        else:
            RP = self.RP
        if AP is not None:
            AP = postfixTokenCalc(AP, DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
            if AP is None:
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{v_i[15]} line  expression error \n'
                return v_i
            self.AP = AP
        else:
            AP = self.AP
        v_i[self.n_h] = RP * math.cos(math.radians(AP)) + polar_cur[self.n_h - 4]
        v_i[self.n_v] = RP * math.sin(math.radians(AP)) + polar_cur[self.n_v - 4]
        #v_i[13] = RP
        #print(f'old_v = {old_v}')
        #if current_g_modal['SC'] == self.m
        print(f'last line = {last_significant_line}')
        last = move_from_main_G549(np.copy(last_significant_line), DictG549shift['G' + str(current_g_modal['SC'])])
        print(f"DictG549shift['G' + str(current_g_modal['SC']) = {DictG549shift['G' + str(current_g_modal['SC'])]}")
        print(f'DictG549shift = {DictG549shift}')
        print(f'last line 22= {last_significant_line}')
        print(f'89898 last = {last}')
        #polar - last for G54
        #if current_g_modal['absolute_or_incremental'] == '91':#relative
        #    v_i[self.n_h + 6] = polar_cur[self.n_h - 4] #- last[self.n_h]
        #    v_i[self.n_v + 6] = polar_cur[self.n_v - 4] #- last[self.n_v]
        #    L1_ = polar_cur[self.n_h - 4] - last[self.n_h]
        #    L2_ = polar_cur[self.n_v - 4] - last[self.n_v]
        #    len_ = math.sqrt(v_i[self.n_h + 6] ** 2 + v_i[self.n_v + 6] ** 2)
        #else:
        v_i[self.n_h + 6] = polar_cur[self.n_h - 4] - last[self.n_h] #- DictG549shift['G' + str(current_g_modal['SC'])][self.n_h - 4]    #-last[self.n_h]        #
        v_i[self.n_v + 6] = polar_cur[self.n_v - 4] - last[self.n_v] #- DictG549shift['G' + str(current_g_modal['SC'])][self.n_v - 4]    #-last[self.n_v]*2      #
        len_ = math.sqrt(v_i[self.n_h + 6]**2 + v_i[self.n_v + 6]**2)
        if round(len_, 5) != round(self.RP, 5):
            print(f'{round(len_, 45)} vs {round(self.RP, 5)}')
            v_i[self.n_h + 6] = None
            v_i[self.n_v + 6] = None
            #v_i[13] = self.RP

        print(f'888 1,2 = {v_i[self.n_h+6]}, {v_i[self.n_v+6]}')
        #if math.fabs(self.RP - math.sqrt((RP * math.cos(math.radians(AP)))**2 + (RP * math.sin(math.radians(AP)))**2))> 0.001:
        #    self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{v_i[0]} line  math error \n'
    print(f'v_i po factu = {v_i}')
    #self.redactor.current_machine.k_applying1_line(v_i)
    v_i[16] = None
    return v_i

def feed_siemens_POLAR_from_dict(self, info, current_vars, last_significant_line, current_g_modal, polar_cur, DictG549shift):# main_G549,
    print('polar_cur = ', polar_cur)#TODO: дело в том что IC и AC бессмысленны. Или нет?
    goal = info[1][2]
    new_dict = {'X': None, 'Y': None, 'Z': None, 'AP': None, 'RP': None}
    polar_new = [0., 0., 0.]
    for key_n in goal:
        if goal[key_n] is None:
            print(f'goal[{key_n}] = None')
            new_dict[key_n] = 0.
            continue
        print(f'key_n = {key_n}, goal = {goal}')
        if not len(goal[key_n]) == 0 and not (len(goal[key_n]) == 1 and goal[key_n][0] == '='):
            if goal[key_n][0] == 'IC':
                a = goal[key_n][1:]
                new_dict[key_n] = postfixTokenCalc(a, DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
                if current_g_modal['absolute_or_incremental'] == '90':
                    new_dict[key_n] += last_significant_line[places[key_n]]
            elif goal[key_n][0] == 'AC':
                new_dict[key_n] = postfixTokenCalc(goal[key_n][1:], DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
                if current_g_modal['absolute_or_incremental'] == '91':
                    new_dict[key_n] -= last_significant_line[places[key_n]]
            else:
                new_dict[key_n]= postfixTokenCalc(goal[key_n], DICT_VARS=current_vars, proc=self.redactor.highlight.reversal_post_processor)
            if np.isnan(new_dict[key_n]) :#None
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{int(info[0][0])} line  expression error [{key_n}]\n'
                return polar_cur
    print('Предполагаем, что polar_coord_siemens раньше перехода к базовой SC')
    print(f'new_dict = {new_dict}')
    print(f' info[1][1] = {info[1][1]}')
    print('self.n_h = ', self.n_h)
    if new_dict['AP'] is None or new_dict['RP'] is None:
        print('ttttt')
        _X = new_dict['X'] if new_dict['X'] != None else 0
        _Y = new_dict['Y'] if new_dict['Y'] != None else 0
        _Z = new_dict['Z'] if new_dict['Z'] != None else 0
        if info[1][1] == 'G111':#to zero
            print('G111')
            polar_new = [_X, _Y, _Z]
        elif info[1][1] == 'G112':
            polar_new = [_X + polar_cur[0], _Y + polar_cur[1], _Z + polar_cur[2]]
        elif info[1][1] == 'G110':#to last position
            #last = move_from_main_G549(last_significant_line, DictG549shift['G' + str(current_g_modal['SC'])])
            last = move_from_main_G549(np.copy(last_significant_line), DictG549shift['G' + str(current_g_modal['SC'])])
            #move_to_main_G549
            polar_new = [_X + last[4], _Y + last[5], _Z + last[6]]
    else:
        if info[1][1] == 'G111':  # to zero
            polar_new[self.n_h - 4] = math.cos(math.radians(new_dict['AP'])) * new_dict['RP']
            polar_new[self.n_v - 4] = math.sin(math.radians(new_dict['AP'])) * new_dict['RP']
        elif info[1][1] == 'G112':#from polar
            polar_new[self.n_h - 4] = math.cos(math.radians(new_dict['AP'])) * new_dict['RP'] + polar_cur[self.n_h - 4]
            polar_new[self.n_v - 4] = math.sin(math.radians(new_dict['AP'])) * new_dict['RP'] + polar_cur[self.n_v - 4]
        elif info[1][1] == 'G110':
            last = move_from_main_G549(np.copy(last_significant_line), DictG549shift['G' + str(current_g_modal['SC'])])
            polar_new[self.n_h - 4] = math.cos(math.radians(new_dict['AP'])) * new_dict['RP'] + last[self.n_h]
            polar_new[self.n_v - 4] = math.sin(math.radians(new_dict['AP'])) * new_dict['RP'] + last[self.n_v]
        self.AP = new_dict['AP']
        self.RP = new_dict['RP']
    print(f'polar_new = {polar_new}')

    return polar_new


def add_frame_address_new(self, NshiftCount, cur_frame_address):
    # копирование быстрее работает!!!!в полтора раза
    print('fix_frame_address')
    #print(f'AAA cur_frame_address = {cur_frame_address}')
    self.frame_address_in_visible_pool = np.concatenate([self.frame_address_in_visible_pool, cur_frame_address])
    NshiftCount = NshiftCount + 1
    return NshiftCount


def create_frame_address_new(self, i_str, cur_i_max, cur_v, i, NshiftCount):
    # копирование быстрее работает!!!!в полтора раза
    print('fix_frame_address_new')
    print(f'656565 i {i}')
   # i = i if i != 36 else i-1
    #i = i - 1 if i > 0 else 0
    print(i_str, cur_i_max, i, NshiftCount)
    print(cur_v)
    n = cur_i_max + 1
    print(f'прибавим {n}')
    cur_frame_address = np.zeros((n, 2), int)
    cur_frame_address[:, 0] = np.arange(i + NshiftCount, i + 1 + NshiftCount + cur_i_max)
    cur_frame_address[:, 1] = np.copy(cur_v[0:, 15]) + 0#todo здесь нельзя прибавлять - это реально списанные данные
    #cur_frame_address[:, 0] = np.arange(i, i + len(cur_v))

    print(f'66 cur_frame_address = {cur_frame_address}')
    #if cur_frame_address[0][0] == 38:
    #    print(f'52 catched, i = {i}')
    #    #2/0
    return cur_frame_address


def turn_around_C(x, y, z, alpha_C):
    #alpha = math.radians(alpha_C)
    x_new = x * math.cos(alpha_C) - y * math.sin(alpha_C)
    y_new = x * math.sin(alpha_C) + y * math.cos(alpha_C)
    return x_new, y_new, z

CYCLE800_dict = {57: 'xyz', 45:'xzy', 54:'yxz', 30:'yzx', 39:'zxy', 27:'zyx'}




def CYCLE800_handler(np_box, current_g_modal:dict, last_significant_line, v_i, info, scene0):
    #current_g_modal['CYCLE800'] = [1, "", 0., 57, 0., 0., 0., 0., 0., 0., 0., 0., 0., 1, 0., 1]
    #сделано#первое значение - отвод по Z. 0 - без отвода
    #TODO второе значение может быть 0, TISCH, KOPF, KOPF_TISCH, KOPF_TISCH_45, TISCH_45, KOPF_KOPF_45, TC1? в станке лежит
    #_____
    #TODO третье значение это 6значное число 100000 ;
    # 2____ - Select+, _1___ - отключает swivel,
    # ____1_ - удерживает кончик инструмента,  ____1 - аддитив
    #четвёртое значение: 57 Axis by axis(57 - XYZ, 45-XZY, 54-YXZ, 30-YZX, 39-ZXY, 27-ZYX), 64 solid angle, 185 - project angle(185-XaYaZb, 189-YaZaXb, 183-ZaXaYb), 192 - directly
    #5-7 это смещения XYZ
    #8-10 rotation arounf xyz
    #11-13 - смещения после поворота XYZ
    #четырнадцатое может быть 1 и -1; -1 значит отрицательное направление поворота
    #15 - длина отвода по Z
    #16 - 0-Не выбрано, 1- G17, 2 - G18, 3 - G19.
    #TODO как объехать????
    print('CYCLE800_handler info = ', info)
    values = info[1][2]
    for n_ in range(4, 10):
        if v_i[n_] is np.nan:
            v_i[n_] = last_significant_line[n_]
    #v_i[16] = 100.
    if values[1] != 0 and values[16] != 0:#Z отвод
        place1 = int(3+values[16][0])
        print(f'valuse16 = {values[16]}, place1 = {place1}')
        v_i[place1] = v_i[place1] + place1

    #преобразование СК
    print(f'valuse444 = {values}')
    #if values[3] ==
    #zdes
    #f = {}
    #g = f.values()
    if postfixTokenCalc(values[4]) not in CYCLE800_dict:
        np_box.redactor.Logs.math_logs = np_box.redactor.Logs.math_logs + f'{info[0][3]} line error. Related to None in stack for REPEAT and PROC\n'
        return v_i
    computed_place = [CYCLE800_dict[postfixTokenCalc(values[4])],
                      [postfixTokenCalc(values[5]), postfixTokenCalc(values[6]), postfixTokenCalc(values[7])],
                      [postfixTokenCalc(values[8]), postfixTokenCalc(values[9]), postfixTokenCalc(values[10])],
                      [postfixTokenCalc(values[11]), postfixTokenCalc(values[12]), postfixTokenCalc(values[13])]]

    print(f'OOO computed_place = {computed_place}')
    SCplace = scene0.g54_g59_AXIS_Display['G' + current_g_modal['SC']]
    SCplace[8].append(computed_place)
    print(f'SCplace = {SCplace}')
    delataXYZ = [+computed_place[1][0], +computed_place[1][1], +computed_place[1][2]]
    #TODO may be minus should not be here
    euler_angles = np.array([-computed_place[2][0], -computed_place[2][1], -computed_place[2][2]])
    print(f'777 euler_angles = {euler_angles}')
    #rotation = Rotation.from_euler(computed_place[0][-1::-1], euler_angles)

    #euler_angles = np.array([0, 0, 0])
    #print(euler_angles)
    rotation88 = [[1., 0., 0.],
                  [0., 1., 0.],
                  [0., 0., 1.]]
    #rot_mat_rel = np.matmul(np.transpose(r_0), r_1)

    #TODO ПРОБЛЕМА В СЛЕДУЮЩЕЙ СТРОКЕ????
    rotation = Rotation.from_euler(computed_place[0], euler_angles, degrees=True)#[-1::-1]

    #dot_mat_rel = np.matmul(np.transpose(rotation88), rotation.as_matrix())

    delataXYZ2 = [+computed_place[3][0], +computed_place[3][1], +computed_place[3][2]]
    print('rotation88 = ', rotation.as_matrix())
    print('rotation quat = ', rotation.as_quat())
    #transformed_point = np.dot(rotation_matrix, point) + translation_vector
    #np_box.CYCLE800current = [delataXYZ, rotation.as_matrix(), delataXYZ2]#[]#как смещать точки
    current_g_modal['CYCLE800'] = [delataXYZ, rotation.as_matrix(), delataXYZ2]  # []#как смещать точки
    return v_i


