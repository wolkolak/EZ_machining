from PyQt5.QtWidgets import QToolBar, QAction, QPushButton
from PyQt5.QtCore import Qt
from Settings import settings



class MyTextToolBar(QToolBar):
    def __init__(self, my_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_window = my_window
        self.setStyleSheet("background-color: {}".format(settings.color3))
        #self.addAction(self.my_window.splitterMove)
        #self.my_window.addToolBar(Qt.RightToolBarArea, self)



