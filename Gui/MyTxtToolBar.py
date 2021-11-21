from PyQt5.QtWidgets import QToolBar, QAction, QPushButton
from PyQt5.QtCore import Qt
from Settings import settings



class MyTextToolBar(QToolBar):
    def __init__(self, my_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_window = my_window
        self.addAction(self.my_window.exitAction)
        #self.setStyleSheet("background-color: {}; QToolTip {{ color: #ffffff; background-color: #000000; border: 0px; }}".format(settings.color3))

        self.setStyleSheet(
            "QToolTip {{ color: #ffffff; background-color: #000000; border: 0px; font: 14px;}} "
            "QToolBar {{background-color: {}; }}".format(settings.color3))

        #self.setStyleSheet("background-color: {}".format(settings.color3))
        #self.addAction(self.my_window.splitterMove)
        #self.my_window.addToolBar(Qt.RightToolBarArea, self)

        self.my_window.addToolBar(Qt.TopToolBarArea, self)



