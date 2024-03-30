from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from PyQt5 import QtGui
from left_zone.D3_interface import d3_interface, change_draft, resize_texture, ChooseDistanceDialog
from Settings.settings import *
import numpy as np
from PIL import Image
from ctypes import byref
from OpenGL.GLU import *
import math
from left_zone.D3_interface import restore_zero_position_shell, make_label
import os
from scipy.spatial.transform import Rotation
from Core.Machine_behavior.machine_assemble import ASSEMBLE_MACHINE
from Core.Machine_behavior.MachiningSCpreparation import give_G549_shift
from left_zone.SCENE_INIT import init_vars
from left_zone.SC_prepare_to_draw import prepare_SC_s_texture #draw_SC #draw_SC_texture

from Core.Machine_behavior.Draw_fincs_universe_TRJt_factorial_64 import order_rotation

from left_zone.additional_functions import read_tool_file, choose_tool_function

from Core.Machine_behavior.angles_compute_for_machine_parts import A_table_function, B_table_function, C_table_function, \
    A_head_function, B_head_function, C_head_function, last_head_move
from Core.Machine_behavior.machine_transmigrations_forward import TR_ABC, RT_ABC
from Core.Machine_behavior.machine_transmigrations_return import return_TR_CBA, return_RT_CBA

#def new_position_object_shell(func):
#    def wrapper(self, ax1, ax2, ax3, angle1, angle2, angle3, *args):
#        glTranslatef(ax1, ax2, ax3)
#        glRotate(angle1, 1., 0., 0.)
#        glRotate(angle2, 0., 1., 0.)
#        glRotate(angle3, 0., 0., 1.)
#        func(self, ax1, ax2, ax3, angle1, angle2, angle3, *args)
#        glRotate(-angle3, 0., 0., 1.)
#        glRotate(-angle2, 0., 1., 0.)
#        glRotate(-angle1, 1., 0., 0.)
#        glTranslatef(-ax1, -ax2, -ax3)
#    return wrapper

class Window3D(QOpenGLWidget):#todo заменить на QOpenGLWidget/ Уже?
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
        #self.substrate = 'fuck///examples/89.01.112.32.00.00.02_14273099_2735.tif'
        self.substrate = 'fuck///Drawing1.tif'
        self.alpha = 0.
        self.flag_draft = True
        #init_light()
        #lightGray = QColor(Qt.gray).light(180)

        print('start opengl')
        self.frame = frame
        self.setMinimumSize(100, 100)
        self.gcod = gcod
        self.setMouseTracking(True)
        init_vars(self)
        self.my_timer = QTimer()
        self.my_timer.timeout.connect(self.showTime)
        #self.my_timer_variable = QTimer()
        d3_interface(self)
        #change_draft(self, self.substrate)
        self.animation_flag = False
        self.frame_frequency = 100
        self.XYZABC_ADD = [0., 0., 0., 0., 0., 0.]#todo -180?????????????
        self.my_timer.start(self.frame_frequency)
        self.setAcceptDrops(True)

        self.draft_zero_vert = 0.0
        self.draft_zero_horiz = 0.0
        self.color = [[0., 0., 1.], [0., 1., 0.], [1., 0., 0.]]
        self.init_methods()



    def init_methods(self):
        self.A_table_function = A_table_function;   self.A_head_function = A_head_function
        self.B_head_function = B_head_function;     self.B_table_function = B_table_function
        self.C_table_function = C_table_function;   self.C_head_function = C_head_function
        self.last_head_move = last_head_move



    def dropEvent(self, e):
        print('dropEvent')
        print(type(e.mimeData().text()))
        print(e.mimeData().text())
        change_draft(self, e.mimeData().text())

    def dragEnterEvent(self, e):
        #if e.mimeData().hasText():
        e.accept()
        #self.draft_scale = self.scaling_draft_prime * self.k_rapprochement
        print('dragEnterEvent')

    def changeTexture(self, image, ix, iy):
        glBindTexture(GL_TEXTURE_2D, self.tex) # this is the texture we will manipulate
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)#тут какая то херня, вероятно todo
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        #print('ix = ', ix)
        glTexImage2D(GL_TEXTURE_2D, 0, self.gl_format, ix, iy, 0, self.gl_format, GL_UNSIGNED_BYTE, image) # load bitmap to texture
        #print('image is ', type(image))
        self.picratio = self.iy / self.ix

    #def draw_special_dot(self):
    #    if self.new_dot1 is None:
    #        return
    #    glLineWidth(30)
    #    glColor3f(0., 0.0, 0.0)
    #    glBegin(GL_LINES)
    #    center1 = self.new_dot1
    #    z = 1000
    #    l = 0.3 / self.k_rapprochement
    #    glVertex3f(-center1[0]+l, -center1[1]+l, z)
    #    glVertex3f(-center1[0]-l, -center1[1]-l, z)
    #    glVertex3f(-center1[0]-l, -center1[1]+l, z)
    #    glVertex3f(-center1[0]+l, -center1[1]-l, z)
    #    glEnd()
    #    if self.new_dot2 is None:
    #        return
    #    center2 = self.new_dot2
    #    glBegin(GL_LINES)
    #    glVertex3f(-center2[0]+l, -center2[1]+l, z)
    #    glVertex3f(-center2[0]-l, -center2[1]-l, z)
    #    glVertex3f(-center2[0]-l, -center2[1]+l, z)
    #    glVertex3f(-center2[0]+l, -center2[1]-l, z)
    #    glEnd()


    def resetTexture(self):
        if self.flag_draft is True:
            self.changeTexture(self.baseimage, self.ix, self.iy)

    def turn_to_turn_view(self):
        self.turn_angleX = 0.
        self.turn_angleY = 90.
        self.turn_angleZ = 90.

    def YX_view(self):
        print('YX_vew')
        self.turn_angleX = 0.
        self.turn_angleY = 0.
        self.turn_angleZ = 0.

    def ZY_view(self):
        print('ZY_vew')
        self.turn_angleX = -90.
        self.turn_angleY = 0.
        self.turn_angleZ = -90.

    def Centre_view(self):
        print('Centre_vew')
        self.draft_zero_horiz = self.draft_zero_horiz - self.cam_horizontal
        self.draft_zero_vert = self.draft_zero_vert - self.cam_height
        self.cam_horizontal = 0.
        self.cam_height = 0.

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:

        self.my_timer.start(100)
        b = a0.button()
        self.where_clicked_x = a0.x()
        self.where_clicked_y = a0.y()
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
                self.refresh()
            elif self.behavior_mode == 'choose distance':
                if self.new_dot1 is None:
                    right_border = self.cam_horizontal / self.w + 2. * (self.w / self.h)
                    x_display_coord = 2*right_border * (self.where_clicked_x-self.w/2)/self.w
                    y_display_coord = -2*self.height_settings * (self.where_clicked_y-self.h/2)/self.h
                    self.setCursor(QtGui.QCursor(Qt.CrossCursor))

                    self.new_dot1 = [(self.cam_horizontal - x_display_coord)/self.k_rapprochement, (self.cam_height - y_display_coord)/self.k_rapprochement]
                    self.render_text_preparation("RClick to choose \n last coordinat dot ", text_size=200, name_png='2st draft dot', k=0.35)
                elif self.new_dot2 is None:
                    self.setCursor(QtGui.QCursor(Qt.ArrowCursor))
                    right_border = self.cam_horizontal / self.w + 2. * (self.w / self.h)
                    x_display_coord = 2*right_border * (self.where_clicked_x-self.w/2)/self.w
                    y_display_coord = -2*self.height_settings * (self.where_clicked_y-self.h/2)/self.h
                    self.new_dot2 = [(self.cam_horizontal - x_display_coord)/self.k_rapprochement, (self.cam_height - y_display_coord)/self.k_rapprochement]
                    dlg = ChooseDistanceDialog(self)
                    dlg.exec()

    def refresh(self):
        self.behavior_mode = ''
        self.new_dot1 = None
        self.new_dot2 = None
        self.setCursor(QtGui.QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent) -> None:
        b = a0.button()
        if b == 1:
            self.m_grabbing = False
        elif b == 4:  # wheel button
            self.m_turning = False

    def mouseMoveEvent(self, a0: QtGui.QMouseEvent) -> None:
        new_horizo = a0.x()
        new_height = a0.y()
        if self.m_grabbing is True:
            horiz_mov = 4*(new_horizo - self.old_horizo_mouse) / self.h
            vert_mov = 4*(self.old_height_mouse - new_height) / self.h
            self.cam_horizontal = self.cam_horizontal + horiz_mov
            self.cam_height = self.cam_height + vert_mov
            angle = - (self.alpha * 2 * math.pi / 360)
            horiz_draft = horiz_mov * math.cos(angle) - vert_mov * math.sin(angle)
            vert_draft = vert_mov * math.cos(angle) + horiz_mov * math.sin(angle)
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
            else:
                #print('снаружи')
                angle_h = - 360 * (new_horizo - self.old_horizo_mouse) / self.h
                angle_v = - 360 * (self.old_height_mouse - new_height) / self.h

                if self.where_clicked_x > self.w/2:
                    angle_v = - angle_v
                if self.where_clicked_y > self.h/2:
                    angle_h = - angle_h

                self.turn_angleZ = self.turn_angleZ + angle_v + angle_h
                if self.turn_angleZ > 360. or self.turn_angleZ < 360:
                    self.turn_angleZ = self.turn_angleZ % 360.
                #self.cam_turn_z = self.cam_turn_z + (new_horizo - self.old_horizo_mouse) / self.h

        self.old_horizo_mouse = new_horizo
        self.old_height_mouse = new_height


    def wheelEvent(self, a0: QtGui.QWheelEvent) -> None:
        if a0.angleDelta().y() > 0:
            self.k_rapprochement = self.k_rapprochement / 0.8
            #что на середине экрана
            #print('+ k_rapprochement - = ', self.k_rapprochement)
            self.cam_height = self.cam_height / 0.8
            self.cam_horizontal = self.cam_horizontal / 0.8
            #сместить
            if self.flag_draft is True:
                self.draft_scale = self.draft_scale / 0.8
                self.draft_zero_horiz = self.draft_zero_horiz / 0.8
                self.draft_zero_vert = self.draft_zero_vert / 0.8
        else:
            self.k_rapprochement = self.k_rapprochement / 1.2
            self.cam_height = self.cam_height / 1.2
            self.cam_horizontal = self.cam_horizontal / 1.2
            if self.flag_draft is True:
                self.draft_scale = self.draft_scale / 1.2
                self.draft_zero_horiz = self.draft_zero_horiz / 1.2
                self.draft_zero_vert = self.draft_zero_vert / 1.2

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
        glMatrixMode(GL_MODELVIEW)
        #glLoadIdentity()
        self.k_rapprochement = self.k_rapprochement * self.h / self.old_h

        self.old_h  = self.h


    def resizeGL(self, w: int, h: int) -> None:
        glViewport(0, 0, w, h)
        k = self.k_rapprochement
        self.w = w
        self.h = h

        self.reshape(w, h)
        self.change_scale_in_resizeGL(self, k)


    @restore_zero_position_shell
    def change_scale_in_resizeGL(self, self_DRY, k):
        self.draft_scale = self.draft_scale * self.k_rapprochement / k

    def render_text_preparation(self, text, text_size, name_png, k=1.):
        if not os.path.exists(r'Settings\textTextures\{}.png'.format(name_png)):
            if not os.path.exists(r'Settings\textTextures'):
                os.makedirs(r'Settings\textTextures')
            lines_of_text = text.splitlines()
            N_lines = lines_of_text.__len__()
            h_of_one_line = int(text_size / N_lines)
            self.typing_height = 0.4 * N_lines
            len_l = 0
            for l in lines_of_text:
                a = l.__len__()
                if a > len_l:
                    len_l = a

            H, W = text_size, int(len_l * text_size * k)#* 0.35
            I = np.zeros((H, W, 4), dtype=np.ubyte)
            angle = 0
            array_L = [np.flip(make_label(textN, './Brave New Era G98.ttf', h_of_one_line, angle=angle), 0) for textN in lines_of_text]
            x0 = W // 2
            #y0 = H // 2
            x = int(x0)
            #y = int(y0)

            def color_text(a, b, c, d):
                def transparentcy(i, j):
                    I[i, j, 3] = 255 if I[i, j, 2] != 0 or I[i, j, 1] != 0 or I[i, j, 0] != 0 else 0
                I[a:b, c:d, 0] |= (L).astype('ubyte') #R
                #I[a:b, c:d, 1] |= (L).astype('ubyte') #G
                #I[a:b, c:d, 2] |= (L).astype('ubyte') #B
                [transparentcy(i, j) for i in range(a, b) for j in range(c, d)]

            start = 0
            line_gap = 5
            for L in array_L:
                h, w = L.shape
                # раскрашиваем
                color_text(start,
                           start + h,
                           x - w // 2,
                           x - w // 2 + w)

                start = start + h + line_gap
                nya = Image.fromarray(I[::1, ::1, ::1], mode='RGBA')
                nya.save(r'Settings\textTextures\{}.png'.format(name_png))
        else:
            im_frame = Image.open(r'Settings\textTextures\{}.png'.format(name_png))
            I = np.array(im_frame.getdata())
            print('I.shape = ', I.shape)
            #W, H, _ = big_array.shape
            W, H = im_frame.size

        self.glyph_tex = glGenTextures(1)

        #OpenGL
        glBindTexture(GL_TEXTURE_2D, self.glyph_tex)  # this is the texture we will manipulate
        # texture options
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, W, H, 0, GL_RGBA,
                     GL_UNSIGNED_BYTE, I)  # bitmap.buffer I


    def render_text(self):
        #initializGL
        if self.behavior_mode == '':
            return

        #dz = -1427
        # typing
        h = self.typing_height
        dz = 1000
        glColor3f(1., 1.0, 1.0)
        glBindTexture(GL_TEXTURE_2D, self.glyph_tex)  # this is the texture we will manipulate

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex3f(-1.5, 1.6, dz)
        glTexCoord2f(1.0, 0.0)
        glVertex3f(1.8, 1.6, dz)
        glTexCoord2f(1.0, 1.0)
        glVertex3f(1.8, 1.6 - h, dz)
        #glVertex3f(1.8, -2., dz)#
        glTexCoord2f(0.0, 1.0)
        glVertex3f(-1.5, 1.6 - h, dz)
        #glVertex3f(-1.5, -2., dz)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)

    #def light_on(self):
    #    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #    glEnable(GL_LIGHTING)
    #    #lightZeroPosition = [10., 4., 10., 1.]
    #    lightZeroColor = [1.0, 1.0, 1.0, 1.0]
    #    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    #    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    #    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    #    glEnable(GL_LIGHT0)

    def create_tool(self):  # todo вернуть try
        # try:
        print('first 1')
        # print(self.current_tool)
        self.tool_dict = read_tool_file(self.current_tool)
        choose_tool_function(self, self.tool_dict)
        self.tool_function(self, self.tool_dict)
        print('first 2')
        # except (FileNotFoundError, TypeError):
        #    #todo p_dict = создаю словарь
        #    print('second 1')
        #    self.tool_dict = {'TYPE': 'mills type1', 'OVERALL_L': 145, 'SORTIE': 100., 'TAIL_R': 8.0, 'TAIL_H': 35.0,
        #                     'CYLINDER1_R1': 20., 'CYLINDER1_R2': 20., 'CYLINDER1_H': 50., 'CYLINDER2_R1': 20.,
        #                     'CYLINDER2_R2': 10., 'CYLINDER2_H': 50., 'SPHERE_R': 10.,
        #                     'PIC': '\Modelling_clay\machine_tools\tool_pics\MILL1_scheme.png'}
        #
        #
        #    choose_tool_function(self, self.tool_dict)
        #    self.tool_function(self, self.tool_dict)
        #    print('second 2')
        # except:
        #    print('third 1')
        #    glEndList()
        #    self.tool_dict = {'TYPE': 'mills type1', 'OVERALL_L': 145, 'SORTIE': 100., 'TAIL_R': 8.0, 'TAIL_H': 35.0,
        #                     'CYLINDER1_R1': 20., 'CYLINDER1_R2': 20., 'CYLINDER1_H': 50., 'CYLINDER2_R1': 20.,
        #                     'CYLINDER2_R2': 10., 'CYLINDER2_H': 50., 'SPHERE_R': 10.,
        #                     'PIC': '\Modelling_clay\machine_tools\tool_pics\MILL1_scheme.png'}
        #    choose_tool_function(self, tool_dict)
        #    self.tool_function(self, tool_dict)
        #    print('third 2')

    def paintGL(self):

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnable(GL_POINT_SMOOTH)
        glPushMatrix()

        self.draft()

        #ddd
        glClearColor(*OpenGL_color_map_RGBA)
        glTranslatef(self.cam_horizontal, self.cam_height, 0.0)
        #z_t = False
        #if self.m_turning and  (self.where_clicked_x - self.w/2) ** 2 + (self.where_clicked_y - self.h/2) ** 2 < 0.1 * self.h * self.h:
        #    z_t = True
        #if z_t is True:
        #    glRotate(self.turn_angleZ, 0., 0., 1.)
        glRotate(self.turn_angleX, 1., 0., 0.)
        glRotate(self.turn_angleY, 0., 1., 0.)
        glRotate(self.turn_angleZ, 0, 0, 1.)
        glColor3f(1.5, 0.5, 0.5)
        #glPolygonMode(GL_FRONT, GL_FILL)



        glScale(self.k_rapprochement, self.k_rapprochement, self.k_rapprochement)
        #self.green_cub_lines()
        self.view_SC_dot()
        #todo в этой же точке рисуем СК обработки. НЕТ! Может и в другой если качаем. при старте совпадают
        # Размер не зависит от k_rapprochement
        # Направление осей зависит от
        # 1 осей станка
        # 2 TRAORI и тд
        #self.cub(0.5)
        # todo here we will make bind dot
        # это перенос конкретной координаты кончика инструмента в ОСК TODO

        self.green_cub_lines()#TODO ВОТ отсюда нужно строить ВСЁ ЗАНОВО
        #ФФФФ

        self.draw_machine()#todo внести перенос в точку и вынести после
        #zdes uje ne te coords base
        self.transmigration_func()#no real transfers

        self.draw_points(self.gcod)
        self.error_lines_draw()
        self.draw_lines(self.gcod)
        #self.draw_special_dot()
        glFlush()
        glPopMatrix()
        self.render_text()


    def green_cub_lines(self):
        glLineWidth(2)
        glColor3f(0.2, 1, 0.2)
        glBegin(GL_LINE_STRIP)
        glVertex3f(0, 0, 0)
        glVertex3f(100, 0, 0)
        glVertex3f(100, 100, 1)
        glVertex3f(100, 100, 100)
        glVertex3f(0, 100, 100)
        glVertex3f(0, 0, 100)
        glEnd()

    def error_lines_draw(self):
        glLineWidth(3)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        for nya in self.ERROR_lines:
            glVertex3f(nya[17], nya[18], nya[19])
            #special_pont_options(*nya[17:20])
            #special_pont_options(nya[17:20])
        glEnd()

    def transmigration_func(self):
        """
        only solving, no rel transfers
        :return:
        """

        x, y, z = self.tip_way_func(self)
        #zdes podumat
        dx, dy, dz = self.DICT_G549shift[self.g54_g59_default]
        for f_l in self.after_draw_return_list:
            x, y, z = f_l[0](f_l[1], x, y, z)
        param_list = [dx, dy, dz, 0, 0, 0, -self.main_G549['A'], -self.main_G549['B'], -self.main_G549['C']]

        x, y, z = TR_ABC(param_list, x, y, z)#todo ТАк нельзя. Вращать нужно не вокруг новых осей, а вокруг базовых?
        #todo сменить в паре - здесь может и не надо
        #x, y, z = -x, -y, -z
        glColor3f(1, 0, 0.5)#dot at the tool tip
        glPointSize(7)
        glBegin(GL_POINTS)
        glVertex3f(x, y, z)#in main coords
        glEnd()

    def draw_machine(self):
        #сейчас мы находимся в первоначальном нуле G549
        #self.view_SC_machining()
        color = [[0., 0., 1.], [0., 1., 0.], [1., 0., 0.]]
        glColor3f(*color[0])
        #TODO the problem here - if order different, than a new function might be necessary SIC!!!

        #Во первых сначала рисуем СК рисования детали - выполнено выше.
        #Во вторых потом поворачиваем.

        #my_list_f = self.machine_start_configuration  # todo для обычного режима
        ##my_list_f = self.machine_draw_list #todo для TRAORI

        #todo где то поворот, но позже его добавлю

        #print(f'd_x, d_y, d_z = {d_x, d_y, d_z}')

        glRotate(-self.main_G549['C'], 0., 0., 1.)
        glRotate(-self.main_G549['B'], 0., 1., 0.)
        glRotate(-self.main_G549['A'], 1., 0., 0.)


        #print('DICT_G549shift default = ', self.g54_g59_default)
        #print('self.DICT_G549shift = ', self.DICT_G549shift)
        #glTranslatef(*[-m for m in self.m_zero_to_m_1ax_center_CONST])
        #self.test_point()
        #glTranslatef(*self.m_zero_to_m_1ax_center_CONST)
        #self.test_point()



        d_x, d_y, d_z = self.DICT_G549shift[self.g54_g59_default]  # Функция уже выполнена! Здесь мы только смотрим результат
        #Результат смещения
        #TODO или назад отскочить можно?

        glTranslatef(d_x, d_y, d_z)#перешёл из СК базовой к машинному нулю/ Нет, переходит к центру стола

        #glTranslatef(0, 800, 0)

        #glTranslatef(0, -800, 0)
        #glTranslatef(*self.m_zero_to_m_1ax_center_CONST)



        #Дальше нужно нарисовать другие нули: т смены инструмента и точка крпления головы так как они от машиинного нуля

        #glCallList(self.special_machine_points['M0_CONST'])


        #glTranslatef(self.offset_pointXYZ[0], self.offset_pointXYZ[1], self.offset_pointXYZ[2])
        #glCallList(self.special_machine_points['M0_VARIANT'])#можно и без этого
        #Теперь нужно нащупать центры вращения стола от детали к станку
        #переместиться на offset_pointXYZ от стола к голове
        #от крепления головы к её последнему элементу, всё это ниже:
        #self.test_point()
        #self.machine_zeros_draw(i=i)
        i = 0
        for list_ in self.machine_draw_list:
            if i == self.Table_Head_place:
                #self.machine_zeros_draw(i=i)
                glTranslatef(*self.m_zero_to_m_1ax_center_CONST)
                glCallList(self.special_machine_points['M0_CONST'])
                glCallList(self.special_machine_points['TOOL_POINT1'])
                glCallList(self.special_machine_points['TOOL_POINT2'])
                #glCallList(self.special_machine_points['M0_VARIANT'])
                self.view_SC_machining()
                glTranslatef(*[-coord for coord in self.m_zero_to_m_1ax_center_CONST])

            params = list_[6]
            list_[0](list_[2], list_[3], list_[4], list_[5], params)
            i += 1

        self.collet_draw()
        #return
        #теперь назад
        for list_ in self.after_draw_return_list:
            params = list_[1]
            list_[2](params)

        #glTranslatef(*[-m for m in self.m_zero_to_m_1ax_center_CONST])
        glTranslatef(-d_x, -d_y, -d_z)
        glRotate(self.main_G549['A'], 1., 0., 0.)
        glRotate(self.main_G549['B'], 0., 1., 0.)
        glRotate(self.main_G549['C'], 0., 0., 1.)

        #вернулся к нулю к G549 default


    def test_point(self):
        hor, vert = 0, 0
        glPointSize(50)
        glBegin(GL_POINTS)
        glColor3f(0.5, 1., 0.5)
        glVertex3f(hor, vert, 0.0)
        glEnd()

    def collet_draw(self):
        glCallList(self.my_collet)
        # self.tool_dict
        deep = self.tool_dict['OVERALL_L'] - self.tool_dict['SORTIE']
        #todo учесть вылет
        glTranslatef(0, 0, -deep)
        glCallList(self.my_tool)#откатилось назад
        glTranslatef(0, 0, deep)
        glTranslatef(0., 0., -self.collet['h'])  # todo сдвиг
        glRotate(self.collet['angle'], 1, 0., 0.)#-angl убрал
        #glTranslatef(0., self.collet['L_from_segment_tip'], 0)


    def machine_model_parts(self):
        ASSEMBLE_MACHINE(self)#todo здесь создаётся g54_g59_AXIS_Display =  {'G54': [100.0, -200.0, 1450.0, 0.0, 0, 0, True],...
        print('after assemble g54_g59_AXIS_Display = ', self.g54_g59_AXIS_Display)#заполнять тру фолсе как
        self.SC_s_dict = prepare_SC_s_texture(self.g54_g59_AXIS, self.g54_g59_default)
        print('G549 dict = ', self.g54_g59_AXIS)



    def bind_Texture(self, image_arr, ix, iy):
        #print('image_arr = ', image_arr)
        #time.sleep(1)# todo не работет пауза
        print('type of self.machine_tex_green: ', type(self.machine_tex_green))
        glBindTexture(GL_TEXTURE_2D, self.machine_tex_green)   # this is the texture we will manipulate
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        print('image_arr = ', image_arr[0])
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_arr) # load bitmap to texture

    #@new_position_object_shell

    # draft1
    def draft(self):
        if self.flag_draft is False:
            return
        #a = 'white'
        a = 'nope'
        if a == 'white':
            glColor3f(1,1,1)
        else:
            glColor4f(*OpenGL_color_map_RGBA)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Clear The Screen And The Depth Buffer
        glLoadIdentity()    # Reset The View
        glBindTexture(GL_TEXTURE_2D, self.tex)# this is the texture we will manipulate
        glEnable(GL_TEXTURE_2D)

        glRotate(self.alpha, 0., 0., 1.)
        dz = -1427
        r = self.ratio / self.picratio# screen h/w  // picture h/w
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

        #draft center
        #glPointSize(30)
        #glBegin(GL_POINTS)
        #glColor3f(0.5, 0.5, 0.5)
        #glVertex3f(hor, vert, 0.0)
        #glColor3f(0.2, 0.5, 0.5)
        #glEnd()

        glRotate(-self.alpha, 0., 0., 1.)
        glDisable(GL_TEXTURE_2D)



    def view_SC_dot(self):
        glPointSize(10)
        glBegin(GL_POINTS)
        glColor3f(1.5, 0.5, 0.5)
        glVertex3f(0.0, 0.0, 0.0)
        glEnd()
        glCallList(self.special_machine_points['PART_SC'])

    def view_SC_machining(self):
        #x, y, z, show = self.g54_g59_AXIS_Display[self.g54_g59_default]
        #my_list_f = self.machine_start_configuration#todo для обычного режима
        #my_list_f = self.machine_draw_list #todo для TRAORI
        #glTranslatef(x, y, z)
        #todo Поворот

        Display = self.g54_g59_AXIS_Display
        #print('Display = ', Display)
        for sc in Display:
            if Display[sc][6]:
                self.show_SC(Display[sc], sc)
        #Display = self.cycle800_AXIS_Display
        #for sc in Display:
        #    try:
        #        print('try show cycle800')
        #        self.show_SC(Display[sc], sc)
        #        print('cycle800 show success')
        #    except:
        #        pass


    def show_SC(self, sc, sc_key):
        glTranslatef(sc[0], sc[1], sc[2])
        glRotate(sc[3], 1, 0, 0)#A
        glRotate(sc[4], 0, 1, 0)#B
        glRotate(sc[5], 0, 0, 1)#C

        glScale(1/self.k_rapprochement, 1/self.k_rapprochement, 1/self.k_rapprochement)
        glCallList(self.special_machine_points['MACHINING_SC'])
        #print(f'sc = {sc}')
        glScale(self.k_rapprochement, self.k_rapprochement, self.k_rapprochement)
        for polarSC in sc[7]:
            #glRotate(sc[3], 1, 0, 0)polarSC[1]
            #вот тут чинить отображение
            glTranslatef(polarSC[0][0], polarSC[0][1], polarSC[0][2])
            glRotate(-90, polarSC[1][0], polarSC[1][1], polarSC[1][2])
            glCallList(self.special_machine_points['POLAR_SC'])
            glRotate(90, polarSC[1][0], polarSC[1][1], polarSC[1][2])
            glTranslatef(-polarSC[0][0], -polarSC[0][1], -polarSC[0][2])
        for smallSC in sc[8]:#CYCLE800 SC
            glTranslatef(*smallSC[1])
            order_rotation(smallSC[0], smallSC[2][0], smallSC[2][1], smallSC[2][2])
            glTranslatef(*smallSC[3])
            glCallList(self.special_machine_points['SMALL_SC'])
            glTranslatef(-smallSC[3][0], -smallSC[3][1], -smallSC[3][2])
            order_rotation(smallSC[0][-1::-1], -smallSC[2][0], -smallSC[2][1], -smallSC[2][2])
            glTranslatef(-smallSC[1][0], -smallSC[1][1], -smallSC[1][2])
        glCallList(self.SC_s_dict[sc_key])
        glRotate(-sc[5], 0, 0, 1)#C
        glRotate(-sc[4], 0, 1, 0)#B
        glRotate(-sc[3], 1, 0, 0)#A
        glTranslatef(-sc[0], -sc[1], -sc[2])




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
        #glPopMatrix()


            #take_machine_sizes(machine_item, )

    def initializeGL(self):
        #self.
        #glClear()

        # draft1
        buf = GLint()
        glGetIntegerv(GL_MAX_TEXTURE_SIZE, byref(buf))
        self.max_texture_video_card = buf.value
        resize_texture(self, self.substrate)
        self.tex = glGenTextures(1)
        self.machine_tex_green = glGenTextures(1)
        self.machine_model_parts()
        print('glGenTextures(2) = ', self.machine_tex_green)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)

        glLoadIdentity()
        self.resetTexture()


    def draw_points(self, np_list):
        adding_dots = self.show_intermediate_dots
        glPointSize(4)
        glEnable(GL_VERTEX_PROGRAM_POINT_SIZE)
        glPushMatrix()
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_POINTS)
        if adding_dots:
            for i in np_list:
                if np.isnan(i[16]):
                    glVertex3f(i[17], i[18], i[19])
                elif i[16] == 5 or i[16] == 7:
                    glVertex3f(i[17], i[18], i[19])
        else:
            for i in np_list:
                if np.isnan(i[16]):
                    glVertex3f(i[17], i[18], i[19])
                elif i[16] == 7:
                    glVertex3f(i[17], i[18], i[19])
        glEnd()

        self.choose_dot()
        glPopMatrix()



    def draw_lines(self, np_list):
        glLineWidth(2)
        glDisable(GL_LINE_SMOOTH)
        glColor3f(*OpenGL_color_G0_line)
        glBegin(GL_LINE_STRIP)
        g0_g1 = 0
        #print('||||||||||||||||||||||||||||||||1')
        #print('np_list = ', np_list[:, 16:20])
        #print('||||||||||||||||||||||||||||||||2')
        #G0X0.Z0.
        #G2 X100.Z - 50. R50.
        #неверный знак и вылет после. потом ось С допилить
        for i in np_list:
            if g0_g1 != i[3]:
                if i[3] == 0:
                    glColor3f(*OpenGL_color_G0_line)
                else:
                    glColor3f(*OpenGL_color_G1_line)
                g0_g1 = i[3]
            if np.isnan(i[16]):
                glVertex3f(i[17], i[18], i[19])
            else:
                special_pont_options(i[16], i[17], i[18], i[19])# intermediate dots for example
        glEnd()



    def choose_dot(self):

        #beginMy = False
        try:#k_rapprochement
            #self.current_dot_Mark
            #may be a dot will be enough
            dot = self.gcod[self.current_dot_Mark]
            glColor3f(0.8, 0.3, 0.8)
            delta = 0.08 / self.k_rapprochement  #перекрестье
            glLineWidth(1)
            glBegin(GL_LINE_LOOP)
            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] + delta)
            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] - delta)
            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] - delta)
            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] - delta)
            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] + delta)
            glEnd()
            glBegin(GL_LINE_LOOP)
            glVertex3f(dot[17] - delta, dot[18] + delta, dot[19] + delta)
            glVertex3f(dot[17] - delta, dot[18] + delta, dot[19] - delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] - delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] - delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] + delta)
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] + delta)
            glVertex3f(dot[17] - delta, dot[18] + delta, dot[19] + delta)

            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] - delta)
            glVertex3f(dot[17] - delta, dot[18] + delta, dot[19] - delta)

            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] - delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] - delta)

            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] + delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] + delta)

            #cross
            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] + delta)
            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] - delta)

            glVertex3f(dot[17] - delta, dot[18] - delta, dot[19] + delta)
            glVertex3f(dot[17] + delta, dot[18] + delta, dot[19] - delta)

            glVertex3f(dot[17] + delta, dot[18] - delta, dot[19] + delta)
            glVertex3f(dot[17] - delta, dot[18] + delta, dot[19] - delta)
            glEnd()

            glLineWidth(5)
            glBegin(GL_LINE_STRIP)
            #beginMy = True
            #current_move_start = self.frame_address_in_visible_pool[0]
            for i in range(self.previous_dot_Mark, self.current_dot_Mark+1):
                if not np.isnan(self.gcod[i][17]):
                    glVertex3f(self.gcod[i][17], self.gcod[i][18], self.gcod[i][19])
            glEnd()


        except:
            #if beginMy:
            #    glEnd()
            pass



def special_pont_options(i, i1, i2, i3):
    if i == 0:
        glVertex3f(i1, i2, i3)
    elif i == 5:
        glVertex3f(i1, i2, i3)
    elif i == 7:
        glVertex3f(i1, i2, i3)


