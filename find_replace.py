from PyQt5.QtWidgets import  QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QApplication
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import Qt



class finder(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        self.setStyleSheet("background-color: {}".format('rgb(240,240,240)'))
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('Find')
        bf = QApplication.clipboard().text()
        if len(bf) > 400:
            bf = ''
        self.string_to_find = QPlainTextEdit(bf)
        self.string_to_find.setStyleSheet("background-color: {}".format('rgb(255,255,255)'))
        grid.addWidget(self.string_to_find, 0, 0, 1, 4)
        self.string_to_find.setMaximumHeight(40)
        self.find_next = QPushButton("NEXT")
        self.find_next.setMaximumSize(80, 40)
        grid.addWidget(self.find_next, 1, 0)
        self.find_next.clicked.connect(lambda: self.naiv_find(False))
        self.find_previous = QPushButton("PREV")
        self.find_previous.setMaximumSize(80, 40)
        grid.addWidget(self.find_previous, 1, 1)
        self.find_previous.clicked.connect(lambda: self.naiv_find(True))
        self.find_all = QPushButton("ALL")
        grid.addWidget(self.find_all, 2, 0)
        self.label_all = QLabel("")
        self.label_all.setStyleSheet("QLabel {"
                                 "border-style: solid;"
                                 "border-width: 1px;"
                                 "border-color: black; "
                                 "}")
        grid.addWidget(self.label_all, 2, 1)
        self.case_sense = QCheckBox("Case sensitive")

        self.case_sense.setMaximumSize(100, 40)
        grid.addWidget(self.case_sense, 1, 2)

        #print(self.papka.textCursor().selectedText())#.selectedText()
        print(self.parent.textCursor().StartOfBlock)


        print(self.parent.textCursor().selection().toPlainText())
        print(self.parent.textCursor().selectionStart())
        print(self.parent.textCursor().selectionEnd())

        self.setGeometry(800, 300, 600, 100)





    def all_mention(self):# todo не дпоисано. Позже
        pass

    def naiv_find(self, direction):
        """        line = 4
        block = self.papka.document().findBlockByLineNumber(line)
        blockPos = block.position()
        cursor = QTextCursor(self.papka.document())
        cursor.setPosition(blockPos)
        cursor.select(QTextCursor.LineUnderCursor)
        cursor.setCharFormat(self.papka.fmt)"""

        #self.setExtraSelections(self.papka.textCursor().selection().toPlainText())

        start_position = self.parent.textCursor()
        #end_position = self.papka.textCursor.anchor()
        #print('pos:', self.parent.textCursor().position())


        if self.parent.textCursor().selection().toPlainText().lower() != self.string_to_find.toPlainText().lower():
            if direction is True:
                start_position.setPosition(self.parent.textCursor().selectionEnd())
            else:
                start_position.setPosition(self.parent.textCursor().selectionStart())
            self.parent.setTextCursor(start_position)


        print(self.parent.textCursor().selectionStart(), self.parent.textCursor().selectionEnd())

        #start_position.movePosition(QTextCursor.Up,  2)#it is working

        print('start:', start_position)

        #extra = self.QPlainTextEdit.format.ExtraSelection()
        #self.papka.extra.setTextBackgroundColor(color3)
        all1 = [self.string_to_find.toPlainText()]
        if direction is True:
            all1.append(QTextDocument.FindBackward)
        if self.case_sense.checkState() is True:
            all1.append(QTextDocument.FindCaseSensitively)



        if self.parent.find(*all1):
            self.setWindowTitle('Find: "{}"'.format(self.string_to_find.toPlainText()))
            self.label_all.setText('"{}"'.format(self.string_to_find.toPlainText()))
        else:
            start_position.movePosition(QTextCursor.End if direction is True else QTextCursor.Start)
            self.parent.setTextCursor(start_position)
            if self.parent.find(*all1):
                self.setWindowTitle('Find: "{}"'.format(self.string_to_find.toPlainText()))
                self.label_all.setText('"{}"'.format(self.string_to_find.toPlainText()))
            else:
                self.setWindowTitle('Find: Found nothing')
                self.label_all.setText('Found nothing')

