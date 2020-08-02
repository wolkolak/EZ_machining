import tkinter as tk



class editor:
    def __init__(self, master, w, h, color):
        self.mainframe = tk.Frame(master,  bg=color)#width=w, height=h,
        self.mainframe.grid_propagate(1)
        self.text = tk.Text(self.mainframe,  bg="darkgreen", fg='white', wrap=tk.NONE, width=20,)# height=30,
        self.scrolly = tk.Scrollbar(self.mainframe, command=self.text.yview, orient=tk.VERTICAL)
        self.scrollx = tk.Scrollbar(self.mainframe, command=self.text.xview, orient=tk.HORIZONTAL)
        #self.text.config(yscrollcommand=self.scrolly.set, )
        self.text.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        self.mainframe.grid(row=0, column=0, sticky='NSWE')
        self.text.grid(row=0, column=0, rowspan=1, sticky="NSWE")
        self.scrollx.grid(row=1, column=0, sticky="WE", columnspan=1)
        self.scrolly.grid(row=0, column=1, sticky="NS", rowspan=1)

        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(0, weight=1)


print("editor working")

