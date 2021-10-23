from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class CBA_Table(Machine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ax_order = 'CBA'
        self.insert_ax_order()
