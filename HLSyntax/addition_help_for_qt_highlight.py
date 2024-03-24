from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence



#def corrected_number_of_lines_redo():
#    return corrected_qt_number_of_lines, starshiy_block, mladshii_block, add_undo, add_redo



def corrected_number_of_lines(my_edit, key, replace_to_nothing):#, oncoming_command
    #print('writing key used')
    problem = False
    corrected_qt_number_of_lines = 0
    add_redo = 0
    add_undo = 0
    my_cursor = my_edit.textCursor()
    print('correct cursor = ', my_cursor.position())
    pos1 = my_cursor.position()
    pos2 = my_cursor.anchor()
    #2/0


    h = my_cursor.hasSelection()
    b = my_cursor.atBlockEnd()
    #anchor_pos = my_cursor.anchor()
    my_cursor.setPosition(pos2)
    c = my_cursor.atBlockEnd()
    #univerasal part
    starshiy = max(pos1, pos2)
    mladshii = min(pos1, pos2)
    print('starshiy = ', starshiy )
    mladshii_block = my_edit._document.findBlock(mladshii).blockNumber()
    st_block_itself = my_edit._document.findBlock(starshiy)
    starshiy_block = st_block_itself.blockNumber()
    #forbid = False
    if starshiy == pos1:
        at_block_end = b
    else:
        at_block_end = c

    if key == Qt.Key_Backspace:
        my_edit.undoStack.edit_type = 'backspace'
        print('Backspace')
        if my_cursor.atBlockStart() and not h:
            print('tut problema bila')
            #tofo как будто необязаельно
            #mladshii_block = mladshii_block - 1#backspace in the beginning of the line will update previous line too

        elif at_block_end and not starshiy_block + 1 == my_edit.blockCount():
            corrected_qt_number_of_lines = 1
            add_redo = 1


    elif key == 'insert':
        #print('insert11')
        #t = 5 /0
        my_edit.insert_dognail = 0
        next_line = st_block_itself.next()
        my_edit.undoStack.edit_type = 'insert'

        #mladshii - pos
        if mladshii == 0:#(pos1 == 0 or pos2 == 0):
            print('mladshiy == 0')
            if starshiy == 0:#ничего не может быть выделено - это же пустая первая строка
                print('starshiy == 0')
                corrected_qt_number_of_lines = 1
                #if h:
                #    corrected_qt_number_of_lines += 1
                #else:
                #    pass
                if next_line.length() == 1:
                    print('Zdes 7')
                    print(f'1 ADD, because next_line.length()  = {next_line.length() }')
                    corrected_qt_number_of_lines += 1
                    my_edit.insert_dognail = 1
                    #forbid = True
                    add_undo = 1
                    add_redo = 1#5
                else:
                    print('Zdes 8')
                    add_redo = 1
                    add_undo = 1
            else:
                #выделил с 0 по некий символ 1 или иной строки
                add_redo = 1
                if mladshii_block == starshiy_block:#всё на первой строке
                    print('mladshii_block == starshiy_block')
                    if next_line.length() == 1:#if h????
                        next_line2 = next_line.next()
                        if next_line2.length() == 1:#следом 2 пустых строки

                            print('Zdes 1')
                            #my_edit.insert_dognail = 1
                            corrected_qt_number_of_lines += 2
                            #starshiy_block = starshiy_block + 1
                            #add_redo = 1
                            add_undo = 0
                        else:#следом одна пустая строка
                            print('Zdes 2')
                            add_undo = 0
                            corrected_qt_number_of_lines += 2
                    else:
                        #print(f'next_line.length = {next_line.length}')
                        print('Zdes 3')
                        corrected_qt_number_of_lines += 1
                        add_undo = 0
                else:#наало на первой - конец ниже
                    corrected_qt_number_of_lines += 1
                    print('Zdes 4')
                    if at_block_end:
                        print('Zdes 64')
                        add_undo = 1
                        if h:
                            print('Zdes 65')#???????????
                            #corrected_qt_number_of_lines += 1
                            add_undo = 1
                            add_redo = 2
                        else:
                            if my_cursor.position() == 0:  # todo QT5.5 treat 1st line differently (1 more line to rehighlight if it exist)
                                print('Zdes 67')
                                corrected_qt_number_of_lines += 1
                    else:
                        print('Zdes 66')
                        add_undo = 1
                        if next_line.length() == 1:  # if h????
                            print('Zdes 54')
                            #my_edit.insert_dognail = 1
                            corrected_qt_number_of_lines += 1
                            next_line2 = next_line.next()
                            add_undo = 0
                            if next_line2.length() == 1:
                                print('Zdes 55')
                                my_edit.insert_dognail = 1
                                add_undo = 0
                                #corrected_qt_number_of_lines += 1


        else:#______________________________________________________
            print(f'Zdes 71')
            add_redo = 1
            if at_block_end:
                add_undo = 1
                print(f'Zdes 72')
                if h:
                    print(f'Zdes 73')
                    corrected_qt_number_of_lines = 1
                    add_redo = 2
                else:
                    print(f'Zdes 74')
                    if my_cursor.position() == 0:#todo QT5.5 treat 1st line differently (1 more line to rehighlight if it exist)
                        print(f'Zdes 75')
                        corrected_qt_number_of_lines += 1
                    else:
                        pass
                        add_redo = 1

            else:
                #if


                print(f'Zdes 76')
                #pass
                add_undo = 2
                #add_redo = 1
                #corrected_qt_number_of_lines += 1
            #add_redo = 2  # -1


        print(f'1 corrected_qt_number_of_lines = {corrected_qt_number_of_lines}')


    elif key == 'replace':
        #print('replace11')
        my_edit.undoStack.edit_type = 'replace'
        if at_block_end:
            if not replace_to_nothing:
                add_undo = 1
            if h:
                corrected_qt_number_of_lines = 1
                add_redo = 1

    elif key == 'cut':
        print('cut1')
        my_edit.undoStack.edit_type = 'cut'
        if at_block_end and h:
            corrected_qt_number_of_lines = 1
            add_redo = 1
            #print('add_redo = 1')

    elif key == Qt.Key_Delete:
        #print('Delete')
        my_edit.undoStack.edit_type = 'delete'
        #if at_block_end and not h:
        #    starshiy_block = starshiy_block + 1#delete BEFORE the end of the line will update next line too.
        #print('my_cursor.positionInBlock() + 1= {}, my_cursor.block().length() = {}'.format(my_cursor.positionInBlock() + 2, my_cursor.block().length()))
        if not h and my_cursor.positionInBlock() + 2 == my_cursor.block().length():
            corrected_qt_number_of_lines = 1
            add_redo = 1
        elif at_block_end and not starshiy_block + 1 == my_edit.blockCount():#h and
            corrected_qt_number_of_lines = 1
            add_redo = 1

    elif key == Qt.Key_Enter or key == Qt.Key_Return:
        print('enter start')
        #corrected_qt_number_of_lines = 1
        my_edit.undoStack.edit_type = 'enter'
        if at_block_end:
            add_undo = 1
        #else:
        #    add_undo = 0#0
        if h and at_block_end:
            corrected_qt_number_of_lines += 1
        add_redo = 1
            #add_redo = 1 todo ПЕРЕМЕЩЕНО НИЖЕ ибо хайлайтилось на Ctrl+Y 2 строки, а np_pool был только на одну
            # todo - 2 раза он заполнялся и записывался. без изменения номеров строк. т.е. в строку 1 писалась строка 2
        #elif not h and not at_block_end and not my_cursor.atBlockStart():#todo всё это новое
        #    problem = True
        #    print('elif not h and not at_block_end')
        #    #corrected_qt_number_of_lines = 1
        #    add_redo = 1
        #    add_undo = 1
        #else:
        #    add_redo = 1


    #elif key == 'undo':
    #    print('corrected_number_of_lines')
    #    print('Undo')
    #    corrected_qt_number_of_lines = 1
    #    add_redo = 1
    #
    #elif key == 'redo':#оно надо вообще?
    #    print('corrected_number_of_lines')
    #    print('redo')
    #    corrected_qt_number_of_lines = 1
    #    add_redo = 0

        print('enter end')
    else:#symbol
        print('important clue = ', at_block_end )
        if key == Qt.Key_Space:
            my_edit.undoStack.edit_type = 'space'
        else:
            my_edit.undoStack.edit_type = 'symbol'
        if at_block_end:
            #print('h= ', h)
            add_undo = 1
            if h:
                corrected_qt_number_of_lines = 1
                add_redo = 1
        #else:
        #    add_redo = 0
        #print('corrected_qt_number_of_lines = ', corrected_qt_number_of_lines)
    print('mladshii_block = ', mladshii_block)
    print('starshiy_block = ', starshiy_block)
    print('corrected_qt_number_of_lines = ', corrected_qt_number_of_lines)
    print('my_edit.blocks_before = ', my_edit.blocks_before)

    # есть следующая строка?
    if starshiy_block + corrected_qt_number_of_lines >= my_edit.blocks_before:# and not problem todo вылетать будет

        #corrected_qt_number_of_lines = 0

        corrected_qt_number_of_lines = corrected_qt_number_of_lines - 1
        if starshiy_block + corrected_qt_number_of_lines >= my_edit.blocks_before:# and not forbid:
            corrected_qt_number_of_lines = corrected_qt_number_of_lines - 1
        if corrected_qt_number_of_lines < 0:
            corrected_qt_number_of_lines = 0
        #corrected_qt_number_of_lines = abs(corrected_qt_number_of_lines - 1)
        print('666 corrected_qt_number_of_lines = ', corrected_qt_number_of_lines)

    #here should be add_undo = 0, but it is too early. we should end editting before checking. look in onChange
    if starshiy_block + add_undo == my_edit.blocks_before:# and not problem:#
        print('if starshiy_block + add_undo == my_edit.blocks_before:')
        add_undo = 0
    #print('tutt:? {} >= {}'.format(starshiy_block + corrected_qt_number_of_lines, my_edit.blocks_before))
    #print('add_undo ', add_undo)
    print('2 corrected_qt_number_of_lines = {}, starshiy_block = {}, mladshii_block = {}, add_undo = {}, add_redo = {}'.format(corrected_qt_number_of_lines, starshiy_block, mladshii_block, add_undo, add_redo))

    #print(f'2 corrected_qt_number_of_lines = {corrected_qt_number_of_lines}')
    #if my_edit.undoStack.edit_type == 'insert':
    #    print('fffffffffffffffffff999')
    #    return corrected_qt_number_of_lines+1, starshiy_block, mladshii_block, add_undo, add_redo

    return corrected_qt_number_of_lines, starshiy_block, mladshii_block, add_undo, add_redo
    #return 2, starshiy_block+1, mladshii_block, add_undo, add_redo
#my_edir.delete_line_corrector