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

        #self.current_g54_g59 = 'G54'#todo на вский случай
        self.open_machine_settings()
        self.ax_order = 'CBA'   # from closest rotate ax around part to the most distant one
                                # Axis from differnt machine parts has no relative order. sort it as u want
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Head', 'LShoulder': 100, 'Order': 1},
                                   'B': {'Place': 'Head', 'LShoulder': 100, 'Order': 2},
                                   'C': {'Place': 'Head', 'LShoulder': 100, 'Order': 3}
                                   }


    def insert_ax_order(self):
        i = 1
        for lit in self.ax_order:
            self.DICT_AX_PARAMETERS[lit]['Order'] = i
            i = + 1

    @classmethod
    def get_home_machine_settings(cls) -> str:
        """
        :return: 'a' is an address of machine_settings.py with slashes, 'a_py_dots' - with dots
        """
        __location__ = sys.modules[cls.__module__].__file__
        __location__ = '\\'.join(__location__.split('\\')[:-1])
        a_ = __location__ + r'\machine_settings'
        a_py = 'Modelling_clay' + a_.split('Modelling_clay')[1]
        a_py_dots = a_py.replace('\\', '.')
        a = a_ + r'.py'
        print('a = {}, a_py_dots = {}'.format(a, a_py_dots))
        return a, a_py_dots

    def open_machine_settings(self):
        a, a_py_dots = self.machine_settings_open, self.machine_settings_import
        print('OPEN: a = {}, a_py_dots = {}'.format(a, a_py_dots))
        try:
            with open(a) as f:
                my_module = importlib.import_module(a_py_dots)
                self.g54_g59_AXIS = my_module.g54_59
                self.start_pointXYZ = my_module.start_pointXYZ
                self.k_XYZABC_list = my_module.k_XYZABC
                self.current_g54_g59 = my_module.current_g54_g59
                #todo we should do something here
            f.close()
            print('self.k_XYZABC_list  = ', self.k_XYZABC_list )
            print('self.g54_g59_AXIS = ', self.g54_g59_AXIS)
        except:
            print('Except in open_machine_settings')
            print('a = ', a)
            with open(a, 'w') as f:
                f.write("g54_59 = {  #ATTENTION: do not change format of the lines by hands. if ypu actually done it, check wenether rewrighting from programm still work\n")
                for n in range(4, 10):
                    f.write("'G5%d': {'X': 0.0, 'Y': 0.0, 'Z': 0.0, 'A': 0.0, 'B': 0.0, 'C': 0.0}, \n" % n)
                f.write('}')
                f.write("start_pointXYZ = [500., 0., 50., 0., 0., 0]")
                f.write("current_g54_g59 = 'G54'")
                f.write("k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}")
            f.close()
            #from .machine_settings import g54_59
            #self.g54_g59_AXIS = g54_59
            my_module = importlib.import_module(a_py_dots)
            self.g54_g59_AXIS = my_module.g54_59

    def save_line_in_machine_settings_py(self, G5N, G_list):
        """Принимает список вида [[name1, value1]...]
        Полностью переписывает файл machine_settings.py"""
        __location__ = sys.modules[self.__module__].__file__
        __location__ = '\\'.join(__location__.split('\\')[:-1])
        a = __location__ + r'\machine_settings.py'
        print('G5N ==== ', G5N)
        new_G5N = "'" + G5N + "'"
        print('new_G5N = ', new_G5N)

        try:
            with fileinput.FileInput(a, inplace=True, backup='.bak') as m_settings:
                for line in m_settings:
                    #gui_classes.simple_warning(new_G5N, line)
                    if re.match('\s*' + new_G5N, line):
                        print("{}: {{'X': {}, 'Y': {}, 'Z': {}, 'A': {}, 'B': {}, 'C': {}}},".format(new_G5N, *G_list)) #, \n
                    else:
                        print(line, end='')
            os.unlink(a + '.bak')
        except OSError:
            gui_classes.simple_warning('Ooh', 'Something went wrong \n in G54-59 \n ¯\_(ツ)_/¯')