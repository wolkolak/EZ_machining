from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QGridLayout, QTextEdit, QWidget, QSplitter, QTabWidget,\
    QScrollBar, QLabel, QHBoxLayout, QPushButton, QFrame, QTabBar, QToolBar, QMessageBox, QStyle, QStylePainter,\
    QStyleOption, QStyleOptionTab, QFileDialog
import gui_classes
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption, QColor, QPainter, QPalette, QBrush

color1 = 'rgb(145,191,204)'
color2 = 'rgb(72,128,143)'
color3 = 'rgb(47, 69, 82)'
color4 = 'rgb(195,221,234)' #бледный




class coloredTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MyEdit(QTextEdit):

    def __init__(self, text, existing, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.existing = existing
        self.setStyleSheet("background-color: {}".format(color4))
        self.setText(text)
        self.changed = False
        self.textChanged.connect(self.changing)


    def changing(self):
        self.changed = True

class Tabs(QTabWidget):

    filter_files = "Text files (*.txt);;All files (*.*)"
    file_formats = [filter_files.split(';;')]
    ff = file_formats[0][0]
    ff = ff[ff.rindex('*') + 1:-1]
    #file_formats = ['a','b']
    print('format are :', ff)

    quantity = 15
    tabs = [["File" + str(i), None] for i in range(0, quantity)]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colored_tabbar = coloredTabBar()
        self.setTabBar(self.colored_tabbar)
        self.setTabsClosable(True)
        self.setMovable(True)

        self.little_widget = QFrame()

        little_layout = QHBoxLayout()
        self.little_widget.setLayout(little_layout )
        self.setCornerWidget(self.little_widget)

        self.new_tab_button = QPushButton("NEW")
        little_layout.addWidget(self.new_tab_button)
        self.new_tab_button.setStyleSheet("background-color: {}".format(color1))
        self.new_tab_button.clicked.connect(self.new_tab)

        self.save_tab_button = QPushButton("SAVE")
        little_layout.addWidget(self.save_tab_button )
        self.save_tab_button.setStyleSheet("background-color: {}".format(color1))
        #save_tab_button connected from interface

        self.cornerWidget().setMinimumSize(20, 40)
        self.tabCloseRequested.connect(self.delete_tab)
        self.currentChanged.connect(self.change_title)

    def change_title(self, n):
        print('tab change')

        if self.currentIndex() != -1:
            if self.currentWidget().existing is False:
                title2 = self.tabText(n)
            else:
                title2 = self.currentWidget().existing
            self.window().setWindowTitle('EZ machining:  {}'.format(title2))
        else:
            self.window().setWindowTitle('EZ machining')

    def delete_tab(self, n):
        print('tab delete')
        if self.currentWidget().changed == False:
            if self.widget(n).existing is False:
                for i in range(1, self.quantity-1):
                    if self.tabs[i][0] == self.tabText(n):
                        self.tabs[i][1] = None
                        break
            self.removeTab(n)
        else:
            print(self.__dict__['little_widget'].__dict__)



    def new_tab(self):
        print('tab create')
        i = 1
        while (i < self.quantity-1) & (self.tabs[i][1] is not None):
            i += 1
        if self.tabs[i][1] is None:
            self.tabs[i][1] = True
            self.insertTab(self.currentIndex()+1, MyEdit(None, existing=False), self.tabs[i][0])
            self.setCurrentIndex(self.currentIndex()+1)
        else:
            simple_warning('warning', "Притормози \n ¯\_(ツ)_/¯")


    def close_all(self):
        while self.currentIndex() != -1:
            self.close_current()


    def close_current(self):
        self.delete_tab(self.currentIndex())

    def open_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        print('QFileDialog.DontUseNativeDialog')
        path, _ = QFileDialog.getOpenFileName(None,
        "Open файлик", "D:\Py_try\EZ_machining\examples", self.filter_files)
        print(path)
        if path:
            self.make_open_DRY(path, True)

    def save_file_as(self):
        print('saving as')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name = "D:\Py_try\EZ_machining\examples\\"+ self.tabText(self.currentIndex())
        if self.currentWidget().existing is False:
            name += str(self.ff)
        path, _ = QFileDialog.getSaveFileName(None, "Save As", name,
                                              self.filter_files, options=options)
        print('___:', _)
        print('path', path)
        if path:
            text = self.currentWidget().toPlainText()
            with open(path, 'w') as file:

                file.write(text)

            self.currentWidget().changed = False
            self.currentWidget().existing = path
            try:
                name_open_file = path[path.rindex('/') + 1:]
            except ValueError:
                name_open_file = path
            self.setTabText(self.currentIndex(), name_open_file)
            self.window().setWindowTitle(path)
            print(path)

    def save_file(self):

        print(self.currentWidget().existing)
        if self.currentWidget().existing is False:
            print('is false')
            self.save_file_as()
            return
        print('saving file')
        path = self.currentWidget().existing
        if path:
            text = self.currentWidget().toPlainText()
            with open(path, 'w') as file:
                file.write(text)
            self.currentWidget().changed = False
            print(path)


    def make_open_DRY(self, path, open1):
        try:
            text = open(path).read()
            try:
                name_open_file = path[path.rindex('/') + 1:]
            except ValueError:
                name_open_file = path

            self.insertTab(self.currentIndex()+1, MyEdit(text, existing=path), name_open_file)
            self.setCurrentIndex(self.currentIndex()+1)
            self.currentWidget().existing = path
        except BaseException:
            gui_classes.simple_warning('warning', "У файла формат не тот \n ¯\_(ツ)_/¯ ")


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

def simple_warning(title, text):
    warning = QMessageBox()
    warning.setWindowTitle(title)
    warning.setText(text)
    warning.exec()
