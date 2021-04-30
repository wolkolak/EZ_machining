import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence, QTextOption
from PyQt5.QtCore import QEvent, Qt



class MyLine(QPlainTextEdit):

    def __init__(self, papa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        """ xyzcba"""

        self.papa = papa
        self._document = self.document()
        #self.installEventFilter(self)


class Form(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.undoStack = MyStack()

        undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QKeySequence.Undo)
        redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QKeySequence.Redo)

        self.nameEdit = MyLine(self)
        self.nameEdit.setWordWrapMode(QTextOption.NoWrap)
        #addressEdit = QLineEdit()

        undoButton = QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QToolButton()
        redoButton.setDefaultAction(redoAction)

        #self.nameEdit.editingFinished.connect(self.storeFieldText)
        self.nameEdit._document.contentsChange.connect(self.storeFieldText)
        #addressEdit.editingFinished.connect(self.storeFieldText)

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

        #self.nameEdit.st_direction = 'r'

    def storeFieldText(self):
        #print(('why are u working?'))
        print('text now', self.nameEdit.toPlainText())
        print('self.undoStack.count() = {}, self.undoStack.index() = {}'.format(self.undoStack.count(), self.undoStack.index()))
        if self.undoStack.count() >= self.undoStack.index():
            return
        if self.undoStack.st_direction1 == 'l':
            return
        if self.undoStack.set_no_set is True:
            self.undoStack.set_no_set = False
            return
        self.undoStack.set_no_set = True
        command = StoreCommand(self.nameEdit, self.undoStack)

        self.undoStack.push(command)

        #self.undoStack.set_no_set = True
        #print('members: ', dir(self.nameEdit))
        print('command.field = ', command.text)
        #self.nameEdit.setText('aaaaaaaaaaaaa')
        #print('command.field = ', command.text)



class StoreCommand(QUndoCommand):

    def __init__(self, field, stack):
        QUndoCommand.__init__(self)
        self.stack = stack
        # Record the field that has changed.
        self.field = field

        # Record the text at the time the command was created.
        self.text = field.toPlainText()


    def undo(self):
        # Remove the text from the file and set it in the field.
        # ...
        print('undo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))

        self.field.setPlainText(self.text)
        self.stack.st_direction = 'l'

            #self.stack.command(self.stack.index()-2).undo()

    def redo(self):
        # Store the text in the file and set it in the field.
        # ...
        print('redo: {}, готов записать в команду № {}'.format(self.text, self.stack.index()))
        self.field.setPlainText(self.text)
        self.stack.st_direction = 'r'

class MyStack(QUndoStack):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.st_direction = 'r'
        self.st_direction1 = 'r'
        self.set_no_set = False
        self.indexChanged.connect(self.stack_corr)

    def stack_corr(self):
        if self.st_direction != self.st_direction1:
            self.st_direction1 = self.st_direction
            if self.st_direction1 == 'r':
                self.redo()
            else:
                self.undo()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())