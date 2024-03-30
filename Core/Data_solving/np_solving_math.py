import numpy as np
from Settings.settings import axises, min_ark_step
import copy
import math
import time
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT, DICTshift
from Core.Data_solving.IF_WHILE_REACTIONS import IF_WHILE_what2do
from Settings.settings import algorithmCycleMax
from Gui.little_gui_classes import simple_warning
from Core.Data_solving.added_special_instructions_in_solving import *
from Core.Data_solving.summirizer import vinoska_vremennaya_pod_CYCLE800, trans_matrix_from_SC
from Core.Data_solving.summirizer import G549_4_1_dot, matrixMorty, Morty_matrix_use


def special_options_applying_new(self):  # and Fill visible_np with axises that is None now
    print('special_options_applying_new')

    self.AP = 0
    self.RP = 0
    #print(f'989 main_g_cod_pool = {self.main_g_cod_pool}')
    self.dots_transformation_matrix = np.eye(4)
    self.Morty_matrixis = None




    current_g_modal = copy.copy(self.g_modal_new)
    current_g_modal['CYCLE800'] = None#[1, "", 0., 57, 0., 0., 0., 0., 0., 0., 0., 0., 0., 1, 0., 1]
    print(f'current_g_modal at the start = {current_g_modal}')
    current_vars = self.VARs.PAPAcopy()
    if self.redactor.tab_.center_widget.app.centre.note.currentIndex() == -1:
        m = self.redactor.tab_.center_widget.app.centre.note.default_machine_item
    else:
        m = self.redactor.tab_.center_widget.app.centre.note.currentWidget().current_machine
    self.redactor.current_machine.k_applying(self.visible_np)
    #self.redactor.highlight.reversal_post_processor.k_applying(self.visible_np)  # visible_np
    self.redactor.highlight.reversal_post_processor.Rad_applying(self.visible_np)
    self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.ERROR_lines = []
    if m.axles_DICT['A'] == m.axles_DICT['B'] == m.axles_DICT['C'] is False:
        need_reckon = False
    else:
        need_reckon = True
    #v = self.visible_np
    #v:np.array
    #old_v = np.copy(v)
    CNC_type = self.redactor.highlight.reversal_post_processor.CNC_op_type# 'Siemens_op'
    NshiftCount = 0
    self.special_instruction = []
    self.frame_address_in_visible_pool = np.zeros((0, 2), int)

    last_significant_line = self.visible_np[0]
    #-------------------Подготовка окончена------------------------------

    #сбор параметров для вычислений

    modal_ark = self.redactor.highlight.reversal_post_processor.ARK_modal  # todo точно чинить/ ARK повторяется. Это проблема - ???? А где? не вижу этого
    #siemens_ijk = self.redactor.highlight.reversal_post_processor.siemens_ijk

    self.return_stack = []#[[NstrCommand, LblStart, [LblEnd1, LblEnd2,], P],                    ]
    #self.special_instructions = []
    polar_cur = [0., 0., 0.]

    i = 0
    i_str = 0

    old_v = self.visible_np
    len_v = len(old_v)
    closest_shift = self.SHIFTcontainer.nextSHIFT(i_str, len_v)
    #closest_shift = closest_shift +1
    print('closest_shift start = ', closest_shift)
    #if closest_shift == -1:
    #    closest_shift = len_v


    #cur_v = np.zeros((closest_shift-i_str, axises), float)
    cur_v = np.copy(old_v[i_str:closest_shift+1])

    self.n_h, self.n_v, self.n_p = self.number_hor_vert_perp_from_plane('17')
    #C_AX_center_in_main_G549 = [self.]

    #print('C_AX_center_in_main_G549 = ', C_AX_center_in_main_G549)
    #print('main table99 = ', self.t)
    #print(f'cur_v для первой вставки {cur_v}')
    print(f'i_str = {i_str}, closest_shift = {closest_shift}')
    cur_i = 0
    cur_i_max = closest_shift - i_str
    cur_frame_addresses = create_frame_address_new(self, i_str, cur_i_max, cur_v, i, NshiftCount)
    print(f'4445 cur_frame_addresses = {cur_frame_addresses}')


    scene0 = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL
    for sc in scene0.g54_g59_AXIS_Display:
        #print('sc = ', sc)
        #print('666sc = ',scene0.g54_g59_AXIS_Display[sc])
        scene0.g54_g59_AXIS_Display[sc][6] = False
        scene0.g54_g59_AXIS_Display[sc][7] = []
        scene0.g54_g59_AXIS_Display[sc][8] = []

    #scene0.g54_g59_AXIS_Display[str(current_g_modal['SC'][6])] = True
    main_G549 = scene0.g54_g59_default[1:]
    print(f'here main_G549  = {main_G549 }')
    scene0.g54_g59_AXIS_Display['G' + str(main_G549)][6] = True
    DictG549shift = scene0.g54_g59_AXIS_Delta
    table_m = scene0.table
    head_m = scene0.head
    # попробую обернуть вокруг оси C
    # l1 = table_m[2][1]

    #transf_matrix = np.eye(4)
    self.Morty_matrixis = matrixMorty(dots_transformation_matrix=self.dots_transformation_matrix, machine=self.redactor.current_machine)

    print('main_G549 = ', main_G549)
    print('table_m = ', table_m)
    print('head_m = ', head_m)
    C_axis = 9
    self.new_v = np.zeros((0, axises), float)
    #n4insert = 0
    #n4insert = n4insert + cur_i_max + 1
    # v[:, 17:] = v[:, 4:7] #todo МОЖЕТ БЫТЬ (БЕС)ПОЛЕЗНО ВАРНИНГ БЛЭТ
    # print('special_options_applying array = ', v)
    #I_end_str = 1
    #while i < len_v:
    jumped_here = False
    self.redactor.Logs.math_logs = '\n'
    print(f'self.g54_g59_AXIS_Display = {scene0.g54_g59_AXIS_Display}')
    shiftCount = 0
    CurLineInCurG549Absolute = np.copy(self.visible_np[0])
    PrevLineInCurG549Absolute = np.copy(self.visible_np[0])  # Отк

    print(f'start TTTT cur_i_max = {cur_i_max}')
    #XYZ_IJK_after_moving = np.copy(last_significant_line)
    range_4_update_from_last = tuple(range(4, 10))
    range_4_update_from_last_2 = tuple(range(17, 20))


    while i_str < len_v:
        v_i = cur_v[cur_i]#TODO ????
        if v_i[16] == 7:#заполнять нужно из переменных
            v_i = feed_axis_from_dict(self, v_i, current_vars, PrevLineInCurG549Absolute, current_g_modal, polar_cur, DictG549shift)#, old_v
        if np.isnan(v_i[16]):
            if current_g_modal['polar_coord_16'] == '16' and not (np.isnan(v_i[4]) or np.isnan(v_i[5])) and CNC_type == 'Fanuc_op':
                v_i = self.fanuc_polar_coordinates_16(PrevLineInCurG549Absolute, v_i)
            for c in range_4_update_from_last:
                if np.isnan(v_i[c]):
                    v_i[c] = last_significant_line[c]
            for c in range_4_update_from_last_2:
                if np.isnan(v_i[c]):
                    v_i[c] = v_i[c-13]

                    #v_i[c] = PrevLineInCurG549Absolute[c]
            if current_g_modal['absolute_or_incremental'] == '91':
                v_i = self.relative_coord_option(PrevLineInCurG549Absolute, v_i)  # TODO меняет только 4:6, 10:12
            CurLineInCurG549Absolute = np.copy(v_i[:])  # TODO Вроде не должно влиять НО ВЛИЯЕТ
            print(f'В цикле после появления CurLineInCurG549Absolute  = {CurLineInCurG549Absolute}')

            if current_g_modal['CYCLE800'] is not None or current_g_modal['SC'] != main_G549:
                print(f'44 self.dots_transformation_matrix = \n{self.dots_transformation_matrix}')
                G549_4_1_dot(dot=v_i, trans_matx=self.dots_transformation_matrix)

            if CNC_type == 'Fanuc_op':
                if current_g_modal['polar_coord'] == '112':
                    v_i = self.fanuc_polar_coordinates(PrevLineInCurG549Absolute, v_i)


           #if v_i[9] != 0:  # todo turn_around_C Сейчас скорее всего чего то не то делает. Должен давать XYZ
           #    # координаты для поворота. Надо проверить
           #    v_i[17:20] = turn_around_C(*v_i[4:7], v_i[9])
           #    #CurLineInCurG549Absolute
            #else:
            #    for c in range(17, 20):
            #        v_i[c] = v_i[c - 13]

            print(f'перед дугой v_i = {v_i}')

            if v_i[modal_ark] == 2 or v_i[modal_ark] == 3:  # todo если хотим наследовать, то v[i, 1] Для круговой интерполяции
                #Проверю координаты CurLineInCurG549Absolute и PrevLineInCurG549Absolute
                print(f'В начале работы с дугой я имею:\n CurLineInCurG549Absolute = '
                      f'{CurLineInCurG549Absolute}\nPrevLineInCurG549Absolute = {PrevLineInCurG549Absolute}')

                n_h, n_v, n_p = self.n_h, self.n_v, self.n_p
                if np.isnan(CurLineInCurG549Absolute[13]):  # todo нет R
                    if np.isnan(CurLineInCurG549Absolute[n_h+4]) or np.isnan(CurLineInCurG549Absolute[n_v+4]): # todo и нет ijk
                        if (CurLineInCurG549Absolute[4] == PrevLineInCurG549Absolute[4] # todo и XYZ такие же
                        and CurLineInCurG549Absolute[5] == PrevLineInCurG549Absolute[5]
                        and CurLineInCurG549Absolute[6] == PrevLineInCurG549Absolute[6]):
                            i = i + 1
                            cur_i = cur_i + 1
                            i_str = i_str + 1
                            continue  #todo Тогда пропустить
                        self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.ERROR_lines.extend((PrevLineInCurG549Absolute, v_i))
                        self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{i_str} not enough params for ark\n'
                        i = i + 1
                        cur_i = cur_i + 1
                        i_str = i_str + 1
                        continue  # todo А если координаты новые, а описания дуги нет, то тоже пропустить и ошибку дать
                    else:  # есть ijk, ищем R
                        if np.isnan(CurLineInCurG549Absolute[n_h + 6]) or np.isnan(CurLineInCurG549Absolute[n_v + 6]):
                            (self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.ERROR_lines
                             .extend((PrevLineInCurG549Absolute, v_i)))
                        CurLineInCurG549Absolute[10:13] = CurLineInCurG549Absolute[10:13] + PrevLineInCurG549Absolute[4:7]
                        CurLineInCurG549Absolute[13] = R_from_ijk(CurLineInCurG549Absolute, n_h, n_v, n_p, PrevLineInCurG549Absolute)
                        # print('|||| R = ', v[i, 13])
                else:  # todo Есть R
                    *v_i[10:13], possible = centre_R_ARK(CurLineInCurG549Absolute[modal_ark],
                                                          current_g_modal['plane'],
                                                          PrevLineInCurG549Absolute, CurLineInCurG549Absolute, n_h, n_v, n_p)#self
                    print(f'*v_i[10:13] = {v_i[10:13]}')
                    CurLineInCurG549Absolute[10:13] = v_i[10:13]

                    if not possible:
                        self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.ERROR_lines.extend((PrevLineInCurG549Absolute, v_i))

                # считаем длину вектора
                len_ark = math.sqrt((CurLineInCurG549Absolute[n_h] - PrevLineInCurG549Absolute[n_h]) ** 2 +
                                    (CurLineInCurG549Absolute[n_v] - PrevLineInCurG549Absolute[n_v]) ** 2)
                print('len_ark963  = ', len_ark )
                #if len_ark < min_ark_step:  # todo будет неверно работать для бОльшей дуги экстремально малого радиуса(недорисует)depreveited
                    #last_significant_line = v_i
                    #i = i + 1
                    #i_str = i_str + 1
                    #continue
                #print(f'min_ark_step = {min_ark_step}, len_ark = {len_ark}')
                #______________________________________________________
                if len_ark > min_ark_step:
                    print('tut 759')
                    #current_g_modal
                    #DictG549shift
                    #TODO Нужен способ перенести сюда преобразователь или нет?
                    cur_v, n = self.add_ark_points(cur_v,
                            cur_i, n_h, n_v, n_p, min_ark_step,
                            DictG549shift['G' + current_g_modal['SC']],
                            main_G549, current_g_modal['CYCLE800'],
                            PrevLineInCurG549Absolute,
                            CurLineInCurG549Absolute)

                    ark_np_array = np.zeros((n, 2), int)
                    ark_np_array[:, 1] = i_str
                    ark_np_array[:, 0] = np.arange(cur_i, cur_i+n, dtype=int)
                    cur_frame_addresses[cur_i:, 0] = cur_frame_addresses[cur_i:, 0] + n
                    cur_i_max = cur_i_max +n#-1
                    i = i + n#-1
                    cur_frame_addresses = np.insert(cur_frame_addresses, cur_i, ark_np_array, axis=0)
                    cur_i = cur_i + n #-1
                    #print('i_str сразу после ', i_str)

            # метка для оси С. Нужен универсальный поворот вокруг случайной оси. Потом добавить его для повернутой системы координат

            elif need_reckon and (CurLineInCurG549Absolute[C_axis] != 0 or CurLineInCurG549Absolute[C_axis] !=
                                  PrevLineInCurG549Absolute[C_axis]):
                print(f'CurLineInCurG549Absolute[C_axis] = {CurLineInCurG549Absolute[C_axis]}')
                print(f'PrevLineInCurG549Absolute[C_axis] = {PrevLineInCurG549Absolute[C_axis]}')
                print('need_reckon and v_i[C_axis] != 0')
            #elif need_reckon and v_i[C_axis] != last_significant_line[C_axis]:
                # or v[i, C_axis] != 0)          (v[i, C_axis] is not np.nan or last_significant_line[C_axis] != 0):#is not np.NAN:  # для поворота вокруг С
                #v_i = v[i]

                """for c in range(4, 10):# предположительно не нужно. Похоже на правду
                    if np.isnan(v_i[c]):
                        v_i[c] = last_significant_line[c]
                """

                Morty_matrix_use(coords=v_i, some_matrx=self.Morty_matrixis)
                #v_i[17:] = turn_around_C(v_i[17], v_i[18], v_i[19], v_i[9])  # Это обычный оборот вокруг нуля

                # print('|turn_around_C = ', v_i[17:])

                if False:  # FIXME: ВЫКЛЮЧИЛ ДОБАВЛЕНИЕ ДОПОЛНИТЕЛЬНЫХ ТОЧЕК
                    #n_h, n_v, n_p = self.number_hor_vert_perp_from_plane('17')
                    n_h, n_v, n_p = self.n_h, self.n_v, self.n_p
                    #n_h, n_v, n_p = self.n_h, self.n_v, self.n_p TODO!!
                    R = math.sqrt(v_i[n_h] ** 2 + v_i[n_v] ** 2)
                    v_i[13] = R
                    v_i[10:13] = [0, 0, 0]  # todo переделать
                    #v_i = cur_v[cur_i]
                    #todo i нужно заменить на коунт внутри cur_v и может быть заменить last_significant_line

                    cur_v, n = self.add_ark_axis_points(cur_v, current_g_modal, last_significant_line, cur_i, n_h, n_v, n_p, min_ark_step, main_axis='C', main_G549=main_G549, DictG549shift=DictG549shift)#todo вышибло на ctrl+z, при этом отстуствовали поворотные точки. дичь

                    #todo и ещё раз так же. + заметил что произошло это после смены одного станка на другой.
                    #self.frame_address_in_visible_pool[i_str:] = self.frame_address_in_visible_pool[i_str:] + n#todo frame_address_in_visible_pool возможжно, на помойку
                    #self.frame_address_in_visible_pool[i_str, 0] = self.frame_address_in_visible_pool[i_str, 0] - n
                    ark_np_array = np.zeros((n, 2), int)
                    ark_np_array[:, 1] = i_str
                    ark_np_array[:, 0] = np.arange(cur_i, cur_i + n, dtype=int)
                    cur_frame_addresses[cur_i:, 0] = cur_frame_addresses[cur_i:, 0] + n
                    cur_i_max = cur_i_max + n  # -1
                    i = i + n  # -1
                    cur_frame_addresses = np.insert(cur_frame_addresses, cur_i, ark_np_array, axis=0)
                    cur_i = cur_i + n  # -1
                    #i = i + n
                #else:
                #    pass

        elif v_i[16] == 0:  # direct move type Т Е Вообще не нужная ветка? или доделывать
            print('G28 or something')
            """
            for k in range(4, 10):#предположительно не нужно
                if np.isnan(cur_v[i, k]):
                    cur_v[i, k] = last_significant_line[k]
            """
            #last_significant_line = v[i]
        elif v_i[16] == 1:#g modal type в условиях отдельной строки только. потом нужно будетт поднять
            print('g modal type detected')
            prev_g_modal_90_91 = current_g_modal['absolute_or_incremental']
            print(f'999 self.RP  = {self.RP }')
            prev_g_modal_SC = current_g_modal['SC']
            #prev_g_modal_800 = current_g_modal['CYCLE800']
            print('prev_g_modal_SC 999 = ', prev_g_modal_SC)
            GMcommands, local_line = self.GM_modal_container.return_info(i_str)
            for gm in GMcommands:
                current_g_modal[gm] = GMcommands[gm]
            self.dots_transformation_matrix = trans_matrix_from_SC(G549=DictG549shift['G' + current_g_modal['SC']], C800=current_g_modal['CYCLE800'])
            self.Morty_matrixis = matrixMorty(dots_transformation_matrix=self.dots_transformation_matrix, machine=self.redactor.current_machine)
            ##print(f'1 n_h_prev, n_p_prev  = {n_h_prev, n_p_prev }')
            self.n_h, self.n_v, self.n_p = self.number_hor_vert_perp_from_plane(current_g_modal['plane'])
            print(f'blyaa: ', i_str)
            #if current_g_modal['CYCLE800'] != prev_g_modal_800:
            #    print('cycle800 detected while solving')
            #    #last_significant_line = move_to_main_G549_new(np.copy(last_significant_line), DictG549shift['G' + str(prev_g_modal_SC)])
            #    #last_significant_line = move_from_main_G549222(last_significant_line, DictG549shift['G' + str(current_g_modal['SC'])])
            #    #CurLineInCurG549Absolute = last_significant_line
            #    self.cycle800_AXIS_Display.append(999)
            #    print(f'self.cycle800_AXIS_Display = {self.cycle800_AXIS_Display}')
            #    #scene0.g54_g59_AXIS_Display[sc][8].append([polar_cur, rot_list])
            #    info = self.SHIFTcontainer.return_info(i_str)
            #    print('info = ', info)
            #    #cycle800_cur = feed_siemens_POLAR_from_dict(self, info, current_vars, last_significant_line, current_g_modal, polar_cur, DictG549shift)#main_G549,
            #    #sc = 'G' + str(current_g_modal['SC'])
            #    #if self.n_p == 6:#G17
            #    #    rot_list = [0., 0., 0.]#todo здесь будет иначе
            #    #elif self.n_p == 4:#G19
            #    #    rot_list = [0, -1, 0]
            #    #else:#G18
            #    #    rot_list = [1, 0, 0]
            #    #scene0.g54_g59_AXIS_Display[sc][8].append([cycle800_cur, rot_list])


            scene0.g54_g59_AXIS_Display['G' + str(current_g_modal['SC'])][6] = True
            if prev_g_modal_SC != current_g_modal['SC']:
                #move_from_main_G549222
                #TODO НЕВЕРНЫЙ ПЕРЕНОС
                print(f'стара  кооррдината до: {last_significant_line}')
                #TODO есть смысл вернуть ибо обе использованные СК могут не быть G54
                #prev
                last_significant_line = move_to_main_G549_new(np.copy(last_significant_line), DictG549shift['G' + str(prev_g_modal_SC)])
                print(f'Из кординаты  prev_g_modal_SC = {prev_g_modal_SC}')
                #last_significant_line = move_from_main_G549(last_significant_line, DictG549shift['G' + str(current_g_modal['SC'])])
                print(f'стара  кооррдината: {last_significant_line}')
                last_significant_line = move_from_main_G549222(last_significant_line, DictG549shift['G' + str(current_g_modal['SC'])])
                print(f'стара  кооррдината после: {last_significant_line}')

                polar_cur = [0., 0., 0.]
        elif v_i[16] == 4:
            #print(f'предварительно for next iteration: i = {i}, cur_i = {cur_i}, i_str = {i_str}, cur_i_max = {cur_i_max}')
            info = self.SHIFTcontainer.return_info(i_str)
            #print('1 info = ', info)
            if info[0][2] == DICTshiftsINT['R = ']: #остановился здесь
                #print('3000000')
                #print('current_vars1 = ', current_vars)
                current_vars[info[1][1][0]] = postfixTokenCalc(info[1][2], current_vars, proc=self.redactor.highlight.reversal_post_processor)
                if current_vars[info[1][1][0]] is None:
                    #print('IS NONE')
                    self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'in {i_str} {info[1][1][0]} = None. Wrong expression or devide by zero\n'
                    print(f'current vars fail = {current_vars}')
                #print(f'expression result: {info[1][1][0]} = {current_vars[info[1][1][0]]}')
            elif info[0][2] == DICTshiftsINT['CYCLE800']:
                print(f'solving cyecle800 case')
                CYCLE800_handler(self, current_g_modal, last_significant_line, v_i, info, scene0)
                self.dots_transformation_matrix  = trans_matrix_from_SC(G549=DictG549shift['G' + current_g_modal['SC']], C800=current_g_modal['CYCLE800'])
                self.Morty_matrixis = matrixMorty(dots_transformation_matrix=self.dots_transformation_matrix, machine=self.redactor.current_machine)
            elif info[0][2] == DICTshiftsINT['POLAR']:
                print('polar sim')
                polar_cur = feed_siemens_POLAR_from_dict(self, info, current_vars, last_significant_line, current_g_modal, polar_cur, DictG549shift)#main_G549,
                sc = 'G' + str(current_g_modal['SC'])
                #print(f'scene0.g54_g59_AXIS_Display[sc][7] = {scene0.g54_g59_AXIS_Display[sc][7]}')
                if self.n_p == 6:#G17
                    rot_list = [0., 0., 0.]
                elif self.n_p == 4:#G19
                    rot_list = [0, -1, 0]
                else:#G18
                    rot_list = [1, 0, 0]
                scene0.g54_g59_AXIS_Display[sc][7].append([polar_cur, rot_list])#, self.n_p
                #print(f'22scene0.g54_g59_AXIS_Display[sc][7] = {scene0.g54_g59_AXIS_Display[sc][7]}')
            #elif cur_i_max != cur_i and info[0][2] != DICTshiftsINT['LABEL']:#todo Если я здесь оказался
            #    #todo это значит, что сюда скакнули откуда то ещё и теперь нужно поределиться с дальнейшими действиями
            #    print(f'cur_i_max != cur_i 666')
            #    print(f'info = {info}')

        print(f'Current last significant 50 = {last_significant_line}')
        if cur_i_max == cur_i:
            #print('cur_i_max == cur_i')
            """
            значит, так.  Если набрёл на РИПИТ, или создаём или 
            """

            all_fine = True
            if shiftCount > algorithmCycleMax:
                simple_warning(f'More than {algorithmCycleMax} shifts', f'Change settings or \ncheck for endless cycle')
                self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{i_str} line shift limit excessed\n'
                break
            #cur_i = 0
            if v_i[16] == 4 and info[0][2] in DICTshift:#df
                # todo cur_i ++
                print('7777 here, i_str = ', i_str)
                if info[0][2] == DICTshiftsINT['M30']:
                    break
                #print('seek for last 4')
                NshiftCount = add_frame_address_new(self, NshiftCount, cur_frame_addresses)
                #NshiftCount = add_frame_address(self, i_str, cur_i_max, cur_v, i, NshiftCount) #вот это ниж  добавить и починить
                self.new_v = np.concatenate([self.new_v, cur_v])

                #if info[0][2] == DICTshiftsINT['SUB_PROGRAM']:
                self.last_significant_line4subprograms = last_significant_line#this is for sub_programs
                #print('i before = ', i)
                i_str, jumped_here, i = IF_WHILE_what2do(self, info, current_vars, i_str, jumped_here, i)
                if info[0][2] == DICTshiftsINT['SUB_PROGRAM']:
                    print(f'i returned as {i}')
                    #print(f'cur_i = ', cur_i)
                    #print(f'1 проверочка {self.frame_address_in_visible_pool}')
                #elif

                last_significant_line = self.last_significant_line4subprograms

                #print(f'foooo new_v = {self.new_v}')
                if i_str == None or i_str == len_v:
                    #print('break here11')                    #all_fine = False
                    break
                #print('after: i_str = ', i_str)
                cur_v = np.copy(old_v[i_str:i_str])#len=0, empty: []
                #print(f'strange cur_v = {cur_v}')

                #i = i + 1
                shiftCount = shiftCount + 1
                if old_v[i_str][16] == 4:
                    print(f'1111 i_str = {i_str}, ')
                if old_v[i_str][16] == 4 and self.SHIFTcontainer.return_info(i_str)[0][2] in DICTshift:#jumped_here:
                    #if i_str >= len_v :
                    #    break
                    while i_str < len_v and old_v[i_str][16] == 4 and self.SHIFTcontainer.return_info(i_str)[0][2] in DICTshift:
                        cur_v = np.vstack((cur_v, old_v[i_str:i_str+1]))
                        shiftCount = shiftCount + 1
                        info = self.SHIFTcontainer.return_info(i_str)
                        i_str, jumped_here, i = IF_WHILE_what2do(self, info, current_vars, i_str, jumped_here, i)
                        if i_str is None or i_str < 0:
                            #print('vot tut None')
                            all_fine = False
                            #self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{i_str} aiming for non-existent line\n'
                            break
                        #i = i + 1


                    if all_fine is False: break
                    l_f_c = len(cur_v)

                    cur_frame_addresses = np.zeros((l_f_c, 2), int)
                    cur_frame_addresses[:, 1] = np.copy(cur_v[0:, 15])
                    #cur_frame_address[:, 1] = np.arange(i - l_f_c + 0 + 0 + NshiftCount, i + NshiftCount)
                    #i = i + 1#todo new
                    cur_frame_addresses[:, 0] = np.arange(i - l_f_c + NshiftCount, i + NshiftCount)
                    #print(f'12155 cur i_str {i_str}')
                    #print(f'12155 zdes {cur_frame_addresses}')
                    self.frame_address_in_visible_pool = np.concatenate([self.frame_address_in_visible_pool, cur_frame_addresses])
                    NshiftCount = NshiftCount + l_f_c
                    self.new_v = np.concatenate([self.new_v, cur_v[:]])#-1 было здесь
                    i = i - 1
                    #во первых протестировать строки в готу и остальных циклах.
                    #во вторых починить отслеживание циклов по крусовру.
                    #в третьих дочинить репит, и , возможно подпрограммы
                    #в5х много операторов перехода подряд протестировать с циклами, готу и репитами
                    #в 6тых прикрутить нормальные дуги
                    #i = i - 1
                closest_shift = self.SHIFTcontainer.nextSHIFT(i_str, len_v)

                cur_v = np.copy(old_v[i_str:closest_shift + 1])
                cur_i_max = closest_shift - i_str
                N = np.isfinite(cur_v[:, 2]).nonzero()[0]
                N = -1 if len(N) == 0 else N[0]
                #print('N = ', N)
                #print(f'N type = {type(N)}')
                cur_v[:N, 3] = last_significant_line[3]
                cur_frame_addresses = create_frame_address_new(self, i_str, cur_i_max, cur_v, i, NshiftCount)
                cur_i = 0
                continue

            else:
                #print(f' zdes i_str = {i_str}')

                #todo Придумай как реагировать на это говно

                if len(self.return_stack) != 0:#return on the previous 4type command

                    if self.SHIFTcontainer.np_for_vars[-1][0] >= i_str:
                        #print('return_stack 22 = ', self.return_stack[-1])
                        #print('22 self.SHIFTcontainer.return_info(i_str) = ', self.SHIFTcontainer.return_info(i_str))

                        if self.return_stack[-1][2][0] == self.SHIFTcontainer.return_info(i_str)[1][0]:#TODO REPEAT start
                            self.new_v = np.concatenate([self.new_v, cur_v])
                            shiftCount = shiftCount + 1
                            i_str = self.return_stack[-1][0]

                            #print(f'может проблема здесь {i_str }')
                            if i_str == None:
                                print('break1')
                                break

                            cur_v = np.copy(old_v[i_str:i_str + 0])
                            if old_v[i_str][16] == 4 and self.SHIFTcontainer.return_info(i_str)[0][2] in DICTshift:  # jumped_here:


                                while old_v[i_str][16] == 4 and self.SHIFTcontainer.return_info(i_str)[0][2] in DICTshift:
                                    #print(f'while old_v[i_str][16] == 4 cycle...')
                                    endenc = cur_frame_addresses[-1][0]
                                    cur_frame_address__ = np.array([[(endenc) + 1, i_str + 0]])
                                    cur_frame_addresses = np.concatenate([cur_frame_addresses, cur_frame_address__])

                                    cur_frame_addresses[:, 0] = cur_frame_addresses[:, 0] - 1
                                    cur_v = np.concatenate([cur_v, old_v[i_str:i_str + 1]])
                                    shiftCount = shiftCount + 1
                                    info = self.SHIFTcontainer.return_info(i_str)

                                    i_str, jumped_here, i = IF_WHILE_what2do(self, info, current_vars, i_str, jumped_here, i)


                                    if i_str == None:
                                        all_fine = False
                                        break
                                    i = i + 1
                                    #print(f'22 i = {i}')
                                if all_fine is False:
                                    break
                                l_f_c = len(cur_v)
                                #cur_frame_address = np.zeros((l_f_c, 2), int)
                                #cur_frame_address[:, 0] = np.copy(cur_v[0:, 15])
                                #cur_frame_address[:, 1] = np.arange(i - l_f_c + 0 + 0 + NshiftCount, i + NshiftCount)
                                #print('seek for last 5')
                                NshiftCount = add_frame_address_new(self, NshiftCount, cur_frame_addresses)


                                #self.frame_address_in_visible_pool = np.concatenate([self.frame_address_in_visible_pool, cur_frame_address])
                                #NshiftCount = NshiftCount + l_f_c
                                self.new_v = np.concatenate([self.new_v, cur_v[:]])  # -1 было здесь
                                i = i - 1
                                #print(f'333 i = {i}')



                            closest_shift = self.SHIFTcontainer.nextSHIFT(i_str, len_v)
                            cur_v = np.copy(old_v[i_str:closest_shift + 1])
                            cur_i_max = closest_shift - i_str
                            #print(f'вот это метсто44')
                            cur_frame_addresses = create_frame_address_new(self, i_str, cur_i_max, cur_v, i, NshiftCount)
                            #if len(self.return_stack) == 0 or self.return_stack[-1][2][0] != self.SHIFTcontainer.return_info(i_str)[1][0]:
                            #    #if
                            #    #add_cur_dognail = np.array([[,],[]])
                            #    pass
                            #    #cur_frame_addresses = np.concatenate(np.array([,]), cur_frame_addresses)

                            cur_i = 0
                            print('курва = ', cur_v)
                            continue#REPEAT end
        print(f'Current last significant 60 = {last_significant_line}')
        i = i + 1
        #print(f'444 i = {i}')
        #self.frame_address_in_visible_pool[:,0] = np.arange(len(self.frame_address_in_visible_pool))
        cur_i = cur_i + 1
        i_str = i_str + 1

        if np.isnan(v_i[16]) or v_i[16] == 2 or v_i[16] == 0:
        #if np.isnan(v_i[16]) or v_i[6] == 2 or v_i[6] == 0:# or forsed_last_coord_update:#todo need to check why
            #last_significant_line = CurLineInCurG549Absolute
            #SMENIL
            #last_significant_line = XYZ_IJK_after_moving
            last_significant_line = cur_v[cur_i-1]
            print(f'CurLineInCurG549Absolute  check2 ='
                  f' {CurLineInCurG549Absolute}')
            PrevLineInCurG549Absolute = CurLineInCurG549Absolute[:]
            print(f' Постфактум присваиваем PrevLineInCurG549Absolute = {PrevLineInCurG549Absolute}')

        print(f'Current last significant 70 = {last_significant_line}')
        #if forsed_last_coord_update:
        #    forsed_last_coord_update = False
        #    print('C axis = ', v_i)
        #    last_significant_line = v_i
        print(f'for next iteration: i = {i}, cur_i = {cur_i}, i_str = {i_str}, cur_i_max = {cur_i_max}')


    print(f'GGG cur_i_max = {cur_i_max}, cur_i = {cur_i}, v_i[16] = {v_i[16]}')
    if cur_i_max <= cur_i:#-0: #and v_i[16] != 4: todo вернуть, наверное
        #print('555 cur_v = ', cur_v)
        print('555 v_i = ', v_i)
        #print(f'121 cur_frame_addresses = {cur_frame_addresses}')
        #closest_shift = self.SHIFTcontainer.nextSHIFT(i_str, len_v)  # todo + 1
        #NshiftCount = add_frame_address(self, i_str-1, cur_i_max, cur_v, i-1, NshiftCount)  # todo + 1
        #print(f'cur frame')

        NshiftCount = add_frame_address_new(self, NshiftCount, cur_frame_addresses)


        self.new_v = np.concatenate([self.new_v, cur_v])
    print('last v_i = ', v_i)
    #print(f'cur_v at the end {cur_v}')
    print('закидываю i_str = ', i_str)

    #closest_shift = self.SHIFTcontainer.nextSHIFT(i_str, len_v)
    print('Получаю closest_shift = ', closest_shift)
    #print('итог new_v = ', new_v)
    self.last_significant_line4subprograms = last_significant_line
    self.visible_np = self.new_v
    #print('self.visible_np = ', self.visible_np)

    self.redactor.editor.after_solving = True
    self.current_vars_dict = current_vars
    if self.redactor.father_np_box is None:
        self.redactor.choose_Logs_or_progress_show(logs_s=True)
        self.redactor.Logs.LogsAlarm()
    #else:
        #self.redactor.father_np_box.redactor.editor.rehighlightNextBlocks()#TODO может добавить сюда иные функции
        #if self.redactor.sub1:
        #    print('дичь4')
        #    self.redactor.sub1 = False
        #    self.redactor.father_np_box.special_options_applying()


if __name__ == "__main__":
    pass
    #import code2flow
#
    #code2flow    Core/Data_solving/np_solving_math.py
