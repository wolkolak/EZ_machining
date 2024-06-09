from Settings.settings import axises, min_ark_step
from left_zone.ARK_solving import *
from Settings.settings import MaxSubProgramsInProject
import math
#from left_zone.bring_coords_to_main_G549 import move_to_main_G549
from Core.Data_solving.VARs_SHIFTs_CONDITIONs import vars_container
from Core.Data_solving.new_G_MODAL_DICT import DICT_with_papa
import copy
import time
from Redactor.useful_things4redactor import find_last_in_block
from Gui.little_gui_classes import simple_warning
from Core.Data_solving.np_solving_math import special_options_applying_new
#def rotate_np1(points, origin, angle):
#    return (points - origin) * np.exp(complex(0, angle)) + origin
import scipy
#from Core.Data_solving.summirizer import CYCLE800_4_many_dots, curentSC_4_many_dots_old
from Core.Data_solving._3D_geometry_SC_moves import my_transform, my_transform_R_T, projection, my_transform_return, C_ROT_1
from Core.Machine_behavior.machine_transmigrations_forward import R_C, R_C_radians

from Redactor import redactor
from Core.Data_solving.summirizer import G549_4_many_dots_NEW  # RT_ABC_many_dots

#def rotate_np(point, origin, degrees):
#    radians = np.deg2rad(degrees)
#    x,y = point
#    offset_x, offset_y = origin
#    adjusted_x = (x - offset_x)
#    adjusted_y = (y - offset_y)
#    cos_rad = np.cos(radians)
#    sin_rad = np.sin(radians)
#    qx = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
#    qy = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
#    return qx, qy

#def turn_around_radians(h, v, angle, p, five):
#    h_new = h * math.cos(angle) - v * math.sin(angle)
#    v_new = h * math.sin(angle) + v * math.cos(angle)
#    return h_new, v_new, p, five

def turn_around_radians1(h, v, angle):
    h_new = h * math.cos(angle) - v * math.sin(angle)
    v_new = h * math.sin(angle) + v * math.cos(angle)
    return h_new, v_new#, p, five

#def turn_around_radians_around_dot(h, v, angle):
#    h_new = h * math.cos(angle) - v * math.sin(angle)
#    v_new = h * math.sin(angle) + v * math.cos(angle)
#    return h_new, v_new#, p, five



def turn_around_radians2(h, v, angle):
    h_new = h * math.cos(angle) - v * math.sin(angle)
    v_new = h * math.sin(angle) + v * math.cos(angle)
    return h_new, v_new, math.degrees(angle)#, p, five


def rotate_around_dot(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    print(f'rotate_around_dot = {origin}|{point}|{angle}')
    #dfsdfsd
    ox, oy = origin
    px, py = point
    #ox = ox * -1

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    print(f'qx = {qx}, qy= {qy}')
    return qx, qy

def turn_around_C_dots(ark_np_array, last_significant_line,  center, n, starting_angle, alpha_segmenta, pp, perp_step, n_p_new):
    #alpha = math.radians(alpha_C)
    print('we are at 70')
    #Rc = math.sqrt(ark_np_array[n-1, 4] **2 + ark_np_array[n-1, 5] **2)
    resulting_angle_C = alpha_segmenta * 1 + starting_angle

    #center[0] = 200
    #center[1] = -500

    for k in range(n):
        resulting_angle_C = alpha_segmenta * k + starting_angle
        ark_np_array[k, 17], ark_np_array[k, 18] = rotate_around_dot(origin=center[0:2], point=last_significant_line[4:6], angle=resulting_angle_C)
        ark_np_array[k, n_p_new] = pp + k * perp_step
        ark_np_array[k, 16] = 5.
    return ark_np_array#, resulting_angle_C#current_line








class NumpyBox():
    """
    class for all numpy objects required for updating 3dModel by changed parts
    """
    def __init__(self, redactor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.redactor = redactor
        print('NumpyBox new')
        self.VARs = DICT_with_papa(self)
        #self.VARs_global =
        self.CUR_PROC = self.redactor.highlight.reversal_post_processor
        self.brackets = self.CUR_PROC.brackets

        reading_lines_number = redactor.reading_lines_number
        self.current_g_cod_pool = np.zeros((reading_lines_number, axises), float)
        #self.redactor.editor.after_rehighlight = False#TODO True
        self.special_instructions = []
        self.sub_programs_dict = {}
        self.calcs_ON = True
        self.current_vars_dict = {}
        self.SUB_exchange_DATA = []#False1 - Переменные не возвращаем
        #self.CYCLE800current = []

        #self.repeat_solving = False#this is for sub programs. It need time to highlight itself

        #self.current_visible_np = np.zeros((reading_lines_number, axises), float)
        self.create_main_and_visual_in_NP(reading_lines_number)
        self.enable_NP_BOX_in_current_HL_Syntax()
        #self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL
        self.return_stack = []
        self.g_modal_new = DICT_with_papa(self)#todo заполнить из постпроцессора
        G_M = self.redactor.highlight.reversal_post_processor.G_MODAL_DICT_in_proc

        for gm in G_M:
            self.g_modal_new[gm] = G_M[gm]

        self.g_modal_new['SC'] = self.redactor.current_machine.current_g54_g59[1:]
        print(f'____________self.g_modal_new = {self.g_modal_new}')
        print(f'G_M = {G_M}')

        #print('проверочка ', self.redactor.highlight.reversal_post_processor.brackets)
        VARSproc = self.redactor.highlight.reversal_post_processor.DICT_VARS
        for v in VARSproc:
            self.VARs[v] = VARSproc[v]
        #проверить заполняемость верхними двумя циклами
        #self.main_g_cod_pool_len = len(self.main_g_cod_pool)
        #self.last_edited_G0_G1 = 0
        #self.before_edited_G0_G1 = 0
        #self.len_str = 0#len(self.main_g_cod_pool)
        print('G_M = ', G_M)
        print('vars in dict = ', VARSproc)
        print(f'после init main_g_cod_pool = {self.main_g_cod_pool}')


    def create_main_and_visual_in_NP(self, reading_lines_number):
        #self.current_SHIFT_list = []
        print('create_main_and_visual_in_NP')
        self.visible_np = np.zeros((1, axises), float)
        self.main_g_cod_pool = np.zeros((1, axises), float)
        self.SHIFTcontainer = vars_container.ShiftContainer(self)
        self.XYZvars_container = vars_container.XYZ_vars_container(self)
        self.GM_modal_container = vars_container.GM_modal_container(self)

        #self.frame_address_in_visible_pool = np.zeros((reading_lines_number + 1, 2), int)
        self.frame_address_in_visible_pool = np.zeros((1, 2), int)
        #self.frame_address_in_visible_pool[0, :] = [0, 0]
        #h, w = self.frame_address_in_visible_pool.shape#todo лишнее же
        #self.frame_address_in_visible_pool[:, 0] = np.arange(1, 1 + h)
        #self.frame_address_in_visible_pool[:, 1] = np.arange(1, 1 + h)

        self.current_g_cod_pool[:] = np.nan

        self.visible_np[:] = np.nan
        self.main_g_cod_pool[:] = np.nan
        #self.main_g_cod_pool.re
        print(f'после создания main_g_cod_pool = {self.main_g_cod_pool}')

    def enable_NP_BOX_in_current_HL_Syntax(self):
        #print('ENABLE')
        self.redactor.highlight.current_g_cod_pool = self.current_g_cod_pool
        #self.redactor.highlight.remember_np_box_parts(self.current_g_cod_pool)

    def create_new_currents_in_np_box(self, axis):
        print('create_new_currents_in_np_box')
        #self.current_SHIFT_list = []
        self.current_g_cod_pool = np.zeros((self.redactor.reading_lines_number, axis), float)
        self.current_g_cod_pool[:] = np.nan



    def propagate_np_box_starting_points(self):
        self.main_g_cod_pool = np.insert(self.main_g_cod_pool, 0, self.main_g_cod_pool, axis=0)



    def add_sub_programs(self, p_name:str):
        print(f'p_name = {p_name}')

        p_name = p_name.lower()
        print(type(p_name))
        if p_name not in self.sub_programs_dict:
            try:
                #print(f'check ehere 33 = {self.redactor.highlight.sub_programs}')
                path = self.redactor.highlight.sub_programs[p_name]
                text = open(path).read()
                self.sub_programs_dict[p_name] = redactor.ParentOfMyEdit(text, existing=False, tab_=self.redactor.tab_, father_np_box=self)
            except BaseException:
                simple_warning('warning', "Файл подпрограммы не открывается \n ¯\_(ツ)_/¯ ")

    def add_line_in_new_tab(self):
        #print('add_line_in_new_tab')
        self.visible_np = np.append(self.visible_np, self.visible_np, axis=0)
        self.visible_np[1, :] = np.nan
        self.visible_np[1, 15] = 1
        self.redactor.tab_.center_widget.left.update_visible_np_left()

    def offset_point(self):
        #print('offset_point')
        self.offset_pointXYZ = [self.redactor.current_machine.offset_pointXYZ[i] *
                               self.redactor.current_machine.k_XYZABC[n] for i, n in zip(range(6), 'XYZ')]
        self.new_np_line = [None, None, 0, 0, *self.offset_pointXYZ, 0., 0., 0., None, None, None, None, None, 0, None, *self.offset_pointXYZ[0:3]]#N100_G40 _G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type_   может ещё RealX_RealY_RealZ
        self.last_significant_line4subprograms = self.current_g_cod_pool[0].copy()
        self.visible_np[0] = self.new_np_line[:]
        self.main_g_cod_pool[0] = self.new_np_line[:]


    def delete_lines_from_np_box(self):
        #2/0
        print('delete_lines_from_np_box: {}\n_________________'.format(self.main_g_cod_pool))
        min_L = self.redactor.editor.min_line_np
        max_L = self.redactor.editor.second_place
        self.redactor.highlight.previous_block_g = self.main_g_cod_pool[min_L-1][3] if min_L > 0 else 0

        #self.before_edited_G0_G1 = self.visible_np[self.frame_address_in_visible_pool[int(self.main_g_cod_pool[self.redactor.highlight.previous_block_g][15])][0]][1]

        #if self.after_rehighlight:
        #    n = max_L- min_L
        #    if n < 5:
        #        print('n<5')
        #        print(f'99 self.main_g_cod_pool[min_L:max_L+1] = {self.main_g_cod_pool[min_L:max_L+1]}')
        #        self.last_edited_G0_G1 = find_last_in_block(self.main_g_cod_pool[min_L:max_L+1], max_L-min_L)
        #    else:
        #        self.last_edited_G0_G1 = False
        #else:
        #    self.last_edited_G0_G1 = False
        #self.last_edited_G0_G1 = last_G1_G0

        #self.last_edited_G0_G1 = self.main_g_cod_pool[max_L][3]#todo а если это не типовая строка?

        #print(f'99 self.last_edited_G0_G1 = {self.last_edited_G0_G1}')
        self.main_g_cod_pool = np.delete(self.main_g_cod_pool, np.s_[min_L:max_L + 1], axis=0)#here
        self.SHIFTcontainer.delete_slice(n_min=min_L, n_max=max_L)
        self.XYZvars_container.delete_slice(n_min=min_L, n_max=max_L)
        self.GM_modal_container.delete_slice(n_min=min_L, n_max=max_L)
        #self.frame_address_in_visible_pool.delete_slice(n_min=min_L, n_max=max_L)
        print('after delete: ', self.main_g_cod_pool)
        print('______')
        print(f'D shifter = {self.SHIFTcontainer}')

    def inserting_current_in_main(self, min_line):
        print('inserting_current_in_main')
        #print('before inserting: ', self.main_g_cod_pool)
        #min_line = min_line + 1000
        self.main_g_cod_pool = np.insert(self.main_g_cod_pool, min_line, self.current_g_cod_pool, axis=0)
        n_new_lines = len(self.current_g_cod_pool)
        m = len(self.main_g_cod_pool)
        if self.redactor.father_np_box is None:
            self.main_g_cod_pool[0:, 15] = np.arange(0, m)
        else:
            ooo = self.redactor.tab_.currentWidget().subNstart
            self.main_g_cod_pool[0:, 15] = np.arange(0 + ooo, m + ooo)  # todo Можно сделать лучше? Не факт, что быстрее будет
        highlight = self.redactor.highlight
        self.SHIFTcontainer.condition_inserter(highlight.current_SHIFT_list, min_line, n_new_lines)#min_line
        self.XYZvars_container.condition_inserter(highlight.current_XYZvars_dict, min_line, n_new_lines)
        self.GM_modal_container.condition_inserter(highlight.GM_current_list, min_line, n_new_lines)
        self.redactor.highlight.reset_current_containers()
        self.visible_np = self.main_g_cod_pool.copy()#todo может убрать ниже под if?
        print('99after inserting: ', self.main_g_cod_pool)
        #print(f'I shifter = {self.SHIFTcontainer}')

    def special_options_applying(self):
        print('special_options_applying in npp_box')

        if self.redactor.father_np_box is None:
            #self.redactor.tab_.currentWidget().len_str = len(self.main_g_cod_pool)
            self.redactor.tab_.currentWidget().all_subs_count = 0
        elif self.redactor.tab_.currentWidget().all_subs_count > MaxSubProgramsInProject:
            self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'Subprograms count in project(>{MaxSubProgramsInProject})\n'
            return
        if self.calcs_ON:
            #self.cycle800_AXIS_Display = []
            special_options_applying_new(self)
        self.redactor.tab_.center_widget.left.update_visible_np_left()

        if self.redactor.sub1 and len(self.main_g_cod_pool) > 1:  # TODO это наверняка неверно
            print('дичь45')
            lowest = True
            for sub_name in self.sub_programs_dict:
                if len(self.sub_programs_dict[sub_name].np_box.main_g_cod_pool) == 1:
                    lowest = False

                    print(f'Искомое общее: {self.redactor.tab_.currentWidget()}')
                    break
            if lowest:
                print(self.main_g_cod_pool)
                self.redactor.sub1 = False
                self.redactor.father_np_box.visible_np = self.redactor.father_np_box.main_g_cod_pool.copy()
                self.redactor.father_np_box.special_options_applying()
        #scene0 = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL
        #print(f'333scene0.g54_g59_AXIS_Display[sc][7] = {scene0.g54_g59_AXIS_Display[sc][7]}')
        self.redactor.editor.highlightCurrentLine_chooseNewDot()

    def add_ark_axis_points(self, cur_v, current_g_modal, last_significant_line, cur_i, n_h, n_v, n_p, min_ark_step, main_axis=None, main_G549=None, DictG549shift=None):
        # todo https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        """We need variable R, because simple ark would be wrong"""
        #пока что просто для оси С
        np_line = cur_v[cur_i]
        # предыдущие данные
        #ph = last_significant_line[n_h]  # previous horizontal
        #pv = last_significant_line[n_v]  # previous vertical
        pp = last_significant_line[n_p]  # previous perpendicular
        #ch = n_h + 6
        #cv = n_v + 6

        n_h_new = n_h + 13
        n_v_new = n_v + 13
        n_p_new = n_p + 13

        # 1 vectors
        #OAx = ph - np_line[ch]#todo need?
        #OAy = pv - np_line[cv]#todo need?

        #ph_corr = last_significant_line[n_h]#13
        #pv_corr = last_significant_line[n_v]#13
        #pp = last_significant_line[n_p]
        #TODO looking for machine_C_center
        print(f'{current_g_modal}')
        sc = 'G' + str(current_g_modal['SC'])
        scene0 = self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL

        machine_center = copy.copy(scene0.g54_g59_AXIS_Display[sc])#TODO только для текущей СК

        machine_center[3:6] = [math.radians(dd) for dd in machine_center[3:6]]
        m = self.redactor.current_machine
        center_AX1 = np.zeros(6)#C Axis
        m0 = np.zeros(6)
        m0[1] = m.DICT_AX_PARAMETERS['C']['LShoulder']
        print(f"m.DICT_AX_PARAMETERS['C']['t_angle'] = {m.DICT_AX_PARAMETERS['C']['t_angle']}")
        m0[3:6] = [math.radians(dd) for dd in m.DICT_AX_PARAMETERS['C']['t_angle']]

        #m0[3] = -m0[3];        m0[4] = -m0[4];        m0[5] = -m0[5]
        print(f'm0 = {m0}')
        #print()
        machine_center_now = my_transform(from_SC=center_AX1, to_SC=m0)
        #остановился здесь

        print(f'8890 machine_center= {machine_center}')

        print(f'8891 machine_center_now = {machine_center_now}')
        machine_center_now = my_transform(from_SC=machine_center_now, to_SC=machine_center)#верно работает

        machine_center_now_return = [-m for m in machine_center_now]
        #todo Это всё можно сделать !ОДИН! раз. То что ниже делаем постоянно
        print(f'777 point = {machine_center_now}')
        print(f'vvv 7 machine_center_now_return = {machine_center_now_return}')
        #https://scask.ru/a_book_mm3d.php?id=60
        #https://ychebnikkompgrafblog.wordpress.com/2-7-%D0%BF%D0%BE%D0%B2%D0%BE%D1%80%D0%BE%D1%82-%D0%B2%D0%BE%D0%BA%D1%80%D1%83%D0%B3-%D0%BF%D1%80%D0%BE%D0%B8%D0%B7%D0%B2%D0%BE%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9-%D0%BE%D1%81%D0%B8-%D0%B2-%D0%BF%D1%80/
        #todo сейчас я перенесу текущую точку в СК с данными machine_center_now

        np_line_const = np.copy(np_line)

        np_line[7] = 0#math.degrees(np_line[7])
        np_line[8] = 0#math.degrees(np_line[8])#TODO можно отдельную функцию написать под радианы/градусы. Заодно лишние переменные убрать
        np_line[9] = 0#math.degrees(np_line[9])
        print(f'между тем np_line было равно {np_line}')
        new_coord_const = my_transform(from_SC=np_line[4:10], to_SC=machine_center_now)#machine_center_now нужны радианы по идее
        #new_coord_const = my_transform_new(from_SC=np_line[4:7], to_SC=machine_center_now)
        print(f'2 между тем np_line было равно {np_line}')
        #new_coord_const = list(new_coord_const)
        print(f'779  point in  {machine_center_now} would be {new_coord_const}')



        new_coord_const[3] = np_line_const[7]
        new_coord_const[4] = np_line_const[8]
        new_coord_const[5] = np_line_const[9]
        p_ = np.zeros(9)
        #p_[8] = math.degrees(np_line_const[9])  # 180#TODO Надо подумать, но позже/ Здесь только С получается
        p_[8] = np_line_const[9]

        print(f'*33** p_ = {p_}')
        print(f'np_line = {np_line}')
        new_coord = R_C_radians(p_, new_coord_const[0], new_coord_const[1], new_coord_const[2],)#radians
        #new_coord = list(new_coord)
        new_coord = [*new_coord, 0, 0, 0]
        print(f'791  point in  {machine_center_now} would be {new_coord}, type = {type(new_coord)}')
        #TODO дальше сместить
        #куда?
        print(f'machine_center_now_return = {machine_center_now_return}')
        #machine_center_now_return[3] = -machine_center_now_return[3]
        #если это итоговая координата, то она пока не нужна.
        coord_in_base = my_transform_return(from_SC=new_coord, to_SC=machine_center_now)
        #cur_v[-1][17:20] = coord_in_base
        np_line[17:20] = coord_in_base
        np_line[7:10] = np_line_const[7:10]

        #np_line[7] = np_line_7
        #np_line[8] = np_line_8
        #np_line[9] = np_line_9
        #machine_center_now_return =

        print('Итоговая координата равна ', coord_in_base)
        print('cur_v[-1] = ', cur_v[-1])
        print('np_line   = ', np_line)
        #g54_dict = g54_g59_AXIS[current_g_modal['SC']][8]
        #g54_g59_AXIS
        print(f'main_G549 = {main_G549}')
        main_SC_coord = DictG549shift['G' + str(main_G549)]
        print(f'main_SC_coord = {main_SC_coord}')
        main_G549_ANGLES = False if (machine_center_now[3] == 0 and machine_center_now[4] == 0 and machine_center_now[5] == 0) else True
        if main_axis == 'C':
            # todo возможно получается однобоко. ибо для2х осей и более это не подойдёт. вроде.
            #if current_g_modal['SC'] == main_G549  and current_g_modal['CYCLE800'] is None:  # and main_G549_ANGLES
            delta = cur_v[cur_i, 9] - last_significant_line[9]  # уже в радианах
            delta_plus = abs(delta)  # радианы
            #TODO НЕТ
            all_rounds_plus = math.floor(delta_plus / 2 / math.pi) * 2 * math.pi
            alpha = delta_plus - all_rounds_plus
            if delta_plus == 0:
                print('ПОЛУНДРА БЛЭТ!')
                if np_line[9] != 0:
                    return cur_v, 0
            elif delta_plus >= 2 * math.pi:
                alpha_segmenta = math.radians(15)
                n = math.floor(all_rounds_plus / alpha_segmenta)  # alpha_segmenta plus
                n = n + math.floor(alpha / alpha_segmenta)
            elif delta_plus < 0.035:
                alpha_segmenta = delta_plus / 5
                print('alpha_segmenta = ', alpha_segmenta)
                n = math.floor(alpha / alpha_segmenta)
            else:
                alpha_segmenta = math.radians(8)
                n = math.floor(alpha / alpha_segmenta)
            #n = n - 1  # todo ???? может вернуть ради двойных краев движений? чтобы цвета не сбивались
            ark_np_array = np.full((n, axises), np_line)
            print(f'007 np_line = {np_line}')
            Lperp = cur_v[cur_i, n_p] - last_significant_line[n_p]
            k_by_step = alpha_segmenta / delta_plus  # math.radians(delta_plus)
            perp_step = Lperp * k_by_step
            #Vstep = Vprep * k_by_step
            #Hstep = Hprep * k_by_step
            prev_alpha = last_significant_line[9]  # math.radians(last_significant_line[9])
            pp = pp + perp_step
            print(f'|||last_significant_line = {last_significant_line}')
            print(f'|||np_line = {np_line}')
            x_step = (np_line[4] - last_significant_line[4])/n
            y_step = (np_line[5] - last_significant_line[5])/n
            z_step = (np_line[6] - last_significant_line[6])/n
            print(f'y_step = {y_step}')
            print('delta = ', delta)
            starting_angle = prev_alpha - alpha_segmenta
            if delta <= math.pi:
                #if x_step == y_step == z_step == 0:
                print('starting_angle = ', starting_angle)
                ark_np_array = C_ROT_1(np_line, ark_np_array, n, alpha_segmenta, starting_angle, p_, x_step, y_step, z_step, new_coord_const,
                                       machine_center_now, last_significant_line)
            else:
                print('Альтернативно')
                ark_np_array = turn_around_C_dots(ark_np_array, last_significant_line, machine_center_now, n, starting_angle, alpha_segmenta, pp,
                                             perp_step, n_p_new)
            print(f'-__cur_v = {cur_v}')



            return np.insert(cur_v, cur_i, ark_np_array, axis=0), n



            #    #без преобразований вращения
            #elif current_g_modal['SC'] == main_G549 and main_G549_ANGLES: #current_g_modal['CYCLE800'] HERE
            #    pass
            #elif current_g_modal['SC'] != main_G549 and current_g_modal['CYCLE800'] is None:#G55 и всё
            #    pass
            #elif current_g_modal['SC'] != main_G549 and main_G549_ANGLES :#G54 но она повернута
            #    pass
            #elif current_g_modal['SC'] != main_G549 :#G54 чисто
            #    pass


            #delta = cur_v[cur_i, 9] - last_significant_line[9]#уже в радианах
            #delta_plus = abs(delta)#радианы
            #cur_v[-1][17], cur_v[-1][18] = rotate_around_dot(origin=machine_center_now[0:2], point=last_significant_line[4:6], angle=delta_plus)
            ##TODO Что если вращать вокруг вектора  777 point = [200. -502.75 -78.49 -45. 0. 0.]
            ##Rotation = scipy.spatial.transform.Rotation
            ##Rotation.as_rotvec()




            #cur_v[-1][17:20] = rotation.apply(cur_v[-1][17:20])
            #all_rounds_plus = math.floor(delta_plus/360) * 360
            ##all_rounds_plus = math.floor(delta_plus / 2 / math.pi) * 2 * math.pi
            ##alpha = delta_plus - all_rounds_plus
            ##if delta_plus >= 2 * math.pi:
            ##    alpha_segmenta = math.radians(15)
            ##    n = math.floor(all_rounds_plus/alpha_segmenta) #alpha_segmenta plus
            ##    n = n + math.floor(alpha / alpha_segmenta)
            ##elif delta_plus < 0.035:
            ##    alpha_segmenta = delta_plus/5
            ##    n = math.floor(alpha / alpha_segmenta)
            ##else:
            ##    alpha_segmenta = math.radians(8)
            ##    n = math.floor(alpha / alpha_segmenta)
            ##n = n - 1#todo ???? может вернуть ради двойных краев движений? чтобы цвета не сбивались
            #n = n + 20
            #ERROR todo
            #alpha_segmenta = math.radians(1)
            #n = math.floor(alpha / alpha_segmenta)
            #print('#ERROR todo, n = ', n)
            ##ark_np_array = np.full((n, axises), np_line)
            # создаем массив
            ##Lperp = cur_v[cur_i, n_p] - last_significant_line[n_p]
            ##Vprep = cur_v[cur_i, n_v] - last_significant_line[n_v]
            ##Hprep = cur_v[cur_i, n_h] - last_significant_line[n_h]
            ##k_by_step = alpha_segmenta / delta_plus#math.radians(delta_plus)
            ##perp_step = Lperp * k_by_step
            ##Vstep = Vprep * k_by_step
            ##Hstep = Hprep * k_by_step
            ##prev_alpha = last_significant_line[9]#math.radians(last_significant_line[9])
            #ph_corr = ph_corr + Hstep
            #pv_corr = pv_corr + Vstep
            ##pp = pp + perp_step
            ##    #херня
            ##if delta < 0:
            ##    starting_angle = prev_alpha -alpha_segmenta
            ##    for k in range(n):
            ##        resulting_angle = -alpha_segmenta*k+starting_angle
            ##        #ark_np_array[k, n_h_new], ark_np_array[k, n_v_new] = turn_around_C_dots(ph_corr + Hstep*k, pv_corr + Vstep*k, resulting_angle, machine_center_now)
            ##        ark_np_array[k] = turn_around_C_dots(ark_np_array[k], last_significant_line, machine_center, n,)
            ##        #(ark_np_array, last_significant_line, center, n, starting_angle, alpha_segmenta, pp, perp_step, n_p_new)
            ##        ark_np_array[k, n_p_new] = pp + k * perp_step
            ##        ark_np_array[k, 16] = 5.
            ##        ark_np_array[k, 9] = math.degrees(resulting_angle)
            ##else:
            ##    starting_angle = prev_alpha + alpha_segmenta
            ##    print('this part working')
            ##    print('machine_center_now = ', machine_center_now)
            ##    ark_np_array = turn_around_C_dots(ark_np_array, last_significant_line, machine_center_now, n, starting_angle, alpha_segmenta, pp, perp_step, n_p_new)
            ##    #print("--- %s seconds ---" % (time.time() - start_time)) 5% slower than one line
        ##else:
        ##    print('redactor add_ark_points failed')
        #хз с шахматами вчего то забыл
        ##print(f'-__cur_v = {cur_v}')
        ###cur_v[-1] =
        ##return np.insert(cur_v, cur_i, ark_np_array, axis=0), n


    #def fanuc_polar_coordinatesOLD(self, last_significant_line, v, n_line): #просто стол станка буду поворачивать в это же время
    #    #FOR XY: Y->C
    #    print('fanuc_polar_coordinates')
    #    print('last_significant_line[9] = ', last_significant_line[9])
    #    new_line = v[n_line]
    #    new_line[5] = new_line[9]
    #    new_line[18] = new_line[9]
    #    for k in range(17, 20):
    #        if np.isnan(new_line[k]):
    #            new_line[k] = last_significant_line[k]
    #    new_line[16] = 7
    #    new_i = n_line
    #    return v, new_i

    #def siemens_polar_coordinates(self, last_significant_line, v_i, polar_cur,  ):
    #    print('siemens_polar_coordinates')
    #    return v_i


    def fanuc_polar_coordinates(self, last_significant_line, v_i): #просто стол станка буду поворачивать в это же время
        #FOR XY: Y->C
        print('fanuc_polar_coordinates')
        #self.polar_cur
        print('last_significant_line[9] = ', last_significant_line[9])
        #new_line = v[n_line]
        v_i[5] = v_i[9]
        v_i[18] = v_i[9]
        for k in range(17, 20):
            if np.isnan(v_i[k]):
                v_i[k] = last_significant_line[k]
        #v_i[16] = 7
        #new_i = n_line
        return v_i

    def fanuc_polar_coordinates_16(self, last_significant_line, v_i): #просто стол станка буду поворачивать в это же время
        #FOR XY: Y->C
        print('fanuc_polar_coordinates 16')
        L = v_i[4]
        print('L3232 = ', L)
        ang = (v_i[5]-90) / 360 * math.pi * 2
        v_i[4] = last_significant_line[4]
        v_i[5] = last_significant_line[5]
        v_i[self.n_h] = math.sin(ang) * L
        v_i[self.n_v] = math.cos(ang) * L
        print(f'v_i end = {v_i}')
        return v_i

    def relative_coord_option_DEPRECIATED(self, last_significant_line, new_line):#подходит для C

        print('relative_coord_option')
        print('last_significant_line_: ', last_significant_line)
        print('1 new_line = ', new_line)
        for k in range(4, 7):#17, 20)
            if not np.isnan(new_line[k]):
                new_line[k] = new_line[k] + last_significant_line[k]
        for k in range(4, 7):#17, 20)
            if not np.isnan(new_line[k]):
                new_line[k] = new_line[k] + last_significant_line[k]
        for k in range(10, 13):#+IJK
            if not np.isnan(new_line[k]):
                new_line[k] = new_line[k] + last_significant_line[k]
        print('2 new_line = ', new_line)
        return new_line

    def relative_coord_option(self, last_significant_line, new_line):#подходит для C

        print('relative_coord_option')
        print('last_significant_line_: ', last_significant_line)
        print('1 new_line = ', new_line)
        for k in range(4, 7):#17, 20)
            if not np.isnan(new_line[k]):
                new_line[k] = new_line[k] + last_significant_line[k]
        #for k in range(17, 20):#17, 20)
        #    if not np.isnan(new_line[k]):
        #        new_line[k] = new_line[k] + last_significant_line[k]
        for k in range(10, 13):#+IJK
            if not np.isnan(new_line[k]):
                new_line[k] = new_line[k] + last_significant_line[k]
        print('2 new_line = ', new_line)
        return new_line

    def number_hor_vert_perp_from_plane(self, plane):
        #print('plane = {}, type = {}'.format(plane, type(plane)))
        #d = 2# added two clomns.
        if plane == '17':
            n_h = 4
            n_v = 5
            n_p = 6
        elif plane == '18':
            n_h = 6
            n_v = 4
            n_p = 5
        else:  # plane 19
            n_h = 5
            n_v = 6
            n_p = 4
        #print('n_h = {}, n_v = {}, n_p = {}'.format(n_h, n_v, n_p))
        return n_h, n_v, n_p

    def add_ark_points(self, v, np_num, n_h, n_v, n_p, min_ark_step,
                       curentSC, main_G549, CYCLE800,
                       L_S_L_noSHIFT:np.ndarray,
                       N_S_L_noSHIFT:np.ndarray):
        """
        Add points to make ark in the current G549
        """

        print(f'add_ark_points curentSC = {curentSC}')
        print(f'L_S_L_noSHIFT = {L_S_L_noSHIFT}')
        print(f'N_S_L_noSHIFT = {N_S_L_noSHIFT}')

        np_line = v[np_num]

        ph = L_S_L_noSHIFT[n_h]  # previous horizontal
        pv = L_S_L_noSHIFT[n_v]  # previous vertical
        pp = L_S_L_noSHIFT[n_p]  # previous perpendicular

        print(f'pv = {pv}, ph = {ph}, pp = {pp}')
        ch = n_h + 6  # - 9# #+
        cv = n_v + 6  # - 9#
        # cp = n_p + 6
        R = np_line[13]#saved

        # 1 vectors
        OAx = ph - np_line[ch]
        OAy = pv - np_line[cv]

        ABx = N_S_L_noSHIFT[n_h] - ph#saved
        ABy = N_S_L_noSHIFT[n_v] - pv#saved

        print(f'OAx = {OAx}, OAy = {OAy}, ABx = {ABx }, ABy = {ABy}, R = {R}')
        # OA = [OAx, OAy]
        # AB = [ABx, ABy]
        # print('||| V = ', v)
        # 2 g2 g3
        if np_line[3] == 2:
            AAx = OAy
            AAy = - OAx
        elif np_line[3] == 3:
            AAx = - OAy
            AAy = OAx
        else:
            print('redactor add_ark_points fail')
        # 3 cor gamma
        # print('AAx = {}, ABx = {}, AAy = {}, ABy = {}'.format(AAx, ABx, AAy, ABy))
        cos_gamma = (AAx * ABx + AAy * ABy) / math.sqrt((AAx ** 2 + AAy ** 2) * (ABx ** 2 + ABy ** 2))
        # 3
        print(f'cos_gamma = {cos_gamma}')
        if np.isnan(cos_gamma):
            print('naaaaan')
            self.redactor.Logs.math_logs = self.redactor.Logs.math_logs + f'{int(np_line[15])} line  R=0??\n'
            self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.ERROR_lines.extend(
                (L_S_L_noSHIFT[9], np_line))
            return v, 0
        alpha = 2 * math.acos(cos_gamma)

        # min_ark_step = R / 10
        # print('here min_ark_step = ', min_ark_step)
        # print('R = ', R)
        cos_alpha_segmenta = 1 - 0.5 * ((min_ark_step ** 2) / (R ** 2))
        # print('cos_alpha_segmenta = ', cos_alpha_segmenta)
        sin_alpha_segmenta = math.sqrt(1 - cos_alpha_segmenta ** 2)
        alpha_segmenta = math.acos(cos_alpha_segmenta)
        print(f'alpha = {alpha}, alppha segmenta = {alpha_segmenta}')
        # ищем сколько строк и синусы
        # var1 = alpha / alpha_segmenta
        n = math.floor(alpha / alpha_segmenta)
        if n < 0:
            print('ТРЕВОООГАА!!! Дальше остаток тоже переделывать')
        # создаем массив

        #ark_np_array = np.full((n, axises), np_line)
        ark_np_array = np.full((n, axises), N_S_L_noSHIFT)

        #Lperp = v[np_num, n_p] - last_significant_line[n_p]
        Lperp = N_S_L_noSHIFT[n_p] - L_S_L_noSHIFT[n_p]
        alpha_less = n * alpha_segmenta
        # Lperp = Lperp * ((alpha_segmenta * n) / math.radians(alpha))
        if alpha != 0:
            Lperp = Lperp * (alpha_less / alpha)
        else:
            print('redactor add_ark_points failed0')
            return v, 0

        perp_step = Lperp / n  # divide by zero?
        ph = OAx
        pv = OAy
        # copy_add = 13
        # print('Угол = {}, n = {}'.format(alpha, n))
        n_h_new = n_h + 13
        n_v_new = n_v + 13
        n_p_new = n_p + 13
        if np_line[3] == 2:
            pp = pp + perp_step
            for k in range(n):
                new_hor_0 = ph * cos_alpha_segmenta + pv * sin_alpha_segmenta
                new_vert_0 = - ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
                ark_np_array[k, n_h_new] = new_hor_0 + np_line[ch]
                ark_np_array[k, n_v_new] = new_vert_0 + np_line[cv]
                ph = new_hor_0
                pv = new_vert_0
                ark_np_array[k, n_p_new] = pp + k * perp_step
                ark_np_array[k, 16] = 5.  # todo дополнительные точки. мы хотим рисовать линии но не точки
        elif np_line[3] == 3:
            pp = pp + perp_step
            for k in range(n):
                new_hor_0 = ph * cos_alpha_segmenta - pv * sin_alpha_segmenta
                new_vert_0 = ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
                ark_np_array[k, n_h_new] = new_hor_0 + np_line[ch]
                ark_np_array[k, n_v_new] = new_vert_0 + np_line[cv]
                ph = new_hor_0
                pv = new_vert_0
                ark_np_array[k, n_p_new] = pp + k * perp_step
                ark_np_array[k, 16] = 5.
                # print('new_hor_0 = ', new_hor_0)
                # print('new_vert_0 = ', new_vert_0)
        else:
            print('redactor add_ark_points failed')


        #if v[np_num, 9] == last_significant_line[9]:
        if N_S_L_noSHIFT[9] == L_S_L_noSHIFT[9]:
            if ark_np_array[0, 9] != 0:
                # a = math.radians(ark_np_array[0, 9])
                a = ark_np_array[0, 9]
                for line in ark_np_array: line[17], line[18] = turn_around_radians1(line[17], line[18], a)
        else:
            # print('|||  ark step = ', ark_np_array)
            #deltaC = v[np_num, 9] - last_significant_line[9]
            deltaC = N_S_L_noSHIFT[9] - L_S_L_noSHIFT[9]
            # Cperp = math.radians(deltaC) * (alpha_less / alpha)
            Cperp = deltaC * (alpha_less / alpha)
            C_step = Cperp / n
            startCangle = L_S_L_noSHIFT[9][9] + C_step
            # todo Пока выключил обороты с осью С (слудющая строка)
        print(f'  GGG CYCLE800 = {CYCLE800}')
        print(f'aerk array first = {ark_np_array}')
        if self.dots_transformation_matrix is not None:
            #trans_matrix_from_SC
            G549_4_many_dots_NEW(ark_np_array, self.dots_transformation_matrix)
        return np.insert(v, np_num, ark_np_array, axis=0), n



def angle_axises_rotate_Direct_line(self):
    pass

def angle_axises_rotate_Ark_line(self):
    pass