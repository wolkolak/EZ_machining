from abc import ABC
import os
import sys
import fileinput
import re
from Gui import gui_classes

import importlib

class Machine(ABC):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.machine_settings_open, self.machine_settings_import = self.get_home_machine_settings()
        print('self.machine_settings_open = ', self.machine_settings_open)
        self.m_zero_to_m_1ax_center_CONST = [0., 0., 0.]#todo смещает серую точку от места крепления головы. Визуально - когда иначе не видно.
        self.start_distance_zero_to_lever = [0., 0., 0.]
        self.XYZABC_ADD = [0., 0., 0., 0., 0., 0.]
        self.open_machine_settings()
        self.ax_order = 'ABC'   # from closest rotate ax around part to the most distant one
                                # Axis from differnt machine parts have no relative order. sort it as u want
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Table',  'LShoulder': 100,    'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},  # it can be None or anything really
                                   'B': {'Place': 'Table',  'LShoulder': 100,    'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},  # t_angle это поворот, который мы делаем до того как переместимся в следующее звено. Наверное.
                                   'C': {'Place': 'Head',   'LShoulder': 100,    'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'}  # j_angle не влияет ни на что
                                   }
        self.k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}
        self.collet = {'angle': 0., 'L_from_segment_tip': 0., 'baseR': 60.,
                       'topR': 30., 'h': 70., 'polygons_r': 20, 'polygons_h': 10}
        self.max_table_head_distance = [500., 250., 500.]
        self.min_table_head_distance = [0., 0., 0.]
        self.for_45grad_angles = {}
        self.animation_line_ax_order = 'XZY'
        self.my_name()

    def give_parts_to_scene(self):
        table = [[None, None, None, None], [None, None, None, None], [None, None, None, None]]#[A][B][C]
        head = [[None, None, None, None], [None, None, None, None], [None, None, None, None]]
        for liter in self.DICT_AX_PARAMETERS:#liter is a letter ABC key
            mini_dict = self.DICT_AX_PARAMETERS[liter]
            if liter == 'A':
                i = 0
            elif liter == 'B':
                i = 1
            else:
                i = 2
            if mini_dict['Place'] == 'Table':
                table[i][0] = mini_dict['LShoulder']
                table[i][1] = mini_dict['j_angle']
                table[i][2] = mini_dict['t_angle']
                table[i][3] = mini_dict['local_order']
            else:
                head[i][0] = mini_dict['LShoulder']
                head[i][1] = mini_dict['j_angle']
                head[i][2] = mini_dict['t_angle']
                head[i][3] = mini_dict['local_order']
        print('give_parts_to_scene table: ', table)
        print('give_parts_to_scene head: ', head)
        return table, head

    def k_applying(self, visible_np):
        visible_np[:, 4] = visible_np[:, 4] * self.k_XYZABC['X']

    def k_applying1_line(self, visible_np):
        visible_np[4] = visible_np[4] * self.k_XYZABC['X']

    def k_devide1_line(self, visible_np):
        visible_np[4] = visible_np[4] / self.k_XYZABC['X']

    def k_devide_applying2line(self, visible_np_line):
        visible_np_line[4] = visible_np_line[4] / self.k_XYZABC['X']

    def insert_ax_order(self):
        i = 1
        for lit in self.ax_order:
            self.DICT_AX_PARAMETERS[lit]['Order'] = i
            i += 1


    def my_name(self):
        self.full_name, self.last_name = self.my_location()
        print('self.last_name = ', self.last_name)


    @classmethod
    def my_location(cls):
        #__location__ = sys.modules[cls.__module__].__file__
        #__location__ = '\\'.join(__location__.split('\\')[:-1])

        full_name = sys.modules[cls.__module__].__file__
        index = full_name.rfind('\\')
        last_name = full_name[:index]
        index = last_name.rfind('\\')
        last_name = last_name[index+1:]

        return full_name, last_name

    @classmethod
    def get_home_machine_settings(cls) -> str:
        """
        :return: 'a' is an address of machine_settings.py with slashes, 'a_py_dots' - with dots
        """
        full_name, __last_name = cls.my_location()
        location = '\\'.join(full_name.split('\\')[:-1])
        a_ = location + r'\machine_settings'
        folder = 'Modelling_clay'
        a_py = folder + a_.split(folder)[1]
        a_py_dots = a_py.replace('\\', '.')
        a = a_ + r'.py'
        print('a = {}, a_py_dots = {}'.format(a, a_py_dots))
        return a, a_py_dots

    def open_machine_settings(self):
        a, a_py_dots = self.machine_settings_open, self.machine_settings_import
        print('OPEN: a = {}, a_py_dots = {}'.format(a, a_py_dots))
        try:
        #if True:
            if a_py_dots in sys.modules:
                print('sys.modules[a_py_dots] = ', sys.modules[a_py_dots])
                my_module = importlib.reload(sys.modules[a_py_dots]) #todo ПОМЕНЯТЬ НАЗАД
                #import Modelling_clay.machines.NT6000_Table_C_Head_BA.machine_settings as my_module
            else:
                print('тут же дрянь')
                my_module = importlib.import_module(a_py_dots)
                print('a nen&')
            #with open(a) as f:
            self.g54_g59_AXIS = my_module.g54_59
            #self.offset_pointXYZ = my_module.offset_pointXYZ
            #self.machine_zero_variant = my_module.machine_zero_variant
            self.offset_pointXYZ = my_module.offset_pointXYZ

            self.change_TOOL_point1 = my_module.change_TOOL_point1
            self.change_TOOL_point2 = my_module.change_TOOL_point2

            #self.k_XYZABC_list = my_module.k_XYZABC
            self.current_g54_g59 = my_module.current_g54_g59
            self.axles_DICT = my_module.axles_DICT
            self.bound_register = my_module.bound_register
            #self.m_zero_to_m_1ax_center = my_module.offset_pointXYZ
            #todo we should do something here
            #f.close()
        #todo временно
        except:
            print('Except in open_machine_settings')
            print('a = ', a)
            with open(a, 'w') as f:
                f.write(
                    "g54_59 = {  #ATTENTION: do not change format of the lines by hands. if ypu actually done it, check wenether rewrighting from program still work\n")
                for n in range(4, 10):
                    f.write("'G5%d': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'A': 0.0, 'B': 0.0, 'C': 0.0}, \n" % n)
                f.write('}\n')
                f.write("offset_pointXYZ = [500., 0., 50.]\n")
                f.write("current_g54_g59 = 'G54'\n")
                #f.write("machine_zero_variant = [-200., 0., 100.]\n")
                f.write("change_TOOL_point1 = [0., 0., 1000., 0., 0., 0.]\n")
                f.write("change_TOOL_point2 = [0., 0., 1500., 0., 0., 0.]\n")
                f.write("k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}\n")
                f.write("axles_DICT = {'X': True, 'Y': True, 'Z': True, 'A': True, 'B': True, 'C': True}")
            f.close()
            self.open_machine_settings()

            #from .machine_settings import g54_59
            #self.g54_g59_AXIS = g54_59
            #my_module = importlib.import_module(a_py_dots)
            #self.g54_g59_AXIS = my_module.g54_59


    #def save_line_in_machine_settings_py(self, G5N, G_list):
    #    print('save_line_in_machine_settings_py')
#
    #    """Принимает список вида [[name1, value1]...]
    #    Полностью переписывает файл machine_settings.py"""
    #    __location__ = sys.modules[self.__module__].__file__
    #    __location__ = '\\'.join(__location__.split('\\')[:-1])
    #    a = __location__ + r'\machine_settings.py'
    #    print('G5N ==== ', G5N)
    #    new_G5N = "'" + G5N + "'"
    #    print('new_G5N = ', new_G5N)
#
    #    try:
    #        with fileinput.FileInput(a, inplace=True, backup='.bak') as m_settings:
    #            for line in m_settings:
    #                #gui_classes.simple_warning(new_G5N, line)
    #                if re.match('\s*' + new_G5N, line):
    #                    print("{}: {{'X': {}, 'Y': {}, 'Z': {}, 'A': {}, 'B': {}, 'C': {}}},".format(new_G5N, *G_list)) #, \n
    #                else:
    #                    print(line, end='')
    #        os.unlink(a + '.bak')
    #    except OSError:
    #        gui_classes.simple_warning('Ooh', 'Something went wrong \n in G54-59 \n ¯\_(ツ)_/¯')