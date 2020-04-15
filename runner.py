from pathlib import Path
import pandas as pd
import shewhart as s
import cusum as c
import ewma as e
import datahandler as dh

# Datasets:
aikido = "radata_vatten_aikido.csv"
karate = "radata_vatten_karate.csv"
kendo = "radata_vatten_kendo.csv"
judo = "radata_vatten_judo.csv"
sumo = "radata_vatten_sumo.csv"

# datahandler omvandlar datan till ett värde per dygn
#df = dh.dateMean(karate)
#df = dh.nightMean(karate)
#df = dh.dayMean(karate)
#df = dh.dayHours(karate)
#df = dh.nightHours(karate)
df = dh.dateHours(kendo)

print(df)
#s.shewhart(df)                         # Kalla på shewhart funktionen. Den kommer plotta shewhart och lägga till det i DataFramen.#
#c.cusum(df)                            # Kalla på cusum funktionen. Den kommer plotta cusum och lägga till det i DataFramen.
e.ewma(df)                              # Kalla på ewma funktionen. Den kommer plotta EWMA och lägga till det i DataFramen.
