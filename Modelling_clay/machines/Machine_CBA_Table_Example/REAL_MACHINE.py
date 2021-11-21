from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.ax_order = 'CBA'
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Table', 'LShoulder': 100, 'Order': 1},
                                   'B': {'Place': 'Table', 'LShoulder': 100, 'Order': 2},
                                   'C': {'Place': 'Table', 'LShoulder': 100, 'Order': 3}
                                   }
        self.insert_ax_order()
