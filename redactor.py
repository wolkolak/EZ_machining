from PyQt5.QtWidgets import  QGridLayout,  QLabel,  QPushButton, QPlainTextEdit, QDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption, QColor, QPainter, QPalette, QBrush, QTextCursor, QTextDocument

from settings import *


class MyEdit(QPlainTextEdit):# QPlainTextEdit

    def __init__(self, text, existing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.existing = existing
        self.setStyleSheet("background-color: {}".format(color4))
        self.setPlainText(text)
        self.changed = False
        self.textChanged.connect(self.changing)

    def changing(self):
        self.changed = True

    def find_in_text(self):
        rez = finder(self).exec()


class finder(QDialog):
    def __init__(self, papka, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.papka = papka
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('Find')
        self.string_to_find = QPlainTextEdit()
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



        self.setGeometry(800, 300, 600, 100)

    def all_mention(self):
        pass

    def naiv_find(self, direction):
        flag = None
        all1 = [self.string_to_find.toPlainText()]
        if direction:
            flag = QTextDocument.FindBackward
        if flag:
            all1.append(flag)
        start_position = self.papka.textCursor()

        if self.papka.find(*all1):
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
