from HLSyntax.ReversPostProcessor_0 import ReversalPostProcessor0
from PyQt5.QtCore import QRegularExpression


class Fanuc_NT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self):#*args, **kwargs
        super().__init__()
        """ this is Fanuc turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as part, order matters
        """
        self.k_XYZCAB['X'] = 0.5
        self.special_commands = [['G28 U0. V0.', self.G28_U0_V0, "format('#468a1a', 'bold')"],
                                 ['G28 W0.', self.G28_W0, "format('#468a1a', 'bold')"]
                                 ]
        for i in range(0, len(self.special_commands)):
            self.special_commands[i][0] = QRegularExpression('^' + self.special_commands[i][0] + '$')
            #look Perl RegularExpressions if u need

        print('self.special_commands = ', self.special_commands)

    # check_command(self, text, np_line, g_modal)

    def G28_U0_V0(self, nya, np_line, g_modal, i):
        np_line[0] = 0
        np_line[9] = 0
        np_line[10] = i
        np_line[1] = self.start_pointXYZ[0]
        np_line[2] = self.start_pointXYZ[1]
        #np_line[3] = self.start_pointXYZ[2]
        print('G28_U0_V0')

    def G28_W0(self, nya, np_line, g_modal, i):
        np_line[0] = 0
        np_line[9] = 0
        np_line[10] = i
        np_line[3] = self.start_pointXYZ[2]
        print('G28_W0')



