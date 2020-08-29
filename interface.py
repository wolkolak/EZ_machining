from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main import settings
import gui_classes


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.splitter_flag = 1

        self.setWindowTitle('EZ machining')
        self.setGeometry(100, 100, settings['main_width'], settings['main_height'])

        openAction = QAction(QIcon('icons\open.png'), 'Open', self)
        openAction.setStatusTip('Open GM Fail')
        openAction.triggered.connect(self.open_file)

        exitAction = QAction(QIcon('icons\exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        splitterMove.triggered.connect(self.close_half)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(exitAction)


        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction(splitterMove)

        toolsMenu = menubar.addMenu('&Tools')
        inportMenu = menubar.addMenu('&Import')
        optionsMenu = menubar.addMenu('&Options')




        toolbar1 = QToolBar(self)
        self.addToolBar( Qt.LeftToolBarArea, toolbar1)
        toolbar1.setStyleSheet("background-color: {}".format(gui_classes.color3))
        toolbar1.addAction(exitAction)

        txt_tools = QToolBar(self)
        self.addToolBar( Qt.RightToolBarArea, txt_tools)
        txt_tools.setStyleSheet("background-color: {}".format(gui_classes.color3))
        txt_tools.addAction(splitterMove)

        self.centre = gui_classes.CenterWindow()

        self.setCentralWidget(self.centre)
        self.statusBar()




    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self,
        "Open файлик", "D:\Py_try\EZ_machining\examples", "Text files (*.txt);;All files (*.*)")
        print(path)
        flag = False
        try:
            text = open(path).read()
            try:
                name_open_file = path[path.rindex('/') + 1:-1]
            except ValueError:
                name_open_file = path
            self.centre.note.addTab(gui_classes.MyEdit(text, existing=path), name_open_file)

            flag = True
        except BaseException:
            if flag is not True:
                gui_classes.simple_warning('warning', "У файла формат не тот \n ¯\_(ツ)_/¯ ")




        
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