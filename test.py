from tkinter import *

class Frame1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg="red")
        self.parent = parent
        self.widgets()

    def widgets(self):
        self.text = Text(self)
        self.text.insert(INSERT, "Hello World\t")
        self.text.insert(END, "This is the first frame")
        self.text.grid(row=0, column=0, padx=20, pady=20) # margins


class MainW(Tk):

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.mainWidgets()

    def mainWidgets(self):

        self.label1 = Label(self, text="Main window label", bg="green")
        self.label1.grid(row=0, column=0)

        self.label2 = Label(self, text="Main window label", bg="yellow")
        self.label2.grid(row=1, column=0)

        self.window = Frame1(self)
        self.window.grid(row=0, column=10, rowspan=2)

if __name__=="__main__":
    app = MainW(None)
    app.mainloop()