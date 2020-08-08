from tkinter import *
from tkinter.ttk import *
from tkinter.scrolledtext import ScrolledText

root = Tk()


class F(Frame):
    def __init__(self):
        super().__init__()
        root.geometry("500x500")
        self.master.resizable(False,False)


        self.tab = Notebook(root)
        self.tab.grid(row=1, column=33, columnspan=10, rowspan=50, padx=5, pady=5, sticky='NS')

        self.mb = Menu( root )
        root.config( menu=self.mb )
        self.sub_mb = Menu( self.mb, tearoff=0 )
        self.mb.add_command( label='create tab', command = self.create_tab )
        self.mb.add_command( label='print', command=self.print_contents_of_all_tabs )

    def create_tab(self):
        self.new_tab = ScrolledText(height=20, width=50)
        self.tab.add( self.new_tab, text='tab' )

    #this should print the contents inside all the tabs**
    def print_contents_of_all_tabs(self):
        all_tabs = self.tab.tabs()            # get frame name of all tabs
        for x in range(len(all_tabs)):
            print(self.tab.index(all_tabs[x])) # print the index using frame name
            print(self.new_tab.get(1.0, END))  # This prints only the content of recently created tab

def main():
    F().mainloop()

main()