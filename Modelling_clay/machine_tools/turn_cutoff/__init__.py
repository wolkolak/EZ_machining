from OpenGL.GL import *
from OpenGL.GLU import *
import math
from Modelling_clay.machine_tools.__init__ import add_COLLET, tool_rot_in_socket
import numpy as np
from mathematic.geometry import GetCirclesIntersect

def init__tool(self, pd):#CUTOFF
    yellow = [1, 1, 0.1]
    angl = math.radians(pd['insert_angle'])
    trigonometry_insert_L = math.cos(angl) * pd['insert_l'] + math.sin(angl) * (
                pd['insert_b'] - pd['insert_r']) - math.cos(angl) * pd['insert_r'] + pd['insert_r']
    insert_sm = pd['insert_l'] - pd['insert_r']
    # center_l = pd['insert_b'] - pd['insert_r'] - pd['insert_r']
    tool = glGenLists(1)
    glNewList(tool, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    glColor3f(0.6, 0.6, 0.6)
    glRotate(pd['fastener'], 0, 0, 1)
    glTranslatef(-pd['L'] / 2, -pd['S'] / 2, 0)

    glBegin(GL_QUADS)  # top
    glVertex3f(0, 0, 0.)
    glVertex3f(pd['L'], 0, 0.)
    glVertex3f(pd['L'], pd['S'], 0.)
    glVertex3f(0., pd['S'], 0.)
    glEnd()

    glBegin(GL_QUAD_STRIP)  # side1
    glVertex3f(0, 0, 0.)
    glVertex3f(0, 0, pd['H'])
    glVertex3f(pd['l'], 0, 0.)
    glVertex3f(pd['l'], 0, pd['H'])
    glVertex3f(pd['L'], 0, 0.)
    glVertex3f(pd['L'], 0, pd['h'])
    glVertex3f(0, 0, 0.)
    glEnd()

    glBegin(GL_QUAD_STRIP)  # side2
    glVertex3f(0, pd['S'], 0.)
    glVertex3f(0, pd['S'], pd['H'])
    glVertex3f(pd['l'], pd['S'], 0.)
    glVertex3f(pd['l'], pd['S'], pd['H'])
    glVertex3f(pd['L'], pd['S'], 0.)
    glVertex3f(pd['L'], pd['S'], pd['h'])
    glVertex3f(0, pd['S'], 0.)
    glEnd()

    glColor3f(0.1, 0.6, 0.6)
    glBegin(GL_QUAD_STRIP)  # front
    glVertex3f(0, pd['S'], 0.)
    glVertex3f(0, pd['S'], pd['H'])

    glVertex3f(0, 0, 0.)
    glVertex3f(0, 0, pd['H'])
    glEnd()

    glBegin(GL_QUAD_STRIP)  # bot
    glVertex3f(0, 0, pd['H'])
    glVertex3f(0, pd['S'], pd['H'])
    glVertex3f(pd['l'], 0, pd['H'])
    glVertex3f(pd['l'], pd['S'], pd['H'])
    glEnd()

    glBegin(GL_QUAD_STRIP)  # back
    glVertex3f(pd['L'], 0, 0.)
    glVertex3f(pd['L'], pd['S'], 0.)
    glVertex3f(pd['L'], 0, pd['h'])
    glVertex3f(pd['L'], pd['S'], pd['h'])
    glVertex3f(pd['l'], 0, pd['H'])
    glVertex3f(pd['l'], pd['S'], pd['H'])
    glEnd()

    glTranslatef(0, pd['S'], pd['H'])
    glRotate(-pd['insert_angle'], 0, 1, 0)
    glBegin(GL_QUAD_STRIP)  # insert
    glColor3f(*yellow)
    glVertex3f(0, 0, -pd['insert_b'])
    glVertex3f(pd['insert_b'], 0, -pd['insert_b'])

    glVertex3f(0, 0, insert_sm)
    glVertex3f(pd['insert_b'], 0, insert_sm)

    glVertex3f(pd['insert_r'], 0, pd['insert_l'])
    glVertex3f(pd['insert_b'] - pd['insert_r'], 0, pd['insert_l'])
    # _______________________
    glVertex3f(pd['insert_r'], pd['insert_s'], pd['insert_l'])
    glVertex3f(pd['insert_b'] - pd['insert_r'], pd['insert_s'], pd['insert_l'])

    glVertex3f(0, pd['insert_s'], insert_sm)
    glVertex3f(pd['insert_b'], pd['insert_s'], insert_sm)

    glVertex3f(0, pd['insert_s'], -pd['insert_b'])
    glVertex3f(pd['insert_b'], pd['insert_s'], -pd['insert_b'])

    glVertex3f(0, 0, -pd['insert_b'])
    glVertex3f(pd['insert_b'], 0, -pd['insert_b'])
    glEnd()
    glColor3f(0.75, 0.75, 0.1)
    glBegin(GL_QUADS)
    glVertex3f(0, pd['insert_s'], -pd['insert_b'])
    glVertex3f(0, pd['insert_s'], insert_sm)
    glVertex3f(0, 0, insert_sm)
    glVertex3f(0, 0, -pd['insert_b'])

    glVertex3f(pd['insert_b'], pd['insert_s'], -pd['insert_b'])
    glVertex3f(pd['insert_b'], pd['insert_s'], insert_sm)
    glVertex3f(pd['insert_b'], 0, insert_sm)
    glVertex3f(pd['insert_b'], 0, -pd['insert_b'])

    glEnd()

    # R

    glRotate(90, 1, 0, 0)

    glTranslatef(pd['insert_r'], pd['insert_l'] - pd['insert_r'], 0)

    gluDisk(my_cylinder, 0., pd['insert_r'], self.collet['polygons_r'], 5)
    glTranslatef(0, 0, -pd['insert_s'])
    gluCylinder(my_cylinder, pd['insert_r'], pd['insert_r'], pd['insert_s'], 20, 10)
    gluDisk(my_cylinder, 0., pd['insert_r'], self.collet['polygons_r'], 5)

    glTranslatef(pd['insert_b'] - pd['insert_r'] - pd['insert_r'], 0, 0)
    gluCylinder(my_cylinder, pd['insert_r'], pd['insert_r'], pd['insert_s'], 20, 10)
    gluDisk(my_cylinder, 0., pd['insert_r'], self.collet['polygons_r'], 5)
    glTranslatef(0, 0, pd['insert_s'])
    gluDisk(my_cylinder, 0., pd['insert_r'], self.collet['polygons_r'], 5)

    glTranslatef(pd['insert_r'] - pd['insert_b'], pd['insert_r'] - pd['insert_l'], 0)
    glRotate(-90, 1, 0, 0)
    glRotate(pd['insert_angle'], 0, 1, 0)

    glTranslatef(pd['L'] / 2, -pd['S'] / 2, -pd['H'])
    glRotate(-pd['fastener'], 0, 0, 1)
    glEndList()
    self.my_tool = tool
    print('N END')

def tip_tool_way(self):
    x = 0; y = 0; z = 0

    angle_insert = - self.tool_dict['insert_angle']    #
    angle_insert = math.radians(angle_insert)
    B_rot_insert = np.array([
        [math.cos(angle_insert), 0, -math.sin(angle_insert), 0],
        [0, 1, 0, 0],
        [math.sin(angle_insert), 0, math.cos(angle_insert), 0],
        [0, 0, 0, 1]
    ])

    x = x + self.tool_dict['bind_left_h']
    z = z - self.tool_dict['bind_left_v']
    z = z + self.tool_dict['insert_l']
    y = y + self.tool_dict['insert_s']

#
    total = np.array([[x, y, z, 1]])
    total = total.dot(B_rot_insert)
    x, y, z = total[0][0], total[0][1], total[0][2]
    x = x - self.tool_dict['L'] / 2

    y = y + self.tool_dict['S'] / 2
    trigonometry_insert_L = math.cos(angle_insert) * self.tool_dict['insert_l'] + math.sin(angle_insert) * (
                self.tool_dict['insert_b'] - self.tool_dict['insert_r']) - math.cos(angle_insert) * self.tool_dict['insert_r'] + self.tool_dict['insert_r']
    #print('trigonometry_insert_L = ', trigonometry_insert_L)
    z = z + self.tool_dict['SORTIE'] - trigonometry_insert_L#self.tool_dict['H']
    x, y, z = tool_rot_in_socket(self, x, y, z)
    # COLLET
    x, y, z = add_COLLET(x, y, z, self)
    return x, y, z

def tool_check(dict):
    problem_keys = []
    angle_insert = math.radians(dict['insert_angle'])
    trigonometry_insert_L = math.cos(angle_insert) * dict['insert_l'] + math.sin(angle_insert) * (
            dict['insert_b'] - dict['insert_r']) - math.cos(angle_insert) * dict['insert_r'] + dict['insert_r']
    dict['OVERALL_L'] = (dict['H'] + trigonometry_insert_L).__round__(5)

    return dict, problem_keys