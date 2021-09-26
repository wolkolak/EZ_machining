from PyQt5.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from Menus.EditMenu import add_action
from PyQt5 import QtCore
from Settings.settings import draft_page_format, g_programs_folder
from Gui.gui_classes import simple_warning
from left_zone.D3_interface import change_draft


def import_menu_opt(self):
    self.importMenu = self.menubar.addMenu('&Import')

    self.importDraftAction = QAction(QIcon('icons/open.png'), 'Draft import', self)
    add_action(self.importMenu, self.importDraftAction, 'Bring draft to the project',
               lambda: empty_draft_import(self), 'Ctrl+I')


def empty_draft_import(self):
    #print('import draft')
    #self.draft_prop = import_draft_dialog(self).show()
    print('QFileDialog.DontUseNativeDialog')
    filter_files = "Images (*.png *.xpm *.jpg *.tif *.tiff);;All files (*.*)"
    path, _ = QFileDialog.getOpenFileName(None, "Open draft", g_programs_folder, filter_files)
    if path:
        #self.make_open_DRY(path)
        try:
            #text = open(path).read()
            #self.centre.note.currentIndex()
            scene0 = self.centre.left.left_tab.b.openGL
            new_image_address = 'file///' + path
            print('new_image_address = ', new_image_address)
            change_draft(scene0, new_image_address)

            #self.insertTab(self.currentIndex() + 1, redactor.ParentOfMyEdit(text, existing=path, tab_=self),
            #               name_open_file)

        except BaseException:
            simple_warning('warning', "Не могу откр \n ¯\_(ツ)_/¯ ")




