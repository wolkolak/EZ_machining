from PyQt5.QtWidgets import QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QTextEdit, QWidget, QApplication, QFrame, QVBoxLayout, QBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QRect, QSize, QTimer, QThread, QThreadPool
from PyQt5.QtGui import QTextOption, QColor, QPainter, QClipboard, QTextCursor, QTextDocument, QTextCharFormat,\
    QTextFormat, QGuiApplication
from settings import *
from find_replace import finder
import HLSyntax.HL_Syntax
import flow
import runnable_flow
import numpy as np




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
        #self.textChanged.connect(self.changing)
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


        self.updateRequest.connect(self.updateLineNumberArea)




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

    def changing(self):
        self.changed = True


class Progress(QProgressBar):
    def __init__(self):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()

class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing):
        super().__init__()

        self.tab_ = tab_

        grid = QGridLayout()
        self.setLayout(grid)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)

        self.progress_bar = Progress()
        self.delta_number_of_lines = self.editor.blockCount()
        self.progress_bar.setMaximum(self.delta_number_of_lines)#//1000*1000
        grid.addWidget(self.progress_bar, 1, 0)
        self.set_syntax()


    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor.document(), base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

        #self.threadpool = QThreadPool()


        #self.oh_no()

    #def oh_no(self):#сейчас не используется
    #    worker = runnable_flow.Worker(self.set_syntax, None)
    #    self.threadpool.start(worker)





