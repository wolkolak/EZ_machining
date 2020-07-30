import tkinter as tk


def dragbar_on_click(event):
    event.widget.mouse_x = event.x


def dragbar_on_release(event):
    event.widget.mouse_x = 0

def dragbar_on_motion(event):
    if event.widget.mouse_x != 0:
        width = event.widget.parent.winfo_width() + event.x - event.widget.mouse_x
        event.widget.parent.config(width=width)
        x = root.winfo_width()
        y = root.winfo_height()
        root.geometry("{}x{}".format(x, y))

class DragBar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent


class SideMenu(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.config(bg='red', width=600)
        self.rowconfigure(0, weight=1)
        self.grid(sticky='NSEW')
        self.grid_propagate(0)

        self.frame = tk.Frame(self, bg='purple')
        self.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, sticky='NSEW')

        self.dragbar = DragBar(self, bg='green', width=10)
        self.dragbar.mouse_x = 0
        self.dragbar.grid(row=0, column=1, sticky='NSW')

        self.dragbar.bind("<Motion>", dragbar_on_motion)
        self.dragbar.bind("<Button-1>", dragbar_on_click)
        self.dragbar.bind("<ButtonRelease-1>", dragbar_on_release)


root = tk.Tk()
root.minsize(width=100, height=200)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

f = SideMenu(root)
tk.Label(f.frame, text='This is a test line.').grid(sticky='NW')

root.mainloop()