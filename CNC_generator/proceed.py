import math
import os
from CNC_generator.usefull_funcs import DrawGrooveGcodeFinish, DrawGrooveGcodeRough, finish_groove_func, move_ax_along, DrawGrooveGcode45Rough, draw_45_tragectory
from CNC_generator.tragectory45 import Make_tragectory_for45
from Gui.little_gui_classes import simple_warning
#from CNC_generator.usefull_funcs import

def finish_part(self):
    print('НАЧАЛИ')
    d_stock = self.father.groove_strategy_item.finish_groove.D_stock
    Top_x_1_R = None; Top_z_1_R = None
    Top_x_2_R = None; Top_z_2_R = None
    Bot_x_1_R = None; Bot_z_1_R = None
    Bot_x_2_R = None; Bot_z_2_R = None
    Bot_x_1_L = None; Bot_z_1_L = None
    Bot_x_2_L = None; Bot_z_2_L = None
    Top_x_1_L = None; Top_z_1_L = None
    Top_x_2_L = None; Top_z_2_L = None

    if self.geometry.symmetry_check.checkState():
        s_list = self.geometry.symmetry_options.symmetry_list
        Z = float(self.geometry.symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(s_list[n][2].text_.text())
        b = float(s_list[n + 1][2].text_.text())
        Alpha = float(s_list[n + 2][2].text_.text())
        D = float(s_list[n + 3][2].text_.text())
        d = float(s_list[n + 4][2].text_.text())
        if d_stock.lbl_ch.checkState():
            d_delta = D - d
            b_delta = B - b
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            Bnew = b_delta * D_delta / d_delta + b
            D = Dnew
            B = Bnew

        sr_list = self.geometry.symmetry_options.symmetry_list_R_Ch
        top_Lvalue = float(sr_list[0][2].text_.text())
        bot_Lvalue = float(sr_list[1][2].text_.text())
        top_Rvalue = float(sr_list[0][2].text_.text())
        bot_Rvalue = float(sr_list[1][2].text_.text())

        Top_x = D
        Top_z = B / 2
        Bot_x = d
        Bot_z = b / 2

        alpha2 = math.radians(90 + Alpha / 2)
        Alpha_rad = math.radians(Alpha)
        top_type_L = sr_list[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list[1][2].chooser_r_ch.current_text
        top_type_R = sr_list[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list[1][2].chooser_r_ch.current_text

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        if top_type_R == 'R':
            O_top_z = top_Rvalue / math.tan(alpha2 / 2) + Top_z
            Top_x_1_R = D
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x - 2 * top_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Top_z_2_R = Top_z - top_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif top_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_R = Top_x - 2 * h
            Top_z_2_R = Top_z - math.tan(Alpha_rad / 2) * h
            Top_x_1_R = Top_x
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            O_bot_z = - bot_Rvalue / math.tan(alpha2 / 2) + Bot_z
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x + 2 * bot_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Bot_z_1_R = Bot_z + bot_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x + 2 * h
            Bot_z_1_R = Bot_z + math.tan(Alpha_rad / 2) * h
            Bot_x_2_R = Bot_x
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

        Top_z_1_L = None if Top_z_1_R is None else -Top_z_1_R
        Top_z_2_L = None if Top_z_2_R is None else -Top_z_2_R
        Bot_z_1_L = None if Bot_z_1_R is None else -Bot_z_1_R
        Bot_z_2_L = None if Bot_z_2_R is None else -Bot_z_2_R
        Top_x_1_L = Top_x_1_R
        Top_x_2_L = Top_x_2_R
        Bot_x_1_L = Bot_x_1_R
        Bot_x_2_L = Bot_x_2_R

        D_r = Top_x
        D_l = Top_x
        Z_R = B / 2
        Z_L = B / 2
        print('Закончили 1')

    else:  ##############################
        l_list = self.geometry.non_symmetry_options.L_list
        r_list = self.geometry.non_symmetry_options.R_list
        Z = float(self.geometry.non_symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.non_symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(l_list[n][2].text_.text())
        b = float(l_list[n + 1][2].text_.text())
        d = float(l_list[n + 2][2].text_.text())
        Alpha_L = float(r_list[n][2].text_.text())
        Alpha_R = float(r_list[n + 1][2].text_.text())
        D_l = float(r_list[n + 2][2].text_.text())
        D_r = float(r_list[n + 3][2].text_.text())
        d_delta_l = D_l - d
        d_delta_r = D_r - d
        b_delta_lm = math.tan(math.radians(Alpha_L)) * d_delta_l / 2
        b_delta_rm = math.tan(math.radians(Alpha_R)) * d_delta_r / 2

        print('Alpha_R = {}, b_delta_rm = {}'.format(Alpha_R, b_delta_rm))

        if d_stock.lbl_ch.checkState():
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            b_delta_lm = b_delta_lm * (D_delta / 2) / (d_delta_l / 2)
            b_delta_rm = b_delta_rm * (D_delta / 2) / (d_delta_r / 2)
            Bnew = b + b_delta_lm + b_delta_rm
            D_l = Dnew
            D_r = Dnew
            B = Bnew
        sr_list_l = self.geometry.non_symmetry_options.left_list_R_Ch
        sr_list_r = self.geometry.non_symmetry_options.right_list_R_Ch
        Top_x_l = D_l

        Bot_x_l = d
        Bot_z_l = -b / 2
        Top_x_r = D_r

        Bot_x_r = d
        Bot_z_r = b / 2
        alpha_l_add = math.radians(90 + Alpha_L)
        Alpha_l_rad = math.radians(Alpha_L)
        alpha_r_add = math.radians(90 + Alpha_R)
        Alpha_r_rad = math.radians(Alpha_R)
        my_tg_R = math.tan(Alpha_r_rad)
        # Z_R = my_tg_R * (D_r - d) / 2 + b / 2
        # Z_L = B - Z_R
        Z_R = b_delta_rm + b / 2
        Z_L = b_delta_lm + b / 2
        print('ZR = {}'.format(Z_R))

        Top_z_l = -Z_L
        Top_z_r = Z_R

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        top_type_L = sr_list_l[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list_l[1][2].chooser_r_ch.current_text
        top_type_R = sr_list_r[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list_r[1][2].chooser_r_ch.current_text

        top_Lvalue = float(sr_list_l[0][2].text_.text())
        bot_Lvalue = float(sr_list_l[0][2].text_.text())
        top_Rvalue = float(sr_list_r[0][2].text_.text())
        bot_Rvalue = float(sr_list_r[0][2].text_.text())

        print('Top_z_l = ', Top_z_l)
        if top_type_L == 'R':
            O_top_z = - top_Lvalue / math.tan(alpha_l_add / 2) + Top_z_l
            Top_x_1_L = D_l
            Top_z_1_L = O_top_z
            Top_x_2_L = Top_x_l - 2 * top_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Top_z_2_L = Top_z_l + top_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif top_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_L = Top_x_l - 2 * h
            Top_z_2_L = Top_z_l + math.tan(Alpha_l_rad) * h
            Top_x_1_L = Top_x_l
            Top_z_1_L = Top_z_2_L - top_Lvalue

        if bot_type_L == 'R':
            O_bot_x = d + 2 * bot_Lvalue
            O_bot_z = Bot_z_l + bot_Lvalue / math.tan(alpha_l_add / 2)
            Bot_x_2_L = d
            Bot_z_2_L = O_bot_z
            Bot_x_1_L = Bot_x_l + 2 * bot_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Bot_z_1_L = Bot_z_l - bot_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif bot_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            print('h in L = ', h)
            print('Bot_z_l = ', Bot_z_l)
            Bot_x_1_L = Bot_x_l + 2 * h
            Bot_z_1_L = Bot_z_l - math.tan(Alpha_l_rad) * h
            Bot_x_2_L = Bot_x_l
            Bot_z_2_L = Bot_z_1_L + bot_Lvalue

        ######################################################################
        if top_type_R == 'R':
            # O_top_x = D - 2 * top_Rvalue;
            O_top_z = top_Rvalue / math.tan(alpha_r_add / 2) + Top_z_r
            Top_x_1_R = D_r
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x_r - 2 * top_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Top_z_2_R = Top_z_r - top_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif top_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Rvalue * math.tan(f_angl)
            Top_x_2_R = Top_x_r - 2 * h
            print('Top_z_r = ', Top_z_r)
            Top_z_2_R = Top_z_r - math.tan(Alpha_r_rad) * h  # ЗДЕСЬ!
            Top_x_1_R = Top_x_r
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            O_bot_x = d + 2 * bot_Rvalue
            O_bot_z = Bot_z_r - bot_Rvalue / math.tan(alpha_r_add / 2)
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x_r + 2 * bot_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Bot_z_1_R = Bot_z_r + bot_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x_r + 2 * h
            Bot_z_1_R = Bot_z_r + math.tan(Alpha_r_rad) * h
            Bot_x_2_R = Bot_x_r
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

    # _______________________________________________
    print("началаи 2")
    finish_trajectory = [[[D_r, Z_R], [Top_x_1_R, Top_z_1_R], [Top_x_2_R, Top_z_2_R]],  # d, z; d1, z1; d2, x2
                         [[d, b / 2], [Bot_x_1_R, Bot_z_1_R], [Bot_x_2_R, Bot_z_2_R]],  # from out to in
                         [[d, -b / 2], [Bot_x_1_L, Bot_z_1_L], [Bot_x_2_L, Bot_z_2_L]],
                         [[D_l, - Z_L], [Top_x_1_L, Top_z_1_L], [Top_x_2_L, Top_z_2_L]]]
    print("finish_trajectory = ", finish_trajectory)
    finish_ = self.father.groove_strategy_item.finish_groove
    finish_tool_panel = self.father.groove_tool_item.finish_groove_panel
    tool_index = self.father.groove_tool_item.finish_groove_panel.tool_chooser.currentIndex()
    finish_exact_tool_panel = finish_tool_panel.tools_list[tool_index]
    tool_r = float(finish_exact_tool_panel.R.text())
    allowanceX = 0
    allowanceZ = 0
    thick = 0
    if finish_.thickness_ch.isChecked():
        thick = float(finish_.thickness.text())
    else:
        allowanceX = float(finish_.X_allowance.text())
        allowanceZ = float(finish_.Z_allowance.text())
    if finish_.corrector.isChecked():
        tool_r_new = 0
        thick_new = 0
    else:
        tool_r_new = tool_r
        thick_new = thick
    # HERE
    new_finish_trajectory = finish_groove_func(geometry=finish_trajectory, allowanceX=allowanceX,
                                               allowanceZ=allowanceZ, allowanceThickness=tool_r_new + thick_new,
                                               top_r_value=top_Rvalue, top_l_value=top_Lvalue,
                                               bot_r_value=bot_Rvalue, bot_l_value=bot_Lvalue, top_type_r=top_type_R,
                                               top_type_l=top_type_L,
                                               bot_type_r=bot_type_R, bot_type_l=bot_type_L)
    for nf in new_finish_trajectory:
        nf = move_ax_along(nf, 1, -Z)
    print('new_finish_trajectory = ', new_finish_trajectory)
    tool_l = self.finish_groove_panel.tools_list
    if self.finish_groove_panel.tool_chooser.currentIndex() == 0:
        tool = {'type': 'B', 'B': float(tool_l[0].B.text()), 'tool_R': tool_r,
                'bind_place': tool_l[0].Bind.currentIndex() + 1}
    elif self.finish_groove_panel.tool_chooser.currentIndex() == 1:
        tool = {'type': 'R', 'B': float(tool_l[1].R.text()) * 2, 'tool_R': tool_r,
                'bind_place': tool_l[1].Bind.currentIndex() + 1}
    else:
        tool = {'type': 'A', 'angle': math.radians(float(tool_l[2].Angle.text())), 'tool_R': tool_r,
                'bind_place': tool_l[2].Bind.currentIndex() + 1, 'rX step': float(tool_l[2].RX_step.text())}
    param = {'TopFRr': [top_type_R, top_Rvalue], 'TopFRl': [top_type_L, top_Lvalue], 'BotFRr': [bot_type_R, bot_Rvalue],
             'BotFRl': [bot_type_L, bot_Lvalue], 'Xa': allowanceX,
             'Za': allowanceZ, 'corrector': self.father.groove_strategy_item.finish_groove.corrector.isChecked(),
             #'rXstock': float(tool_l[2].rXallowance.text()),
             'Thick': thick}
    print('PARAM bot value = ', param['BotFRr'])
    print('FINISH trajectory: ', new_finish_trajectory)
    result_str, r_, l_ = DrawGrooveGcodeFinish(tool, new_finish_trajectory, param)
    if result_str is not False:
        result_str = '\r\n;FINISH:\r\n' + result_str
        return result_str, r_, l_
    else:
        print("Закончили2")
        return "\r\n;Tool can't be put here\r\n", r_, l_

    # Наконец-то
    # дальше G код нарисовать и инструмент прикрутить

def semifinish_part(self):
    print('НАЧАЛИ')
    d_stock = self.father.groove_strategy_item.semi_finish_groove.D_stock
    Top_x_1_R = None; Top_z_1_R = None
    Top_x_2_R = None; Top_z_2_R = None
    Bot_x_1_R = None; Bot_z_1_R = None
    Bot_x_2_R = None; Bot_z_2_R = None
    Bot_x_1_L = None; Bot_z_1_L = None
    Bot_x_2_L = None; Bot_z_2_L = None
    Top_x_1_L = None; Top_z_1_L = None
    Top_x_2_L = None; Top_z_2_L = None

    if self.geometry.symmetry_check.checkState():
        s_list = self.geometry.symmetry_options.symmetry_list
        Z = float(self.geometry.symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(s_list[n][2].text_.text())
        b = float(s_list[n + 1][2].text_.text())
        Alpha = float(s_list[n + 2][2].text_.text())
        D = float(s_list[n + 3][2].text_.text())
        d = float(s_list[n + 4][2].text_.text())
        if d_stock.lbl_ch.checkState():
            d_delta = D - d
            b_delta = B - b
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            Bnew = b_delta * D_delta / d_delta + b
            D = Dnew
            B = Bnew

        sr_list = self.geometry.symmetry_options.symmetry_list_R_Ch
        top_Lvalue = float(sr_list[0][2].text_.text())
        bot_Lvalue = float(sr_list[1][2].text_.text())
        top_Rvalue = float(sr_list[0][2].text_.text())
        bot_Rvalue = float(sr_list[1][2].text_.text())

        Top_x = D
        Top_z = B / 2
        Bot_x = d
        Bot_z = b / 2

        alpha2 = math.radians(90 + Alpha / 2)
        Alpha_rad = math.radians(Alpha)
        top_type_L = sr_list[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list[1][2].chooser_r_ch.current_text
        top_type_R = sr_list[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list[1][2].chooser_r_ch.current_text

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        if top_type_R == 'R':
            O_top_z = top_Rvalue / math.tan(alpha2 / 2) + Top_z
            Top_x_1_R = D
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x - 2 * top_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Top_z_2_R = Top_z - top_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif top_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_R = Top_x - 2 * h
            Top_z_2_R = Top_z - math.tan(Alpha_rad / 2) * h
            Top_x_1_R = Top_x
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            O_bot_z = - bot_Rvalue / math.tan(alpha2 / 2) + Bot_z
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x + 2 * bot_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Bot_z_1_R = Bot_z + bot_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x + 2 * h
            Bot_z_1_R = Bot_z + math.tan(Alpha_rad / 2) * h
            Bot_x_2_R = Bot_x
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

        Top_z_1_L = None if Top_z_1_R is None else -Top_z_1_R
        Top_z_2_L = None if Top_z_2_R is None else -Top_z_2_R
        Bot_z_1_L = None if Bot_z_1_R is None else -Bot_z_1_R
        Bot_z_2_L = None if Bot_z_2_R is None else -Bot_z_2_R
        Top_x_1_L = Top_x_1_R
        Top_x_2_L = Top_x_2_R
        Bot_x_1_L = Bot_x_1_R
        Bot_x_2_L = Bot_x_2_R

        D_r = Top_x
        D_l = Top_x
        Z_R = B / 2
        Z_L = B / 2
        print('Закончили 1')

    else:
        l_list = self.geometry.non_symmetry_options.L_list
        r_list = self.geometry.non_symmetry_options.R_list
        Z = float(self.geometry.non_symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.non_symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(l_list[n][2].text_.text())
        b = float(l_list[n + 1][2].text_.text())
        d = float(l_list[n + 2][2].text_.text())
        Alpha_L = float(r_list[n][2].text_.text())
        Alpha_R = float(r_list[n + 1][2].text_.text())
        D_l = float(r_list[n + 2][2].text_.text())
        D_r = float(r_list[n + 3][2].text_.text())
        d_delta_l = D_l - d
        d_delta_r = D_r - d
        b_delta_lm = math.tan(math.radians(Alpha_L)) * d_delta_l / 2
        b_delta_rm = math.tan(math.radians(Alpha_R)) * d_delta_r / 2

        print('Alpha_R = {}, b_delta_rm = {}'.format(Alpha_R, b_delta_rm))

        if d_stock.lbl_ch.checkState():
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            b_delta_lm = b_delta_lm * (D_delta / 2) / (d_delta_l / 2)
            b_delta_rm = b_delta_rm * (D_delta / 2) / (d_delta_r / 2)
            Bnew = b + b_delta_lm + b_delta_rm
            D_l = Dnew
            D_r = Dnew
            B = Bnew
        sr_list_l = self.geometry.non_symmetry_options.left_list_R_Ch
        sr_list_r = self.geometry.non_symmetry_options.right_list_R_Ch
        Top_x_l = D_l

        Bot_x_l = d
        Bot_z_l = -b / 2
        Top_x_r = D_r

        Bot_x_r = d
        Bot_z_r = b / 2
        alpha_l_add = math.radians(90 + Alpha_L)
        Alpha_l_rad = math.radians(Alpha_L)
        alpha_r_add = math.radians(90 + Alpha_R)
        Alpha_r_rad = math.radians(Alpha_R)
        my_tg_R = math.tan(Alpha_r_rad)
        Z_R = b_delta_rm + b / 2
        Z_L = b_delta_lm + b / 2
        print('ZR = {}'.format(Z_R))

        Top_z_l = -Z_L
        Top_z_r = Z_R

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        top_type_L = sr_list_l[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list_l[1][2].chooser_r_ch.current_text
        top_type_R = sr_list_r[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list_r[1][2].chooser_r_ch.current_text

        top_Lvalue = float(sr_list_l[0][2].text_.text())
        bot_Lvalue = float(sr_list_l[0][2].text_.text())
        top_Rvalue = float(sr_list_r[0][2].text_.text())
        bot_Rvalue = float(sr_list_r[0][2].text_.text())

        print('Top_z_l = ', Top_z_l)
        if top_type_L == 'R':
            O_top_z = - top_Lvalue / math.tan(alpha_l_add / 2) + Top_z_l
            Top_x_1_L = D_l
            Top_z_1_L = O_top_z
            Top_x_2_L = Top_x_l - 2 * top_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Top_z_2_L = Top_z_l + top_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif top_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_L = Top_x_l - 2 * h
            Top_z_2_L = Top_z_l + math.tan(Alpha_l_rad) * h
            Top_x_1_L = Top_x_l
            Top_z_1_L = Top_z_2_L - top_Lvalue

        if bot_type_L == 'R':
            O_bot_x = d + 2 * bot_Lvalue
            O_bot_z = Bot_z_l + bot_Lvalue / math.tan(alpha_l_add / 2)
            Bot_x_2_L = d
            Bot_z_2_L = O_bot_z
            Bot_x_1_L = Bot_x_l + 2 * bot_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Bot_z_1_L = Bot_z_l - bot_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif bot_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            print('h in L = ', h)
            print('Bot_z_l = ', Bot_z_l)
            Bot_x_1_L = Bot_x_l + 2 * h
            Bot_z_1_L = Bot_z_l - math.tan(Alpha_l_rad) * h
            Bot_x_2_L = Bot_x_l
            Bot_z_2_L = Bot_z_1_L + bot_Lvalue

        ######################################################################
        if top_type_R == 'R':
            # O_top_x = D - 2 * top_Rvalue;
            O_top_z = top_Rvalue / math.tan(alpha_r_add / 2) + Top_z_r
            Top_x_1_R = D_r
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x_r - 2 * top_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Top_z_2_R = Top_z_r - top_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif top_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Rvalue * math.tan(f_angl)
            Top_x_2_R = Top_x_r - 2 * h
            print('Top_z_r = ', Top_z_r)
            Top_z_2_R = Top_z_r - math.tan(Alpha_r_rad) * h  # ЗДЕСЬ!
            Top_x_1_R = Top_x_r
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            O_bot_x = d + 2 * bot_Rvalue
            O_bot_z = Bot_z_r - bot_Rvalue / math.tan(alpha_r_add / 2)
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x_r + 2 * bot_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Bot_z_1_R = Bot_z_r + bot_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x_r + 2 * h
            Bot_z_1_R = Bot_z_r + math.tan(Alpha_r_rad) * h
            Bot_x_2_R = Bot_x_r
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

    # _______________________________________________
    print("началаи 2")
    finish_trajectory = [[[D_r, Z_R], [Top_x_1_R, Top_z_1_R], [Top_x_2_R, Top_z_2_R]],  # d, z; d1, z1; d2, x2
                         [[d, b / 2], [Bot_x_1_R, Bot_z_1_R], [Bot_x_2_R, Bot_z_2_R]],  # from out to in
                         [[d, -b / 2], [Bot_x_1_L, Bot_z_1_L], [Bot_x_2_L, Bot_z_2_L]],
                         [[D_l, - Z_L], [Top_x_1_L, Top_z_1_L], [Top_x_2_L, Top_z_2_L]]]
    print("finish_trajectory = ", finish_trajectory)
    semifinish_ = self.father.groove_strategy_item.semi_finish_groove
    semifinish_tool_panel = self.father.groove_tool_item.semifinish_groove_panel
    tool_index = self.father.groove_tool_item.semifinish_groove_panel.tool_chooser.currentIndex()
    semifinish_exact_tool_panel = semifinish_tool_panel.tools_list[tool_index]
    tool_r = float(semifinish_exact_tool_panel.R.text())
    allowanceX = 0
    allowanceZ = 0
    thick = 0
    if semifinish_.thickness_ch.isChecked():
        thick = float(semifinish_.thickness.text())
    else:
        allowanceX = float(semifinish_.X_allowance.text())
        allowanceZ = float(semifinish_.Z_allowance.text())
    if semifinish_.corrector.isChecked():
        tool_r_new = 0
        thick_new = 0
    else:
        tool_r_new = tool_r
        thick_new = thick

    new_semi_finish_trajectory = finish_groove_func(geometry=finish_trajectory, allowanceX=allowanceX,
                                               allowanceZ=allowanceZ, allowanceThickness=tool_r_new + thick_new,
                                               top_r_value=top_Rvalue, top_l_value=top_Lvalue,
                                               bot_r_value=bot_Rvalue, bot_l_value=bot_Lvalue, top_type_r=top_type_R,
                                               top_type_l=top_type_L,
                                               bot_type_r=bot_type_R, bot_type_l=bot_type_L)
    for nf in new_semi_finish_trajectory:
        nf = move_ax_along(nf, 1, -Z)
    print('new_finish_trajectory = ', new_semi_finish_trajectory)
    tool_l = self.finish_groove_panel.tools_list
    if self.finish_groove_panel.tool_chooser.currentIndex() == 0:
        tool = {'type': 'B', 'B': float(tool_l[0].B.text()), 'tool_R': tool_r,
                'bind_place': tool_l[0].Bind.currentIndex() + 1}
    elif self.finish_groove_panel.tool_chooser.currentIndex() == 1:
        tool = {'type': 'R', 'B': float(tool_l[1].R.text()) * 2, 'tool_R': tool_r,
                'bind_place': tool_l[1].Bind.currentIndex() + 1}
    else:
        tool = {'type': 'A', 'angle': math.radians(float(tool_l[2].Angle.text())), 'tool_R': tool_r,
                'bind_place': tool_l[2].Bind.currentIndex() + 1, 'rX step': float(tool_l[2].RX_step.text())}
    param = {'TopFRr': [top_type_R, top_Rvalue], 'TopFRl': [top_type_L, top_Lvalue], 'BotFRr': [bot_type_R, bot_Rvalue],
             'BotFRl': [bot_type_L, bot_Lvalue], 'Xa': allowanceX,
             'Za': allowanceZ, 'corrector': self.father.groove_strategy_item.semi_finish_groove.corrector.isChecked(),
             'Thick': thick}
    print('PARAM bot value = ', param['BotFRr'])

    result_str, r_, l_ = DrawGrooveGcodeFinish(tool, new_semi_finish_trajectory, param)
    result_str = '\r\n;SEMI-FINISH:\r\n' + result_str
    print("Закончили2")
    return result_str, r_, l_



def rough_part(self):
    print('Rough start')
    d_stock = self.father.groove_strategy_item.rough_groove.D_stock
    Top_x_1_R = None; Top_z_1_R = None
    Top_x_2_R = None; Top_z_2_R = None
    Bot_x_1_R = None; Bot_z_1_R = None
    Bot_x_2_R = None; Bot_z_2_R = None
    Bot_x_1_L = None; Bot_z_1_L = None
    Bot_x_2_L = None; Bot_z_2_L = None
    Top_x_1_L = None; Top_z_1_L = None
    Top_x_2_L = None; Top_z_2_L = None

    if self.geometry.symmetry_check.checkState():
        s_list = self.geometry.symmetry_options.symmetry_list
        Z = float(self.geometry.symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(s_list[n][2].text_.text())
        b = float(s_list[n + 1][2].text_.text())
        Alpha = float(s_list[n + 2][2].text_.text())
        D = float(s_list[n + 3][2].text_.text())
        d = float(s_list[n + 4][2].text_.text())
        if d_stock.lbl_ch.checkState():
            d_delta = D - d
            b_delta = B - b
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            Bnew = b_delta * D_delta / d_delta + b
            D = Dnew
            B = Bnew

        sr_list = self.geometry.symmetry_options.symmetry_list_R_Ch
        top_Lvalue = float(sr_list[0][2].text_.text())
        bot_Lvalue = float(sr_list[1][2].text_.text())
        top_Rvalue = float(sr_list[0][2].text_.text())
        bot_Rvalue = float(sr_list[1][2].text_.text())

        Top_x = D
        Top_z = B / 2
        Bot_x = d
        Bot_z = b / 2

        alpha2 = math.radians(90 + Alpha / 2)
        Alpha_rad = math.radians(Alpha)
        top_type_L = sr_list[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list[1][2].chooser_r_ch.current_text
        top_type_R = sr_list[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list[1][2].chooser_r_ch.current_text

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        if top_type_R == 'R':
            print('===top_type_R===')
            # O_top_x = D - 2 * top_Rvalue;
            O_top_z = top_Rvalue / math.tan(alpha2 / 2) + Top_z
            Top_x_1_R = D
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x - 2 * top_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Top_z_2_R = Top_z - top_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif top_type_R == 'Chamfer':
            print('===top_type_R=Chamfer===')
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_R = Top_x - 2 * h
            Top_z_2_R = Top_z - math.tan(Alpha_rad / 2) * h
            Top_x_1_R = Top_x
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            # O_bot_x = d + 2 * bot_Rvalue
            O_bot_z = - bot_Rvalue / math.tan(alpha2 / 2) + Bot_z
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x + 2 * bot_Rvalue / math.tan(alpha2 / 2) * math.cos(alpha2 - math.pi / 2)
            Bot_z_1_R = Bot_z + bot_Rvalue / math.tan(alpha2 / 2) * math.sin(alpha2 - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x + 2 * h
            Bot_z_1_R = Bot_z + math.tan(Alpha_rad / 2) * h
            Bot_x_2_R = Bot_x
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

        Top_z_1_L = None if Top_z_1_R is None else -Top_z_1_R
        Top_z_2_L = None if Top_z_2_R is None else -Top_z_2_R
        Bot_z_1_L = None if Bot_z_1_R is None else -Bot_z_1_R
        Bot_z_2_L = None if Bot_z_2_R is None else -Bot_z_2_R
        Top_x_1_L = Top_x_1_R
        Top_x_2_L = Top_x_2_R
        Bot_x_1_L = Bot_x_1_R
        Bot_x_2_L = Bot_x_2_R

        D_r = Top_x
        D_l = Top_x
        Z_R = B / 2
        Z_L = B / 2
        print('Закончили 1')

    else:  ##############################
        l_list = self.geometry.non_symmetry_options.L_list
        r_list = self.geometry.non_symmetry_options.R_list
        Z = float(self.geometry.non_symmetry_options.Z.Z_value.text())
        Z_type = self.geometry.non_symmetry_options.Z.Z_n.currentText()
        n = 0
        B = float(l_list[n][2].text_.text())
        b = float(l_list[n + 1][2].text_.text())
        d = float(l_list[n + 2][2].text_.text())
        Alpha_L = float(r_list[n][2].text_.text())
        Alpha_R = float(r_list[n + 1][2].text_.text())
        D_l = float(r_list[n + 2][2].text_.text())
        D_r = float(r_list[n + 3][2].text_.text())
        d_delta_l = D_l - d
        d_delta_r = D_r - d
        b_delta_lm = math.tan(math.radians(Alpha_L)) * d_delta_l / 2
        b_delta_rm = math.tan(math.radians(Alpha_R)) * d_delta_r / 2

        print('Alpha_R = {}, b_delta_rm = {}'.format(Alpha_R, b_delta_rm))

        if d_stock.lbl_ch.checkState():
            Dnew = d_stock.give_new_D()
            D_delta = Dnew - d
            b_delta_lm = b_delta_lm * (D_delta / 2) / (d_delta_l / 2)
            b_delta_rm = b_delta_rm * (D_delta / 2) / (d_delta_r / 2)
            Bnew = b + b_delta_lm + b_delta_rm
            D_l = Dnew
            D_r = Dnew
            B = Bnew
        sr_list_l = self.geometry.non_symmetry_options.left_list_R_Ch
        sr_list_r = self.geometry.non_symmetry_options.right_list_R_Ch
        Top_x_l = D_l

        Bot_x_l = d
        Bot_z_l = -b / 2
        Top_x_r = D_r

        Bot_x_r = d
        Bot_z_r = b / 2
        alpha_l_add = math.radians(90 + Alpha_L)
        Alpha_l_rad = math.radians(Alpha_L)
        alpha_r_add = math.radians(90 + Alpha_R)
        Alpha_r_rad = math.radians(Alpha_R)
        my_tg_R = math.tan(Alpha_r_rad)
        # Z_R = my_tg_R * (D_r - d) / 2 + b / 2
        # Z_L = B - Z_R
        Z_R = b_delta_rm + b / 2
        Z_L = b_delta_lm + b / 2
        print('ZR = {}'.format(Z_R))

        Top_z_l = -Z_L
        Top_z_r = Z_R

        if Z_type == 'Z1':
            Z = Z - B / 2
        elif Z_type == 'Z3':
            Z = Z + B / 2

        top_type_L = sr_list_l[0][2].chooser_r_ch.current_text
        bot_type_L = sr_list_l[1][2].chooser_r_ch.current_text
        top_type_R = sr_list_r[0][2].chooser_r_ch.current_text
        bot_type_R = sr_list_r[1][2].chooser_r_ch.current_text

        top_Lvalue = float(sr_list_l[0][2].text_.text())
        bot_Lvalue = float(sr_list_l[0][2].text_.text())
        top_Rvalue = float(sr_list_r[0][2].text_.text())
        bot_Rvalue = float(sr_list_r[0][2].text_.text())

        print('Top_z_l = ', Top_z_l)
        if top_type_L == 'R':
            O_top_z = - top_Lvalue / math.tan(alpha_l_add / 2) + Top_z_l
            Top_x_1_L = D_l
            Top_z_1_L = O_top_z
            Top_x_2_L = Top_x_l - 2 * top_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Top_z_2_L = Top_z_l + top_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif top_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Lvalue * math.tan(f_angl)
            Top_x_2_L = Top_x_l - 2 * h
            Top_z_2_L = Top_z_l + math.tan(Alpha_l_rad) * h
            Top_x_1_L = Top_x_l
            Top_z_1_L = Top_z_2_L - top_Lvalue

        if bot_type_L == 'R':
            O_bot_x = d + 2 * bot_Lvalue
            O_bot_z = Bot_z_l + bot_Lvalue / math.tan(alpha_l_add / 2)
            Bot_x_2_L = d
            Bot_z_2_L = O_bot_z
            Bot_x_1_L = Bot_x_l + 2 * bot_Lvalue / math.tan(alpha_l_add / 2) * math.cos(alpha_l_add - math.pi / 2)
            Bot_z_1_L = Bot_z_l - bot_Lvalue / math.tan(alpha_l_add / 2) * math.sin(alpha_l_add - math.pi / 2)
        elif bot_type_L == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            print('h in L = ', h)
            print('Bot_z_l = ', Bot_z_l)
            Bot_x_1_L = Bot_x_l + 2 * h
            Bot_z_1_L = Bot_z_l - math.tan(Alpha_l_rad) * h
            Bot_x_2_L = Bot_x_l
            Bot_z_2_L = Bot_z_1_L + bot_Lvalue

        ######################################################################
        if top_type_R == 'R':
            # O_top_x = D - 2 * top_Rvalue;
            O_top_z = top_Rvalue / math.tan(alpha_r_add / 2) + Top_z_r
            Top_x_1_R = D_r
            Top_z_1_R = O_top_z
            Top_x_2_R = Top_x_r - 2 * top_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Top_z_2_R = Top_z_r - top_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif top_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = top_Rvalue * math.tan(f_angl)
            Top_x_2_R = Top_x_r - 2 * h
            print('Top_z_r = ', Top_z_r)
            Top_z_2_R = Top_z_r - math.tan(Alpha_r_rad) * h  # ЗДЕСЬ!
            Top_x_1_R = Top_x_r
            Top_z_1_R = Top_z_2_R + top_Rvalue

        if bot_type_R == 'R':
            O_bot_x = d + 2 * bot_Rvalue
            O_bot_z = Bot_z_r - bot_Rvalue / math.tan(alpha_r_add / 2)
            Bot_x_2_R = d
            Bot_z_2_R = O_bot_z
            Bot_x_1_R = Bot_x_r + 2 * bot_Rvalue / math.tan(alpha_r_add / 2) * math.cos(alpha_r_add - math.pi / 2)
            Bot_z_1_R = Bot_z_r + bot_Rvalue / math.tan(alpha_r_add / 2) * math.sin(alpha_r_add - math.pi / 2)
        elif bot_type_R == 'Chamfer':
            f_angl = math.radians(45)
            h = bot_Lvalue * math.tan(f_angl)
            Bot_x_1_R = Bot_x_r + 2 * h
            Bot_z_1_R = Bot_z_r + math.tan(Alpha_r_rad) * h
            Bot_x_2_R = Bot_x_r
            Bot_z_2_R = Bot_z_1_R - bot_Rvalue

    # _______________________________________________
    print("началаи 2")

    rough_trajectory = [[[D_r, Z_R], [Top_x_1_R, Top_z_1_R], [Top_x_2_R, Top_z_2_R]],  # d, z; d1, z1; d2, x2
                         [[d, b / 2], [Bot_x_1_R, Bot_z_1_R], [Bot_x_2_R, Bot_z_2_R]],  # from out to in
                         [[d, -b / 2], [Bot_x_1_L, Bot_z_1_L], [Bot_x_2_L, Bot_z_2_L]],
                         [[D_l, - Z_L], [Top_x_1_L, Top_z_1_L], [Top_x_2_L, Top_z_2_L]]]
    rough_ = self.father.groove_strategy_item.rough_groove
    rough_tool_panel = self.father.groove_tool_item.rough_groove_panel
    tool_index = self.father.groove_tool_item.rough_groove_panel.tool_chooser.currentIndex()


    if tool_index == 3:
        rough_exact_tool_panel_45 = rough_tool_panel.tools_list[tool_index]
        tool_r_45 = float(rough_exact_tool_panel_45.R.text())
        tool_index_in45 = rough_exact_tool_panel_45.tool_panel.tool_chooser.currentIndex()
        rough_exact_tool_panel = rough_exact_tool_panel_45.tool_panel.tools_list[tool_index_in45]
    else:
        rough_exact_tool_panel = rough_tool_panel.tools_list[tool_index]
    tool_r = float(rough_exact_tool_panel.R.text())

    allowanceX = 0
    allowanceZ = 0
    thick = 0
    if rough_.thickness_ch.isChecked():
        thick = float(rough_.thickness.text())
    else:
        allowanceX = float(rough_.X_allowance.text())
        allowanceZ = float(rough_.Z_allowance.text())

    tool_r_new = tool_r
    thick_new = thick
    print('rough_trajectory before 0 finish ', rough_trajectory)
    new_rough_trajectory = finish_groove_func(geometry=rough_trajectory, allowanceX=allowanceX,
                                               allowanceZ=allowanceZ, allowanceThickness=tool_r_new + thick_new,
                                               top_r_value=top_Rvalue, top_l_value=top_Lvalue,
                                               bot_r_value=bot_Rvalue, bot_l_value=bot_Lvalue, top_type_r=top_type_R,
                                               top_type_l=top_type_L,
                                               bot_type_r=bot_type_R, bot_type_l=bot_type_L)
    if tool_index == 3:
        print('||| tool_index == 3: tool_r_45 = {}, thick_new = {}'.format(tool_r_45, thick_new))
        print('rough_trajectory before finish ', rough_trajectory)
        new_rough_trajectory_45 = finish_groove_func(geometry=rough_trajectory, allowanceX=allowanceX,
                                                   allowanceZ=allowanceZ, allowanceThickness=tool_r_45 + thick_new,
                                                   top_r_value=top_Rvalue, top_l_value=top_Lvalue,
                                                   bot_r_value=bot_Rvalue, bot_l_value=bot_Lvalue, top_type_r=top_type_R,
                                                   top_type_l=top_type_L,
                                                   bot_type_r=bot_type_R, bot_type_l=bot_type_L)
        print('in tool_index == 3, new_rough_trajectory_45 = {}'.format(new_rough_trajectory_45))
        #здесь проблема
        for nf in new_rough_trajectory_45:#todo не на всё распротсраненно сейчас, наверное нужно и для другого инструмента других территорий
            nf = move_ax_along(nf, 1, -Z)


    print('new_rough_trajectory = ', new_rough_trajectory)
    for nf in new_rough_trajectory:
        nf = move_ax_along(nf, 1, -Z)
    tool_l = self.rough_groove_panel.tools_list
    #print("self.rough_groove_panel.tool_chooser.currentIndex() = ", self.rough_groove_panel.tool_chooser.currentIndex())
    second_tool_dict = None
    param = {'TopFRr': [top_type_R, top_Rvalue], 'TopFRl': [top_type_L, top_Lvalue], 'BotFRr': [bot_type_R, bot_Rvalue],
             'BotFRl': [bot_type_L, bot_Lvalue], 'Xa': allowanceX, 'Za': allowanceZ, 'accurate': rough_.accurate.isChecked(),
             'Thick': thick, 'corrector': False}

    if self.rough_groove_panel.tool_chooser.currentIndex() == 0:
        tool = {'type': 'B', 'B': float(tool_l[0].B.text()), 'tool_R': tool_r,
                'bind_place': tool_l[0].Bind.currentIndex() + 1, 'rX step': float(tool_l[0].RX_step.text()),
                'Lap min': float(tool_l[0].ZX_step.text())}
    elif self.rough_groove_panel.tool_chooser.currentIndex() == 1:
        tool = {'type': 'R', 'B': float(tool_l[1].R.text()) * 2, 'tool_R': tool_r, 'rX step': float(tool_l[1].RX_step.text()),
                'Lap min': float(tool_l[1].ZX_step.text()), 'bind_place': tool_l[1].Bind.currentIndex() + 1}
    elif self.rough_groove_panel.tool_chooser.currentIndex() == 2:
        tool = {'type': 'A', 'angle': math.radians(float(tool_l[2].Angle.text())),
                'tool_R': tool_r, 'rX step': float(tool_l[2].RX_step.text()),  'bind_place': tool_l[2].Bind.currentIndex() + 1,
                #'Dstock': float(tool_l[3].tool_panel.tools_list[2].rXallowance.text())
                }
    else:#tool_panel 45
        if tool_l[3].tool_panel.tool_chooser.currentIndex() == 0:#float(tool_l[3].tool_panel.tools_list[0].R.text())
            second_tool_dict = {'type': 'B',
                                'B': float(tool_l[3].tool_panel.tools_list[0].B.text()), 'tool_R': tool_r,
                                'bind_place': tool_l[3].tool_panel.tools_list[0].Bind.currentIndex() + 1,
                                'rX step': float(tool_l[3].tool_panel.tools_list[0].RX_step.text()),
                                'Lap min': float(tool_l[3].tool_panel.tools_list[0].ZX_step.text())}

        elif tool_l[3].tool_panel.tool_chooser.currentIndex() == 1:
            second_tool_dict = {'type': 'R', 'B': float(tool_l[3].tool_panel.tools_list[1].R.text()) * 2,
                                'tool_R': tool_r,
                                'rX step': float(tool_l[3].tool_panel.tools_list[1].RX_step.text()),
                                'Lap min': float(tool_l[3].tool_panel.tools_list[1].ZX_step.text()),
                                'bind_place': tool_l[3].tool_panel.tools_list[1].Bind.currentIndex() + 1}
        else:#2
            second_tool_dict = {'type': 'A',
                                'angle': math.radians(float(tool_l[3].tool_panel.tools_list[2].Angle.text())),
                                'tool_R': tool_r,
                                'rX step': float(tool_l[3].tool_panel.tools_list[2].RX_step.text()),
                                'bind_place': tool_l[3].tool_panel.tools_list[2].Bind.currentIndex() + 1}
        tool = {'type': '45', 'rX step': float(tool_l[3].RX_step.text()), 'tool_R': tool_r_45, 'second_tool': second_tool_dict}

    if tool['type'] == '45':
        #clear = lambda: os.system('cls')
        #clear()
        tragectory45, tragectory_prev_limit = Make_tragectory_for45(geometry=rough_trajectory, tragectory45=new_rough_trajectory_45, tragectory_2=new_rough_trajectory, tool45=tool, tool2=second_tool_dict, param=param)
        #
        print('|||| tragectory45 = ', tragectory45)# центр инструмента 45
        #tragectory45, tragectory_prev_limit, geometry, tool45, tool, param
        str45 = ';45 Tool\r\n' + draw_45_tragectory(tragectory45=tragectory45, tragectory_prev_limit=tragectory_prev_limit, geometry=new_rough_trajectory, tool45=tool, tool=second_tool_dict, param=param)
        #tragectory45, tragectory_prev_limit, geometry, tool45, tool, param
        str_finish_after, _garbage1, garbage2 = DrawGrooveGcodeFinish(tool=second_tool_dict, trajectory_dots=new_rough_trajectory, param=param)
        str2 = str_finish_after
        result_str0, result_str1 = str45, str2
    else:
        result_str1, r_side_track, l_side_track = DrawGrooveGcodeFinish(tool, new_rough_trajectory, param)
        result_str0 = DrawGrooveGcodeRough(tool, r_side_track, l_side_track, param, new_rough_trajectory)#second_tool_dict,

    print("Закончили2")
    return ';ROUGH:\r\n' + result_str0 + result_str1