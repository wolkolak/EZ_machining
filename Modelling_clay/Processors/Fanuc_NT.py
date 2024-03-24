from Modelling_clay.Processors.Processor_base.ReversPostProcessor_0 import ReversalPostProcessor0, format
from PyQt5.QtCore import QRegularExpression
#G1_G1_X_Y_Z_A_B_C_cX_cY_cZ_R_F_np_line_n_type
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTshiftsINT
from os import listdir
from os.path import isfile, join
import numpy as np
#todo insert_in_main_gmodal везде убрать

class Fanuc_NT(ReversalPostProcessor0):#ReversalPostProcessor0
    def __init__(self, redactor):#*args, **kwargs

        self.special_commands = [
                                [r'\s*G(1[789])\s*', self.change_plane, format('blue', 'bold')],
                                [r'G28\s*(([UVW])\s*0.?\s*)(([UVW])\s*0.?\s*)?(([UVW])\s*0.?\s*)?$', self.G28_U0_V0_W0, format('red', 'bold')],
                                [r'\s*G(9[01])\s*', self.absolut_and_reference_coord_G90_G91, format('blue', 'bold')],
                                [r'\s*(G\s*(5[456789]))(\s|$|[a-zA-Z])', self.G54_G59, format('blue', 'bold')],
                                [r'^\s*(G1((1[23])|([23]\.1)))\s*', self.polar_coord_G112, format('pink', 'bold')],
                                [r'^\s*(G(1[56]))\s*', self.polar_coord_G16, format('pink', 'bold')]
                                 ]
        super().__init__(redactor)
        """ this is Fanuc turn - milling simulator. If u writing similar one, use it as parent or collateral.
        To add command, create behavior function; add to special_commands list string, color, style. 
        Note, that pattern will be checked one after another, so if u have patternA thant includes patternB as a part, order matters
        """
        #self.k_XYZABC['X'] = 0.5
        #self.ABC_HEAD[2] = Falzse#ax Z belong to table or spindle
        #print('self.k_XYZABC = ', self.k_XYZABC)
        self.CNC_op_type = 'Fanuc_op'
        self.brackets = ['[', ']', '(', ')']
        self.update_rules()

        for i in range(0, len(self.special_commands)):
            self.special_commands[i][0] = QRegularExpression(self.special_commands[i][0])
            #look Perl RegularExpressions if u need
        print('self.special_commands = ', self.special_commands)

    # check_command(self, text, np_line, g_modal)

    #def N_number(self, lineBlock, nya, np_line, count, g_modal, i):
    #    start1 = nya.capturedStart(0)
    #    end1 = nya.capturedEnd(1)
    #    lineBlock.setFormat(start1, end1, self.special_commands[i][2])


    def change_plane(self, lineBlock, nya, np_line, count, g_modal, i):#todo позже подстроить под N10
        np_line[16] = 1.
        #2/0
        plane = nya.captured(1)
        #print('plane 222 = ', plane)
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
        lineBlock.setFormat(start1, len(nya.captured(0)), self.special_commands[i][2])
        key = 'absolute_or_incremental'
        value = ABS_ref
        return key, value


    def polar_coord_G112(self, lineBlock, nya, np_line, count, g_modal, i):
        print('polar coord')
        np_line[16] = 1
        if nya.captured(1) == 'G12.1' or nya.captured(1) == 'G112':
            POLAR_ON_OFF = '112'
        else:# nya.captured(1) == 'G13.1' or nya.captured(1) == 'G113':
            POLAR_ON_OFF = '113'
        #self.redactor.g_modal.insert_in_main_gmodal('polar_coord', count + self.redactor.editor.min_line_np, POLAR_ON_OFF)
        start1 = nya.capturedStart(0)
        lineBlock.setFormat(start1, len(nya.captured(0)), self.special_commands[i][2])
        key = 'polar_coord'
        value = POLAR_ON_OFF
        print('kkk = ', value)
        return key, value

    def polar_coord_G16(self, lineBlock, nya, np_line, count, g_modal, i):
        print('polar coord 16')
        np_line[16] = 1
        #if nya.captured(1) == 'G12.1' or nya.captured(1) == 'G112':
        #    POLAR_ON_OFF = '112'
        #else:# nya.captured(1) == 'G13.1' or nya.captured(1) == 'G113':
        #    POLAR_ON_OFF = '113'
        #self.redactor.g_modal.insert_in_main_gmodal('polar_coord', count + self.redactor.editor.min_line_np, POLAR_ON_OFF)
        #POLAR_ON_OFF
        start1 = nya.capturedStart(0)
        lineBlock.setFormat(start1, len(nya.captured(0)), self.special_commands[i][2])
        key = 'polar_coord_16'

        value = nya.captured(2) #POLAR_ON_OFF
        print('kkk = ', value)
        return key, value

    def G54_G59(self, lineBlock, nya, np_line, count, g_modal, i):
        #print('SC was noted')
        np_line[16] = 1
        SC = nya.captured(2)
        start1 = nya.capturedStart(1)
        #self.redactor.g_modal.insert_in_main_gmodal('SC', count + self.redactor.editor.min_line_np, SC)#todo убрать???!
        #self.redactor.tab_.center_widget.left.left_tab.parent_of_3d_widget.openGL.g54_g59_AXIS_Display['G'+str(SC)][6] = True
        lineBlock.setFormat(start1, len(nya.captured(1)), self.special_commands[i][2])
        #return True
        key = 'SC'
        value = nya.captured(2)
        return key, value
        #return True

    def SHIFT_operators(self):
        #'GOTO': 14,
        #'GOTOC': 15,  # GOTO without error
        #'GOTOS': 16,  # to start of the program
        #'GOTOB': 17,  # backward direction
        #'GOTOF': 18,  # forward direction
        ## 'REPEAT_LB':    19,
        #'R = ': 30,
        #'LABEL': 40

        #NumberN = r'(N(\d+)\s*)?'
        NumberN = r'(N(\d+)\s*)?'
        #starts = '^(\s*)' + NumberN
        starts = '^(\s*)' + NumberN
        ends = '(\(.*\))?\s*$'#todo or ;
        #ends = '(;.*)?$'  # todo or ;
        Label = '(\w*:\s*)?'#TODO а меток то у фанука не бывает!!!
        long_starts = starts + Label
        #todo временно для сименса
        self.label = long_starts

        last_part = '([^\{}]*)'.format(self.brackets[2])

        #p = '([^GOTO]+)'#)|(DEFAULT)

        #p = '(.*)'
        #это всё неверно конечно
        #of_goto = '(' + '(\s+)' + '(\d+)' + '(\s*GOTO([FBCS])?\s*)'+ p + ')?'

        #case_default_str = '(' + '(DEFAULT)' + '(\s*GOTO([FBCS])?\s*)'+ '([^;]+)'+ ')?'
        #case_default_str = '(.*)'

        #case_str = '(CASE\s*)' + '\((.*)\)'+ '(OF\s*) ' + '(.*)'# of_goto#*5 + case_default_str
        center_sub = '(M98\s*)(O\d+)(\s*L(\d+)\s*)?'  # для сименса сейчас subr1 и subr2(x=2, z=8)

        SHIFT_masks = {#отдельно сделать переменные и метки
            long_starts + '(IF)'    + '(.*)' + '(GOTO)'   + last_part +     ends: DICTshiftsINT['IF_GOTO_FANUC'],
            long_starts + '(IF\s+)' + '(.*)' +      '(THEN\s+)' +    '(.*)' +     ends: DICTshiftsINT['IF_THEN'],
            #long_starts + '(END)' +                                         ends: DICTshiftsINT['END_LOOP'],  # '(\s*)' +
            long_starts + '(WHILE)' + '(.*)' + '(DO)' + last_part +         ends: DICTshiftsINT['WHILE'],
            long_starts + '(END)'   +     last_part +                       ends: DICTshiftsINT['ENDWHILE'],#'(\s*)' +
            #long_starts + '(DO)'  +                                         ends: DICTshiftsINT['LOOP'],#+ '(\s*)'
            #long_starts + '(GOTO)' + last_part +                            ends: DICTshiftsINT['GOTO'],
            long_starts + '(GOTO)' + last_part + ends: DICTshiftsINT['GOTO_FANUC'],
            #long_starts + '((\w*\d*)|(\#\d*))(\s*=\s*)(.*)' +               ends: DICTshiftsINT['R = '],
            long_starts + '(()?(\#\d+)|(\#\d+))(\s*=\s*)([^;(]*)' + ends: DICTshiftsINT['R = '],
            long_starts + '(M30)' + ends: DICTshiftsINT['M30'],
            long_starts + '(M99)' + ends: DICTshiftsINT['M30'],
        }

        self.SUBprogram_mask = QRegularExpression(long_starts + center_sub + ends)
        print(f'self.SUBprogram_mask = {long_starts + center_sub + ends}')
        self.SHIFT_masks = {}
        for k, v in SHIFT_masks.items():
            self.SHIFT_masks[QRegularExpression(k)] = v

    def sub_programs(self):
        main_address = 'Modelling_clay/Processors/Processor_base/Fanuc_subprograms/'
        catalog = [main_address + 'fanuc_sys',]#, main_address + '_N_CUS_DIR', main_address + '_N_CMA_DIR', main_address + '_N_CST_DIR']
        sub_program_names = {}
        # sub_program_names.
        for cat in reversed(catalog):
            f_c = [f for f in listdir(cat) if isfile(join(cat, f))]
            if len(f_c) > 0:
                for f1 in f_c:
                    print(f'here f1 = {f1}')
                    f2 = f1.split('.')
                    if len(f2) == 1 or f2[1] in ['.mpf', '.nc', 'p-1']:
                        sub_program_names[f2[0].lower()] = cat + '/' + f1
                    #if f1.endswith('.nc') or f1.endswith('.mpf') or f1.find('.') == -1:
                    #    sub_program_names[f1[:-4].lower()] = cat + '/' + f1

                        #sub_program_names[f1[:-4].lower() + '_' + f1[-3:].lower()] = cat + '/' + f1
        # i did not add _N_name in sub_program_names. too much combinations. i don't really care. if u have :"_N_name" from machine, then use "_N_name" in your code too
        print('sub_program_names = ', sub_program_names)
        return sub_program_names


    def sub_programs_current(self, cat):
        sub_program_names = {}
        try:
            f_c = [f for f in listdir(cat) if isfile(join(cat, f))]
            print('f_c = ', f_c)
            if len(f_c) > 0:
                for f1 in f_c:
                    f2 = f1.split('.')
                    print(f'f2 here is {f2}')
                    if len(f2) == 1 or f2[1].lower() in ['mpf', 'nc', 'p-1']:
                        sub_program_names[f2[0].lower()] = cat + '/' + f1
        except:
            print('Mother catalogue for current file was not found. It\'s subprograms not included' )
        print('sub_program_names current = ', sub_program_names)
        return sub_program_names

    def save_vars_as_local_global(self, np_box, current_vars, red, info):
        print(f'save_vars_as_local_global fanuc')
        L = 1 if info[1][4] is None else int(info[1][4][0][0][1:])
        print('L = ', L)
        #print('L = ', info[1][4][0][0])
        print('current_vars = ', current_vars)

        for l in range(L):
            for k in current_vars:
                print(f'k[1:].isnumeric() is {k[1:].isnumeric()}')
                if k[0] == '#' and k[1:].isnumeric() and 33<int(k[1:]):
                        #print(f'999 current_vars[k] = {current_vars[k]}')
                        red.np_box.VARs[k] = current_vars[k]
                        #print(f'Подпрограмма: {k} = {red.np_box.current_vars_dict[k]}')
            print(f'red.np_box.current_vars_dict = ', red.np_box.current_vars_dict)
            red.np_box.special_options_applying()
            print(f'red.np_box.current_vars_dict = ', red.np_box.current_vars_dict)
            for k in red.np_box.current_vars_dict:
                if k[0] == '#' and k[1:].isnumeric() and 33<int(k[1:]):
                       current_vars[k] = red.np_box.current_vars_dict[k]
            if l == 0:
                all_np_boxes = red.np_box.visible_np
            else:
                all_np_boxes = np.vstack((all_np_boxes, red.np_box.visible_np))
        red.np_box.visible_np = all_np_boxes
