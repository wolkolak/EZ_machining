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

    def storeFieldText(self):
        if self.edit_type == False:
            return
        command = StoreCommand(self)
        self.edit_type = False
        self.push(command)
        print('command.field = ', command.text())

    def merging_world(self):

        print('merge')
        while self.index() > 1 and (self.command(self.index() - 2).id != -1):
            print('self.index() ==== ', self.index())
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
        self.add_undo = self.stack.add_undo
        self.add_redo = self.stack.add_redo
        self.id = -1
        self.child_count = 0
        #self.corrected_qt_number_of_lines = self.field.corrected_qt_number_of_lines
        # todo self.text перевести на self.id
        print('new command')
        text12345 = self.text()

        if text12345 == 'symbol' or text12345 == 'enter' or text12345 == 'space':  # остальные символы
            if text12345 == 'symbol':
                self.id = 1
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
            print('self.childCount() = ', self.childCount())
            return

        self.command_created_only = True
        #self.give_line_numbers()

        print('                    self.pos1 = {}, self.pos2 = {}'.format(self.pos1, self.pos2))
        self.text_deleted = self.store_cursor.selectedText()
        print('                    selectedText', self.text_deleted)

        print('                    last_edited', self.text_inserted)

    def give_position(self):
        #self.corrected_qt_number_of_lines = 1#получить с верхнего этажа
        pos1 = self.store_cursor.position()
        pos2 = self.store_cursor.anchor()
        self.pos1 = min(pos1, pos2)
        self.pos2 = max(pos1, pos2)


    def mergeWith(self, other: 'QUndoCommand') -> bool:
        print('{} mergeWith {}'.format(self.text_inserted, other.text_inserted))
        self.text_inserted = self.text_inserted + other.text_inserted
        self.pos3 = other.pos3
        print('self.pos3 = ', self.pos3)
        # other.setObsolete(True)
        return True

    def undo(self):
        self.command_created_only = False
        if self.stack.sutulaya_sobaka is True:
            print('pseudo undo')
        else:
            #u dont need to play around macroUndo cuz it nether dive here
            print(
                'undo text_inserted: {}, готов записать в команду № {}'.format(self.text_inserted, self.stack.index()))
            self.stack.edit_type = 'undo'
            self.store_cursor.setPosition(self.pos3, 0)  #
            self.store_cursor.setPosition(self.pos1, 1)#pos3
            self.stack.previous_max_line = self.field._document.findBlock(self.pos3).blockNumber()
            self.store_cursor.insertText(self.text_deleted)#после onchange НАЧИНАЕТСЯ HighLight
            print('index undostack: ', self.stack.index())
            print('check')

    def redo(self):
        print('redo: {}, готов записать в команду № {}'.format(self.text(), self.stack.index()))
        if self.command_created_only is False:
            self.stack.edit_type = 'redo'
            self.store_cursor.setPosition(self.pos1, 0)
            self.store_cursor.setPosition(self.pos2, 1)
            self.stack.previous_max_line = self.field._document.findBlock(self.pos2).blockNumber()
            self.store_cursor.insertText(self.text_inserted)