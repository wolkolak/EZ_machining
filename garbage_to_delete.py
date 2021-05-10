import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QTextOption, QTextDocumentFragment, QTextCursor
from PyQt5.QtCore import QEvent, Qt

class Form(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.nameEdit = MyLine(self)

        undoAction = self.nameEdit.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QKeySequence.Undo)
        redoAction = self.nameEdit.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QKeySequence.Redo)

        undoButton = QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QToolButton()
        redoButton.setDefaultAction(redoAction)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Name"), self.nameEdit)
        #formLayout.addRow(self.tr("&Address"), addressEdit)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(undoButton)
        buttonLayout.addWidget(redoButton)

        layout = QHBoxLayout(self)
        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)
        self.setWindowTitle(self.tr("Undo Example"))



class MyLine(QPlainTextEdit):

    def __init__(self, papa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ xyzcba"""

        self.papa = papa
        self._document = self.document()
        self.installEventFilter(self)
        self.undoStack = MyStack(self)
        self.setWordWrapMode(QTextOption.NoWrap)



    def eventFilter(self, widget, event):
        # должен ссылаться на универсальную замену текста
        # print('event.type() = ', event.type())

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
                    #self.my_undo()
                if event.key() == (Qt.Key_Control and Qt.Key_Y):
                    print('вернуть')
                if event.key() == (Qt.Key_Control and Qt.Key_X):
                    print('Вырез')
                    self.undoStack.edit_type = 'Cut'# ['Cut']
                    #QPlainTextEdit.cut(self)
                    self.undoStack.last_edited = ''
                    self.undoStack.storeFieldText()
                if event.key() == (Qt.Key_Control and Qt.Key_V):
                    print('Вставка')
                    self.undoStack.edit_type = 'Insert'
                    insert_txt = QApplication.clipboard().text()
                    if insert_txt is not '':
                        self.undoStack.last_edited = insert_txt
                        self.undoStack.storeFieldText()
            else:
                #txt = event.text()
                if event.text():
                    if key == Qt.Key_Backspace:
                        self.undoStack.edit_type = 'Backspace'
                    elif key == Qt.Key_Delete:
                        self.undoStack.edit_type = 'Delete'
                    else:
                        if Qt.Key_0 <= key <= Qt.Key_9:
                            self.undoStack.edit_type = 'digital'
                        elif Qt.Key_A <= key <= Qt.Key_Z:
                            self.undoStack.edit_type = 'symbol'
                        elif key == Qt.Key_Space:
                            self.undoStack.merging_world()
                            self.undoStack.edit_type = 'space'
                        elif key == Qt.Key_Return or Qt.Key_Enter:
                            self.undoStack.merging_world()
                            self.undoStack.edit_type = 'enter'
                        elif key == Qt.Key_Dead_Belowdot or Qt.Key_Comma:
                            self.undoStack.edit_type = 'comma'
                        else:
                            self.undoStack.edit_type = 'another'
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
        #self.merge_n = 1
        #self.edit_type = 'symbol'

    def storeFieldText(self):
        if self.last_edited == False:
            return
        command = StoreCommand(self)
        self.last_edited = False
        self.push(command)
        print('command.field = ', command.text)

    def merging_world(self):
        if self.edit_type == 'space' and self.index() > 0:
            print('merge')
            g = self.command(self.index()).MYmergeWith(self.command(self.index() - 1), 1, 0)
            print('g = ', g)



class StoreCommand(QUndoCommand):

    def __init__(self, stack):
        QUndoCommand.__init__(self)
        self.stack = stack
        # Record the field that has changed.
        self.field = self.stack.edit
        self.store_cursor = self.field.textCursor()
        self.text_inserted = self.stack.last_edited
        self.text = self.stack.edit_type
        self.id = 1


        if self.text == 'Backspace':
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
            #self.text_inserted = ''
            self.give_position()
            self.pos3 = self.pos1
        if self.text == 'Insert':
            self.give_position()
            self.pos3 = self.pos1 + len(self.text_inserted)
        else:#остальные символы
            self.give_position()
            self.pos3 = self.pos1 + 1
        self.command_created_only = True

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



    def undo(self):
        print('undo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        self.store_cursor.setPosition(self.pos3, 0)#
        self.store_cursor.setPosition(self.pos1, 1)
        self.store_cursor.insertText(self.text_deleted)
        self.command_created_only = False

    def redo(self):
        print('redo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        if self.command_created_only is False:
            self.store_cursor.setPosition(self.pos1, 0)
            self.store_cursor.setPosition(self.pos2, 1)
            self.store_cursor.insertText(self.text_inserted)

    def MYmergeWith(self, previous_command, merge_n, obsolete):

        print('my mergeeeee: {} and {}'.format(self.text, previous_command.text))
        if previous_command.text != 'enter' and previous_command.pos1 == self.pos1 - 1:
            if previous_command.text == self.text:
                #сложить

                obsolete???!!!
                if self.stack.index() > 0:
                    self.mergeWith(self.stack.command(self.index() - 1), merge_n)
            else:
                if not self.text != 'space' and self.stack.index() - self.stack.merge_n > 0:
                    self.stack.command(self.index() - merge_n).mergeWith(self.stack.command(self.index()
                    - merge_n - 1), merge_n+1, 0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
