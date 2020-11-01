from PyQt5.QtCore import Qt, QRect, QSize, QThread, pyqtSignal, QTimer

def foo():
    print('foo')
    n = 1
    while True:
        print('n = ', n)
        n += 1

class ThreadClass(QThread):
    stastSignal = pyqtSignal(int)
    finishSignal = pyqtSignal(str)

    def __init__(self, func_to_execute, percent_panel):
        super().__init__()
        self.func = func_to_execute


    def run(self):
        print('start running')
        value = 1000
        print(self.func)
        self.stastSignal.emit(value)
        self.func()
        print('vse')
        #self.finishSignal.emit("Готово!")
