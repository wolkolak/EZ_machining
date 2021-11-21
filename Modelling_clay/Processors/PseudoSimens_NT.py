from Modelling_clay.ReversPostProcessor_0 import ReversalPostProcessor0, format
from PyQt5.QtCore import QRegularExpression
#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type

class PseudoSimensNT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self, redactor):#*args, **kwargs
        super().__init__(redactor)
        """ this is Fanuc turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as a part, order matters
        """
        #self.k_XYZABC['X'] = 0.5
        #self.ABC_HEAD[2] = False#ax Z belong to table or spindle
        #print('self.k_XYZABC = ', self.k_XYZABC)

        self.update_rules()


        #self.ABC_turning_Zero['A'] =
        #print('k_XYZABC_list = ', self.k_XYZABC_list)
        #n_number = r'^\s*N(\d*)\s*'#херня какая то
        self.special_commands = [
                                [r'\s*G(1[789])\s*', self.change_plane, format('blue', 'bold')],
                                [r'G28\s*(([UVW])\s*0.?\s*)(([UVW])\s*0.?\s*)?(([UVW])\s*0.?\s*)?$', self.G28_U0_V0_W0, format('red', 'bold')],
                                [r'\s*G(9[01])\s*', self.absolut_and_reference_coord_G90_G91, format('blue', 'bold')],
                                #[r'^\s*N(\d*)\s*', self.N_number, format('blue', 'bold')],
                                 ]
        for i in range(0, len(self.special_commands)):
            self.special_commands[i][0] = QRegularExpression(self.special_commands[i][0])
            #look Perl RegularExpressions if u need

        print('self.special_commands = ', self.special_commands)

    # check_command(self, text, np_line, g_modal)

    def N_number(self, lineBlock, nya, np_line, count, g_modal, i):
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(1)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])

    def change_plane(self, lineBlock, nya, np_line, count, g_modal, i):#todo позже подстроить под N10
        print('plane change')
        np_line[16] = 1
        plane = nya.captured(1)
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(1)
        self.redactor.g_modal.insert_in_main_gmodal('plane', count+self.redactor.editor.min_line_np, plane)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])


    def G28_U0_V0_W0(self, lineBlock, nya, np_line, count, g_modal, i):
        start_pointXYZ = self.redactor.current_machine.start_pointXYZ
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

    def absolut_and_reference_coord_G90_G91(self, lineBlock, nya, np_line, count, g_modal, i):
        print('G90_91')
        np_line[16] = 1
        ABS_ref = nya.captured(1)
        self.redactor.g_modal.insert_in_main_gmodal('absolute_or_incremental', count + self.redactor.editor.min_line_np, ABS_ref)
        start1 = nya.capturedStart(0)
        end1 = nya.capturedEnd(1)
        lineBlock.setFormat(start1, end1, self.special_commands[i][2])
        #вставить в

    def update_rules(self):
        """Синтаксические маркеры для языка. """
        # G-func
        # g_cod = ['G0', 'G1', 'G2', 'G3']
        # axises
        # todo perl выражения должны заимствоваться из псведопостпроцессора
        axises0 = ['X', 'Y', 'Z', 'A', 'B', 'C']
        I, J, K, R = 'I', 'J', 'K', 'CR='
        axises = ['X', 'Y', 'Z', 'A', 'B', 'C', I, J, K, R]  # - , 'G', 'F'
        g_prefix = r'(G0?([0123])\s*)?'
        f_postfix = r'(F\s*(\d+(.\d*)?\s*))?'#todo вопрос: а не должен ли "?" стоять в конце?
        NumberN = r'(N(\d+)\s*)?'
        Corrector = r'(G(4[012])\s*)?'
        i_postfix = '(' + I + r'(\d+.\d*))?\s*'#todo сейчас только R реализован для несортированного варианта
        j_postfix = '(' + J + r'(\d+.\d*))?\s*'
        k_postfix = '(' + K + r'(\d+.\d*))?\s*'
        r_postfix = '(' + R + r'(-?\d+.\d*)\s*)?'
        # most strings look like 'main_rule'

        sorted_axis_rule = ''
        for letter in axises:
            sorted_axis_rule += r'(\s*(?:{})(-?\d+\.\d*)\s*)?'.format(letter)
            # sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)

        self.sorted_axis_rule = '^' + NumberN + Corrector + g_prefix + sorted_axis_rule + f_postfix + '$'  # '(?:G0?\d)?\s*'   + f_postfix

        # sorted_axis_rule = r'^(?:X)(\d)$'  # UDALIT

        axises_str = ''.join(axises0)
        axises_coord = r'(\s*([{}])\s*(-?\d+\.\d*)\s*)?'.format(axises_str)
        ijk_str = I + J + K
        ijk_coord = r'(([{}])\s*(-?\d+\.\d*)\s*)?'.format(ijk_str)
        # unsorted_axis_rule = r'(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)#r'^\d((?:X)(-?\d+\.\d*)\s*)$'

        unsorted_axis_rule = axises_coord * 6 + ijk_coord * 3

        unsorted_axis_rule = NumberN + Corrector + g_prefix + unsorted_axis_rule + r_postfix + f_postfix
        self.unsorted_axis_rule = '^' + unsorted_axis_rule + '$'
        print('unsorted_axis_rule = ', self.unsorted_axis_rule)