from PyQt5.QtWidgets import QGridLayout, QWidget,  QProgressBar, QPushButton, QDialog, QPlainTextEdit
import HLSyntax.HL_Syntax, HLSyntax.addition_help_for_qt_highlight
from Redactor.My_plain_text import MyEdit
from Core.Data_solving.numpy_box import NumpyBox
from PyQt5.QtCore import Qt
from Settings.settings import MaxFileLen
#from Redactor.G_MODAL_commands import G_MODAL_DICT
import importlib
import inspect
import Modelling_clay
import sys
import time

class Progress(QProgressBar):
    def __init__(self, base):
        super().__init__()
        #print('QProgressBar init')
        self.start_time = time.time()
        print('self.start_time = ', self.start_time)
        self.base = base
        self.first_time = True
        self.valueChanged.connect(self.finish_current_batch)
        #self.blockSignals(False)
        #self.base.choose_Logs_or_progress_show(False)

    def finish_current_batch(self, current_value):#Не ломает после смены процессора?
        print('XXX finish_current_batch, step = ', self.base.highlight.count_in_step)
        print('current_value = ', current_value)
        #logs = self.base.Logs
        #self.show()
        #logs.hide()
        self.base.highlight.count_in_step = 0
        #if current_value+1 == self.maximum():
        #    self.base.tab_.center_widget.left.left_tab.a.setStyleSheet('background-color:red')
        #else:
        #    self.base.tab_.center_widget.left.left_tab.a.setStyleSheet('background-color:green')
        print(f'current_value = {current_value}, self.maximum() = {self.maximum()}')
        if current_value == self.maximum():
            print(' current_value == self.maximum() = ', current_value)
            if self.base.father_np_box is not None:
                self.base.subNstart = self.base.tab_.currentWidget().subNstart
                self.base.tab_.currentWidget().subNstart = self.base.tab_.currentWidget().subNstart + len(self.base.np_box.main_g_cod_pool) #+ 10
                #self.base.tab_.currentWidget().subNstart = subNstart

            self.base.np_box.current_g_cod_pool = self.base.highlight.current_g_cod_pool  # todo есть ли в этом смысл???? Должен быть!
            #print(f' 9898 self.base.np_box.current_g_cod_pool = {self.base.np_box.current_g_cod_pool}')
            self.base.np_box.inserting_current_in_main(self.base.editor.min_line_np)
            #print(f'9898 self.base.np_box.main_g_cod_pool = {self.base.np_box.main_g_cod_pool}')
            self.base.tab_.center_widget.left.update_visible_np_left()
            self.blockSignals(True)
            self.base.highlight.to_the_start()#setValue(1)
            print('здесь проверка')

            ooo = self.base.editor.undoStack


            ooo = ooo.text(ooo.count()-1)
            print('ooo = ', ooo)
            #time.sleep(0.02)

            self.base.editor.setExtraSelections({})
            #todo то что ниже исправит всё кроме первого действия по соединению строк
            #if self.first_time or ooo == 'enter' or ooo == 'insert' or ooo == 'delete':
            #    #print('sleep 0.02')
            #    self.base.editor.setExtraSelections({})
                #time.sleep(0.02)#QProgressBar need time to recieve  new setValue
            #print('1setValue(0)')
            self.setValue(0)
            #print('669')
            self.blockSignals(False)
            print('changed or not = ', self.base.editor.changed)
            if not self.base.editor.changed and self.first_time is True:
                #self.base.editor.setExtraSelections({})
                print('FOOOOOO: ', self.first_time)
                self.first_time = False
                #logs.math_logs = ''
                self.base.np_box.special_options_applying()
                self.base.tab_.center_widget.left.update_visible_np_left()
                print("--- %s seconds ---" % (time.time() - self.start_time))
                #self.base.editor.after_solving = False#todo щсторожно, я это добавил пытаясь уййти от бага при delete на конце строки первым действием



        elif self.base.reading_lines_number < self.base.highlight.count + self.base.highlight.standart_step:
            print('finosh 44')
            self.base.highlight.standart_step = self.base.reading_lines_number - self.base.highlight.count  # - 1?
        else:
            if self.base.highlight.standart_step > 10:
                print('else happened')
                self.base.choose_Logs_or_progress_show(False)
        #print('finish_current_batch END:')
        print(self.base.np_box.main_g_cod_pool)
        if current_value == 0:
            print('stop')

        print('finish_current_batch, END')

    def setValue(self, value: int) -> None:
        print(f'fucking setValue happened, value = {value}, max = {self.maximum()}__________________________')
        QProgressBar.setValue(self, value)
        print('it ended_____________________________________________________________________________________')

class ShowLogsClass(QDialog):
    def __init__(self, father, text2, *args, **kwargs):#text1,
        super().__init__(father, *args, **kwargs)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('Logs:')
        self.setStyleSheet("background-color : gray")
        grid = QGridLayout()
        self.setLayout(grid)
        self.setFixedSize(550, 450)
        prev_text = ['Problems:\n', 'in text:\n', '\nin math:\n']
        #t1 = prev_text[1] + text1 if text1 != '\n' else text1
        #t1 = prev_text[1] + [f'{str(a)} line error\n' for a in text1] if len(text1) != 0 else '\n'
        t2 = prev_text[2] + text2 if text2 != '\n' else '...Nope! No problems found'
        self.log_plain = QPlainTextEdit(prev_text[0] + t2)
        self.log_plain.setStyleSheet('font-size: 20px; color: gray; background-color: white;')

        self.log_plain.setReadOnly(True)
        grid.addWidget(self.log_plain, 0, 0)

class LogButton(QPushButton):
    def __init__(self, father):
        super().__init__(father)
        self.setText('Logs')
        self.setStyleSheet("background-color : gray")
        self.redactor = father
        self.math_logs = '\n'
        self.clicked.connect(self.showLogs)

    def LogsAlarm(self):
        if self.math_logs != '\n':
            self.setStyleSheet("background-color : pink")
        else:
            self.setStyleSheet("background-color : gray")

    def showLogs(self):
        print(self.math_logs)#self.text_logs +
        ShowLogsClass(self, self.math_logs).show()



class ParentOfMyEdit(QWidget):
    def __init__(self, text, tab_, existing, father_np_box=None):
        super().__init__()

        self.index_insert = 1
        self.tab_ = tab_
        grid = QGridLayout()
        self.father_np_box = father_np_box
        self.sub1 = True if father_np_box is not None else False
        self.all_subs_count = 0
        self.subNstart = MaxFileLen
        self.setLayout(grid)
        self.Logs = LogButton(self)
        self.progress_bar = Progress(self)
        self.editor = MyEdit(text, existing=existing, tab_=self.tab_, base=self)
        grid.addWidget(self.editor, 0, 0)
        #СЮДА ЕЩё
        self.refresh_reading_reading_lines_number()
        #print('set_machine_in_DOC from redactor')
        self.tab_.set_machine_in_DOC(self)
        self.set_syntax()
        self.after_set_syntax()
        print('тут проверямсс 98: ', self.np_box.main_g_cod_pool)
        #brackets
        self.progress_bar.setMaximum(self.reading_lines_number)

        grid.addWidget(self.progress_bar, 1, 0)
        grid.addWidget(self.Logs, 1, 0)
        self.choose_Logs_or_progress_show(True)
        #self.progress_bar.hide()


    def choose_Logs_or_progress_show(self, logs_s:bool):
        """
        :param logs_s: True - Logs, False - progress
        """
        if logs_s:
            self.progress_bar.hide()
            self.Logs.show()
        else:
            self.progress_bar.show()
            self.Logs.hide()


    def after_set_syntax(self):
        #print('after_set_syntax ||||1')
        self.refresh_reading_reading_lines_number()
        self.np_box.__init__(self) #todo нах
        self.editor.creating_np_pool()
        self.editor.arithmetic_ones()
        self.np_box.offset_point()
        self.tab_.center_widget.app.st_bar.set_permanent_part()
        #self.g_modal = G_MODAL_DICT(self)  # todo здесь последнее изменение ЭТО НА ПОМОЙКУ в numpy_box пусть лежит
        #ПОсле этого начинаются хайлайты

    def refresh_reading_reading_lines_number(self):
        self.reading_lines_number = self.editor.blockCount() or 1



    def set_syntax(self, adress=None):#, l = None
        print('set_syntax = ')
        if adress is None:
            adress = self.tab_.default_processor_address
        #if adress == 'Modelling_clay.Processors.PseudoSimens_NT.py':
        #    f = 5 / 0
        #print('SET syntax1')
        if adress.endswith('.py'):
            adress = adress[:-3]
        str0 = adress.replace('/', '.')
        if str0[0] == '.':
            str0 = str0[1:]
        module = importlib.import_module(str0)
        is_class_member = lambda member: inspect.isclass(member) and member.__module__ == module.__name__
        clsmembers = inspect.getmembers(sys.modules[module.__name__], is_class_member)  # todo WTF? but it works just fine
        proc_class = None
        for i in clsmembers:
            if issubclass(i[1], Modelling_clay.Processors.Processor_base.ReversPostProcessor_0.ReversalPostProcessor0):
                proc_class = i[1]
        if proc_class is None:
            return False
        if hasattr(self, 'highlight'):
            #self.base.editor.setExtraSelections({})
            #self.highlight.setExtraSelections({})
            self.highlight.setDocument(None)
        self.highlight = HLSyntax.HL_Syntax.GMHighlighter(self.editor._document, base=self, proc_class=proc_class)
        self.current_processor_address = adress
        self.np_box = NumpyBox(self)
        print('a zdes 999 = ', self.np_box.main_g_cod_pool)
        self.highlight.SHIFTcontainer = self.np_box.SHIFTcontainer
        #print('SET syntax2')


        return True




    def on_count_changed(self, value):
        #print('on_count_changed value {} / {}'.format(value, self.progress_bar.maximum()))
        print('on_count_changed = ', value)
        #self.progress_bar.blockSignals(True)
        self.progress_bar.setValue(value)
        #self.progress_bar.blockSignals(False)
        #self.editor.highlightCurrentLine_chooseNewDot()

        print('on_count_changed ended')

