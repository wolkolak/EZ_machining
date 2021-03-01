from PyQt5.QtWidgets import QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QTextEdit, QWidget, QApplication, QFrame, QVBoxLayout, QBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QRect, QSize, QTimer, QThread, QThreadPool, pyqtSlot, QEvent, Qt
from PyQt5.QtGui import QTextOption, QColor, QPainter, QClipboard, QTextCursor, QTextDocument, QTextCharFormat,\
    QTextFormat, QGuiApplication
from settings import *
from find_replace import finder
import HLSyntax.HL_Syntax
import flow
import runnable_flow
import numpy as np
import time



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

        self.g_cod_pool = np.array([[200, 0, 3, 0, 0, 0],
                                   [160, 0, -5, 0, 0, 0],
                                   [163, 0, 3, 0, 0, 0],
                                   [155, 0, -5, 0, 0, 0],
                                   [166, 0, 0, 0, 0, 0],
                                   [100, 0, 200, 0, 0, 0]],
                                   float)
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
        self.previousBlockCount = 1

        self.updateRequest.connect(self.updateLineNumberArea)
        print('self.blockCount() = ', self.blockCount())
        self.installEventFilter(self)
        self._document = self.document()

        self._document.contentsChange.connect(self.onChange)

    def onChange(self, position, charsRemoved, charsAdded):
        """
        Я думаю, нужно сначала удалить из numpy лишнее, потому указать место вставки. Логично? вроде - да
        А если в данный момент мы уже читаем некий участок?  Тогда этот новый участок будет вставлен не там, так?
        Значит, сначала красим текст, потом вставляем и удаляем единовременно. Где беда?
        Если добавлены изменения пока идёт покраска участка. Что делать?
        В очередь. И? Новый onchange должен запустить процессы после того как работа с прерыдущим участком будет закончена?

        Допустим, очередь в 3 возможных подсчёта. Пока


        """
        #time.sleep(5)
        firstBlock = self._document.findBlock(position).blockNumber()
        untilBlock = self._document.findBlock(position + charsAdded - charsRemoved).blockNumber()
        delta = untilBlock - firstBlock
        print('on change position = {}, charsRemoved = {}, charsAdded = {}'
              .format(position, charsRemoved, charsAdded))
        print('How mach lines? = {} - {}'.format(untilBlock + 1, firstBlock))

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


    #todo сделать set maximum +1 для не последней строки на конце вставки
    def insertFromMimeData(self, source):
        if source.hasText():
            self.base.delta_number_of_lines = source.text().count('\n') + 1
            print('paaaste: ', self.base.delta_number_of_lines)
            self.base.current_g_cod_pool = np.zeros((self.base.delta_number_of_lines, 7), float)
            self.base.progress_bar.setMaximum(self.base.delta_number_of_lines)

            #Запомни текущую строку
            self.base.index_insert = self.base.editor.textCursor().blockNumber()

            if self.base.delta_number_of_lines < self.base.highlight.const_step:
                self.base.highlight.standart_step = self.base.delta_number_of_lines
            else:
                self.base.highlight.standart_step = self.base.highlight.const_step
            QPlainTextEdit.insertFromMimeData(self, source)


        #self.base.current_g_cod_pool =

    def eventFilter(self, widget, event):

        if (event.type() == QEvent.KeyPress and widget is self):
            self.base.highlight.standart_step = 1
            #self.base.highlight.count = 0
            key = event.key()
            if key == Qt.Key_Backspace:
                print('Backspace')
            #else:
            #    if key == Qt.Key_Return:
            #        print('return')
            #    elif key == Qt.Key_Enter:
            #        print('enter')
            #    return True
            self.base.progress_bar.setMaximum(self.base.delta_number_of_lines)
            self.base.on_count_changed(0)

            QWidget.eventFilter(self, widget, event)
            if self._document.isModified():
                print('was modified')

                self._document.setModified(False)
        return QWidget.eventFilter(self, widget, event)


class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()
        self.base = base
        self.valueChanged.connect(self.finish_current_batch)


    def finish_current_batch(self, current_value):
        self.base.highlight.count_in_step = 0
        if current_value == self.maximum():
            self.inserting_in_main_g_cod(self.base.index_insert)
            print('Load 100%')
            print('LOAD inserting current pool:', self.base.current_g_cod_pool[0])
            self.base.delta_number_of_lines = 1
            self.base.current_g_cod_pool = np.zeros((self.base.delta_number_of_lines, 7), float)
            self.base.highlight.to_the_start()
            print('specially here count', self.base.highlight.count)
            self.setValue(0)



        elif self.base.delta_number_of_lines < self.base.highlight.count + self.base.highlight.standart_step:
                print('Делаем шаг поменьше: self.base.delta_number_of_lines={}, self.base.highlight.count={}, self.base.highlight.standart_step={}'
                      .format(self.base.delta_number_of_lines, self.base.highlight.count, self.base.highlight.standart_step))
                self.base.highlight.standart_step = self.base.delta_number_of_lines - self.base.highlight.count# - 1?
        print('progressbar finish current batch Hcount ', self.base.highlight.count)


    def inserting_in_main_g_cod(self, index_start=0, lines_to_delete=1):
        #добавить self.base.main_g_cod_pool в
        #print('index = ', index_start)
        self.base.main_g_cod_pool = np.insert(self.base.main_g_cod_pool, 0, self.base.current_g_cod_pool, axis=0)

        self.base.tab_.center_widget.left.left_tab.a.reset_np_array_in_left_field()
        print('inserting current pool:', self.base.current_g_cod_pool[0])
        print('inserting to main pool:', self.base.main_g_cod_pool )
        #print('let s see = ', self.base.tab_.center_widget.left.left_tab.a)

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

        self.delta_number_of_lines = self.editor.blockCount() or 1
        #self.delta_number_of_lines = 1
        self.current_g_cod_pool = np.zeros((self.delta_number_of_lines, 7), float)#.fill(np.nan)
        print('START: Создан массив размером ', self.current_g_cod_pool.shape)
        self.main_g_cod_pool = np.zeros((0, 7), float)
        self.progress_bar.setMaximum(self.delta_number_of_lines)
        grid.addWidget(self.progress_bar, 1, 0)
        self.set_syntax()



    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

        #self.threadpool = QThreadPool()


        #self.oh_no()

    #def oh_no(self):#сейчас не используется
    #    worker = runnable_flow.Worker(self.set_syntax, None)
    #    self.threadpool.start(worker)





