from OpenGL.GL import *

from Core.Machine_behavior.Draw_fincs_universe_TRJt_factorial_64 import MACHINE_FUNCTIONS
#return_list = [[func, x, y, z, a, b, c, L, tier_c], ..]
#COORDs_T_R
from Core.Machine_behavior.Standart_machine_parts import createJaw, create_gag, create_cylinder_on_table_head_end
from  Core.Machine_behavior.angles_compute_for_machine_parts import aliquot_90_degrees

def choose_draw_JawTier_func(draw_and_return_list, elem_type, place_in_list, jaw, tier, tier1, tier2, jaw_abc,  tier_abc, dx=0., dy=0., dz=0., self=None):

    print('elem_type={}, jaw={}, tier={}'.format(elem_type, jaw, tier))
    if elem_type != 'HeadTable':
        if place_in_list == 0:
            letter = 'A'
        elif place_in_list == 1:
            letter = 'B'
        elif place_in_list == 2:
            letter = 'C'
        else:
            letter = 'N'

        if letter in self.for_45grad_angles:
            if self.table[place_in_list][0] is not None:
                func_0 = MACHINE_FUNCTIONS['Rj'][0]
                func_reverse_0 = MACHINE_FUNCTIONS['Rj'][1]
                func_TransRot_return0 = MACHINE_FUNCTIONS['Rj'][2]
            else:
                func_0 = MACHINE_FUNCTIONS['inverse_Rj'][0]
                func_reverse_0 = MACHINE_FUNCTIONS['inverse_Rj'][1]
                func_TransRot_return0 = MACHINE_FUNCTIONS['inverse_Rj'][2]
            jaw_0 = createJaw(D=40, a=0, b=0, c=0, gauge=70)
            #jaw_0 = create_cylinder_on_table_head_end(R=30, L=50)
            empty_tier = create_gag()
            tier_0 = tier1_0 = tier2_0 = empty_tier
            dx_0 = dy_0 = dz_0 = 0
            jaw_abc_0 = [0., 0., 0.]
            tier_abc_0 = self.for_45grad_angles[letter][0]
            if not self.for_45grad_angles[letter][1]:
                jaw_0 = empty_tier
            #todo во-вторых разобраться передавать ли управление (не здесь очевидно)

            if len(draw_and_return_list) > 0 and draw_and_return_list[-1][0] == MACHINE_FUNCTIONS['HeadTable'][0]:
                draw_and_return_list[-1][2] = empty_tier

            #draw_and_return_list.append([func_0, func_reverse_0, jaw_0, tier_0, tier1_0, tier2_0,  [-dx_0, -dy_0, -dz_0, -jaw_abc_0[0], -jaw_abc_0[1], -jaw_abc_0[2], -tier_abc_0[0], -tier_abc_0[1], -tier_abc_0[2]], func_TransRot_return0])
            draw_and_return_list.append([func_0, func_reverse_0, jaw_0, tier_0, tier1_0, tier2_0, [dx_0, dy_0, dz_0, jaw_abc_0[0], jaw_abc_0[1], jaw_abc_0[2], tier_abc_0[0], tier_abc_0[1], tier_abc_0[2]], func_TransRot_return0])

    print(':::::::::', elem_type)
    print(MACHINE_FUNCTIONS[elem_type])
    func = MACHINE_FUNCTIONS[elem_type][0]
    func_reverse = MACHINE_FUNCTIONS[elem_type][1]
    func_TransRot_return = MACHINE_FUNCTIONS[elem_type][2]
    #draw_and_return_list.append([func, func_reverse, jaw, tier, tier1, tier2, [-dx, -dy, -dz, -jaw_abc[0], -jaw_abc[1], -jaw_abc[2], -tier_abc[0], -tier_abc[1], -tier_abc[2]], func_TransRot_return])#tier_c, -abc[0]
    draw_and_return_list.append([func, func_reverse, jaw, tier, tier1, tier2, [dx, dy, dz, jaw_abc[0], jaw_abc[1], jaw_abc[2], tier_abc[0], tier_abc[1], tier_abc[2]], func_TransRot_return])  # tier_c, -abc[0]
    print('draw_and_return_list current = ', draw_and_return_list[-1])
    return True




#def choose_draw_JawTier_func_NEW(draw_and_return_list, elem_type, place_in_list, jaw, tier, tier1, tier2, jaw_abc,  tier_abc, dx=0., dy=0., dz=0., self=None):
#    #todo потом сделать оптимизацию
#
#    print('elem_type={}, jaw={}, tier={}'.format(elem_type, jaw, tier))
#    if elem_type != 'HeadTable':
#        if place_in_list == 0:
#            letter = 'A'
#        elif place_in_list == 1:
#            letter = 'B'
#        elif place_in_list == 2:
#            letter = 'C'
#        else:
#            letter = 'N'
#
#        if letter in self.for_45grad_angles and not aliquot_90_degrees(self.for_45grad_angles[letter]):
#
#            if self.table[place_in_list][0] is not None:
#                func_0 = MACHINE_FUNCTIONS['Rj'][0]
#                func_reverse_0 = MACHINE_FUNCTIONS['Rj'][1]
#            else:
#                func_0 = MACHINE_FUNCTIONS['inverse_Rj'][0]
#                func_reverse_0 = MACHINE_FUNCTIONS['inverse_Rj'][1]
#            jaw_0 = createJaw(D=40, a=0, b=0, c=0, gauge=70)
#            #jaw_0 = create_cylinder_on_table_head_end(R=30, L=50)
#            empty_tier = create_gag()
#            tier_0 = tier1_0 = tier2_0 = empty_tier
#            dx_0 = dy_0 = dz_0 = 0
#            jaw_abc_0 = [0., 0., 0.]
#            tier_abc_0 = self.for_45grad_angles[letter][0]
#            if not self.for_45grad_angles[letter][1]:
#                jaw_0 = empty_tier
#            #todo во-вторых разобраться передавать ли управление (не здесь очевидно)
#
#            if len(draw_and_return_list) > 0 and draw_and_return_list[-1][0] == MACHINE_FUNCTIONS['HeadTable'][0]:
#                draw_and_return_list[-1][2] = empty_tier
#
#            draw_and_return_list.append([func_0, func_reverse_0, jaw_0, tier_0, tier1_0, tier2_0,  [-dx_0, -dy_0, -dz_0, -jaw_abc_0[0], -jaw_abc_0[1], -jaw_abc_0[2], -tier_abc_0[0], -tier_abc_0[1], -tier_abc_0[2]]])
#
#
#    print(':::::::::', elem_type)
#    print(MACHINE_FUNCTIONS[elem_type])
#    func = MACHINE_FUNCTIONS[elem_type][0]
#    func_reverse = MACHINE_FUNCTIONS[elem_type][1]
#    draw_and_return_list.append([func, func_reverse, jaw, tier, tier1, tier2, [-dx, -dy, -dz, -jaw_abc[0], -jaw_abc[1], -jaw_abc[2], -tier_abc[0], -tier_abc[1], -tier_abc[2]]])#tier_c, -abc[0]
#
#
#    return True