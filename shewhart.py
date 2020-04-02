import pandas as pd
import xlrd
import matplotlib
import matplotlib.pyplot as plt

def shewhart(df):                    
    avg = df['Flow (l/s)'].mean()                                
    df['avg'] = avg                                    
    std = df['Flow (l/s)'].std() 
    UCL = avg + (3*std)
    LCL = avg - (3*std)                                
    df2 = df.copy()
    lock = True
    while(lock):
        lock = False
        a = len(df2['Flow (l/s)'])
        indexNames = df2[(df2['Flow (l/s)'] > UCL)|(df2['Flow (l/s)'] < LCL) ].index
        df2.drop(indexNames , inplace=True)
        avg = df['Flow (l/s)'].mean()                                
        df2['avg'] = avg                                     
        std = df2['Flow (l/s)'].std() 
        UCL = avg + (3*std)
        LCL = avg - (3*std)  
        if(a > len(df2['Flow (l/s)'])):
            lock = True

                                
    ax = plt.gca()                                      
    df['UCL'] = UCL                          
    df['LCL'] = LCL 
    df.plot(y='Flow (l/s)', color="blue",ax=ax)                            
    df.plot(y='avg', color='black', ax=ax)                                  
    df.plot(y='UCL', color='red', ax=ax)                                   
    df.plot(y='LCL', color='red', ax=ax)                                   

    plt.show()                                                              # Visa plotten

