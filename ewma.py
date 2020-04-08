import pandas as pd
import numpy as np
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import dateutil
import math

def o_ewma(df):
    data = df['Flow (l/s)']                        # Plocka ut kolumnen med originaldatan. Vet inte om man ska göra detta på originaldatan eller flytande dygn egentligen.
    avg_ewma = data.mean()
    std_ewma = data.std()
    alpha = 0.3
    dataEWMA = data.ewm(alpha=alpha, adjust=False).mean()          # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.
    df['EWMA'] = dataEWMA                          # Skapa en ny kolumn i DataFramen som är EWMA
    s_ewma = math.sqrt((alpha/(2-alpha))*(std_ewma**2))
    ewma_ucl = avg_ewma + 3*s_ewma
    ewma_lcl = avg_ewma - 3*s_ewma
    df['UCL_EWMA'] = ewma_ucl
    df['LCL_EWMA'] = ewma_lcl

    ax = plt.gca()                                 # Axlarna för ploten
    df.plot(y='Flow (l/s)', color="blue",ax=ax)    # Plotta originaldatan
    df.plot(y='EWMA', color='pink', ax=ax)         # Plotta EWMA
    df.plot(y='UCL_EWMA', color='red', ax=ax)
    df.plot(y='LCL_EWMA', color='black', ax=ax)
    

    plt.show()                                     # Visa plotten

