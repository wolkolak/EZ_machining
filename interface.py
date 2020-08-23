from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QTextEdit, QWidget, QSplitter, QTabWidget,\
    QScrollBar, QLabel, QHBoxLayout, QPushButton, QFrame, QTabBar
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtCore import Qt
from main import settings



class Tabs(QTabWidget):

    quantity = 10
    tabs = [["File" + str(i), None] for i in range(1, quantity)]
    print(tabs)
    def __init__(self):
        super().__init__()
        self.new_button = QFrame()
        self.addTab(self.new_button, "NEW")
        self.new_tab()
        self.new_tab()

        self.setTabsClosable(True)
        self.setMovable(True)


        # Tab button's
        self.tabBar().setTabButton(0, self.tabBar().RightSide, None)
        #self.tabBar().setTabPosition(0, self.tabBar().RightSide, None)
        self.tabBar().RightSide

        self.tabCloseRequested.connect(self.delete_tab)
        self.currentChanged.connect(self.change_new_tab)

    def change_new_tab(self):
        if self.currentIndex() == 0:
            print('new')
        print('change')

    def delete_tab(self, n):

        self.removeTab(n)
        self.tabs[n][1] = None

    def new_tab(self):
        i = 0
        flag = False
        while flag is False & (i < self.quantity):
            if self.tabs[i][1] is None:
                self.tabs[i][1] = QTextEdit()
                self.tabs[i][1].setWordWrapMode(QTextOption.NoWrap)
                self.addTab(self.tabs[i][1], self.tabs[i][0])
                print(flag)
                flag = True

            i += 1
        if not flag:
            print('Ну хорош уже вкладки создавать, надоел')





class CenterWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        centr_grid = QGridLayout()
        self.setLayout(centr_grid)
        self.setStyleSheet("background-color: gray")

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet('background-color:green')

        centr_grid.addWidget(splitter)

        self.left = QWidget()
        self.left.setStyleSheet("background-color: cyan")
        splitter.addWidget(self.left)

        self.right = QWidget()
        self.right.setStyleSheet("background-color: yellow")
        splitter.addWidget(self.right)


        self.note = Tabs()

        grid_right = QGridLayout()
        self.right.setLayout(grid_right)
        grid_right.addWidget(self.note, 0, 0)

        splitter.setSizes([100, 200])




class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()



    def initUI(self):
        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings['main_width'], settings['main_height'])



        printAction = QAction(QIcon('exit24.png'), 'ololo', self)
        printAction.triggered.connect(self.ololo)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)



        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(printAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)



        self.toolbar = self.addToolBar('New')
        self.toolbar.addAction(exitAction)

        centre = CenterWindow()

        self.setCentralWidget(centre)
        self.statusBar()


    def ololo(self):
        print('ololo')