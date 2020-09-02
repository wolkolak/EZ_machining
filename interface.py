from PyQt5.QtWidgets import QMainWindow, QAction, qApp,  QToolBar, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from main import settings
import gui_classes


class MyMainWindow(QMainWindow):


    filter_files = "Text files (*.txt);;All files (*.*)"
    file_formats = [filter_files.split(';;')]
    ff = file_formats[0][0]
    ff = ff[ff.rindex('*') + 1:-1]
    #file_formats = ['a','b']
    print('format are :', ff)
    #path[path.rindex('/') + 1:-1]
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

        saveAsAction = QAction(QIcon('icons\save_as.png'), 'Save As', self)
        saveAsAction.setStatusTip('Save File As')
        saveAsAction.triggered.connect(self.save_file_as)

        closeTab = QAction(QIcon('icons\save_as.png'), 'Close Tab', self)
        closeTab.setStatusTip('Close Current')
        closeTab.triggered.connect(self.close_current)

        closeAll = QAction(QIcon('icons\save_as.png'), 'Close All', self)
        closeAll.setStatusTip('Close All Tabs')
        closeAll.triggered.connect(self.close_all)

        exitAction = QAction(QIcon('icons\exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)


        splitterMove = QAction(QIcon('icons\splitter.png'), 'shift', self)
        splitterMove.triggered.connect(self.close_half)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newTabAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(saveAsAction)
        fileMenu.addAction(closeTab)
        fileMenu.addAction(closeAll)
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

    def close_all(self):
        while self.centre.note.currentIndex() != -1:
            self.close_current()


    def close_current(self):
        self.centre.note.delete_tab(self.centre.note.currentIndex())

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path, _ = QFileDialog.getOpenFileName(self,
        "Open файлик", "D:\Py_try\EZ_machining\examples", self.filter_files)
        print(path)
        self.make_open_DRY(path, None)

    def save_file_as(self):
        print('saving as')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #todo
        path, _ = QFileDialog.getSaveFileName(self, "Save As", "D:\Py_try\EZ_machining\examples\\"+
                                              self.centre.note.tabText(self.centre.note.currentIndex())+str(self.ff),
                                              self.filter_files, options=options)
        #path[path.rindex('/') + 1:-1]
        print('___:', _)
        if path:
            text = self.centre.note.currentWidget().toPlainText()
            file = open(path, 'w')
            file.write(text)
            file.close()
            n = self.centre.note.currentIndex()
            self.make_open_DRY(path, n)

            # todo  расширение прикрутить
            print(path)

    def save_file(self):

        print(self.centre.note.currentWidget().existing)
        if self.centre.note.currentWidget().existing is False:
            self.save_file_as()
            return
        print('saving file')
        path = self.centre.note.currentWidget().existing
        if path:
            text = self.centre.note.currentWidget().toPlainText()
            file = open(path, 'w')
            file.write(text)
            file.close()
            n = self.centre.note.currentIndex()
            self.make_open_DRY(path, n)
            print(path)


    def make_open_DRY(self, path, n):
        flag = False
        try:
            text = open(path).read()
            try:
                name_open_file = path[path.rindex('/') + 1:]
                print(name_open_file)
            except ValueError:
                name_open_file = path
            self.centre.note.insertTab(self.centre.note.currentIndex()+1, gui_classes.MyEdit(text, existing=path), name_open_file)
            self.centre.note.setCurrentIndex(self.centre.note.currentIndex()+1)
            if n is not None:
                self.centre.note.removeTab(n)
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