
from PyQt5.QtWidgets import QFileDialog, QWidget, QPushButton, QVBoxLayout, QDialog, QApplication

class FileDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QFileDialog.ExistingFiles)

    def accept(self):
        super(FileDialog, self).accept()

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        dialog = FileDialog()
        if dialog.exec_() == QDialog.Accepted:
            print(dialog.selectedFiles())

if __name__ == '__main__':

    import sys
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())