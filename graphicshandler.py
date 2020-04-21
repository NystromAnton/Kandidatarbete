from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plotAll(df):
    ax = plt.gca()                          #Något för plottarna

    gs = gridspec.GridSpec(2, 2) # Create 2x2 sub plot

    # plot shewhart
    ax = plt.subplot(gs[0, 0]) # row 0, col 0
    df.plot(y='Flow (l/s)', color="blue",ax=ax)  #plottar flödesdatan från column "Flow (l/s)"
    df.plot(y='avg', color='black', ax=ax)       #Plottar en medelvärdeslinje
    df.plot(y='UCL', color='red', ax=ax)         #Plottar UCL
    df.plot(y='LCL', color='red', ax=ax)         #Plottar LCL
    ax.set_title("Shewhart")
    plt.gcf().autofmt_xdate()

    # plot cusum
    ax = plt.subplot(gs[0, 1]) # row 0, col 1
    df.plot(y='cusum', color='green', ax=ax)                                    # Lägg till CUSUMen i plotten.
    df.plot(y='v-mask', color='red', ax=ax, linewidth=2)                        # Gör de delar som är ur kontroll röda
    ax.set_title("Cusum")
    plt.gcf().autofmt_xdate()

    # plot ewma
    ax = plt.subplot(gs[1, 0]) # row 1, col 0
    df.plot(y='EWMA', color='green', ax=ax)         # Plotta EWMA
    df.plot(y='UCL_EWMA', color='red', ax=ax)
    df.plot(y='LCL_EWMA', color='red', ax=ax)
    ax.set_title("EWMA")
    plt.gcf().autofmt_xdate()

    plt.show()                                   # Visa plotten
    return
