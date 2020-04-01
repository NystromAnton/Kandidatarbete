import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

# Funktion för att räkna ut "The high cusum value"
def get_cusum_h(data):
    normalized = (data - data.mean()) / data.std()
    s = [0]
    for i in range(1, len(data)):
        s.append(max(0,s[i-1] + normalized[i] - 1))
    return s

# Funktion för att räkna ut "The low cusum value"
def get_cusum_l(data):
    normalized = (data - data.mean()) / data.std()
    s = [0]
    for i in range(1, len(data)):
        s.append((max(0,s[i-1] - normalized[i] - 1)))
    return s

# Funktion för att räna ut cusum. Jävligt tveksam om det är såhär man gör.
def get_cusum(data):
    s = []
    H = get_cusum_h(data)
    L = get_cusum_l(data)
    for i in range(0, len(data)):
        if H[i] == 0 and L[i] == 0:
            s.append(0)
        elif H[i] != 0:
            s.append(H[i])
        elif L[i] != 0:
            s.append(-L[i])
    return pd.DataFrame(s)/1000  # Kurvan blev orimligt stor i plotten så delade med tusen för att kunna se bättre

def cusum(df):
    df['cusum'] = get_cusum(df['Dygn'])                                     # Skapa en ny kolumn i DataFramen som är cusum

    ax = plt.gca()                                                          # Nåt med axlarna för ploten

    df.plot(y='Flöde (l/s)', color="blue",ax=ax)                            # Plotta originaldatan
    df.plot(y='Dygn', color="yellow",ax=ax)                                 # Plotta flytande dygn
    df.plot(y='cusum', color='orange', ax=ax)                               # Plotta cusum

    plt.show()                                                              # Visa plotten

#cusum("Rådata_vatten_Arboga.xlsx")
