
from PyQt5 import Qt
import sys
import HL_Syntax1, HLSyntax.HL_Syntax
from PyQt5.QtWidgets import QPushButton, QGridLayout, QPlainTextEdit, QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont

class MyW(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('nyak1')
        grid = QGridLayout()
        self.setLayout(grid)

        self.editor = QPlainTextEdit()
        self.editor.setMinimumSize(100,100)
        self.check = QPushButton("check syntax")
        self.lb = QPlainTextEdit()
        self.lb.setStyleSheet("QLabel {"
                                 "border-style: solid;"
                                 "border-width: 1px;"
                                 "border-color: black; "
                                 "}")
        self.editor.setMinimumSize(40,100)
        grid.addWidget(self.editor, 0, 0, 2, 1)
        grid.addWidget(self.check, 0, 1)
        grid.addWidget(self.lb, 1, 1)
        font = QFont()
        font.setPointSize(12)
        self.editor.setFont(font)
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor.document())
        self.resize(700, 400)
        # Загрузите что-нибудь (например, editor_2.py) в редактор для демонстрации.
        infile = open('D:\Py_try\EZ_machining\examples\g1_billion.txt', 'r')
        self.editor.setPlainText(infile.read())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyW()
    ex.show()
    sys.exit(app.exec_())






