from Gui import gui_classes
import re
import codecs
import fileinput
import os
from Gui.little_gui_classes import simple_warning


#def rewrite_file(address:str, names:list, split='=', comment=''):
#    """Принимает список вида [[name1, value1]...]
#    Полностью переписывает файл"""
#    with codecs.open(address, 'r', 'utf-8') as f:
#        replacement = ""
#        for line in f:




def printLog(*args, **kwargs):
    print(*args, **kwargs)
    with open('output.out','a') as file:
        print(*args, **kwargs, file=file)


def change_file_vars(address:str, names:list, split='='):

    print('change_file_vars:')
    print('names = ', names)
    """Принимает список вида [[name1, value1]...]
    Нереписывает файл не требуя всех переменных"""
    #try: #todo return try
    #address = r'D:\Users\72014\Desktop\EZ_machining-master\Modelling_clay\machines\NT6000_Table_C_Head_BA\machine_settings.py'
    #address = address.replace('.', '\\')

    #Тут починить тоже.
    with open(address, 'r', encoding='utf8') as settings:
        #printLog('settings: ', settings.)
        replacement = ""
        for line in settings:
            #printLog('line = ', line)
            equal = False
            for i in names:
                word = re.escape(i[0]) + "\s*" + split
                if re.match(word, line):
                    replacement = replacement + '{}{}{}\r'.format(i[0], split, i[1])#\n
                    equal = True
                    break
            if equal == False:
                replacement = replacement + line
    settings.close()
    print('Length = ', len(replacement))
    print('В файл уходит: \n', str(replacement))
    with open(address, 'w', encoding='utf8') as settings:#, encoding='utf8'
        settings.write(replacement)
        settings.close()



def change_any_file_completly(address, names, split='='):
    """Принимает список вида [[name1, value1]...]
    Полностью переписывает файл Settings.py"""
    #try: #todo return try
    replacement = ''
    for line in names:
        replacement = replacement + line[0] + split + line[1] + '\n'
    with codecs.open(address, 'w', 'utf-8') as settings:
        settings.write(replacement)
        settings.close()
    #except OSError:
    #    gui_classes.simple_warning('Ooh', 'Something 1went wrong \n ¯\_(ツ)_/¯')