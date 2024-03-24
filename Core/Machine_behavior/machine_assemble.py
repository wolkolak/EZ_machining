
from OpenGL.GL import *
from PyQt5 import QtGui
from Core.Machine_behavior.assemble_machine_functions import assemble_functions_to_draw_machine
from OpenGL.GL import *
from OpenGL.GLU import *
from  Core.Machine_behavior.Standart_machine_parts import make_romb


def create_collet(self):
    collet = glGenLists(1)
    glNewList(collet, GL_COMPILE)
    my_cylinder = gluNewQuadric()
    #glLineWidth(111)
    glColor3f(0.75, 0.75, 0.75)
    #glTranslatef(0., -self.collet['L_from_segment_tip'], 0)  # todo сдвиг
    glRotate(self.collet['angle'], 1, 0., 0.)  # todo поворот
    gluDisk(my_cylinder, 0., self.collet['baseR'], self.collet['polygons_r'], 5)
    gluCylinder(my_cylinder, self.collet['baseR'], self.collet['topR'], self.collet['h'], self.collet['polygons_r'],
                self.collet['polygons_h'])
    glColor3f(0.3, 0.3, 0.3)

    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(self.collet['baseR']+2, 0, 0)
    glVertex3f(self.collet['topR']+2, 0, self.collet['h'])
    glEnd()


    gluDisk(my_cylinder, self.collet['baseR'], self.collet['baseR'] + 2, self.collet['polygons_r'], 5)
    gluCylinder(my_cylinder, self.collet['baseR']+2, self.collet['baseR']+2, 2, self.collet['polygons_r'], self.collet['polygons_h'])

    glTranslatef(0., 0., self.collet['h'])  # todo сдвиг
    gluDisk(my_cylinder, self.collet['baseR'], self.collet['topR'] + 2, self.collet['polygons_r'], 5)
    gluCylinder(my_cylinder, self.collet['topR']+2, self.collet['topR']+2, 2, self.collet['polygons_r'], self.collet['polygons_h'])
    glColor3f(0.75, 0.75, 0.75)
    gluDisk(my_cylinder, 0., self.collet['topR'], self.collet['polygons_r'], 5)

    glEndList()
    self.my_collet = collet


def init_machine_settings(self):
    print('init_machine_settings')
    if self.frame.left_tab.parent.central_widget.note.currentIndex() == -1:
        machine_item = self.frame.left_tab.parent.central_widget.note.default_machine_item  # ??????????????????
    else:
        machine_item = self.frame.left_tab.parent.central_widget.note.currentWidget().current_machine
    print('machine_item.current_g54_g59 = ', machine_item.current_g54_g59)
    self.g54_g59_default = machine_item.current_g54_g59
    self.main_G549 = machine_item.g54_g59_AXIS[machine_item.current_g54_g59]
    print('self.main_G549 = ', self.main_G549)
    self.for_45grad_angles = machine_item.for_45grad_angles
    self.animation_line_ax_order = machine_item.animation_line_ax_order
    self.XYZABC_ADD = machine_item.XYZABC_ADD
    self.BASE_XYZABC = self.XYZABC_ADD.copy()
    print('machine_item = ', machine_item)
    self.offset_pointXYZ = machine_item.offset_pointXYZ
    self.change_TOOL_point1 = machine_item.change_TOOL_point1
    self.change_TOOL_point2 = machine_item.change_TOOL_point2

    #self.offset_pointXYZ = machine_item.offset_pointXYZ
    self.min_table_head_distance = machine_item.min_table_head_distance

    # просуммировать с G549???!!!
    print('self.XYZABC_ADD =', self.XYZABC_ADD)
    print('self.main_G549 = ', self.main_G549)

    #for a1, a2 in zip(range(0, 6), 'XYZABC'): self.XYZABC_ADD[a1] += self.main_G549[a2]  # Здесь прибавка
    #todo сдвинуть и повернуть вокруг геометрических осей



    # место проблемы

    #print('2 self.XYZABC_ADD =', self.XYZABC_ADD)
    # print('g549 = ', self.main_G549)
    self.m_zero_to_m_1ax_center_CONST = machine_item.m_zero_to_m_1ax_center_CONST
    self.ax_order = machine_item.ax_order
    self.table, self.head = machine_item.give_parts_to_scene()
    # print('table = ', self.table)
    # print('head = ', self.head)
    self.max_table_head_distance = machine_item.max_table_head_distance

    self.collet = machine_item.collet
    print('self.table in scene ', self.table)



def ASSEMBLE_MACHINE(self):
    init_machine_settings(self)
    create_collet(self)
    self.create_tool()




    glColor4f(1., 1.0, 1.0, 255)
    im = QtGui.QImage(r'Settings\machineTextures\machine_green.png')
    ix = im.width()
    iy = im.height()
    im = im.smoothScaled(ix, iy)
    # im = im.convertToFormat(QtGui.QImage.Format_RGB888)
    im = im.convertToFormat(QtGui.QImage.Format_RGBA64)
    ptr = im.scanLine(0)
    ptr.setsize(im.sizeInBytes())
    image_array = ptr.asstring()

    # make textures
    self.machine_tex_green = glGenTextures(1)
    print('almost all things done1')
    print('AAA self.table = ', self.table)
    # self.XYZABC_ADD = []

    for i in range(len(self.table)):
        if self.table[i][0] is not None:
            print('self.table[i] = ', self.table[i])
            l = self.table[i][0]
            j_angl = self.table[i][1]
            t_angl = self.table[i][2]
            L_order = self.table[i][3]#ТУ Т пролбема

            self.table[i] = [make_romb(self, l, l / 3, 10, image_array, ix, iy), l, j_angl, t_angl, L_order]  # [ h, r1, r2, n_angles], length, angle
            print('|| self.table[i] = ', self.table[i])

    for i in range(len(self.head)):
        if self.head[i][0] is not None:
            print('self.head[i] = ', self.head[i])
            l = self.head[i][0]
            j_angl = self.head[i][1]
            t_angl = self.head[i][2]
            L_order = self.head[i][3]
            self.head[i] = [make_romb(self, l, l / 3, 10, image_array, ix, iy), l, j_angl, t_angl, L_order]
    print('self.head AAAAA: ', self.head)

    # draw_and_return_list
    self.machine_draw_list = []
    self.after_draw_return_list = []
    # self.func_list, self.func_list_return = assemble_functions_to_draw_machine(self)
    assemble_functions_to_draw_machine(self)

    # x, y, z = self.max_table_head_distance
    # print('||x = ', x)
    # self.X_balk , self.Y_balk, self.Z_balk = create_connection(x, y, z, self)#, order='XYZ'
    print('BBB self.table = ', self.table)
    print('EEE self.head = ', self.head)

    # self.XYZABC_ADD