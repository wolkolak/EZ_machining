from PyQt5.QtWidgets import QTabWidget, QFrame, QPlainTextEdit,  QWidget, QGridLayout, QPushButton, QLabel, QDialog, QLineEdit
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtOpenGL import QGLWidget
from OpenGL.GL import *
from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QResizeEvent, QPixmap, QDoubleValidator
from Settings.settings import *
import numpy as np
import cv2
from Settings.settings import scaling_draft_prime
import math
import re
from freetype import *


def restore_zero_position_shell(func):
    def wrapper(self, scene, *args):
        ugol = -(scene.alpha * 2 * math.pi / 360)
        pod_uglom_x = scene.cam_horizontal * math.cos(ugol) - scene.cam_height * math.sin(ugol)#СК в косой системе
        pod_uglom_y = scene.cam_height * math.cos(ugol) + scene.cam_horizontal * math.sin(ugol)
        position_hor = (pod_uglom_x - scene.draft_zero_horiz) / scene.draft_scale
        position_ver = (pod_uglom_y - scene.draft_zero_vert) / scene.draft_scale
        scene.draft_zero_horiz = pod_uglom_x
        scene.draft_zero_vert = pod_uglom_y
        func(self, scene, *args)
        scene.draft_zero_horiz = scene.draft_zero_horiz - position_hor * scene.draft_scale
        scene.draft_zero_vert = scene.draft_zero_vert - position_ver * scene.draft_scale
    return wrapper

def d3_interface(self):
    # draft1
    #garbage, new_image_address = self.substrate.split(r'///')
    #print('jjjjjjjjjj ', self)
    #self.initializeGL()

    self.grid = QGridLayout(self)

    # grid.setRowStretch(0, 20)
    # grid.setColumnStretch(0, 30)
    self.setLayout(self.grid)
    self.scene_ZX = QPushButton('Turn (XZ)')#scene_XZ
    add_widget_to_scene(self, self.scene_ZX, self.turn_to_turn_view, 60, 30, 0, 0)
    self.scene_YX = QPushButton('YX')#scene_XY
    add_widget_to_scene(self, self.scene_YX, self.YX_view, 60, 30, 0, 1)
    self.scene_ZY = QPushButton('ZY')#scene_XY
    add_widget_to_scene(self, self.scene_ZY, self.ZY_view, 60, 30, 0, 2)
    self.scene_Centre = QPushButton('Centre')#scene_XY
    add_widget_to_scene(self, self.scene_Centre, self.Centre_view, 60, 30, 0, 3)

    self.grid.setColumnMinimumWidth(5, 2000)



def add_widget_to_scene(self, widget, func, fw, fh, posH, posV, align=Qt.AlignTop | Qt.AlignLeft):
    widget.clicked.connect(func)
    widget.setFixedWidth(fw)
    widget.setFixedHeight(fh)
    self.grid.addWidget(widget, posH, posV, align)

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
        self.substrate = f#new_image_address
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

class ChooseDistanceDialog(QDialog):
    def __init__(self, father, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.father = father
        self.setWindowTitle("Distance, mm")
        self.setFixedSize(240, 100)
        self.validate_text_digit()
        grid = QGridLayout()
        self.setLayout(grid)
        self.distance_edit = QLineEdit()
        self.distance_edit.setValidator(self.onlyInt)
        grid.addWidget(self.distance_edit, 0, 0)
        self.OK_distance_edit = QPushButton('OK')
        self.OK_distance_edit.clicked.connect(lambda: self.resize_draft_to_mm(self.father))
        self.OK_distance_edit.setFixedSize(60, 23)
        grid.addWidget(self.OK_distance_edit, 0, 1)
        self.choose_label = QLabel()
        grid.addWidget(self.choose_label, 1, 0, 1, 2)
        choose_im = QPixmap('icons/distance.png')
        self.choose_label.setPixmap(choose_im)

    def validate_text_digit(self):
        self.onlyInt = QDoubleValidator()
        local_field = QtCore.QLocale(QtCore.QLocale.English)
        self.onlyInt.setLocale(local_field)

    @restore_zero_position_shell
    def resize_draft_to_mm(self, scene):
        print('resize_draft_to_mm')
        x_px1 = scene.new_dot1[0]
        y_px1 = scene.new_dot1[1]
        x_px2 = scene.new_dot2[0]
        y_px2 = scene.new_dot2[1]
        distance_number = float(self.distance_edit.text())
        distance_measured_px = math.sqrt((x_px1-x_px2)**2 + (y_px1-y_px2)**2)
        pixes_in_mm = distance_number/distance_measured_px
        #top_border = self.father.height_settings
        #right_border = self.father.cam_horizontal / self.father.w + 2. * (self.father.w / self.father.h)
        #print('pixes_in_mm = ', pixes_in_mm)
        scene.scaling_draft_prime = scene.scaling_draft_prime * pixes_in_mm#/200
        scene.draft_scale = scene.scaling_draft_prime * scene.k_rapprochement
        #self.father.draft_scale = self.father.draft_scale*pixes_in_mm/1000*12

        print('distance')
        print('y_px2 = self.father.new_dot2[1] = ', y_px2)
        #scene.behavior_mode = ''
        #scene.new_dot1 = None
        #scene.new_dot2 = None
        self.close()

    def done(self, a0: int) -> None:
        print('choose distance done')
        self.father.refresh()
        #self.father.behavior_mode = ''
        #self.father.new_dot1 = None
        #self.father.new_dot2 = None
        QDialog.done(self, a0)

def make_label(text, filename, size=12, angle=0):
    '''
    Parameters:
    -----------
    text : string
        Text to be displayed
    filename : string
        Path to a font
    size : int
        Font size in 1/64th points
    angle : float
        Text angle in degrees
    '''
    face = Face(filename)
    face.set_char_size( size*64 )
    angle = (angle/180.0)*math.pi
    matrix  = FT_Matrix( (int)( math.cos( angle ) * 0x10000 ),
                         (int)(-math.sin( angle ) * 0x10000 ),
                         (int)( math.sin( angle ) * 0x10000 ),
                         (int)( math.cos( angle ) * 0x10000 ))
    flags = FT_LOAD_RENDER
    pen = FT_Vector(0,0)
    FT_Set_Transform( face._FT_Face, byref(matrix), byref(pen) )
    previous = 0
    xmin, xmax = 0, 0
    ymin, ymax = 0, 0
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(previous, c)
        previous = c
        width = face.glyph.bitmap.width
        rows = face.glyph.bitmap.rows
        top = face.glyph.bitmap_top
        left = face.glyph.bitmap_left
        pen.x += kerning.x
        x0 = (pen.x >> 6) + left
        x1 = x0 + width
        y0 = (pen.y >> 6) - (rows - top)
        y1 = y0 + rows
        xmin, xmax = min(xmin, x0),  max(xmax, x1)
        ymin, ymax = min(ymin, y0), max(ymax, y1)
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    L = np.zeros((ymax-ymin, xmax-xmin), dtype=np.ubyte)
    previous = 0
    pen.x, pen.y = 0, 0
    for c in text:
        face.load_char(c, flags)
        kerning = face.get_kerning(previous, c)
        previous = c
        bitmap = face.glyph.bitmap
        pitch  = face.glyph.bitmap.pitch
        width  = face.glyph.bitmap.width
        rows   = face.glyph.bitmap.rows
        top    = face.glyph.bitmap_top
        left   = face.glyph.bitmap_left
        pen.x += kerning.x
        x = (pen.x >> 6) - xmin + left
        y = (pen.y >> 6) - ymin - (rows - top)
        data = []
        for j in range(rows):
            data.extend(bitmap.buffer[j*pitch:j*pitch+width])
        if len(data):
            Z = np.array(data, dtype=np.ubyte).reshape(rows, width)
            L[y:y+rows, x:x+width] |= Z[::-1, ::1]
        pen.x += face.glyph.advance.x
        pen.y += face.glyph.advance.y

    return L