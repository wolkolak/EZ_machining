import numpy as np
from scipy.spatial.transform import Rotation

def my_transform(from_SC, to_SC):#little_SC
    from_SC = [from_SC[i1] - to_SC[i1] for i1 in range(6)]
    euler_angles_rad = from_SC[3:6]
    rotation = Rotation.from_euler('xyz', euler_angles_rad)
    print(f'my_transform from_SC = {from_SC}')
    fff = rotation.apply(np.array([from_SC[0], from_SC[1], from_SC[2]]))


    from_SC[0:3] = fff
    print(f'from_SC = {from_SC}')
    #print(f'why not list? {type(from_SC)}')
    return from_SC

def my_transform_return(from_SC, to_SC):#little_SC
    print(f'dot in 1st SC = {from_SC}')
    print('to_SC = ', to_SC)
    euler_angles_rad = to_SC[3:6]
    rotation = Rotation.from_euler('xyz', euler_angles_rad)  # порядок почему то сохраненю А почему? Потому что это порядок вставки данных, наверное
    from_SC[0:3]= rotation.apply(np.array([from_SC[0], from_SC[1], from_SC[2]]))  # ????
    from_SC =[from_SC[i1] + to_SC[i1] for i1 in range(3)] #+ little_SC[i1]
    #print(print(f'77 why not list? {type(from_SC[0:3])}'))
    return from_SC[0:3]

def projection(p,a):
    lambda_val = np.dot(p,a)/np.dot(a,a)
    return p - lambda_val * a


#def angles2vector(np_arr_angls:np.array):
#    a =
#    return

def my_transform_R_T(from_SC, to_SC):#Не пользуюсь
    print(f'little_SC = {from_SC}')
    #euler_angles = np.array([45, 0, 0])
    euler_angles = from_SC[3:6]
    euler_angles_rad = np.radians(euler_angles)
    print(f'euler_angles_rad = {euler_angles_rad}')
    rotation = Rotation.from_euler('xyz', euler_angles_rad)  # .as_matrix()
    point = np.array([from_SC[0], from_SC[1], from_SC[2]])  # ????
    point = rotation.apply(point)
    from_SC[0:3] = point
    print(f'778 point = {from_SC}')

    for i1 in range(6):  # TODO это всё пока выключаем
        from_SC[i1] = from_SC[i1] - to_SC[i1] #+ little_SC[i1]
    return from_SC






import math
from Core.Machine_behavior.machine_transmigrations_forward import R_C, R_C_radians

def C_ROT_1(np_line, ark_np_array, n, alpha_segmenta, starting_angle, p_, x_step, y_step, z_step, new_coord_const, machine_center_now, last_significant_line):
    #TODO ПОЗЖЕ!
    if x_step == y_step == z_step == 0:
        for k in range(n):
            resulting_angle = -alpha_segmenta * k + starting_angle
            p_[8] = resulting_angle
            new_coord = R_C_radians(p_, new_coord_const[0] + k * x_step, new_coord_const[1] + k * y_step, new_coord_const[2] + k * z_step, )
            new_coord = list(new_coord)
            ark_np_array[k, 17:20] = my_transform_return(from_SC=new_coord, to_SC=machine_center_now)  # TODO Надо радианы
            ark_np_array[k, 16] = 5.
            ark_np_array[k, 9] = resulting_angle

    else:
        np_line_const = np.copy(np_line)
        #np_line[7] = 0
        #np_line[8] = 0
        #np_line[9] = 0
        cur_dot = np_line[4:10]

        print(f'|||| x_step = {x_step}, y_step = {y_step}, z_step = {z_step}')
        for k in range(n):
            #print()
            cur_dot[0] = last_significant_line[4] + k * x_step#/10
            cur_dot[1] = last_significant_line[5] + k * y_step#/10
            cur_dot[2] = last_significant_line[6] + k * z_step#/10
            print(f'333 cur_dot = {cur_dot}')
            new_coord_const = my_transform(from_SC=cur_dot, to_SC=machine_center_now)
            print(f'00new_coord_const = {new_coord_const}')
            new_coord_const[3] = np_line_const[7]
            new_coord_const[4] = np_line_const[8]
            new_coord_const[5] = np_line_const[9]
            #p_[8] = np_line_const[9]


            resulting_angle = -alpha_segmenta * k + starting_angle
            p_[8] = resulting_angle

            print('222 resulting angle = ', resulting_angle)
            print('11new_coord_const[0] = ', new_coord_const[0])
            print('new_coord_const = ', new_coord_const)
            print('new_coord_const[0] + k * y_step = ', new_coord_const[0] + k * y_step)
            что то не так
            new_coord = R_C_radians(p_, new_coord_const[0] + k * x_step, new_coord_const[1] + k * y_step, new_coord_const[2] + k * z_step, )
            print('222 new_coord = ', new_coord)
            new_coord = list(new_coord)
            ark_np_array[k, 17:20] = my_transform_return(from_SC=new_coord, to_SC=machine_center_now)  # TODO Надо радианы
            ark_np_array[k, 16] = 5.
            ark_np_array[k, 9] = resulting_angle
    return ark_np_array