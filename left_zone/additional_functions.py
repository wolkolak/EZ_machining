import math
import numpy as np
import importlib
from Modelling_clay.machine_tools.__init__ import *
from OpenGL.GL import *



def read_tool_file(address):
    """
    can take any tool file. working only for vars with '='
    :return:
    """
    with open(address) as f:
        lines = f.readlines()
    properties_dict = {}
    for line in lines:
        n = line.find('=')
        if n != -1:
            key = line[:n]
            value = line[n+1:]
            if value != None:
                try:
                    value = float(value)
                except:
                    if value.endswith('\n'):
                        value = value[:-1]
            properties_dict[key] = value
    return properties_dict


def choose_tool_function(self, p_dict):

    print('TYPE of tool: ', p_dict['TYPE'])
    str1 = "Modelling_clay.machine_tools." + p_dict['TYPE'] + ".__init__"
    module_real = importlib.import_module(str1)
    self.tool_function = module_real.init__tool
    self.tip_way_func = module_real.tip_tool_way








