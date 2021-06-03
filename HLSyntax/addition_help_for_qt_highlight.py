from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

def corrected_number_of_lines(my_edit, key, replace_to_nothing):
    print('writing key used')
    corrected_qt_number_of_lines = 0
    add_redo = 0
    add_undo = 0
    my_cursor = my_edit.textCursor()
    pos1 = my_cursor.position()
    pos2 = my_cursor.anchor()

    h = my_cursor.hasSelection()
    b = my_cursor.atBlockEnd()
    #anchor_pos = my_cursor.anchor()
    my_cursor.setPosition(pos2)
    c = my_cursor.atBlockEnd()
    #univerasal part
    starshiy = max(pos1, pos2)
    mladshii = min(pos1, pos2)
    mladshii_block = my_edit._document.findBlock(mladshii).blockNumber()
    starshiy_block = my_edit._document.findBlock(starshiy).blockNumber()
    if starshiy == pos1:
        important_clue = b
    else:
        important_clue = c

    if key == Qt.Key_Backspace:
        my_edit.undoStack.edit_type = 'backspace'
        print('Backspace')
        if my_cursor.atBlockStart() and not h:
            print('tut problema bila')
            mladshii_block = mladshii_block - 1#backspace in the beginning of the line will update previous line too
        if important_clue and not starshiy_block + 1 == my_edit.blockCount():
            corrected_qt_number_of_lines = 1
            add_redo = 1

    elif key == 'insert':
        print('insert11')
        my_edit.undoStack.edit_type = 'insert'
        if important_clue:
            add_undo = 1
            if h:
                corrected_qt_number_of_lines = 1
                add_redo = 1

    elif key == 'replace':
        print('replace11')
        my_edit.undoStack.edit_type = 'replace'
        if important_clue:
            if not replace_to_nothing:
                add_undo = 1
            if h:
                corrected_qt_number_of_lines = 1
                add_redo = 1

    elif key == 'cut':
        print('cut1')
        my_edit.undoStack.edit_type = 'cut'
        if important_clue and h:
            corrected_qt_number_of_lines = 1
            add_redo = 1
            print('add_redo = 1')

    elif key == Qt.Key_Delete:
        print('Delete')
        my_edit.undoStack.edit_type = 'delete'
        #if important_clue and not h:
        #    starshiy_block = starshiy_block + 1#delete BEFORE the end of the line will update next line too.
        print('my_cursor.positionInBlock() + 1= {}, my_cursor.block().length() = {}'.format(my_cursor.positionInBlock() + 2, my_cursor.block().length()))
        if not h and my_cursor.positionInBlock() + 2 == my_cursor.block().length():
            corrected_qt_number_of_lines = 1
            add_redo = 1
        elif important_clue and not starshiy_block + 1 == my_edit.blockCount():#h and
            corrected_qt_number_of_lines = 1
            add_redo = 1

    elif key == Qt.Key_Enter or key == Qt.Key_Return:
        print('enter')
        my_edit.undoStack.edit_type = 'enter'
        add_undo = 1
        if h and important_clue:
            corrected_qt_number_of_lines = 1
            add_redo = 1

    else:#symbol
        print('important clue = ', important_clue )
        if key == Qt.Key_Space:
            my_edit.undoStack.edit_type = 'space'
        else:
            my_edit.undoStack.edit_type = 'symbol'
        if important_clue:
            print('h= ', h)
            add_undo = 1
            if h:
                corrected_qt_number_of_lines = 1
                add_redo = 1
        print('corrected_qt_number_of_lines = ', corrected_qt_number_of_lines)

    # есть следующая строка?
    if starshiy_block + corrected_qt_number_of_lines == my_edit.blocks_before:
        corrected_qt_number_of_lines = 0
    #here should be add_undo = 0, but it is too early. we should end editting before checking. look in onChange
    if starshiy_block + add_undo == my_edit.blocks_before:
        add_undo = 0
    print('tutt:? {} >= {}'.format(starshiy_block + corrected_qt_number_of_lines, my_edit.blocks_before))
    print('add_undo ', add_undo)
    return corrected_qt_number_of_lines, starshiy_block, mladshii_block, add_undo, add_redo
#my_edir.delete_line_corrector