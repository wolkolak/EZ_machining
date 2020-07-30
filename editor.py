import tkinter as tk



class editor:
    def __init__(self, master, w, h, color, p=tk.LEFT):
        self.mainframe = tk.Frame(master, width=w, height=h, bg=color)
        self.mainframe.pack_propagate(False)
        self.text = tk.Text(self.mainframe, width=67, height=60, bg="darkgreen", fg='white', wrap=tk.NONE)
        self.scrolly = tk.Scrollbar(self.mainframe, command=self.text.yview, orient=tk.VERTICAL)
        self.scrollx = tk.Scrollbar(self.mainframe, command=self.text.xview, orient=tk.HORIZONTAL)
        self.text.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)


        self.mainframe.pack(side=p, anchor=tk.NW)
        self.scrollx.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.LEFT, anchor=tk.NW)
        self.scrolly.pack(side=tk.LEFT, fill=tk.Y)




print("editor working")

class Block:
    def __init__(self, master):
        self.e = tk.Entry(master, width=40)
        self.b = tk.Button(master, text="Преобразовать")
        self.l = tk.Label(master, bg='black', fg='white', width=40)
        self.b['command'] = self.strToSortlist
        self.e.pack(side=tk.LEFT)
        self.b.pack(side=tk.TOP)
        self.l.pack(side=tk.TOP)

    def strToSortlist(self):
        s = self.e.get()
        s = s.split()
        s.sort()
        self.l['text'] = ' '.join(s)