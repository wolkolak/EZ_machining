from PyQt5 import QtCore
import PyQt5.QtWidgets as QtGui



import sys



class coloredTabBar(QtGui.QTabBar):
    def __init__(self, parent = None):
        QtGui.QTabBar.__init__(self, parent)



    def paintEvent(self, event):
        p = QtGui.QStylePainter(self)
        painter = QtGui.QPainter(self)
        painter.save()
        for index in range(self.count()): #for all tabs



            tabRect = self.tabRect(index)
            tabRect.adjust(-1, 3, -1, -1) #ajust size of every tab (make it smaller)
            if index == 0: #make first tab red
                color = QtGui.QColor(255, 0, 0)
            elif index == 1: #make second tab yellow
                color = QtGui.QColor(255, 255, 0)
            else: #make all other tabs blue
                color = QtGui.QColor(0, 0, 255)
            if index == self.currentIndex(): #if it the selected tab
                color = color.lighter(130) #highlight the selected tab with a 30% lighter color
                tabRect.adjust(0, -3, 0, 1) #increase height of selected tab and remove bottom border



            brush = QtGui.QBrush(color)
            painter.fillRect(tabRect, brush)



            painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.black))) #black pen (for drawing the text)
            painter.drawText(tabRect, QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter,
                             self.tabText(index))



            painter.setPen(QtGui.QPen(QtGui.QColor(QtCore.Qt.gray))) #gray pen (for drawing the border)
            painter.drawRect(tabRect)
        painter.restore()



class coloredTabWidget(QtGui.QTabWidget):
    def __init__(self, parent = None):
        QtGui.QTabWidget.__init__(self, parent)



        coloredTabs = coloredTabBar()
        self.setTabBar(coloredTabs) #replace default tabBar with my own implementation



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)



    tabWidget = coloredTabWidget()



    tabWidget.addTab(QtGui.QWidget(), "Tab 1")
    tabWidget.addTab(QtGui.QWidget(), "Tab 2")
    tabWidget.addTab(QtGui.QWidget(), "Tab 3")
    tabWidget.addTab(QtGui.QWidget(), "Tab 4")



    tabWidget.show()



    sys.exit(app.exec_())