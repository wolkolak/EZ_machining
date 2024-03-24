import numpy as np
from scipy.spatial.transform import Rotation

def my_transform(from_SC, to_SC):#little_SC
    print(f'little_SC = {from_SC}')
    print('to_SC = ', to_SC)
    for i1 in range(6):  # TODO это всё пока выключаем
        from_SC[i1] = from_SC[i1] - to_SC[i1] #+ little_SC[i1]
    print(f'from_SC = {from_SC}')
    euler_angles = from_SC[3:6]#np.array([-45, 0, 0])
    #euler_angles = little_SC[3:6]
    euler_angles_rad = np.radians(euler_angles)
    print(f'euler_angles_rad = {euler_angles_rad}')
    rotation = Rotation.from_euler('xyz', euler_angles_rad)  # .as_matrix()
    point = np.array([from_SC[0], from_SC[1], from_SC[2]])  # ????
    point = rotation.apply(point)
    from_SC[0:3] = point
    print(f'778 point = {from_SC}')
    return from_SC


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
