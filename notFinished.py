class coloredTabBar(QTabBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.colorIndexes = {
            1: QColor(Qt.red),
            3: QColor(Qt.blue),
            }
    #Первый раз работаю с перерисовкой. Нифига не понимаю, но заработало
    def paintEvent(self, event):
        qp = QPainter(self)
        qp.setRenderHints(qp.Antialiasing)
        option = QStyleOptionTab()
        option.features |= option.HasFrame
        palette = option.palette
        for index in range(self.count()):
            self.initStyleOption(option, index)
            #palette.setColor(palette.Button, self.colorIndexes.get(index, QColor(Qt.green)))
            if self.window().centre.note.widget(index).existing is True:
                palette.setColor(palette.Window, QColor.fromRgb(195, 221, 234)) #color4
            else:
                palette.setColor(palette.Window, QColor(Qt.lightGray))

            option.palette = palette
            self.style().drawControl(QStyle.CE_TabBarTab, option, qp)
            #qp.save()

#main.py
QApplication.setStyle(QStyleFactory.create('windows'))

connect(lambda: self.restore_options('interface_settings', 'default_interface_settings'))
def restore_some_options(self, name, defaultname):
    """
    :param name: string
    :param defaultname: string
    :return: change value of the 'name' to the value of 'defaultname'
    """
    x = None
    y = None
    name = name + ' '
    defaultname = defaultname + ' '

    with open('settings.py') as settings:
        for index, line in enumerate(settings):
            if re.match(name, line):
                x, cur_line = index, line
            if re.match(defaultname, line):
                y, def_line = index, line
            if x and y:
                print('x=', x, 'y=', y)
                break
    try:
        with fileinput.FileInput('settings.py', inplace=True, backup='.bak') as settings:
            for index, line in enumerate(settings):
                if index != x:
                    print(line, end='')
                else:
                    print(name + def_line[len(defaultname):])
        os.unlink('settings.py' + '.bak')
    except OSError:
        gui_classes.simple_warning('Ooh', 'Something went wrong \n ¯\_(ツ)_/¯')
    self.setGeometry(100, 100, interface_settings['main_width'], interface_settings['main_height'])