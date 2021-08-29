from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtGui import QResizeEvent, QPixmap
from Settings.settings import *
import numpy as np
import cv2
from Settings.settings import scaling_draft_prime

def d3_interface(self):
    # draft1
    #garbage, new_image_address = self.substrate.split(r'///')
    #print('jjjjjjjjjj ', self)
    #self.initializeGL()

    grid = QGridLayout(self)

    # grid.setRowStretch(0, 20)
    # grid.setColumnStretch(0, 30)
    self.setLayout(grid)
    self.a = QPushButton('Turn View')
    self.a.clicked.connect(self.turn_to_turn_vew)
    self.a.setFixedWidth(60)
    self.a.setFixedHeight(30)
    grid.addWidget(self.a, 0, 0, Qt.AlignTop | Qt.AlignLeft)

def change_draft(self, new_image_address):
        self.substrate = new_image_address
        d3_interface(self)
        # do scalling
        resize_texture(self, self.substrate)

        self.draft()
        self.resetTexture()


def resize_texture(self,  new_image_address, scaling_draft_prime=scaling_draft_prime):
    try:
        self.flag_draft = False
        #Image.MAX_IMAGE_PIXELS = None
        print('new_image_address == ', new_image_address)
        garbage, new_image_address = new_image_address.split(r'///')
        if new_image_address:
            f = new_image_address
        else:
            f = garbage
        self.substrate = new_image_address
        im = QtGui.QImage(f)
        self.ix = im.width()
        self.iy = im.height()
        x_k = 1
        y_k = 1
        if self.ix > self.max_texture_video_card:
            x_k = self.ix / self.max_texture_video_card
        if self.iy > self.max_texture_video_card:
            y_k = self.iy / self.max_texture_video_card
        if x_k > y_k:
            new_x = self.ix / x_k
            new_y = self.iy / x_k
        else:# x_k > y_k:
            new_x = self.ix / y_k
            new_y = self.iy / y_k

        self.ix = new_x
        self.iy = new_y
        print('self.ix = {}, self.iy = {}'.format(self.ix, self.iy))
        im = im.smoothScaled(self.ix, self.iy)
        im = im.convertToFormat(QtGui.QImage.Format_RGB888)
        ptr = im.scanLine(0)
        ptr.setsize(im.sizeInBytes())
        self.baseimage = ptr.asstring()
        self.gl_format = GL_RGB
        self.ratio = 1
        self.picratio = 1
        self.draft_scale = scaling_draft_prime * self.k_rapprochement#число должно зависеть от
        self.flag_draft = True
        print('next222')

    except:
        print('File opening failed. Either it is not an image, either it is broken')
        self.flag_draft = False
    #finally:


