from PyQt5.QtWidgets import QUndoStack, QUndoCommand


class MyStack(QUndoStack):
    def __init__(self, edit, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.edit = edit
        self.last_edited = ''
        self.sutulaya_sobaka = False
        self.line_max_np_del = 0
        self.line_max_np_insert = 0
        # self.edit_type = something
        self.previous_max_line = 0
        self.add_undo = 0
        self.add_redo = 0
        self.edit_type = False

    def storeFieldText(self):
        if self.edit_type == False:
            print('999 self.edit_type == False')
            return
        print('999 self.edit_type = ', self.edit_type)
        command = StoreCommand(self)
        self.edit_type = False
        print('before push')
        self.push(command)
        print('after push')
        #self.
        #print('command.field = ', command.text())

    def merging_word(self):

        #print('merge')
        while self.index() > 1 and (self.command(self.index() - 2).id != -1):
            #print('self.index() ==== ', self.index())
            g = self.command(self.index() - 2).mergeWith(self.command(self.index() - 1))
            self.sutulaya_sobaka = True
            self.undo()  # silent undo
            self.sutulaya_sobaka = False

class StoreCommand(QUndoCommand):

    def __init__(self, stack):
        QUndoCommand.__init__(self)
        self.stack = stack
        # Record the field that has changed.
        self.field = self.stack.edit
        self.store_cursor = self.field.textCursor()
        self.text_inserted = self.stack.last_edited
        self.setText(self.stack.edit_type)
        print('self.stack.edit_type = ', self.stack.edit_type)
        self.add_undo = self.stack.add_undo
        self.add_redo = self.stack.add_redo
        self.id = -1
        self.child_count = 0
        #self.corrected_qt_number_of_lines = self.field.corrected_qt_number_of_lines
        # todo self.text перевести на self.id
        print('new command')
        text12345 = self.text()

        if text12345 == 'symbol' or text12345 == 'space':  # остальные символы
            if text12345 == 'symbol':
                self.id = 1
            self.give_position()
            self.pos3 = self.pos1 + 1

        elif text12345 == 'enter':
            self.give_position()
            self.pos3 = self.pos1 + 1

        elif text12345 == 'backspace':
            self.text_inserted = ''
            #if not self.store_cursor.hasSelection():#no longer need it. i was forsed to not use default event ending
            #    self.store_cursor.setPosition(self.store_cursor.position() - 1, 1)
            self.give_position()
            self.pos3 = self.pos1
        elif text12345 == 'delete':
            self.text_inserted = ''
            #if not self.store_cursor.hasSelection():#the same as backspace. i'll move cursor in event
            #    self.store_cursor.setPosition(self.store_cursor.position() + 1, 1)
            self.give_position()
            self.pos3 = self.pos1
        elif text12345 == 'cut':
            # self.text_inserted = ''
            self.give_position()
            self.pos3 = self.pos1
        elif text12345 == 'insert':
            self.give_position()
            self.pos3 = self.pos1 + len(self.text_inserted)
        elif text12345 == 'replace':
            self.give_position()
            self.pos3 = self.pos1 + len(self.text_inserted)
        elif text12345 == 'glue':
            print('emaaaa')
            #self.command_created_only = True
            #print('self.childCount() = ', self.childCount())
            return

        self.command_created_only = True
        #self.give_line_numbers()

        #print('                    self.pos1 = {}, self.pos2 = {}'.format(self.pos1, self.pos2))
        self.text_deleted = self.store_cursor.selectedText()
        #print('                    selectedText', self.text_deleted)
        #print('                    last_edited', self.text_inserted)

    def give_position(self):
        #self.corrected_qt_number_of_lines = 1#получить с верхнего этажа
        pos1 = self.store_cursor.position()
        pos2 = self.store_cursor.anchor()
        self.pos1 = min(pos1, pos2)
        self.pos2 = max(pos1, pos2)
        print('give_position')
        print('self.pos1 = ', self.pos1)
        print('self.pos2 = ', self.pos2)

    def mergeWith(self, other: 'QUndoCommand') -> bool:
        #print('{} mergeWith {}'.format(self.text_inserted, other.text_inserted))
        self.text_inserted = self.text_inserted + other.text_inserted
        self.pos3 = other.pos3
        #print('self.pos3 = ', self.pos3)
        # other.setObsolete(True)
        return True

    def undo(self):
        print('undo start')
        #2/0
        self.command_created_only = False
        if self.stack.sutulaya_sobaka is True:
            print('pseudo undo')
        else:
            #u dont need to play around macroUndo cuz it nether dive here
            #print(
            #    'undo text_inserted: {}, готов записать в команду № {}'.format(self.text_inserted, self.stack.index()))
            self.stack.edit_type = 'undo'
            self.store_cursor.setPosition(self.pos3, 0)  #don't worry, selection happened
            self.store_cursor.setPosition(self.pos1, 1)
            #print(f'cursor postion = {self.store_cursor.position()}, anchor = {self.store_cursor.anchor()}')
            self.stack.previous_max_line = self.field._document.findBlock(self.pos3).blockNumber()#+1
            self.store_cursor.insertText(self.text_deleted)#после onchange НАЧИНАЕТСЯ HighLight
            #self.stack.edit.min_line_np = self.stack.edit.textCursor().blockNumber()
            #self.stack.edit.second_place = self.stack.edit.textCursor().blockNumber()
            #print('index undostack: ', self.stack.index())
            print('undo end')


    def redo(self):
        print('redo: {}, готов записать в команду № {}'.format(self.text(), self.stack.index()))
        #return
        if self.command_created_only is False:
            #print('command_created_only is False')
            self.stack.edit_type = 'redo'
            self.store_cursor.setPosition(self.pos1, 0)
            self.store_cursor.setPosition(self.pos2, 1)
            self.stack.previous_max_line = self.field._document.findBlock(self.pos2).blockNumber()#-1
            #TODO -1????????????????????????? added for isert in first line
            #print('redo max = ', self.stack.edit.base.progress_bar.maximum())
            self.store_cursor.insertText(self.text_inserted)
            #МОЖЕТ сюда внести рехайлайт и его правила
            #self.store_cursor.p
            #self.stack.edit.min_line_np = self.stack.edit.textCursor().blockNumber()
            #self.stack.edit.second_place = self.stack.edit.textCursor().blockNumber()
            #self.stack.edit.second_place = self.stack.edit.textCursor().blockNumber()#????????????????
            #может обновить точку курсора?
