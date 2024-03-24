from PyQt5.QtWidgets import QToolBar
from PyQt5.QtCore import Qt
from Settings import settings
from Gui.gui_classes import AnimationModes


class MyViewToolBar(QToolBar):
    def __init__(self, my_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.my_window = my_window
        self.setStyleSheet(
            "QToolTip {{ color: #ffffff; background-color: #000000; border: 0px; font: 14px;}} "
            "QToolBar {{background-color: {}; }}".format(settings.color3))
        self.addAction(self.my_window.splitterMove)
        self.my_window.addToolBar(Qt.TopToolBarArea, self)
        self.animationMode = AnimationModes(self)
        self.addWidget(self.animationMode)
        self.orientationChanged.connect(self.change_bar)


    def change_bar(self):
        x = self.orientation()
        if x == 1:
            self.HorVert = 'Hor'
        else:
            self.HorVert = 'Vert'
        print('self.HorVert = ', self.HorVert)
        self.animationMode.refresh_layout()
        #refresh animation mode


