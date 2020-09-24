from PyQt5.QtWidgets import  QSplitter, QTabWidget, QHBoxLayout,  \
    QFrame, QTabBar,  QMessageBox, QFileDialog, QFontDialog

from redactor import *
from settings import *


class My_Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(font3)

class coloredTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFont(font2)


current_files = []

class Tabs(QTabWidget):

    filter_files = "Text files (*.txt);;All files (*.*)"
    file_formats = [filter_files.split(';;')]
    ff = file_formats[0][0]
    ff = ff[ff.rindex('*') + 1:-1]
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

        self.new_tab_button = My_Button("NEW")
        little_layout.addWidget(self.new_tab_button)
        self.new_tab_button.setStyleSheet("background-color: {}".format(color1))
        self.new_tab_button.clicked.connect(self.new_tab)

        self.save_tab_button = My_Button("SAVE")
        little_layout.addWidget(self.save_tab_button )
        self.save_tab_button.setStyleSheet("background-color: {}".format(color1))

        self.cornerWidget().setMinimumSize(20, 40)
        self.tabCloseRequested.connect(self.delete_tab)

        #todo унаследовать нормально
        stylesheet = """ 
               QTabBar::tab:selected {background: rgb(145,191,204)}
               QTabWidget>QWidget>QWidget{background: gray;}
               """

        self.setStyleSheet(stylesheet)



    def delete_tab(self, n):

        name = self.widget(n).existing
        if not name:
            name = self.tabText(n)
        print('tab delete:', name)
        if self.widget(n).changed:
            if 'Cancel' != simple_2_dialog(self.save_file, lambda: self.close_only(n), "Save changes in {}?".format(self.tabText(n))):
                self.removeTab(n)
                remove_new_name(name)

        else:
            self.close_only(n)
            self.removeTab(n)
            if name:
                remove_new_name(name)


    def close_only(self, n):
        if self.widget(n).existing is False:
            for i in range(1, self.quantity - 1):
                if self.tabs[i][0] == self.tabText(n):
                    self.tabs[i][1] = None
                    break

    def new_tab(self):
        print('tab create')
        i = 1
        while (i < self.quantity-1) & (self.tabs[i][1] is not None):
            i += 1
        if self.tabs[i][1] is None:
            self.tabs[i][1] = True
            print('new tab1')
            self.insertTab(self.currentIndex()+1, MyEdit(None, existing=False, base=self), self.tabs[i][0])
            print('new tab1')
            self.setCurrentIndex(self.currentIndex()+1)
            add_new_name(self.tabs[i][0])
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
            self.make_open_DRY(path)

    def save_file_as(self):
        if self.currentIndex() == -1:
            return
        print('saving as')
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        name = "D:\Py_try\EZ_machining\examples\\" + self.tabText(self.currentIndex())
        if self.currentWidget().existing is False:
            name += str(self.ff)
        path, _ = QFileDialog.getSaveFileName(None, "Save As", name,
                                              self.filter_files, options=options)

        if path in current_files:
            simple_warning('Nope, not recommended!', 'File name already \ntaking part in session')
            return
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
            add_new_name(name)

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


    def make_open_DRY(self, path):
        if path in current_files:
            simple_warning('Nope, not recommended!', 'File name already taking part in session')
            return
        try:
            text = open(path).read()
            try:
                name_open_file = path[path.rindex('/') + 1:]
            except ValueError:
                name_open_file = path

            self.insertTab(self.currentIndex()+1, MyEdit(text, existing=path, base=self), name_open_file)
            self.setCurrentIndex(self.currentIndex()+1)
            self.currentWidget().existing = path
            add_new_name(path)
        except BaseException:
            simple_warning('warning', "У файла формат не тот \n ¯\_(ツ)_/¯ ")

class left1(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(color1))

def add_new_name(name):
    current_files.append(name)
    print('current_files', current_files)
def remove_new_name(name):
    current_files.remove(name)
    print('current_files', current_files)

class right2(QWidget):
    def __init__(self, base, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base = base
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyleSheet("background-color: {}".format(color2))
        self.setAcceptDrops(True)

    def dragEnterEvent(self, e):

        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        # self.addItem(e.mimeData().text())
        nya = e.mimeData().text()
        nya = nya[8:]
        print(nya)

        self.base.note.make_open_DRY(nya)


class CenterWindow(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        centr_grid = QGridLayout()
        self.setLayout(centr_grid)
        self.setStyleSheet("background-color: gray")

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.setStyleSheet('background-color:green')

        centr_grid.addWidget(self.splitter)
        self.left = left1()
        self.splitter.addWidget(self.left)
        self.right = right2(self)
        self.splitter.addWidget(self.right)
        self.note = Tabs()
        grid_right = QGridLayout()
        self.right.setLayout(grid_right)
        grid_right.addWidget(self.note, 0, 0)

        self.splitter.setSizes([splitter_parameters['lefty'], splitter_parameters['righty']])

        #self.setAcceptDrops(True)

        #print('drop:', self.acceptDrops())



class m_f_d(QFontDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def my_font_diag():
    pass


def simple_warning(title, text):
    warning = QMessageBox()
    warning.setWindowTitle(title)
    warning.setText(text)
    warning.exec()

def simple_2_dialog(func1, func2, title):
   save_or_throw = QMessageBox()
   save_or_throw.setWindowTitle(title)
   #save_or_throw.setText(text)
   save_or_throw.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
   rez = save_or_throw.exec()
   if rez == QMessageBox.Yes:
       func1()
   elif rez == QMessageBox.No:
       func2()
   else:
       return 'Cancel'

