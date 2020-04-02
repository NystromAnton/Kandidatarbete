from pathlib import Path
import pandas as pd

def datahandler(dataset_name):

    data_folder = Path("Data/")                         # Metod för att pathen ska funka på både linux och windows
    loc = data_folder / dataset_name                    # För att hitta filen

    df = pd.read_csv(loc, sep= ';', decimal= ',', engine= 'python')   # Läs in filen som en DataFrame. OBS använder python som engine - funkar men tydligen ganska långsamt

    df.drop(['Time'], axis=1, inplace=True)             # Tar bort tidscolumnen
    indexStar = df[df['Flow (l/s)'] == '*' ].index      # Hitta alla index där asterisker finns
    df.drop(indexStar, inplace=True)                    # Tar bort alla dessa index ur df
    df['Flow (l/s)'] = df['Flow (l/s)'].astype(float)   # Byter Flow (l/s) från object till float
    df_time_sorted = df.groupby('Date').mean()          # Grupperar df för dag och tar medelvärdet

    return df_time_sorted
