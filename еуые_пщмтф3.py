from tkinter import *


def insertText():
    s = "Hello World"
    text.insert(1.0, s)


def getText():
    s = text.get(1.0, END)
    label['text'] = s


def deleteText():
    text.delete(1.0, END)


root = Tk()

text = Text(width=25, height=5)
text.pack()

frame = Frame()
frame.pack()

b_insert = Button(frame, text="Вставить", command=insertText)
b_insert.pack(side=LEFT)

b_get = Button(frame, text="Взять", command=getText)
b_get.pack(side=LEFT)

b_delete = Button(frame, text="Удалить", command=deleteText)
b_delete.pack(side=LEFT)

label = Label()
label.pack()

root.mainloop()