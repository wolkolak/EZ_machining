from HLSyntax.ReversPostProcessor_0 import ReversalPostProcessor0, STYLES, STYLES_list_G1, STYLES_list_G0, format
from PyQt5.QtCore import QRegularExpression
#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type

class Fanuc_NT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self):#*args, **kwargs
        super().__init__()
        """ this is Fanuc turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as part, order matters
        """
        self.k_XYZABC['X'] = 0.5
        print('self.k_XYZABC = ', self.k_XYZABC)
        self.update_options_postprocessor()
        print('k_XYZABC_list = ', self.k_XYZABC_list)
        self.special_commands = [
                                [r'\s*G(1[789])\s*', self.change_plane, "format('blue', 'bold')"],
                                [r'^G28 (([UVW])\s*0.\s*)(([UVW])\s*0.\s*)(([UVW])\s*0.\s*)$', self.G28_U0_V0_W0, format('red', 'bold')],
                                 ]
        for i in range(0, len(self.special_commands)):
            self.special_commands[i][0] = QRegularExpression(self.special_commands[i][0])
            #look Perl RegularExpressions if u need

        print('self.special_commands = ', self.special_commands)

    # check_command(self, text, np_line, g_modal)

    def change_plane(self, lineBlock, nya, np_line, g_modal, i):
        print('kkkkk')


    def G28_U0_V0_W0(self, lineBlock, nya, np_line, g_modal, i):#todo это должна быть одна операция
        print('G28_U0_V0_W0 nya = ', nya)
        np_line[0] = 0
        np_line[1] = 0
        np_line[14] = i
        f = [nya.captured(2), nya.captured(4), nya.captured(6)]
        #for i in range(10):
        #    print('nya.captured(1) = ', nya.captured(i))
        for i1 in f:
            if i1 == 'U':
                np_line[2] = self.start_pointXYZ[0]
            elif i1 == 'V':
                np_line[3] = self.start_pointXYZ[1]
            elif i1 == 'W':
                np_line[4] = self.start_pointXYZ[2]

        lineBlock.setFormat(0, len(nya.captured(0)), self.special_commands[i][2])
        #np_line[3] = self.start_pointXYZ[2]


