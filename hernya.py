def insertFromMimeData(self, source):
    # должен ссылаться на универсальную замену текста
    if source.hasText():
        self.corrected_qt_number_of_lines, self.untilBlock, self.firstBlock = HLSyntax.addition_help_for_qt_highlight.corrected_number_of_lines(
            self, key)

        self.base.delta_number_of_lines = source.text().count('\n') + 1
        print('paaaste: ', self.base.delta_number_of_lines)
        self.universal_replace()
        QPlainTextEdit.insertFromMimeData(self, source)
