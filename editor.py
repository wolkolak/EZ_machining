from PyQt5 import Qt
import HL_Syntax

app    = Qt.QApplication([])
editor = Qt.QPlainTextEdit()

font = Qt.QFont()
font.setPointSize(12)
editor.setFont(font)

highlight = HL_Syntax.PythonHighlighter(editor.document())
editor.show()
editor.resize(700, 400)

# Загрузите что-нибудь (например, editor_2.py) в редактор для демонстрации.
infile = open('editor.py', 'r')
editor.setPlainText(infile.read())

app.exec_()