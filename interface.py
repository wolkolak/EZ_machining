import tkinter as tk
from editor import editor
import tkinter.ttk as ttk

#main window
root = tk.Tk()
width = 1450
height = 900
root.minsize(width=width, height=height)
root.title("EZ machining")


def dragbar_on_click(event):
    event.widget.mouse_x = event.x
    root.config(cursor="tcross")

def dragbar_on_release(event):
    width = event.widget.parent.winfo_width() + event.x - event.widget.mouse_x
    if width < 10:
        width = 10
    if width > root.winfo_width() - 10:
        width = root.winfo_width()
    event.widget.parent.config(width=width)
    event.widget.mouse_x = 0
    x = root.winfo_width()
    y = root.winfo_height()
    root.geometry("{}x{}".format(x, y))
    root.config(cursor="")

class DragBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

class SideMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg='blue', width=700, height=400)
        self.rowconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky='NEWS')
        self.grid_propagate(0)

        self.frame = tk.Frame(self, bg='purple', width=200, height=200)
        self.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='NSEW')
        self.dragbar = DragBar(self, bg='orange', width=10)
        self.dragbar.mouse_x = 0
        self.dragbar.grid(row=0, column=1, sticky='NSW')

        self.dragbar.bind("<Button-1>", dragbar_on_click)
        self.dragbar.bind("<ButtonRelease-1>", dragbar_on_release)


def create_frame(master, propagate, width, height, color, row, column, rowspan=None, columnspan=None, sticky='NSWE'):
    name = tk.Frame(master, width=width, height=height, bg=color)#
    name.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
    name.grid_propagate(propagate)
    return name

menu = create_frame(root, False, width, 60, "gray", 0, 0, columnspan=2, sticky='NWE')


gkod = create_frame(root, True, width - width/2.5, height, "green4", 1, 1, sticky='NSWE')



root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)

gkod.columnconfigure(0, weight=1)
gkod.rowconfigure(0, weight=1)

screen = SideMenu(root)
screen.frame.columnconfigure(0, weight=1)
screen.frame.rowconfigure(0, weight=1)

tray = create_frame(root, False, width, 40, "gray", 2, 0, columnspan=2, sticky='SWE')


"""nb = ttk.Notebook(gkod)
nb.grid(row=0, column=0, sticky="nswe", columnspan=1)
f1 = tk.Text(gkod)
f2 = tk.Text(gkod)
nb.add(f1, text='page1')
nb.add(f2, text='page2')"""
editor1 = editor(gkod, 508, 800, "cyan")

editor2 = editor(screen.frame, 508, 800, "cyan")

