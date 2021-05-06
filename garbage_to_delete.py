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
                    self.my_undo()
                if event.key() == (Qt.Key_Control and Qt.Key_X):
                    print('Вырез')
                    self.undoStack.edit_type = 'Cut'# ['Cut']
                    self.my_cut()
                if event.key() == (Qt.Key_Control and Qt.Key_V):
                    print('Вставка')
                    self.undoStack.edit_type = 'Insert'
            else:
                #txt = event.text()
                if event.text():
                    if key == Qt.Key_Backspace:
                        self.undoStack.edit_type = 'Backspace'
                    elif key == Qt.Key_Delete:
                        self.undoStack.edit_type = 'Delete'
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
        #self.edit_type = 'symbol'

    def storeFieldText(self):
        if self.last_edited == False:
            return
        command = StoreCommand(self)
        self.last_edited = False
        self.push(command)
        print('command.field = ', command.text)


class StoreCommand(QUndoCommand):

    def __init__(self, stack):
        QUndoCommand.__init__(self)
        self.stack = stack
        # Record the field that has changed.
        self.field = self.stack.edit
        self.store_cursor = self.field.textCursor()
        self.text_inserted = self.stack.last_edited
        self.text = self.stack.edit_type

        if not self.store_cursor.hasSelection():
            print('not selection')
            if self.text == 'Backspace':
                self.text_inserted = ''
                # self.store_cursor.movePosition(19, 1)
                self.store_cursor.setPosition(self.store_cursor.position() - 1, 1)
                # pos2 = pos1
                # self.pos1 = self.pos1 - 1
            elif self.text == 'Delete':
                self.text_inserted = ''
                # self.pos1 = self.pos1 + 1

        pos1 = self.store_cursor.position()
        pos2 = self.store_cursor.anchor()
        self.pos1 = min(pos1, pos2)
        self.pos2 = max(pos1, pos2)
        #print('self.store_cursor.hasSelection = ', self.store_cursor.hasSelection)
        #if self.store_cursor.hasSelection():
        #    self.pos3 = self.pos1
        #else:
        #    self.pos3 = self.pos1 + 1


        #todo self.store_cursor.selectedText() и pos2 = pos1
        print('text = ', self.field.toPlainText())


        print('                    self.pos1 = {}, self.pos2 = {}'.format(self.pos1, self.pos2))
        self.text_deleted = self.store_cursor.selectedText() #QTextDocumentFragment.fromPlainText('')  insertFragment
        print('                    selectedText', self.text_deleted)


        self.command_created_only = True

        print('                    last_edited', self.text_inserted)
        # Record the text at the time the command was created.



    def undo(self):
        print('undo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        self.store_cursor.setPosition(self.pos1+1, 0)#
        self.store_cursor.setPosition(self.pos1, 1)
        self.store_cursor.insertText(self.text_deleted)
        self.command_created_only = False

    def redo(self):
        print('redo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        if self.command_created_only is False:
            self.store_cursor.setPosition(self.pos1, 0)
            self.store_cursor.setPosition(self.pos2, 1)
            self.store_cursor.insertText(self.text_inserted)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
