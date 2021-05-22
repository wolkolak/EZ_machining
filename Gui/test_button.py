from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import Settings


def test_opt(self):
    self.testAction = QAction(QIcon('../icons/open.png'), 'test', self)
    self.testAction.setStatusTip('Test')
    self.testAction.triggered.connect(lambda: test_func(self))
    self.testAction.setShortcut('Ctrl+Q')



    self.testMenu = self.menubar.addMenu('&test')
    self.testMenu.addAction(self.testAction)

def test_func(self):
    print('test start')
    #self.centre.note.currentWidget().editor.self.blockCount()
    print('blockCount = {}'.format(self.centre.note.currentWidget().editor.blockCount()))
