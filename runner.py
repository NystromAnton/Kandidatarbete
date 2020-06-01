from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh
import graphicshandler as gh
import matplotlib.pyplot as plt

# Datasets:
aikido = "Data/radata_vatten_aikido.csv"
karate = "Data/radata_vatten_karate.csv"
kendo  = "Data/radata_vatten_kendo.csv"
judo   = "Data/radata_vatten_judo.csv"
sumo   = "Data/radata_vatten_sumo.csv"

# datahandler omvandlar datan till ett värde per dygn
df = dh.dateMean(karate)
#df = dh.nightMean(karate)
#df = dh.dayMean(karate)
#df = dh.dayHours(karate)
#df = dh.nightHours(karate)
#df = dh.dateHours(kendo)

s.shewhart(df)                         # Kalla på shewhart funktionen. Den kommer plotta shewhart och lägga till det i DataFramen.
c.cusum(df)                            # Kalla på cusum funktionen. Den kommer plotta cusum och lägga till det i DataFramen.
e.o_ewma(df)                              # Kalla på ewma funktionen. Den kommer plotta EWMA och lägga till det i DataFramen.

print(df)

def plotFlow(df):
    ax = plt.gca()

    df.plot(y='Flow (l/s)', color='blue', label='Vattenflöde', ax=ax, fontsize=11)
    plt.title('Vattenflöde', fontsize=40)
    plt.xlabel("Datum", fontsize=25)
    plt.ylabel("Liter per sekund", fontsize=25)
    plt.legend(loc=1, fontsize = 'xx-large')
    plt.tick_params(labelsize=15)

    plt.show()

def plotShewhart(df):
    ax = plt.gca()

    df.plot(y='Flow (l/s)', color='blue', label='Vattenflöde', ax=ax, fontsize=11)
    df.plot(y='avg', color='black', label='Medelflöde', ax=ax, fontsize=11)       #Plottar en medelvärdeslinje
    df.plot(y='UCL', color='red', ax=ax, fontsize=11)         #Plottar UCL
    df.plot(y='LCL', color='red', ax=ax, fontsize=11)         #Plottar LCL
    plt.title('Shewhart', fontsize=40)
    plt.xlabel("Datum", fontsize=25)
    plt.ylabel("Liter per sekund", fontsize=25)
    plt.legend(loc=1, fontsize = 'xx-large')
    plt.tick_params(labelsize=15)

    plt.show()

def plotCUSUM(df):
    ax = plt.gca()
    
    df.plot(y='cusum', color='green', label='CUSUM', ax=ax, fontsize=11)              # Lägg till CUSUMen i plotten.
    df.plot(y='v-mask', color='red', label='Ur kontroll', ax=ax, linewidth=2, fontsize=11)  # Gör de delar som är ur kontroll röda
    plt.title('CUSUM', fontsize=40)
    plt.xlabel("Datum", fontsize=25)
    plt.ylabel(r'$\sigma$', fontsize=30)
    plt.legend(loc=1, fontsize = 'xx-large')
    plt.tick_params(labelsize=15)

    plt.show()

def plotEWMA(df):
    ax = plt.gca()

    df.plot(y='EWMA', color='green', ax=ax, fontsize=11)         # Plotta EWMA
    df.plot(y='UCL_EWMA', color='red', label='UCL', ax=ax, fontsize=11)
    df.plot(y='LCL_EWMA', color='red', label='LCL', ax=ax, fontsize=11)
    plt.title('EWMA', fontsize=40)
    plt.xlabel("Datum", fontsize=25)
    plt.ylabel("Liter per sekund", fontsize=25)
    plt.legend(loc=1, fontsize = 'xx-large')
    plt.tick_params(labelsize=15)

    plt.show()

#plotFlow(df)
#plotShewhart(df)
plotCUSUM(df)
#plotEWMA(df)