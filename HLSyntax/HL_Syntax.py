import numpy as np
from PyQt5.QtGui import QSyntaxHighlighter
from PyQt5.QtCore import QRegularExpression
from Modelling_clay.Processors.Processor_base.ReversPostProcessor_0 import STYLES, STYLES_list_G0, STYLES_list_G1
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT


class GMHighlighter(QSyntaxHighlighter):

    def __init__(self, document, base, proc_class):
        QSyntaxHighlighter.__init__(self, document)
        #print('DICTS that i am seeking for ', proc_class.OPERATORs_DICT_math)
        self.base = base
        #print('wtf: ', type(base))
        self.reversal_post_processor = proc_class(base)
        #print('wtf2: ', type(self.reversal_post_processor))
        self.SHIFT_masks = self.reversal_post_processor.SHIFT_masks
        self.SUBprogram_mask = self.reversal_post_processor.SUBprogram_mask
        print(f'Hy self.SUBprogram_mask = {self.SUBprogram_mask}')

        #то что выше - нельзя делать. Последовательность нарушена
        #нужно организовать
        #self.np_box = self.base.np_box todo НЕТ
        self.current_SHIFT_list = []
        self.current_XYZvars_dict = {}
        self.GM_current_list = []
        #self.IF

        self.list_number_captured_1 = [i * 2 for i in range(1, 15)]#todo добавь ijk
        self.list_number_captured_1.insert(3, 6)
        self.previous_block_g = 0

        #self.reversal_post_processor.

        self.count = 0
        self.count_in_step = 0
        self.const_step = 1000
        self.standart_step = self.const_step
        self.main_rule_regular_expression = QRegularExpression(self.reversal_post_processor.sorted_axis_rule)
        self.simple_format = STYLES['axis']#self.first_rule[2]
        self.second_rule_regular_expression = QRegularExpression(self.reversal_post_processor.unsorted_axis_rule)#self.rules[0][0]
        self.rule_ax_vars = QRegularExpression(self.reversal_post_processor.unsorted_rule_ax_vars)

        #self.START_EXP_param =  self.reversal_post_processor.START_EXP_param
        self.START_EXP_var = self.reversal_post_processor.START_EXP_var

        #self.third_rule_regular_expression = QRegularExpression(self.reversal_post_processor.third_rule) don't need now
        self.too_little_number_for_big_step_check()
        self.sub_programs = self.full_dcit_sub_programs_without_masks()
        print(f'99 self.sub_programs = {self.sub_programs}')

        print(self.main_rule_regular_expression)


    def full_dcit_sub_programs_without_masks(self):#thats does not need editing. edit sub_programs_current instead
        print(self.base.editor.existing)
        self.current_catalog_vars = self.reversal_post_processor.sub_programs_static
        print('self.current_catalog_vars = ', self.current_catalog_vars)
        if self.base.editor.existing:
            catalog = self.base.editor.existing.rsplit('/', 1)

            if len(catalog) > 1:
                cat = self.reversal_post_processor.sub_programs_current(catalog[0])
                for k_ in cat:
                    self.current_catalog_vars[k_] = cat[k_]

        return self.current_catalog_vars

    def too_little_number_for_big_step_check(self):
        print('too_little_number_check')
        if self.base.reading_lines_number < self.const_step:
            self.standart_step = self.base.reading_lines_number


    def highlightBlock(self, text):
        """Применить выделение синтаксиса к данному блоку текста. """
        print(f'highlight: {text}, из {self.count}')
        #self.recount_some_line(type16=999)#todo временно отключен hightlightBlock
        #return
        nya = self.main_rule_regular_expression.match(text, 0)
        start = nya.capturedStart()
        len_match = nya.capturedLength()
        if len_match != 0:
            print('first rule')
            self.recount(nya, STYLES_list_G0, STYLES_list_G1)
        elif start == 0:
            print('empty string')
            #self.recount_empty_line()
            self.recount_some_line(type16=999)
        elif text[0] == self.reversal_post_processor.comment_start:
            ax = len(text)
            self.setFormat(0, ax, STYLES['comment'])
            self.recount_some_line(type16=999)
        else:
            nya = self.second_rule_regular_expression.match(text, 0)
            print('self.second_rule_regular_expression = ', self.second_rule_regular_expression)
            len_match = nya.capturedLength()
            if len_match != 0:
                self.unsorted_recount(nya, STYLES_list_G0, STYLES_list_G1)
            else:
                print('22 здесь проверяю')
                special_here, command_dict = self.special_rare_case(text, self.count)#G & M коды
                if special_here:
                    self.GM_current_list.append([self.count, command_dict])
                    self.recount_some_line(type16=1)
                else:
                    print('try text: ', text)
                    nya = self.rule_ax_vars.match(text, 0)
                    len_match = nya.capturedLength()
                    if len_match != 0:
                        self.unsorted_ax_vars_exps_match_count(nya, STYLES_list_G0, STYLES_list_G1)
                    #CAPturedShift, nya, type16 = self.IF_WHILE_rule_regular_expression_match(text)
                    #if CAPturedShift:#include vars
                    #    #self.WHILE_exp_colors(nya)
                    #    self.recount_some_line(type16=4)
                    else:
                        print('axis vars rule = ', self.rule_ax_vars)
                        CAPturedShift, nya, type16 = self.IF_WHILE_rule_regular_expression_match(text)
                        if CAPturedShift:  # include vars
                            self.recount_some_line(type16=4)
                        #nya = self.rule_ax_vars.match(text, 0)
                        #len_match = nya.capturedLength()
                        #if len_match != 0:
                        #    self.unsorted_ax_vars_exps_match_count(nya, STYLES_list_G0, STYLES_list_G1)
                        else:
                            nya = self.SUBprogram_mask.match(text, 0)#todo перенесено в IF_WHILE
                            len_match = nya.capturedLength()
                            print(f'первично поймал')
                            print(f'self.sub_programs2 = ', self.sub_programs)
                            #for pp in range(15):
                            #   print('M98 {} = |{}|'.format(pp, nya.captured(pp)))
                            if len_match != 0 and nya.captured(6).lower() in self.sub_programs:
                                print('99 text {} match'.format(text))
                                self.color_and_feed_SHIFT_subprograms(nya)
                                self.recount_some_line(type16=4)#todo 4, вообще это временно, пока операция не является ПЕРЕХОДом
                            else:
                                print('ERROR LINE {}: {}'.format(self.count, text))
                                self.recount_some_line(type16=6)

        #print(f'999 self.current_g_cod_pool[self.count] = {self.current_g_cod_pool[self.count-1]}')

    def color_and_feed_SHIFT_subprograms(self, nya):
        #print(f'656 nya.captured(5) = {nya.captured(6)}')
        ax = len(nya.captured(2))
        start = len(nya.captured(1))
        self.setFormat(start, ax, STYLES_list_G1[0])
        start = start + ax
        ax = len(nya.captured(4))
        self.setFormat(start, ax, STYLES['label'])
        start = start + ax

        ax = len(nya.captured(5))
        self.setFormat(start, ax, STYLES['if_while'])
        start = start + ax
        ax = len(nya.captured(6))

        self.setFormat(start, ax, STYLES['if_while'])
        start = start + ax
        ax = len(nya.captured(7))
        self.setFormat(start, ax, STYLES['R = '])
        start = start + ax
        #if add_:
        type_OP = 33
        self.current_SHIFT_list.append([self.count, type_OP, nya])
        #else:
        #    type_OP = 35

        i_ = 8

        if nya.captured(i_) != '' and nya.captured(i_)[0] in ['(', ';']:  # comments
            ax = len(nya.captured(i_))
            start = len(nya.captured(0)) - ax
            self.setFormat(start, ax, STYLES['comment'])
            # start = start + ax



    def reset_current_containers(self):
        self.current_XYZvars_dict = {}
        self.current_SHIFT_list = []
        self.GM_current_list = []

    def unsorted_ax_vars_exps_match_count(self, nya, STYLES_list_G0, STYLES_list_G1):
        print('unsorted_ax_vars_exps_match')
        for pp in range(92):
            print('unsorted_ax_vars_exps_match_coun {} = {}'.format(pp, nya.captured(pp)))
        self.current_g_cod_pool[self.count][0] = nya.captured(2) or None
        # label = nya.captured(3)
        self.current_g_cod_pool[self.count][1] = nya.captured(6) or None  # +1
        if nya.captured(4)[0:2] == 'G4':
            self.current_g_cod_pool[self.count][1] = nya.captured(6) or None
            self.current_g_cod_pool[self.count][2] = nya.captured(8) or None
            G40_first = True
        else:
            self.current_g_cod_pool[self.count][1] = nya.captured(8) or None
            self.current_g_cod_pool[self.count][2] = nya.captured(6) or None
            G40_first = False
        if np.isnan(self.current_g_cod_pool[self.count][2]):#+0
            self.current_g_cod_pool[self.count][3] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][2]
            self.current_g_cod_pool[self.count][3] = self.previous_block_g

        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        n = 1#N
        ax = len(nya.captured(n))

        if ax != 0:
            self.setFormat(start, ax, stile[0])#N
            start = start + ax

        n = n + 2 + 1
        ax = len(nya.captured(n))#label

        #print('это не то i = {}? {}'.format(n, nya.captured(n)))
        if ax != 0:
            print("STYLES['label'] on")
            type_OP = 41 #todo 41?????
            self.current_SHIFT_list.append([self.count, type_OP, nya])
            self.setFormat(start, ax, STYLES['label'])
            start = start + ax
            #return

        n = n + 1 #here + 1
        ax = len(nya.captured(n))

        if G40_first:
            if ax != 0:
                self.setFormat(start, ax, stile[1])#G40 todo
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            if ax != 0:
                self.setFormat(start, ax, stile[2])#G1
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            n = n + 1
        else:
            if ax != 0:
                self.setFormat(start, ax, stile[2])#G1
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            if ax != 0:
                self.setFormat(start, ax, stile[1])#G40 todo
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            n = n + 1

        #еще не радактировал
        #n = n + 1
        #code = 0b00000

        #for pp in range(40):
        #    print('unsorted_ax_vars_exps_match_coun {} = {}'.format(pp, nya.captured(pp)))

        while nya.captured(n) != '' and n < 40:#вероятно, избыточное условие
            i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)#, add=1
            start = start + ax
            n = n + 6
            ax = len(nya.captured(n-1))

        n = 46
        ax = len(nya.captured(n-1))

        while nya.captured(n) != '' and n < 59:#вероятно, избыточное условие
            i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)#, add=1
            print('что здесь делать: ', nya.captured(n))
            start = start + ax
            n = n + 6
            ax = len(nya.captured(n-1))


        #51 52 53 54
        ax = len(nya.captured(63))#R
        n = 64
        i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)
        print(f'R colored at {start}, ax = {ax}')

        start = start + ax
        ax = len(nya.captured(69))#AR
        n = 70
        i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)

        start = start + ax
        ax = len(nya.captured(75))#AP
        n = 76
        print(f'colorize: start = {start}, ax = {ax}')
        i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)

        start = start + ax
        ax = len(nya.captured(81))#RP
        n = 82
        i = self.nesting_axis_ijk_f_vars(n, nya, start, ax, stile)

        start = start + ax
        ax = len(nya.captured(87))#F #69
        i = 13
        print(f'F colored at {start}, ax = {ax}')
        self.setFormat(start, ax, stile[i])

        start = start + ax
        ax = len(nya.captured(90))#Comments
        #print(f'comms colored at {start}, ax = {ax}')
        self.setFormat(start, ax, STYLES['comment'])
        if n > 9:
            self.current_XYZvars_dict[self.count] = nya
        self.recount_some_line(type16=7)

    def IF_WHILE_rule_regular_expression_match(self, text):
        print(f'IF_WHILE_rule_regular_expression_match ')
        CAPturedShift = False
        nya = None
        type16 = 4
        for IFwhileRULE in self.SHIFT_masks:
            nya = IFwhileRULE.match(text, 0)
            len_match = nya.capturedLength()
            if len_match > 0:
                # todo здесь запись в контейнер переходов. ещё метки добавить
                #if text[0] == self.reversal_post_processor.comment_start:
                #    #type16 = self.SHIFT_masks[DICTshiftsINT['LABEL']]#TODO comment wil be 100???!
                #    nya = self.SHIFT_masks.match(text, 0)
                #    #self.WHILE_exp_colors(nya)
                #    #CAPturedShift = True
                #    #break
                #else:
                if self.SHIFT_masks[IFwhileRULE] == DICTshiftsINT['R = ']:
                    print(f'ПЕРЕМЕННАЯ ОБНАРУЖЕНА')
                    type16 = 3#it temporally need for right colors
                self.current_SHIFT_list.append([self.count, self.SHIFT_masks[IFwhileRULE], nya])
                self.WHILE_exp_colors(nya)
                CAPturedShift = True
                print('IFwhileRULE = ', IFwhileRULE)
                print(f'А тут что? : {self.SHIFT_masks[IFwhileRULE]}')
                break
        print(f'IF_WHILE_rule_regular_expression_match returns: text = {text}, res: {CAPturedShift}')
        return CAPturedShift, nya, type16

    #def non_universal_operators(self, nya):
    #    for i_ in range(50):
    #       print('N_U_O: nya[{}] = |{}|'.format(i_, nya.captured(i_)))
    #    ax = len(nya.captured(2))
    #    start = len(nya.captured(1))
    #    self.setFormat(start, ax, STYLES_list_G1[0])
    #    start = start + ax
    #    ax = len(nya.captured(4))
    #    self.setFormat(start, ax, STYLES['label'])
    #    start = start + ax




    def recount_some_line(self, type16):
        self.current_g_cod_pool[self.count][3] = self.previous_block_g
        self.current_g_cod_pool[self.count][16] = type16
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            #self.base.progress_bar.blockSignals(True)
            self.base.on_count_changed(self.count)  # progressBar
            #self.progress_bar.blockSignals(False)

        return

    def WHILE_exp_colors(self, nya):#IF [1000>1] error not here
        #todo добавить комментарии в конце
        #if self.current_SHIFT_list[-1][1] == DICTshiftsINT['SUB_PROGRAM']:# and nya.captured(6).lower() in self.sub_programs:
        #    print(f'66 self.current_SHIFT_list[-1][1] = {self.current_SHIFT_list[-1][1]}')
        #    self.color_and_feed_SHIFT_subprograms(nya)
        #    return
        for i_ in range(45):
            print('55 nya[{}] = |{}|'.format(i_, nya.captured(i_)))
        if self.current_SHIFT_list[-1][1] == DICTshiftsINT['SUB_PROG_START']:#todo for siemens at least
            #своё правило раскрашивания!!!
            #print('color for SUB_PROG_START')
            ax = len(nya.captured(2))
            start = len(nya.captured(1))
            self.setFormat(start, ax, STYLES_list_G1[0])
            start = start + ax
            ax = len(nya.captured(4))
            self.setFormat(start, ax, STYLES['label'])
            start = start + ax

            ax = len(nya.captured(5))
            self.setFormat(start, ax, STYLES['if_while'])
            start = start + ax
            #ax = len(nya.captured(6))
            #start = start + ax
            ax = len(nya.captured(7))
            self.setFormat(start, ax, STYLES['R = '])
            #type_OP = 35

            start = start + ax
            ax = len(nya.captured(8))
            self.setFormat(start, ax, STYLES['comment'])
            return

        ax = len(nya.captured(2))
        start = len(nya.captured(1))
        self.setFormat(start, ax, STYLES_list_G1[0])


        start = start + ax
        ax = len(nya.captured(4))
        self.setFormat(start, ax, STYLES['label'])
        start = start + ax
        if self.current_SHIFT_list[-1][1] == DICTshiftsINT['R = ']:
            ax = len(nya.captured(5))
            self.setFormat(start, ax, STYLES['R = '])

            start = start + len(nya.captured(9)) + ax
            #print('start = ', start)
            #print(f'start here = {start - len(nya.captured(7)) - len(nya.captured(6))}')
            self.setFormat(start - len(nya.captured(7)) - len(nya.captured(6)) - len(nya.captured(9)), len(nya.captured(6)), STYLES['condition'])

            ax = len(nya.captured(10))
            self.setFormat(start, ax, STYLES['condition'])
            #start = start + len(nya.captured(9)) + ax
            start = start + ax
            ax = len(nya.captured(11))
            self.setFormat(start, ax, STYLES['comment'])

        elif self.current_SHIFT_list[-1][1] == DICTshiftsINT['M30']:
            ax = len(nya.captured(5))
            self.setFormat(start, ax, STYLES['if_while'])
            start += ax
            ax = len(nya.captured(6))
            self.setFormat(start, ax, STYLES['comment'])


        elif self.current_SHIFT_list[-1][1] in self.reversal_post_processor.OPs_with_different_rules:
            print('reverse isk ', self.reversal_post_processor.OPs_with_different_rules)
            self.reversal_post_processor.OPs_with_different_rules[self.current_SHIFT_list[-1][1]][0](self, nya, start)
        else:
            #here will be a cycle
            for i_ in range(5, 11, 2):
                ax = len(nya.captured(i_))
                self.setFormat(start, ax, STYLES['if_while'])
                start = start + ax
                ax = len(nya.captured(i_ + 1))
                self.setFormat(start, ax, STYLES['condition'])
                start = start + ax
            if nya.captured(i_) != '' and nya.captured(i_)[0] in ['(', ';']:#comments
                ax = len(nya.captured(i_))
                start = start - ax
                self.setFormat(start, ax, STYLES['comment'])
                #start = start + ax



    def special_rare_case(self, text, count):#todo вышибло на Ctrl+Zб при не прочитываемой строке
        #todo после изменений в: CASE (R1) OF 1 GOTOB LB11 2 GOTOF LB22 GOTOF ENDLBL1 DEFAULT GOTOF ENDLBL1
        #G28 U0. V0.
        print('special_rare_case')
        #result, command_dict = self.reversal_post_processor.check_command(self, text, self.current_g_cod_pool[count], count,self.base.g_modal)
        result, command_dict = self.reversal_post_processor.check_command(self, text, self.current_g_cod_pool[count], count, g_modal=None)
        if result:#todo это не тот g_modal
            #self.current_g_cod_pool[self.count][16] = 1
            #print('self.current_g_cod_pool[self.count][16] = 1')
            #print('true55')
            return True, command_dict
        else:
            self.current_g_cod_pool[self.count][16] = 9997
            #print('false55')
            return False, command_dict

        #print('self.start_pointXYZ = ', self.reversal_post_processor.start_pointXYZ)


    def recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        #print('recount nay = ', nya.captured(0))
        #for p in range(0, 45):
        #    print('nya.captured({}) = {}'.format(p, nya.captured(p)))
        self.current_g_cod_pool[self.count, np.r_[0:15]] = [nya.captured(i) or None for i in self.list_number_captured_1]

        #nope. i need to use k anyway. better assign in solving
        #self.current_g_cod_pool[self.count, np.r_[17:20]] = self.current_g_cod_pool[self.count, np.r_[4:7]]

        #Заполнения здесь не происходит, так как оно только между numpy массивами
        #print('current_g_cod_pool == ', self.base.current_g_cod_pool[self.count])
        #G0-G3
        if np.isnan(self.current_g_cod_pool[self.count][3]):
            self.current_g_cod_pool[self.count][3] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][3]
            self.current_g_cod_pool[self.count, 2] = self.previous_block_g
        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        #colors
        # простая подсветка одним цветом
        # self.setFormat(index, len_match, self.simple_format)
        #полноценная подсветка
        i = 0
        ax = len(nya.captured(i * 2 + 1))
        start = 0
        #start = 0
        #print('||| here |||')
        #for o in range(16):
        #    print('nya ({}) ={}'.format(o, nya.captured(o)))
        while i < 14:#todo надо подумать. По идее надо добавлять +1 строку в style, но работало, вроде...
            if ax != 0:
                #print('takt ', i)
                self.setFormat(start, ax, stile[i])
            start = start + ax
            i = i + 1
            ax = len(nya.captured(i * 2 + 1))

        #print('recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)
        return

    def unsorted_recount(self, nya, STYLES_list_G0, STYLES_list_G1):
        print('unsorted_recount start')
        #поменять

        #for p in range(0, 45):
        #    print('nya.captured({}) = {}|'.format(p, nya.captured(p)))

        #for i in range(35):
        #    print('55 nya.captured({}) = {}'.format(i, nya.captured(i)))
        # G0-G3
        self.current_g_cod_pool[self.count][0] = nya.captured(2) or None
        #label = nya.captured(3)
        self.current_g_cod_pool[self.count][1] = nya.captured(6) or None#+1
        if nya.captured(4)[0:2] == 'G4':
            self.current_g_cod_pool[self.count][1] = nya.captured(6) or None
            self.current_g_cod_pool[self.count][2] = nya.captured(8) or None
            G40_first = True
        else:
            self.current_g_cod_pool[self.count][1] = nya.captured(8) or None
            self.current_g_cod_pool[self.count][2] = nya.captured(6) or None
            G40_first = False



        if np.isnan(self.current_g_cod_pool[self.count][2]):#+0
            self.current_g_cod_pool[self.count][3] = self.previous_block_g
        else:
            self.previous_block_g = self.current_g_cod_pool[self.count][2]
            self.current_g_cod_pool[self.count][3] = self.previous_block_g

        stile = STYLES_list_G0 if self.previous_block_g == 0 else STYLES_list_G1
        start = 0
        n = 1#N
        ax = len(nya.captured(n))

        if ax != 0:
            self.setFormat(start, ax, stile[0])#N
            start = start + ax

        n = n + 2 + 1
        ax = len(nya.captured(n))#label

        #print('это не то i = {}? {}'.format(n, nya.captured(n)))
        if ax != 0:
            #print("STYLES['label'] on")
            type_OP = 41
            self.current_SHIFT_list.append([self.count, type_OP, nya])
            self.setFormat(start, ax, STYLES['label'])
            start = start + ax
            #return

        n = n + 1 #here + 1
        ax = len(nya.captured(n))

        if G40_first:
            if ax != 0:
                self.setFormat(start, ax, stile[1])#G40 todo
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            if ax != 0:
                self.setFormat(start, ax, stile[2])#G1
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            n = n + 1
        else:
            if ax != 0:
                self.setFormat(start, ax, stile[2])#G1
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            if ax != 0:
                self.setFormat(start, ax, stile[1])#G40 todo
                start = start + ax
            n = n + 2
            ax = len(nya.captured(n))
            n = n + 1

        #n = n + 1
        while nya.captured(n) != '' and  n < 26:#вероятно, избыточное условие nya.captured(n) != '' and
            #print('cheking {}'.format(n))
            self.nesting_axis_ijk(n, nya, start, ax, stile)#, add = 2
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))

        n = 28
        ax = len(nya.captured(n - 1))
        #тут проблемы
        while nya.captured(n) != '' and n < 38:#вероятно, избыточное условие nya.captured(n) != '' and
            #print('cheking {}'.format(n))
            self.nesting_axis_ijk(n, nya, start, ax, stile)#, add = 2
            start = start + ax
            n = n + 3
            ax = len(nya.captured(n-1))



        #n = 35

        n = 36
        ax = len(nya.captured(n))
        self.setFormat(start, ax, stile[12])
        numbeR = nya.captured(n + 1)
        self.current_g_cod_pool[self.count][13] = numbeR if numbeR != '' else None#todo Костыль
        #self.nesting_axis_ijk(n, nya, start, ax, stile)
        #add_fix = 0

        self.current_g_cod_pool[self.count][14] = nya.captured(39) or None#F #+add_fix
        ax = len(nya.captured(38))#+add_fix
        #print('self.current_g_cod_pool[self.count][14] = ', self.current_g_cod_pool[self.count][14])
        self.setFormat(start, ax, stile[13])
        start = start + ax
        #comment = nya.captured(40)
        ax = len(nya.captured(41))
        self.setFormat(start, ax, STYLES['comment'])
        #print('unsorted recount current_g_cod_pool again == ', self.current_g_cod_pool[self.count])
        self.count_in_step += 1
        self.count += 1
        if self.count_in_step == self.standart_step:
            self.base.on_count_changed(self.count)  # progressBar
            # QApplication.processEvents()
        return


    #def nestingIJK(self, n, nya, start, ax, stile):
    #    print('nestingIJK')
    #    add = 2
    #    symbol = nya.captured(n)
    #    if symbol == 'I':
    #        i = 7 + add
    #    elif symbol == 'J':
    #        i = 8 + add
    #    elif symbol == 'K':
    #        i = 9 + add
    #    else:
    #        print('Ты не должен сюда попасть, но вдруг 1')
    #        return
    #    self.setFormat(start, ax, stile[i])
    #    self.current_g_cod_pool[self.count][i+1] = nya.captured(n+1)


    def nesting_axis_ijk(self, n, nya, start, ax, stile):
        print('super nesting') #todo что то допилить для универсальных IJK
        add = 2
        symbol = nya.captured(n)
        R = self.reversal_post_processor.RIJK[0]
        #print(R)
        #print('||  symbol = ', symbol)

        if symbol == 'X':
            i = 1 + add
        elif symbol == 'Y':
            i = 2 + add
        elif symbol == 'Z':
            i = 3 + add
        elif symbol == 'C':
            i = 6 + add
        elif symbol == 'B':
            i = 5 + add
        elif symbol == 'A':
            i = 4 + add
        elif symbol == R or symbol == 'CR=':#'R' todo подкрутить для сименса и тд
            i = 10 + add

        elif symbol == 'I':
            i = 7 + add
        elif symbol == 'J':
            i = 8 + add
        elif symbol == 'K':
            i = 9 + add
        else:
            print('Ты не должен сюда попасть, но вдруг')
            print('symbol = ', symbol)
            return
        self.setFormat(start, ax, stile[i])
        #print(f'setFormat {symbol}: start = {start}, ax = {ax}, ')
        self.current_g_cod_pool[self.count][i+1] = nya.captured(n+1)

    def nesting_axis_ijk_f_vars(self, n, nya, start, ax, stile):
        print('super nesting vars') #todo что то допилить для универсальных IJK
        add = 2
        symbol = nya.captured(n).replace(" ", "")
        #ddd= 'dfdf'.sp
        #print(f'||  symbol = |{symbol}|')
        if symbol == 'X' or symbol == 'RP=':
            i = 1 + add
        elif symbol == 'Y':
            i = 2 + add
        elif symbol == 'Z':
            i = 3 + add
        elif symbol == 'C':
            i = 6 + add
        elif symbol == 'B':
            i = 5 + add
        elif symbol == 'A':
            i = 4 + add
        elif symbol == 'R' or symbol == 'CR=' or symbol == 'AR=' or symbol == 'AP=':#todo подкрутить для сименса и тд
            i = 10 + add
        elif symbol == 'I':
            i = 7 + add
        elif symbol == 'J':
            i = 8 + add
        elif symbol == 'K':
            i = 9 + add
        elif symbol == 'F':
            i = 13
            #print('F = ', nya.captured(n + 1))
            #self.current_g_cod_pool[self.count][i + 1] = nya.captured(n + 1)
        else:
            print('Ты не должен сюда попасть, но вдруг')
            print('symbol = ', symbol)
            return
        self.setFormat(start, ax, stile[i])
        return i - add

    def to_the_start(self):
        self.standart_step = 1
        self.count = 0
        self.base.progress_bar.blockSignals(True)
        self.base.progress_bar.setMaximum(1)
        self.base.progress_bar.blockSignals(False)
        print("the end1")