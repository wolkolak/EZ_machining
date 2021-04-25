def insertFromMimeData(self, source):
    # должен ссылаться на универсальную замену текста
    if source.hasText():
        self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
            self, key)

        self.base.delta_number_of_lines = source.text().count('\n') + 1
        print('paaaste: ', self.base.delta_number_of_lines)
        self.universal_replace()
        QPlainTextEdit.insertFromMimeData(self, source)
################################
        if event == QKeySequence.Undo:

            if self.make_undo_work_1_time == 0:
                print('QKeySequence.Undo для однократного исполнения')
                # self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock, self.blocks_before = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
                #    self, key='Undo')
                self.make_undo_work_1_time = 1
            elif self.make_undo_work_1_time == 2:
                self.make_undo_work_1_time = 0