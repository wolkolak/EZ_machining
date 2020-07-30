import tkinter as tk
from editor import editor
import copy

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
    if event.widget.mouse_x != 0:
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

        self.config(bg='red', width=300, height=500)
        self.rowconfigure(0, weight=1)
        self.grid(row=1, column=0, sticky='NSEW')
        self.grid_propagate(0)

        self.frame = tk.Frame(self, bg='purple')
        self.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='NSEW')

        self.dragbar = DragBar(self, bg='green', width=10)
        self.dragbar.mouse_x = 0
        self.dragbar.grid(row=0, column=1, sticky='NSW')

        #self.dragbar.bind("<Motion>", dragbar_on_motion)
        self.dragbar.bind("<Button-1>", dragbar_on_click)
        self.dragbar.bind("<ButtonRelease-1>", dragbar_on_release)


def create_frame(master, propagate, width, height, color, row, column, rowspan=None, columnspan=None, sticky='NSW' ):
    name = tk.Frame(master, width=width, height=height, bg=color)
    name.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, sticky=sticky)
    if propagate:
        name.grid_propagate(0)
        #name.pack_propagate(False)
    #name.pack(side=place, anchor=tk.NW)


    return name

menu = create_frame(root, True, width, 60, "gray", 0, 0, columnspan=2, sticky='NWE')

#gkod = create_frame(root, True, int(width/2.5), height, "yellow4", 1, 0)
#screen = create_frame(root, True, width - width/2.5, height, "green4", 1, 1)


root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
gkod = SideMenu(root)
tray = create_frame(root, True, width, 40, "red", 2, 0, columnspan=2, sticky='SWE')

tool_bar = tk.Label(gkod, bg='gray', text="блять").grid(sticky='NSEW')

editor1 = editor(gkod, 608, 900, "green", tk.LEFT)

