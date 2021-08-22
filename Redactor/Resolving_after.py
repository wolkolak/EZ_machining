import copy
import numpy as np
from Settings.settings import axises


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
        self.current_frame_address_in_visible_pool[:, 0] = np.arange(1, 1 + h)
        self.current_frame_address_in_visible_pool[:, 1] = np.arange(1, 1 + h)

        self.current_visible_np[:] = np.nan
        self.current_g_cod_pool[:] = np.nan
        self.visible_np[:] = np.nan
        self.main_g_cod_pool[:] = np.nan
        self.frame_address_in_visible_pool = np.zeros((1, 2), int)
        # self.frame_address_in_visible_pool = np.nan

    def resolving(self, min_line):
        step = 100
        n_visual1 = self.frame_address_in_visible_pool[min_line][0]
        n_visual2 = self.frame_address_in_visible_pool[min_line + step][0]
        if min_line + step > len(self.main_g_cod_pool):
            step = len(self.main_g_cod_pool) - min_line
        min_visual = self.frame_address_in_visible_pool[min_line - 1, 1] + 1
        self.current_visible_np = self.main_g_cod_pool[min_line:min_line+step+1]#todo +1??
        self.special_options_applying(min_line)#todo переделать

        #left_b = self.frame_address_in_visible_pool[min_L, 0]
        #right_b = self.frame_address_in_visible_pool[max_L, 1] + 1
        # del_number =self.frame_address_in_visible_pool[max_L, 1] - self.frame_address_in_visible_pool[min_L, 0]
        #self.frame_address_in_visible_pool = np.delete(self.frame_address_in_visible_pool, np.s_[min_L:max_L + 1],
        #                                               axis=0)
        self.delete_lines_from_np_box(False)

        self.frame_address_in_visible_pool[min_L:] = self.frame_address_in_visible_pool[
                                                     min_L:] - right_b + left_b  # delta_min_max

        self.visible_np = np.delete(self.visible_np, np.s_[left_b: right_b], axis=0)
        self.visible_np = np.insert(self.visible_np, min_visual,
                                    self.current_visible_np, axis=0)

        self.frame_address_in_visible_pool[min_line:] = self.frame_address_in_visible_pool[
            min_line:] + len(self.current_visible_np)
        self.frame_address_in_visible_pool = np.insert(self.frame_address_in_visible_pool, min_line,
                                    self.current_frame_address_in_visible_pool, axis=0)

        N_line_number = min_line + len(self.current_g_cod_pool) - 1#self.current_g_cod_pool[len(self.current_g_cod_pool)-1]


def compare(line_new, line_old):

    if line_new == line_old:
        print('ОДИНАКОВЫ')