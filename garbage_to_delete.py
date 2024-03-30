import numpy as np
import math
from Core.Data_solving.summirizer import RT_ABC_many_dots, curentSC_4_many_dots22#, trans_matrix_from_SC

def trans_matrix_from_SC(G549):
    ox, oy, oz = G549[0:3]
    ax, ay, az = G549[3:]
    ax = math.radians(ax)
    ay = math.radians(ay)
    az = math.radians(az)
    translation_matrix = np.array([[1, 0, 0, ox],
                                   [0, 1, 0, oy],
                                   [0, 0, 1, oz],
                                   [0, 0, 0, 1]])

    rotation_matrix_x = np.array([[1, 0, 0, 0],
                                  [0, np.cos(ax), -np.sin(ax), 0],
                                  [0, np.sin(ax), np.cos(ax), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_y = np.array([[np.cos(ay), 0, np.sin(ay), 0],
                                  [0, 1, 0, 0],
                                  [-np.sin(ay), 0, np.cos(ay), 0],
                                  [0, 0, 0, 1]])

    rotation_matrix_z = np.array([[np.cos(az), -np.sin(az), 0, 0],
                                  [np.sin(az), np.cos(az), 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

    transformation_matrix = np.dot(np.dot(rotation_matrix_z, rotation_matrix_y), rotation_matrix_x)
    transformation_matrix = np.dot(translation_matrix, transformation_matrix)


    #trans_matr_sum = transformation_matrix#np.dot(transformation_matrix, translation_matrix)

    trans_matr_sum = np.eye(4)
    trans_matr_sum[:3, 3] = G549[0:3]
    return trans_matr_sum


G549 = [500.0, 10.0, 400.0, 10.0, 0.0, 0.0]
X = 100.; Y = 150; Z = 200
sign = 1
param_list = [sign * G549[0], sign * G549[1], sign * G549[2], None, None, None, sign * G549[3], sign * G549[4], sign * G549[5]]
print(f' RT_ABC_many_dots = {RT_ABC_many_dots(param_list, X, Y, Z)}')

new_G549_matrix = trans_matrix_from_SC(G549=G549)
total = np.array([[X, Y, Z, 1.]])
print('тип ', total.dtype)
print(f'new_G549_matrix = {new_G549_matrix}')
print(f'total = {total}')

ax, ay, az = G549[3:]
ax = math.radians(ax)
ay = math.radians(ay)
az = math.radians(az)

rotation_matrix_x = np.array([[1, 0, 0, 0],
                              [0, np.cos(ax), -np.sin(ax), 0],
                              [0, np.sin(ax), np.cos(ax), 0],
                              [0, 0, 0, 1]])

#print(f'1 res = {total.dot(new_G549_matrix)}')
print(f'2 res = {rotation_matrix_x.dot(new_G549_matrix.dot(total.T))}')
print(f'3 res = {rotation_matrix_x.dot(new_G549_matrix.dot(total.T))}')