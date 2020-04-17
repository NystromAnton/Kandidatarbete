from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
from datetime import time


#-------------------------------------------------
# Läser in en df som är fritt från asterisker från givet dataset
# In: dataset
# Out: DataFrame med column för datum("Date") och flöde("Flow (l/s)")
# Side effect: -
#-------------------------------------------------
def converter(dataset):
    data_folder = Path("Data/")                                         # Metod för att pathen ska funka på både linux och windows
    loc = data_folder / dataset                                         # För att hitta filen
    df = pd.read_csv(loc, sep= ';', decimal= ',', engine= 'python')     # Läs in filen som en DataFrame. OBS använder python som engine - funkar men tydligen ganska långsamt
    indexStar = df[df['Flow (l/s)'] == '*' ].index                      # Hitta alla index där asterisker finns
    df.drop(indexStar, inplace=True)                                    # Tar bort alla dessa index ur df

    df['Flow (l/s)'] = df['Flow (l/s)'].astype(float)                   # Byter column 'Flow (l/s)' från object till float
    df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])          # Converterar columnerna 'Date' och 'Time' från object till datetime64
    df.drop(['Time'], axis=1, inplace=True)                             # Tar bort column 'Time'
    return df


#-------------------------------------------------
# Räknar ut medelvärdet för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dateMean(dataset):

    df = converter(dataset)                                 # Rensar dataset till df

    df_sorted = df.groupby(df['Date'].dt.date).mean()       # Grupperar df för dag och tar medelvärdet

    return df_sorted


#-------------------------------------------------
# Räknar ut medelvärdet mellan 0-5 varje natt för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def nightMean(dataset):

    df = converter(dataset)                                              # Rensar dataset till df

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    dfResult = df.groupby(df['Date'].dt.date).mean()                     # Räknar ut medelvärdet för varje datum
    indexHour = [5, 6, 7, 8, 9, 10, 11, 12, 13, 
                14, 15, 16, 17, 18, 19, 20, 21, 22, 23]                  # Alla timmar från 0-23 som ska bort

    for i in range(len(dfSize)):
        indexMax = dfSize.iloc[i]                                        # Tar fram antalet datapunker för datum 'i'
        dfMean = df.head(indexMax)                                       # Tar fram datum 'i'
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar
        df.drop(df.head(indexMax).index, axis=0, inplace=True)           # Datum 'i' tas bort från df
        if len(dfMean) == 24:                                           
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort 
            dfResult['Flow (l/s)'][i] = dfMean.mean()[0]                 # Medelflödet på natten läggs in i 'dfResult'
        else:
            break                                                        # Räknar inte med den sista dagen

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet mellan 9-17 varje dag för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dayMean(dataset):

    df = converter(dataset)                                              # Rensar dataset till df

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    dfResult = df.groupby(df['Date'].dt.date).mean()                     # Räknar ut medelvärdet för varje datum
    indexHour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
                17, 18, 19, 20, 21, 22, 23]                              # Alla timmar från 0-23 som ska bort

    for i in range(len(dfSize)):
        indexMax = dfSize.iloc[i]                                        # Tar fram antalet datapunker för datum 'i'
        dfMean = df.head(indexMax)                                       # Tar fram datum 'i'
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()               # Datum 'i' grupperas i timmar
        df.drop(df.head(indexMax).index, axis=0, inplace=True)           # Datum 'i' tas bort från df
        if len(dfMean) == 24:                                           
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort                          
            dfResult['Flow (l/s)'][i] = dfMean.mean()[0]                 # Medelflödet på natten läggs in i 'dfResult'
        else:
            break                                                        # Räknar inte med den sista dagen

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme mellan 9-17 varje dag för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dayHours(dataset):

    df = converter(dataset)                                              # Rensar dataset till df

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17, 
                18, 19, 20, 21, 22, 23]                                  # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    format = "%Y-%m-%d"
    f = ['0','1','2','3','4','5','6','7','8','9']
    t = ['00','01','02','03','04','05','06','07','08','09']

    for i in range(len(dfSize)):
        indexMax = dfSize.iloc[i]                                        # Tar fram antalet datapunker för datum 'i'
        dfMean = df.head(indexMax)                                       # Tar fram datum 'i'
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar
        df.drop(df.head(indexMax).index, axis=0, inplace=True)           # Datum 'i' tas bort från df
        if len(dfMean) == 24:                                           
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort                          
        else:
            break                                                        # Räknar inte med den sista dagen

        date = dfSize.index[i]                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):                                     
            data = dfMean.iloc[j][0]                                     # Data för timme 'j'
            hourSTR = dfMean.index[j].astype(str)                        # Gör om int till str
            for k in range(len(f)):                                       
                if hourSTR == f[k]:                                      # Kollar om timmarna är i rätt format
                    hourSTR = t[k]                                       # kl 1 -> kl 01
            dateSTR = date.strftime(format)                              # Gör om datetime.date till str
            time = datetime.fromisoformat(dateSTR + ' ' + 
                                          hourSTR + ':00:00')            # Gör om str till datetime
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [time])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                           # Appendar df på dfResult

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme mellan 0-5 varje natt för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def nightHours(dataset):

    df = converter(dataset)                                              # Rensar dataset till df

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [5, 6, 7, 8, 9, 10, 11, 12, 13, 
                14, 15, 16, 17, 18, 19, 20, 21, 22, 23]                  # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras
    format = "%Y-%m-%d"
    f = ['0','1','2','3','4','5','6','7','8','9']
    t = ['00','01','02','03','04','05','06','07','08','09']

    for i in range(len(dfSize)):
        indexMax = dfSize.iloc[i]                                        # Tar fram antalet datapunker för datum 'i'
        dfMean = df.head(indexMax)                                       # Tar fram datum 'i'
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar
        df.drop(df.head(indexMax).index, axis=0, inplace=True)           # Datum 'i' tas bort från df
        if len(dfMean) == 24:
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort
        else:
            break                                                        # Räknar inte med den sista dagen

        date = dfSize.index[i]                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):                                     
            data = dfMean.iloc[j][0]                                     # Data för timme 'j'
            hourSTR = dfMean.index[j].astype(str)                        # Gör om int till str
            for k in range(len(f)):                                      
                if hourSTR == f[k]:                                      # Kollar om timmarna är i rätt format
                    hourSTR = t[k]                                       # kl 1 -> kl 01
            dateSTR = date.strftime(format)                              # Gör om datetime.date till str
            time = datetime.fromisoformat(dateSTR + ' ' + 
                                          hourSTR + ':00:00')            # Gör om str till datetime
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [time])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                           # Appendar df på dfResult

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme för varje datum
# In: dataset
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dateHours(dataset):

    df = converter(dataset)                                              # Rensar dataset till df

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    dfResult = pd.DataFrame()                                            # df som ska retuneras
    format = "%Y-%m-%d"
    f = ['0','1','2','3','4','5','6','7','8','9']
    t = ['00','01','02','03','04','05','06','07','08','09']

    for i in range(len(dfSize)):
        indexMax = dfSize.iloc[i]                                        # Tar fram antalet datapunker för datum 'i'
        dfMean = df.head(indexMax)                                       # Tar fram datum 'i'
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar
        df.drop(df.head(indexMax).index, axis=0, inplace=True)           # Datum 'i' tas bort från df

        date = dfSize.index[i]                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):                                     
            data = dfMean.iloc[j][0]                                     # Data för timme 'j'
            hourSTR = dfMean.index[j].astype(str)                        # Gör om int till str
            for k in range(len(f)):                                       
                if hourSTR == f[k]:                                      # Kollar om timmarna är i rätt format
                    hourSTR = t[k]                                       # kl 1 -> kl 01
            dateSTR = date.strftime(format)                              # Gör om datetime.date till str
            time = datetime.fromisoformat(dateSTR + ' ' + 
                                          hourSTR + ':00:00')            # Gör om str till datetime
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [time])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                           # Appendar df på dfResult

    return dfResult


