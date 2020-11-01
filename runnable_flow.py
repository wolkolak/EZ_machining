from PyQt5.QtCore import Qt, QRect, QSize, QRunnable, pyqtSignal, QTimer

class Worker(QRunnable):

    def __init__(self, func_to_execute, percent_panel):
        super().__init__()
        self.func = func_to_execute

    def run(self):
        print('start running')
        value = 1000
        print(self.func)
        #self.stastSignal.emit(value)
        self.func()
        print('vse')
        #self.finishSignal.emit("Готово!")