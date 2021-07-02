from PyQt5.QtWidgets import QGridLayout, QWidget,  QProgressBar
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
from Settings.settings import min_ark_step
from Redactor.My_plain_text import MyEdit
from left_zone.ARK_solving import *

class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()
        self.base = base
        self.valueChanged.connect(self.finish_current_batch)

    def finish_current_batch(self, current_value):
        self.base.highlight.count_in_step = 0
        #print('progressbar finish current batch Hcount ', self.base.highlight.count)
        if current_value == self.maximum():
            #print('finish_current_batch->inserting_in_main_g_cod')
            self.inserting_in_main_g_cod()
            print('Load 100%')
            # создаю пустышку на одну строку на всякий случай. как минимум при разработке это полезно
            self.base.reading_lines_number = 1
            axises = 15
            self.base.current_g_cod_pool = np.zeros((self.base.reading_lines_number, axises), float)
            self.base.current_g_cod_pool[:] = np.nan
            self.base.highlight.to_the_start()
            self.setValue(0)
        elif self.base.reading_lines_number < self.base.highlight.count + self.base.highlight.standart_step:
            #print(
            #    'Делаем шаг поменьше: number_of_lines={}, self.base.highlight.count={}, self.base.highlight.standart_step={}'
            #    .format(self.base.reading_lines_number, self.base.highlight.count, self.base.highlight.standart_step))
            self.base.highlight.standart_step = self.base.reading_lines_number - self.base.highlight.count  # - 1?


    def inserting_in_main_g_cod(self):
        print('how many')
        #print('вставить {} перед np строкой {}'.format(self.base.current_g_cod_pool, self.base.editor.min_line_np))
        self.base.main_g_cod_pool = np.insert(self.base.main_g_cod_pool, self.base.editor.min_line_np, self.base.current_g_cod_pool, axis=0)
        self.base.change_visible_array()
        self.base.tab_.center_widget.left.update_visible_np_left()




class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing):
        super().__init__()

        self.index_insert = 1
        self.tab_ = tab_
        self.g_modal = np.array([0], float)
        #self.lastGcod = 0
        grid = QGridLayout()
        self.setLayout(grid)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)
        self.progress_bar = Progress(self)
        self.reading_lines_number = self.editor.blockCount() or 1

        axises = 15
        self.current_g_cod_pool = np.zeros((self.reading_lines_number, axises), float)
        self.visible_np = np.zeros((1, axises), float)
        self.main_g_cod_pool = np.zeros((1, axises), float)
        self.current_g_cod_pool[:] = np.nan
        self.visible_np[:] = np.nan
        self.main_g_cod_pool[:] = np.nan
        self.progress_bar.setMaximum(self.reading_lines_number)
        grid.addWidget(self.progress_bar, 1, 0)
        self.set_syntax()

        self.index_operations = 0
    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

    def special_options_applying(self):
        #processor = self.central_widget.note.currentWidget().highlight.reversal_post_processor
        #print('clear zyzcab from Nan')
        #заполнить первую строку
        self.highlight.reversal_post_processor.k_appliying(self.visible_np)
        #print('self.highlight.reversal_post_processor.k_XYZABC_list[0] = ', self.highlight.reversal_post_processor.k_XYZABC_list[0])
        start_pointXYZ = [self.highlight.reversal_post_processor.start_pointXYZ[i] * self.highlight.reversal_post_processor.k_XYZABC_list[i] for i in range(6)]
        new_np_line = [0, 0, *start_pointXYZ, None, None, None, None, None, 0, None]#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type
        #print('start_pointXYZ = ', start_pointXYZ)
        v = self.visible_np
        v[0] = new_np_line[:]
        last_significant_line = new_np_line
        h, w = v.shape
        v[:, 13] = np.arange(h)#todo Наверняка это можно как то ускорить
        plane = 18
        i = 1
        len_v = len(v)
        while i < len_v:
            if np.isnan(v[i, 14]):
                for c in range(2, 8):
                    if np.isnan(v[i, c]):
                        v[i, c] = last_significant_line[c]
                if v[i, 0] == 2 or v[i, 0] == 3:#todo если хотим наследовать, то v[i, 1]
                    #print('v[i, 11] = ', v[i, 11])
                    if np.isnan(v[i, 11]):
                        n_h, n_v, n_p = self.number_hor_vert_perp_from_plane(plane)
                        #print('v[i, n_h] = {}, v[i, n_v] = {}'.format(v[i, n_h+6], v[i, n_v+6]))
                        if np.isnan(v[i, n_h+6]) or np.isnan(v[i, n_v+6]):
                            print('frame {} - not enough DATA for ARK'.format(i))
                            last_significant_line = v[i]
                            i = i + 1
                            continue
                        centre_ijk_ARK(v[i], n_h, n_v, n_p)
                    else:
                        if not np.isnan(v[i, 8:11]).any():
                            print('Too mach data in line {}. Recommend to choose either R either IJK format'.format(i))
                        n_h, n_v, n_p = self.number_hor_vert_perp_from_plane(plane)
                        v[i, 8:11] = centre_R_ARK(v[i, 0], plane, v[i-1], v[i], n_h, n_v, n_p)


                    #print('G23 заполнен {} вот этим {}'.format(i, v[i]))
                    if v[i, 11] < min_ark_step:
                        last_significant_line = v[i]
                        i = i + 1
                        continue
                    v, n = self.add_ark_points(v, i, n_h, n_v, n_p)#todo процесс копирования запускает цикл повторно
                    len_v = len(v)
                    self.visible_np = v
                    i = i + n
                last_significant_line = v[i]
            i = i + 1
        #print('v = ', v)

    def number_hor_vert_perp_from_plane(self, plane):
        if plane == 17:
            n_h = 2
            n_v = 3
            n_p = 4
        elif plane == 18:
            n_h = 4
            n_v = 2
            n_p = 3
        else:  # plane 19
            n_h = 3
            n_v = 4
            n_p = 2
        return n_h, n_v, n_p

    def change_visible_array(self):#todo здесб переключатель чтобы не просчитывать visible при отключенном бэкплотте

        self.visible_np = self.main_g_cod_pool.copy()
        self.special_options_applying()
        self.tab_.center_widget.left.reset_np_array_in_left_field(self.visible_np)

    def add_ark_points(self, v, np_num, n_h, n_v, n_p):
        np_line = v[np_num]
        # предыдущие данные
        ph = v[np_num - 1, n_h]  # previous horizontal
        pv = v[np_num - 1, n_v]  # previous vertical
        pp = v[np_num - 1, n_p]  # previous perpendicular
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
        ark_np_array = np.full((n, 15), np_line)  # axises
        # perpendicular
        #print('alpha = ', alpha)
        # L = math.pi * R / 180 * alpha
        # L = min_ark_step * n
        # tg_feta = (np_line[perp] - cp)/L
        # perp_step = min_ark_step * tg_feta
        Lperp = v[np_num, n_p] - v[np_num - 1, n_p]
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
            for k in range(n - 1):
                new_hor_0 = ph * cos_alpha_segmenta + pv * sin_alpha_segmenta
                new_vert_0 = - ph * sin_alpha_segmenta + pv * cos_alpha_segmenta
                ark_np_array[k, n_h] = new_hor_0 + np_line[ch]
                ark_np_array[k, n_v] = new_vert_0 + np_line[cv]
                ph = new_hor_0
                pv = new_vert_0
                ark_np_array[k, n_p] = pp + (k - 1) * perp_step
        elif np_line[1] == 3:
            for k in range(n - 1):
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
        return np.insert(v, np_num, ark_np_array, axis=0), n


