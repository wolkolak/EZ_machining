from OpenGL.GL import *
from OpenGL.GLU import *





def create_cube_frame(gauge2):
    #glDisable(GL_LINE_SMOOTH)
    glLineWidth(2)
    glColor3f(0.5, 0.5, 0.5)
    glBegin(GL_LINES)  # XY
    glVertex3f(-gauge2, -gauge2, -gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)

    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)


    glEnd()



def createXbalk(x, zero, gauge, minus, how1, form_type='f+f'):
    #form_type='frame'  form_type='filled'  form_type='f+f'  form_type='nothing'
    gauge2 = gauge * 2
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    print(' how1 in x =', how1)
    if how1 != 'X' :
        glColor3f(0.3, 0.5, 0.75)
        print('how1 != X')
        if form_type == 'filled' or form_type == 'f+f':
            create_cube(gauge2)
        elif form_type == 'frame':
            create_cube_frame(gauge2)

    if form_type == 'filled' or form_type == 'f+f':
        glTranslatef(minus, 0, 0)
        glColor3f(0.75, 0.75, 0.75)

        glBegin(GL_QUADS)
        glVertex3f(0, -gauge, -gauge)
        glVertex3f(0, gauge, -gauge)
        glVertex3f(0, gauge, gauge)
        glVertex3f(0, -gauge, gauge)

        glVertex3f(x, -gauge, -gauge)
        glVertex3f(x, gauge, -gauge)
        glVertex3f(x, gauge, gauge)
        glVertex3f(x, -gauge, gauge)

        glVertex3f(x, -gauge, -gauge)
        glVertex3f(x, -gauge, gauge)
        glVertex3f(0, -gauge, gauge)
        glVertex3f(0, -gauge, -gauge)
        #
        glVertex3f(x, gauge, gauge)
        glVertex3f(x, gauge, -gauge)
        glVertex3f(0, gauge, -gauge)
        glVertex3f(0, gauge, gauge)

        #
        glVertex3f(x, -gauge, -gauge)
        glVertex3f(x, gauge, -gauge)
        glVertex3f(0, gauge, -gauge)
        glVertex3f(0, -gauge, -gauge)
        #
        glVertex3f(x, -gauge, gauge)
        glVertex3f(x, gauge, gauge)
        glVertex3f(0, gauge, gauge)
        glVertex3f(0, -gauge, gauge)
        glEnd()
        glTranslatef(-minus, 0, 0)

    if form_type == 'f+f' or form_type == 'frame':

        glTranslatef(minus, 0, 0)
        glColor3f(0.5, 0.5, 0.5)

        # glEnable(GL_LINE_SMOOTH)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        zero -= 0.1
        gauge += 0.1
        glVertex3f(x, -gauge, -gauge)
        glVertex3f(x, -gauge, gauge)
        glVertex3f(x, gauge, gauge)
        glVertex3f(x, gauge, -gauge)
        glVertex3f(x, -gauge, -gauge)
        glVertex3f(zero, -gauge, -gauge)
        glVertex3f(zero, -gauge, gauge)
        glVertex3f(zero, gauge, gauge)
        glVertex3f(zero, gauge, -gauge)
        glVertex3f(zero, -gauge, -gauge)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(zero, gauge, -gauge)
        glVertex3f(x, gauge, -gauge)
        glVertex3f(zero, gauge, gauge)
        glVertex3f(x, gauge, gauge)
        glVertex3f(zero, -gauge, gauge)
        glVertex3f(x, -gauge, gauge)
        glEnd()
        # glDisable(GL_LINE_SMOOTH)
        glTranslatef(-minus, 0, 0)
    glEndList()
    return CONNECTION

def createYbalk(x, zero, gauge, minus, how1, form_type='f+f'):
    print('form_type= y = ', form_type)
    gauge2 = gauge * 2  # +1
    #glDisable(GL_LINE_SMOOTH)
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)

    if how1 != 'Y' and (form_type == 'filled' or form_type == 'f+f'):
        glColor3f(0.3, 0.5, 0.75)
        if form_type == 'filled' or form_type == 'f+f':
            create_cube(gauge2)
        elif form_type == 'frame':
            create_cube_frame(gauge2)

    if form_type == 'filled' or form_type == 'f+f':
        glColor3f(0.75, 0.75, 0.75)
        glTranslatef(0, minus, 0)
        glBegin(GL_QUADS)
        glVertex3f(-gauge, 0, -gauge)
        glVertex3f(gauge, 0, -gauge)
        glVertex3f(gauge, 0, gauge)
        glVertex3f(-gauge, 0, gauge)

        glVertex3f(-gauge, x, -gauge)
        glVertex3f(gauge, x, -gauge)
        glVertex3f(gauge, x, gauge)
        glVertex3f(-gauge, x, gauge)

        glVertex3f(-gauge, x, -gauge)
        glVertex3f(-gauge, x, gauge)
        glVertex3f(-gauge, 0, gauge)
        glVertex3f(-gauge, 0, -gauge)
        #
        glVertex3f(gauge, x, gauge)
        glVertex3f(gauge, x, -gauge)
        glVertex3f(gauge, 0, -gauge)
        glVertex3f(gauge, 0, gauge)

        #
        glVertex3f(-gauge, x, -gauge)
        glVertex3f(gauge, x, -gauge)
        glVertex3f(gauge, 0, -gauge)
        glVertex3f(-gauge, 0, -gauge)
        #
        glVertex3f(-gauge, x, gauge)
        glVertex3f(gauge, x, gauge)
        glVertex3f(gauge, 0, gauge)
        glVertex3f(-gauge, 0, gauge)
        glEnd()
        glTranslatef(0, -minus, 0)

    if form_type == 'f+f' or form_type == 'frame':
        glTranslatef(0, minus, 0)

        glColor3f(0.5, 0.5, 0.5)
        glLineWidth(2)

        glBegin(GL_LINE_STRIP)
        zero -= 0.1
        gauge += 0.1
        glVertex3f(-gauge, x, -gauge)
        glVertex3f(-gauge, x, gauge)
        glVertex3f(gauge, x, gauge)
        glVertex3f(gauge, x, -gauge)
        glVertex3f(-gauge, x, -gauge)
        glVertex3f(-gauge, zero, -gauge)
        glVertex3f(-gauge, zero, gauge)
        glVertex3f(gauge, zero, gauge)
        glVertex3f(gauge, zero, -gauge)
        glVertex3f(-gauge, zero, -gauge)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(gauge, zero, -gauge)
        glVertex3f(gauge, x, -gauge)
        glVertex3f(gauge, zero, gauge)
        glVertex3f(gauge, x, gauge)
        glVertex3f(-gauge, zero, gauge)
        glVertex3f(-gauge, x, gauge)
        glEnd()

    glTranslatef(0, -minus, 0)
    glEndList()
    return CONNECTION

def createZbalk(x, zero, gauge, minus, how1, form_type='f+f'):#, addition
    print('form_type= z = ', form_type)
    CONNECTION = glGenLists(1)
    gauge2 = gauge * 2
    #gauge3 = gauge * 1.5
    glNewList(CONNECTION, GL_COMPILE)

    if how1 != 'Z' and (form_type == 'filled' or form_type == 'f+f'):
        glColor3f(0.3, 0.5, 0.75)
        if form_type == 'filled' or form_type == 'f+f':
            create_cube(gauge2)
        elif form_type == 'frame':
            create_cube_frame(gauge2)

    if form_type == 'filled' or form_type == 'f+f':
        glTranslatef(0, 0, minus)
        glColor3f(0.75, 0.75, 0.75)
        glBegin(GL_QUADS)
        glVertex3f(-gauge, -gauge, 0)
        glVertex3f(gauge, -gauge, 0)
        glVertex3f(gauge, gauge, 0)
        glVertex3f(-gauge, gauge, 0)

        glVertex3f(-gauge, -gauge, x)
        glVertex3f(gauge, -gauge, x)
        glVertex3f(gauge, gauge, x)
        glVertex3f(-gauge, gauge, x)

        glVertex3f(-gauge, -gauge, x)
        glVertex3f(-gauge, gauge, x)
        glVertex3f(-gauge, gauge, 0)
        glVertex3f(-gauge, -gauge, 0)
        #
        glVertex3f(gauge, gauge, x)
        glVertex3f(gauge, -gauge, x)
        glVertex3f(gauge, -gauge, 0)
        glVertex3f(gauge, gauge, 0)

        #
        glVertex3f(-gauge, -gauge, x)
        glVertex3f(gauge, -gauge, x)
        glVertex3f(gauge, -gauge, 0)
        glVertex3f(-gauge, -gauge, 0)
        #
        glVertex3f(-gauge, gauge, x)
        glVertex3f(gauge, gauge, x)
        glVertex3f(gauge, gauge, 0)
        glVertex3f(-gauge, gauge, 0)
        glEnd()

        glTranslatef(0, 0, -minus)

    if form_type == 'f+f' or form_type == 'frame':
        create_cube_frame(gauge2)

        glTranslatef(0, 0, minus)

        glColor3f(0.5, 0.5, 0.5)

        # glEnable(GL_LINE_SMOOTH)
        glLineWidth(2)
        glBegin(GL_LINE_STRIP)
        zero -= 0.1
        gauge += 0.1
        glVertex3f(-gauge, -gauge, x)
        glVertex3f(-gauge, gauge, x)
        glVertex3f(gauge, gauge, x)
        glVertex3f(gauge, -gauge, x)
        glVertex3f(-gauge, -gauge, x)
        glVertex3f(-gauge, -gauge, zero)
        glVertex3f(-gauge, gauge, zero)
        glVertex3f(gauge, gauge, zero)
        glVertex3f(gauge, -gauge, zero)
        glVertex3f(-gauge, -gauge, zero)
        glEnd()
        glBegin(GL_LINES)
        glVertex3f(gauge, -gauge, zero)
        glVertex3f(gauge, -gauge, x)
        glVertex3f(gauge, gauge, zero)
        glVertex3f(gauge, gauge, x)
        glVertex3f(-gauge, gauge, zero)
        glVertex3f(-gauge, gauge, x)
        glEnd()
        # glTranslatef(-addition, 0, 0)
        # glDisable(GL_LINE_SMOOTH)
        glTranslatef(0, 0, -minus)
        glEndList()

    return CONNECTION

def create_cube(gauge2):
    #glDisable(GL_LINE_SMOOTH)
    glLineWidth(2)
    glBegin(GL_QUADS)  # XY
    glVertex3f(-gauge2, -gauge2, -gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)

    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)

    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)

    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)
    glEnd()

    glColor3f(0.6, 0.6, 0.6)
    glBegin(GL_LINE_STRIP)
    glVertex3f(-gauge2, -gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, -gauge2, -gauge2)

    glVertex3f(gauge2, -gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(gauge2, -gauge2, -gauge2)
    glEnd()

    glBegin(GL_LINES)
    glVertex3f(gauge2, -gauge2, gauge2)
    glVertex3f(-gauge2, -gauge2, gauge2)
    glVertex3f(gauge2, gauge2, gauge2)
    glVertex3f(-gauge2, gauge2, gauge2)
    glVertex3f(gauge2, gauge2, -gauge2)
    glVertex3f(-gauge2, gauge2, -gauge2)
    glEnd()


def createJaw(D, a, b, c, gauge, form_type='f+f'):#, letterN=4)
    D = D * 0.9
    main_color = [1, 1, 1]
    ornament_color = [0.3, 0.3, 0.3]
    segments = 12
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    #if letterN != 4:
    print('letterN != 4')
    glRotate(a, 1, 0, 0)
    glRotate(b, 0, 1, 0)
    glRotate(c, 0, 0, 1)

    #glTranslatef(0, 0, -gauge*0.5)

    glTranslatef(0, 0, -gauge)
    make_ornament(ornament_color, my_cylinder, D, 1, main_color, segments, direction=-1)
    glColor3f(*main_color)
    gluCylinder(my_cylinder, D, D, gauge, segments, 10)
    glTranslatef(0, 0, gauge)
    make_ornament(ornament_color, my_cylinder, D, 1, main_color, segments, direction=1)
    #glTranslatef(0, 0, gauge * 0.5)
    #if letterN != 4:
    glRotate(-c, 0, 0, 1)
    glRotate(-b, 0, 1, 0)
    glRotate(-a, 1, 0, 0)



    glEndList()
    return CONNECTION


def make_ornament(ornament_color, my_cylinder, R, gauge, main_color, segments, direction, form_type='f+f'):
    glColor3f(*main_color)
    gluDisk(my_cylinder, 0., R, segments, 5)
    glColor3f(*ornament_color)
    gluDisk(my_cylinder, R, R+gauge, segments, 2)
    gluCylinder(my_cylinder, R+gauge, R+gauge, gauge, segments, 10)
    #glColor3f(0.8, 0.1, 0.1)
    glColor3f(*ornament_color)
    glBegin(GL_QUADS)
    glVertex3f(R, 0, direction)
    glVertex3f(-0.5 * R,  0.43301 * 2*R, direction)
    glVertex3f(-0.5 * R, -0.43301 * 2*R, direction)
    glVertex3f(R, 0, direction)
    glEnd()
    glTranslatef(0, 0, direction*2)
    glColor3f(*main_color)
    gluDisk(my_cylinder, 0., R/20, segments, 5)
    glTranslatef(0, 0, -direction * 2)






def create_gag(D=0, a=0, b=0, c=0, gauge=0, form_type='f+f'):
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    glBegin(GL_POINTS)
    glVertex3f(0, 0, 0)
    glEnd()
    glEndList()
    return CONNECTION


def create_cylinder_on_table_head_end(R=30, L=50, how_to_rotate=None, form_type='f+f'):
    print('how_to_rotate = ', how_to_rotate)
    if how_to_rotate is None:
        how_to_rotate_angle = [90, 1, 0, 0]
    else:
        if how_to_rotate[2] == 0:
            how_to_rotate_angle = [90, 0, 1, 0]#верно
        elif how_to_rotate[2] == 1:
            how_to_rotate_angle = [90, 1, 0, 0]#верно
        elif how_to_rotate[2] == 2:
            how_to_rotate_angle = [90, 0, 0, 1]#не факт
    print('how_to_rotate_angle = ', how_to_rotate_angle)
    #how_to_rotate_angle = [90, 1, 0, 0]
    segments = 15
    ornament_color = [0.3, 0.3, 0.3]
    main_color = [1, 1, 1]
    CONNECTION = glGenLists(1)
    glNewList(CONNECTION, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    glRotate(*how_to_rotate_angle)
    glColor3f(0.5, 0.5, 0.5)
    gluCylinder(my_cylinder, R, R, L, segments, 10)
    make_ornament(ornament_color, my_cylinder, R, 1, main_color, segments, direction=-1)
    glTranslatef(0, 0, L)
    make_ornament(ornament_color, my_cylinder, R, 1, main_color, segments, direction=1)
    glTranslatef(0, 0, -L)
    glRotate(-how_to_rotate_angle [0], how_to_rotate_angle [1], how_to_rotate_angle [2], how_to_rotate_angle[3])
    glEndList()
    return CONNECTION


def make_romb(self, h, w, s, image_array, ix, iy, form_type='f+f'): # h - length, w - width, s - another
       #вдоль какой линии?
       h = h - s#/2
       self.bind_Texture(image_array, ix, iy)
       nn = glGenLists(1)#GLuint glGenLists(	GLsizei range);
       glNewList(nn, GL_COMPILE)
       sphere = gluNewQuadric()
       gluSphere(sphere, 5.0, 32, 16)  # quad radius slices stacks
       glTranslatef(0, s/2, -s/2)

       glLineWidth(1)
       l = 0.1

       glColor3f(0.9, 0.9, 0.9)
       glBegin(GL_LINE_STRIP)
       glVertex3f(0, 0, 0-l)
       glVertex3f(w / 2, h / 4, 0-l)
       glVertex3f(w/2, 3*h/4, 0-l)
       glVertex3f(0, h, 0-l)
       glVertex3f(-w/2, 3*h/4, 0-l)
       glVertex3f(-w/2, h/4, 0-l)

       glVertex3f(0, 0, 0 - l)

       glVertex3f(0, 0, s+l)
       glVertex3f(w/2, h/4, s+l)
       glVertex3f(w / 2, 3 * h / 4, s+l)
       glVertex3f(0, h, s+l)
       glVertex3f(-w / 2, 3 * h / 4, s+l)
       glVertex3f(-w / 2, h / 4, s+l)
       glVertex3f(0, 0, s + l)



       glEnd()

       glColor3f(1, 1, 1)

       glBindTexture(GL_TEXTURE_2D, self.machine_tex_green)  # this is the texture we will manipulate
       glEnable(GL_BLEND)
       glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
       glEnable(GL_TEXTURE_2D)

       glBegin(GL_QUAD_STRIP)
       glVertex3f(0, 0, s)
       glVertex3f(0, 0, 0)
       glVertex3f(w/2, h/4, s)
       glVertex3f(w / 2, h / 4, 0)
       glVertex3f(w / 2, 3 * h / 4, s)
       glVertex3f(w/2, 3*h/4, 0)
       glVertex3f(0, h, s)
       glVertex3f(0, h, 0)
       glVertex3f(-w / 2, 3 * h / 4, s)
       glVertex3f(-w/2, 3*h/4, 0)
       glVertex3f(-w / 2, h / 4, s)
       glVertex3f(-w/2, h/4, 0)
       glVertex3f(0, 0, s)
       glVertex3f(0, 0, 0)
       glEnd()





       glBegin(GL_TRIANGLE_FAN)
       glTexCoord2f(0.0, 0.0); glVertex3f(0, 0, 0)
       glTexCoord2f(1.0, 0.0); glVertex3f(w / 2, h / 4, 0)
       glTexCoord2f(0.0, 0.0); glVertex3f(w / 2, 3 * h / 4, 0)
       glTexCoord2f(1.0, 0.0); glVertex3f(0, h, 0)
       glTexCoord2f(0.0, 0.0); glVertex3f(-w / 2, 3 * h / 4, 0)
       glTexCoord2f(1.0, 0.0); glVertex3f(-w / 2, h / 4, 0)
       glEnd()

       glBegin(GL_TRIANGLE_FAN)
       glVertex3f(0, 0, s)
       glVertex3f(w / 2, h / 4, s)
       glVertex3f(w / 2, 3 * h / 4, s)
       glVertex3f(0, h, s)
       glVertex3f(-w / 2, 3 * h / 4, s)
       glVertex3f(-w / 2, h / 4, s)
       glEnd()

       glDisable(GL_TEXTURE_2D)
       glDisable(GL_BLEND)
       glTranslatef(0, -s / 2, s / 2)
       glEndList()
       #gluDeleteQuadric(circle)
       return nn


