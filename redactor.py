from PyQt5.QtWidgets import QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QTextEdit, QWidget, QApplication, QFrame, QVBoxLayout, QBoxLayout, QProgressBar, QAction
from PyQt5.QtCore import QRect, QSize, QTimer, QThread, QThreadPool, pyqtSlot, QEvent, Qt, pyqtSignal
from PyQt5.QtGui import QTextOption, QColor, QPainter, QClipboard, QTextCursor, QTextDocument, QTextCharFormat,\
    QTextFormat, QGuiApplication, QKeySequence,QContextMenuEvent, QInputEvent, QMouseEvent, QCursor, QKeyEvent
from settings import *
from find_replace import finder
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import flow
import runnable_flow
import numpy as np
import time
import pyautogui


class QLineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor
        self.setFont(font1)

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)


class MyEdit(QPlainTextEdit):

    def __init__(self, text, tab_, base, existing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ xyzcba"""

        self.flag_modificationChanged_workaround = True


        #modal coomnds
        self.g_modal = np.array([0], float)

        self.tab_ = tab_
        self.base = base
        self.setWordWrapMode(QTextOption.NoWrap)
        self.existing = existing
        self.start_point = None#todo
        self.setStyleSheet("background-color: {}".format(color4))
        if text:
            self.setPlainText(text)
        self.changed = False
        self.modificationChanged.connect(self.changing)
        #self.document().setModified(False)
        #self.modificationChanged.disconnect(self.document().codeModificationChanged)

        self.zoomIn(5)
        #self.setTextBackgroundColor(Qt.lightGray)

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
        #self.previousBlockCount = 1

        self.updateRequest.connect(self.updateLineNumberArea)
        print('self.blockCount() = ', self.blockCount())
        self.installEventFilter(self)
        self._document = self.document()

        self._document.contentsChange.connect(self.onChange)
        #contex menu settings
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__contextMenu)
        self.arithmetic_ones()

    def arithmetic_ones(self):
        self.corrected_qt_number_of_lines = 0
        self.adding_lines = 1
        self.min_line_np = 1
        self.second_place = 1
        self.blocks_before = 1
        self.make_undo_work_1_time = 0

    def find_in_text(self):
        self.rez = finder(self).show()

    def dragEnterEvent(self, e):

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        # self.addItem(e.mimeData().text())
        nya = e.mimeData().text()
        if nya[:8] == 'file:///':
            nya = nya[8:]
            self.tab_.make_open_DRY(nya)
        else:
            QPlainTextEdit.dropEvent(self, e)
        print(nya)

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
            """        if rect.contains(self.viewport().rect()):
            pass
            self.updateLineNumberAreaWidth(0)"""

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
        self._menu_to_borrow = self.createStandardContextMenu()
        self._normalMenu = self.createStandardContextMenu()
        self._addCustomMenuItems(self._normalMenu)
        self._normalMenu.exec_(QCursor.pos())

    def _addCustomMenuItems(self, menu):
        #self.my_undo_action = QAction("My Undo", self)
        #self.my_undo_action.triggered.connect(self.my_undo)

        self.my_redo_action = QAction("My Redo", self)
        self.my_redo_action.triggered.connect(self.my_redo)
        menu.removeAction(menu.actions()[0])
        menu.removeAction(menu.actions()[0])
        menu.insertAction(menu.actions()[0], self.my_redo_action)
        menu.insertAction(menu.actions()[0], self.base.tab_.center_widget.)

    def my_undo(self):
        print('undo21')
        QPlainTextEdit.undo(self)
        #в стек запомнить длину удаленного, добавленного в строках. место заполнится без моего участия
        #pyautogui.hotkey('ctrl', 'z')

    def my_redo(self):
        pyautogui.hotkey('ctrl', 'y')

    #pyqtSlot()
    def changing(self):
        """С одной стороны я хочу отслеживать изменения в документе, с другой - отслеживать их момент.
        Не знаю как выставить верную стратегию изменений документа (сигнал приходит дважды),
        посему - чётные изменения я буду игнорировать"""

        #if self.flag_modificationChanged_workaround is False:
        #    self.flag_modificationChanged_workaround = True
        #    #print('Ветка False')
        #    return

        print('changing')
        self.changed = True



    def onChange(self, position, charsRemoved, charsAdded):
        """
        Я думаю, нужно сначала удалить из numpy лишнее, потому указать место вставки. Логично? вроде - да
        А если в данный момент мы уже читаем некий участок?  Тогда этот новый участок будет вставлен не там, так?
        Значит, сначала красим текст, потом вставляем и удаляем единовременно. Где беда?
        Если добавлены изменения пока идёт покраска участка. Что делать?
        В очередь. И? Новый onchange должен запустить процессы после того как работа с прерыдущим участком будет закончена?

        Допустим, очередь в 2 возможных подсчёта. Алгоритм сложный но реальный.
        Иная проблема - onChange принимает мало данных. нельзя поличить вторую position или можно? нука. Вроде
        работает

        """
        #time.sleep(5)
        print('выспался')
        self.change_position = position
        #арифметика
        self.line_arithmetic()
        self.universal_replace_new()
        if self.make_undo_work_1_time == 1:
            self.make_undo_work_1_time = 2

    def line_arithmetic(self):
        self.text_lines_delete = self.untilBlock - self.firstBlock + 1
        print('self.untilBlock = {}, self.firstBlock = {}'.format(self.untilBlock, self.firstBlock ))
        self.text_lines_insert = self.blockCount() - self.blocks_before + self.text_lines_delete
        print('text_lines_delete = {}, text_lines_insert = {}'.format(self.text_lines_delete, self.text_lines_insert))

        self.min_line_np = self.firstBlock + 1
        self.np_lines_delete = self.text_lines_delete + self.corrected_qt_number_of_lines - self.adding_lines #+ 1
        print('text_lines_delete = {}, self.corrected_qt_number_of_lines = {}, self.adding_lines = {}'.format(self.text_lines_delete, self.corrected_qt_number_of_lines, self.adding_lines))
        self.base.reading_lines_number = self.text_lines_insert + self.corrected_qt_number_of_lines - self.adding_lines #+1
        print('self.base.reading_lines_number', self.base.reading_lines_number)
        self.second_place = self.min_line_np + self.np_lines_delete - 1
        #self.second_place = self.min_line_np + self.np_lines_delete - self.adding_lines
        print('self.min_line_np = ', self.min_line_np)
        print('self.np_lines_delete = ', self.np_lines_delete )
        #self.untilBlock - self.text_lines_delete + self.corrected_qt_number_of_lines

    def universal_replace_new(self):
        self.base.highlight.standart_step = 1
        #self.find_lines_to_replace()
        self.creating_np_pool()
        self.delete_lines_from_main_np_g_pool()

    def creating_np_pool(self):
        self.base.current_g_cod_pool = np.zeros((self.base.reading_lines_number, 7), float)
        self.base.current_g_cod_pool[:] = np.nan
        self.base.progress_bar.setMaximum(self.base.reading_lines_number)
        self.base.highlight.too_little_number_check()

    def delete_lines_from_main_np_g_pool(self):
        print('min_line = ', self.min_line_np)
        print('было: ', self.base.main_g_cod_pool.shape)
        print('удалить строго диапазон: c {} по {} включительно'.format(self.base.main_g_cod_pool[self.min_line_np],                                                              self.second_place))
        self.base.main_g_cod_pool = np.delete(self.base.main_g_cod_pool, np.s_[self.min_line_np:self.second_place + 1], axis=0)
        print('стало: ', self.base.main_g_cod_pool.shape)


    def eventFilter(self, widget, event):
        # должен ссылаться на универсальную замену текста
        #print('event.type() = ', event.type())


        if (event.type() == QEvent.KeyPress and widget is self):
            key = event.key()

            self.blocks_before  = self._document.blockCount()
            if Qt.KeypadModifier:
                print('KeypadModifie', int(event.modifiers()))
            mod_sum = int(event.modifiers())
            if mod_sum > 0 and mod_sum != Qt.ShiftModifier and mod_sum != Qt.KeypadModifier \
                    and mod_sum != Qt.ShiftModifier + Qt.KeypadModifier:
                print('модификаторы кроме шифта')

                if event.key() == (Qt.Key_Control and Qt.Key_X):
                    print('Вырез')
                self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
                    self, key='cut')

                #if event.key() == (Qt.Key_Control and Qt.Key_Z):
                #    self.my_undo()
            else:
                if event.text():
                    self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock= HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(self, key)
            if self._document.isModified():
                print('was modified')
                self._document.setModified(False)

        return QWidget.eventFilter(self, widget, event)


    def insertFromMimeData(self, source):
        # должен ссылаться на универсальную замену текста
        self.blocks_before = self._document.blockCount()

        if source.hasText():
            self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
               self, key='insert')
            print('paaaste: ')
            QPlainTextEdit.insertFromMimeData(self, source)

class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()
        self.base = base
        self.valueChanged.connect(self.finish_current_batch)


    def finish_current_batch(self, current_value):
        self.base.highlight.count_in_step = 0
        print('progressbar finish current batch Hcount ', self.base.highlight.count)

        if current_value == self.maximum():
            self.inserting_in_main_g_cod()
            print('Load 100%')
            self.base.reading_lines_number = 1

            self.base.current_g_cod_pool = np.zeros((self.base.reading_lines_number, 7), float)
            self.base.current_g_cod_pool[:] = np.nan
            self.base.highlight.to_the_start()
            print('specially here count', self.base.highlight.count)
            self.setValue(0)

        elif self.base.reading_lines_number < self.base.highlight.count + self.base.highlight.standart_step:
                print('Делаем шаг поменьше: number_of_lines={}, self.base.highlight.count={}, self.base.highlight.standart_step={}'
                      .format(self.base.reading_lines_number, self.base.highlight.count, self.base.highlight.standart_step))
                self.base.highlight.standart_step = self.base.reading_lines_number - self.base.highlight.count# - 1?


    def inserting_in_main_g_cod(self):

        print('вставить {} перед строкой {}'.format(self.base.current_g_cod_pool, self.base.editor.min_line_np))
        self.base.main_g_cod_pool = np.insert(self.base.main_g_cod_pool, self.base.editor.min_line_np, self.base.current_g_cod_pool, axis=0)
        self.base.tab_.center_widget.left.left_tab.a.reset_np_array_in_left_field()


class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing):
        super().__init__()

        self.index_insert = 1
        self.tab_ = tab_

        grid = QGridLayout()
        self.setLayout(grid)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)

        self.progress_bar = Progress(self)

        self.reading_lines_number = self.editor.blockCount() or 1

        self.current_g_cod_pool = np.zeros((self.reading_lines_number, 7), float)
        self.current_g_cod_pool[:] = np.nan
        print('START: Создан массив размером ', self.current_g_cod_pool.shape)
        self.main_g_cod_pool = np.zeros((1, 7), float)
        self.main_g_cod_pool[:] = np.nan
        self.progress_bar.setMaximum(self.reading_lines_number)
        grid.addWidget(self.progress_bar, 1, 0)
        self.set_syntax()

    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

