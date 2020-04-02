import shewhart as s
import cusum as c
import ewma as e
import pandas as pd

loc = "Data\Rådata_vatten_Arboga.xlsx"

df = pd.read_excel(loc)                             # Läs in excelfilen som en DataFrame. Ganska långsam.
for i in range(0, len(df['Flöde (l/s)'])):          # Loopa igenom datan och ta bort '*'
    if df['Flöde (l/s)'][i] == '*':
        df['Flöde (l/s)'][i] = 0                    # Ger meddelandet "A value is trying to be set on a copy of a slice from a DataFrame" men verkar funka. Kanske kolla mer på det så att det inte blir knas

data = df['Flöde (l/s)']
dygn = data.rolling(2880).sum()/1000                # Räkna ut flytande dygn, 2880 då vi har datapunkter var 30e sekund. => 2 per minut => 120 per timme => 2880 per dygn. Delat med 1000 för skala
df['Dygn'] = dygn                                   # Skapa en ny kolumn i DataFramen som är flytande dygn

s.shewhart(df)                                      # Kalla på shewhart funktionen. Den kommer plotta shewhart och lägga till det i DataFramen.
c.cusum(df)                                         # Kalla på cusum funktionen. Den kommer plotta cusum och lägga till det i DataFramen.
e.ewma(df)                                          # Kalla på ewma funktionen. Den kommer plotta EWMA och lägga till det i DataFramen.
print(df)
