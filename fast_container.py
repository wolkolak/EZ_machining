import numpy as np

line_numbers = 10
columns = 2


a = np.array([  [-1,  0,  0,  0,],
                [ 2, 40, 41,  2,]])
#delete 2
#min_L = np.searchsorted(a, 2)
#max_L = np.searchsorted(a, 2)


#a = np.delete(a, np.s_[min_L:max_L + 1], axis=0)#here
L = 1
print('a = ', a)
a[min_line + L:-1, 0] = a[min_line + L:-1, 0] + L
print('a = ', a)
#b = np.array([8])
#a = np.insert(a, 1, b, axis=0)
#print(a)