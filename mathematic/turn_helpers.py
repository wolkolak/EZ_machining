import math
from mathematic.arithmetic import equation_root, min_None, max_None
from mathematic.geometry import find_center
from mathematic.tragectory import Tragectory_3D_one_direction


def takeZl_Zr_from_groove1(DCurr, l_1, r_1, param, tool, Radd):
    #coord_list = [[x1, y1, z1, R, 'G2'], [x2', y2', z2', -R', 'G3'], ...]
    Z_L = None; Z_R = None
    if DCurr > l_1[0][0]:
        print('Z_L != None')
        Z_L = l_1[0][1]
    if DCurr > r_1[0][0]:
        print('Z_R != None')
        Z_R = r_1[0][1]
    DCurr = DCurr / 2
    l_ = l_1.copy()
    r_ = r_1.copy()

    for n in range(len(l_)):
        R = 0; move = None
        if n == 1:
            if param['TopFRl'][0] == 'R':
                R = param['TopFRl'][1] + Radd; move = 'G2'
        elif n == 3:
            if param['BotFRl'][0] == 'R':
                R = param['BotFRl'][1] - Radd; move = 'G3'
        l_[n] = [l_[n][0]/2, 0, l_[n][1], R, move]
    l_track = Tragectory_3D_one_direction(l_, plane='G18')
    for n in range(len(r_)):
        R = 0; move = None
        if n == 1:
            if param['TopFRr'][0] == 'R':
                R = param['TopFRr'][1] + Radd; move = 'G3'
        elif n == 3:
            if param['BotFRr'][0] == 'R':
                R = param['BotFRr'][1] - Radd; move = 'G2'
        r_[n] = [r_[n][0]/2, 0, r_[n][1], R, move]
    r_track = Tragectory_3D_one_direction(r_, plane='G18')
    if Z_L is None:
        print('1]|[1  l_track = ', l_track)
        print('DCurr = ', DCurr)
        x1L, y1L, z1L, x2L, y2L, z2L = l_track.return_axes(x=DCurr, y=0, z=None, ax='x')
        Z_L = max_None(z1L, z2L) if x1L >= l_track[1][0] else min_None(z1L, z2L)
        print('Zl = ', Z_L)
        print("L: x = {}, y = {}, z = {},  x2 = {}, y2 = {}, z2 = {}".format(x1L, y1L, z1L, x2L, y2L, z2L))
    if Z_R is None:
        x1R, y1R, z1R, x2R, y2R, z2R = r_track.return_axes(x=DCurr, y=0, z=None, ax='x')
        Z_R = max_None(z1R, z2R) if x1R < r_track[1][0] else min_None(z1R, z2R)
    return Z_L, Z_R

def takeXl_from_groove1(ZL, l_1,  param, Radd):
    l_ = l_1.copy()
    for n in range(len(l_)):
        R = 0; move = None
        if n == 1:
            if param['TopFRl'][0] == 'R':
                R = param['TopFRl'][1] + Radd; move = 'G2'
        elif n == 3:
            if param['BotFRl'][0] == 'R':
                R = param['BotFRl'][1] + Radd; move = 'G3'
        l_[n] = [l_[n][0]/2, 0, l_[n][1], R, move]
    l_track = Tragectory_3D_one_direction(l_, plane='G18')
    x1L, y1L, z1L, x2L, y2L, z2L = l_track.return_axes(x=None, y=0, z=ZL, ax='z')
    X_L = max_None(x1L, x2L) if z1L < l_track[1][2] else min_None(x1L, x2L)
    X_L = X_L * 2
    return X_L



def takeXR_from_groove1(ZR, r_1,  param, Radd):
    r_ = r_1.copy()
    print('r_ = ', r_)
    for n in range(len(r_)):
        R = 0; move = None
        if n == 1:
            if param['TopFRr'][0] == 'R':
                print('verh R')
                R = param['TopFRr'][1] + Radd; move = 'G3'
        elif n == 3:
            if param['BotFRr'][0] == 'R':
                print('niz R')
                R = param['BotFRr'][1] - Radd; move = 'G2'
        r_[n] = [r_[n][0]/2, 0, r_[n][1], R, move]
    r_track = Tragectory_3D_one_direction(r_, plane='G18')
    x1R, y1R, z1R, x2R, y2R, z2R = r_track.return_axes(x=None, y=0, z=ZR, ax='z')
    print("X К: x = {}, y = {}, z = {},  x2 = {}, y2 = {}, z2 = {}".format(x1R, y1R, z1R, x2R, y2R, z2R))
    print("К_track[1][0] = ", r_track[1][0])
    print('z1R = {}, r_track[1][1] = {}'.format(z1R, r_track[1][2]))
    X_R = max_None(x1R, x2R) if z1R > r_track[1][2] else min_None(x1R, x2R)
    X_R = X_R * 2
    return X_R#, X_R

