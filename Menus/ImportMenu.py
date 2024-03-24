from PyQt5.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QGridLayout, QFrame, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PIL import Image, ImageGrab
import os
from PyQt5.QtGui import QIcon, QPixmap
from Menus.EditMenu import add_action
from PyQt5 import QtCore
from Settings.settings import g_programs_folder
from Gui.gui_classes import simple_warning
from left_zone.D3_interface import change_draft

def import_menu_opt(self):
    self.importMenu = self.menubar.addMenu('&Import')

    self.importDraftAction = QAction(QIcon('icons/open.png'), 'Draft import', self)
    add_action(self.importMenu, self.importDraftAction, 'Bring draft to the project',
               lambda: empty_draft_import(self), 'Ctrl+I')

    self.importDraftActionPrtScr = QAction(QIcon('icons/open.png'), 'Draft PrtScr import', self)
    add_action(self.importMenu, self.importDraftActionPrtScr, 'You copied image to buffer',
               lambda: print_screen_draft_import(self), 'Ctrl+P')

def empty_draft_import(self):
    print('QFileDialog.DontUseNativeDialog')
    filter_files = "Images (*.png *.xpm *.jpg *.tif *.tiff);;All files (*.*)"
    path, _ = QFileDialog.getOpenFileName(None, "Open draft", g_programs_folder, filter_files)
    if path:
        try:
            scene0 = self.centre.left.left_tab.parent_of_3d_widget.openGL
            new_image_address = 'file///' + path
            print('new_image_address = ', new_image_address)
            change_draft(scene0, new_image_address)

        except BaseException:
            simple_warning('warning', "Не могу открыть \n ¯\_(ツ)_/¯ ")


def print_screen_draft_import(self):
    path = os.getcwd() + r'\temp\buffer draft.PNG'
    try:
        im = ImageGrab.grabclipboard()
        im.save(path, 'PNG')
        scene0 = self.centre.left.left_tab.parent_of_3d_widget.openGL
        new_image_address = 'file///' + path
        change_draft(scene0, new_image_address)
        print('success print_screen_draft_import')
    except:
        print('Nothing to insert')

