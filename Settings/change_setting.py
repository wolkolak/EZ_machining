from Gui import gui_classes
import re
import fileinput
import os

def change_settins(names):
    """Принимает список вида [[name1, value1]...]
    Полностью переписывает файл Settings.py"""
    try:
        with fileinput.FileInput('Settings\settings.py', inplace=True, backup='.bak') as settings:
            for line in settings:
                for i in names:
                    if re.match(i[0], line):
                        print('{}={}'.format(i[0], i[1]))
                        break
                else:
                    print(line, end='')
        os.unlink('Settings\settings.py' + '.bak')
    except OSError:
        gui_classes.simple_warning('Ooh', 'Something 1went wrong \n ¯\_(ツ)_/¯')