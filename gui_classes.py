from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QTextEdit, QWidget, QSplitter, QTabWidget,\
    QScrollBar, QLabel, QHBoxLayout, QPushButton, QFrame, QTabBar, QToolBar

from PyQt5.QtGui import QIcon, QTextOption
from PyQt5.QtCore import Qt

color1 = 'rgb(22,222,222)'
color2 = 'rgb(222,222,22)'
color3 = 'rgb(135, 108, 153)'




class Tabs(QTabWidget):

    quantity = 15
    tabs = [["File" + str(i), None] for i in range(0, quantity)]
    print(tabs)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #my_tab_bar = MyTabBar()
        #self.setTabBar( my_tab_bar)
        self.setTabsClosable(True)
        self.setMovable(True)
        #self.setAttribute(Qt.WA_DeleteOnClose) #useless

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

        print(type(n))
        # gets the widget
        #widget = self.widget(n)
        for i in range(1, self.quantity-1):
            #print('udol', self.accessibleName(n-1))
            if self.tabs[i][0] == self.tabText(n):
                print("вкладку удалил")
                self.tabs[i][1] = None
                break
        self.removeTab(n)
        #print(self.tabs)


    def new_tab(self):
        i = 1
        print(i,"____",self.tabs[i][1])
        while (i < self.quantity-1) & (self.tabs[i][1] is not None):
            i += 1
            print('i=',i)
        print('itog:', i)
        if self.tabs[i][1] is None:
            self.tabs[i][1] = 1
            self.addTab(QTextEdit(), self.tabs[i][0])
        else:
            print('too many new files, go away')


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
