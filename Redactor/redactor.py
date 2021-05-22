from PyQt5.QtWidgets import QGridLayout, QWidget,  QProgressBar
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
from Redactor.My_plain_text import MyEdit

class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()
        self.base = base
        self.valueChanged.connect(self.finish_current_batch)


    def finish_current_batch(self, current_value):
        self.base.highlight.count_in_step = 0
        print('progressbar finish current batch Hcount ', self.base.highlight.count)

        if current_value == self.maximum():
            self.inserting_in_main_g_cod()
            print('Load 100%')
            self.base.reading_lines_number = 1

            self.base.current_g_cod_pool = np.zeros((self.base.reading_lines_number, 7), float)
            self.base.current_g_cod_pool[:] = np.nan
            self.base.highlight.to_the_start()
            print('specially here count', self.base.highlight.count)
            self.setValue(0)

        elif self.base.reading_lines_number < self.base.highlight.count + self.base.highlight.standart_step:
                print('Делаем шаг поменьше: number_of_lines={}, self.base.highlight.count={}, self.base.highlight.standart_step={}'
                      .format(self.base.reading_lines_number, self.base.highlight.count, self.base.highlight.standart_step))
                self.base.highlight.standart_step = self.base.reading_lines_number - self.base.highlight.count# - 1?


    def inserting_in_main_g_cod(self):

        print('вставить {} перед строкой {}'.format(self.base.current_g_cod_pool, self.base.editor.min_line_np))
        self.base.main_g_cod_pool = np.insert(self.base.main_g_cod_pool, self.base.editor.min_line_np, self.base.current_g_cod_pool, axis=0)
        self.base.tab_.center_widget.left.left_tab.a.reset_np_array_in_left_field()


class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing):
        super().__init__()

        self.index_insert = 1
        self.tab_ = tab_

        grid = QGridLayout()
        self.setLayout(grid)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)

        self.progress_bar = Progress(self)

        self.reading_lines_number = self.editor.blockCount() or 1

        self.current_g_cod_pool = np.zeros((self.reading_lines_number, 7), float)
        self.current_g_cod_pool[:] = np.nan
        print('START: Создан массив размером ', self.current_g_cod_pool.shape)
        self.main_g_cod_pool = np.zeros((1, 7), float)
        self.main_g_cod_pool[:] = np.nan
        self.progress_bar.setMaximum(self.reading_lines_number)
        grid.addWidget(self.progress_bar, 1, 0)
        self.set_syntax()

    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)


