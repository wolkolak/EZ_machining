from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ax_order = 'BAC'
        self.m_zero_to_m_1ax_center_CONST = [0., 0., 50.]
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Head', 'LShoulder': 300, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},#seems i dont need the order
                                   'B': {'Place': 'Head', 'LShoulder': 400, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'},
                                   'C': {'Place': 'Head', 'LShoulder': 200, 'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'TRjt'}
                                   }
        self.k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}
        self.collet = {'angle': 0., 'baseR': 60., 'L_from_segment_tip': 0.,
                       'topR': 30., 'h': 70., 'polygons_r': 10, 'polygons_h': 10}
        self.max_table_head_distance = [500., -250., 500.]

        self.insert_ax_order()
