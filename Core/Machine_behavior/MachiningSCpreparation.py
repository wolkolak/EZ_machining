


def give_G549_shift(self, my_list_f):
    #my_list_f = self.machine_start_configuration  # todo для обычного режима
    # my_list_f = self.machine_draw_list #todo для TRAORI
    x, y, z = 0., 0., 0.
    print('self.machine_draw_list len= ', len(self.machine_draw_list))
    print('self.Table_Head_place  = ', self.Table_Head_place)

    for u in range(0, self.Table_Head_place):  # чтобы можно было качать
        print('self.machine_draw_list[u] = ', self.machine_draw_list[u])
        params = [-ff for ff in my_list_f[u][6]]
        x, y, z = self.machine_draw_list[u][8](params, x, y, z)
    print('x, y, z  = ', x, y, z )
    # self.XYZABC_ADD не надо?
    from_Machine_to_G549_X = self.m_zero_to_m_1ax_center_CONST[0] + self.offset_pointXYZ[0] + self.main_G549['X']
    from_Machine_to_G549_Y = self.m_zero_to_m_1ax_center_CONST[1] + self.offset_pointXYZ[1] + self.main_G549['Y']
    from_Machine_to_G549_Z = self.m_zero_to_m_1ax_center_CONST[2] + self.offset_pointXYZ[2] + self.main_G549['Z']

    d_x = x - from_Machine_to_G549_X
    d_y = y - from_Machine_to_G549_Y
    d_z = z - from_Machine_to_G549_Z
    print('dx, dy, dz  = ', d_x, d_y, d_z)
    return d_x, d_y, d_z#+550


def give_G549_shifts(self, machine_item):#Для draw работает прекрасно.

    dict_G549 = {}#todo Нужны и другие G549
    my_list_f_default = self.machine_start_configuration
    #Выяснение где лежит начальная G549
    dict_G549[machine_item.current_g54_g59] = give_G549_shift(self, my_list_f_default)
    print('dict_G549 = ', dict_G549)

    return dict_G549