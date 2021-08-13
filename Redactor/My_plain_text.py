from PyQt5.QtWidgets import QPlainTextEdit, QTextEdit, QWidget, QMenu
from PyQt5.QtCore import QRect, QSize, QEvent, Qt, QMimeData
from PyQt5.QtGui import QTextOption, QColor, QPainter,  QTextCharFormat,\
    QTextFormat,  QCursor, QKeySequence, QDropEvent
from Settings.settings import *
from Redactor.find_replace import finder
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
import pyautogui
from Redactor.Undo_redo import MyStack
from Menus.EditMenu import update_edit_menu
from Settings.settings import axises

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
        if text:
            self.setPlainText(text)
        self.changed = False
        #self.LastGCod = 0
        self.zoomIn(5)

        self.fmt = QTextCharFormat()
        self.fmt.setUnderlineColor(Qt.red)
        self.fmt.setUnderlineStyle(QTextCharFormat.SpellCheckUnderline)
        self.setPlaceholderText('Enjoy your work, please!')

        #number line
        self.lineNumberArea = QLineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
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
        #self.textChanged.connect(self.textChanged_check)
        #contex menu Settings
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.arithmetic_ones()

    def arithmetic_ones(self):
        self.corrected_qt_number_of_lines = 0
        #self.adding_lines = 1
        self.min_line_np = 1
        self.second_place = 1
        self.blocks_before = 1
        self.make_undo_work_1_time = 0

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
            dummyEvent = QDropEvent(e.posF(), e.possibleActions(),
                                          mimeData, e.mouseButtons(), e.keyboardModifiers())
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
        #self.setGeometry(QRect(cr.left(), cr.top() + 100, 1000, cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.yellow).lighter(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

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
        for i in range(2, 12):
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
            if self.undoStack.command(self.undoStack.index()).text() == 'glue':
                self.undoStack.child_count = 0
            self.undoStack.redo()
            self.rehighlightNextBlocks()

    def my_del(self):
        print('my_del21')
        if self.textCursor().hasSelection():
            self.blocks_before = self._document.blockCount()
            self.event_data_acquiring(Qt.Key_Delete)
            self.undoStack.storeFieldText()
            self.textCursor().removeSelectedText()
            self.rehighlightNextBlocks()

    def my_paste(self):
        #seems, it can not work directly, we need insertFromMimeData :((
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
        QPlainTextEdit.cut(self)
        self.rehighlightNextBlocks()

    def onChange(self, position, charsRemoved, charsAdded):
        """
                Тут необходимо добавить n_deleted_lines, n_highlighted_lines
                и pos1_del pos1_insert
                 в self.undoStack.command(self.undoStack.index()-1)
                """
        self.base.progress_bar.rehighlight = True
        if self.undoStack.edit_type == 'undo':  # only for undo redo зщщы2
            z = self.undoStack.command(self.undoStack.index() - 1)
            if z.childCount() > 0:
                z = z.child(self.undoStack.child_count)
                self.undoStack.child_count = self.undoStack.child_count - 1
            line1 = self._document.findBlock(z.pos1).blockNumber() + 1# for numpy
            line2 = self.undoStack.previous_max_line + 1# for deleting last
            line3 = self._document.findBlock(z.pos2).blockNumber() + 1
            self.min_line_np = line1
            self.second_place = line2 + z.add_undo #-1
            #self.delete_lines_from_main_np_g_pool()
            self.base.reading_lines_number = line3 - line1 + 1 + z.add_undo  # + z.corrected_qt_number_of_lines
            #self.base.np_box.delete_lines_from_np_box()
            #self.creating_np_pool()
            self.universal_replace_new()

        elif self.undoStack.edit_type == 'redo':
            z = self.undoStack.command(self.undoStack.index())
            if z.childCount() > 0:
                z = z.child(self.undoStack.child_count)
                self.undoStack.child_count = self.undoStack.child_count + 1
            line1 = self._document.findBlock(z.pos1).blockNumber() + 1
            line2 = self.undoStack.previous_max_line + 1
            line3 = self._document.findBlock(z.pos3).blockNumber() + 1
            self.min_line_np = line1
            self.second_place = line2 + z.add_redo
            self.base.reading_lines_number = line3 - line1 + 1 + z.add_redo#+ z.corrected_qt_number_of_lines #+ z.add_undo#+
            # self.delete_lines_from_main_np_g_pool()
            #self.base.np_box.delete_lines_from_np_box()
            #self.creating_np_pool()
            self.universal_replace_new()
        else:
            self.onChange_new_command(position)


    def onChange_new_command(self, position):
        self.changed = True
        self.change_position = position
        self.line_arithmetic()
        self.universal_replace_new()
        if self.make_undo_work_1_time == 1:
            self.make_undo_work_1_time = 2

    def line_arithmetic(self):#todo self.firstBlock возможно не нужен
        self.text_lines_delete = self.untilBlock - self.firstBlock + 1
        self.text_lines_insert = self.blockCount() - self.blocks_before + self.text_lines_delete
        self.min_line_np = self.firstBlock + 1
        self.np_lines_delete = self.text_lines_delete + self.corrected_qt_number_of_lines
        self.base.reading_lines_number = self.text_lines_insert + self.corrected_qt_number_of_lines
        self.second_place = self.min_line_np + self.np_lines_delete - 1

    def universal_replace_new(self):
        self.base.highlight.standart_step = 1#todo ЗАЧЕЕМ?!
        self.creating_np_pool()
        self.base.np_box.delete_lines_from_np_box()
        #self.delete_lines_from_main_np_g_pool()

    def creating_np_pool(self):
        #axis
        self.base.np_box.create_new_currents_in_np_box(axises)
        self.base.highlight.current_g_cod_pool = self.base.np_box.current_g_cod_pool
        self.base.progress_bar.setMaximum(self.base.reading_lines_number)
        self.base.highlight.too_little_number_check()


    def eventFilter(self, widget, event):
        if (event.type() == QEvent.KeyPress and widget is self):
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
                    self.my_redo()
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_Z:
                    print('отменить')
                    self.my_undo()
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_X:
                    print('Вырез')
                    self.my_cut()
                    return True
                if mod_sum == Qt.ControlModifier and event.key() == Qt.Key_V:
                    print('Вставка check')
            else:
                if event.text():
                    if key == Qt.Key_Backspace:
                        self.event_data_acquiring(key)
                        #self.undoStack.storeFieldText()
                        c = self.textCursor()
                        if c.hasSelection():
                            self.my_del()
                        else:
                            c.movePosition(c.PreviousCharacter, c.KeepAnchor)
                            self.setTextCursor(c)
                            self.my_del()
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
                        return True
                    else:
                        if key == Qt.Key_Space:
                            self.undoStack.merging_world()
                            print('space')
                        elif key == Qt.Key_Return or key == Qt.Key_Enter:
                            print('enter')
                        self.undoStack.last_edited = event.text()
                        self.event_data_acquiring(key)
                        self.undoStack.storeFieldText()
                        self.insertPlainText(self.undoStack.last_edited)
                        self.rehighlightNextBlocks()
                        return True
        return QWidget.eventFilter(self, widget, event)



    def event_data_acquiring(self, key, replace_to_nothing=False):
        self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock, self.undoStack.add_undo, self.undoStack.add_redo = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
            self, key, replace_to_nothing)
        print('self.firstBlock = ', self.firstBlock)
        #self.base.g_modal.create_current_from_g_modal(self.firstBlock)


    def rehighlightNextBlocks(self):
        #return
        print('rehighlight start')
        i = self.second_place + 1
        #g_old = self.LastGCod

        len = int(self.base.np_box.current_g_cod_pool.size/axises) + self.min_line_np-1
        g_new = self.base.np_box.main_g_cod_pool[len][0]
        lines = 0
        number_of_lines = self.blockCount() + 1
        while i < number_of_lines and self.base.np_box.main_g_cod_pool[i][0] != g_new and np.isnan(self.base.np_box.main_g_cod_pool[i][9]):
                #self.base.main_g_cod_pool[i][0] == g_old: #and self.base.main_g_cod_pool[i][0] == g_old:
            lines = lines + 1
            i = i + 1
        if lines == 0:# or self.second_place == number_of_lines:
            print('rehighlight end0')
            return
        #now we know how many lines should be rehighlighted
        self.base.reading_lines_number = lines#lines
        #self.base.progress_bar.setValue(0)
        self.base.highlight.to_the_start()
        self.base.progress_bar.setMaximum(lines-1)#lines-1
        #self.creating_np_pool()
        self.min_line_np = self.second_place + 1
        self.second_place = self.second_place + lines
        self.universal_replace_new()
        #self.base.np_box.main_g_cod_pool = np.delete(self.base.np_box.main_g_cod_pool,
        #                                      np.s_[self.min_line_np:i], axis=0)#todo maybe i can be too mach
        n = self.min_line_np
        while n < i:
            self.base.highlight.rehighlightBlock(self._document.findBlockByNumber(n-1))
            n = n + 1
        print('rehighlight end1')

    def insertFromMimeData(self, source):
        #мы можем сюда напрямую кинуть source

        if source.hasText():
            #self.undoStack.edit_type = 'insert'
            self.event_data_acquiring('insert')
            self.undoStack.last_edited = source.text()#insert_txt
            self.undoStack.storeFieldText()
            QPlainTextEdit.insertFromMimeData(self, source)
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
