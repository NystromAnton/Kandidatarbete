import pandas as pd
import numpy as np
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import dateutil
import math



def o_ewma(df):
    print(df)
    data = df['Flow (l/s)']                     # Plocka ut kolumnen med originaldatan. Vet inte om man ska göra detta på originaldatan eller flytande dygn egentligen.
    avg_ewma = data.mean()
    std_ewma = data.std()
    alpha = 0.3
    dataEWMA = data.ewm(alpha=alpha, adjust=False).mean()          # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.
    
    #########test########
    #dataEWMA_01 = data.ewm(alpha=0.1, adjust=False).mean()
    #dataEWMA_02 = data.ewm(alpha=0.2, adjust=False).mean()
    #dataEWMA_09 = data.ewm(alpha=0.9, adjust=False).mean()
    #dataEWMA_05 = data.ewm(alpha=0.5, adjust=False).mean()
    #dataEWMA_07 = data.ewm(alpha=0.7, adjust=False).mean()

    #df['01'] = dataEWMA_01
    #df['02'] = dataEWMA_02
    #df['09'] = dataEWMA_09
    #df['05'] = dataEWMA_05
    #df['07'] = dataEWMA_07

    ######################
    df['EWMA'] = dataEWMA                          # Skapa en ny kolumn i DataFramen som är EWMA
    s_ewma = math.sqrt((alpha/(2-alpha))*(std_ewma**2))
    ewma_ucl = avg_ewma + 3*s_ewma
    ewma_lcl = avg_ewma - 3*s_ewma
    df['UCL_EWMA'] = ewma_ucl
    df['LCL_EWMA'] = ewma_lcl

    count_row = range(df.shape[0])
    print(count_row)
    df['num_rows'] = count_row
    print(df)
    indexNames = df[(df['EWMA'] > ewma_ucl)|(df['EWMA'] < ewma_lcl) ].num_rows
    print(indexNames)
    print(type(indexNames))

    ax = plt.gca()                                 # Axlarna för ploten
    #df.plot(y='Flow (l/s)', color="blue",ax=ax)    # Plotta originaldatan
    df.plot(y='EWMA', color='green', ax=ax)         # Plotta EWMA
    df.plot(y='UCL_EWMA', color='red', ax=ax)
    df.plot(y='LCL_EWMA', color='red', ax=ax)

    for i in indexNames:
        ax.axvline(x=i, color="purple", linestyle="--")

    ########TEST############
    #df.plot(y='01', color="green", ax=ax)
    #df.plot(y='02', color="black", ax=ax)
    #df.plot(y='09', color="gold", ax=ax)
    #df.plot(y='05', color="aqua", ax=ax)
    #df.plot(y='07', color="orange", ax=ax)


    plt.show()                                     # Visa plotten

