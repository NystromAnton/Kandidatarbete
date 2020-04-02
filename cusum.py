import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

# Funktion för att räkna ut "The high cusum value"
def get_cusum_h(data):
    normalized = (data - data.mean()) / data.std()
    s = [0]
    for i in range(1, len(data)):
        s.append(max(0,s[i-1] + normalized[i] - normalized.mean()))
    return s

# Funktion för att räkna ut "The low cusum value"
def get_cusum_l(data):
    normalized = (data - data.mean()) / data.std()
    s = [0]
    for i in range(1, len(data)):
        s.append((max(0,s[i-1] - normalized[i] - normalized.mean())))
    return s

def cusum2(data):
    normalized = (data - data.mean()) / data.std()
    s = [0]
    for i in range(1, len(data)):
        s.append(s[i-1] + normalized[i] - normalized.mean())
    return pd.DataFrame(s)

# Funktion för att räna ut cusum.
def get_cusum(data):
    s = []
    H = get_cusum_h(data)
    L = get_cusum_l(data)
    for i in range(0, len(data)):
        if H[i] == 0 and L[i] == 0:
            s.append(data.mean())
        elif H[i] != 0:
            s.append(H[i])
        elif L[i] != 0:
            s.append(-L[i])
    return pd.DataFrame(s)

def cusum(df):
    df['cusum'] = get_cusum(df['Flow (l/s)']).set_index(df.index)                                     # Skapa en ny kolumn i DataFramen som är cusum
    df['cusum2'] = cusum2(df['Flow (l/s)']).set_index(df.index)                                     # Skapa en ny kolumn i DataFramen som är cusum

    ax = plt.gca()                                                          # Nåt med axlarna för ploten
                               # Plotta flytande dygn
    df.plot(y='cusum', color='green', ax=ax)                               # Plotta cusum
    df.plot(y='cusum2', color='orange', ax=ax)                               # Plotta cusum
    df.plot(y='Flow (l/s)', color='blue', ax=ax)

    plt.show()                                                              # Visa plotten
