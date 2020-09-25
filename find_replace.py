from PyQt5.QtWidgets import  QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QApplication
from PyQt5.QtGui import QTextCursor, QTextDocument




class finder(QDialog):
    def __init__(self, papka, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papka = papka
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('Find')
        bf = QApplication.clipboard().text()
        if len(bf) > 400:
            bf = ''
        self.string_to_find = QPlainTextEdit(bf)

        grid.addWidget(self.string_to_find, 0, 0, 1, 4)
        self.string_to_find.setMaximumHeight(40)
        self.find_next = QPushButton("NEXT")
        self.find_next.setMaximumSize(80, 40)
        grid.addWidget(self.find_next, 1, 0)
        self.find_next.clicked.connect(lambda: self.naiv_find(None))
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
        print(self.papka.textCursor().StartOfBlock)


        print(self.papka.textCursor().selection().toPlainText())
        print(self.papka.textCursor().selectionStart())
        print(self.papka.textCursor().selectionEnd())
        self.setGeometry(800, 300, 600, 100)





    def all_mention(self):#todo
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

        start_position = self.papka.textCursor()
        #end_position = self.papka.textCursor.anchor()
        print('pos:', self.papka.textCursor().position())

        if self.papka.textCursor().selection().toPlainText() != self.string_to_find.toPlainText():
            """            pos1 = self.papka.textCursor().position()
            pos2 = self.papka.textCursor().anchor()
            if pos1 > pos2:
                print('курсор ниже')
                #pos1, pos2 = pos2, pos1"""
            start_position.setPosition(self.papka.textCursor().selectionStart())

            print(self.papka.textCursor().selectionStart(), self.papka.textCursor().selectionEnd())

            #start_position.movePosition(QTextCursor.Up,  2)#it is working
            self.papka.setTextCursor(start_position)
            print('start:', start_position)

        #extra = self.QPlainTextEdit.format.ExtraSelection()
        #self.papka.extra.setTextBackgroundColor(color3)
        all1 = [self.string_to_find.toPlainText()]
        if direction:
            all1.append(QTextDocument.FindBackward)
        if self.case_sense.checkState():
            all1.append(QTextDocument.FindCaseSensitively)



        if self.papka.find(*all1):#todo не дпоисано. Позже
            self.setWindowTitle('Find: "{}"'.format(self.string_to_find.toPlainText()))
            self.label_all.setText('"{}"'.format(self.string_to_find.toPlainText()))
        else:
            start_position.movePosition(QTextCursor.End if direction else QTextCursor.Start)
            self.papka.setTextCursor(start_position)
            if self.papka.find(*all1):
                self.setWindowTitle('Find: "{}"'.format(self.string_to_find.toPlainText()))
                self.label_all.setText('"{}"'.format(self.string_to_find.toPlainText()))
            else:
                self.setWindowTitle('Find: Found nothing')
                self.label_all.setText('Found nothing')