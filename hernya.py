import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


#########################################################
#             STYLESHEET FOR QTABWIDGET                 #
#########################################################
def get_QTabWidget_style():
    styleStr = str("""
        QTabWidget::pane {             
            border-width: 2px;         
            border-style: solid;       
            border-color: #0000ff;         
            border-radius: 6px;        
        }                              
        QTabWidget::tab-bar {          
            left: 5px;                 
        }                              
    """)
    return styleStr

#########################################################
#               STYLESHEET FOR QTABBAR                  #
#########################################################
def get_QTabBar_style():
    styleStr = str("""
        QTabBar {                                          
            background: #00ffffff;                         
            color: #ff000000;                              
            font-family: Courier;                          
            font-size: 12pt;                               
        }                                                  
        QTabBar::tab {                  
            background: #00ff00;                         
            color: #000000;                              
            border-width: 2px;                             
            border-style: solid;                           
            border-color: #0000ff;                             
            border-bottom-color: #00ffffff;                
            border-top-left-radius: 6px;                   
            border-top-right-radius: 6px;                  
            min-height: 40px;                              
            padding: 2px 12px;                                  
        }                                                  
        QTabBar::tab:selected {                            
            border-color: #0000ff;                             
            border-bottom-color: #00ffffff;                
        }                                                  
        QTabBar::tab:!selected {                           
            margin-top: 2px;                               
        }                                                  
        QTabBar[colorToggle=true]::tab {                   
            background: #ff0000;                         
        }                                                  
    """)

    return styleStr


#########################################################
#                  SUBCLASS QTABBAR                     #
#########################################################
class MyTabBar(QTabBar):
    def __init__(self):
        QTabBar.__init__(self)
        self.colorIndexes = {
            1: QColor(Qt.red),
            3: QColor(Qt.blue),
        }

    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        option = QStyleOptionTab()
        option.features |= option.HasFrame
        palette = option.palette
        for index in range(self.count()):
            self.initStyleOption(option, index)
            palette.setColor(palette.Button, self.colorIndexes.get(index, QColor(Qt.green)))
            #palette.setColor(palette.Window, QColor(Qt.blue))
            option.palette = palette
            self.style().drawControl(QStyle.CE_TabBarTab, option, qp)


#########################################################
#                SUBCLASS QTABWIDGET                    #
#########################################################
class MyTabWidget(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)

        self.setTabBar(MyTabBar())

        self.tabBar().setStyleSheet(get_QTabBar_style())
        self.setStyleSheet(get_QTabWidget_style())
        self.setTabsClosable(True)



'''=========================================================='''
'''|                  CUSTOM MAIN WINDOW                    |'''
'''=========================================================='''
class CustomMainWindow(QMainWindow):

    def __init__(self):
        super(CustomMainWindow, self).__init__()

        # -------------------------------- #
        #           Window setup           #
        # -------------------------------- #

        # 1. Define the geometry of the main window
        # ------------------------------------------
        self.setGeometry(100, 100, 800, 800)
        self.setWindowTitle("Custom TabBar test")

        # 2. Create frame and layout
        # ---------------------------
        self.__frm = QFrame(self)
        self.__frm.setStyleSheet("QWidget { background-color: #efefef }")
        self.__lyt = QVBoxLayout()
        self.__frm.setLayout(self.__lyt)
        self.setCentralWidget(self.__frm)

        # 3. Insert the TabMaster
        # ------------------------
        self.__tabMaster = MyTabWidget()
        self.__lyt.addWidget(self.__tabMaster)

        # 4. Add some dummy tabs
        # -----------------------
        self.__tabMaster.insertTab(self.__tabMaster.currentIndex() + 1,QTextEdit(), "nya")
        self.__tabMaster.addTab(QFrame(), "first")
        self.__tabMaster.addTab(QFrame(), "second")
        self.__tabMaster.insertTab(self.__tabMaster.currentIndex() + 1, QTextEdit(), "nya")
        self.__tabMaster.addTab(QFrame(), "third")
        self.__tabMaster.addTab(QFrame(), "fourth")

        # 5. Show window
        # ---------------
        self.show()

    ''''''

'''=== end Class ==='''


if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    myGUI = CustomMainWindow()
    sys.exit(app.exec_())