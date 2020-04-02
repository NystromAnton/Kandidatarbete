from pathlib import Path
import shewhart as s
import cusum as c
import ewma as e
import pandas as pd

def datahandler(dataset_name):
    data_folder = Path("Data/")
    loc = data_folder / dataset_name

    df = pd.read_csv(loc, sep= ';', decimal= ',', engine= 'python')   # Läs in filen som en DataFrame. OBS använder python som engine - funkar men tydligen ganska långsamt
    #print(df.dtypes)

    df.drop(['Time'], axis=1, inplace=True)
    indexStar = df[df['Flow (l/s)'] == '*' ].index        # Get names of indexes for which column Age has value 30
    df.drop(indexStar, inplace=True)                      # Delete these row indexes from dataFrame
    df['Flow (l/s)'] = df['Flow (l/s)'].astype(float)
    #print(df.dtypes)
    #print(df.head())
    df_time_sorted = df.groupby('Date').mean()
    #print(df_time_sorted.head())

    return df_time_sorted
