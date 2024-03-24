from PyQt5.QtWidgets import QDialog, QGridLayout, QFrame, QScrollArea, QPlainTextEdit, QTreeWidget, QTreeWidgetItem, QLabel, QPushButton, QLineEdit


class ShortHelp(QDialog):
    def __init__(self, father, address: str, w, h, *args, **kwargs):
        super().__init__(*args, **kwargs)
        last = address.split('/')
        a = last[-1]
        a_ = a.split('.')
        title = a_[0]
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(w, h)
        self.setWindowTitle(title)
        with open(address) as file:
            help_text = file.read()
        self.father = father
        grid = QGridLayout()
        self.setLayout(grid)
        self.help_me_tool_register = QPlainTextEdit()
        self.help_me_tool_register.setReadOnly(True)
        self.help_me_tool_register.setPlainText(help_text)
        grid.addWidget(self.help_me_tool_register, 0, 0)
