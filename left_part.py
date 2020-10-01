from PyQt5.QtWidgets import QSplitter, QTabWidget, QHBoxLayout,  \
    QFrame, QTabBar,  QMessageBox, QPlainTextEdit,  QWidget, QGridLayout
from PyQt5.QtCore import Qt, QRect, QSize
import redactor
from settings import *


class checker(QPlainTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.setReadOnly(True)

class leftTab(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        a = checker()
        self.addTab(a, 'text_read')
        b = QFrame()
        self.addTab(b, 'visual')


class left1(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(color1))

        grid = QGridLayout()
        self.setLayout(grid)
        self.left_tab = leftTab()
        grid.addWidget(self.left_tab, 0, 0)


