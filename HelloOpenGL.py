from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtOpenGL import *
from OpenGL.arrays import vbo
import sys
from PyQt5.QtWidgets import QApplication, QSlider, QMainWindow
from PyQt5.QtWidgets import QWidget,  QVBoxLayout
import numpy as np

class GLWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

            
    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 255))    # initialize the screen to blue
        glEnable(GL_DEPTH_TEST)                  # enable depth testing

        self.initGeometry()

        self.rotX = 0.0
        self.rotY = 0.0
        self.rotZ = 0.0
         
    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)

        gluPerspective(45.0, aspect, 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glPushMatrix()    # push the current matrix to the current stack

        glTranslate(0.0, 0.0, -50.0)    # third, translate cube to specified depth
        glScale(20.0, 20.0, 20.0)       # second, scale cube
        glRotate(self.rotX, 1.0, 0.0, 0.0)
        glRotate(self.rotY, 0.0, 1.0, 0.0)
        glRotate(self.rotZ, 0.0, 0.0, 1.0)
        glTranslate(-0.5, -0.5, -0.5)   # first, translate cube center to origin

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)

        glVertexPointer(3, GL_FLOAT, 0, self.vertVBO)
        glColorPointer(3, GL_FLOAT, 0, self.colorVBO)

        glDrawElements(GL_QUADS, len(self.cubeIdxArray), GL_UNSIGNED_INT, self.cubeIdxArray)

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)

        glPopMatrix()    # restore the previous modelview matrix
        
    def initGeometry(self):
        self.cubeVtxArray = np.array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()
        
        self.cubeClrArray = np.array(
                [[0.0, 0.0, 0.0],
                 [1.0, 0.0, 0.0],
                 [1.0, 1.0, 0.0],
                 [0.0, 1.0, 0.0],
                 [0.0, 0.0, 1.0],
                 [1.0, 0.0, 1.0],
                 [1.0, 1.0, 1.0],
                 [0.0, 1.0, 1.0 ]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))
        self.colorVBO.bind()

        self.cubeIdxArray = np.array(
                [0, 1, 2, 3,
                 3, 2, 6, 7,
                 1, 0, 4, 5,
                 2, 1, 5, 6,
                 0, 3, 7, 4,
                 7, 6, 5, 4 ])

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val

        
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)   # call the init for the parent class
        
        self.resize(300, 300)
        self.setWindowTitle('Hello OpenGL App')

        self.glWidget = GLWidget(self)
        self.initGUI()
        
        timer = QtCore.QTimer(self)
        timer.setInterval(20)   # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()
        
    def initGUI(self):
        central_widget = QWidget()
        gui_layout = QVBoxLayout()
        central_widget.setLayout(gui_layout)

        self.setCentralWidget(central_widget)

        gui_layout.addWidget(self.glWidget)

        sliderX = QSlider(QtCore.Qt.Horizontal)
        sliderX.valueChanged.connect(lambda val: self.glWidget.setRotX(val))

        sliderY = QSlider(QtCore.Qt.Horizontal)
        sliderY.valueChanged.connect(lambda val: self.glWidget.setRotY(val))

        sliderZ = QSlider(QtCore.Qt.Horizontal)
        sliderZ.valueChanged.connect(lambda val: self.glWidget.setRotZ(val))
        
        gui_layout.addWidget(sliderX)
        gui_layout.addWidget(sliderY)
        gui_layout.addWidget(sliderZ)

        
if __name__ == '__main__':

    app = QApplication(sys.argv)
    
    win = MainWindow()
    win.show()

    sys.exit(app.exec_())
    
