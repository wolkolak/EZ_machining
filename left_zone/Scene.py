from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PyQt5 import QtGui
from left_zone.D3_interface import d3_interface
from PyQt5.QtGui import QResizeEvent
from Settings.settings import *
import numpy as np
from HLSyntax.PostProcessors_revers.Fanuc_NT import Fanuc_NT
import copy


class Window3D(QGLWidget):
    """Визуализацию ты можешь разместить где то тут.
    Класс QGLWidget это 3д класс для работы с OpenGL графонием.
    Необходим ли он нам и насколько он похож на то, про что ты читал, я пока не знаю.
    https://doc.qt.io/qt-5/qglwidget.html
    """
    def __init__(self, frame, gcod, gmodal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('start opengl')
        self.frame = frame
        self.setMinimumSize(100, 100)
        self.gcod = gcod
        self.setMouseTracking(True)
        self.init_vars()
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.showTime)
        d3_interface(self)
        #self.processor = Fanuc_NT()#todo
            #self.frame.left_tab.parent.central_widget.note.currentWidget().\
            #highlight.reversal_post_processor
        self.animation_flag = False
        self.frame_frequency = 100
        self.my_timer.start(self.frame_frequency)
        #self.my_timer.stop()
    #def choosing_backplotter(self):
    #    self.processor = self.frame.left_tab.parent.central_widget.note.currentWidget()

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
        self.w = self.width()#maybe it will work faster
        self.h = self.height()
        self.old_h = self.height()
        self.where_clicked_x = 0
        self.where_clicked_y = 0
        self.turn_angleX = 0
        self.turn_angleY = 0
        self.turn_angleZ = 0

    def turn_to_turn_vew(self):
        print('turn_to_turn_vew')
        self.turn_angleX = 0.
        self.turn_angleY = 90.
        self.turn_angleZ = 90.

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.my_timer.start(100)
        print('a0.button() = ', a0.button())
        b = a0.button()
        self.where_clicked_x = a0.x()
        self.where_clicked_y = a0.y()
        print('self.where_clicked_x = ', self.where_clicked_x)

        if b == 1:
            self.m_grabbing = True
        elif b == 4:#wheel button
            self.m_turning = True
    #    self.horizontal = self.horizontal - 0.01
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        print('release a0.button() = ', a0.button())
        b = a0.button()
        if b == 1:
            self.m_grabbing = False
        elif b == 4:  # wheel button
            self.m_turning = False
        #self.timer_stop()

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:

        #работает только на грабе?
        new_horizo = a0.x()
        #print('self.m_grabbing = ', self.m_grabbing)
        new_height = a0.y()
        if self.m_grabbing is True:
            #self.timer_start()
            self.cam_horizontal = self.cam_horizontal + self.k_rapprochement * (new_horizo - self.old_horizo_mouse) / self.h
            self.cam_height = self.cam_height + self.k_rapprochement * (self.old_height_mouse - new_height) / self.h
            #self.cam_height = new_height
        elif self.m_turning is True:
            #print('turn turn turn')
            #self.timer_start()
            #if 0.2 * self.w < self.where_clicked_x < 0.8 * self.w and 0.2 * self.h < self.where_clicked_y < 0.8 * self.h:
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
        if a0.angleDelta().y() > 0:
            glScale(0.8, 0.8, 0.8)
            self.k_rapprochement = self.k_rapprochement / 0.8
            #print('11111')
        else:
            glScale(1.2, 1.2, 1.2)
            self.k_rapprochement = self.k_rapprochement / 1.2
            #print('2222')
        #print('wheel k_rapprochement = ', self.k_rapprochement)

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
        glOrtho(-2.0 * aspect, 2.0 * aspect, -2.0, 2.0,  -2.0 * aspect, 2.0 * aspect)
        #self.k_rapprochement = self.k_rapprochement + self.k_rapprochement * aspect
        #glOrtho(-self.h/2, self.h, -self.w/2, self.w/2, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        self.k_rapprochement = self.k_rapprochement * self.h / self.old_h

        self.old_h  = self.h


    def resizeGL(self, w: int, h: int) -> None:
        #print('ggg')
        glViewport(0, 0, w, h)
        self.w = w
        self.h = h
        #glLoadIdentity()
        #glScale(1,1,1)
        #Тут размещаются смещения СК глобальные
        #glTranslatef(0.5, 0.0, 0.0)
        self.reshape(w, h)


    #def view_zone(self, Width, Height):
    #    glViewport(0, 0, Width, Height)
    #    glMatrixMode(GL_PROJECTION)
    #    glLoadIdentity()
    #    aspect = Width/Height
    #    glOrtho(-5, 5, -2, 2, -1.0, 1.0)
    #    #glOrtho(-self.h / 2, self.h/2, -self.w/2, self.w/2, -1.0, 1.0)


    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.85, 0.85, 0.8, 1.)
        glEnable(GL_POINT_SMOOTH)

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
        glVertex3f(0.2 * self.k_rapprochement, 0., 0.)
        glEnd()

        glColor3f(0.5, 1.5, 0.5)
        glBegin(GL_LINES)#Y
        glVertex3f(0., 0., 0.)
        glVertex3f(0., 0.2 * self.k_rapprochement,  0.)
        glEnd()

        glColor3f(0.5, 0.5, 1.5)
        glBegin(GL_LINES)#Z
        glVertex3f(0., 0., 0.)
        glVertex3f(0., 0., 0.2 * self.k_rapprochement)
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
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        #self.view_zone(700, 600)
        #

    def part_turn_points(self, np_list):
        glPointSize(5)
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_POINTS)
        for i in np_list:
            if np.isnan(i[14]):
                glVertex3f(i[2], i[3], i[4])
                if i[0] == 2 or i[0] == 3:
                    glVertex3f(i[8], i[9], i[10])
            else:
                special_pont_options(i[14], i[2], i[3], i[4])
        glEnd()
        glPopMatrix()

    def part_turn_lines(self, np_list):
        #glPointSize(5)
        glPushMatrix()
        glLineWidth(3)
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_LINE_STRIP)
        #new_np_line = [0, *self.processor.start_pointXYZ, 0, 0, 0, 0]
        #previous_list = copy.deepcopy(new_np_line)
        # print('self.processor.start_pointXYZ[:] = ', *self.processor.start_pointXYZ)
        # print('new_np_line = ', new_np_line)
        #glVertex3f(new_np_line[1], new_np_line[2], new_np_line[3])
        for i in np_list:
            # print('x = {}, y = {}, z = {}'.format(i[1], i[2], i[3]))
            # glRotate(i[5] or new_np_line[5], 1., 0., 0.)
            # glRotate(i[6] or new_np_line[6], 0., 1., 0.)
            # glRotate(i[4] or new_np_line[4], 0., 0., 1.)
            #print('zero')
            if np.isnan(i[14]):
                #print('np.isnan(i[14])')
                glVertex3f(i[2], i[3], i[4])
            else:
                special_pont_options(i[14], i[2], i[3], i[4])
                #x, y, z = i[1], i[2], i[3]
                #if np.isnan(x):
                #    x = previous_list[1]
                #if np.isnan(y):
                #    y = previous_list[2]
                #if np.isnan(z):
                #    z = previous_list[3]
                #glVertex3f(x, y, z)
                #previous_list[1:4] = x, y, z
            #else:
            #    pass
            #    #print('special paint')
        glEnd()
        glPopMatrix()

def special_pont_options(i, i1, i2, i3):
    if i == 0:
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

