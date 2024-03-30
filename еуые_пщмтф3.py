import numpy as np
import math

coords = np.array([4., 2., 1])

alpha = math.radians(33.69)

transform = np.array([
    [math.cos(alpha),     math.sin(alpha),         0],
    [-math.sin(alpha),     math.cos(alpha),          0],
    [-3,             6,          1]])#-0.83,             -6.656
#print(coords.dot(transform))
#print('____________')
transform_inv = np.linalg.inv(transform)
print(f'inverse = {transform_inv}')
print('_________через inverse_______')
nyak1 = coords.dot(transform_inv )
print(nyak1)

#alpha = math.radians(-60.26)
#matrixDfromB = np.array([
#    [math.cos(alpha),     math.sin(alpha),         0],
#    [-math.sin(alpha),     math.cos(alpha),          0],
#    [6.6,             -10.2,          1]])
#
#matrixDfromB_inv  = np.linalg.inv(matrixDfromB )
#print('_________через inverse_2_____')
#print(nyak1.dot(matrixDfromB_inv ))  # [-4.08065662 -1.11733933  1.        ]
##print(f'right answe =   1.424 -5.646  1.')
#
#itog_matrix = matrixDfromB.dot(transform)
#itog_matrix_inv = np.linalg.inv(itog_matrix)
#print('_________________')
#print(coords.dot(itog_matrix_inv))


print('____________')
h1 = np.array([
    [math.cos(alpha),     math.sin(alpha),         0],
    [-math.sin(alpha),     math.cos(alpha),          0],
    [-3,             6,          1]])

h2 = h1.T
print(f'h2 = {h2}')

print('________')
print(h1.dot(h2))
print('__________')
print(h2.dot(h1))