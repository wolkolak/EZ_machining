from PyQt5.QtWidgets import QGridLayout, QWidget,  QProgressBar
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
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
        print('clear zyzcab from Nan')
        #заполнить первую строку
        self.highlight.reversal_post_processor.k_appliying(self.visible_np)
        print('self.highlight.reversal_post_processor.k_XYZABC_list[0] = ', self.highlight.reversal_post_processor.k_XYZABC_list[0])
        start_pointXYZ = [self.highlight.reversal_post_processor.start_pointXYZ[i] * self.highlight.reversal_post_processor.k_XYZABC_list[i] for i in range(6)]
        new_np_line = [0, 0, *start_pointXYZ, None, None, None, None, None, 0, None]#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type
        print('start_pointXYZ = ', start_pointXYZ)
        v = self.visible_np
        v[0] = new_np_line[:]
        last_significant_line = new_np_line
        h, w = v.shape
        v[:, 13] = np.arange(h)#todo Наверняка это можно как то ускорить
        plane = 18
        i = 1
        while i in range(1, len(v)):
            #v[i, 13] = i
            if np.isnan(v[i, 14]):
                for c in range(2, 8):
                    if np.isnan(v[i, c]):
                        v[i, c] = last_significant_line[c]
                last_significant_line = v[i]
                if v[i, 0] == 2 or v[i, 0] == 3:#todo если хотим наследовать, то v[i, 1]
                    v[i, 8:11] = centre_R_ARK(v[i, 0], plane, v[i, 11], *v[i-1, 2:5], *v[i, 2:5])
                    #print('G23 заполнен {} вот этим {}'.format(i, v[i]))
                    v, n = self.add_ark_points(v, i, 18)#todo процесс копирования запускает цикл повторно
                    i = i + n
            i = i + 1
        #print('v = ', v)

    def change_visible_array(self):#todo здесб переключатель чтобы не просчитывать visible при отключенном бэкплотте
        self.visible_np = self.main_g_cod_pool.copy()
        self.special_options_applying()
        self.tab_.center_widget.left.reset_np_array_in_left_field()

    def add_ark_points(self, v, np_num, plane):
        np_line0 = v[np_num]
        if plane == 17:
            hor = 2
            vert = 3
            perp = 4
        elif plane == 18:
            hor = 2
            vert = 4
            perp = 3
        else:
            hor = 3
            vert = 4
            perp = 2
        #предыдущие данные
        p_np_arr_hor = v[np_num-1, hor]
        p_np_arr_vert = v[np_num - 1, vert]
        p_np_arr_perp = v[np_num - 1, perp]
        #ищем сколько строк и синусы
        n = 2
        #создаем массив
        ark_np_array = np.full((n, 15), np_line0)#axises
        #ark_np_array[: 0] = 22
        #ark_np_array[: 1] = 22
        #заполняем массив
        print('v.shape = ', v.shape)
        print('ark_np_array.shape = ', ark_np_array.shape)
        for k in range(n):
            ark_np_array[k, hor] = v[np_num-1, hor]
            ark_np_array[k, vert] = v[np_num - 1, vert]
            ark_np_array[k, perp] = v[np_num - 1, vert]
            #прибавляе
        return np.insert(v, np_num, ark_np_array, axis=0), n
