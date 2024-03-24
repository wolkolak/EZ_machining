#from left_zone.Scene import
import numpy as np
import math
from Core.Data_solving.VARs_SHIFTs_CONDITIONs.encryption_IF_WHILE_GOTO import DICTconstructionsF, DICTconstructionsB, DICTconstrucionINTERIM, DICTshiftsINT, DICTshift
from Redactor.useful_things4redactor import cycle_iter_show
from Settings.settings import MaxFileLen


def JumpSearch (lys, val):
    length = len(lys)
    jump = int(math.sqrt(length))
    left, right = 0, 0
    while left < length and lys[left] <= val:
        right = min(length - 1, left + jump)
        if lys[left] <= val and lys[right] >= val:
            break
        left += jump
    if left >= length or lys[left] > val:
        return -1
    right = min(length - 1, right)
    i = left
    while i <= right and lys[i] <= val:
        if lys[i] == val:
            return i
        i += 1
    return -1

def JumpSearchLast (lys, val):
    length = len(lys)
    jump = int(math.sqrt(length))
    left, right = length-1, length-1
    while right > 0 and lys[right] >= val:
        left = max(0, right - jump)
        if lys[left] <= val <= lys[right]:
            break
        right -= jump
    #if left >= length or lys[left] > val:
    #    return -1
    left = max(0, left)
    i = right
    while i >= left and lys[i] >= val:
        if lys[i] == val:
            return i
        i -= 1
    return 1

def point_dot_from_line_depreited(line_number, left):
    leftTab = left.left_tab
    scene0 = leftTab.parent_of_3d_widget.openGL
    find_n_line = line_number + 1
    arr_ = scene0.gcod.T[15]
    scene0.current_dot_Mark = JumpSearchLast(arr_, find_n_line)

def point_dot_from_line(np_box, blockNumber, left, iter):
    '''

    :param np_box:
    :param blockNumber: visualising line number - 1
    :param left:
    :return:
    '''



    print('point_dot_from_line')
    #return
    print('blockNumber = ', blockNumber)
    #todo nya = gcod_np[start_line, 16] выбивает иногда.
    #todo выбивает при вы

    frame_address = np_box.frame_address_in_visible_pool
    gcod_text_np = np_box.main_g_cod_pool
    gcod_np = np_box.visible_np

    #print(f'Почемут опроблемы:{len(np_box.visible_np)} \n np_box.visible_np = {np_box.visible_np}')
    #if len(np_box.visible_np) == 20:
    #    2/0
    leftTab = left.left_tab
    scene0 = leftTab.parent_of_3d_widget.openGL
    #print(f'**** anchor = {np_box.redactor.editor.textCursor().anchor()}')
    realNframe = blockNumber + 1
    print('gcod_text_np[n][16] = ', gcod_text_np[realNframe][16])
    cur_type = gcod_text_np[realNframe][16]
    if cur_type in [2, 4]:
        #Нет. так недостаточно. нужен список цикличных конструкций
        if cur_type == 4:#DICTconstructionsF
            info = np_box.SHIFTcontainer.return_info(realNframe)#, local_line
            print('info  info = ', info )
            if info[0][2] in DICTconstructionsF:#prev_N_in_frame, N_in_frame =
                cycle_iter_show(np_box, gcod_np, frame_address, realNframe, scene0, iter, info)
                #scene0.previous_dot_Mark = prev_N_in_frame
                #scene0.current_dot_Mark = N_in_frame
                return
            elif info[0][2] == DICTshiftsINT['REPEAT_LB']:
                print(f'REPEAT_LB connect')
                prev_N_in_text = info[0][0]
                prev_N_s = np.where(frame_address[:, 1] == prev_N_in_text)[0]
                print(f'prev_N_s = {prev_N_s}')
                myL = len(prev_N_s)
                if myL == 0:
                    scene0.previous_dot_Mark = 0
                    scene0.current_dot_Mark = 0
                    return
                #iter_ = int(iter / 2)
                print(f'myL = {myL}')
                if myL > iter + 1:
                    print('2>1')
                    prev_N = prev_N_s[iter]
                    next_N = prev_N_s[iter + 1]
                else:
                    prev_N = 0
                    next_N = 0
                    #prev_N = prev_N_s[0]
                    #if myL > 1:
                    #    next_N = prev_N_s[1]
                    #else:
                    #    next_N = prev_N_s[0]
                print(f'99 prev_N_s[0] = {prev_N_s}')
                print(f'iter = {iter}')

                scene0.previous_dot_Mark = prev_N
                scene0.current_dot_Mark = next_N
                print(f'988 start value = {prev_N}, end = {next_N}')
                return
            else:
                if info[0][2] == DICTshiftsINT['SUB_PROGRAM']:
                    print(f'SUB_PROGRAM info = {info}')
                    prev_N_in_text = info[0][0]
                    prev_N_s = np.where(frame_address[:, 1] == prev_N_in_text)[0]
                    print(f'prev_N_s = {prev_N_s}')
                    myL = len(prev_N_s)
                    if myL == 0:
                        scene0.previous_dot_Mark = 0
                        scene0.current_dot_Mark = 0
                        return
                    iter_ = int(iter / 2)
                    print(f'myL = {myL}')
                    if myL > iter_+1:
                        print('2>1')
                        prev_N = prev_N_s[iter_]
                        next_N = prev_N_s[iter_ + 1]
                    else:
                        prev_N = 0
                        next_N = 0
                        #prev_N = prev_N_s[0]
                        #if myL > 1:
                        #    next_N = prev_N_s[1]
                        #else:
                        #    next_N = prev_N_s[0]
                    print(f'99 prev_N_s[0] = {prev_N_s}')
                    print(f'iter_ = {iter_}')

                    scene0.previous_dot_Mark = prev_N
                    scene0.current_dot_Mark = next_N
                    print(f'988 start value = {prev_N}, end = {next_N}')
                    return
        else:
            pass

    try:
    #if True:
        #print(f'frame_address = {frame_address}')
        print('realNframe = ', realNframe)

        #place_in_frame = np.searchsorted(frame_address[:, 0], realNframe)#todo нельзя searchsorted ибо значения потом могут повторится.
        places_in_frame = np.where(frame_address[:, 1] == realNframe)
        #print('BEFORE places_in_frame = ', places_in_frame)
        #ничего не нашёл  BEFORE place_in_frame =  (array([], dtype=int64),)!!!!!!!!!
        print(f'3232 iter = {iter}')
        myL = len(places_in_frame[0])
        #iter = iter - 1

        if myL > iter:
            N_line_in_frame = places_in_frame[0][iter]
        else:
            N_line_in_frame = places_in_frame[0][0]
            #FFFF
        #frame_address[place_in_frame][0][1]


        #N_in_frame = frame_address[place_in_frame, 0]  # first note of needed text line
        nya = gcod_np[N_line_in_frame, 16]  # type of

        #prev_place_in_frame = np.searchsorted(frame_address[:, 0], realNframe-1)
        prev_N_line_in_frame = N_line_in_frame - 1
        prev_nya = gcod_np[prev_N_line_in_frame, 16]
        #prev_N_in_frame = frame_address[prev_place_in_frame,0]

        #print('А ну-ка gcod_np = ', gcod_np)
        print('999 prev_N_line_in_frame  = ', prev_N_line_in_frame )
        print(f'отыщем старт подпрограммы:  {np_box.sub_programs_dict}')
        #if
        #prev_N_in_frame = prev_N_in_frame if prev_N_in_frame < MaxFileLen else prev_N_in_frame - MaxFileLen#todo this is useless anyway.
        #TODO ОТРЕЗАТЬ ЗНАЧЕНИЯ БОЛЬШЕ 10МЛН

        while not (np.isnan(prev_nya) or prev_nya == 0 or prev_nya == 7) and prev_N_line_in_frame > 0:#>1 was.
            prev_N_line_in_frame  = prev_N_line_in_frame  - 1
            #prev_N_in_frame = frame_address[prev_N_line_in_frame , 0]

            #prev_nya = gcod_np[prev_N_in_frame, 16]
            prev_nya = gcod_np[prev_N_line_in_frame, 16]
            print(f'11 prev_nya = {prev_nya}, prev_N_line_in_frame  = {prev_N_line_in_frame }')

        L = len(gcod_np)
        print(f'nya in connect = {nya}')
        if not (np.isnan(nya) or nya == 0 or nya == 7):
            print(f'thats working 555')
        print(f'N_line_in_frame 000 = {N_line_in_frame}')
        print('L = ', L)
        while not (np.isnan(nya) or nya == 0 or nya == 7) and L > N_line_in_frame + 1:#todo 7 вообще не нужна поидее
            N_line_in_frame = N_line_in_frame + 1
            #print(f'N_line_in_frame = {N_line_in_frame}')
            #N_in_frame = frame_address[N_line_in_frame, 0]
            #nya = gcod_np[N_in_frame, 16]
            nya = gcod_np[N_line_in_frame, 16]

        print(f'Начинаем со строки {np_box.visible_np[prev_N_line_in_frame]},\n а заканчиваем строкой {np_box.visible_np[N_line_in_frame]}')
        scene0.previous_dot_Mark = prev_N_line_in_frame
        scene0.current_dot_Mark = N_line_in_frame

        #scene0.previous_dot_Mark = frame_address[N_in_frame][1]
        #scene0.current_dot_Mark = frame_address[end_N_in_frame][1]
    except IndexError:
        print('Так ошибка же была')
        scene0.previous_dot_Mark = -1
        scene0.current_dot_Mark = -1



def from_point_to_line(number):
    print('from_point_to_line, number = ', from_point_to_line)