import pandas as pd
import numpy as np
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import dateutil

def ewma(df):
    data = df['Flow (l/s)']                        # Plocka ut kolumnen med originaldatan. Vet inte om man ska göra detta på originaldatan eller flytande dygn egentligen.
    dataEWMA = data.ewm(com=100).mean()            # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.
    df['EWMA'] = dataEWMA                          # Skapa en ny kolumn i DataFramen som är EWMA
#    ax = plt.gca()                                 # Axlarna för ploten

#    df.plot(y='Flow (l/s)', color="blue",ax=ax)    # Plotta originaldatan
#    df.plot(y='EWMA', color='pink', ax=ax)         # Plotta EWMA

    plt.scatter(df.index, data)
    plt.show()                                     # Visa plotten
