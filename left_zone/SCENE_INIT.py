from Settings.settings import *
import numpy as np
from Core.Machine_behavior.MachiningSCpreparation import give_G549_shifts



def init_vars(self):
    self.animationMode = 'edit'  # , 'look', 'check'
    self.current_dot_Mark = 1
    self.previous_dot_Mark = 0
    self.old_horizo_mouse = 0
    self.old_height_mouse = 0
    self.old_depth = 1
    self.m_grabbing = False
    self.m_turning = False
    self.cam_horizontal = 0
    self.cam_height = 0
    self.turn_angle = 0
    self.k_rapprochement = 1.0
    self.cam_depth = 1
    self.w = self.width() - 2  # maybe it will work faster
    self.h = self.height()
    self.old_h = self.height()
    self.where_clicked_x = 0
    self.where_clicked_y = 0
    self.turn_angleX = 0
    self.turn_angleY = 0
    self.turn_angleZ = 0
    self.draft_scale = self.scaling_draft_prime * self.k_rapprochement
    self.refresh()
    self.typing_height = 0.8
    self.current_tool = default_tool
    self.tool_list = {}
    self.head_start = 0  # если отсюда не потребуется брать, то вынести в assemble_machine_connections
    self.CurrentAXDict = {}
    self.tip_way_func = None
    self.ERROR_lines = []
    self.frame_address_in_visible_pool = np.zeros((1, 2), int)
    self.show_intermediate_dots = False
    self.X_balk = None
    self.Table_Head_place = 0
    self.count_machine_op = 0
    self.DICT_G549shift = {}
    #print('self.DICT_G549shift = ', self.DICT_G549shift)
    # self.machine_zero_variant = [0, 0, 0]
    # self.change_TOOL_point1 = [0., 0., 0]
    # self.change_TOOL_point2 = [111., 0., 0]