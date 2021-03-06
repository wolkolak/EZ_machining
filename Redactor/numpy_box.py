import numpy as np
from Settings.settings import axises, min_ark_step
from left_zone.ARK_solving import *

class NumpyBox():
    """
    class for all numpy objects required for updating 3dModel by changed parts
    """
    def __init__(self, redactor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('jj11')
        self.redactor = redactor
        reading_lines_number = redactor.reading_lines_number
        print('jj22')
        self.current_g_cod_pool = np.zeros((reading_lines_number, axises), float)
        self.visible_np = np.zeros((1, axises), float)
        self.main_g_cod_pool = np.zeros((1, axises), float)
        self.current_visible_np = np.zeros((reading_lines_number, axises), float)

        self.current_frame_address_in_visible_pool = np.zeros((reading_lines_number, 2), int)
        h, w = self.current_frame_address_in_visible_pool.shape
        self.current_frame_address_in_visible_pool[:, 0] = np.arange(1, 1+h)
        self.current_frame_address_in_visible_pool[:, 1] = np.arange(1, 1+h)

        self.current_visible_np[:] = np.nan
        self.current_g_cod_pool[:] = np.nan
        self.visible_np[:] = np.nan
        self.main_g_cod_pool[:] = np.nan
        self.frame_address_in_visible_pool = np.zeros((1, 2), int)
        #self.frame_address_in_visible_pool = np.nan




    def create_new_currents_in_np_box(self, axis):
        print('self.redactor.reading_lines_number = ', self.redactor.reading_lines_number)
        self.current_g_cod_pool = np.zeros((self.redactor.reading_lines_number, axis), float)
        self.current_visible_np = np.zeros((self.redactor.reading_lines_number, axis), float)
        self.current_frame_address_in_visible_pool = np.zeros((self.redactor.reading_lines_number, 2), int)
        self.current_g_cod_pool[:] = np.nan
        self.current_visible_np[:] = np.nan
        h, w = self.current_frame_address_in_visible_pool.shape
        print('create_new_currents_np(', h)
        #n = self.redactor.editor.min_line_np-1
        n = self.frame_address_in_visible_pool[self.redactor.editor.min_line_np-1, 1] + 1

        self.current_frame_address_in_visible_pool[:, 0] = np.arange(n, n+h)
        self.current_frame_address_in_visible_pool[:, 1] = np.arange(n, n+h)

    def delete_lines_from_np_box(self):
        min_L = self.redactor.editor.min_line_np
        max_L = self.redactor.editor.second_place
        delta_min_max = max_L - min_L# + 1
        left_b = self.frame_address_in_visible_pool[min_L, 0]
        right_b = self.frame_address_in_visible_pool[max_L, 1]+1
        self.frame_address_in_visible_pool = np.delete(self.frame_address_in_visible_pool, np.s_[min_L:max_L + 1],
                                                       axis=0)
        self.frame_address_in_visible_pool[min_L:] = self.frame_address_in_visible_pool[min_L:] - delta_min_max
        self.redactor.highlight.previous_block_g = self.main_g_cod_pool[min_L-1][1] if min_L > 0 else 0
        self.main_g_cod_pool = np.delete(self.main_g_cod_pool, np.s_[min_L:max_L + 1], axis=0)

        self.redactor.g_modal.del_all_modal_commands_in_range(min_L, max_L, self.redactor.reading_lines_number, delta_min_max-1)

        self.visible_np = np.delete(self.visible_np, np.s_[left_b: right_b], axis=0)
        #self.visible_np = np.delete(self.visible_np, np.s_[min_L:max_L + 1], axis=0)



        #self.frame_address_in_visible_pool = np.delete(self.frame_address_in_visible_pool, np.s_[min_L:max_L + 1], axis=0)

        #todo удаляем из visual np self.current_frame_address_in_visible_pool


    def start_point(self):
        self.start_pointXYZ = [self.redactor.highlight.reversal_post_processor.start_pointXYZ[i] * self.redactor.highlight.reversal_post_processor.k_XYZABC_list[i] for i in range(6)]
        print('ending11')
        self.new_np_line = [0, 0, *self.start_pointXYZ, None, None, None, None, None, 0, None]#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type
        self.visible_np[0] = self.new_np_line[:]
        self.main_g_cod_pool[0] = self.new_np_line[:]

    def new_current_g_cod_pool(self, reading_lines_number):
        self.current_g_cod_pool = np.zeros((reading_lines_number, axises), float)
        self.current_g_cod_pool[:] = np.nan

    def inserting_current_in_main(self, min_line):

        n = 0

        self.current_visible_np = self.current_g_cod_pool.copy()
        self.special_options_applying(min_line+n)#todo переделать
        self.main_g_cod_pool = np.insert(self.main_g_cod_pool, min_line, self.current_g_cod_pool, axis=0)
        self.visible_np = np.insert(self.visible_np, min_line+n,
                                    self.current_visible_np, axis=0)
        #print('current frame_ = ', self.current_frame_address_in_visible_pool)
        #print('self.frame_address_in_visible_pool1 = ', self.frame_address_in_visible_pool)
        self.frame_address_in_visible_pool[min_line + n - 0:] = self.frame_address_in_visible_pool[
            min_line + n - 0:] + len(self.current_frame_address_in_visible_pool)
        self.frame_address_in_visible_pool = np.insert(self.frame_address_in_visible_pool, min_line+n-0,
                                    self.current_frame_address_in_visible_pool, axis=0)
        #todo g modal insert DATA in modal dict will happen from recount. we dont need it here
        print('G_modal = ', self.redactor.g_modal)





    def special_options_applying(self, min_visual_line):
        self.redactor.g_modal.create_current_from_g_modal(self.redactor.editor.min_line_np)
        print('Вот здесь нужнен firstblock')
        #заполнить первую строку
        min_cod_line = self.redactor.editor.min_line_np
        self.redactor.highlight.reversal_post_processor.k_appliying(self.current_visible_np)#visible_np
        #print('self.highlight.reversal_post_processor.k_XYZABC_list[0] = ', self.highlight.reversal_post_processor.k_XYZABC_list[0])

        #print('start_pointXYZ = ', start_pointXYZ)
        #v = self.visible_np
        v = self.current_visible_np
        print('mmmm')
        print('self.editor.min_line_np-1 = ', self.main_g_cod_pool[min_cod_line-1])
        #todo нужно верную строку копировать
        last_significant_line = self.visible_np[min_cod_line-1]
        h, w = v.shape
        v[:, 13] = np.arange(min_visual_line, min_visual_line+h)#todo Наверняка это можно как то ускорить
        #plane = 18
        #plane = self.redactor.g_modal.current_g_modal['plane']

        print('plane = ', self.redactor.g_modal.current_g_modal['plane'])
        print('type of plane ', type(self.redactor.g_modal.current_g_modal['plane']))
        i = 0
        i_str = 0
        len_v = len(v)
        while i < len_v:
            if np.isnan(v[i, 14]):
                for c in range(2, 8):
                    if np.isnan(v[i, c]):
                        v[i, c] = last_significant_line[c]
                if v[i, 0] == 2 or v[i, 0] == 3:#todo если хотим наследовать, то v[i, 1]
                    #print('ark start')
                    if np.isnan(v[i, 11]):
                        n_h, n_v, n_p = self.number_hor_vert_perp_from_plane(self.redactor.g_modal.current_g_modal['plane'])
                        #print('v[i, n_h] = {}, v[i, n_v] = {}'.format(v[i, n_h+6], v[i, n_v+6]))
                        if np.isnan(v[i, n_h+6]) or np.isnan(v[i, n_v+6]):
                            print('frame {} - not enough DATA for ARK'.format(i))
                            last_significant_line = v[i]
                            i = i + 1
                            i_str = i_str + 1
                            continue
                        v[i, 11] = centre_ijk_ARK(v[i], n_h, n_v, n_p)
                    else:
                        if not np.isnan(v[i, 8:11]).any():
                            print('Too mach data in line {}. Recommend to choose either R either IJK format'.format(i))
                        print('zdes')
                        print('self.redactor.g_modal.current_g_modal[plane] = ', self.redactor.g_modal.current_g_modal['plane'])
                        n_h, n_v, n_p = self.number_hor_vert_perp_from_plane(self.redactor.g_modal.current_g_modal['plane'])
                        v[i, 8:11] = centre_R_ARK(v[i, 0], self.redactor.g_modal.current_g_modal['plane'], last_significant_line, v[i], n_h, n_v, n_p)
                    #print('G23 заполнен {} вот этим {}'.format(i, v[i]))
                    #считаем длину вектора
                    len_ark = math.sqrt((v[i, n_h] - last_significant_line[n_h])**2 + (v[i, n_v] - last_significant_line[n_v])**2)
                    #print('len ark = ', len_ark)
                    if len_ark < min_ark_step:
                        last_significant_line = v[i]
                        i = i + 1
                        i_str = i_str + 1
                        continue
                    v, n = self.add_ark_points(v, last_significant_line, i, n_h, n_v, n_p, min_ark_step)
                    #print('i почемуто равно ', i)
                    #print('n точек = ', n)
                    print('self.current_frame_address_in_visible_pool2 = ', self.current_frame_address_in_visible_pool)
                    self.current_frame_address_in_visible_pool[i_str:] = self.current_frame_address_in_visible_pool[i_str:] + n

                    print('self.current_frame_address_in_visible_pool2 = ', self.current_frame_address_in_visible_pool)
                    self.current_frame_address_in_visible_pool[i_str, 0] = self.current_frame_address_in_visible_pool[i_str, 0] - n
                    #print('current_frame_address_in_visible_pool[i, 0] = ', self.current_frame_address_in_visible_pool[i, 0])
                    len_v = len(v)#todo + n
                    self.current_visible_np = v
                    i = i + n
                last_significant_line = v[i]
            i = i + 1
            i_str = i_str + 1

    def number_hor_vert_perp_from_plane(self, plane):
        print('plane = {}, type = {}'.format(plane, type(plane)))
        if plane == '17':
            n_h = 2
            n_v = 3
            n_p = 4
        elif plane == '18':
            n_h = 4
            n_v = 2
            n_p = 3
        else:  # plane 19
            n_h = 3
            n_v = 4
            n_p = 2
        print('n_h = {}, n_v = {}, n_p = {}'.format(n_h, n_v, n_p))
        return n_h, n_v, n_p

    def add_ark_points(self, v, last_significant_line, np_num, n_h, n_v, n_p, min_ark_step):
        np_line = v[np_num]
        # предыдущие данные
        ph = last_significant_line[n_h]  # previous horizontal
        pv = last_significant_line[n_v]  # previous vertical
        pp = last_significant_line[n_p]  # previous perpendicular
        ch = n_h + 6
        cv = n_v + 6
        #cp = n_p + 6
        R = np_line[11]

        # 1 vectors
        OAx = ph - np_line[ch]
        OAy = pv - np_line[cv]

        ABx = np_line[n_h] - ph
        ABy = np_line[n_v] - pv

        # OA = [OAx, OAy]
        # AB = [ABx, ABy]

        # 2 g2 g3
        if np_line[1] == 2:
            AAx = OAy
            AAy = - OAx
        elif np_line[1] == 3:
            AAx = - OAy
            AAy = OAx
        else:
            print('redactor add_ark_points fail')
        # 3 cor gamma
        #print('AAx = {}, ABx = {}, AAy = {}, ABy = {}'.format(AAx, ABx, AAy, ABy))
        cos_gamma = (AAx * ABx + AAy * ABy) / math.sqrt((AAx ** 2 + AAy ** 2) * (ABx ** 2 + ABy ** 2))
        # 3
        alpha = 2 * math.acos(cos_gamma)

        cos_alpha_segmenta = 1 - 0.5 * ((min_ark_step ** 2) / (R ** 2))
        sin_alpha_segmenta = math.sqrt(1 - cos_alpha_segmenta ** 2)
        alpha_segmenta = math.acos(cos_alpha_segmenta)
        # ищем сколько строк и синусы
        var1 = alpha / alpha_segmenta
        n = math.floor(var1)
        if n < 0:
            print('ТРЕВОООГАА!!! Дальше остаток тоже переделывать')
        # создаем массив

        ark_np_array = np.full((n, axises), np_line)
        # perpendicular
        #print('alpha = ', alpha)
        # L = math.pi * R / 180 * alpha
        # L = min_ark_step * n
        # tg_feta = (np_line[perp] - cp)/L
        # perp_step = min_ark_step * tg_feta
        Lperp = v[np_num, n_p] - last_significant_line[n_p]
        perp_step = Lperp / var1  # divide by zero?

        # ark_np_array[: 0] = 22
        # ark_np_array[: 1] = 22
        # заполняем массив
        # print('v.shape = ', v.shape)
        #print('ark_np_array.shape = ', ark_np_array.shape)
        ph = OAx
        pv = OAy

        #print('Угол = {}, n = {}'.format(alpha, n))
        if np_line[1] == 2:
            for k in range(n):
                new_hor_0 = ph * cos_alpha_segmenta + pv * sin_alpha_segmenta
                new_vert_0 = - ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
                ark_np_array[k, n_h] = new_hor_0 + np_line[ch]
                ark_np_array[k, n_v] = new_vert_0 + np_line[cv]
                ph = new_hor_0
                pv = new_vert_0
                ark_np_array[k, n_p] = pp + (k - 1) * perp_step
        elif np_line[1] == 3:
            for k in range(n):
                new_hor_0 = ph * cos_alpha_segmenta - pv * sin_alpha_segmenta
                new_vert_0 = ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
                ark_np_array[k, n_h] = new_hor_0 + np_line[ch]
                ark_np_array[k, n_v] = new_vert_0 + np_line[cv]
                ph = new_hor_0
                pv = new_vert_0
                ark_np_array[k, n_p] = pp + (k - 1) * perp_step
        else:
            print('redactor add_ark_points failed')
            # прибавляе
        #print('n in add_ark_points = ', n)
        return np.insert(v, np_num, ark_np_array, axis=0), n

    def slide_next_address_cuz_new_points(self):
        self.current_frame_address_in_visible_pool = 0