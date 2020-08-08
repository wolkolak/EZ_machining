import tkinter as tk
import tkinter.ttk as ttk






class Editor(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid_propagate(1)
        self.text = tk.Text(self,  bg="darkgreen", fg='white', wrap=tk.NONE, width=20,)# height=30,
        self.scrolly = tk.Scrollbar(self, command=self.text.yview, orient=tk.VERTICAL)
        self.scrollx = tk.Scrollbar(self, command=self.text.xview, orient=tk.HORIZONTAL)
        #self.text.config(yscrollcommand=self.scrolly.set, )
        self.text.config(yscrollcommand=self.scrolly.set, xscrollcommand=self.scrollx.set)

        #self.mainframe.grid(row=0, column=0, sticky='NSWE')
        self.text.grid(row=0, column=0, rowspan=1, sticky="NSWE")
        self.scrollx.grid(row=1, column=0, sticky="WE", columnspan=1)
        self.scrolly.grid(row=0, column=1, sticky="NS", rowspan=1)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)





class MyTabs(ttk.Notebook):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid(row=0, column=0, sticky="nswe", columnspan=1)
        self.field1 = Editor(self)
        self.add(self.field1, text='page1')
        self.new_tab_button = tk.Frame(self)
        self.add(self.new_tab_button, text='NEW')
        #self.new_tab_button.bind("<Button-1>", self.press_for_new_tab)
        #self.select(1).bind("<Button-1>", self.press_for_new_tab)
        self.tabs_nom_generator = self.generate()
        self.bind("<<NotebookTabChanged>>", self.selected_new_tab)
        self.number = 1

    def new_tab(self):
        self.new_field = Editor(self)

        #number = next(self.tabs_nom_generator)
        self.add(self.new_field, text='page{}'.format(self.number))
        #return number

    def generate(self):
        for value in range(2, 10000):
            yield value

    #@staticmethod
    def selected_new_tab(self, event):
        if self.index(self.select()) == self.number:
            # todo delete new
            self.forget(self.select())
            self.new_tab()
            self.select(self.number)
            # todo create new
            self.number = next(self.tabs_nom_generator)
            self.new_tab_button = tk.Frame(self)
            self.add(self.new_tab_button, text='NEW')
        print("new tab activaited!!")



"""
    @staticmethod
    def new_name():
        if 
"""



#self.f1 = Editor(self, "cyan")
#self.f2 = Editor(self, "cyan")