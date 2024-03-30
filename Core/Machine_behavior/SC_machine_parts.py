from OpenGL.GL import *
from OpenGL.GLU import *




#def return_transfer(self, dx=0., dy=0., dz=0., da=0., db=0., dc=0.):
#    glRotate(dc, 0, 0, 1)
#    glRotate(db, 0, 1, 0)
#    glRotate(da, 1, 0, 0)
#
#    glTranslatef(dx, dy, dz)





def create_pyramid(length):
    glRotate(-90, 0, 1, 0)
    glTranslatef(0, 0, -50)
    glBegin(GL_QUADS)
    glVertex3f(length, length, 0)
    glVertex3f(length, -length, 0)
    glVertex3f(-length, -length, 0)
    glVertex3f(-length, length, 0)
    glVertex3f(length, length, 0)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex3f(length, length, 0)
    glVertex3f(0, 0, length)
    glVertex3f(length, -length, 0)

    glVertex3f(length, -length, 0)
    glVertex3f(0, 0, length)
    glVertex3f(-length, -length, 0)

    glVertex3f(-length, -length, 0)
    glVertex3f(0, 0, length)
    glVertex3f(-length, length, 0)
    glVertex3f(-length, length, 0)
    glVertex3f(0, 0, length)
    glVertex3f(length, length, 0)
    glEnd()
    new1 = gluNewQuadric()
    gluCylinder(new1, 1, 1, 50, 5, 10)

    glTranslatef(0, 0, 50)
    glRotate(90, 0, 1, 0)

def create_M0_CONST(self):
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    length = 10
    glColor3f(0., 0., 0.)
    create_pyramid(length)

    glEndList()
    return CONNECTION


def create_M0_VARIANT(self):
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    length = 10
    glColor3f(0.5, 0.5, 0.5)

    glTranslatef(self.offset_pointXYZ[0], self.offset_pointXYZ[1], self.offset_pointXYZ[2])

    create_pyramid(length)
    glTranslatef(-self.offset_pointXYZ[0], -self.offset_pointXYZ[1], -self.offset_pointXYZ[2])
    #glTranslatef(-self.machine_zero_variant[0], -self.machine_zero_variant[1], -self.machine_zero_variant[2])
    glEndList()
    return CONNECTION



def create_TOOL_change_point1(self):
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)

    length = 10

    glColor3f(0.2, 0.6, 0.2)
    glTranslatef(self.change_TOOL_point1[0], self.change_TOOL_point1[1], self.change_TOOL_point1[2])

    create_pyramid(length)

    glTranslatef(-self.change_TOOL_point1[0], -self.change_TOOL_point1[1], -self.change_TOOL_point1[2])
    glEndList()
    return CONNECTION


def create_TOOL_change_point2(self):
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    length = 10
    glColor3f(0.3, 0.8, 0.3)

    glTranslatef(self.change_TOOL_point2[0], self.change_TOOL_point2[1], self.change_TOOL_point2[2])
    create_pyramid(length)
    glTranslatef(-self.change_TOOL_point2[0], -self.change_TOOL_point2[1], -self.change_TOOL_point2[2])
    glEndList()
    return CONNECTION


def create_PART_draw_SC(self):
    L = 2

    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)

    glLineWidth(2)
    glColor3f(1.5, 1.5, 0.5)
    glBegin(GL_LINES)#X
    glVertex3f(0., 0., 0.)
    glVertex3f(L, 0., 0.)

    glVertex3f(0., L/2, 0.)
    glVertex3f(L, L/2, 0.)
    glVertex3f(0., L, 0.)
    glVertex3f(L/2, L, 0.)

    glVertex3f(0.,  0., L/2)
    glVertex3f(L, 0.,  L/2)
    glVertex3f(0.,  0., L)
    glVertex3f(L/2, 0.,  L)

    glEnd()

    #glColor3f(0.5, 0.5, 1.5)

    glBegin(GL_LINES)#Y
    glVertex3f(0., 0., 0.)
    glVertex3f(0., L, 0.)

    glVertex3f(L/2, 0., 0.)
    glVertex3f(L/2, L, 0.)
    glVertex3f(L, 0., 0.)
    glVertex3f(L, L/2, 0.)


    glVertex3f(0., 0.,  L/2)
    glVertex3f(0., L, L/2)
    glVertex3f(0., 0.,  L)
    glVertex3f(0., L/2, L)
    glEnd()


    #glColor3f(0.5, 1.5, 0.5)
    glBegin(GL_LINES)#Z
    glVertex3f(0., 0., 0.)
    glVertex3f(0., 0., L)

    glVertex3f(L, 0., 0.)
    glVertex3f(L, 0., L/2)

    glVertex3f(L/2, 0., 0.)
    glVertex3f(L/2, 0., L)


    glVertex3f(0., L, 0.)
    glVertex3f(0., L, L/2)
    glVertex3f(0., L/2, 0.)
    glVertex3f(0., L/2, L)

    glEnd()

    glEndList()
    return CONNECTION


def create_MACHINING_SC(self):
    #L = 2

    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    glLineWidth(5)
    glPointSize(2)
    glColor3f(1.5, 0.5, 0.5)

    glBegin(GL_POINTS)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    glColor3f(1.5, 0.5, 0.5)
    glBegin(GL_LINES)  # X
    glVertex3f(0., 0., 0.)
    glVertex3f(0.6, 0., 0.)
    glEnd()

    glColor3f(0.5, 0.5, 1.5)
    glBegin(GL_LINES)  # Y
    glVertex3f(0., 0., 0.)
    glVertex3f(0., 0.6, 0.)
    glEnd()

    glColor3f(0.5, 1.5, 0.5)
    glBegin(GL_LINES)  # Z
    glVertex3f(0., 0., 0.)
    glVertex3f(0., 0., 0.6)
    glEnd()

    glEndList()
    return CONNECTION


def create_SMALL_SC(self):
    L = 20
    #TODO может быть развернута как угодно
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    glLineWidth(3)
    glPointSize(2)
    glColor3f(1.5, 0.5, 0.5)

    glBegin(GL_POINTS)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()

    glColor3f(1.5, 0.5, 0.5)
    glBegin(GL_LINES)  # X
    glVertex3f(0., 0., 0.)
    glVertex3f(0.6*L, 0., 0.)
    glEnd()

    glColor3f(0.5, 0.5, 1.5)
    glBegin(GL_LINES)  # Y
    glVertex3f(0., 0., 0.)
    glVertex3f(0., 0.6*L, 0.)
    glEnd()

    glColor3f(0.5, 1.5, 0.5)
    glBegin(GL_LINES)  # Z
    glVertex3f(0., 0., 0.)
    glVertex3f(0., 0., 0.6*L)
    glEnd()

    glEndList()
    return CONNECTION


def create_POLAR_SC(self):
    #L = 2
    print('create_POLAR_SC')
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    glLineWidth(3)
    glPointSize(5)
    glColor3f(0.5, 0.5, 0.5)

    glBegin(GL_POINTS)
    glVertex3f(0.0, 0.0, 0.0)
    glEnd()
    max6=5.
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINE_STRIP)  # X
    glVertex3f(max6, max6/2, 0.)#1
    glVertex3f(max6 / 2, max6, 0.)
    glVertex3f(max6, 0., 0.)#2
    glVertex3f(max6/2, -max6, 0.)#3
    glVertex3f(-max6/2, -max6, 0.)#4
    glVertex3f(-max6, 0., 0.)#5
    glVertex3f(-max6/2, max6, 0.)
    glVertex3f(max6/2, max6, 0.)
    #glVertex3f(max6, 0., 0.)
    glVertex3f(max6/2, max6/2.5, 0.)
    glEnd()

    #glColor3f(0.5, 0.5, 1.5)
    #glBegin(GL_LINES)  # Y
    #glVertex3f(0., 0., 0.)
    #glVertex3f(0., 0.6, 0.)
    #glEnd()
#
    #glColor3f(0.5, 1.5, 0.5)
    #glBegin(GL_LINES)  # Z
    #glVertex3f(0., 0., 0.)
    #glVertex3f(0., 0., 0.6)
    #glEnd()

    glEndList()
    return CONNECTION