from PyQt5.QtWidgets import  QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog,\
    QCheckBox, QApplication, QTabWidget, QWidget
from PyQt5.QtGui import QTextCursor, QTextDocument
from PyQt5.QtCore import Qt

class Page1(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
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
        #self.find_next.setMaximumSize(80, 40)
        self.find_next.setFixedSize(80, 25)
        grid.addWidget(self.find_next, 1, 0)
        self.find_next.clicked.connect(lambda: self.naiv_find(False))
        self.find_previous = QPushButton("PREV")
        self.find_previous.setMaximumSize(80, 40)
        grid.addWidget(self.find_previous, 1, 1)
        self.find_previous.clicked.connect(lambda: self.naiv_find(True))
        self.find_all = QPushButton("COUNT")
        self.find_all.clicked.connect(self.all_mention)
        self.label_all = QLabel("")
        self.label_all.setStyleSheet("QLabel {"
                                     "border-style: solid;"
                                     "border-width: 1px;"
                                     "border-color: black; "
                                     "}")

        self.case_sense = QCheckBox("Case sensitive")

        self.case_sense.setMaximumSize(100, 40)
        grid.addWidget(self.case_sense, 1, 2)
        grid.addWidget(self.find_all, 2, 0)
        grid.addWidget(self.label_all, 2, 1)


    def all_mention(self):
        i = 0
        start_position = self.parent.textCursor()
        pos = start_position.position()
        start_position.setPosition(0)
        self.parent.setTextCursor(start_position)
        while self.parent.find(self.string_to_find.toPlainText()):
            i = i + 1
        self.label_all.setText(str(i))
        start_position.setPosition(pos)
        self.parent.setTextCursor(start_position)


    def naiv_find(self, direction):
        start_position = self.parent.textCursor()

        if self.parent.textCursor().selection().toPlainText().lower() != self.string_to_find.toPlainText().lower():
            if direction is True:
                start_position.setPosition(self.parent.textCursor().selectionEnd())
            else:
                start_position.setPosition(self.parent.textCursor().selectionStart())
            self.parent.setTextCursor(start_position)


        print(self.parent.textCursor().selectionStart(), self.parent.textCursor().selectionEnd())

        print('start:', start_position)
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


class Page2(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
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

        self.string_new = QPlainTextEdit(bf)
        self.string_new.setStyleSheet("background-color: {}".format('rgb(255,255,255)'))
        grid.addWidget(self.string_new, 1, 0, 1, 4)
        self.string_new.setMaximumHeight(40)

        self.find_next = QPushButton("REPLACE AFTER")
        self.find_next.setMaximumSize(100, 40)
        grid.addWidget(self.find_next, 2, 0)
        self.find_next.clicked.connect(lambda: self.naiv_find(False))
        self.find_previous = QPushButton("REPLACE PREV")
        self.find_previous.setMaximumSize(100, 40)
        grid.addWidget(self.find_previous, 2, 1)
        self.find_previous.clicked.connect(lambda: self.naiv_find(True))
        self.find_all = QPushButton("REPLACE ALL")
        self.find_all.clicked.connect(self.all_mention)
        grid.addWidget(self.find_all, 3, 0)
        self.label_all = QLabel("")
        self.label_all.setStyleSheet("QLabel {"
                                     "border-style: solid;"
                                     "border-width: 1px;"
                                     "border-color: black; "
                                     "}")
        grid.addWidget(self.label_all, 3, 1)
        self.case_sense = QCheckBox("Case sensitive")

        self.case_sense.setMaximumSize(100, 40)
        grid.addWidget(self.case_sense, 2, 2)




    def all_mention(self):
        i = 0
        start_position = self.parent.textCursor()
        pos = start_position.position()
        start_position.setPosition(0)
        self.parent.setTextCursor(start_position)
        self.parent.undoStack.edit_type = 'glue'
        self.parent.undoStack.beginMacro('glue')
        while self.parent.find(self.string_to_find.toPlainText()):
            i = i + 1
            self.replace()
            print('self.childCount()', self.parent.undoStack.command(self.parent.undoStack.index()).childCount())

        self.parent.undoStack.endMacro()

        self.label_all.setText(str(i))
        start_position.setPosition(pos)
        self.parent.setTextCursor(start_position)

    def naiv_find(self, direction):

        #self.setExtraSelections(self.papka.textCursor().selection().toPlainText())

        start_position = self.parent.textCursor()

        if self.parent.textCursor().selection().toPlainText().lower() != self.string_to_find.toPlainText().lower():
            if direction is True:
                start_position.setPosition(self.parent.textCursor().selectionEnd())
            else:
                start_position.setPosition(self.parent.textCursor().selectionStart())

            self.parent.setTextCursor(start_position)
            print('start_position ', start_position)

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
            self.label_all.setText('"{}"'.format(self.string_new.toPlainText()))
            #замена здесь
            self.replace()

        else:
            start_position.movePosition(QTextCursor.End if direction is True else QTextCursor.Start)
            self.parent.setTextCursor(start_position)

            if self.parent.find(*all1):
                self.setWindowTitle('Find: "{}"'.format(self.string_to_find.toPlainText()))
                self.label_all.setText('"{}"'.format(self.string_to_find.toPlainText()))
                # замена здесь
                self.replace()

            else:
                self.setWindowTitle('Find: Found nothing')
                self.label_all.setText('Found nothing')

    def replace(self):
        insert = self.string_new.toPlainText()
        print('insert replace = ', insert)
        self.parent.undoStack.edit_type = 'replace'
        replace_to_nothing = False if len(self.string_new.toPlainText()) > 0 else True
        print('len(self.string_new.toPlainText()) = {}, replace_to_nothing = {}'.format(len(self.string_new.toPlainText()), replace_to_nothing))
        self.parent.event_data_acquiring(self.parent.undoStack.edit_type, replace_to_nothing)
        self.parent.undoStack.last_edited = insert

        self.parent.undoStack.storeFieldText()

        self.parent.textCursor().insertText(insert)


class finder(QDialog):
    def __init__(self, parent, i=0):
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        self.i = i
        grid = QGridLayout()
        self.setLayout(grid)
        self.page1 = Page1(self.parent)
        self.page2 = Page2(self.parent)

        self.tab = QTabWidget()
        self.tab.insertTab(0, self.page1, 'FIND')
        self.tab.insertTab(1, self.page2, 'REPLACE')

        grid.addWidget(self.tab)

        self.tab.setCurrentIndex(i)

        self.setGeometry(800, 300, 600, 100)