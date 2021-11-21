from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):    #CAB NT6000
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ax_order = 'CAB'
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Head', 'LShoulder': 100, 'Order': 1},
                                   'B': {'Place': 'Head', 'LShoulder': 100, 'Order': 2},
                                   'C': {'Place': 'Table', 'LShoulder': 100, 'Order': 3}
                                   }
        self.insert_ax_order()

