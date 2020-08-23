from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QTextEdit, QWidget, QSplitter, QTabWidget,\
    QScrollBar, QLabel, QHBoxLayout, QPushButton, QFrame, QTabBar, QToolBar
from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtCore import Qt
from main import settings

color1 = 'rgb(22,222,222)'
color2 = 'rgb(222,222,22)'
color3 = 'rgb(135, 108, 153)'

class Tabs(QTabWidget):

    quantity = 10
    tabs = [["File" + str(i), None] for i in range(1, quantity)]
    print(tabs)
    def __init__(self):
        super().__init__()

        self.setTabsClosable(True)
        self.setMovable(True)

        self.little_widget = QFrame()

        little_layout = QHBoxLayout()
        self.little_widget.setLayout(little_layout )
        self.setCornerWidget(self.little_widget)

        self.new_tab_button = QPushButton("NEW")
        little_layout.addWidget(self.new_tab_button)
        self.new_tab_button.setStyleSheet("background-color: {}".format(color1))

        self.save_tab = QPushButton("SAVE")
        little_layout.addWidget(self.save_tab )
        self.save_tab.setStyleSheet("background-color: {}".format(color1))

        self.cornerWidget().setMinimumSize(20, 40)

        self.tabCloseRequested.connect(self.delete_tab)
        self.new_tab_button.clicked.connect(self.new_tab)


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

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet('background-color:green')

        centr_grid.addWidget(self.splitter)

        self.left = QWidget()
        self.left.setStyleSheet("background-color: {}".format(color1))
        self.splitter.addWidget(self.left)

        self.right = QWidget()
        self.right.setStyleSheet("background-color: {}".format(color2))
        self.splitter.addWidget(self.right)


        self.note = Tabs()

        grid_right = QGridLayout()
        self.right.setLayout(grid_right)
        grid_right.addWidget(self.note, 0, 0)

        self.splitter.setSizes([100, 200])




class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.splitter_flag = 1

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings['main_width'], settings['main_height'])



        printAction = QAction(QIcon('exit24.png'), 'ololo', self)
        printAction.triggered.connect(self.close_half)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)



        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(printAction)

        toolbar1 = QToolBar(self)
        self.addToolBar( Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(color3))
        toolbar1.addAction(exitAction)

        txt_tools = QToolBar(self)
        self.addToolBar( Qt.RightToolBarArea, txt_tools)
        txt_tools.setStyleSheet("background-color: {}".format(color3))
        txt_tools.addAction(printAction)

        self.centre = CenterWindow()

        self.setCentralWidget(self.centre)
        self.statusBar()



    def close_half(self):

        if self.splitter_flag == 1:
            self.centre.splitter.setSizes([100, 0])
            self.splitter_flag = self.splitter_flag + 1
        elif self.splitter_flag == 2:
            self.centre.splitter.setSizes([100, 100])
            self.splitter_flag = self.splitter_flag + 1
        else:
            self.centre.splitter.setSizes([0, 100])
            self.splitter_flag = 1
        print(self.splitter_flag )