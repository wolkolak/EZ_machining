
#from Core.Machine_behavior.machine_transmigrations_forward import RT_ABC, TR_ABC
from Core.Machine_behavior.machine_transmigrations_return import return_TR_CBA, return_RT_CBA, return_RT_inverse_CBA, return_TR_inverse_CBA
from Core.Machine_behavior.machine_transmigrations_forward import TR_ABC, R_ABC, RT_C, RT_ABC

#def move_to_main_G549(v_i, G549shift):
#    print('move_to_main_G549')
#    #pass
#    print('G549shift1 = ', G549shift)
#    #G549shift
#    print('2 v_i = ', v_i)
#    param_list = [G549shift[0], G549shift[1], G549shift[2], None, None, None, G549shift[3], G549shift[4], G549shift[5]]
#    #v_i[4], v_i[5], v_i[6] = return_TR_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
#    # todo сменить в паре
#    v_i[4], v_i[5], v_i[6] = return_RT_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])#todo Так,
#    #v_i[4], v_i[5], v_i[6] = v_i[4] + G549shift[0], v_i[5] + G549shift[1], v_i[6] + G549shift[2]
#    print('1 v_i = ', v_i)
#    return v_i

def move_to_main_G549_new(v_i, G549shift):#TODO работаю здесь для перемещения координаты точки
    print('move_to_main_G549new')
    #k = 1
    #param_list = [k*G549shift[0], k*G549shift[1], k*G549shift[2], None, None, None, k*G549shift[3], k*G549shift[4],
    # k*G549shift[5]]
    param_list = [G549shift[0], G549shift[1], G549shift[2], None, None, None, G549shift[3], G549shift[4], G549shift[5]]
    #param_list = [k * G549shift[0], k * G549shift[1], k * G549shift[2], None, None, None, 0, 0, -90]
    v_i[4], v_i[5], v_i[6] = RT_ABC(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
    print('1 v_i = ', v_i)
    return v_i


def move_from_main_G549(v_i, G549shift):
    #2/0

    print('move_from_main_G549')
    print('G549shift3 = ', G549shift)
    print('2 v_i = ', v_i)
    k = -1
    param_list = [k*G549shift[0], k*G549shift[1], k*G549shift[2], None, None, None, k*G549shift[3], k*G549shift[4], k*G549shift[5]]
    #v_i[4], v_i[5], v_i[6] = return_TR_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
    # todo сменить в паре
    v_i[4], v_i[5], v_i[6] = return_RT_inverse_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])#todo Так,
    #v_i[4], v_i[5], v_i[6] = v_i[4] + G549shift[0], v_i[5] + G549shift[1], v_i[6] + G549shift[2]
    print('1 v_i = ', v_i)
    return v_i


def move_from_main_G549222(v_i, G549shift):
    #2/0

    print('move_from_main_G549')
    print('G549shift3 = ', G549shift)
    print('2 v_i = ', v_i)
    k = -1
    param_list = [k*G549shift[0], k*G549shift[1], k*G549shift[2], None, None, None, k*G549shift[3], k*G549shift[4], k*G549shift[5]]
    #v_i[4], v_i[5], v_i[6] = return_TR_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
    # todo сменить в паре
    v_i[4], v_i[5], v_i[6] = return_TR_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])#todo Так,
    #v_i[4], v_i[5], v_i[6] = v_i[4] + G549shift[0], v_i[5] + G549shift[1], v_i[6] + G549shift[2]
    print('1 v_i = ', v_i)
    return v_i



#def move_from_main_G549_DEPRECIETED(v_i, G549shift):
#    #2/0
#    from Core.Machine_behavior.machine_transmigrations_return import return_RT_C
#    print('move_from_main_G549')
#    print('G549shift3 = ', G549shift)
#    print('2 v_i = ', v_i)
#    k = -1
#    param_list = [k*G549shift[0], k*G549shift[1], k*G549shift[2], None, None, None, k*G549shift[3], k*G549shift[4], k*G549shift[5]]
#    #v_i[4], v_i[5], v_i[6] = return_TR_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])
#    # todo сменить в паре
#    v_i[4], v_i[5], v_i[6] = return_RT_inverse_CBA(param_list=param_list, X=v_i[4], Y=v_i[5], Z=v_i[6])#todo Так,
#    #v_i[4], v_i[5], v_i[6] = v_i[4] + G549shift[0], v_i[5] + G549shift[1], v_i[6] + G549shift[2]
#
#    #self.g54_g59_AXIS_Delta
#    #v_i[4]
#    #G549shift.
#    #v_i[4]
#    print('1 v_i = ', v_i)
#    return v_i