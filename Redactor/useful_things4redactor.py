from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QLabel, QSpinBox, QPushButton
from PyQt5.QtCore import Qt
import numpy as np
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTconstructionsF, DICTconstructionsB, DICTconstrucionINTERIM, DICTshiftsINT, DICTshift
from Gui.little_gui_classes import simple_warning

class IterDialog(QDialog):
    def __init__(self, father_, *args, **kwargs):
        super().__init__(father_, *args, **kwargs)
        print('create IterDialog')
        self.setFixedSize(200, 105)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('ITER')
        grid = QGridLayout()
        self.setLayout(grid)
        self.edit_papa = father_
        self.setStyleSheet('font-size: 20px;')
        self.lbl = QPushButton('Help')#0 = last iteration\nn+1 = empty cycle
        self.lbl.setToolTip('If iterations show\nsomething unexpected for You')
        self.lbl.clicked.connect(self.help)
        grid.addWidget(self.lbl, 0, 0)
        self.text_iter = QSpinBox()
        self.text_iter.setValue(1)
        grid.addWidget(self.text_iter, 1, 0)
        self.text_iter.textChanged.connect(self.changeIter)

    def help(self):
        simple_warning('Unecpected behavior?', "1) '0' show last iteration, it is an alternative way.\n2)Algorithmic loop show one empty iteration after it ends.\nSo, loop in loop will have different index from it's insides")


    def changeIter(self):
        p = self.text_iter.text()
        if p == '':
            iter = 1
            self.text_iter.setText('')
        else:
            iter = int(p)-1
        self.edit_papa.line_iter = iter
        self.edit_papa.highlightCurrentLine_chooseNewDot()

    def done(self, a0: int) -> None:
        self.edit_papa.line_iter = 0
        QDialog.done(self, a0)


def cycle_iter_show(np_box, gcod_np_visible, frame_address, realNframe, scene0, iter, info):
    print('cycle_iter_show')
    print('realNframe = ', realNframe)#это реальная строка
    #prev_place_in_frame = place_in_frame - 1
    #prev_value_in_frame = frame_address[prev_place_in_frame, 1]
    #prev_nya = gcod_np[prev_value_in_frame, 16]
    #print()

    prev_place_in_frame = np.where(frame_address[:, 1] == realNframe)
    print('prev_place_in_frame first = ', prev_place_in_frame)
    #prev_place_in_frame = np.delete(prev_place_in_frame, -1)
    prev_place_in_frame = prev_place_in_frame[0]
    print('prev_place_in_frame second = ', prev_place_in_frame)
    myL = len(prev_place_in_frame)
    if myL > iter:
        prev_place_in_frame = prev_place_in_frame[iter]
        print(f'myL prev_place_in_frame = {prev_place_in_frame}')
    else:
        if len(prev_place_in_frame) == 0:
            prev_place_in_frame = 1
        else:
            prev_place_in_frame = prev_place_in_frame[0]

    #prev_value_in_frame = frame_address[prev_place_in_frame, 0]  # first note of needed text line
    prev_nya = gcod_np_visible[prev_place_in_frame, 16]  # type of
    cycle_type = info[0][2]
    i = np.searchsorted(np_box.SHIFTcontainer.np_for_vars[:, 0], realNframe)#-1
    print('cycle_type = ', cycle_type)
    print('DICTshift[cycle_type] = ', DICTshift[cycle_type])
    print('DICTshift[cycle_type][1] = ', DICTshift[cycle_type][1])
    #это работало ж np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i__, start=DICTshiftsINT['FOR'], end=[DICTshiftsINT['END_FOR']])
    print(f'curr_int = {i}, cycle_type = {cycle_type}, end = {[DICTshift[cycle_type][1][-1]]}')
    next_place_in_frame = np_box.SHIFTcontainer.SearchConditionDawn(curr_int=i, start=cycle_type, end=[DICTshift[cycle_type][1][-1]])
    print(f'898 next_place_in_frame = {next_place_in_frame}')
    #todo прислать последний элемент но в списке
    next_place_in_frame = np.where(frame_address[:, 1] == next_place_in_frame)
    next_place_in_frame = next_place_in_frame[0]
    myL = len(next_place_in_frame)

    if myL > iter:
        next_place_in_frame = next_place_in_frame[iter]
        print(f'after next_place_in_frame = {next_place_in_frame}')
    else:
        scene0.previous_dot_Mark = 0
        scene0.current_dot_Mark = 0
        return
        #if len(next_place_in_frame) == 0:
        #    next_place_in_frame = 1
        #else:
        #    next_place_in_frame = next_place_in_frame[0]


        #next_place_in_frame = next_place_in_frame[0][iter]
    print(f'11 next_place_in_frame = {next_place_in_frame}')
    print(f'565 prev_place_in_frame = {prev_place_in_frame}')
    while not (np.isnan(prev_nya) or prev_nya == 0 or prev_nya == 7) and prev_place_in_frame > 1:
        prev_place_in_frame = prev_place_in_frame - 1
        print(f'Now prev_place_in_frame = {prev_place_in_frame}')
        #prev_value_in_frame = frame_address[prev_place_in_frame, 1]
        prev_nya = gcod_np_visible[prev_place_in_frame, 16]

    print(f'Начинаем со строки {np_box.visible_np[prev_place_in_frame ]},\n а заканчиваем строкой {np_box.visible_np[next_place_in_frame]}')
    scene0.previous_dot_Mark = prev_place_in_frame
    scene0.current_dot_Mark = next_place_in_frame#next_value_in_frame


def find_last_in_block(current_np, len_current_np, direction=1):#работать будет в insert
    #Нужно для нахождения последнего действующего G0/G1/G2/G3
    print(f'find_last_in_block current_np = {current_np}')
    print(f'len_current_np = {len_current_np}')
    last = False
    if direction == 1:
        for i in range(len_current_np-1, -1, -1):
            print('99 i = ', i)
            if current_np[i, 3] is not np.nan:#todo сюда вышибло при вставке строки R= в среднюю строку кода
                last = current_np[i, 3]
                print('current_np[i, 3] = ', current_np[i, 3])
                break
    else:
        for i in range(0, len_current_np, 1):
            print('99 i = ', i)
            if current_np[i, 3] is not np.nan:
                last = current_np[i, 3]
                print('current_np[i, 3] = ', current_np[i, 3])
                break
    print(f'find_last_in_bloc result = {last}')
    return last
