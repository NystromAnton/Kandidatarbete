from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog

class App(tk.Tk):

    #def __init__(self, *args, **kwargs):
        #tk.Tk.__init__(self, *args, **kwargs)
    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("500x500")
        self.title('Vattenläckor interface')


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

    path = ""



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Startsida", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        def explorer():
            global path
            path =  filedialog.askopenfilename(initialdir = "C:/Users/User/Documents/Kandidat/Data",title = "Select file")
            T.delete(1.0,"end")
            T.insert(1.0,path)
            bShow.pack()

        def calcShow():
            print(path)
            df = dh.nightHours(path)
            print(df)
            bAnalysis.pack()
            #plot here anton

        bChoose = tk.Button(self, text ="Välj fil", command = explorer)
        bChoose.pack()

        T = tk.Text(self, height=2, width=60)
        T.insert(1.0,"Vald fil..")
        T.pack()

        bShow = tk.Button(self, text ="Räkna ut", command = calcShow)
        bAnalysis = tk.Button(self, text="Visa analys", command=lambda: controller.show_frame("analysisPage"))

        # Om vi behöver en till page:
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        #button2.pack()


class analysisPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analys", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Tillbaka till startsidan",
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
