from OpenGL.GL import *
from OpenGL.GLU import *
import math
#import numpy as np
from Modelling_clay.machine_tools.__init__ import add_COLLET, tool_rot_in_socket
from mathematic.geometry import GetCirclesIntersect

def init__tool(self, pd):#MILL1
    """
            MILL leg, main cone1, main cone2, tip sphere '-_>o'.
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
    if 'Cylinder1 R1' in pd and 'Cylinder1 R2' in pd and 'CYLINDER1_H' in pd:
        print("it's working!")
        gluDisk(my_cylinder, 0., pd['Cylinder1 R1'], self.collet['polygons_r'], 5)
        # (object, R_in, R_out, polygons_r, polygons_h)
        gluCylinder(my_cylinder, pd['Cylinder1 R1'], pd['Cylinder1 R2'], pd['H1'], 10, 10)
        glTranslatef(0., 0., pd['H1'])
        gluDisk(my_cylinder, 0., pd['Cylinder1 R1'], self.collet['polygons_r'], 5)
    # SECOND PART
    if 'Cylinder2 R1' in pd and 'Cylinder2 R2' in pd and 'H2' in pd:
        gluDisk(my_cylinder, 0., pd['Cylinder2 R1'], self.collet['polygons_r'], 5)
        gluCylinder(my_cylinder, pd['Cylinder2 R1'], pd['Cylinder2 R2'], pd['H2'], 10, 10)
        glTranslatef(0., 0., pd['H2'])
        gluDisk(my_cylinder, 0., pd['Cylinder2 R2'], self.collet['polygons_r'], 5)
    # SPHERE
    sphere_r = 0
    if pd['Sphere R'] != 0:
        gluSphere(my_cylinder, pd['Sphere R'], 32, 16)
        sphere_r = pd['Sphere R']
    glTranslatef(0., 0., sphere_r - pd['OVERALL_L'])
    #glRotate(-pd['fastener'], 0, 0, 1)
    glEndList()
    self.my_tool = tool

def tip_tool_way(self):
    x = 0; y = 0; z = 0
    z = z + self.tool_dict['SORTIE']

    x, y, z = tool_rot_in_socket(self, x, y, z)
    #COLLET
    x, y, z = add_COLLET(x, y, z, self)
    return x, y, z

def tool_check(dict):
    problem_keys = []
    dict['OVERALL_L'] = dict['H tail'] + dict['H1'] + dict['H2'] + dict['Sphere R']
    #if dict['Sphere R'] in dict:
    #    dict['OVERALL_L'] = dict['OVERALL_L'] + dict['Sphere R']
    return dict, problem_keys