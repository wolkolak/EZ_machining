#from machine_transmigrations import reverseCOORDs_T_R, reverseCOORDs_R_T, reverseCOORDs_R_T_Rc, reverseCOORDs_HeadTable
#from Draw_fucs import COORDs_Rc_T_R, COORDs_T_R, COORDs_R_T, COORDs_TableHead
from Core.Machine_behavior.Draw_fincs_universe_TRJt_factorial_64 import HeadTable#, HeadTableR
from Core.Machine_behavior.choose_draw_funcs import choose_draw_JawTier_func#, choose_draw_JawTier_func_NEW
from Core.Machine_behavior.Standart_machine_parts import createJaw, create_gag, create_cylinder_on_table_head_end
from Core.Machine_behavior.angles_compute_for_machine_parts import create_connection
#from Core.Machine_behavior.add_for_45_issues import moveJawFromTHto45HeadElement
from Core.Machine_behavior.SC_machine_parts import create_M0_CONST, create_M0_VARIANT, create_TOOL_change_point1, create_TOOL_change_point2, create_PART_draw_SC, create_MACHINING_SC, create_POLAR_SC, create_SMALL_SC
import copy
from Core.Machine_behavior.MachiningSCpreparation import give_G549_shifts
from Core.Machine_behavior.G549_coords import Display_G549_places


def assemble_functions_to_draw_machine(self):#todo Сюда нужно добавить связи списка значений осей с общим списком отображения
    """
    choosing functions to create machine
    :return:
    """
    #self.self.start_count = 0
    order = self.ax_order  # 'CAB'
    parts_in_order = {}
    dx = self.max_table_head_distance[0] - self.min_table_head_distance[0]
    dy = self.max_table_head_distance[1] - self.min_table_head_distance[1]
    dz = self.max_table_head_distance[2] - self.min_table_head_distance[2]
    X_balk, Y_balk, Z_balk = create_connection(dx, dy, dz, self)



    self.special_machine_points = {'M0_CONST': create_M0_CONST(self), 'M0_VARIANT': create_M0_VARIANT(self),  'TOOL_POINT1': create_TOOL_change_point1(self), 'TOOL_POINT2': create_TOOL_change_point2(self),
                                   'PART_SC': create_PART_draw_SC(self), 'MACHINING_SC': create_MACHINING_SC(self), 'POLAR_SC': create_POLAR_SC(self), 'SMALL_SC': create_SMALL_SC(self)}

    #delta_x = self.XYZABC_ADD[0];    delta_y = self.XYZABC_ADD[1];    delta_z = self.XYZABC_ADD[2]

    dx = self.offset_pointXYZ[0] + self.m_zero_to_m_1ax_center_CONST[0] #+ delta_x
    dy = self.offset_pointXYZ[1] + self.m_zero_to_m_1ax_center_CONST[1] #+ delta_y
    dz = self.offset_pointXYZ[2] + self.m_zero_to_m_1ax_center_CONST[2] #+ delta_z
    #dx = delta_x;    dy = delta_y;    dz = delta_z
    len_order = len(order)
    start_count = 0
    head_start = 0

    #func0 = 'G549'
    #add_JawTier_table_to_list(self, func0, place_in_list=-100)


    for l in range(len_order):  # 'CAB'
        if order[l] == 'A':
            n = 0
        elif order[l] == 'B':
            n = 1
        else:  # C
            n = 2
        if self.table[n][0] is not None:
            thing = 'Table'
        elif self.head[n][0] is not None:
            thing = 'Head'
        else:
            thing = None
        if thing is not None:
            parts_in_order[order[l]] = thing
    # Table
    func1 = None
    func2 = None
    func3 = None
    func_transfer_happened = False
    dy_tab_prev = 0.
    # Rotate_coordinates
    if len_order >= 1:
        # смести углы стола. мб сработает
        if order[0] == 'A' and parts_in_order['A'] == 'Table':  # first lit in CAB
            func1, place_in_list = self.A_table_function, 0
        elif order[0] == 'B' and parts_in_order['B'] == 'Table':
            func1, place_in_list = self.B_table_function, 1
        elif order[0] == 'C' and parts_in_order['C'] == 'Table':
            func1, place_in_list = self.C_table_function, 2
        elif func_transfer_happened == False:
            func_transfer_happened = True
            place_in_list = None
            add_Table_head_to_list(self, func1, place_in_list, dx, dy, dz, X_balk, Y_balk, Z_balk)
        if func1 is not None:
            add_JawTier_table_to_list(self, func1, place_in_list=place_in_list)#todo не те x y z
            head_start += 1
    # ____________________

    if len_order >= 2:
        if order[1] == 'A' and parts_in_order['A'] == 'Table':
            func2, place_in_list = self.A_table_function, 0
        elif order[1] == 'B' and parts_in_order['B'] == 'Table':
            func2, place_in_list = self.B_table_function, 1
        elif order[1] == 'C' and parts_in_order['C'] == 'Table':
            func2, place_in_list = self.C_table_function, 2
        elif func_transfer_happened == False:
            func_transfer_happened = True
            place_in_list = None
            add_Table_head_to_list(self, func2, place_in_list, dx, dy, dz, X_balk, Y_balk, Z_balk)
        if func2 is not None:
            add_JawTier_table_to_list(self, func1, place_in_list=place_in_list)
            head_start += 1
    # _____________________

    if len_order >= 3:
        if order[2] == 'A' and parts_in_order['A'] == 'Table':
            func3, place_in_list = self.A_table_function, 0
        elif order[2] == 'B' and parts_in_order['B'] == 'Table':
            func3, place_in_list = self.B_table_function, 1
        elif order[2] == 'C' and parts_in_order['C'] == 'Table':
            func3, place_in_list = self.C_table_function, 2
        elif func_transfer_happened == False:
            func_transfer_happened = True
            place_in_list = None
            add_Table_head_to_list(self, func3, place_in_list, dx, dy, dz, X_balk, Y_balk, Z_balk)
        if func3 is not None:
            add_JawTier_table_to_list(self, func1, place_in_list=place_in_list)
            head_start += 1
    # _______________________

    # Head
    func4 = None
    func5 = None
    func6 = None

    print('head_start = ', head_start)

    if len_order >= 1:
        if order[0] == 'A' and parts_in_order['A'] == 'Head':  # first lit in CAB
            func4, place_in_list = self.A_head_function, 0
        elif order[0] == 'B' and parts_in_order['B'] == 'Head':
            func4, place_in_list = self.B_head_function, 1
        elif order[0] == 'C' and parts_in_order['C'] == 'Head':
            func4, place_in_list = self.C_head_function, 2
        if func4 is not None:
            add_JawTier_head_to_list(self, func4, place_in_list=place_in_list)
    # _______________________
    if len_order >= 2:
        if order[1] == 'A' and parts_in_order['A'] == 'Head':  # first lit in CAB
            func5, place_in_list = self.A_head_function, 0
        elif order[1] == 'B' and parts_in_order['B'] == 'Head':
            func5, place_in_list = self.B_head_function, 1
        elif order[1] == 'C' and parts_in_order['C'] == 'Head':
            func5, place_in_list = self.C_head_function, 2
        if func5 is not None:
            add_JawTier_head_to_list(self, func5, place_in_list=place_in_list)
    # ____________________
    if len_order >= 3:
        if order[2] == 'A' and parts_in_order['A'] == 'Head':  # first lit in CAB
            func6, place_in_list = self.A_head_function, 0
        elif order[2] == 'B' and parts_in_order['B'] == 'Head':
            func6, place_in_list = self.B_head_function, 1
        elif order[2] == 'C' and parts_in_order['C'] == 'Head':
            func6, place_in_list = self.C_head_function, 2
        if func6 is not None:
             add_JawTier_head_to_list(self, func6, place_in_list=place_in_list)

    CurrentAXDict_old = {}
    NewMorder = order[:head_start] + 'M' + order[head_start:]
    print('NewMorder = ', NewMorder)
    str_xyzabc = 'XYZABC'
    for l in range(len(NewMorder)):
        if NewMorder[l] in str_xyzabc:
            if NewMorder[l] in self.for_45grad_angles and not self.for_45grad_angles[NewMorder[l]][1]:# and not aliquot_90_degrees(self.for_45grad_angles[NewMorder[l]][0]):
                start_count += 1
            numb = str_xyzabc.index(NewMorder[l])#-1
            self.machine_draw_list[l + start_count][6][8] += self.XYZABC_ADD[numb]

        if NewMorder[l] == 'M' and self.machine_draw_list[l + start_count][0] is not HeadTable:# and something
            start_count += 1
        CurrentAXDict_old[NewMorder[l]] = self.machine_draw_list[l + start_count][6]#
        if NewMorder[l] in self.for_45grad_angles and self.for_45grad_angles[NewMorder[l]][1]:# and not aliquot_90_degrees(self.for_45grad_angles[NewMorder[l]][0]):
            start_count += 1

    #достроить тут до выбора верной ячейки при дополнительном элементе 45 градусов

    CurrentAXDict = {}
    print('ЗДЕСЬ: CurrentAXDict_old: ', CurrentAXDict_old)
    CurrentAXDict['X'] = [CurrentAXDict_old['M'], 0]
    CurrentAXDict['Y'] = [CurrentAXDict_old['M'], 1]
    CurrentAXDict['Z'] = [CurrentAXDict_old['M'], 2]
    CurrentAXDict_old.pop('M')
    #after_M_let = NewMorder[self.head_start + 1 - start_count]
    print('CurrentAXDict_old = ', CurrentAXDict_old)
    for let in CurrentAXDict_old:
        place = 8
        CurrentAXDict[let] = [CurrentAXDict_old[let], place]
    self.CurrentAXDict = CurrentAXDict
    print('|||| draw_and_return_list = ', self.machine_draw_list)
    self.machine_start_configuration = copy.deepcopy(self.machine_draw_list)

    if self.frame.left_tab.parent.central_widget.note.currentIndex() == -1:
        machine_item = self.frame.left_tab.parent.central_widget.note.default_machine_item  # ??????????????????
    else:
        machine_item = self.frame.left_tab.parent.central_widget.note.currentWidget().current_machine
    self.g54_g59_AXIS = machine_item.g54_g59_AXIS
    self.g54_g59_AXIS_Display, self.g54_g59_AXIS_Delta = Display_G549_places(self)
    #self.cycle800_AXIS_Display = []
    print('machine_item G549 = ', machine_item.g54_g59_AXIS)
    print('self.g54_g59_AXIS_Delta = ', self.g54_g59_AXIS_Delta)
    print('g54_g59_AXIS_Display = ', self.g54_g59_AXIS_Display)


    self.after_draw_return_list = []

    #current_XYZABC = []
    self.count_machine_op = len(self.machine_draw_list)
    i = 0
    for op in self.machine_draw_list:
        if op[0] is HeadTable:# or op[0] is HeadTableR
            self.Table_Head_place = i
        print('op = ', op)
        op[1], op_8 = op[1](op[6][6:9])
        op.append(op_8)
        return_op = [op[1], op[6], op[7]]
        #return_op[2] = return_op[2](return_op[1][6:9])
        self.after_draw_return_list.append(return_op)
        i+=1
    self.after_draw_return_list.reverse()

    self.DICT_G549shift = give_G549_shifts(self, machine_item)
    print('DICT_G549shift  = ', self.DICT_G549shift)




def add_JawTier_table_to_list(self, func1, place_in_list):
    #elem_type = 'Table'
    print('self.table ========= ', self.table)
    elem_type = self.table[place_in_list][4]
    print(elem_type)
    y = self.table[place_in_list][1]
    x = 0;    z = 0
    Jaw_angles = self.table[place_in_list][3]
    dy_tab_prev = y
    a, b, c = Jaw_angles#self.START_angles[i]

    jaw = createJaw(dy_tab_prev, a=a, b=b, c=c, gauge=10)
    tier = self.table[place_in_list][0]
    print('5454 tier = ', tier)
    print(type(tier))
    jaw_abc, tier_c = func1(self, dy_tab_prev, place_in_list)
    tier_abc = self.table[place_in_list][3]
    #tier_abc[2] += 55
    choose_draw_JawTier_func(draw_and_return_list=self.machine_draw_list, elem_type=elem_type, place_in_list=place_in_list, jaw=jaw, tier=tier, tier1=0, tier2=0,
                             jaw_abc=jaw_abc, tier_abc=tier_abc, dx=x, dy=y, dz=z, self=self)#tier_abc
    #choose_draw_JawTier_func_NEW(draw_and_return_list=self.draw_and_return_list, elem_type=elem_type, place_in_list=place_in_list, jaw=jaw, tier=tier, tier1=0, tier2=0,
    #                         jaw_abc=jaw_abc, tier_abc=tier_abc, dx=x, dy=y, dz=z, self=self)#tier_abc

def add_JawTier_head_to_list(self, func1, place_in_list):#, angle
    elem_type = self.head[place_in_list][4]
    y = self.head[place_in_list][1]
    x = 0; z = 0
    jaw = create_gag(0, 0, 0, 0, 0)
    tier = self.head[place_in_list][0]
    dy_tab_prev = y
    jaw_abc, tier_c = func1(self, dy_tab_prev, place_in_list)
    tier_abc = self.head[place_in_list][3]
    choose_draw_JawTier_func(draw_and_return_list=self.machine_draw_list, elem_type=elem_type, place_in_list = place_in_list, jaw=jaw, tier=tier, tier1=0, tier2=0,
                             jaw_abc=jaw_abc, tier_abc=tier_abc, dx=x, dy=y, dz=z, self=self)


def add_Table_head_to_list(self, func, place_in_list, dx, dy, dz, X_balk, Y_balk, Z_balk):

    tier = X_balk; tier1 = Y_balk; tier2 = Z_balk
    if self.animation_line_ax_order[0] == 'X':
        f0 = 0
    if self.animation_line_ax_order[0] == 'Y':
        f0 = 1
    if self.animation_line_ax_order[0] == 'Z':
        f0 = 2
    if self.animation_line_ax_order[1] == 'X':
        f1 = 0
    if self.animation_line_ax_order[1] == 'Y':
        f1 = 1
    if self.animation_line_ax_order[1] == 'Z':
        f1 = 2
    if self.animation_line_ax_order[2] == 'X':
        f2 = 0
    if self.animation_line_ax_order[2] == 'Y':
        f2 = 1
    if self.animation_line_ax_order[2] == 'Z':
        f2 = 2

    jaw_abc = [f0, f1, f2]

    #if 'M' in self.for_45grad_angles:
    #    print('M happened')
    #    elem_type = 'HeadTableR'
    #    tier_abc = self.for_45grad_angles['M'][0]
    #    jaw = create_cylinder_on_table_head_end(how_to_rotate=jaw_abc)
    #else:
    #    elem_type = 'HeadTable'
    #    tier_abc = [0., 0., 0.]
    #    jaw = create_cylinder_on_table_head_end(how_to_rotate=jaw_abc)
    if 'M' in self.for_45grad_angles:
        print('M happened')
        #elem_type0 = 'HeadTableR'
        elem_type0 = 'R'
        tier_abc0 = self.for_45grad_angles['M'][0]
        jaw0 = tier0 = tier10 = tier20 = create_gag()
        dx0 = dy0 = dz0 = 0
        choose_draw_JawTier_func(draw_and_return_list=self.machine_draw_list, elem_type=elem_type0,  place_in_list=place_in_list, jaw=jaw0, tier=tier0, tier1=tier10, tier2=tier20,
                                 jaw_abc=jaw_abc, tier_abc=tier_abc0, dx=dx0, dy=dy0, dz=dz0, self=self)

    elem_type = 'HeadTable'
    tier_abc = [0., 0., 0.]
    jaw = create_cylinder_on_table_head_end(how_to_rotate=jaw_abc)
    choose_draw_JawTier_func(draw_and_return_list=self.machine_draw_list, elem_type=elem_type, place_in_list=place_in_list, jaw=jaw, tier=tier, tier1=tier1, tier2=tier2,
                             jaw_abc=jaw_abc, tier_abc=tier_abc, dx=dx, dy=dy, dz=dz, self=self)


