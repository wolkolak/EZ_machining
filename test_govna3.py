try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except ImportError:
    import Tkinter as tk


def on_button_press(widget):
    width = 512
    height = 256
    x = 16
    y = 32
    widget.winfo_toplevel().geometry('{}x{}+{}+{}'.format(width, height, x, y))


if __name__ == '__main__':
    root = tk.Tk()
    window = tk.Toplevel(root)
    button = tk.Button(window, text="Resize & Place")
    #the line below is related to calling a method when a button is pressed
    button['command'] = lambda w=button: on_button_press(w)
    button.pack()
    tk.mainloop()