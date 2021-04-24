
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

def corrected_number_of_lines(my_edit, key):
    print('writing key used')
    a = 0
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
        print('Backspace')
        if my_cursor.atBlockStart() and not h:
            print('tut problema bila')
            mladshii_block = mladshii_block - 1#backspace in the beginning of the line will update previous line too
        #a = a + 1
        if important_clue and not starshiy_block + 1 == my_edit.blockCount():
            a = a + 1
    elif key == Qt.Key_Delete:
        print('Delete')
        if b and not h:
            starshiy_block = starshiy_block + 1#delete on the end of the line will update next line too
        if h and important_clue and not starshiy_block + 1 == my_edit.blockCount():
            a = a + 1
    elif key == Qt.Key_Enter or Qt.Key_Return:
        print('enter')

        if h and important_clue:
            a = a + 1
    elif key == 'Undo':#todo
        print('QKeySequence.Undo шляпа')


    else:#symbol
        if h and important_clue:
            a = a + 1
    print('key was', key)
    print('И вот a = ', a)
    return a, starshiy_block, mladshii_block, my_edit._document.blockCount()
#my_edir.delete_line_corrector