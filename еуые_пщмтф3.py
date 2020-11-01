
from PyQt5        import QtCore, QtWidgets, QtGui, uic
from PyQt5.QtCore import QThread, pyqtSignal, QTimer

#import os
#import yadisk
import sys

#y = yadisk.YaDisk(token="токен яндекс диска")

class ThreadClass(QThread):
    stastSignal = pyqtSignal(int)
    finishSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ThreadClass, self).__init__(parent)

    def run(self):
#   это ваша длительная задача, 
#   попробуйте ее ракомментировать, а то что между  `# +++ str` и `# +++ end` убрать
#
#        if os.path.exists('test.zip'):
#            print('Удаление...')
#            os.remove('test.zip')
#        print('Загрузка...')
###        value = 1000                  # какое-то значение, которое можем использовать для progressBar
###                                      # например размер загружаемого 'test.zip'
###        self.stastSignal.emit(value)
#        y.download("/Загрузки/test.zip", 'test.zip')

# +++ str        
        value = 1000 # 
        self.stastSignal.emit(value)
        while value:
            value -= 10
            self.msleep(100)  
# +++ end    

        # этот сигнал сработает когда загрузка закончится
        self.finishSignal.emit("Готово!")


class MainWindow(QtWidgets.QMainWindow): 
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

#        uic.loadUi("design.ui", self)
#        self.pushButton.clicked.connect(self.onButton)

        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setProperty("value", 0)

        self.pushButton = QtWidgets.QPushButton("Start")
        self.pushButton.clicked.connect(self.onButton)

        self.layout = QtWidgets.QVBoxLayout(self.centralwidget)                
        self.layout.addWidget(self.progressBar)
        self.layout.addWidget(self.pushButton)

        self.threadclass = ThreadClass()
        self.threadclass.stastSignal.connect(self.stast_process)
        self.threadclass.finishSignal.connect(self.finishSignal_process)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timeout_func)

        self.value = ...

    def onButton(self):
        self.pushButton.setEnabled(False)
        self.progressBar.setValue(0)
        self.threadclass.start()

    def stast_process(self, val):
        self.value = val // 100   
        self.timer.start(1000)

    def finishSignal_process(self, val): 
        self.progressBar.setValue(100)    
        self.timer.stop()
        self.pushButton.setEnabled(True)
        print(val)

    def timeout_func(self):
        self.progressBar.setValue(self.value)
        self.value += 10

if __name__ == "__main__":
    app   = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_()) 