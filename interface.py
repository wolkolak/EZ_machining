from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QTextEdit, QWidget, QSplitter
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main import settings
class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def ololo(self):
        print('ololo')

    def initUI(self):

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