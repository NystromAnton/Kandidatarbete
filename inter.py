from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
#from tkinter import filedialog
#from tkinter import *

"""
w = Tk()

def explorer():
    filename =  filedialog.askopenfilename(initialdir = "C:/Users/User/Documents/Kandidat/Data",title = "Select file")
    print(filename)
    return filename

B = Button(w, text ="Hello", command = explorer)
print("2")

B.pack()
w.mainloop()

# Datasets:
aikido = "radata_vatten_aikido.csv"
karate = "radata_vatten_karate.csv"
kendo = "radata_vatten_kendo.csv"
judo = "radata_vatten_judo.csv"
sumo = "radata_vatten_sumo.csv"
"""
"""class startPage:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="Quit", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

        self.hi_there = Button(frame, text="Hello", command=self.say_hi)
        #self.hi_there = Button(frame, text="Visit Page 2", command=lambda: controller.show_frame(plotPage))
        self.hi_there.pack(side=LEFT)

    def say_hi(self):
        print("hi there, everyone!")

class plotPage:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()

        self.button = Button(
            frame, text="plotQuit", fg="red", command=frame.quit
            )
        self.button.pack(side=LEFT)

root = Tk()
App = startPage(root)

root.mainloop()
root.destroy()
"""
import tkinter as tk
from tkinter import font  as tkfont

class App(tk.Tk):

    #def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs)
    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # På stacken ligger frames, den frame som är högst upp är den som syns.
        # Så för att visa olika vyer (pages) flyttar man vilken som är högst upp
        stack = tk.Frame(self)
        stack.pack(side="top", fill="both", expand=True)
        stack.grid_rowconfigure(0, weight=1)
        stack.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #for F in (startPage, analysisPage, PageTwo):
        for F in (startPage, analysisPage):
            page_name = F.__name__
            frame = F(parent=stack, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew") # Alla frames ligger på samma ställa i en grid. Så bara den högst upp syns.

        self.show_frame("startPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class startPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("analysisPage"))
        # Om vi behöver en till page:
        #button2 = tk.Button(self, text="Go to Page Two",
        #                    command=lambda: controller.show_frame("PageTwo"))
        button1.pack()
        #button2.pack()


class analysisPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("startPage"))
        button.pack()

# Om vi behöver en till page:
"""class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("startPage"))
        button.pack()"""


if __name__ == "__main__":
    App = App()
    App.mainloop()
