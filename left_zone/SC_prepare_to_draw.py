from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from PIL import Image
import numpy as np




def prepare_SC(address):
    im_frame = Image.open(address)
    I = np.array(im_frame.getdata())
    W, H = im_frame.size

    glyph_tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, glyph_tex)  # this is the texture we will manipulate
    # texture options
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA,
                 GL_UNSIGNED_BYTE, I)  # bitmap.buffer I
    return glyph_tex

def prepare_SC_s_texture(g54_g59_AXIS, g54_g59_default):
    SC_s_dict = {}
    base_address = r'Settings\textTextures\G549\\'
    for key_ in g54_g59_AXIS:
        address549 = base_address + key_ + '.png'
        texture54 = prepare_SC(address=address549)
        G549text = prepare_text_G549(typing_height=1, glyph_tex=texture54)
        SC_s_dict[key_] = G549text

    address549 = base_address + g54_g59_default + 'main' + '.png'
    texture549 = prepare_SC(address=address549)
    G549text = prepare_text_G549(typing_height=1, glyph_tex=texture549)
    SC_s_dict[g54_g59_default] = G549text

    return SC_s_dict


#def prepare_SC_s1():
#    SC_s_dict = {}
#    address54 = r'Settings\textTextures\G54main.png'
#    texture54 = prepare_SC(address=address54)
#
#    SC_s_dict['G54'] = texture54
#
#    return SC_s_dict

def prepare_text_G549(typing_height, glyph_tex):
    G549text = glGenLists(1)
    glNewList(G549text, GL_COMPILE)
    h = typing_height
    dz = 0
    glColor3f(1., 1.0, 1.0)
    glBindTexture(GL_TEXTURE_2D, glyph_tex)  # this is the texture we will manipulate

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_TEXTURE_2D)
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(0, 3, dz)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(5, 3, dz)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(5, 3 - h, dz)
    # glVertex3f(1.8, -2., dz)#
    glTexCoord2f(0.0, 1.0)
    glVertex3f(0, 3 - h, dz)
    # glVertex3f(-1.5, -2., dz)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)
    glEndList()
    return G549text


#def draw_SC_texture(behavior_mode, SC_s_dict):#todo выкинуть
#    #print('draw_SC_texture')
#    if behavior_mode == '':
#        return
#    else:
#        glCallList(SC_s_dict['G54'])
#    # dz = -1427
#    # typing


#def draw_SC():
#    pass