from Modelling_clay.machines.Machine_0.Machine_0 import Machine

class REAL_MACHINE(Machine):    #BA
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ax_order = 'BAC'
        #self.m_zero_to_m_1ax_center_CONST = [1110., -250., 0.]
        self.m_zero_to_m_1ax_center_CONST = [0., 300., 0.]

        self.DICT_AX_PARAMETERS = {'A': {'Place': 'Table',  'LShoulder': 800,    'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'tTR'},# it can be None or anything really
                                   'B': {'Place': 'Table',  'LShoulder': 701,    'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'jRtT'},
                                   'C': {'Place': 'Head',   'LShoulder': 60,     'j_angle': [0., 0., 0.], 't_angle': [0., 0., 0.], 'local_order': 'inverse_R'}
                                   }
        lx = self.DICT_AX_PARAMETERS['B']['LShoulder']
        self.animation_line_ax_order = 'ZYX'
        self.k_XYZABC = {'X': 1., 'Y': 1., 'Z': 1., 'A': 1., 'B': 1., 'C': 1.}
        self.XYZABC_ADD = [-lx, 0, 0., 0., -90., -90.]
        self.collet = {'angle': 180., 'baseR': 50.,#L_from_segment_tip убрать совсем
                       'topR': 50., 'h': 200., 'polygons_r': 20, 'polygons_h': 10}
        self.for_45grad_angles = {'B': [[-90., 0, 0.], False], 'A': [[90., 0, 0.], False], 'M': [[0., 90, 0.], False]}#M - не случайна. нельзя от балды менять
        self.max_table_head_distance = [800.-lx, 2000., 2500.]
        self.min_table_head_distance = [-800.-lx, 0., 0.]
        self.insert_ax_order()

        self.analyze_dict = {'Dmax': 1070, 'Lmax': 6076, 'Smax': 1500, 'smax': 8000}