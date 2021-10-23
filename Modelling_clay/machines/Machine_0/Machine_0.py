from abc import ABC
import os
import sys
import fileinput
import re

class Machine(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.open_machine_settings()
        #from .machine_settings import g54_59
        # self.g54_g59_AXIS = g54_59
        self.current_g54_g59 = 'G54'



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

    def open_machine_settings(self):
        print('FFFFF')
        #__location__ = os.path.realpath(
        #    os.path.join(os.getcwd(), os.path.dirname(__file__)))
        __location__ = sys.modules[self.__module__].__file__
        print('__location = ', __location__)
        a = __location__ + r'\machine_settings.py'
        try:
            with open(a) as f:
                from .machine_settings import g54_59
                self.g54_g59_AXIS = g54_59
                #todo we should do something here
            f.close()
            print('self.g54_g59_AXIS = ', self.g54_g59_AXIS)
        except:
            print('Except in open_machine_settings')
            with open(a, 'w') as f:
                f.write("g54_59 = {  #ATTENTION: do not change format of the lines by hands. if ypu actually done it, check wenether rewrighting from programm still work\n")
                for n in range(4,10):
                    f.write("'G5%d': {'X': 0., 'Y': 0., 'Z': 0., 'A': 0., 'B': 0., 'C': 0.}, \n" % n)
                f.write('}')
            f.close()
            from .machine_settings import g54_59
            self.g54_g59_AXIS = g54_59
