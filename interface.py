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
        self.centre = gui_classes.CenterWindow()
        self.setCentralWidget(self.centre)
        self.statusBar()


        openAction = QAction(QIcon('icons\open.png'), 'Open', self)
        openAction.setStatusTip('Open GM File')
        openAction.triggered.connect(self.open_file)

        newTabAction = QAction(QIcon(r'icons\new_tab.png'), 'New', self)
        newTabAction.setShortcut('Ctrl+N')
        newTabAction.setStatusTip('New File')
        newTabAction.triggered.connect(self.centre.note.new_tab)

        saveAction = QAction(QIcon('icons\save.png'), 'Save', self)
        saveAction.setShortcut('Ctrl+S')
        saveAction.setStatusTip('Save current File')
        saveAction.triggered.connect(self.save_file)
        self.centre.note.save_tab_button.clicked.connect(self.save_file)

        exitAction = QAction(QIcon('icons\exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        splitterMove.triggered.connect(self.close_half)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openAction)
        fileMenu.addAction(newTabAction)
        fileMenu.addAction(saveAction)
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
            self.centre.note.insertTab(self.centre.note.currentIndex()+1, gui_classes.MyEdit(text, existing=path), name_open_file)
            self.centre.note.setCurrentIndex(self.centre.note.currentIndex()+1)

            flag = True
            #self.centre.note.colorTab(0)
        except BaseException:
            if flag is not True:
                gui_classes.simple_warning('warning', "У файла формат не тот \n ¯\_(ツ)_/¯ ")

    def save_file(self):
        print('saving')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        fileName, _ = QFileDialog.getSaveFileName(self, "Open bleat", "D:\Py_try\EZ_machining\examples",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        print('fdfddf')
        if fileName:
            text = self.centre.note.currentWidget().toPlainText()
            file = open(fileName, 'w')
            file.write(text)
            file.close()
            print(fileName)



        """        name = QFileDialog.getSaveFileName(self, 'Save File')
        print('1')
        file = open(name,'w')
        print('2')
        text = self.centre.note.currentWidget().toPlainText()
        print('3')
        file.write(text)
        file.close()"""


        
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