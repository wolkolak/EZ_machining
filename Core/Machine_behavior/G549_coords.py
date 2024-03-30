
from Core.Machine_behavior.machine_transmigrations_forward import RT_ABC, TR_ABC
from Core.Machine_behavior.machine_transmigrations_return import return_TR_CBA, return_RT_CBA

#g54_g59_AXIS_Display
def Display_G549_places(self):
    print('displayyyyyyyyyyyyyyyyyy')
    #base_off = [self.m_zero_to_m_1ax_center_CONST[0] + self.offset_pointXYZ[0],
    #            self.m_zero_to_m_1ax_center_CONST[1] + self.offset_pointXYZ[1],
    #            self.m_zero_to_m_1ax_center_CONST[2] + self.offset_pointXYZ[2]]
    g54_g59_AXIS_Display = {}
    for ii in range(54, 60):
        ii_s = str(ii)
        key_ = 'G' + ii_s
        #g54_59 = data from machine_settings, g54_59
        x = self.g54_g59_AXIS[key_]['X']#+base_off[0] +
        y = self.g54_g59_AXIS[key_]['Y']#+base_off[1] +
        z = self.g54_g59_AXIS[key_]['Z']#+base_off[2] +
        g54_g59_AXIS_Display['G' + ii_s] = [x, y, z, self.g54_g59_AXIS[key_]['A'], self.g54_g59_AXIS[key_]['B'], self.g54_g59_AXIS[key_]['C'], False, [], []]
    g54_g59_AXIS_Display[self.g54_g59_default][6] = True

    g54_g59_AXIS_Delta = {}
    #Так, что теперь делаь? перевести
    #param_list = [*g54_g59_AXIS_Display[self.g54_g59_default][0:3], None, None, None, *g54_g59_AXIS_Display[self.g54_g59_default][3:6]]
    param_list = [0, 0, 0, None, None, None, -g54_g59_AXIS_Display[self.g54_g59_default][3], -g54_g59_AXIS_Display[self.g54_g59_default][4], -g54_g59_AXIS_Display[self.g54_g59_default][5]]
    print('param_list где надо ', param_list)
    for ii in range(54, 60):
        ii_s = str(ii)
        key_ = 'G' + ii_s
        #todo А отнимать можно? вроде да. Нет. Нужно в СК g54_g59_AXIS_Display[self.g54_g59_default перейти, наверное
        #g54_g59_AXIS_Delta[key_] = [g54_g59_AXIS_Display[key_][i2] - g54_g59_AXIS_Display[self.g54_g59_default][i2] for i2 in range(6)]
        g54_g59_AXIS_Delta[key_] = [g54_g59_AXIS_Display[key_][i2] - g54_g59_AXIS_Display[self.g54_g59_default][i2] for i2 in range(6)]

        # todo сменить в паре
        g54_g59_AXIS_Delta[key_][0], g54_g59_AXIS_Delta[key_][1], g54_g59_AXIS_Delta[key_][2] = TR_ABC(param_list=param_list, #return_TR_CBA
                                                                                                              X=g54_g59_AXIS_Delta[key_][0],
                                                                                                              Y=g54_g59_AXIS_Delta[key_][1],
                                                                                                              Z=g54_g59_AXIS_Delta[key_][2])
    #Получаю здесь разницу между положениями G549 в СК станины

    print('g54_g59_AXIS_Delta = ', g54_g59_AXIS_Delta)
    #g54_g59_AXIS_Delta[]

    #для G55
    #x0, y0, z0 = g54_g59_AXIS_Display['G54'][0:3]
    #a0, b0, c0 = g54_g59_AXIS_Display['G54'][3:6]
    #x, y, z = g54_g59_AXIS_Display['G55'][0:3]

    # RT_ABC, TR_ABC
    # return_TR_CBA, return_RT_CBA
    #param_list = [x0, y0, z0, None, None, None, a0, b0, c0]
#
    #x_new, y_new, z_new = return_TR_CBA(param_list, X=x, Y=y, Z=z)
    #print('x, y, z  = ', x, y, z)
    #g54_g59_AXIS_Delta['G55'][0] = x_new
    #g54_g59_AXIS_Delta['G55'][1] = y_new
    #g54_g59_AXIS_Delta['G55'][2] = z_new


    return g54_g59_AXIS_Display, g54_g59_AXIS_Delta
