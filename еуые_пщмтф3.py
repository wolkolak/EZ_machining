from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt


class Color(QtWidgets.QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(color))
        self.setPalette(palette)


class TabBar(QtWidgets.QTabBar):
    def tabSizeHint(self, index):
        s = QtWidgets.QTabBar.tabSizeHint(self, index)
        s.transpose()
        return s

    def paintEvent(self, event):
        painter = QtWidgets.QStylePainter(self)
        opt = QtWidgets.QStyleOptionTab()

        for i in range(self.count()):
            self.initStyleOption(opt, i)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabShape, opt)
            painter.save()

            s = opt.rect.size()
            s.transpose()
            r = QtCore.QRect(QtCore.QPoint(), s)
            r.moveCenter(opt.rect.center())
            opt.rect = r

            c = self.tabRect(i).center()
            painter.translate(c)
            painter.rotate(90)
            painter.translate(-c)
            painter.drawControl(QtWidgets.QStyle.CE_TabBarTabLabel, opt);
            painter.restore()


class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, *args, **kwargs):
        QtWidgets.QTabWidget.__init__(self, *args, **kwargs)
        self.setTabBar(TabBar(self))
        self.setTabPosition(QtWidgets.QTabWidget.West)


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(800, 400)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)         # !!!

        self.tabs = TabWidget()                                                  # QtWidgets.QTabWidget()

        self.tabs.setTabPosition(QtWidgets.QTabWidget.West)                      #
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
        self.tabs.addTab(QtWidgets.QLabel('1', alignment=QtCore.Qt.AlignCenter),
                QIcon('images/info.ico'), '')                                    # 'Вкладка 1'

        self.tabs.addTab(QtWidgets.QLabel('2'), QIcon('head3.png'), '')          # , 'Вкладка 2'
        self.tabs.setIconSize(QtCore.QSize(50, 50))

        for n, color in enumerate(['red','green','blue','yellow']):
            self.tabs.addTab( Color(color), color)

        self.tabs.setCurrentIndex(0)

        box = QtWidgets.QVBoxLayout(self)
        box.addWidget(self.tabs)
        box.setContentsMargins(0, 0, 0, 0)

    def closeTab(self, index):
        tab = self.tabs.widget(index)
        tab.deleteLater()
        self.tabs.removeTab(index)


qss = '''
QTabBar {
    background: #c3c3c3;          
}
QTabBar::tab {
    background: rgb(34, 137, 163);
    color: white;
}
QTabBar::tab:selected {
    background-color: rgb(48, 199, 184,);
    color: #000000;
}
QLabel {
    background-color: #23272a;
    font-size: 22px;
    padding-left: 5px;
    color: white;
}
'''


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qss)                             # +
    window = MyWindow()
    window.setWindowTitle('QTabWidget')
    window.show()
    sys.exit(app.exec_())