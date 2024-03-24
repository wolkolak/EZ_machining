import math
import numpy as np


def add_COLLET(x, y, z, self):
    angle = self.collet['angle']
    #Где то здесь
    angle = math.radians(angle)
    A_rot = np.array([
        [1, 0, 0, 0],
        [0, math.cos(angle), math.sin(angle), 0],
        [0, -math.sin(angle), math.cos(angle), 0],
        [0, 0, 0, 1]
    ])
    z = z + self.collet['h']
    #y = y - self.collet['L_from_segment_tip']
    total = np.array([[x, y, z, 1]])
    total = total.dot(A_rot)
    x, y, z = total[0][0], total[0][1], total[0][2]
    return x, y, z

def tool_rot_in_socket(self, x, y, z):
    #и здесь
    fastener = math.radians(self.tool_dict['fastener'])
    #fastener = math.radians(-45)
    C_rot = np.array([
        [math.cos(fastener), math.sin(fastener), 0, 0],
        [-math.sin(fastener), math.cos(fastener), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    total = np.array([[x, y, z, 1]])#todo problem
    total = total.dot(C_rot)
    x, y, z = total[0][0], total[0][1], total[0][2]
    return x, y, z

