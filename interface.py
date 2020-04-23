from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
import graphicshandler as gh
import tkinter as tk
from tkinter import font as tkfont
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import numpy as np

class App(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry("500x500")
        self.title('Vattenläckor interface')

        self.shared_data = { # Delad data som alla frames kan komma åt
            "dataPath": tk.StringVar()
        }

        # På stacken ligger frames, den frame som är högst upp är den som syns.
        # Så för att visa olika vyer (pages) flyttar man vilken som är högst upp (med funktionen show_frame)
        stack = tk.Frame(self)
        stack.pack(side="top", fill="both", expand=True)
        stack.grid_rowconfigure(0, weight=1)
        stack.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #for F in (startPage, analysisPage, PageTwo): #OBS den här raden om vi ska ha en frame till
        for F in (startPage, analysisPage):
            page_name = F.__name__
            frame = F(parent=stack, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew") # Alla frames ligger på samma ställa i en grid. Så bara den högst upp syns.

        self.show_frame("startPage")

    def show_frame(self, page_name): # Gör givna framen synlig
        frame = self.frames[page_name]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>")

class startPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Startsida", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        def explorer():
            self.controller.shared_data["dataPath"] = filedialog.askopenfilename(initialdir = "C:/Users/User/Documents/Kandidat/Data",title = "Select file")
            T.delete(1.0,"end")
            T.insert(1.0, self.controller.shared_data["dataPath"])
            bAnalysis.pack()

        bChoose = tk.Button(self, text ="Välj fil", command = explorer)
        bChoose.pack()

        T = tk.Text(self, height=2, width=60)
        T.insert(1.0,"Vald fil..")
        T.pack()

        bAnalysis = tk.Button(self, text="Analysera", command=lambda: controller.show_frame("analysisPage"))

        # Om vi behöver en till page:
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        #button2.pack()

class analysisPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analys", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        bBack = tk.Button(self, text="Tillbaka till startsidan", command=lambda: controller.show_frame("startPage"))
        bBack.pack()

        self.bind("<<ShowFrame>>", self.on_show_frame) # Används för att on_show_frame funktionen ska köras när den här framen blir synlig

    def calcShow(self):
        #print(self.controller.shared_data["dataPath"])
        """A = tk.Text(self, height=2, width=60)
        A.insert(1.0,"Beräknar...")
        A.pack()"""
        df = dh.nightHours(self.controller.shared_data["dataPath"])
        print(df)

        fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        ###########################################################
        """ax = plt.gca()                          #Något för plottarna

        gs = gridspec.GridSpec(2, 2) # Create 2x2 sub plot

        # plot shewhart
        ax = plt.subplot(gs[0, 0]) # row 0, col 0
        df.plot(y='Flow (l/s)', color='blue', ax=ax)  #plottar flödesdatan från column "Flow (l/s)"
        df.plot(y='avg', color='black', ax=ax)       #Plottar en medelvärdeslinje
        df.plot(y='UCL', color='red', ax=ax)         #Plottar UCL
        df.plot(y='LCL', color='red', ax=ax)         #Plottar LCL
        ax.set_title("Shewhart")
        plt.gcf().autofmt_xdate()"""
        #########################################################
        canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea. # Stod root istället för self innan
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, self) # Stod root istället för self innan
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def on_show_frame(self, event):
        self.calcShow()


# Om vi behöver en till page:
"""class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page", command=lambda: controller.show_frame("startPage"))
        button.pack()"""

if __name__ == "__main__":
    App = App()
    App.mainloop()
