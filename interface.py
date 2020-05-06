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
from tkinter import ttk

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
        self.geometry("700x500")
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
            frame.grid(row=0, column=0, sticky="nsew") # Alla frames ligger på samma ställe i en grid. Så bara den högst upp syns.

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
            T.configure(state="normal")
            T.delete(1.0,"end")
            T.insert(1.0, self.controller.shared_data["dataPath"])
            T.configure(state="disabled")
            bAnalysis.pack()

        bChoose = tk.Button(self, text ="Välj fil", command = explorer)
        bChoose.pack()

        T = tk.Text(self, height=2, width=60)
        T.insert(1.0,"Vald fil..")
        T.configure(state="disabled") # Gör att användaren inte kan skriva
        T.pack()

        bAnalysis = tk.Button(self, text="Analysera", command=lambda: controller.show_frame("analysisPage"))

        # Om vi behöver en till page:
        #button2 = tk.Button(self, text="Go to Page Two", command=lambda: controller.show_frame("PageTwo"))
        #button2.pack()
        labelTop = tk.Label(self, height=0, width=60, pady=20, anchor="s", text = "Välj över vilken tidsperiod ett genomsnitt ska beräknas")
        #labelTop.grid(pady=10)
        comboExample = ttk.Combobox(self, state="readonly",
                            values=[
                                    "Dygn",
                                    "Natt",
                                    "Dag",
                                    "Varje timme (dagtid)",
                                    "Varje timme (nattid)",
                                    "Varje timme (dygn)"])
        #print(dict(comboExample))
        #comboExample.grid(column=0, row=1)
        comboExample.current(0)
        labelTop.pack()
        comboExample.pack()

class analysisPage(tk.Frame):
    def creator(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analys", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        bBack = tk.Button(self, text="Tillbaka till startsidan", command=lambda: controller.show_frame("startPage")).place(x=100, y=12)
        #bBack.pack()

        self.bind("<<ShowFrame>>", self.on_show_frame) # Används för att on_show_frame funktionen ska köras när den här framen blir synlig


    def __init__(self, parent, controller):
        #self.creator(parent, controller)
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Analys", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        bBack = tk.Button(self, text="Tillbaka till startsidan", command=lambda: controller.show_frame("startPage")).place(x=100, y=12)
        #bBack.pack()

        self.bind("<<ShowFrame>>", self.on_show_frame) # Används för att on_show_frame funktionen ska köras när den här framen blir synlig


    def calcShow(self):
        df = dh.dateMean(self.controller.shared_data["dataPath"])
        #print(df)

        s.shewhart(df)
        c.cusum(df)
        e.o_ewma(df)

        #scrollbar = tk.Scrollbar(self)
        #scrollbar.pack(side="right", fill="y")

        """for child in analysisPage.winfo_children(self):
            child.destroy()
        #self.creator(parent, controller)
        self.__init__(parent, controller)
        """

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)

        df.plot(y='Flow (l/s)', color='blue', ax=ax1)
        df.plot(y='avg', color='black', ax=ax1)       #Plottar en medelvärdeslinje
        df.plot(y='UCL', color='red', ax=ax1)         #Plottar UCL
        df.plot(y='LCL', color='red', ax=ax1)         #Plottar LCL

        df.plot(y='cusum', color='green', ax=ax2)                                    # Lägg till CUSUMen i plotten.
        df.plot(y='v-mask', color='red', ax=ax2, linewidth=2)                        # Gör de delar som är ur kontroll röda

        df.plot(y='EWMA', color='green', ax=ax3)         # Plotta EWMA
        df.plot(y='UCL_EWMA', color='red', ax=ax3)
        df.plot(y='LCL_EWMA', color='red', ax=ax3)

        fig.autofmt_xdate()

        ax1.set_title('Shewhart')
        ax2.set_title('CUSUM')
        ax3.set_title('EWMA')

        try:
            self.canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.

        try:
            #self.toolbar.get_tk_widget().pack_forget()
            self.toolbar.get_tk_widget().destroy()
        except AttributeError:
            pass
        self.toolbar = NavigationToolbar2Tk(self.canvas, self) # Navigationbar för att kunna zooma och spara plotten mm
        self.toolbar.update()

        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


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
