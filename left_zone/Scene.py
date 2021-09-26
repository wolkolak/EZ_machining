from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PyQt5 import QtGui
from left_zone.D3_interface import d3_interface, change_draft, resize_texture, ChooseDistanceDialog
from PyQt5.QtGui import QResizeEvent
from Settings.settings import *
import numpy as np
from PIL import Image
from HLSyntax.PostProcessors_revers.Fanuc_NT import Fanuc_NT
import copy
from ctypes import byref
from OpenGL.GLU import *
import math


class Window3D(QOpenGLWidget):#todo заменить на QOpenGLWidget
    """Визуализацию ты можешь разместить где то тут.
    Класс QGLWidget это 3д класс для работы с OpenGL графонием.
    Необходим ли он нам и насколько он похож на то, про что ты читал, я пока не знаю.
    https://doc.qt.io/qt-5/qglwidget.html
    """
    height_settings = 2.
    scaling_draft_prime = scaling_draft_prime

    def __init__(self, frame, gcod, gmodal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #draft1
        #self.substrate = 'fuck///40В6М-Р.0402-13_5327425_2735.TIF'
        self.substrate = 'fuck///examples/89.01.112.32.00.00.02_14273099_2735.tif'
        self.alpha = 0.
        #self.max_texture_video_card = 1024#16384
        #self.max_texture_video_card = 1



        self.flag_draft = True

        print('start opengl')
        self.frame = frame
        self.setMinimumSize(100, 100)
        self.gcod = gcod
        self.setMouseTracking(True)
        self.init_vars()
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.showTime)
        d3_interface(self)
        #change_draft(self, self.substrate)
        self.animation_flag = False
        self.frame_frequency = 100
        self.my_timer.start(self.frame_frequency)
        self.setAcceptDrops(True)

        self.draft_zero_vert = 0.0
        self.draft_zero_horiz = 0.0
        self.behavior_mode = ''


    def dropEvent(self, e):
        print(type(e.mimeData().text()))
        print(e.mimeData().text())
        change_draft(self, e.mimeData().text())

    def dragEnterEvent(self, e):
        #if e.mimeData().hasText():
        e.accept()
        #else:
        #    e.ignore()

    # draft1
    def changeTexture(self,image,ix,iy):


        #iy = iy * 0.5
        #print('image.width() = ', image.width())
        glBindTexture(GL_TEXTURE_2D, self.tex) # this is the texture we will manipulate
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, self.gl_format, ix, iy, 0, self.gl_format, GL_UNSIGNED_BYTE, image) # load bitmap to texture
        self.picratio = self.iy / self.ix


    # draft1
    def resetTexture(self):
        if self.flag_draft is True:
            print('type(self.baseimage) = ', type(self.baseimage))
            self.changeTexture(self.baseimage, self.ix, self.iy)
        #glDisable(GL_TEXTURE_2D)

    def init_vars(self):
        self.old_horizo_mouse = 0
        self.old_height_mouse = 0
        self.old_depth = 1
        self.m_grabbing = False
        self.m_turning = False
        self.cam_horizontal = 0
        self.cam_height = 0
        #self.cam_turn_x = 0
        #self.cam_turn_y = 0
        #self.cam_turn_z = 0
        self.turn_angle = 0
        self.k_rapprochement = 1.0
        self.cam_depth = 1
        self.w = self.width()-2#maybe it will work faster
        self.h = self.height()
        self.old_h = self.height()
        self.where_clicked_x = 0
        self.where_clicked_y = 0
        self.turn_angleX = 0
        self.turn_angleY = 0
        self.turn_angleZ = 0
        self.draft_scale = self.scaling_draft_prime * self.k_rapprochement
        self.new_dot1 = None
        self.new_dot2 = None



    def turn_to_turn_view(self):
        print('turn_to_turn_vew')
        self.turn_angleX = 0.
        self.turn_angleY = 90.
        self.turn_angleZ = 90.

    def YX_view(self):
        print('YX_vew')
        self.turn_angleX = 0.
        self.turn_angleY = 0.
        self.turn_angleZ = 90.

    def ZY_view(self):
        print('ZY_vew')
        self.turn_angleX = 0.
        self.turn_angleY = 90.
        self.turn_angleZ = 180.

    def Centre_view(self):
        print('Centre_vew')
        self.draft_zero_horiz = self.draft_zero_horiz - self.cam_horizontal
        self.draft_zero_vert = self.draft_zero_vert - self.cam_height
        self.cam_horizontal = 0.
        self.cam_height = 0.





    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:

        self.my_timer.start(100)
        print('a0.button() = ', a0.button())
        b = a0.button()
        self.where_clicked_x = a0.x()
        self.where_clicked_y = a0.y()
        print('self.where_clicked_x = ', self.where_clicked_x)
        print('self.where_clicked_y = ', self.where_clicked_y)

        print('self.x = ', self.w)
        print('self.y = ', self.h)
        print('mouse button = ', b)
        if b == 1:
            self.m_grabbing = True  # OpenGL has MouseGrabber, but im am not sure if i should rewrite it
        elif b == 4:#wheel button
            self.m_turning = True
        if b == 2:  #rightClick?
            if self.behavior_mode == 'draft_point':
                print('look up')
                L_half_display = self.cam_horizontal/self.w + 2.*(self.w/self.h)
                from_right_border = (1 - self.where_clicked_x/self.w)
                where_clicked_x_in_GL_coord = 2*L_half_display*from_right_border - L_half_display
                where_clicked_y_in_GL_coord = 4*(self.where_clicked_y / self.h)-2
                angle = - (self.alpha * 2 * math.pi / 360)
                super_vert = self.cam_height + where_clicked_y_in_GL_coord
                super_hor = self.cam_horizontal + where_clicked_x_in_GL_coord
                horiz_draft = super_hor * math.cos(angle) - super_vert * math.sin(angle)
                vert_draft = super_vert * math.cos(angle) + super_hor * math.sin(angle)
                self.draft_zero_vert = self.draft_zero_vert + vert_draft
                self.draft_zero_horiz = self.draft_zero_horiz + horiz_draft
                self.behavior_mode = ''
            elif self.behavior_mode == 'choose distance':
                if self.new_dot1 is None:
                    print('yyyyyyyyyyyyyyyy')
                    print('self.k_rapprochement1 = ', self.k_rapprochement)
                    right_border = self.cam_horizontal / self.w + 2. * (self.w / self.h)

                    x_display_coord = 2*right_border * (self.where_clicked_x-self.w/2)/self.w
                    y_display_coord = -2*self.height_settings * (self.where_clicked_y-self.h/2)/self.h
                    self.new_dot1 = [(self.cam_horizontal - x_display_coord)/self.k_rapprochement, (self.cam_height - y_display_coord)/self.k_rapprochement]
                elif self.new_dot2 is None:
                    print('self.k_rapprochement2 = ', self.k_rapprochement)
                    right_border = self.cam_horizontal / self.w + 2. * (self.w / self.h)

                    x_display_coord = 2*right_border * (self.where_clicked_x-self.w/2)/self.w
                    y_display_coord = -2*self.height_settings * (self.where_clicked_y-self.h/2)/self.h
                    self.new_dot2 = [(self.cam_horizontal - x_display_coord)/self.k_rapprochement, (self.cam_height - y_display_coord)/self.k_rapprochement]
                    print('scaling to mm')
                    dlg = ChooseDistanceDialog(self)


                    dlg.exec()
                    #self.behavior_mode = ''
                    #self.new_dot1 = None
                    #self.new_dot2 = None
#



                #self.behavior_mode = ''
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        #print('release a0.button() = ', a0.button())
        b = a0.button()
        if b == 1:
            self.m_grabbing = False
        elif b == 4:  # wheel button
            self.m_turning = False
        #self.timer_stop()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        new_horizo = a0.x()
        new_height = a0.y()
        if self.m_grabbing is True:
            #self.timer_start()
            horiz_mov = 4*(new_horizo - self.old_horizo_mouse) / self.h
            vert_mov = 4*(self.old_height_mouse - new_height) / self.h
            self.cam_horizontal = self.cam_horizontal + horiz_mov
            self.cam_height = self.cam_height + vert_mov
            #problem here
            angle = - (self.alpha * 2 * math.pi / 360)
            #horiz_mov = (horiz_mov + vert_mov * math.tan(angle)) * math.cos(angle)
            #vert_mov = (vert_mov - horiz_mov * math.sin(angle)) / math.cos(angle)

            horiz_draft = horiz_mov * math.cos(angle) - vert_mov * math.sin(angle)
            vert_draft = vert_mov * math.cos(angle) + horiz_mov * math.sin(angle)

            #horiz_draft = horiz_mov * math.cos(angle)
            #vert_draft =  horiz_mov * math.sin(angle)

            #horiz_draft = - vert_mov * math.sin(angle*0.2)
            #vert_draft = vert_mov * math.cos(angle)
            #print('angle = ', angle)
            #print('math.cos(angle) = ', math.cos(angle))

            self.draft_zero_horiz = self.draft_zero_horiz + horiz_draft

            self.draft_zero_vert = self.draft_zero_vert + vert_draft

        elif self.m_turning is True:
            if (self.where_clicked_x - self.w/2) ** 2 + (self.where_clicked_y - self.h/2) ** 2 < 0.1 * self.h * self.h:
                #print('внутри')
                angle_h = 360 * (new_horizo - self.old_horizo_mouse) / self.h
                angle_v = 360 * (self.old_height_mouse - new_height) / self.h
                self.turn_angleX = self.turn_angleX - angle_v
                self.turn_angleY = self.turn_angleY + angle_h
                #self.turn_angle = angle_h + angle_v + self.turn_angle
                if self.turn_angleX > 360. or self.turn_angleX < 360:
                    self.turn_angleX = self.turn_angleX % 360.
                if self.turn_angleY > 360. or self.turn_angleY < 360:
                    self.turn_angleY = self.turn_angleY % 360.

                #self.cam_turn_x = self.cam_turn_x + -(self.old_height_mouse - new_height) / self.h
                #self.cam_turn_y = self.cam_turn_y + -(new_horizo - self.old_horizo_mouse) / self.h
                    #self.cam_turn_z = self.cam_turn_z

                #print('turn_angle ', self.turn_angle)
            else:
                #print('снаружи')
                angle_h = - 360 * (new_horizo - self.old_horizo_mouse) / self.h
                angle_v = - 360 * (self.old_height_mouse - new_height) / self.h

                if self.where_clicked_x > self.w/2:
                    angle_v = - angle_v
                    #print('тут ')
                if self.where_clicked_y > self.h/2:
                    #print('здесь')
                    angle_h = - angle_h

                self.turn_angleZ = self.turn_angleZ + angle_v + angle_h
                if self.turn_angleZ > 360. or self.turn_angleZ < 360:
                    self.turn_angleZ = self.turn_angleZ % 360.
                #self.cam_turn_z = self.cam_turn_z + (new_horizo - self.old_horizo_mouse) / self.h


        self.old_horizo_mouse = new_horizo
        self.old_height_mouse = new_height

    #def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        new_horizo = a0.x()
        new_height = a0.y()
        #print('new_horizo = ', new_horizo)
        #print('self.cam_horizontal ', self.cam_horizontal)
        #print('new_height = ', new_height)
        #print('self.cam_height ', self.cam_height)
        #horiz_mov = 4 * (new_horizo - self.old_horizo_mouse) / self.h

        if a0.angleDelta().y() > 0:
            #glScale(0.8, 0.8, 0.8)
            self.k_rapprochement = self.k_rapprochement / 0.8
            #что на середине экрана
            print('++++ self.k_rapprochement = ', self.k_rapprochement)
            self.cam_height = self.cam_height / 0.8
            self.cam_horizontal = self.cam_horizontal / 0.8

            #сместить
            if self.flag_draft is True:
                self.draft_scale = self.draft_scale / 0.8
                self.draft_zero_horiz = self.draft_zero_horiz / 0.8
                self.draft_zero_vert = self.draft_zero_vert / 0.8
            #print('11111')
        else:
            #glScale(1.2, 1.2, 1.2)
            self.k_rapprochement = self.k_rapprochement / 1.2
            self.cam_height = self.cam_height / 1.2
            self.cam_horizontal = self.cam_horizontal / 1.2
            if self.flag_draft is True:
                self.draft_scale = self.draft_scale / 1.2
                self.draft_zero_horiz = self.draft_zero_horiz / 1.2
                self.draft_zero_vert = self.draft_zero_vert / 1.2
            #print('2222')


    def timer_start(self):
        if self.animation_flag is False:
            self.my_timer.start(self.frame_frequency)

    def timer_stop(self):
        if self.animation_flag is False:
            self.my_timer.stop()

    def showTime(self):
        #Animation
        #print('show')
        #glTranslatef(0.01, 0.0, 0.0)

        self.update()



    def reshape(self, w, h):

        #glViewport(0, 0, w, h)#(GLsizei)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = w / h
        #glOrtho() определяет координатную систему .
        glOrtho(-2.0 * aspect, 2.0 * aspect, -2.0, 2.0,  -2000.0 * aspect, 2000.0 * aspect)
        #self.k_rapprochement = self.k_rapprochement + self.k_rapprochement * aspect
        #glOrtho(-self.h/2, self.h, -self.w/2, self.w/2, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        self.k_rapprochement = self.k_rapprochement * self.h / self.old_h

        self.old_h  = self.h


    def resizeGL(self, w: int, h: int) -> None:
        #print('ggg')
        glViewport(0, 0, w, h)
        k = self.k_rapprochement
        dzv = (self.cam_height - self.draft_zero_vert)/self.draft_scale
        dzhor = (self.cam_horizontal - self.draft_zero_horiz) / self.draft_scale
        self.draft_zero_vert = self.cam_height
        self.draft_zero_horiz = self.cam_horizontal
        #dzh = self.draft_zero_horiz/k
        #self.draft_scale =
        #вот тут всё поменять. а то чертёж не подстраивается
        self.w = w
        self.h = h
        #glLoadIdentity()
        #glScale(1,1,1)
        #Тут размещаются смещения СК глобальные
        #glTranslatef(0.5, 0.0, 0.0)

        self.reshape(w, h)
        self.draft_scale = self.draft_scale * self.k_rapprochement/k
        self.draft_zero_vert = self.draft_zero_vert - dzv * self.draft_scale
        self.draft_zero_horiz = self.draft_zero_horiz - dzhor * self.draft_scale

        #self.draft_zero_horiz = self.draft_zero_horiz - dzh * self.k_rapprochement

        #def view_zone(self, Width, Height):
    #    glViewport(0, 0, Width, Height)
    #    glMatrixMode(GL_PROJECTION)
    #    glLoadIdentity()
    #    aspect = Width/Height
    #    glOrtho(-5, 5, -2, 2, -1.0, 1.0)
    #    #glOrtho(-self.h / 2, self.h/2, -self.w/2, self.w/2, -1.0, 1.0)




    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_POINT_SMOOTH)
        self.draft()
        #ddd
        glClearColor(*OpenGL_color_map_RGBA)
        #self.paint_point()
        glPushMatrix()

        #Тут размещаются смещения СК для объектов (камера)
        glTranslatef(self.cam_horizontal, self.cam_height, 0.0)
        #glRotate(self.turn_angle, self.cam_turn_x, self.cam_turn_y, self.cam_turn_z)
        glRotate(self.turn_angleX, 1., 0., 0.)
        glRotate(self.turn_angleY, 0., 1., 0.)
        glRotate(self.turn_angleZ, 0., 0., 1.)

        self.view_SC()
        glColor3f(1.5, 0.5, 0.5)
        #glPolygonMode(GL_FRONT, GL_FILL)
        glScale(self.k_rapprochement, self.k_rapprochement, self.k_rapprochement)



        self.cub(0.5)

        self.part_turn_points(self.gcod)
        self.part_turn_lines(self.gcod)
        #print('upd self.gcod size = ', self.gcod.shape)
        #angley = 45.
        #glRotate(angley, 0.5, 1, 0.3)

        glFlush()
        #print('screen updated')
        # print(glGetString(GL_VERSION))

        glPopMatrix()

    # draft1
    def draft(self):
        if self.flag_draft is False:
            return

        a = 'white'
        a = 'nope'
        if a == 'white':
            glColor3f(1,1,1)
        else:
            glColor4f(*OpenGL_color_map_RGBA)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
        #glLoadIdentity() # Reset The View
        glBindTexture(GL_TEXTURE_2D, self.tex)# this is the texture we will manipulate
        glEnable(GL_TEXTURE_2D)

        glRotate(self.alpha, 0., 0., 1.)


        dz = -1427

        r = self.ratio / self.picratio# screen h/w  // picture h/w
        #print('self.draft_scale ==== ', self.draft_scale)
        k = self.draft_scale#*2
        hor = self.draft_zero_horiz
        vert = self.draft_zero_vert


        if (r < 1):   # screen wider than image
            dy = 1
            dx = r
        elif (r > 1): # screen taller than image
            dx = 1
            dy = 1 / r
        else:
            dx = 1
            dy = 1

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0); glVertex3f(-k*dx+hor, k*dy+vert, dz)
        glTexCoord2f(1.0, 0.0); glVertex3f(k*dx+hor, k*dy+vert, dz)
        glTexCoord2f(1.0, 1.0); glVertex3f(k*dx+hor, -k*dy+vert, dz)
        glTexCoord2f(0.0, 1.0); glVertex3f(-k*dx+hor, -k*dy+vert, dz)
        glEnd()

        glPointSize(30)
        glBegin(GL_POINTS)
        glColor3f(0.5, 0.5, 0.5)
        glVertex3f(hor, vert, 0.0)
        glColor3f(0.2, 0.5, 0.5)
        glEnd()

        glRotate(-self.alpha, 0., 0., 1.)
        glDisable(GL_TEXTURE_2D)

    def view_SC(self):
        glPointSize(20)
        glBegin(GL_POINTS)
        glColor3f(1.5, 0.5, 0.5)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()
        glLineWidth(5)
        glColor3f(1.5, 0.5, 0.5)
        glBegin(GL_LINES)#X
        glVertex3f(0., 0., 0.)
        #glVertex3f(0.2 * self.k_rapprochement, 0., 0.)
        glVertex3f(0.6, 0., 0.)
        glEnd()

        glColor3f(0.5, 1.5, 0.5)
        glBegin(GL_LINES)#Y
        glVertex3f(0., 0., 0.)
        #glVertex3f(0., 0.2 * self.k_rapprochement,  0.)
        glVertex3f(0., 0.6, 0.)
        glEnd()

        glColor3f(0.5, 0.5, 1.5)
        glBegin(GL_LINES)#Z
        glVertex3f(0., 0., 0.)
        #glVertex3f(0., 0., 0.2 * self.k_rapprochement)
        glVertex3f(0., 0., 0.6)
        glEnd()


    def cub(self, z):
        glLineWidth(8)
        #z = -0.5
        glBegin(GL_LINE_LOOP)
        glColor3f(1, 0, 0)
        glVertex3f(-0.5, -0.5, z)
        glVertex3f(-0.5, 0.5, z)
        glVertex3f(0.5, 0.5, z)
        glVertex3f(0.5, -0.5, z)
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0, 0, 1)
        glVertex3f(-0.5, -0.5, -z)
        glVertex3f(-0.5, -0.5, z)
        glVertex3f(-0.5, 0.5, -z)
        glVertex3f(-0.5, 0.5, z)
        glVertex3f(0.5, 0.5, -z)
        glVertex3f(0.5, 0.5, z)
        glVertex3f(0.5, -0.5, -z)
        glVertex3f(0.5, -0.5, z)
        glEnd()

        glBegin(GL_LINE_LOOP)
        z = z * (-1)
        glColor3f(0, 1, 0)
        glVertex3f(-0.5, -0.5, z)
        glVertex3f(-0.5, 0.5, z)
        glVertex3f(0.5, 0.5, z)
        glVertex3f(0.5, -0.5, z)
        glEnd()



    def paint_point(self):
        glPushMatrix()
        #glScale(1., 1., 1.)

        glPointSize(20)
        glBegin(GL_POINTS)
        glColor3f(1.5, 0.5, 0.5)
        glVertex3f(0.0, 0.0, 0.0)
        glColor3f(0.5, 0.5, 0.5)
        glVertex3f(1.0, 1.0, 0.0)
        glColor3f(0.6, 0.1, 0.3)
        glVertex3f(1.0, -1.0, 0.0)
        glColor3f(0.2, 0.7, 0.0)
        glVertex3f(-1.0, -1.0, 0.0)
        glColor3f(0.0, 0.5, 0.8)
        glVertex3f(-1.0, 1.0, 0.0)
        glEnd()
        glPopMatrix()

    def initializeGL(self):
        #glfwWindowHint(GLFW_SAMPLES, 4)
        #glEnable(GL_MULTISAMPLE)
        # draft1
        buf = GLint()
        glGetIntegerv(GL_MAX_TEXTURE_SIZE, byref(buf))
        self.max_texture_video_card = buf.value
        resize_texture(self, self.substrate)
        self.tex = glGenTextures(1)
        print('self.tex = ', self.tex)


        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)

        #glfwWindowHint(GLFW_SAMPLES, 4)
        #glWindow
        #glEnable(GL_MULTISAMPLE)

        glLoadIdentity()
        self.resetTexture()

        #self.view_zone(700, 600)
        #

    def part_turn_points(self, np_list):
        glPointSize(7)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_POINTS)
        for i in np_list:
            if np.isnan(i[16]):
                glVertex3f(i[4], i[5], i[6])
                if i[2] == 2 or i[2] == 3:
                    glVertex3f(i[10], i[11], i[12])
            else:
                pass
                #special_pont_options(i[16], i[4], i[5], i[6])
        glEnd()
        glPopMatrix()

    def part_turn_lines(self, np_list):
        #glPointSize(5)

        glPushMatrix()
        glLineWidth(3)
        glColor3f(*OpenGL_color_G0_line)
        glBegin(GL_LINE_STRIP)
        #new_np_line = [0, *self.processor.start_pointXYZ, 0, 0, 0, 0]
        #previous_list = copy.deepcopy(new_np_line)
        # print('self.processor.start_pointXYZ[:] = ', *self.processor.start_pointXYZ)
        # print('new_np_line = ', new_np_line)
        #glVertex3f(new_np_line[1], new_np_line[2], new_np_line[3])
        g0_g1 = 0
        for i in np_list:
            # print('x = {}, y = {}, z = {}'.format(i[1], i[2], i[3]))
            # glRotate(i[5] or new_np_line[5], 1., 0., 0.)
            # glRotate(i[6] or new_np_line[6], 0., 1., 0.)
            # glRotate(i[4] or new_np_line[4], 0., 0., 1.)
            #print('zero')
            if g0_g1 != i[3]:
                if i[3] == 0:
                    glColor3f(*OpenGL_color_G0_line)
                    #print('check2222')
                else:
                    glColor3f(*OpenGL_color_G1_line)
                    #print('check3333')
                g0_g1 = i[3]
            if np.isnan(i[16]):
                #print('np.isnan(i[14])')
                glVertex3f(i[4], i[5], i[6])
            else:
                special_pont_options(i[16], i[4], i[5], i[6])

        glEnd()
        glPopMatrix()




def special_pont_options(i, i1, i2, i3):
    if i == 0:
        glVertex3f(i1, i2, i3)
    elif i == 5:
        #glColor3f(*OpenGL_color_extra1_point)
        #glPointSize(4)без шейдера работать не будет
        glVertex3f(i1, i2, i3)
        #r = 20
        # move camera a distance r away from the center
        #glTranslatef(0, 0, -r)
        #angley = 45.
        #anglex = 0.0

        # rotate
        #glRotate(angley, 0.5, 1, 0.3)
        #glRotatef(anglex, 1, 0, 0);

        # move to center of circle
        #glTranslatef(-cx, -cy, -cz)

        #self.resizeGL(1000,1000)
        # gluPerspective(0.0,0.,0.0, 0.0)
        # glMatrixMode(GL_MODELVIEW)

