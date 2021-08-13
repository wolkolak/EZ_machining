from PyQt5.QtWidgets import QGridLayout, QWidget,  QProgressBar
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
import numpy as np
from Settings.settings import min_ark_step, axises
from Redactor.My_plain_text import MyEdit
from left_zone.ARK_solving import *
from Redactor.numpy_box import NumpyBox
from Redactor.G_MODAL_commands import G_MODAL_DICT

class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #self.setMaximum(100)
        #self.hide()
        self.base = base
        self.valueChanged.connect(self.finish_current_batch)

    def finish_current_batch(self, current_value):
        self.base.highlight.count_in_step = 0
        #print('progressbar finish current batch Hcount ', self.base.highlight.count)
        if current_value == self.maximum():
            #print('finish_current_batch->inserting_in_main_g_cod')
            self.base.np_box.current_g_cod_pool = self.base.highlight.current_g_cod_pool
            self.base.np_box.inserting_current_in_main_shell(self.base.editor.min_line_np)
            self.base.tab_.center_widget.left.update_visible_np_left()
            print('Load 100%')
            self.base.highlight.to_the_start()
            self.setValue(0)
        elif self.base.reading_lines_number < self.base.highlight.count + self.base.highlight.standart_step:
            #print(
            #    'Делаем шаг поменьше: number_of_lines={}, self.base.highlight.count={}, self.base.highlight.standart_step={}'
            #    .format(self.base.reading_lines_number, self.base.highlight.count, self.base.highlight.standart_step))
            self.base.highlight.standart_step = self.base.reading_lines_number - self.base.highlight.count  # - 1?
        #print('hhhhh: ', self.base.np_box.main)


    #def inserting_in_main_g_cod(self):
    #    print('how many')
    #    #print('вставить {} перед np строкой {}'.format(self.base.current_g_cod_pool, self.base.editor.min_line_np))
    #    self.base.main_g_cod_pool = np.insert(self.base.main_g_cod_pool, self.base.editor.min_line_np, self.base.current_g_cod_pool, axis=0)
    #    self.base.change_visible_array()
    #    self.base.tab_.center_widget.left.update_visible_np_left()


class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing):
        super().__init__()

        self.index_insert = 1
        self.tab_ = tab_

        #self.lastGcod = 0
        grid = QGridLayout()
        self.setLayout(grid)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)
        self.progress_bar = Progress(self)
        self.reading_lines_number = self.editor.blockCount() or 1
        self.np_box = NumpyBox(self)
        self.set_syntax()
        self.np_box.start_point()
        self.g_modal = G_MODAL_DICT()#todo здесь последнее изменение

        self.progress_bar.setMaximum(self.reading_lines_number)
        grid.addWidget(self.progress_bar, 1, 0)


        self.index_operations = 0


    def set_syntax(self):
        print('SET syntax1')
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self)
        print('SET syntax2')

    def on_count_changed(self, value):
        self.progress_bar.setValue(value)

