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