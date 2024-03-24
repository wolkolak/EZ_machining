from OpenGL.GL import *
from OpenGL.GLU import *
import math
import numpy as np
from mathematic.geometry import GetCirclesIntersect
from Modelling_clay.machine_tools.__init__ import add_COLLET, tool_rot_in_socket

def init__tool(self, pd):#CUT
    alpha = math.radians(pd['insert_angle'])
    l_big = 2 * (pd['L'] / 2 + pd['r'] / math.sin(alpha / 2) - pd['r'])
    h = math.tan(alpha / 2) * l_big
    dot_1 = [0., h / 2]
    r_c2 = [pd['L'] / 2 - pd['r'], 0]
    R = math.sqrt((dot_1[0] - r_c2[0]) ** 2 + (dot_1[1] - r_c2[1]) ** 2)
    P1 = GetCirclesIntersect(dot_1, R, r_c2, pd['r'])
    tool = glGenLists(1)
    glNewList(tool, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    glColor3f(0.6, 0.6, 0.6)
    glRotate(pd['fastener'], 0, 0, 1)
    glTranslatef(-pd['p1']/2, -pd['p2']/2, 0)

    if 'p1' in pd and 'p2' in pd and 'p3' in pd:
        glBegin(GL_QUADS)   # top
        glVertex3f(0, 0, 0.)
        glVertex3f(pd['p1'], 0, 0.)
        glVertex3f(pd['p1'], pd['p2'], 0.)
        glVertex3f(0., pd['p2'], 0.)
        glEnd()
        glBegin(GL_QUADS)   # side1
        glVertex3f(0, 0, 0.)
        glVertex3f(pd['p1'], 0, 0.)
        glVertex3f(pd['p1'], 0, pd['p3'])
        glVertex3f(0, 0, pd['p3'])
        glEnd()
        glBegin(GL_QUADS)   # side2
        glVertex3f(0, pd['p2'], 0.)
        glVertex3f(pd['p1'], pd['p2'], 0.)
        glVertex3f(pd['p1'], pd['p2'], pd['p3'])
        glVertex3f(0, pd['p2'], pd['p3'])
        glEnd()
        glColor3f(0., 0., 0.6)
        glBegin(GL_QUADS)   # side3
        glVertex3f(pd['p1'], 0, 0.)
        glVertex3f(pd['p1'], pd['p2'], 0.)
        glVertex3f(pd['p1'], pd['p2'], pd['p3'])
        glVertex3f(pd['p1'], 0, pd['p3'])
        glEnd()
        glBegin(GL_QUADS)   # side4
        glVertex3f(0, 0, 0.)
        glVertex3f(0, pd['p2'], 0.)
        glVertex3f(0, pd['p2'], pd['p3'])
        glVertex3f(0, 0, pd['p3'])
        glEnd()
    if 'p1' in pd and 'p2' in pd and 'p3' in pd and 'q1' in pd and 'q2' in pd and 'q3' in pd and 'q4' in pd and 'q5' in pd:
        glBegin(GL_QUADS)   # above bottom
        glVertex3f(pd['p1'], pd['p2'], pd['p3'])
        glVertex3f(pd['p1'], 0, pd['p3'])
        glVertex3f(pd['q4'], 0, pd['p3'])
        glVertex3f(pd['q4'], pd['p2'], pd['p3'])
        glEnd()
        glBegin(GL_QUADS)   # front
        glVertex3f(pd['q4'], 0, pd['p3'])
        glVertex3f(pd['q4'], pd['p2'], pd['p3'])
        glVertex3f(pd['q4'], pd['p2'], pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'], 0, pd['p3'] + pd['q3'])
        glEnd()
        glBegin(GL_QUADS)   # bot
        glVertex3f(pd['q4'], pd['p2'], pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'], 0, pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'] - pd['q1'], 0, pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'] - pd['q1'], pd['p2'], pd['p3'] + pd['q3'])
        glEnd()
        glBegin(GL_QUADS)  # back
        glVertex3f(pd['q4'] - pd['q1'], 0, pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'] - pd['q1'], pd['p2'], pd['p3'] + pd['q3'])
        glVertex3f(0, pd['p2'], pd['p3'])
        glVertex3f(0, 0, pd['p3'])
        glEnd()
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_QUADS)
        glVertex3f(0, 0, pd['p3'])
        glVertex3f(pd['q4'], 0, pd['p3'])
        glVertex3f(pd['q4'], 0, pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'] - pd['q1'], 0, pd['p3'] + pd['q3'])
        glEnd()
        glBegin(GL_QUADS)
        glVertex3f(0, pd['q2'], pd['p3'])
        glVertex3f(pd['q4'], pd['q2'], pd['p3'])
        glVertex3f(pd['q4'], pd['q2'], pd['p3'] + pd['q3'])
        glVertex3f(pd['q4'] - pd['q1'], pd['q2'], pd['p3'] + pd['q3'])
        glEnd()
    transfer_vector = [pd['q4']-pd['from_tip_h'], 0., pd['q3']+pd['p3']-pd['from_tip_v']]#from_tip_h
    ret_transfer_vector = [-1 * a for a in transfer_vector]
    glTranslatef(*transfer_vector)
    angle = pd['insert_angle']/2 + pd['rot_angle']
    glRotate(-angle, 0, 1, 0.)
    create_CUT_insert(self, pd, P1, h, my_cylinder)
    glRotate(angle, 0, 1., 0.)
    glTranslatef(*ret_transfer_vector)
    glColor3f(1., 1., 0.)
    glTranslatef(pd['p1'] / 2, pd['p2'] / 2, 0)
    glRotate(-pd['fastener'], 0, 0, 1)
    glEndList()
    self.my_tool = tool
    print('N END')


def create_CUT_insert(self, insert_parts, P1, h, my_cylinder):  # from centre
    step = insert_parts['L'] / 2 - insert_parts['r']
    glLineWidth(0.5)
    yellow = [1, 1, 0.1]
    black = [0., 0., 0.]

    for half in range(2):
        glColor3f(*yellow)
        glBegin(GL_QUADS)  # side1
        glVertex3f(0, 0, h / 2)
        glVertex3f(P1[0], 0, P1[1])
        glVertex3f(P1[0], 0, -P1[1])
        glVertex3f(0, 0, -h / 2)
        glEnd()

        glBegin(GL_QUADS)  # side2
        glVertex3f(0, -insert_parts['s'], h / 2)
        glVertex3f(P1[0], -insert_parts['s'], P1[1])
        glVertex3f(P1[0], -insert_parts['s'], -P1[1])
        glVertex3f(0, -insert_parts['s'], -h / 2)
        glEnd()

        glBegin(GL_QUADS)  # top
        glVertex3f(0, 0, h / 2)
        glVertex3f(0, -insert_parts['s'], h / 2)
        glVertex3f(P1[0], -insert_parts['s'], P1[1])
        glVertex3f(P1[0], 0, P1[1])
        glEnd()

        glBegin(GL_QUADS)  # bot
        glVertex3f(0, 0, -h / 2)
        glVertex3f(0, -insert_parts['s'], -h / 2)
        glVertex3f(P1[0], -insert_parts['s'], -P1[1])
        glVertex3f(P1[0], 0, -P1[1])
        glEnd()

        glColor3f(*black)  # outline lines
        glBegin(GL_LINES)
        glVertex3f(0, 0, h / 2)
        glVertex3f(P1[0], 0, P1[1])

        glVertex3f(P1[0], 0, -P1[1])
        glVertex3f(0, 0, -h / 2)

        glVertex3f(0, -insert_parts['s'], h / 2)
        glVertex3f(P1[0], -insert_parts['s'], P1[1])

        glVertex3f(P1[0], -insert_parts['s'], -P1[1])
        glVertex3f(0, -insert_parts['s'], -h / 2)

        glVertex3f(P1[0], 0, P1[1])
        glVertex3f(P1[0], -insert_parts['s'], P1[1])

        glVertex3f(P1[0], 0, -P1[1])
        glVertex3f(P1[0], -insert_parts['s'], -P1[1])

        glEnd()

        glColor3f(*yellow)
        glRotate(90, 1., 0., 0.)
        glTranslatef(step, 0., 0.)

        gluCylinder(my_cylinder, insert_parts['r'], insert_parts['r'], insert_parts['s'], 10, 10)

        gluDisk(my_cylinder, 0., insert_parts['r'] - 0.03, self.collet['polygons_r'], 5)  # inner disk
        glColor3f(*black)
        gluDisk(my_cylinder, insert_parts['r'] - 0.03, insert_parts['r'], self.collet['polygons_r'], 5)  # outer line

        glTranslatef(0, 0, insert_parts['s'])
        glColor3f(*yellow)
        gluDisk(my_cylinder, 0., insert_parts['r'] - 0.03, self.collet['polygons_r'], 5)  # inner disk
        glColor3f(*black)
        gluDisk(my_cylinder, insert_parts['r'] - 0.03, insert_parts['r'], self.collet['polygons_r'], 5)  # outer line

        glTranslatef(-step, 0., -insert_parts['s'])

        glRotate(-90, 1., 0., 0.)

        glRotate(180, 0., 0., 1.)  # make another half
        glTranslatef(0, insert_parts['s'], 0.)

def tip_tool_way(self):
    x = 0.  # -170.
    y = 0.
    z = 0.  # 370.
    #print('here y1 = ', y)
    angle_insert = - (self.tool_dict['insert_angle'] / 2 + self.tool_dict['rot_angle'])  #
    angle_insert = math.radians(angle_insert)
    B_rot_insert = np.array([
        [math.cos(angle_insert), 0, -math.sin(angle_insert), 0],
        [0, 1, 0, 0],
        [math.sin(angle_insert), 0, math.cos(angle_insert), 0],
        [0, 0, 0, 1]
    ])

    #print('here y2 = ', y)

    r_c = self.tool_dict['L'] / 2 - self.tool_dict['r']
    x = x + r_c

    total = np.array([[x, y, z, 1]])
    total = total.dot(B_rot_insert)
    x, y, z = total[0][0], total[0][1], total[0][2]

    x = x + self.tool_dict['bind_h']
    z = z + self.tool_dict['bind_v']

    x_ = - self.tool_dict['from_tip_h']
    z_ = -self.tool_dict['from_tip_v']
    x = x + x_
    z = z + z_

    x_ = self.tool_dict['q4'] - self.tool_dict['p2'] / 2
    y_ = - self.tool_dict['q2'] / 2 - self.tool_dict['s']  # self.tool_dict['']
    #print('y_1 = ', y_)
    x = x + x_
    y = y + y_
    #print('y_2 = ', y_)
    trigonometry_insert_L = math.cos(angle_insert) * (self.tool_dict['L'] / 2) - math.cos(angle_insert) * self.tool_dict['r'] + self.tool_dict['r']
    z = z + self.tool_dict['SORTIE'] - trigonometry_insert_L
    #print('trigonometry_insert_L = ', trigonometry_insert_L)

    x, y, z = tool_rot_in_socket(self, x, y, z)
    #print('y_3 = ', y_)
    #COLLET
    x, y, z = add_COLLET(x, y, z, self)
    #print('y_3 = ', y_)
    return x, y, z

def tool_check(dict):
    problem_keys = []
    angle_insert = math.radians(dict['insert_angle']/2 + dict['rot_angle'])
    trigonometry_insert_L = math.cos(angle_insert) * (dict['L'] / 2) - math.cos(angle_insert) * dict['r'] + dict['r']
    dict['OVERALL_L'] = (dict['p3'] + dict['q3'] + trigonometry_insert_L).__round__(5)
    #problem_keys.append('OVERALL_L')
    #problem_keys.append('TYPE')
    return dict, problem_keys
