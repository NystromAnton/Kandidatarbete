from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta, time
from time import process_time

#-------------------------------------------------
# Läser in en df som är fritt från asterisker från givet path
# In: path, csv fil att läsa in
# Out: DataFrame med column för datum("Date") och flöde("Flow (l/s)")
# Side effect: -
#-------------------------------------------------
def converter(path):
    start = process_time()

    df = pd.read_csv(path, sep= ';', decimal= ',', engine= 'python')    # Läser in csv fil from path
    df.rename(columns={df.columns[2 ]:'Flow (l/s)'}, inplace=True)       # Översätter den tredje columnen till 'Flow (l/s)'
    indexStar = df[df['Flow (l/s)'] == '*' ].index                      # Hitta alla index där asterisker finns
    df.drop(indexStar, inplace=True)                                    # Tar bort alla dessa index ur df

    df['Flow (l/s)'] = df['Flow (l/s)'].astype(float)                   # Byter column 'Flow (l/s)' från object till float
    df['Date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])          # Converterar columnerna 'Date' och 'Time' från object till datetime64
    df.drop(['Time'], axis=1, inplace=True)                             # Tar bort column 'Time'

    end = process_time()
    elapsed = end - start
    #print("Converter: " + str(elapsed))
    return df


#-------------------------------------------------
# Räknar ut medelvärdet för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dateMean(path):

    df = converter(path)                                    # Rensar path till df

    start = process_time()

    df_sorted = df.groupby(df['Date'].dt.date).mean()       # Grupperar df för dag och tar medelvärdet

    end = process_time()
    #print("dateMean: " + str(end - start))

    return df_sorted


#-------------------------------------------------
# Räknar ut medelvärdet mellan 0-5 varje natt för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def nightMean(path):

    df = converter(path)                                              # Rensar path till df

    start = process_time()

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [5, 6, 7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 21, 22, 23]                  # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    indexMin = 0
    indexMax = 0
    for i in range(len(dfSize)):
        indexMin = indexMax
        indexMax = indexMin + dfSize.iloc[i]
        dfMean = df.iloc[indexMin:indexMax]
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()                                  # Datum 'i' grupperas i timmar
        if len(dfMean) == 24:
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)                          # Timmarna tas bort
            dfData = pd.DataFrame({"Flow (l/s)":dfMean.mean()[0]}, index = [dfSize.index[i]])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                                                  # Appendar df på dfResult
        else:
            break                                                                               # Räknar inte med den sista dagen

    end = process_time()
    #print("nightMean: " + str(end - start))


    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet mellan 9-17 varje dag för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dayMean(path):

    df = converter(path)                                              # Rensar path till df

    start = process_time()

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                17, 18, 19, 20, 21, 22, 23]                              # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    indexMin = 0
    indexMax = 0
    for i in range(len(dfSize)):
        indexMin = indexMax
        indexMax = indexMin + dfSize.iloc[i]
        dfMean = df.iloc[indexMin:indexMax]
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()                                  # Datum 'i' grupperas i timmar
        if len(dfMean) == 24:
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)                          # Timmarna tas bort
            dfData = pd.DataFrame({"Flow (l/s)":dfMean.mean()[0]}, index = [dfSize.index[i]])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                                                  # Appendar df på dfResult
        else:
            break                                                                               # Räknar inte med den sista dagen

    end = process_time()
    #print("dayMean: " + str(end - start))

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme mellan 9-17 varje dag för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dayHours(path):

    df = converter(path)                                              # Rensar path till df

    start = process_time()

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 17,
                18, 19, 20, 21, 22, 23]                                  # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    indexMin = 0
    indexMax = 0
    for i in range(len(dfSize)):
        indexMin = indexMax
        indexMax = indexMin + dfSize.iloc[i]
        dfMean = df.iloc[indexMin:indexMax]
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar

        if len(dfMean) == 24:
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort
        else:
            break                                                        # Räknar inte med den sista dagen

        dtArray = dfSize.index                                           # Tar fram datumet för datum 'i'
        tmArray = dfMean.index                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):
            data = dfMean.iloc[j][0]                                          # Data för timme 'j'
            dt = dtArray[i]                                                   # Tar fram datumet för datum 'i'
            tm = time(tmArray[j])
            indexDate = datetime.combine(dt,tm)
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [indexDate])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                                # Appendar df på dfResult


    end = process_time()
    #print("dayHours: " + str(end - start))

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme mellan 0-5 varje natt för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def nightHours(path):

    df = converter(path)                                              # Rensar path till df

    start = process_time()

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    indexHour = [5, 6, 7, 8, 9, 10, 11, 12, 13,
                14, 15, 16, 17, 18, 19, 20, 21, 22, 23]                  # Alla timmar från 0-23 som ska bort
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    indexMin = 0
    indexMax = 0
    for i in range(len(dfSize)):
        indexMin = indexMax
        indexMax = indexMin + dfSize.iloc[i]
        dfMean = df.iloc[indexMin:indexMax]
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar

        if len(dfMean) == 24:
            dfMean.drop(dfMean.index[indexHour], axis=0, inplace=True)   # Timmarna tas bort
        else:
            break                                                        # Räknar inte med den sista dagen

        dtArray = dfSize.index                                           # Tar fram datumet för datum 'i'
        tmArray = dfMean.index                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):
            data = dfMean.iloc[j][0]                                          # Data för timme 'j'
            dt = dtArray[i]                                                   # Tar fram datumet för datum 'i'
            tm = time(tmArray[j])
            indexDate = datetime.combine(dt,tm)
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [indexDate])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                                # Appendar df på dfResult


    end = process_time()
    #print("nightHours: " + str(end - start))

    return dfResult


#-------------------------------------------------
# Räknar ut medelvärdet för varje timme för varje datum
# In: path, csv fil att läsa in
# Out: DataFrame med datum som index och "Flow (l/s)" som column
# Side effect: -
#-------------------------------------------------
def dateHours(path):

    df = converter(path)                                              # Rensar path till df

    start = process_time()

    dfSize = df.groupby(df['Date'].dt.date).size()                       # Summerar alla datapunkter med samma datum
    dfResult = pd.DataFrame()                                            # df som ska retuneras

    indexMin = 0
    indexMax = 0
    for i in range(len(dfSize)):
        indexMin = indexMax
        indexMax = indexMin + dfSize.iloc[i]
        dfMean = df.iloc[indexMin:indexMax]
        dfMean = dfMean.groupby(dfMean['Date'].dt.hour).mean()           # Datum 'i' grupperas i timmar

        dtArray = dfSize.index                                           # Tar fram datumet för datum 'i'
        tmArray = dfMean.index                                           # Tar fram datumet för datum 'i'
        for j in range(len(dfMean)):
            data = dfMean.iloc[j][0]                                          # Data för timme 'j'
            dt = dtArray[i]                                                   # Tar fram datumet för datum 'i'
            tm = time(tmArray[j])
            indexDate = datetime.combine(dt,tm)
            dfData = pd.DataFrame({"Flow (l/s)":data}, index = [indexDate])   # Skapar en df med index datum 'i' och column 'Flow (l/s)' för timme 'j'
            dfResult = dfResult.append(dfData)                                # Appendar df på dfResult

    end = process_time()
    #print("dateHours: " + str(end - start))

    return dfResult
