from tkinter import *
import tkinter.ttk as ttk

root = Tk()
root.title('test')
#root.grid_propagate(0)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=0)
nb = ttk.Notebook(root)
nb.grid(row=0, column=0, sticky="we", columnspan=1)


f1 = Text(root)
f2 = Text(root)
f3 = Text(root)

nb.add(f1, text='page1')
nb.add(f2, text='page2')
nb.add(f3, text='page3')

root.mainloop()