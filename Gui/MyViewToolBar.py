from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt
from Settings import settings


class MyViewToolBar(QToolBar):
    def __init__(self, my_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_window = my_window
        #self.setStyleSheet("QToolTip { color: #ffffff; background-color: #000000; border: 0px; }")
        self.setStyleSheet(
            "QToolTip {{ color: #ffffff; background-color: #000000; border: 0px; font: 14px;}} "
            "QToolBar {{background-color: {}; }}".format(settings.color3))
        self.addAction(self.my_window.splitterMove)
        self.my_window.addToolBar(Qt.TopToolBarArea, self)
