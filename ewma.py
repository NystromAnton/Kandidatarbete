import pandas as pd
import numpy as np
import xlrd
import matplotlib
import matplotlib.pyplot as plt
import dateutil
import math




def o_ewma(df):
    print(df)
    data = df['Flow (l/s)']                     # Plocka ut kolumnen med originaldatan. Vet inte om man ska göra detta på originaldatan eller flytande dygn egentligen.
    avg_ewma = data.mean()
    std_ewma = data.std()
    alpha = 0.3
    dataEWMA = data.ewm(alpha=alpha, adjust=False).mean()          # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.

    df['EWMA'] = dataEWMA                          # Skapa en ny kolumn i DataFramen som är EWMA
    s_ewma = math.sqrt((alpha/(2-alpha))*(std_ewma**2))
    ewma_ucl = avg_ewma + 3*s_ewma
    ewma_lcl = avg_ewma - 3*s_ewma
    df['UCL_EWMA'] = ewma_ucl
    df['LCL_EWMA'] = ewma_lcl

    count_row = range(df.shape[0])
    print(count_row)
    df['num_rows'] = count_row
    print(df)
    indexNames = df[(df['EWMA'] > ewma_ucl)|(df['EWMA'] < ewma_lcl) ].num_rows
    print(indexNames)
    print(type(indexNames))

    ax = plt.gca()                                 # Axlarna för ploten
    #df.plot(y='Flow (l/s)', color="blue",ax=ax)    # Plotta originaldatan
    df.plot(y='EWMA', color='green', ax=ax)         # Plotta EWMA
    df.plot(y='UCL_EWMA', color='red', ax=ax)
    df.plot(y='LCL_EWMA', color='red', ax=ax)

    for i in indexNames:
        ax.axvline(x=i, color="purple", linestyle="--")


    #plt.show()
    return



def o_ewma_train_test(df):
    rows = df.shape[0]
    train = round(rows* 0.7)

    df_train = df.iloc[:train, :]
    df_test = df.iloc[train:,:]
    print("df_train")
    print(df_train)
    print("df_test")
    print(df_test)

    #data = df['Flow (l/s)']                     # Plocka ut kolumnen med originaldatan. Vet inte om man ska göra detta på originaldatan eller flytande dygn egentligen.
    data = df_train['Flow (l/s)']
    avg_ewma = data.mean()
    std_ewma = data.std()
    alpha = 0.3

    data_test = df_test['Flow (l/s)']
    dataEWMA = data_test.ewm(alpha=alpha, adjust=False).mean()          # Räkna ut EWMA. Com är typ en skalär vet inte riktig hur viktig den är. Det verkar kanske vara lite som man själv vill.


    df_test['EWMA'] = dataEWMA                          # Skapa en ny kolumn i DataFramen som är EWMA
    s_ewma = math.sqrt((alpha/(2-alpha))*(std_ewma**2))
    ewma_ucl = avg_ewma + 3*s_ewma
    ewma_lcl = avg_ewma - 3*s_ewma
    df_test['UCL_EWMA'] = ewma_ucl
    df_test['LCL_EWMA'] = ewma_lcl

    count_row = range(df.shape[0])

    #df['num_rows'] = count_row
    #indexNames = df[(df['EWMA'] > ewma_ucl)|(df['EWMA'] < ewma_lcl) ].num_rows


    ax = plt.gca()                                 # Axlarna för ploten
    df_test.plot(y='Flow (l/s)', color="blue",ax=ax)    # Plotta originaldatan
    df_test.plot(y='EWMA', color='green', ax=ax)         # Plotta EWMA ax=ax
    df_test.plot(y='UCL_EWMA', color='red', ax=ax)
    df_test.plot(y='LCL_EWMA', color='red', ax=ax)

    #for i in indexNames:
     #   ax.axvline(x=i, color="purple", linestyle="--")

    plt.show()                                     # Visa plotten


##SHIT FUNCTION
def linreg(df):
    from sklearn import datasets, linear_model
    from sklearn.model_selection import train_test_split
    print("hej")
    y = df['Flow (l/s)']
    X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2)


    lm = linear_model.LinearRegression()
    model = lm.fit(X_train, y_train)
    predictions = lm.predict(X_test)

    plt.scatter(y_test, predictions)
    plt.xlabel("True Values")
    plt.ylabel("Predictions")
    plt.show()

    print(model.score(X_test, y_test))
