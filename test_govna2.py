#!/usr/bin/python3
# -*- coding: utf-8 -*-


import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QGridLayout, QLabel, QLineEdit, QTextEdit, QWidget, QSplitter, QFrame
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import copy

#todo from settings
default_settings = {'main_width': 1450, 'main_height': 900, 'font_txt': "nyaa", 'txt_width': 600}
settings = copy.deepcopy(default_settings)

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def ololo(self):
        print('ololo')

    def initUI(self):

        title = QLabel('Title')




        printAction = QAction(QIcon('exit24.png'), 'ololo', self)
        printAction.triggered.connect(self.ololo)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        self.statusBar()
        centr = QWidget()
        centr_grid = QGridLayout()
        centr.setLayout(centr_grid)
        self.setCentralWidget(centr)
        centr.setStyleSheet("background-color: gray")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(printAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)



        self.setGeometry(100, 100, settings['main_width'], settings['main_height'])
        self.setWindowTitle('EZ machining')


        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet('background-color:green')

        centr_grid.addWidget(splitter)



        self.left = QWidget()
        self.left.setStyleSheet("background-color: cyan")
        splitter.addWidget(self.left )

        self.right = QWidget()
        self.right.setStyleSheet("background-color: yellow")
        splitter.addWidget(self.right )

        self.textEdit = QTextEdit(self)
        grid_right = QGridLayout()
        self.right.setLayout(grid_right)
        grid_right.addWidget(self.textEdit, 0, 0)

        splitter.setSizes([100, 200])


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()

    title = QLabel('Title')

    ex.show()#иначе сохранять состояние окна нельзя будет
    sys.exit(app.exec_())
