from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QToolBar, QTableWidget, QComboBox, QTableWidgetItem, QTreeWidget, QTreeWidgetItem

my_data = 'my custom data'

# QComboBox
combo_box = QComboBox()
combo_box.addItem( 'description', my_data ) # set description, set data
print (combo_box.currentText()) # get description
print (combo_box.itemData( combo_box.currentIndex() )) # get data


# QTableWidget
table_widget = QTableWidget()
table_widget.setRowCount(1) # add one row
item = QTableWidgetItem()
item.setText( 'description') # set description
item.setData( QtCore.Qt.UserRole, my_data ) # set data
table_widget.setItem( 0, 0, item ) # add item to table on row 0, colum 0
current_row = table_widget.currentRow() # selected row
item = table_widget.item( 0, 0 )
print (item.text() )# get description
print (item.data( QtCore.Qt.UserRole )) # get data

# QTreeWidget
tree_widget = QTreeWidget()
item = QTreeWidgetItem( tree_widget, ['description'] ) # set description
item.setData(1, QtCore.Qt.EditRole, my_data) # set data
item.setData(2, QtCore.Qt.EditRole, my_data) # set data
item.setData(3, QtCore.Qt.EditRole, my_data) # set data
print (item.text(0)) # get description
print (item.text(1)) # get data
print (item.text(2)) # get data
print (item.text(3)) # get data