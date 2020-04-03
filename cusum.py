import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

# Hjälpfunktion för att räkna ut cusumen för en kolumn.
# Precondition: None
# In: data = en kolumn i en DataFrame.
# Out: En DataFrame med en CUSUM för den givna kolumnen.
# Sideeffect: None
def get_cusum(data):
    normalized = (data - data.mean()) / data.std()                              # Normalisera datan i kolumnen.
    s = [0]                                                                     # Skapa en lista och sätt första värdet till 0.
    for i in range(1, len(data)):                                               # Loopa igenom kolumnen.
        s.append(s[i-1] + normalized[i] - normalized.mean())                    # Räkna ut CUSUM värdet för den datapunkten och lgg till i listan.
    return pd.DataFrame(s)                                                      # Returnera CUSUMen som en DataFrame

# Funktion som tar kolumnen 'Flow (l/s)' i en DataFrame och räknar ut en CUSUM för den kolumnen.
# Precondition: DataFramen måste ha en kolumn med namnet 'Flow (l/s)'.
# In: En DataFrame.
# Out: None
# Sideeffect: Skapar en ny kolum i den givna DataFramen som heter 'cusum'.
def cusum(df):
    df['cusum'] = get_cusum(df['Flow (l/s)']).set_index(df.index)               # Skapa en ny kolumn i DataFramen som heter 'cusum'. set_index synkar indexeringen på den nya kolumnen och DataFramen så att de är samma.

    ax = plt.gca()                                                              # Nåt med axlarna för ploten

    df.plot(y='cusum', color='green', ax=ax)                                    # Lägg till CUSUMen i plotten.

    plt.show()                                                                  # Visa plotten
