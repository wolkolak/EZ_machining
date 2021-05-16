import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QTextOption, QColor, QTextCharFormat, QSyntaxHighlighter, QFont
from PyQt5.QtCore import QEvent, Qt, QRegularExpression


class Form(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.nameEdit = MyLine(self)

        undoAction = self.nameEdit.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QKeySequence.Undo)
        undoAction.setShortcuts(QKeySequence.Undo)
        redoAction = self.nameEdit.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QKeySequence.Redo)

        undoButton = QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QToolButton()
        redoButton.setDefaultAction(redoAction)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Name"), self.nameEdit)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(undoButton)
        buttonLayout.addWidget(redoButton)

        layout = QHBoxLayout(self)
        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)
        self.setWindowTitle(self.tr("Undo Example"))
        self.highlight = GMHighlighter(self.nameEdit._document, base=self)


class MyLine(QPlainTextEdit):

    def __init__(self, papa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ xyzcba"""

        self.papa = papa
        self._document = self.document()
        self.installEventFilter(self)
        self.undoStack = MyStack(self)
        self.setWordWrapMode(QTextOption.NoWrap)
        self._document.contentsChange.connect(self.onChange)
        self.corrected_qt_number_of_lines = 0
        self.adding_lines = 0

    def onChange(self, position, charsRemoved, charsAdded):
        """
        Тут необходимо добавить n_deleted_lines, n_highlighted_lines
        и pos1_del pos1_insert
         в self.undoStack.command(self.undoStack.index()-1)
        """
        print('onchange start')
        print('self.undoStack.index()=', self.undoStack.index())
        z = self.undoStack.command_onChange_for

        print('z.command_created_only = ', z.command_created_only)
        if z.command_created_only is False:
            print('gggg')
            if self.undoStack.undo_direction == 0:#undo
                self.undoStack.line_max_np_insert = self._document.findBlock(z.pos3).blockNumber() + 1
                #print('undo self.undoStack.line_max_np_insert = ', self.undoStack.line_max_np_insert)
                print('удалим с {} по {}, вставим с {} по {}'.format(self._document.findBlock(z.pos1).blockNumber(),
                                                                     self._document.findBlock(z.pos2).blockNumber(),
                                                                     self._document.findBlock(z.pos1).blockNumber(),
                                                                     self.undoStack.line_max_np_insert))
            else:
                self.undoStack.line_max_np_insert = self._document.findBlock(z.pos2).blockNumber() + 1 + z.corrected_qt_number_of_lines
                #print('redo self.undoStack.line_max_np_insert = ', self.undoStack.line_max_np_insert)
                print('удалим с {} по {}, вставим с {} по {}'.format(self._document.findBlock(z.pos1).blockNumber(),
                                                                     self._document.findBlock(z.pos3).blockNumber(),
                                                                     self._document.findBlock(z.pos1).blockNumber(),
                                                                     self.undoStack.line_max_np_insert))
            return



    def eventFilter(self, widget, event):
        if (event.type() == QEvent.KeyPress and widget is self):
            key = event.key()
            self.blocks_before = self._document.blockCount()
            if Qt.KeypadModifier:
                print('KeypadModifie', int(event.modifiers()))
            mod_sum = int(event.modifiers())
            if mod_sum > 0 and mod_sum != Qt.ShiftModifier and mod_sum != Qt.KeypadModifier \
                    and mod_sum != Qt.ShiftModifier + Qt.KeypadModifier:
                print('модификаторы кроме шифта')
                if event.key() == (Qt.Key_Control and Qt.Key_Z):
                    print('отменить')
                    self.undoStack.undo_direction = 0
                    self.undoStack.undo()
                    return True
                if event.key() == (Qt.Key_Control and Qt.Key_Y):
                    print('вернуть')
                    self.undoStack.undo_direction = 1
                    self.undoStack.redo()
                    return True
                if event.key() == (Qt.Key_Control and Qt.Key_X):
                    print('Вырез')
                    self.undoStack.edit_type = 'Cut'
                    self.undoStack.last_edited = ''
                    self.undoStack.storeFieldText()
                if event.key() == (Qt.Key_Control and Qt.Key_V):
                    print('Вставка')
                    self.undoStack.edit_type = 'Insert'
                    insert_txt = QApplication.clipboard().text()
                    if insert_txt != '':
                        self.undoStack.last_edited = insert_txt
                        self.undoStack.storeFieldText()
            else:
                if event.text():
                    if key == Qt.Key_Backspace:
                        self.undoStack.edit_type = 'Backspace'
                    elif key == Qt.Key_Delete:
                        self.undoStack.edit_type = 'Delete'
                    else:
                        if key == Qt.Key_Space:
                            self.undoStack.merging_world()
                            self.undoStack.edit_type = 'space'
                        elif key == Qt.Key_Return or key == Qt.Key_Enter:
                            self.undoStack.merging_world()
                            self.undoStack.edit_type = 'enter'
                        else:
                            self.undoStack.edit_type = 'symbol'
                        self.undoStack.last_edited = event.text()
                    self.undoStack.storeFieldText()
            if self._document.isModified():
                print('was modified')
                self._document.setModified(False)
        return QWidget.eventFilter(self, widget, event)


class MyStack(QUndoStack):
    def __init__(self, edit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit = edit
        self.last_edited = ''
        self.sutulaya_sobaka = False
        self.line_max_np_del = 0
        self.line_max_np_insert = 0
        self.undo_direction = 1
        self.command_onChange_for = self.command(self.index()-1)
        # self.edit_type = something

    def storeFieldText(self):
        if self.edit_type == False:
            return
        command = StoreCommand(self)
        self.edit_type = False
        self.push(command)
        print('command.field = ', command.text)

    def merging_world(self):

        print('merge')
        while self.index() > 1 and (self.command(self.index() - 2).id != -1):
            print('self.index() ==== ', self.index())
            g = self.command(self.index() - 2).mergeWith(self.command(self.index() - 1))
            self.sutulaya_sobaka = True
            self.undo()  # silent undo
            self.sutulaya_sobaka = False
            # print('g = ', g)
            # print('self.index() zzzz = ', self.index())


class StoreCommand(QUndoCommand):

    def __init__(self, stack):
        QUndoCommand.__init__(self)
        self.stack = stack
        # Record the field that has changed.
        self.field = self.stack.edit
        self.store_cursor = self.field.textCursor()
        self.text_inserted = self.stack.last_edited
        self.text = self.stack.edit_type
        self.id = -1
        self.corrected_qt_number_of_lines = 1
        # todo self.text перевести на self.id

        self.command_created_only = True

        if self.text == 'symbol' or self.text == 'enter' or self.text == 'space':  # остальные символы
            if self.text == 'symbol':
                self.id = 1
            self.give_position()
            self.pos3 = self.pos1 + 1
        elif self.text == 'Backspace':
            self.text_inserted = ''
            if not self.store_cursor.hasSelection():
                self.store_cursor.setPosition(self.store_cursor.position() - 1, 1)
            self.give_position()
            self.pos3 = self.pos1
        elif self.text == 'Delete':
            self.text_inserted = ''
            if not self.store_cursor.hasSelection():
                self.store_cursor.setPosition(self.store_cursor.position() + 1, 1)
            self.give_position()
            self.pos3 = self.pos1
        elif self.text == 'Cut':
            # self.text_inserted = ''
            self.give_position()
            self.pos3 = self.pos1
        elif self.text == 'Insert':
            self.give_position()
            self.pos3 = self.pos1 + len(self.text_inserted)

        print('self.command_created_only = True')

        print('text = ', self.field.toPlainText())
        print('                    self.pos1 = {}, self.pos2 = {}'.format(self.pos1, self.pos2))
        self.text_deleted = self.store_cursor.selectedText()
        print('                    selectedText', self.text_deleted)

        print('                    last_edited', self.text_inserted)

    def give_position(self):
        pos1 = self.store_cursor.position()
        pos2 = self.store_cursor.anchor()
        self.pos1 = min(pos1, pos2)
        self.pos2 = max(pos1, pos2)

    def mergeWith(self, other: 'QUndoCommand') -> bool:
        print('{} mergeWith {}'.format(self.text_inserted, other.text_inserted))
        self.text_inserted = self.text_inserted + other.text_inserted
        self.pos3 = other.pos3
        print('self.pos3 = ', self.pos3)
        # other.setObsolete(True)
        return True

    def undo(self):
        self.command_created_only = False
        if self.stack.sutulaya_sobaka is True:
            print('pseudo undo')
        else:
            print(
                'undo text_inserted: {}, готов записать в команду № {}'.format(self.text_inserted, self.stack.index()))
            self.store_cursor.setPosition(self.pos3, 0)  #
            self.store_cursor.setPosition(self.pos1, 1)
            self.store_cursor.insertText(self.text_deleted)
            self.stack.line_max_np_del = self.field._document.findBlock(self.pos2).blockNumber()
            print('UNDO self.stack.line_max_np_del = ', self.stack.line_max_np_del)
            self.stack.command_onChange_for = self

    def redo(self):
        print('redo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        if self.command_created_only is False:
            self.store_cursor.setPosition(self.pos1, 0)
            self.store_cursor.setPosition(self.pos2, 1)
            self.store_cursor.insertText(self.text_inserted)
            self.stack.line_max_np_del = self.field._document.findBlock(self.pos3).blockNumber() + self.corrected_qt_number_of_lines
            print('REDO self.stack.line_max_np_del = ', self.stack.line_max_np_del)
            self.stack.command_onChange_for = self


def format(color, style=''):
    """ Верните QTextCharFormat с указанными атрибутами. """
    _color = QColor()
    _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Синтаксические стили, которые могут использоваться
STYLES = {
    'axis': format('blue'),
    'g_cod': format('red'),
    'comment_brace': format('darkGray'),
    'defclass': format('black', 'bold'),
    'string': format('magenta'),
    'string2': format('darkMagenta'),
    'comment': format('darkGreen', 'italic'),
    'self': format('black', 'italic'),
    'numbers': format('brown'),
}


class GMHighlighter(QSyntaxHighlighter):
    """Синтаксические маркеры для языка. """
    # G-func
    g_cod = ['G0', 'G1', 'G2', 'G3']
    # axises
    axises = ['X', 'Y', 'Z', 'C', 'B', 'A', 'R']
    # most strings look like 'main_rule'

    sorted_axis_rule = ''
    for letter in axises:
        sorted_axis_rule += r'((?:{})(-?\d+\.\d*)\s*)?'.format(letter)
        # sorted_axis_rule += r'(([{}]\s*)(-)?(\d+.\d*)\s*)?'.format(letter)
    sorted_axis_rule = '^' + '(?:G\d+)?\s*' + sorted_axis_rule + '$'
    # print('nabor XYZ:', sorted_axis_rule)

    main_rule = sorted_axis_rule

    axises_str = ''.join(axises)
    axises_coord = r'([{}]\s*(-)?(\d+\.\d*)\s*)'.format(axises_str)
    second_rule = r'^(G0?\d)?\s*{}+(F\d(\.)?)?(?:;)?$'.format(axises_coord)
    # condition operators
    condition_operators = ['WHILE', 'IF']

    # comment braces
    comment_braces = ['\([\w.]*\)']

    # condition braces
    logic_op = ['EQ', 'NE', 'GT', 'LT', 'GE', 'LE']

    def __init__(self, document, base):
        QSyntaxHighlighter.__init__(self, document)
        self.max_number_ax = [i * 2 for i in range(1, 8)]
        self.base = base
        self.count = 0
        self.count_in_step = 0
        self.const_step = 1000
        self.standart_step = self.const_step
        rules = []

        rules += [(r'{}'.format(GMHighlighter.second_rule), 0, STYLES['axis'])]

        # comment rules
        rules += [(r'{}'.format(GMHighlighter.comment_braces[0]), 2,
                   STYLES['comment_brace'])]  # rules += [(r'\([\w.]*\)', 0, STYLES['string'])]

        # Создайте QRegExp для каждого шаблона
        self.first_rule = [QRegularExpression(self.main_rule), 0, STYLES['axis']]
        self.rules = [(QRegularExpression(pat), index, fmt) for (pat, index, fmt) in rules]
        self.main_rule_regular_expression = self.first_rule[0]
        self.main_format = self.first_rule[2]
        self.second_rule_regular_expression = self.rules[0][0]
        self.second_format = self.rules[0][2]

    def highlightBlock(self, text):
        """Применить выделение синтаксиса к данному блоку текста. """

        # if self.base.editor._document.isModified():
        # print('waiting')
        # print('reading_lines_number', self.base.reading_lines_number)
        # time.sleep(5)

        common_length = 0

        nya = self.main_rule_regular_expression.match(text, 0)
        # print('nya0 = ', nya.captured(0))
        index = nya.capturedStart()
        len_match = nya.capturedLength()
        if len_match != 0:
            self.setFormat(index, len_match, self.main_format)
            # print('self.base.current_g_cod_pool[0]  = ', self.base.current_g_cod_pool[0])
            print('nya = ', nya.captured())
        else:
            print('nya = pusto')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
