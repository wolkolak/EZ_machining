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
        self.horizontal = 0
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.showTime)
        #self.mouseGrabber.connect(self.camera_move)

    #def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
    #    self.horizontal = self.horizontal - 0.01


    def grabMouse(self) -> None:
        self.horizontal = self.horizontal - 0.01

    #def eventFilter(self, a0: 'QObject', a1: 'QEvent') -> bool:


    def showTime(self):
        #Animation
        print('show')
        #glTranslatef(0.01, 0.0, 0.0)
        self.update()




    def resizeGL(self, w: int, h: int) -> None:
        #print('ggg')
        glViewport(0, 0, w, h)
        glLoadIdentity()
        #Тут размещаются смещения СК глобальные
        #glTranslatef(0.5, 0.0, 0.0)



    def view_zone(self, Width, Height):
        glViewport(0, 0, Width, Height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-5, 5, -5, 5, 2, 12)


    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        #Тут размещаются смещения СК для объектов
        glTranslatef(self.horizontal, 0.0, 0.0)


        glEnable(GL_POINT_SMOOTH)

        glColor3f(1.5, 0.5, 0.5)
        #glPolygonMode(GL_FRONT, GL_FILL)
        glPointSize(20)

        #angley = 45.
        #glRotate(angley, 0.5, 1, 0.3)
        self.paint_point(0.5, 0.5, 0.)
        glFlush()
        #print('screen updated')
        # print(glGetString(GL_VERSION))

        glPopMatrix()



    def paint_point(self, x, y, z):
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

    def camera_move(self):
        #glTranslatef(0.1, 0.0, 0.0)
        print('move')

    def camera_turn(self):
        print('turn')

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

