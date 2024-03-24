from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtGui import QIcon, QFont


def edit_opt(self):
    self.findAction = QAction(QIcon('icons/open.png'), 'Find', self) #../icons/open.png
    self.findAction.setStatusTip('find in current text')
    self.findAction.triggered.connect(self.find_obertka)
    self.findAction.setShortcut('Ctrl+F')

    self.replaceAction = QAction(QIcon('icons/open.png'), 'Replace', self) #../icons/open.png
    self.replaceAction.setStatusTip('replace in current text')
    self.replaceAction.triggered.connect(self.replace_obertka)
    self.replaceAction.setShortcut('Ctrl+H')


    self.editMenu = self.menubar.addMenu('&Edit')
    self.editMenu.addAction(self.findAction)
    self.editMenu.addAction(self.replaceAction)

    self.undoAction = QAction('Undo', self)

    #undoAction = self.centre.note.currentWidget().editor.undoStack.createUndoAction(self.centre.note.currentWidget().editor, self.tr("&Undo"))
    #undoAction.setShortcuts(QKeySequence.Undo)
    self.redoAction = QAction("Redo", self)
    self.cutAction = QAction('Cut', self)
    self.copyAction = QAction('Copy', self)
    self.select_allAction = QAction('Select all', self)
    self.delAction = QAction('Delete', self)
    self.pasteAction = QAction('Paste', self)
    self.change_iteration = QAction('Iter = ?', self)

    self.editMenu.addSeparator()
    add_action(self.editMenu, self.undoAction, 'Cancel previous change', self.undo_obertka, 'Ctrl+Z')
    add_action(self.editMenu, self.redoAction, 'Rewriting undone changes', self.redo_obertka, 'Ctrl+Y')
    self.editMenu.addSeparator()
    add_action(self.editMenu, self.cutAction, 'Cut text', self.cut_obertka, 'Ctrl+X')
    add_action(self.editMenu, self.copyAction, 'Copy text', self.copy_obertka, 'Ctrl+C')
    add_action(self.editMenu, self.pasteAction, 'Paste text', self.paste_obertka, 'Ctrl+V')
    add_action(self.editMenu, self.delAction, 'Delete text', self.del_obertka, 'Delete')
    self.editMenu.addSeparator()
    add_action(self.editMenu, self.select_allAction, 'Select all text', self.select_all_obertka, 'Ctrl+A')
    self.editMenu.addSeparator()
    add_action(self.editMenu, self.change_iteration, 'Specify time of the used line(for cycles)', self.myIter_obertka, 'Ctrl+3')
    self.change_iteration.setFont (QFont("Times", 8, QFont.Bold))

    self.menubar.hovered.connect(lambda: update_edit_menu(self, self.centre.note.currentIndex()))


def add_action(menu, nameaction, tip, my_slot, short_cut):
    nameaction.setStatusTip(tip)
    nameaction.triggered.connect(my_slot)
    nameaction.setShortcut(short_cut)
    menu.addAction(nameaction)

def update_edit_menu(self, current_index):
    if current_index == -1:
        #всё отключи
        self.editMenu.setEnabled(False)
        for action in self.editMenu.actions():
            action.setEnabled(False)
    else:
        #print('update_edit_menu')
        self.editMenu.setEnabled(True)
        edit = self.centre.note.currentWidget().editor
        self.editMenu.actions()[0].setEnabled(True)
        self.editMenu.actions()[1].setEnabled(True)
        self.editMenu.actions()[11].setEnabled(True)
        a = True if edit.undoStack.canUndo() else False
        self.editMenu.actions()[3].setEnabled(a)
        a = True if edit.undoStack.canRedo() else False
        self.editMenu.actions()[4].setEnabled(a)
        a = True if edit.textCursor().hasSelection() else False
        self.editMenu.actions()[6].setEnabled(a)
        self.editMenu.actions()[7].setEnabled(a)
        self.editMenu.actions()[9].setEnabled(a)
        a = True if QApplication.clipboard().text() else False
        self.editMenu.actions()[8].setEnabled(a)

        a = True #if edit.textCursor(). else False
        self.editMenu.actions()[13].setEnabled(a)
        #print(f'self.editMenu.actions()[14] = {self.editMenu.actions()[13]}')
        #print('Update_edit_menu')

        #self.editMenu.actions() =
        #self.centre.note.currentWidget().editor
