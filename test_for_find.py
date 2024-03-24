from mathematic.geometry import find_center

#find center,
dot1 = [25.000000047115485, 23.079755108707353] # -0.01
dot2 = [25.0, 23.078220255350043]
r = 25.
d_f1, d_f2 = find_center(dot1, dot2, r)
print('d_f1 = {}, d_f2 = {}'.format(d_f1, d_f2))