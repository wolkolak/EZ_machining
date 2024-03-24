from OpenGL.GL import *
from Core.Machine_behavior.Standart_machine_parts import createXbalk, createYbalk, createZbalk
from Core.Machine_behavior.SC_machine_parts import create_M0_CONST, create_M0_VARIANT, create_TOOL_change_point1, create_TOOL_change_point2



def aliquot_90_degrees(degrees_list):
    first = degrees_list[0] % 90
    second = degrees_list[1] % 90
    third = degrees_list[2] % 90
    if first == second == third == 0:
        return True
    else:
        return False

def create_connection(x, y, z, self, form_type='f+f'):#, order='XYZ'
    gauge = 10
    print('create_connection(x, y, z)')
    # form_type='frame'  form_type='filled'  form_type='f+f'  form_type='nothing'

    how1 = self.animation_line_ax_order[0]
    glEnable(GL_LINE_SMOOTH)
    zero = 0
    #form_type = 'frame'



    X_balk = createXbalk(x, zero, gauge, self.min_table_head_distance[0], how1, form_type=form_type)
    Y_balk = createYbalk(y, zero, gauge, self.min_table_head_distance[1], how1, form_type=form_type)
    Z_balk = createZbalk(z, zero, gauge, self.min_table_head_distance[2], how1, form_type=form_type)
    glDisable(GL_LINE_SMOOTH)

    #GGG = create_M0_CONST(self)

    return X_balk, Y_balk, Z_balk#, AfterZ


def A_table_function(self, dy, i):  # A
    glColor3f(*self.color[0])
    delta_a = self.XYZABC_ADD[3]
    delta_a = delta_a - (delta_a // 360) * 360
    #da_add, db_add, dc_add = lever_turn_helper_new('Table', self.table[i][2], delta_a)
    da_add, db_add, dc_add = 0., 0., 0.
    da =  da_add#self.const_a[0] +
    db =  db_add#self.const_a[1] +
    dc =  dc_add#self.const_a[2] +
    tier_c = self.XYZABC_ADD[3]
    #self.angles_list.append([da, db, dc])
    #table_movement1 = transfer_rotate_draw_table(self.table[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)
    return [da, db, dc], tier_c


def B_table_function(self, dy, i):  # B
    glColor3f(*self.color[2])
    delta_b = self.XYZABC_ADD[4]
    delta_b = delta_b - (delta_b // 360) * 360
    print('self.table[i] = ', self.table[i][2])
    #da_add, db_add, dc_add = lever_turn_helper_new('Table', self.table[i][2], delta_b)
    da_add, db_add, dc_add = 0., 0.,0.

    da = da_add#self.const_b[0] +
    db = db_add#self.const_b[1] +
    dc = dc_add#self.const_b[2] +
    tier_c = self.XYZABC_ADD[4]
    #self.angles_list.append([da, db, dc])
    #table_movement2 = transfer_rotate_draw_table(self.table[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)
    return [da, db, dc], tier_c


def C_table_function(self, dy, i):  # C
    #i определяет где в table лежит соответствующее звено
    #dy = dy_tab_prev. это длина элемента.
    #print('dy = ', dy)
    glColor3f(*self.color[1])

    delta_c = self.XYZABC_ADD[5]
    #print('C_table_function = ', delta_c)
    delta_c = delta_c - (delta_c // 360) * 360
    #da_add, db_add, dc_add = lever_turn_helper_new('Table', self.table[i][2], delta_c)
    da_add, db_add, dc_add = 0., 0., 0.
    da =  da_add#self.const_c[0] +
    db =  db_add#self.const_c[1] +
    dc =  dc_add#self.const_c[2] +
    tier_c = self.XYZABC_ADD[5]
    #self.angles_list.append([da, db, dc])
    #table_movement3 = transfer_rotate_draw_table(self.table[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)#None

    return [da, db, dc], tier_c


def A_head_function(self, dy, i):  # A
    glColor3f(*self.color[0])
    delta_a = self.XYZABC_ADD[3]
    delta_a = delta_a - (delta_a // 360) * 360
    #da_add, db_add, dc_add = lever_turn_helper_new('Head', self.head[i][2], delta_a)
    da_add, db_add, dc_add = 0., 0., 0.
    da =  da_add#self.const_a[0] +
    db =  db_add#self.const_a[1] +
    dc =  dc_add#self.const_a[2] +
    tier_c = self.XYZABC_ADD[3]
    #self.angles_list.append([da, db, dc])
    #head_movement1 = transfer_rotate_draw_head(self.head[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)
    #return head_movement1
    return [da, db, dc], tier_c




def B_head_function(self, dy, i):  # B
    glColor3f(*self.color[2])
    delta_b = self.XYZABC_ADD[4]
    delta_b = delta_b - (delta_b // 360) * 360
    #da_add, dc_add, db_add
    print('b head je')
    #da_add, db_add, dc_add = lever_turn_helper_new('Head', self.head[i][2], delta_b)#todo ВСЕ поменять????
    da_add, db_add, dc_add = 0., 0., 0.
    print('da_add = {}, db_add = {}, dc_add = {}'.format(da_add, db_add, dc_add))
    #da_add = da_add / 2
    da =  da_add#self.const_b[0] +
    db =  db_add#self.const_b[1] +
    dc =  dc_add#self.const_b[2] +
    #self.angles_list.append([da, db, dc])
    #head_movement2 = transfer_rotate_draw_head(self.head[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)
    #return head_movement2
    tier_c = self.XYZABC_ADD[4]#не оттуда сцк?
    print('+++++++++++++tier_c = ', tier_c)
    return [da, db, dc], tier_c


def C_head_function(self, dy, i):  # C todo все эти функции бесполезное говно наверное
    glColor3f(*self.color[1])
    delta_c = self.XYZABC_ADD[5]
    delta_c = delta_c - (delta_c // 360) * 360
    #da_add, db_add, dc_add = lever_turn_helper_new('Head', self.head[i][2], delta_c)
    da_add, db_add, dc_add = 0., 0., 0.
    da = da_add#self.const_b[0] +
    db = db_add#self.const_b[1] +
    dc = dc_add#self.const_b[2] +
    #self.angles_list.append([da, db, dc])
    #head_movement3 = transfer_rotate_draw_head(self.head[i][0], dx=0., dy=dy, dz=0., da=da, db=db, dc=dc)
    #return head_movement3
    tier_c = self.XYZABC_ADD[5]
    return [da, db, dc], tier_c




def last_head_move(self, dy, i):#todo Тут тчо то менять тоже
    da = 0.;    db = 0.;    dc = 0.
    dx = 0;    dz = 0.
    #self.angles_list.append([da, db, dc])
    # print('dy == ', dy)
    glTranslatef(dx, dy, dz)
    movement = [dx, dy, dz, da, db, dc]
    movement = [m * (-1) for m in movement]
    return movement



def lever_turn_helper_new(ax, angl, delta):
    #вообще не надо
    #тут  дрянь
    if ax == 'Table':
        if angl == 0.:
            print('|||111')
            main1 = delta #/ 2
            main2 = 0.
            #return main2, main2, main1
        else:#45 grad
            print('|||222')
            main1 = 0.
            main2 = 0#delta #/ 2
    elif ax == 'Head':
        if angl == 0.:
            print('|||333')
            main1 = -delta #/ 2
            main2 = 0.
            #return main2, main2, main1
        else:#45 grad
            print('|||444')
            main1 = 0.
            main2 = 0#delta #/ 2
    return main2, main2, main1


def draw_machine_zero_pont_CONST(self):
    glTranslatef(self.m_zero_to_m_1ax_center_CONST[0], self.m_zero_to_m_1ax_center_CONST[1], self.m_zero_to_m_1ax_center_CONST[2])
    #print('dfgdfgdfg')
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(1.5, 1.5, 1.5)
    glVertex3f(0.0, 0.0, 0.0)
    glColor3f(0., 0.5, 0.5)
    glEnd()
    glTranslatef(-self.m_zero_to_m_1ax_center_CONST[0], -self.m_zero_to_m_1ax_center_CONST[1], -self.m_zero_to_m_1ax_center_CONST[2])


def draw_machine_zero_pont_vatiant(self):
    glTranslatef(self.offset_pointXYZ[0], self.offset_pointXYZ[1], self.offset_pointXYZ[2])
    #print('dfgdfgdfg')
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(1.5, 1.5, 1.5)
    glVertex3f(0.0, 0.0, 0.0)
    glColor3f(0., 0.5, 0.5)
    glEnd()
    glTranslatef(-self.offset_pointXYZ[0], -self.offset_pointXYZ[1], -self.offset_pointXYZ[2])

def draw_machine_TOOL_pont_change1(self):
    glTranslatef(self.offset_pointXYZ[0], self.offset_pointXYZ[1], self.offset_pointXYZ[2])
    #print('dfgdfgdfg')
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(1.5, 1.5, 1.5)
    glVertex3f(0.0, 0.0, 0.0)
    glColor3f(0., 0.5, 0.5)
    glEnd()
    glTranslatef(-self.offset_pointXYZ[0], -self.offset_pointXYZ[1], -self.offset_pointXYZ[2])

def draw_machine_TOOL_pont_change2(self):
    glTranslatef(self.offset_pointXYZ[0], self.offset_pointXYZ[1], self.offset_pointXYZ[2])
    #print('dfgdfgdfg')
    glPointSize(20)
    glBegin(GL_POINTS)
    glColor3f(1.5, 1.5, 1.5)
    glVertex3f(0.0, 0.0, 0.0)
    glColor3f(0., 0.5, 0.5)
    glEnd()
    glTranslatef(-self.offset_pointXYZ[0], -self.offset_pointXYZ[1], -self.offset_pointXYZ[2])