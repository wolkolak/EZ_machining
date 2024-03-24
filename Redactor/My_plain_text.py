from PyQt5.QtWidgets import  QTextEdit, QWidget, QMenu, QPlainTextEdit
#from PyQt6.QtWidgets import QPlainTextEdit

from PyQt5.QtCore import QRect, QSize, QEvent, Qt, QMimeData
from PyQt5.QtGui import QTextOption, QColor, QPainter,  QTextCharFormat,\
    QTextFormat,  QCursor, QKeySequence, QDropEvent, QTextDocument
from Settings.settings import *
from Redactor.find_replace import finder
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
import pyautogui
from Redactor.Undo_redo import MyStack
from Menus.EditMenu import update_edit_menu
from Settings.settings import axises
from left_zone.connect_editor_left_zone import point_dot_from_line
import time
import copy
from Redactor.useful_things4redactor import find_last_in_block

from Redactor.useful_things4redactor import IterDialog

class MyEdit(QPlainTextEdit):

    def __init__(self, text, tab_, base, existing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ xyzcba"""
        #modal coomnds
        self.tab_ = tab_
        self.base = base
        self.setWordWrapMode(QTextOption.NoWrap)
        self.existing = existing
        self.start_point = None#todo
        self.setStyleSheet("background-color: {}".format(color4))
        print('55 existing = ', existing)
        if text:
            #self.setExtraSelections({})
            #nyak = QTextDocument()
            #self.setDocument(nyak)
            #nyak.setPlainText(text)
            self.setPlainText(text)
            #self.setExtraSelections({})

        #self.after_rehighlight = False
        self.changed = False
        self.zoomIn(5)
        print('here my check 1')
        self.line_iter = 0
        self.after_solving = False
        self.fmt = QTextCharFormat()
        self.fmt.setUnderlineColor(Qt.red)
        self.fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.setPlaceholderText('Enjoy your work, please')

        #number line
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.cursorPositionChanged.connect(self.highlightCurrentLine_chooseNewDot)
        self.updateLineNumberAreaWidth(0)
        self.setAcceptDrops(True)

        self.updateRequest.connect(self.updateLineNumberArea)
        self.installEventFilter(self)
        self._document = self.document()
        #undo/redo
        self.undoStack = MyStack(self)
        self.undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        self.undoAction.setShortcuts(QKeySequence.Undo)
        self.redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        self.redoAction.setShortcuts(QKeySequence.Redo)

        self._document.contentsChange.connect(self.onChange)
        #self.document().contentsChange.connect(self.onChange)
        #self.textChanged.connect(self.textChanged_check)
        #contex menu Settings
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.arithmetic_ones()
        print('nyaaak')
        #g = 'fgfd/dd'

            #self.current_catalog_vars =
        #print('self.current_catalog_vars = ', self.current_catalog_vars)
        #self.processor_change_toggle = False


        #1self.base.Logs.hide()
        #self.base.progress_bar.show()
        print('here my check 2')

    def arithmetic_ones(self):
        self.corrected_qt_number_of_lines = 0
        #self.adding_lines = 1
        self.min_line_np = 1
        self.second_place = 1
        self.blocks_before = 1
        #self.make_undo_work_1_time = 0

    def find_in_text(self):
        self.rez = finder(self).show()

    def replace_in_text(self):
        self.rez = finder(self, 1).show()

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        # self.addItem(e.mimeData().text())
        mime = e.mimeData()
        nya = mime.text()
        if nya[:8] == 'file:///':
            nya = nya[8:]
            self.tab_.make_open_DRY(nya)
        else:
            self.undoStack.edit_type = 'glue'
            self.undoStack.beginMacro('glue')
            self.my_del()
            u = self.cursorForPosition(e.pos())
            self.setTextCursor(u)
            self.insertFromMimeData(mime)
            self.undoStack.endMacro()
            print(' drop event: ', nya)
            #i do not know how to override proposed event, so i am making another hollow event to unfreeze text cursor
            mimeData = QMimeData()
            mimeData.setText("")
            dummyEvent = QDropEvent(e.posF(), e.possibleActions(), mimeData, e.mouseButtons(), e.keyboardModifiers())
            QPlainTextEdit.dropEvent(self, dummyEvent)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine_chooseNewDot(self):#todo here add things
        print('highlightCurrentLine_chooseNewDot')
        #return
        if self.after_solving:
            print('self.after_solving is True')
            extraSelections = []
            iter = self.line_iter
            print('highlightCurrentLine_chooseNewDot iter = ', iter)
            #sec_doc = self.document().Ex
            self.extraSelections().clear()

            if not self.isReadOnly():
                selection = QTextEdit.ExtraSelection()
                lineColor = QColor(Qt.yellow).lighter(160)
                selection.format.setBackground(lineColor)
                selection.cursor = self.textCursor()

                selection.format.setProperty(QTextFormat.FullWidthSelection, True)
                #FFFFFFFFFFFFFoooooooooooooooooooo
                #selection.format.setProperty(QTextFormat.FullWidthSelection, False)
                #selection.cursor.clearSelection()

                extraSelections.append(selection)

                self.setExtraSelections(extraSelections)
                #self.setExtraSelections({})
                #return
                point_dot_from_line(self.base.np_box, selection.cursor.blockNumber(), self.tab_.center_widget.left, iter=iter)#self.textCursor()
            #else:
            #    selection = self.extraSelections()[0]
            #    #selection.cursor = self.textCursor()
            #    selection.format.setProperty(QTextFormat.FullWidthSelection, False)
            # point_dot_from_line(selection.cursor.blockNumber(), self.tab_.center_widget.left)   #self.main_interface.centre.left.left_tab.parent_of_3d_widget.openGL
            # print(f'selection color = {selection.format.background().color().getRgb()}')
            # print(f'main cursor = {self.textCursor()}')
            # print(f'selection.cursor = {selection.cursor}')

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter.fillRect(event.rect(), Qt.lightGray)
        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), height, Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def __contextMenu(self):
        update_edit_menu(self.base.tab_.center_widget.app, self.tab_.currentIndex())
        self._normalMenu = QMenu()
        self._addCustomMenuItems(self._normalMenu, self.base.tab_.center_widget.app.editMenu)
        self._normalMenu.exec_(QCursor.pos())

    def _addCustomMenuItems(self, new_menu1, old_menu):
        for i in range(2, 14):
            new_menu1.addAction(old_menu.actions()[i])

    def my_undo(self):
        print('undo21')
        if self.undoStack.canUndo():
            if self.undoStack.command(self.undoStack.index()-1).text() == 'glue':# todo
                self.undoStack.child_count = self.undoStack.command(self.undoStack.index()-1).childCount() - 1
            self.undoStack.undo()
            self.rehighlightNextBlocks()

    def my_redo(self):
        print('redo21')
        if self.undoStack.canRedo():
            self.undoStack.redo()
            print('ttt')
            self.rehighlightNextBlocks()

    def my_del(self):
        print('my_del21')
        if self.textCursor().hasSelection():
            print(f'selection has: |{self.textCursor().selectedText()}|')
            print(f'len of selection in my_del = {len(self.textCursor().selectedText())}')
            self.blocks_before = self._document.blockCount()
            print(f'self.blocks_before = {self.blocks_before}')
            self.event_data_acquiring(Qt.Key_Delete)
            print('acquiring success')
            self.undoStack.storeFieldText()

            print('storeddd?')
            self.textCursor().removeSelectedText()
            print('removed&??')
            #self.rehighlightNextBlocks()


    def my_paste(self):
        #seems, it can not work directly, we need insertFromMimeData :((
        #insertFromMimeData

        QPlainTextEdit.paste(self)

    def my_select_all(self):
        print('my chose21')
        pyautogui.hotkey('ctrl', 'a')

    def my_copy(self):
        print('my copy21')
        pyautogui.hotkey('ctrl', 'c')

    def my_cut(self):
        print('my cut21')
        self.undoStack.last_edited = ''
        self.event_data_acquiring('cut')
        self.undoStack.storeFieldText()
        self.undoStack.storeFieldText()
        QPlainTextEdit.cut(self)
        self.rehighlightNextBlocks()

    def my_iter(self):
        print('my_iter')

        self.iter_dialog = IterDialog(self).show()



    def onChange(self, position):#, charsRemoved, charsAdded
        print('onChange started')
        #time.sleep(1)
        #self.setExtraSelections({})
        self.base.editor.after_solving = False
        self.base.progress_bar.rehighlight = True
        if self.undoStack.edit_type == 'undo':  # only for undo redo зщщы2
            print('on change undo')
            z = self.undoStack.command(self.undoStack.index() - 1)
            if z is None:
                return
            if z.childCount() > 0:
                z = z.child(self.undoStack.child_count)
                self.undoStack.child_count = self.undoStack.child_count - 1
            line1 = self._document.findBlock(z.pos1).blockNumber() + 1# for numpy
            line2 = self.undoStack.previous_max_line + 1#+1 for deleting last ОБЫЧНО + 1. ПРОБЛЕМА С ВСТАВКОЙ ТЕКСТА В ПЕРВУЮ СТРОКУ
            line3 = self._document.findBlock(z.pos2).blockNumber() + 1
            self.min_line_np = line1
            self.second_place = line2 + z.add_undo #-2
            #надо -2 чтобы работало.
            #а для reading_lines_number не надо ((((
            print(f'ppp z.add_undo = {z.add_undo}')
            print('onChange1: |second_place = ', self.second_place)
            self.base.reading_lines_number = line3 - line1 + 1 + z.add_undo # + z.corrected_qt_number_of_lines
            print(f'here line number = {self.base.reading_lines_number}')
            print('1')
            self.universal_replace_new()
            self.min_line_np = self.min_line_np  #+1
            #что то здесь???

        elif self.undoStack.edit_type == 'redo':# тут неверно подсчитывается макимум для для count
            print('on change redo')#ТОЛЬКО REDO redo
            z = self.undoStack.command(self.undoStack.index())
            if z.childCount() > 0:
                z = z.child(self.undoStack.child_count)
                self.undoStack.child_count = self.undoStack.child_count + 1
            line1 = self._document.findBlock(z.pos1).blockNumber() + 1
            line2 = self.undoStack.previous_max_line #+ 1
            line3 = self._document.findBlock(z.pos3).blockNumber() + 1
            self.min_line_np = line1
            self.second_place = line2 + z.add_redo#-1????????
            print('z.text() = ', z.text())
            kostil = 1 if (z.text() == 'symbol' or z.text() == 'space' or z.text() == 'delete') else 0
            self.base.reading_lines_number = line3 - line1 + z.add_redo + kostil#+1#if +1 no working with insert
            self.universal_replace_new()
        else:
            #print('||| onChange_new_command |||')
            #print('charsRemoved = {}, charsAdded = {}, position {}'.format(charsRemoved, charsAdded, position))
            #if self.processor_change_toggle:
            #    self.processor_change_toggle = False
            #    print('||||     self.change = ', self.changed)
            #else:
            print(f'263 было : ')#{self.base.np_box.main_g_cod_pool}')
            if hasattr(self, 'untilBlock'):
                self.onChange_new_command(position)
        self.base.choose_Logs_or_progress_show(logs_s=False)
        print('onChange ended')


    def onChange_new_command(self, position):
        print('onChange_new_command start')
        #hh = 5 / 0
        #if hasattr(self, 'untilBlock'):
        self.changed = True

        self.change_position = position
        self.line_arithmetic()
        print('3')
        self.universal_replace_new()
        print('onChange_new_command end')
        #if self.make_undo_work_1_time == 1:
        #    self.make_undo_work_1_time = 2

    def line_arithmetic(self):#todo self.firstBlock возможно не нужен
        self.text_lines_delete = self.untilBlock - self.firstBlock + 1
        self.text_lines_insert = self.blockCount() - self.blocks_before + self.text_lines_delete
        self.min_line_np = self.firstBlock + 1
        self.np_lines_delete = self.text_lines_delete + self.corrected_qt_number_of_lines
        self.base.reading_lines_number = self.text_lines_insert + self.corrected_qt_number_of_lines
        self.second_place = self.min_line_np + self.np_lines_delete - 1 #+ self.text_lines_insert
        #self.second_place = self.min_line_np + self.text_lines_insert - self.np_lines_delete - 1  # +
        print('line_arithmetic: |second_place = ', self.second_place)

    def universal_replace_new(self):
        print('universal_replace_new start')
        #5/0
        #print(f'было : {self.base.np_box.main_g_cod_pool}')
        self.base.highlight.standart_step = 1#todo ЗАЧЕЕМ?!
        self.creating_np_pool()

        self.base.np_box.delete_lines_from_np_box()
        #self.textCursor().blockNumber()
        print('universal_replace_new end')
        #print('reading_lines_number = {}, max = {}'.format(self.base.reading_lines_number, self.base.progress_bar.maximum()))

    def creating_np_pool(self):
        #axis
        print('creating_np_pool')
        self.base.np_box.create_new_currents_in_np_box(axises)
        self.base.highlight.current_g_cod_pool = self.base.np_box.current_g_cod_pool
        self.base.progress_bar.setMaximum(self.base.reading_lines_number)
        #Здесь, навреное не нужно
        self.base.highlight.too_little_number_for_big_step_check()#self.standart_step = self.base.reading_lines_number хз зачем вообще
        #print('creating_np_pool end, self.base.highlight.current_g_cod_pool = ', self.base.highlight.current_g_cod_pool)


    def eventFilter(self, widget, event):
        #print('event = ', event.type())
        #if hasattr(self.base, 'np_box'):
        #    print(f'eventFilter было : {self.base.np_box.main_g_cod_pool}')

        if (event.type() == QEvent.KeyPress and widget is self):
            #self.after_rehighlight = False#todo Опустил на уровень
            key = event.key()
            self.blocks_before  = self._document.blockCount()
            if Qt.KeypadModifier:
                print('KeypadModifie', int(event.modifiers()))
            mod_sum = int(event.modifiers())
            if mod_sum > 0 and mod_sum != Qt.ShiftModifier and mod_sum != Qt.KeypadModifier \
                    and mod_sum != Qt.ShiftModifier + Qt.KeypadModifier:
                print('модификаторы кроме шифта')
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_Y or \
                        mod_sum == Qt.ControlModifier + Qt.ShiftModifier and event.key() == Qt.Key_Z:
                    print('вернуть')
                    self.my_redo()#rehighlightNextBlocks() already inside
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_Z:
                    print('отменить')
                    self.my_undo()
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_X:
                    print('Вырез')
                    self.my_cut()#rehighlightNextBlocks() already inside
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_V:
                    print('Вставка check')
                    self.my_paste()#не помогает
                    return True#не помогает

                    #mime = event.mimeData()
                    #event.
                    #self.insertFromMimeData(mime)
                    #return True

            else:
                if event.text():
                    if key == Qt.Key_Backspace:
                        self.event_data_acquiring(key)
                        #self.undoStack.storeFieldText()
                        c = self.textCursor()
                        if c.hasSelection():
                            self.my_del()#тут что то неверно, скорее всего
                        else:
                            c.movePosition(c.PreviousCharacter, c.KeepAnchor)
                            self.setTextCursor(c)
                            self.my_del()
                        self.rehighlightNextBlocks()
                        return True
                    elif key == Qt.Key_Delete:
                        self.event_data_acquiring(key)
                        #self.undoStack.storeFieldText()
                        c = self.textCursor()
                        if c.hasSelection():
                            self.my_del()
                        else:
                            c.movePosition(c.NextCharacter, c.KeepAnchor)
                            self.setTextCursor(c)
                            self.my_del()
                        self.rehighlightNextBlocks()
                        return True
                    else:
                        if key == Qt.Key_Space:
                            self.undoStack.merging_word()
                            print('space')
                        elif key == Qt.Key_Return or key == Qt.Key_Enter:
                            print('enter')
                        self.undoStack.last_edited = event.text()
                        self.event_data_acquiring(key)
                        self.undoStack.storeFieldText()

                        self.insertPlainText(self.undoStack.last_edited)
                        print('this is problematick rehighlight')
                        self.rehighlightNextBlocks()
                        return True
        #self.base.progress_bar.show()
        #1self.base.Logs.hide()
        return QWidget.eventFilter(self, widget, event)#for not text events - resize, change position, etc

    #def event_data_acquiring_redo(self, key, replace_to_nothing=False):
    #    self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock, self.undoStack.add_undo, self.undoStack.add_redo = \
    #        HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines_redo(self, key, replace_to_nothing)

    def event_data_acquiring(self, key, replace_to_nothing=False):#, oncoming_command=None
        self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock, self.undoStack.add_undo, self.undoStack.add_redo = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
            self, key, replace_to_nothing)#, oncoming_command
        print(f'self.corrected_qt_number_of_lines = {self.corrected_qt_number_of_lines}, self.untilBlock = {self.untilBlock}, '
              f'self.firstBlock = {self.firstBlock}, self.undoStack.add_undo = {self.undoStack.add_undo}, self.undoStack.add_redo = {self.undoStack.add_redo}')

    def rehighlightNextBlocks(self):#todo надо переподсвечивать будет только до следующего оператора.
        # todo Ибо расчёты все будут проведены заново с нуля внутри нампи бокса
        """
        refresh how to render syntax text, after changing
        :return:
        """
        #self.base.np_box.special_options_applying()
        #self.base.np_box.after_rehighlight = True
        #return
        print('rehighlightNextBlocks start')

        #2/0
        #self.after_rehighlight = False#TODO нужно поднять это до rehigh
        #self.base.np_box.after_rehighlight = True
        i = self.second_place +1
        #n_frame_type = 16
        n_new_operation = 2
        lines = 0
        number_of_lines = self.blockCount() + 1# -1
        if i < number_of_lines:     # dog-nail for key 'return'. no idea how to do better. looking for second G1/G0, not first
            print('cycle1')
            lines = lines + 1
            i = i + 1
        print('i = ', i)
        print(f'PPPPPPPPPPPPP = {self.base.reading_lines_number}')
        print(f'PPPPPPPPPPPP self.base.np_box.main_g_cod_poo = {self.base.np_box.main_g_cod_pool}')
        print(f'PPPPPP self.min_line_np = {self.min_line_np}')
        print(f'PPPPPPPPPPPP self.second_place = {self.second_place}')
        print(f'PPPPPPPPPP i = {i}, number_of_lines = {number_of_lines}')
        #где искать:
        #
        #
        #self.base.reading_lines_number < 5 and
        #if more than 4 lines after edited part
        #if

        if self.second_place > 2 and i+4 < number_of_lines and find_last_in_block(self.base.np_box.main_g_cod_pool[self.second_place:self.second_place+3], len_current_np=3, direction=1) \
                == find_last_in_block(self.base.np_box.main_g_cod_pool[i:i + 4], len_current_np=3, direction=0):
            #TODO было - find_last_in_block(self.base.np_box.main_g_cod_pool[self.min_line_np:self.second_place+1], поменял ибо замена строки вышибала. Не думал
            lines = 0
        else:
            print(f'number_of_lines = {number_of_lines}')#todo IndexError: index 59 is out of bounds for axis 0 with size 53
            while i < number_of_lines and (np.isnan(self.base.np_box.main_g_cod_pool[i][n_new_operation]) ):#or not np.isnan(self.base.np_box.main_g_cod_pool[i][n_frame_type])):#Сравнить показатели X, Y, Z, A, B, C
                print('cycle2, i = ', i)
                lines = lines + 1
                #nen
                i = i + 1
        if lines == 0 :
                self.base.progress_bar.setMaximum(self.base.progress_bar.maximum())
                #self.after_rehighlight = True
                self.base.np_box.special_options_applying()
                #self.base.np_box.after_rehighlight = False

                #self.base.tab_.center_widget.left.update_visible_np_left()

                #self.base.highlight.to_the_start()
                #print('setValue(0)')
                #self.base.progress_bar.setValue(0)
                #if self.base.sub1:#TODO здесь может быть бесполезно
                #    print('дичь43')
                #    self.base.father_np_box.special_options_applying()
                print('rehighlightNextBlocks end2')
                return

        self.base.reading_lines_number = lines#lines
        #if lines >0:
        #    lines -=1
        self.base.highlight.to_the_start()
        self.base.progress_bar.setMaximum(lines-1)#lines-1
        self.min_line_np = self.second_place + 1
        #self.min_line_np = self.second_place + 1 if lines > 0 else self.min_line_np
        self.second_place = self.second_place + lines
        print('4')
        self.universal_replace_new()
        n = self.min_line_np
        while n < i:
            self.base.highlight.rehighlightBlock(self._document.findBlockByNumber(n-1))
            n = n + 1
        #self.after_rehighlight = True
        self.base.np_box.special_options_applying()

        #if self.base.sub1:#TODO здесь может быть бесполезно
        #    print('дичь4')
        #    self.base.father_np_box.special_options_applying()

        #self.highlightCurrentLine_chooseNewDot()
        print('rehighlightNextBlocks end')

        #self.base.progress_bar.hide()
        #self.base.Logs.show()

        #self.base.np_box.special_options_applying()
        #new arithmetic need to be done in np_box


    def insertFromMimeData(self, source):
        if source.hasText():
            #вот тут что то починить
            print('insertFromMimeData')
            self.event_data_acquiring('insert')
            self.undoStack.last_edited = source.text()#insert_txt
            self.undoStack.storeFieldText()
            QPlainTextEdit.insertFromMimeData(self, source)
            #self.min_line_np =
            print(f'self.insert_dognail = {self.insert_dognail}')
            self.second_place = self.textCursor().blockNumber()+1#+self.insert_dognail

            self.rehighlightNextBlocks()

class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        self.setFont(font1)

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)
