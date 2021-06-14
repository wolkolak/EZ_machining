from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PyQt5 import QtGui
from PyQt5.QtGui import QResizeEvent
from Settings.settings import *
import numpy as np

class Window3D(QGLWidget):
    """Визуализацию ты можешь разместить где то тут.
    Класс QGLWidget это 3д класс для работы с OpenGL графонием.
    Необходим ли он нам и насколько он похож на то, про что ты читал, я пока не знаю.
    https://doc.qt.io/qt-5/qglwidget.html
    """
    def __init__(self, gcod, gmodal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('start opengl')
        self.setMinimumSize(100, 100)
        self.gcod = gcod
        self.old_horizo = 0
        self.old_height = 0
        self.old_depth = 1
        self.m_grabbing = False
        self.setMouseTracking(True)
        self.cam_horizontal = 0
        self.cam_height = 0
        self.cam_depth = 1
        self.w = self.width()#maybe it will work faster
        self.h = self.height()
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.showTime)


    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.m_grabbing = True
    #    self.horizontal = self.horizontal - 0.01
    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.m_grabbing = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        #работает только на грабе?
        new_horizo = a0.x()
        #print('self.m_grabbing = ', self.m_grabbing)
        new_height = a0.y()
        if self.m_grabbing is True:
            self.cam_horizontal = self.cam_horizontal + (new_horizo - self.old_horizo)/self.w
            self.cam_height = self.cam_height + (self.old_height - new_height)/self.h
            #self.cam_height = new_height
        self.old_horizo = new_horizo
        self.old_height = new_height

    #def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:

    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        print('wheel')
        glScale(0.9, 0.9, 0.9)

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
        glOrtho(-2.0 * aspect, 2.0 * aspect, -2.0, 2.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



    def resizeGL(self, w: int, h: int) -> None:
        #print('ggg')
        glViewport(0, 0, w, h)
        self.w = w
        self.h = h
        glLoadIdentity()
        glScale(1,1,1)
        #Тут размещаются смещения СК глобальные
        #glTranslatef(0.5, 0.0, 0.0)
        #self.reshape(w, h)


    def view_zone(self, Width, Height):
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-5, 5, -5, 5, 2, 12)


    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_POINT_SMOOTH)
        self.paint_point(0.5, 0.5, 0.)
        glPushMatrix()
        #Тут размещаются смещения СК для объектов
        glTranslatef(self.cam_horizontal, self.cam_height, 0.0)




        glColor3f(1.5, 0.5, 0.5)
        #glPolygonMode(GL_FRONT, GL_FILL)
        self.cub(0.5)

        #angley = 45.
        #glRotate(angley, 0.5, 1, 0.3)

        glFlush()
        #print('screen updated')
        # print(glGetString(GL_VERSION))

        glPopMatrix()

    def cub(self, z):
        glLineWidth(5)
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



    def paint_point(self, x, y, z):
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


    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        self.view_zone(700, 600)
        self.my_timer.start(100)




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

