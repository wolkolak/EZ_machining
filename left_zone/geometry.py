import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QKeySequence

class Form(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)

        self.undoStack = QUndoStack()

        undoAction = self.undoStack.createUndoAction(self, self.tr("&Undo"))
        undoAction.setShortcuts(QKeySequence.Undo)
        redoAction = self.undoStack.createRedoAction(self, self.tr("&Redo"))
        redoAction.setShortcuts(QKeySequence.Redo)

        nameEdit = QPlainTextEdit()
        nameEdit.document = nameEdit.document()
        #addressEdit = QLineEdit()

        undoButton = QToolButton()
        undoButton.setDefaultAction(undoAction)
        redoButton = QToolButton()
        redoButton.setDefaultAction(redoAction)

        nameEdit.document.contentsChange.connect(self.obertka_storeFieldText)# <- СМОТРЕТЬ СЮДА
        #nameEdit.editingFinished.connect(self.storeFieldText)
        #addressEdit.editingFinished.connect(self.storeFieldText)

        formLayout = QFormLayout()
        formLayout.addRow(self.tr("&Name"), nameEdit)
        #formLayout.addRow(self.tr("&Address"), addressEdit)

        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(undoButton)
        buttonLayout.addWidget(redoButton)

        layout = QHBoxLayout(self)
        layout.addLayout(formLayout)
        layout.addLayout(buttonLayout)

        self.setWindowTitle(self.tr("Undo Example"))
        self.ind = 0

    def obertka_storeFieldText(self):
        if self.ind == 0:
            self.storeFieldText()


    def storeFieldText(self):
        self.ind = 1
        command = StoreCommand(self.sender())
        self.undoStack.push(command)
        self.ind = 0



class StoreCommand(QUndoCommand):

    def __init__(self, field):

        QUndoCommand.__init__(self)

        # Record the field that has changed.
        self.field = field
        print('type field = ', type(self.field))
        print('self.field.text()', self.field.toPlainText())

        # Record the text at the time the command was created.
        self.text = field.toPlainText()

    def undo(self):
        print('undo start')
        # Remove the text from the file and set it in the field.
        # ...
        self.field.setPlainText(self.text)
        print('undo end')

    def redo(self):
        print('redo start')
        # Store the text in the file and set it in the field.
        # ...
        self.field.setPlainText(self.text)
        print('redo end')


if __name__ == "__main__":

    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

    