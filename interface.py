from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
from tkinter import filedialog
from tkinter import *

path = ""

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
    #plot here anton

w = Tk()
w.geometry("500x500")
w.title('Vattenläckor interface')

bChoose = Button(w, text ="Välj fil", command = explorer)
bChoose.pack()

bShow = Button(w, text ="Räkna ut", command = calcShow)

T = Text(w, height=2, width=60)
T.insert(1.0,"Vald fil..")
T.pack()

w.mainloop()
