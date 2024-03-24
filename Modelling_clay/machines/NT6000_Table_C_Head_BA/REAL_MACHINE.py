from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):    #CAB NT6000
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('REAL_MACHINE CAB NT6000')
        self.ax_order = 'CBA'

        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Head', 'LShoulder': 60,     'j_angle': [0., 0., 0.], 't_angle': [-90., 0., 0.],      'local_order': 'inverse_Rt'},# it can be None or anything really
                                   'B': {'Place': 'Head', 'LShoulder': 302.,    'j_angle': [0., 0., 0.], 't_angle': [90.,  0., -90.],    'local_order': 'inverse_RtT'},
                                   'C': {'Place': 'Table', 'LShoulder': 200,   'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.],        'local_order': 'jRtT'}
                                   }
        self.animation_line_ax_order = 'XZY'

        self.collet = {'angle': 0.,  'baseR': 60.,
                       'topR': 30., 'h': 70., 'polygons_r': 20, 'polygons_h': 10}
        self.k_XYZABC = {'X': 0.5, 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}
        l = self.DICT_AX_PARAMETERS['C']['LShoulder']
        self.m_zero_to_m_1ax_center_CONST = [1100., -l, -50.]  # todo Это машинный ноль
        self.XYZABC_ADD = [0., -l, 0., 0., 0., 0.]
        self.max_table_head_distance = [2000., 330.-l, 6076.]#660/330
        self.min_table_head_distance = [-500., -330-l, 0.]
        self.insert_ax_order()

        self.analyze_dict = {'Dmax': 1070, 'Lmax': 6076, 'Smax': 1500, 'smax': 8000}



