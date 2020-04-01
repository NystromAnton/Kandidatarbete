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


loc = ("data.xlsx")
df = pd.read_excel(loc)                             #Läs in excelfilen som en DataFrame

data = df['Flödesdata  (MED) (l/s, 15 min medel)']  #Plocka ut kolumnen med datan
dataEWM = data.ewm(com=100).mean()                  # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.
dygn = data.rolling(96).sum()/100
df['Dygn'] = dygn                                 # Skapa en ny kolumn i DataFramen som är rullande dygn
avg = dygn.mean()                                # Medelvärdet av EWMA
df['avg'] = avg                                     # Skapa en ny kolumn i DataFramen som är medelvärdet
std = dygn.std()                                 # Räkna ut standardavvikelsen
df['std+'] = avg + (3*std)                          # Skapa en ny kolumn i DataFramen som är medelvärdet + 3*standardavvikelse
df['std-'] = avg - (3*std)                          # Skapa en ny kolumn i DataFramen som är medelvärdet - 3*standardavvikelse
df['cusum'] = get_cusum(dygn)                    # Skapa en ny kolumn i DataFramen som är cusum

ax = plt.gca()                                      # Nåt med axlarna för ploten

df.plot(y='Flödesdata  (MED) (l/s, 15 min medel)', color="blue",ax=ax)  # Plotta originaldatan
df.plot(y='Dygn', color="yellow",ax=ax)                                 # Plotta flytande dygn
df.plot(y='avg', color='black', ax=ax)                                  # Plotta medelvärdet
df.plot(y='std+', color='red', ax=ax)                                   # Plotta medelvärdet + 3*standardavvikelse
df.plot(y='std-', color='red', ax=ax)                                   # Plotta medelvärdet - 3*standardavvikelse
df.plot(y='cusum', color='orange', ax=ax)                               # Plotta cusum

plt.show()                                                              # Visa plotten
