import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import math

# Funktion som med hjälp av en v-mask identifierar när en cusum-kurva är ur kontroll.
# Precondition: DataFramen måste innehålla en kolumn som heter 'cusum'
# In: data = en DataFrame.
# Out: None
# Sideeffect: Lägger till en ny kolumn i DataFramen som heter 'v-mask'
def v_mask(data):
    data['v-mask'] = None
    delta = 1                                                                   # Delta är antal sigma som krävs för att masken ska reagera.
    k = delta/2                                                                 # Lutningen i v-maskens linjer.
    h = 8                                                                       # h och d är en del av en förskjutning i v-masken för att hantera type1/type 2 errors.
    d = h/k
    for i in range(1, int(len(data['cusum'])-d)):                               # Loopa genom varje datapunkt. Första datapunkten har inga föregående punkter så börja på index 1 istället för 0. Avsluta på längden minus d för att index ej ska gå out of bound.
        x1 = (data['cusum'][i])                                                 # Plocka ut datapunktens värde
        j = i - 1                                                               # Börja i den föregående punkten.
        while j >= 1:                                                           # Loopa genom alla föregående datapunkter.
            x2 = (data['cusum'][j])                                             # Plocka ut datapunktens värde
            upper = (k*(int(j+d))) + x1                                         # Räkna ut värdet i den övre v-mask linjen. d är en förskjutning från originaldatapunkten till vertex för v-masken.
            lower = (-k*(int(j+d))) + x1                                        # Räkna ut värdet i den undre v-mask linjen d är en förskjutning från originaldatapunkten till vertex för v-masken.
            if x2 < lower or x2 > upper:                                        # Kolla om datapunkten befinner sig utanför övre/undre gränsen.
                data['v-mask'][i] = x1                                          # Om den gör det så är den ur kontroll. Lägg till den i 'v-mask' kolumnen.
            j = j - 1

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
    v_mask(df)                                                                  # Applicera v-masken på dataframen. En ny kolumn som heter 'v-mask' skapas i df.

    ax = plt.gca()                                                              # Nåt med axlarna för ploten


    df.plot(y='cusum', color='green', ax=ax)                                    # Lägg till CUSUMen i plotten.
    df.plot(y='v-mask', color='red', ax=ax, linewidth=2)                        # Gör de delar som är ur kontroll röda

    plt.show()                                                                  # Visa plotten
