from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title('test')
#root.grid_propagate(0)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
nb = ttk.Notebook(root)
nb.grid(row=0, column=0, sticky="we", columnspan=1)







f1 = Text(root, wrap=NONE)
f2 = Text(root)
f3 = Text(root)

nb.add(f1, text='page1')
nb.add(f2, text='page2')
nb.add(f3, text='page3')

tabName = nb.select()
pointer = nb.nametowidget(tabName)

scrolly = Scrollbar(root, command=pointer.yview, orient=VERTICAL)
scrollx = Scrollbar(root, command=pointer.xview, orient=HORIZONTAL)
pointer.config(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
scrollx.grid(row=1, column=0, sticky="WE", columnspan=1)
scrolly.grid(row=0, column=1, sticky="NS", rowspan=1)

l1 = Button(text=nb.select(), font="Arial 32")
def printi():
    #print(nb.select())
    l1['text'] = nb.select()
    #nb.select(2)
l1.config(command=printi)
l1.grid(row=1, column=0, sticky="NSWE", rowspan=1)
root.mainloop()