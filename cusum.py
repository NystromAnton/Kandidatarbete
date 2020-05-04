import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import math

def get_cusum2(data):
    normalized = (data['Flow (l/s)'] - data['Flow (l/s)'].mean()) / data['Flow (l/s)'].std()                              # Normalisera datan i kolumnen.
    s_low = [0]
    s_high = [0]
    delta = 1                                                                   # Delta är antal sigma som krävs för att masken ska reagera.
    k = delta/2                                                                 # Lutningen i v-maskens linjer.
    a = 0.0027
    B = 0.01
    d = 2 * math.log((1-B)/a)
    h = d*k
    vmask = [None]
    for i in range(1, len(normalized)):                                               # Loopa igenom kolumnen.
        high = max(0, s_high[i-1] + normalized[i] - normalized.mean() - k)
        low = max(0, s_low[i-1] + normalized.mean() - k - normalized[i])
        s_high.append(high)
        s_low.append(low)
        if high > h or low > h:
            vmask.append(max(high, low))
        else:
            vmask.append(None)

    data['cusum'] = pd.DataFrame(s_high).set_index(data.index)
    data['v-mask'] = pd.DataFrame(vmask).set_index(data.index)

def get_dates(data):
    datapoints_out_of_control = data[data['v-mask'] != 0].index #Tar ut alla index /dagar den är out of control.
    return datapoints_out_of_control

# Funktion som tar kolumnen 'Flow (l/s)' i en DataFrame och räknar ut en CUSUM för den kolumnen.
# Precondition: DataFramen måste ha en kolumn med namnet 'Flow (l/s)'.
# In: En DataFrame.
# Out: None
# Sideeffect: Skapar en ny kolum i den givna DataFramen som heter 'cusum'.
def cusum(df):
    get_cusum2(df)               # Skapa en ny kolumn i DataFramen som heter 'cusum'. set_index synkar indexeringen på den nya kolumnen och DataFramen så att de är samma.
    dates = get_dates(df)
    return dates


################################GAMMALT#########################################
# Funktion som med hjälp av en v-mask identifierar när en cusum-kurva är ur kontroll.
# Precondition: DataFramen måste innehålla en kolumn som heter 'cusum'
# In: data = en DataFrame.
# Out: None
# Sideeffect: Lägger till en ny kolumn i DataFramen som heter 'v-mask'
def v_mask(data):
    data['v-mask'] = 0
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
    s = [0]                                                                   # Skapa en lista och sätt första värdet till 0.
    for i in range(1, len(data)):                                               # Loopa igenom kolumnen.
        s.append(s[i-1] + normalized[i] - normalized.mean())                    # Räkna ut CUSUM värdet för den datapunkten och lgg till i listan.
    return pd.DataFrame(s)                                                      # Returnera CUSUMen som en DataFrame
