from OpenGL.GL import *
from OpenGL.GLU import *
import math
#import numpy as np
from Modelling_clay.machine_tools.__init__ import add_COLLET, tool_rot_in_socket


def init__tool(self, pd):#DRILL!
    """
    DRILL leg, cylinder1, cone2 through angle,'-_>'.
    """
    tool = glGenLists(1)
    glNewList(tool, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    glColor3f(0.6, 0.6, 0.6)
    #glRotate(pd['fastener'], 0, 0, 1)
    # TAIL
    if 'R tail' in pd and 'H tail' in pd:
        gluCylinder(my_cylinder, pd['R tail'], pd['R tail'], pd['H tail'], 10,
                    10)  # (object, baseR, topR, h, polygons_r, polygons_h)
        glTranslatef(0., 0., pd['H tail'])
        gluDisk(my_cylinder, 0., pd['R tail'], self.collet['polygons_r'], 5)
    # FIRST PART
    glColor3f(0.5, 0.5, 0.5)
    if 'Cylinder1 R1' in pd and 'Cylinder1 R2' in pd and 'H' in pd:
        print("it's working!")
        gluDisk(my_cylinder, 0., pd['Cylinder1 R1'], self.collet['polygons_r'],
                5)  # (object, R_in, R_out, polygons_r, polygons_h)
        gluCylinder(my_cylinder, pd['Cylinder1 R1'], pd['Cylinder1 R2'], pd['H'], 10, 10)
        glTranslatef(0., 0., pd['H'])
        gluDisk(my_cylinder, 0., pd['Cylinder1 R1'], self.collet['polygons_r'], 5)
    # SECOND PART
    if 'Cylinder2 R1' in pd and 'Cylinder2 ANGLE' in pd:
        gluDisk(my_cylinder, 0., pd['Cylinder2 R1'], self.collet['polygons_r'], 5)
        # print("math.tan(pd['CYLINDER2_ANGLE'] = ", math.tan(pd['CYLINDER2_ANGLE']))
        drill_angle = math.radians(pd['Cylinder2 ANGLE'])
        H_tip = (pd['Cylinder2 R1'] / 2) / math.tan(drill_angle / 2)
        gluCylinder(my_cylinder, pd['Cylinder2 R1'], 0., H_tip, 10, 10)
        glTranslatef(0., 0., H_tip)

    glTranslatef(0., 0., - pd['OVERALL_L'])
    #glRotate(-pd['fastener'], 0, 0, 1)
    glEndList()
    self.my_tool = tool


def tip_tool_way(self):
    x = 0; y = 0; z = 0
    z = z + self.tool_dict['SORTIE']
    #print("self.tool_dict['SORTIE'] = ", self.tool_dict['SORTIE'])
    x, y, z = tool_rot_in_socket(self, x, y, z)
    x, y, z = add_COLLET(x, y, z, self)
    return x, y, z

def tool_check(dict):
    problem_keys = []
    drill_angle = math.radians(dict['Cylinder2 ANGLE'])
    H_tip = (dict['Cylinder2 R1'] / 2) / math.tan(drill_angle / 2)
    dict['OVERALL_L'] = (dict['H'] + dict['H tail'] + H_tip).__round__(5)
    return dict, problem_keys
