from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtGui import QResizeEvent, QPixmap
from Settings.settings import *
import numpy as np

def d3_interface(self):
    # draft1
    #garbage, new_image_address = self.substrate.split(r'///')
    print('jjjjjjjjjj')
    resize_texture(self, self.substrate)
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
    #try:
            self.substrate = new_image_address
            #d3_interface(self)


            #self.draft_scale = 1.0
            resize_texture(self, self.substrate)
            # do scalling

            self.draft()
            self.resetTexture()
    #except:
    #    print('File opening failed. Either it is not an image, either it is broken')

def resize_texture(self,  new_image_address):
    try:
        print('new_image_address == ', new_image_address)
        garbage, new_image_address = new_image_address.split(r'///')
        if new_image_address:
            f = new_image_address
        else:
            f = garbage

        with Image.open(f) as im:
            im.verify()  # I perform also verify, don't know if he sees other types o defects
            im.close()  # reload is necessary in my case
            #width, height = im.size
            self.substrate = new_image_address
            self.baseimage, self.ix, self.iy = self.getImg(new_image_address)
            self.gl_format = GL_RGB
            self.ratio = 1
            self.picratio = 1
            self.draft_scale = 12.0#число должно зависеть от
            self.flag_draft = True
    except:
        print('File opening failed. Either it is not an image, either it is broken')
        self.flag_draft = False