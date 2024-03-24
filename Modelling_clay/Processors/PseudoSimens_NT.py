
from Modelling_clay.Processors.Processor_base.ReversPostProcessor_0 import ReversalPostProcessor0, format, STYLES, STYLES_list_G0, STYLES_list_G1
from PyQt5.QtCore import QRegularExpression
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT
from os import listdir
from os.path import isfile, join
#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.math_logic_expressions.postfix4tokens import string2postfix_tuple, tokensPostfixing



DICT_X_Y_Z_AP_RP = {'X': STYLES_list_G1[3], 'Y': STYLES_list_G1[4], 'Z': STYLES_list_G1[5], 'AP': STYLES_list_G1[12], 'RP': STYLES_list_G1[3]}


def REPEAT_LB_color(self, nya, start):
    print('REPEAT_color')
    ax = len(nya.captured(5))
    self.setFormat(start, ax, STYLES['if_while'])
    start = start + ax

    ax = len(nya.captured(7))
    self.setFormat(start, ax, STYLES['label'])
    start = start + ax

    ax = len(nya.captured(9))
    self.setFormat(start, ax, STYLES['label'])
    start = start + ax

    ax = len(nya.captured(11))
    self.setFormat(start, ax, STYLES['R = '])
    start = start + ax

    n = 14
    if nya.captured(n) != '':# and nya.captured(n)[0] == ';':  # comments
        ax = len(nya.captured(n))
        self.setFormat(start, ax, STYLES['comment'])
        start = start + ax



def REPEAT_LB_feed_dict(self, el, i, min_line, new_slice):
    #for pp in range(15):
    #    print(f'el[2].captured({pp}) = {el[2].captured(pp)}')
    fourth_token = None if el[2].captured(6) == '' else True
    lbl1 = el[2].captured(8)
    first_token = string2postfix_tuple(lbl1, self.brackets)
    lbl2 = el[2].captured(10)
    Pn = string2postfix_tuple(el[2].captured(12), self.brackets)
    third_tokens = string2postfix_tuple(lbl2, self.brackets) if lbl2 != '' else None
    return first_token, third_tokens, Pn, fourth_token, new_slice

def CYCLE800_color(self, nya, start):
    print('CYCLE800color')
    #np_line[16] = 1
    #pass
    for pp in range(25):
        print(f'el[2].captured({pp}) = {nya.captured(pp)}')
    start1 = nya.capturedStart(0)
    end1 = nya.capturedEnd(0)
    #nen [thyz]
    value = ['1', "", '0.', '57', '0.', '0.', '0.',' 0.', '0.', '0.', '0.', '0.', '0.', '1', '0.', '1']
    self.setFormat(start1, end1, STYLES_list_G1[0])
    #params: str = nya.captured(5)[1:-1]
    param_list = nya.captured(5)[1:-1].split(',')
    #last1 = nya.captured(6)
    #if last1[-1] == ',':
    #    last1 = last1[:-1]
    #param_list.append(last1)#todo учитывать ли мне возможную запятую после?
    start1 = nya.capturedStart(5)+1
    print('param ;ist = ', param_list)
    print('stert1 = ', start1)
    for n in range(len(param_list)):
        L = len(param_list[n])+1
        if L > 1:
            value[n] = param_list[n]
        if n%4 == 0:
            self.setFormat(start1, L, format('magenta', 'bold'))
        start1 += L

    #L = len(nya.captured(6)) #+ 1
    #if L > 1:
    #    value[n] = nya.captured(6)
    #if n % 4 == 0:
    #    self.setFormat(start1, L, format('magenta', 'bold'))
    #start1 += L

    self.setFormat(start1-0, 1, STYLES_list_G1[0])
    self.setFormat(start1, 300, format('gray', 'bold'))
    self.base.np_box.CYCLE800_for_reading = value
    print(f'валя равна ', value)
    print('here is the type = ', type(self.base.np_box))
    #key = 'CYCLE800'
    #return key, value

def CYCLE800_feed(self, el, i, min_line, new_slice, proc):
    print('CYCLE800_feed')
    print('2 here is the type = ', type(self))
    thirst_token =  'CYCLE800'#el[2].captured(6)# == '' else True
    dcit_axises = {}#{'X': None, 'Y': None, 'Z': None, 'AP': None, 'RP': None}
    for ddd in range(1, 17):#+1
        dcit_axises[ddd] = string2postfix_tuple(self.np_box.CYCLE800_for_reading[ddd-1], self.brackets, proc=proc)
    return thirst_token, dcit_axises, None, None, new_slice

def POLAR_color(self, nya, start):
    print('POLAR_color')
    #print('here is the type = ', type(self))
    #for pp in range(45):
    #    print(f'nya.captured({pp}) = {nya.captured(pp)}')
    ax = len(nya.captured(5))
    self.setFormat(start, ax, STYLES_list_G1[0])#G112
    #start = start + ax
    print(f'new start = {start}')

    for ddd in range(10, 19, 3):#1
        print('ddd = ', ddd)
        catched = nya.captured(ddd)
        start = start + ax
        ax = len(catched)
        if ax == 0:
            continue
        print(f'catched99 = {catched}')
        if catched in DICT_X_Y_Z_AP_RP:
            self.setFormat(start, ax, DICT_X_Y_Z_AP_RP[catched])
        start = start + ax
        print(f'new start1 = {start}')
        ax = len(nya.captured(ddd+1))
        self.setFormat(start, ax, STYLES['axis'])

        print(f'new start2 = {start}')
    print(f'new start3 = {start}')

    for ddd in range(20, 24, 3):#+1
        print('ddd2 = ', ddd)
        catched = nya.captured(ddd)
        start = start + ax
        ax = len(catched)
        print('9898 ax = ', ax)
        if ax == 0:
            continue

        if catched in DICT_X_Y_Z_AP_RP:
            print(f'catched = {catched}, and colored, start = {start}')
            self.setFormat(start, ax, DICT_X_Y_Z_AP_RP[catched])
        start = start + ax
        ax = len(nya.captured(ddd+1))
        self.setFormat(start, ax, STYLES['axis'])


    n = 25#+1
    if nya.captured(n) != '':# and nya.captured(n)[0] == ';':  # comments
        start = start + ax
        ax = len(nya.captured(n))
        self.setFormat(start, ax, STYLES['comment'])
        #start = start + ax

def POLAR_feed(self, el, i, min_line, new_slice, proc):
    print('POLAR_feed')
    #for pp in range(15):
    #    print(f'el[2].captured({pp}) = {el[2].captured(pp)}')
    thirst_token =  el[2].captured(6)# == '' else True
    dcit_axises = {}#{'X': None, 'Y': None, 'Z': None, 'AP': None, 'RP': None}
    for ddd in range(10, 19, 3):#+1
        ax1 = el[2].captured(ddd)
        dcit_axises[ax1] = string2postfix_tuple(el[2].captured(ddd+1), self.brackets, proc=proc)
    for ddd in range(20, 24, 3):
        ax1 = el[2].captured(ddd)
        dcit_axises[ax1] = string2postfix_tuple(el[2].captured(ddd+1), self.brackets, proc=proc)
    if '' in dcit_axises:
        dcit_axises.pop('')
    return thirst_token, dcit_axises, None, None, new_slice



def CASE_color(self, nya, start):
    ax = len(nya.captured(5))
    self.setFormat(start, ax, STYLES['if_while'])
    start = start + ax

    ax = len(nya.captured(6))
    self.setFormat(start, ax, STYLES['condition'])
    start = start + ax

    ax = len(nya.captured(7))  # OF
    self.setFormat(start, ax, STYLES['if_while'])
    start = start + ax

    for n in range(9, 47, 6):  # 9 + 7*6 + 1
        print('psshh n = ', n)
        ax = len(nya.captured(n))  # empty
        start = start + ax
        ax = len(nya.captured(n + 1))  # CASE I
        self.setFormat(start, ax, STYLES['R = '])
        start = start + ax
        ax = len(nya.captured(n + 2))  # GOTO
        self.setFormat(start, ax, STYLES['if_while'])
        start = start + ax
        ax = len(nya.captured(n + 4))  # OF
        self.setFormat(start, ax, STYLES['label'])
        start = start + ax

    n = n + 6
    ax = len(nya.captured(n))  # DEFAULT
    self.setFormat(start, ax, STYLES['if_while'])
    start = start + ax
    ax = len(nya.captured(n + 1))  # GOTOF
    self.setFormat(start, ax, STYLES['if_while'])
    start = start + ax
    ax = len(nya.captured(n + 3))
    self.setFormat(start, ax, STYLES['label'])
    start = start + ax
    n = n + 1
    if nya.captured(n) != '' and nya.captured(n)[0] == '(':  # comments
        ax = len(nya.captured(n))
        start = start - ax
        self.setFormat(start, ax, STYLES['comment'])

dict_for_GOTO_inCASE = {'': DICTshiftsINT['GOTO'], 'F': DICTshiftsINT['GOTOF'], 'B': DICTshiftsINT['GOTOB'], 'C': DICTshiftsINT['GOTOC'], 'S': DICTshiftsINT['GOTOS']}


def CASE_feed_dict(self, el, i, min_line, new_slice):#,
    list_exp = [el[2].captured(6), *[el[2].captured(n) for n in range(10, 47, 6)]]
    for i in range(len(list_exp)):
        list_exp[i] = string2postfix_tuple(list_exp[i], self.brackets) if list_exp[i] != '' else None
    list_GOTO = [*[el[2].captured(n) for n in range(12, 49, 6)], el[2].captured(53)]
    list_GOTO = [*[el[2].captured(n) for n in range(12, 49, 6)], el[2].captured(53)]
    list_GOTO = [dict_for_GOTO_inCASE[list_GOTO[i]] for i in range(len(list_GOTO))]
    list_lbl = [*[el[2].captured(n) for n in range(13, 50, 6)], el[2].captured(54)]
    fourth_token = None

    print('list_lbl  = ', list_lbl)
    third_tokens = [string2postfix_tuple(list_lbl[n], self.brackets) if list_lbl[n] != '' else None for n in range(len(list_lbl))]
    print(f'дичь first_tokens = {third_tokens}')
    return list_exp, list_GOTO, third_tokens, fourth_token, new_slice



class PseudoSimensNT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self, redactor):#*args, **kwargs
        super().__init__(redactor)
        #self.siemens_ijk = True
        """ this is Siemens turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as a part, order matters
        """
        #self.k_XYZABC['X'] = 0.5
        #self.ABC_HEAD[2] = False#ax Z belong to table or spindle
        #print('self.k_XYZABC = ', self.k_XYZABC)
        self.CNC_op_type = 'Siemens_op'
        self.update_rules()
        self.brackets = ['(', ')', '[', ']']

        #self.ABC_turning_Zero['A'] =
        #print('k_XYZABC_list = ', self.k_XYZABC_list)
        #n_number = r'^\s*N(\d*)\s*'#херня какая то
        #cycle800_str = r'([^,]*,){8,15}' + r'([^,]*)'
        self.special_commands = [
                                [r'\s*G(1[789])\s*', self.change_plane, format('blue', 'bold')],
                                [r'G28\s*(([UVW])\s*0.?\s*)(([UVW])\s*0.?\s*)?(([UVW])\s*0.?\s*)?;?$', self.G28_U0_V0_W0, format('red', 'bold')],
                                [r'\s*G(9[01])\s*', self.absolut_and_reference_coord_G90_G91, format('blue', 'bold')],
                                [r'\s*(G\s*(5[456789]))(\s|$|[a-zA-Z])', self.G54_G59, format('blue', 'bold')],
                                #[r'^\s*N(\d*)\s*', self.N_number, format('blue', 'bold')],
                                #[r'^\s*(G1((1[012])))\s*', self.polar_coord_G112, format('pink', 'bold')],
                                [r'\s*CYCLE800\(\)\s*', self.cancel_CYCLE800, format('blue', 'bold')],
                                 ]
        for i in range(0, len(self.special_commands)):
            self.special_commands[i][0] = QRegularExpression(self.special_commands[i][0])
            #look Perl RegularExpressions if u need
        #\d{16}(,\d{16})
        print('self.special_commands = ', self.special_commands)

    # check_command(self, text, np_line, g_modal)

    #def N_number(self, lineBlock, nya, np_line, count, g_modal, i):
    #    start1 = nya.capturedStart(0)
    #    end1 = nya.capturedEnd(1)
    #    lineBlock.setFormat(start1, end1, self.special_commands[i][2])

    def sub_programs(self):
        main_address = 'Modelling_clay/Processors/Processor_base/Siemens_subprograms/'
        catalog = [main_address + '_N_SPF_DIR', main_address + '_N_CUS_DIR', main_address + '_N_CMA_DIR', main_address + '_N_CST_DIR']
        sub_program_names = {}
        # sub_program_names.
        for cat in reversed(catalog):
            f_c = [f for f in listdir(cat) if isfile(join(cat, f))]
            if len(f_c) > 0:
                for f1 in f_c:
                    if f1.endswith('.spf') or f1.endswith('.mpf'):
                        sub_program_names[f1[:-4].lower()] = cat + '/' + f1
                        sub_program_names[f1[:-4].lower() + '_' + f1[-3:].lower()] = cat + '/' + f1
        # i did not add _N_name in sub_program_names. too much combinations. i don't really care. if u have :"_N_name" from machine, then use "_N_name" in your code too
        print('sub_program_names = ', sub_program_names)
        return sub_program_names


    def G54_G59(self, lineBlock, nya, np_line, count, g_modal, i):
        #print('SC was noted')
        np_line[16] = 1
        SC = nya.captured(2)
        start1 = nya.capturedStart(1)
        #self.redactor.g_modal.insert_in_main_gmodal('SC', count + self.redactor.editor.min_line_np, SC)#todo убрать???!
        lineBlock.setFormat(start1, len(nya.captured(1)), self.special_commands[i][2])
        #return True
        key = 'SC'
        value = nya.captured(2)
        return key, value
        #return True

    def change_plane(self, lineBlock, nya, np_line, count, g_modal, i):#todo позже подстроить под N10
        print('plane change')
        np_line[16] = 1
        plane = nya.captured(1)
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(1)
        #self.redactor.g_modal.insert_in_main_gmodal('plane', count+self.redactor.editor.min_line_np, plane)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])
        key = 'plane'
        value = plane
        return key, value



    def G28_U0_V0_W0(self, lineBlock, nya, np_line, count, g_modal, i):
        start_pointXYZ = self.redactor.current_machine.offset_pointXYZ
        np_line[2] = 0
        np_line[3] = 0
        np_line[16] = 0#zero group of commands mean that point should be paint directly
        f = [nya.captured(2), nya.captured(4), nya.captured(6)]#4
        for i1 in f:
            if i1 == 'U':
                np_line[4] = start_pointXYZ[0]
            elif i1 == 'V':
                np_line[5] = start_pointXYZ[1]
            elif i1 == 'W':
                np_line[6] = start_pointXYZ[2]
            #elif i1 == 'A super':  np_line[7] = self.start_pointXYZ[3]
        lineBlock.setFormat(0, len(nya.captured(0)), self.special_commands[i][2])
        key = 'G28'
        value = None
        return key, value

    def absolut_and_reference_coord_G90_G91(self, lineBlock, nya, np_line, count, g_modal, i):
        print('G90_91')
        np_line[16] = 1
        ABS_ref = nya.captured(1)
        #self.redactor.g_modal.insert_in_main_gmodal('absolute_or_incremental', count + self.redactor.editor.min_line_np, ABS_ref)
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(1)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])
        key = 'absolute_or_incremental'
        value = ABS_ref
        return key, value
        #вставить в

    def cancel_CYCLE800(self, lineBlock, nya, np_line, count, g_modal, i):
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(0)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])
        return 'CYCLE800', None

    #def polar_coord_G112(self, lineBlock, nya, np_line, count, g_modal, i):
    #    print('polar coord')
    #    np_line[16] = 1
    #    POLAR_ON_OFF = nya.captured(1)[1:]
    #
    #    #self.redactor.g_modal.insert_in_main_gmodal('polar_coord', count + self.redactor.editor.min_line_np, POLAR_ON_OFF)
    #    start1 = nya.capturedStart(0)
    #    lineBlock.setFormat(start1, len(nya.captured(0)), self.special_commands[i][2])
    #    key = 'polar'
    #    value = POLAR_ON_OFF
    #    print('kkk = ', value)
    #    return key, value


    def update_rules(self):
        """Синтаксические маркеры для языка. """
        # G-func
        # g_cod = ['G0', 'G1', 'G2', 'G3']
        # axises
        # todo perl выражения должны заимствоваться из псведопостпроцессора
        #axises0 = self.AXISnames
        self.RIJK[0] = 'CR\s*='
        R, I, J, K = self.RIJK
        print('rijk = ', R, I, J, K)

        self.comment_braces = ['((;.*))?']
        self.comment_start = ';'
        #self.OPs_with_different_rules = {DICTshiftsINT['CASE']: [CASE_color, CASE_feed_dict],
        #                                 DICTshiftsINT['REPEAT_LB']: [REPEAT_LB_color, REPEAT_LB_feed_dict],
        #                                 DICTshiftsINT['POLAR']: [POLAR_color, POLAR_feed]}

        self.OPs_with_different_rules = {DICTshiftsINT['CASE']: [CASE_color, CASE_feed_dict],
                                         DICTshiftsINT['REPEAT_LB']: [REPEAT_LB_color, REPEAT_LB_feed_dict],
                                         DICTshiftsINT['POLAR']:[POLAR_color, POLAR_feed],
                                         DICTshiftsINT['CYCLE800']: [CYCLE800_color, CYCLE800_feed]}
        axises = ['X', 'Y', 'Z', 'A', 'B', 'C', I, J, K, R]  # - , 'G', 'F'
        g_prefix = r'(G0?([0123])\s*)?'
        f_postfix = r'(F\s*(\d+.?\d*\s*))?'#todo вопрос: а не должен ли "?" стоять в конце?
        NumberN = r'(N(\d+)\s*)?'
        Corrector = r'(G(4[012])\s*)?'
        i_postfix = '(' + I + r'(\d+.?\d*))?\s*'#todo сейчас только R реализован для несортированного варианта
        j_postfix = '(' + J + r'(\d+.?\d*))?\s*'
        k_postfix = '(' + K + r'(\d+.?\d*))?\s*'
        # = '(' + '({})'.format(R) + r'(-?\d+.\d*)\s*)?'
        r_postfix = '(' + R + r'(-?\d+.?\d*)\s*)?'
        #r_postfix = '(' + f'(?:{R})|(?:AR\s*=))'  + r'(-?\d+.?\d*)\s*)?'
        #ar_postfix = '(' + 'AR' + r'(-?\d+.?\d*)\s*)?'
        # most strings look like 'main_rule'

        sorted_axis_rule = ''
        for letter in axises:
            sorted_axis_rule += r'(\s*(?:{})(-?\d+\.?\d*)\s*)?'.format(letter)
            # sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)

        self.sorted_axis_rule = '^' + NumberN + Corrector + g_prefix + sorted_axis_rule + f_postfix + ';?$'  # '(?:G0?\d)?\s*'   + f_postfix

        # sorted_axis_rule = r'^(?:X)(\d)$'  # UDALIT

        #axises_str = ''.join(axises0)
        X = 'X';        Y = 'Y';        Z = 'Z';        A = 'A';        B = 'B';        C = 'C'
        main_axises = ''.join([X, Y, Z, A, B, C])#R,

        axises_coord = r'(\s*([{}])\s*(-?\d+\.?\d*)\s*)?'.format(main_axises)
        #axises_coord.replace(R, '({})'.format(R))
        #print('111 axises_coord = ', axises_coord)
        ijk_str = I + J + K

        ijk_coord = r'(([{}])\s*(-?\d+\.?\d*)\s*)?'.format(ijk_str)
        # unsorted_axis_rule = r'(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)#r'^\d((?:X)(-?\d+\.\d*)\s*)$'

        unsorted_axis_rule = axises_coord * 6 + ijk_coord * 3
        #unsorted_axis_rule = axises_coord * 10

        Corrector_g_prefix_unsorted = '(([^;\)\(]*:\s*))?' + r'(\s*G(0?[0123]|4[012])\s*)?' * 2  # (\s*) добавил вначале

        #unsorted_axis_rule = NumberN + Corrector + g_prefix + unsorted_axis_rule + r_postfix + f_postfix
        unsorted_axis_rule = NumberN + Corrector_g_prefix_unsorted + unsorted_axis_rule + r_postfix + f_postfix
        self.unsorted_axis_rule = '^' + unsorted_axis_rule + ';?$'
        print('unsorted_axis_rule = ', self.unsorted_axis_rule)


        #sample = r'(([{}])\s*((-?\s*\d+\.\d*)|(-?\s*#\d+)|(-?\s*\[[^\]]*\]))\s*)?'
        #sample = r'(([{}])(\s*(=?-?\s*\d+\.?\d*)|(=\s*-?\s*R\d+)|(=\s*-?\s*\s*[^XYZABCIJKF]*))\s*)?'#TODO что делать то!!!!!
        sample = r'(([{}])(\s*(=?-?\s*\d+\.?\d*)|(=\s*-?\s*R\d+)|(\s*=\s*-?\s*[^;]*?))\s*)?'  # (?:=)
        #[^ABCXYZIJKF]
        ax_vars = sample.format(main_axises)
        unsorted_rule_ax_vars_ = ax_vars * 6  # r'\s*' +
        ijk = sample.format('IJK')
        #ar_postfix = '
        add_R_AR = r'(({}\s*)(\s*-?(\d+\.?\d*)|(R\d+)|([^;]*?))\s*)?'#7*()

        addR = add_R_AR.format(R)

        #addR   = r'(({}\s*)\s*(-?(\d+\.?\d*)|(R\d+)|(.*))\s*)?'.format(R)
        #add_AR = r'(({}\s*)\s*(-?(\d+\.?\d*)|(R\d+)|(.*))\s*)?'.format('AR\s*=')
        add_AR = add_R_AR.format('AR\s*=')
        add_AP = add_R_AR.format('(?:A|R)P\s*=')
        #add_RP = add_R_AR.format('AP|RP\s*=')
        unsorted_rule_ax_vars_ = unsorted_rule_ax_vars_ + ijk*3 + addR + add_AR + 2*add_AP #+ add_RP#u cn't change amount of bracers:(,).

        #unsorted_rule_ax_vars_ = unsorted_rule_ax_vars_ + ijk*3 + r'(({})\s*(-?(\d+\.\d*)|(#\d+)|(\[[^\]]*\]))\s*)?'.format(R)
        #НЕ ВЕРНО ФУРЫЧИТ
        print('unsorted_rule_ax_vars_ = ', unsorted_rule_ax_vars_)
        unsorted_rule_ax_vars_ = '^' + NumberN + Corrector_g_prefix_unsorted + unsorted_rule_ax_vars_ + f_postfix + self.comment_braces[0] + ';?$'
        #unsorted_rule_ax_vars_ = 'some_bullshit'
        self.unsorted_rule_ax_vars = unsorted_rule_ax_vars_
        self.assemble_tools_register()
        self.sub_programs_static = self.sub_programs()
        print(f'222 sub_programs_static = {self.sub_programs_static}')

        self.MATH_operators()
        self.SHIFT_operators()

    def SHIFT_operators(self):

        #'GOTO': 14,
        #'GOTOC': 15,  # GOTO without error
        #'GOTOS': 16,  # to start of the program
        #'GOTOB': 17,  # backward direction
        #'GOTOF': 18,  # forward direction
        ## 'REPEAT_LB':    19,
        #'R = ': 30,
        #'LABEL': 40
        #self.label = '^(.*):/s*$'

        NumberN = r'(N(\d+)\s*)?'
        # starts = '^(\s*)' + NumberN
        starts = '^(\s*)' + NumberN
        #ends = '(\(.*\))?\s*$'  # todo or ;
        ends = '(;.*)?$'  # todo or ;
        #print('this is happened 22')
        Label = '([^;\(\)]*:\s*)?'#TODO
        #Label = '(PPPPP)?'
        #print(f'tutochki {Label}')
        long_starts = starts + Label
        # todo временно для сименса
        self.label = long_starts

        #last_part = '([^\{}]*)'.format(self.brackets[2])
        last_part = '([^;]*)'
        p = '([^GOTO]+)'  # )|(DEFAULT)

        # p = '(.*)'
        # это всё неверно конечно
        of_goto = '(' + '(\s+)' + '(\d+)' + '(\s*GOTO([FBCS])?\s*)' + p + ')?'

        case_default_str = '(' + '(DEFAULT)' + '(\s*GOTO([FBCS])?\s*)' + '([^;]+)' + ')?'
        # case_default_str = '(.*)'

        # case_str = '(CASE\s*)' + '\((.*)\)'+ '(OF\s*) ' + '(.*)'# of_goto#*5 + case_default_str

        case_str = '(CASE\s*)' + '(\(.*\))' + r'(\s*OF)' + of_goto * 7 + case_default_str  # + '(.*)'       \t*
        forbid_XYZABC = '[^XYZABCFR]\s*=-s*'
        #todo временно для сименса

        one_var = '(\([^;]+\)'
        #center_sub_in_main = '(\w*)\s*{})?\s*'.format(one_var)
        center_sub = '(\w*)\s*{})?\s*'.format(one_var)#для сименса сейчас subr1 и subr2(x=2, z=8)
        #sub_start_ = '(^)?' if self.redactor is None else 'INACHE11'
        print(f'323self.redactor  = {self.redactor.tab_.currentWidget() }')
        #print(f'sub_start_ = {sub_start_}')
        cycle800_str = r'([^,]*,){8,15}' + r'([^,]*)'
        #r'\s*CYCLE800(\({}\))\s*'.format(cycle800_str)
        SHIFT_masks = {#отдельно сделать переменные и метки
            #long_starts + '(IF)' + '(.*)' + '(THEN)' + last_part + ends: DICTshiftsINT['IF_THEN'],
            long_starts + '(IF)' + '(.*)' + '(GOTOF)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            long_starts + '(IF)' + '(.*)' + '(GOTOB)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            long_starts + '(IF)' + '(.*)' + '(GOTOC)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            long_starts + '(IF)' + '(.*)' + '(GOTOS)' + last_part +         ends: DICTshiftsINT['IF_GOTO'],
            long_starts + '(IF)' + '(.*)' + '(GOTO)'   + last_part +     ends: DICTshiftsINT['IF_GOTO'],
            long_starts + '(IF)' + '(.*)' +                                 ends: DICTshiftsINT['IF'],
            #long_starts + '(ELIF)'  + '(.*)' + '(GOTO)' + last_part +       ends: DICTshiftsINT['ELIF'],#todo в исменс не надо, в фанук - тоже
            long_starts + '(ELSE)'  + '(\s*)' +                             ends: DICTshiftsINT['ELSE'],
            long_starts + '(ENDLOOP)' +                                     ends: DICTshiftsINT['END_LOOP'],  # '(\s*)' +
            long_starts + '(ENDIF)' + '(\s*)' +                             ends: DICTshiftsINT['ENDIF'],
            long_starts + '(ENDFOR)' +      '(\s*)' +                       ends: DICTshiftsINT['END_FOR'],  # '(\s*)' +
            long_starts + '(WHILE)' + '([^;]*)'  + last_part +         ends: DICTshiftsINT['WHILE'],
            long_starts + '(END)'   +     last_part +                       ends: DICTshiftsINT['ENDWHILE'],#'(\s*)' +
            long_starts + '(LOOP)'  +                                       ends: DICTshiftsINT['LOOP'],#+ '(\s*)'
            long_starts + '(REPEAT\s*)' +                                      ends: DICTshiftsINT['REPEATu'],#'(\s*)' +
            long_starts + '(UNTIL\s+)' +      '([^;]+)'           +               ends: DICTshiftsINT['UNTIL'],#'(\s*)'
            long_starts + '(FOR)' + '(.*)' + '(TO)' + last_part +           ends: DICTshiftsINT['FOR'],
            long_starts + case_str                  +                        ends: DICTshiftsINT['CASE'],
            long_starts + '(GOTOC)'  + last_part +                          ends: DICTshiftsINT['GOTOC'],
            long_starts + '(GOTOS)'  + last_part +                          ends: DICTshiftsINT['GOTOS'],
            long_starts + '(GOTOB)'  + last_part +                          ends: DICTshiftsINT['GOTOB'],
            long_starts + '(GOTOF)'  + last_part +                          ends: DICTshiftsINT['GOTOF'],
            long_starts + '(GOTO)' + last_part +                            ends: DICTshiftsINT['GOTO'],
            long_starts + '(REPEAT(B)?)' + '(\s+(\w+))?'  +'(\s+(\w+))?' + '(\s+P\s*=\s*([^;]+))?' + '(\s*)' + ends: DICTshiftsINT['REPEAT_LB'],#TODO: REPEATB!!
            #long_starts + '(([^XYZABCFR]|\w\w+\d*)|(R\d+))(\s*=\s*)([^;]*)' +               ends: DICTshiftsINT['R = '],
            #long_starts + '(((?:DEF)\s+(INT)\s+[^XYZABCFR]|\w\w+\d*)|(R\d+))(\s*=\s*)([^;]*)' + ends: DICTshiftsINT['R = '],#REAL|STRING| #CR is a problem possible
            long_starts + '((?:DEF\s+)?(REAL\s+|INT\s+|STRING\s+|BOOL\s+|CHAR\s+)?([^XYZABCFR]|\w\w+\d*)|(R\d+))(\s*=\s*)([^;]*)' + ends: DICTshiftsINT['R = '],#R probably does not needed
            long_starts + '((?:DEF\s+)(REAL\s+|INT\s+|STRING\s+|BOOL\s+|CHAR\s+)([^XYZABCFR]|\w\w+\d*))' + ends: DICTshiftsINT['R = '],
            long_starts + r'((G11[012])\s*)(((([XYZ])(\s*=?\s*[^;]*?))(([XYZ])(\s*=?\s*[^;]*?))(([XYZ])(\s*=?\s*[^;]*?))?)|(((AP|RP)(\s*=\s*?[^;]*?))((AP|RP)(\s*=\s*?[^;]*?))))?' + ends: DICTshiftsINT['POLAR'],
            long_starts + r'\s*CYCLE800(\({}\))\s*'.format(cycle800_str) + ends: DICTshiftsINT['CYCLE800'],

            #REAL|STRING|INT
            #long_starts + '((\w*\d*)|(\R\d*))(\s*=\s*)(.*)' + ends: DICTshiftsINT['R = '],
            long_starts + '()()()()' + ends: DICTshiftsINT['LABEL'],
            long_starts + '(M30)' + ends: DICTshiftsINT['M30'],
            long_starts + '(RET)' + ends: DICTshiftsINT['M30'],
            long_starts + f'(PROC\s*[^(;]+){center_sub}' + ends: DICTshiftsINT['SUB_PROG_START'],
            #long_starts + center_sub + ends: DICTshiftsINT['SUB_PROGRAM'],

        }
        #one_var = '(\([^\(\)]+\)'

        self.SUBprogram_mask = QRegularExpression(long_starts + '(^)?' + center_sub + ends)


        self.SHIFT_masks = {}
        for k, v in SHIFT_masks.items():
            self.SHIFT_masks[QRegularExpression(k)] = v

    #def save_vars_as_local(self, VARs, main_current_vars):
    #   VARs.update(main_current_vars)
#
    #def save_vars_as_global(self, VARs, main_current_vars):
    #    print(VARs)
    #    for k in VARs:
    #        if k[0] == 'R' and k[1:].isnumeric() or k in main_current_vars:
    #            main_current_vars[k] = VARs[k]
#

    def save_vars_as_local_global(self, np_box, current_vars, red, info):
        is_sub = np_box.redactor.sub1
        print(f'save_vars_as_local_global')
        main_current_vars = np_box.redactor.tab_.currentWidget().np_box.current_vars_dict
        print(f'9999 info = {info}')
        #(array([2, -1, 33, 10]), ['', None, ('cycle_goto',), ['a', ' b '], [(5.0,), (7.0,)]], 1)

        if is_sub:
            #siemens_SUB_helper(current_vars, main_current_vars)
            for k in current_vars:

                if k[0] == 'R' and k[1:].isnumeric() or k in main_current_vars:
                    main_current_vars[k] = current_vars[k]
        else:
            np_box.current_vars_dict = current_vars

        red.np_box.VARs.update(main_current_vars)
        red.np_box.SUB_exchange_DATA = [info[1][3], info[1][4]]
        red.np_box.special_options_applying()
        #_________________________________________________________________________________________________________________
        for k in red.np_box.current_vars_dict:
            if k[0] == 'R' and k[1:].isnumeric() or k in current_vars:
                current_vars[k] = red.np_box.current_vars_dict[k]

        #if len(info[1][4]) > 0:
        k = 0
        print(f'r666 ed.np_box.SUB_exchange_DATA = {red.np_box.SUB_exchange_DATA}')
        print(f'7777red.np_box.current_vars_dict = {red.np_box.current_vars_dict}')
        print(f'info all = {info}')
        print(f'info[1][4] = {info[1][4]}')
        print(f'info[1][3] = {info[1][3]}')
        if info[1][4] is not None:
            for V_ in info[1][4]:
                print(f'V_ = {V_}')
                if len(V_) == 0 or type(V_[0]) is not str:
                    #print(f'info[1][4][0] is not ')
                    k += 1
                    continue

                if red.np_box.SUB_exchange_DATA[k][0]:
                    print(f'red.np_box.SUB_exchange_DATA[k][1] = {red.np_box.SUB_exchange_DATA[k][1]}')
                    print(f'red.np_box.current_vars_dict[red.np_box.SUB_exchange_DATA[k][1]] = {red.np_box.current_vars_dict[red.np_box.SUB_exchange_DATA[k][1]]}')
                    current_vars[V_[0]] = red.np_box.current_vars_dict[red.np_box.SUB_exchange_DATA[k][1]]
                k+=1
