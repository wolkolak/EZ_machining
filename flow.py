from PyQt5.QtCore import Qt, QRect, QSize, QThread, pyqtSignal, QTimer

class ThreadClass(QThread):
    stastSignal = pyqtSignal(int)
    finishSignal = pyqtSignal(str)

    def __init__(self, func_to_execute, percent_panel, parent=None, ):
        super(ThreadClass, self).__init__(parent)

    def run(self):
        pass