import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

def shewhart(df):
    avg = df['Dygn'].mean()                                # Medelvärdet av EWMA
    df['avg'] = avg                                     # Skapa en ny kolumn i DataFramen som är medelvärdet
    std = df['Dygn'].std()                                 # Räkna ut standardavvikelsen
    df['std+'] = avg + (3*std)                          # Skapa en ny kolumn i DataFramen som är medelvärdet + 3*standardavvikelse
    df['std-'] = avg - (3*std)                          # Skapa en ny kolumn i DataFramen som är medelvärdet - 3*standardavvikelse

    ax = plt.gca()                                      # Nåt med axlarna för ploten

    df.plot(y='Flöde (l/s)', color="blue",ax=ax)                            # Plotta originaldatan
    df.plot(y='Dygn', color="yellow",ax=ax)                                 # Plotta flytande dygn
    df.plot(y='avg', color='black', ax=ax)                                  # Plotta medelvärdet
    df.plot(y='std+', color='red', ax=ax)                                   # Plotta medelvärdet + 3*standardavvikelse
    df.plot(y='std-', color='red', ax=ax)                                   # Plotta medelvärdet - 3*standardavvikelse

    plt.show()                                                              # Visa plotten

#shewhart("Rådata_vatten_Arboga.xlsx")
