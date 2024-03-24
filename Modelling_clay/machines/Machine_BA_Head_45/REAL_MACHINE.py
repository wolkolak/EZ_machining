from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ax_order = 'CBA'
        self.m_zero_to_m_1ax_center_CONST = [0., 0., 50.]#todo Это влияет на вращение осей напрямую
        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Head', 'LShoulder': 60,   'j_angle': [0., 0., 0.], 't_angle': [-90., 0., 0.],'local_order': 'inverse_Rt'},#seems i dont need the order
                                   'B': {'Place': 'Head', 'LShoulder': 400,   'j_angle': [0., 0., 0.], 't_angle': [45., 0., 0.],'local_order': 'inverse_RtT'},#[0., 45., 90.],
                                   'C': {'Place': 'Table', 'LShoulder': 800,  'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.],'local_order': 'jRtT'}
                                   }
        l = self.DICT_AX_PARAMETERS['C']['LShoulder']
        self.XYZABC_ADD = [0., -l, 0., 180., -180., 0.]
        self.for_45grad_angles = {'B': [[135., 0, 0.], True]}
        self.k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}

        self.min_table_head_distance = [-500., -330 - l, 0.]
        self.max_table_head_distance = [670., 500., 2200.]

        self.animation_line_ax_order = 'XZY'
        self.collet = {'angle': 0., 'baseR': 60.,
                       'topR': 30., 'h': 70., 'polygons_r': 10, 'polygons_h': 10}


        self.insert_ax_order()
