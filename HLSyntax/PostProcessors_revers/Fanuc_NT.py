from HLSyntax.ReversPostProcessor_0 import ReversalPostProcessor0, STYLES, STYLES_list_G1, STYLES_list_G0, format
from PyQt5.QtCore import QRegularExpression
#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type

class Fanuc_NT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self, redactor):#*args, **kwargs
        super().__init__(redactor)
        """ this is Fanuc turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as a part, order matters
        """
        self.k_XYZABC['X'] = 0.5
        self.ABC_HEAD[2] = False#ax Z belong to table or spindle
        print('self.k_XYZABC = ', self.k_XYZABC)
        self.update_options_postprocessor()
        print('k_XYZABC_list = ', self.k_XYZABC_list)
        n_number = r'^\s*N(\d*)\s*'#херня какая то
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
        np_line[2] = 0
        np_line[3] = 0
        np_line[16] = 0#zero group of commands mean that point should be paint directly
        f = [nya.captured(2), nya.captured(4), nya.captured(6)]#4
        for i1 in f:
            if i1 == 'U':
                np_line[4] = self.start_pointXYZ[0]
            elif i1 == 'V':
                np_line[5] = self.start_pointXYZ[1]
            elif i1 == 'W':
                np_line[6] = self.start_pointXYZ[2]
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

