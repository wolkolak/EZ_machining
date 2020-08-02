from tkinter import *

root=Tk()

framic_left = Frame(root, width=100, height=100, bg='cyan')
framic_left.grid(row=0, column=0, sticky='nswe')

framic_right = Frame(root, width=100, height=100, bg='green')
framic_right.grid(row=0, column=1, sticky='nswe')


framic1 = Frame(framic_right, width=100, height=100, bg='red')
framic1.grid(row=0, column=0, sticky='nswe')

text = Text(framic_right, wrap=NONE)
vscrollbar = Scrollbar(framic_right,orient='vert', command=text.yview)
text['yscrollcommand'] = vscrollbar.set
hscrollbar = Scrollbar(framic_right, orient='hor', command=text.xview)
text['xscrollcommand'] = hscrollbar.set

# размещаем виджеты
text.grid(row=0, column=0, sticky='nsew')
vscrollbar.grid(row=0, column=1, sticky='ns')
hscrollbar.grid(row=1, column=0, sticky='ew')

# конфигурируем упаковщик, чтобы текстовый виджет расширялся
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.mainloop()