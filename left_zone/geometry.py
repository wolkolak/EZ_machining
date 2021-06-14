from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = glWidget(self)
        self.button = QPushButton('Test', self)
        self.button.setMaximumWidth(80)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.widget)
        mainLayout.addWidget(self.button)
        self.setLayout(mainLayout)

class glWidget(QGLWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(840, 480)



    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glEnable(GL_POINT_SMOOTH)
        glTranslatef(-1.1, 0.0, 0.0)
        glColor3f(1.5, 0.5, 0.5)
        glPolygonMode(GL_FRONT, GL_FILL)
        glPointSize(30)
        self.paint_point(0.5, 0.5, 0.)
        glFlush()
        #print(glGetString(GL_VERSION))

    def paint_point(self, x, y, z):
        glBegin(GL_POINTS)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glEnd()


    def initializeGL(self):
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #gluPerspective(0.0,0.,0.0, 0.0)
        #glMatrixMode(GL_MODELVIEW)


if __name__ == '__main__':
    app = QApplication(['Yo'])
    window = MainWindow()
    window.show()
    app.exec_()