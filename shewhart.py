import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

#Funktion som genererar plottar som visar en shewhart control chart med övre och undre kontrollgränser
#In: En dataframe
#Out: Inget
#Side effect: ritar upp plottar

def shewhart(df):
    avg = df['Flow (l/s)'].mean()  #Räknar ut medelvärdet på "Flow (l/s)" columnen
    df['avg'] = avg                #Lägger till en ny column med avg värdet
    std = df['Flow (l/s)'].std()   #Räknar ut standardavvikelsen för "Flow (l/s)" columnen
    UCL = avg + (3*std)            #Räknar fram uper control limit
    LCL = avg - (3*std)            #Räknar fram lower control limit
    df2 = df.copy()                #Skapar en kopia av dataframen
    lock = True                    #Bool för att veta när gränserna är optimerade
    while(lock):
        lock = False               #Sätter låset till false
        a = len(df2['Flow (l/s)']) #Tar ut längden på columnen "Flow (l/s)"
        indexNames = df2[(df2['Flow (l/s)'] > UCL)|(df2['Flow (l/s)'] < LCL) ].index #Hittar alla index på datapunkter som har ett värde större än UCL och mindre än LCL
        df2.drop(indexNames , inplace=True) #Droppar alla som är på de beräknade indexarna
        avg = df['Flow (l/s)'].mean()       #Beräknar om medelvärdet på "Flow (l/s)" columnen
        df2['avg'] = avg                    #Sätter nya medelvärdem
        std = df2['Flow (l/s)'].std()       #Beräknar ny standardavvikelse
        UCL = avg + (3*std)                 #Beräknar om UCL
        LCL = avg - (3*std)                 #Beräknar om LCL
        if(a > len(df2['Flow (l/s)'])):     #Kollar om några datapunkter droppades detta varv
            lock = True                     #Låser lock för att köra ett varv till i loopen
    ax = plt.gca()                          #Något för plottarna
    df['UCL'] = UCL                         #Skapar en column med UCL
    df['LCL'] = LCL                         #Skapar en column med LCL
    df.plot(y='Flow (l/s)', color="blue",ax=ax)  #plottar flödesdatan från column "Flow (l/s)"
    df.plot(y='avg', color='black', ax=ax)       #Plottar en medelvärdeslinje
    df.plot(y='UCL', color='red', ax=ax)         #Plottar UCL
    df.plot(y='LCL', color='red', ax=ax)         #Plottar LCL

    #plt.show()                                   # Visa plotten
    return
