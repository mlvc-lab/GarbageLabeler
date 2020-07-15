from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import pathlib
import csv
import pandas as pd


class IndicatorFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='blue')
        self.parent = parent
        self.widgets()
    
    def widgets(self):
        self.imgDirFrame = Frame(self)
        self.imgDirLablePrefix = Label(self, text='Image Dir: ')
        self.imgDirLablePrefix.grid(row=0, column=0, padx=5, pady=5, sticky=W)

        self.imgDirLable = Label(self, text='')
        self.imgDirLable.grid(row=0, column=1, padx=5, pady=5)

        self.saveLablePrefix = Label(self, text='SaveFile: ')
        self.saveLablePrefix.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        self.saveLable = Label(self, text='')
        self.saveLable.grid(row=1, column=1, padx=5, pady=5)


class ImageFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, bg='red')
        self.parent = parent
        self.imageDir = None
        self.index = 0
        self.widgets()

    def updateImage(self):
        if self.imageDir == None:
            return

        glob = sorted(self.imageDir.glob('**/*'))
        files = [x for x in glob if x.is_file()]

        if self.index >= len(files):
            self.index -= 1
        elif self.index < 0:
            self.index += 1

        image = Image.open(files[self.index])
        self.size = image.size
        self.img = ImageTk.PhotoImage(image=image)
        self.name.configure(text=files[self.index])
        self.imglb.configure(image=self.img, width=self.size[0], height=self.size[1])

    def prevImage(self):
        self.index -= 1
        self.updateImage()

    def nextImage(self):
        self.index += 1
        self.updateImage()

    def widgets(self):
        self.name = Label(self, text='')
        self.name.pack()

        self.img = ImageTk.PhotoImage(image=Image.open('no-image.jpg'))
        self.imglb = Label(self, image=self.img)
        self.imglb.bind('<Button-1>', lambda e: self.updateImage())
        self.imglb.pack()

        self.nextbtn = Button(self, text='Next >>', command=self.nextImage)
        self.nextbtn.pack(side=RIGHT)
        self.prevbtn = Button(self, text='<< Prev', command=self.prevImage)
        self.prevbtn.pack(side=RIGHT)
        


class LabelCheckFrame(Frame):
    def __init__(self, parent, labels):
        Frame.__init__(self, parent, bg='green')
        self.parent = parent
        self.labels = labels
        self.vars = []
        self.widgets()

    def widgets(self):
        for i, label in enumerate(self.labels):
            self.vars.append(IntVar())
            checkbutton = Checkbutton(self,
                                      text=label,
                                      variable=self.vars[i],
                                      offvalue=0,
                                      onvalue=1,
                                      command=self.makeLabel)
            checkbutton.pack()

        self.lbl = Label(self, text='')
        self.lbl.pack()

        self.saveBtn = Button(self, text='Save', command=self.save)
        self.saveBtn.pack()

    def save(self):
        fname = pathlib.Path(self.parent.imageFrame.name.cget('text')).name
        self.parent.saveFileWriter.writerow([fname, self.lbl.cget('text')])
        # self.parent.saveFileWriter.
        print([fname, self.lbl.cget('text')])

    def makeLabel(self):
        name = []
        for i, var in enumerate(self.vars):
            if var.get() == 1:
                name.append(str(i+1))

        self.lbl.configure(text=', '.join(name))


class MainWindow(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.labels = [
            'etc', 'paper', 'can', 'glass', 'plastic', 'vinyl', 'styrofoam', 'leftovers'
        ]
        # self.geometry("600x400+10+10")
        self.fileDir = None
        self.saveFile = None
        self.data = pd.DataFrame(columns=['img', 'class'])
        self.mainMenu()
        self.mainWidgets()
        self.protocol("WM_DELETE_WINDOW", self.closeFile)

    def mainMenu(self):
        self.menubar = Menu(self)
        fileMenu = Menu(self.menubar)
        fileMenu.add_command(label='Open Image Dir', command=self.openImageDir)
        fileMenu.add_command(label='Load File', command=self.loadFile)
        fileMenu.add_command(label='Save', command=self.save)
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=None)
        self.menubar.add_cascade(label="File", menu=fileMenu)
        self.configure(menu=self.menubar)

    def mainWidgets(self):
        self.indicatorFrame = IndicatorFrame(self)
        self.indicatorFrame.grid(row=0, column=0, sticky=W, columnspan=2)

        self.imageFrame = ImageFrame(self)
        self.imageFrame.grid(row=1, column=0, sticky=S)

        self.lableCheck = LabelCheckFrame(self, self.labels)
        self.lableCheck.grid(row=1, column=1, sticky=E+S)

    def openImageDir(self):
        self.fileDir = filedialog.askdirectory()
        self.indicatorFrame.imgDirLable.configure(text=self.fileDir)
        self.imageFrame.imageDir = pathlib.Path(self.fileDir)
        self.imageFrame.updateImage()

    def loadFile(self):
        self.saveFile = filedialog.asksaveasfilename()
        self.indicatorFrame.saveLable.configure(text=saveFileName)
        self.data = pd.read_csv(saveFileName, header=None)
    
    def save(self):
        if 
        self.data.to_csv(self.saveFile)

    def closeFile(self):
        if self.saveFile:
            self.saveFile.close()
        self.destroy()


if __name__ == "__main__":
    app = MainWindow(None)
    app.mainloop()