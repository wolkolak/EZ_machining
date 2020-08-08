import tkinter.ttk as ttks
from tkinter import LEFT, RIGHT, X, Y, BOTH


class MainUI:
    def __init__(self, master):
        self.master = master

        self.nb = ttks.Notebook(self.master)
        self.nb.pack(fill='both', expand=1)

        self.name = ttks.Entry(self.master)
        self.name.pack()
        self.save_tab = ttks.Button(self.master, text="save", command=lambda: self.save_file()).pack()
        # tab1
        self.page1 = ttks.Frame(self.nb)
        self.txt = ttks.tkinter.Text(self.page1)
        self.txt.pack(fill='both', expand=1)
        self.nb.add(self.page1, text="tab1")

        self.page2 = ttks.Frame(self.nb)
        self.nb.add(self.page2, text="tab2")
        self.master.bind('', self.add_tabs)

    def add_tabs(self, event):
        self.page_name = ttks.Frame(self.nb)
        self.tx = ttks.tkinter.Text(self.page_name)
        self.tx.pack(fill=BOTH, expand=1)
        self.nb.add(self.page_name, text="pagename")

    def save_file(self):
        self.fname = self.name.get()
        self.txtinput = self.tx.get("1.0", "end-1c")
        with open(self.fname, 'w') as f:
            f.write(self.txtinput)


if True:
    root = ttks.tkinter.Tk()
    root.title('Tabs>>')
    root.geometry('500x500')
    MainUI(root)
root.mainloop()