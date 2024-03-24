from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.ax_order = 'CBA'
        self.m_zero_to_m_1ax_center_CONST = [0., 0., 0.]
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Table', 'LShoulder': 100, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},
                                   'B': {'Place': 'Table', 'LShoulder': 201, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},
                                   'C': {'Place': 'Table', 'LShoulder': 302, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'}
                                   }
        self.k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}
        self.collet = {'angle': 0., 'baseR': 60., 'L_from_segment_tip': 550.,
                       'topR': 30., 'h': 70., 'polygons_r': 10, 'polygons_h': 10}
        self.max_table_head_distance = [1500., -250., 500.]
        self.insert_ax_order()
