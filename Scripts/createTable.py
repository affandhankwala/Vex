import pandas as pd
import numpy as np

def createTable(openActual, openPredicted, closeActual, closePredicted,
                highActual, highPredicted, lowActual, lowPredicted,
                positions, revenueList, accountList, successess,
                leverage, SL):
    
    # Equalize length
    maxSize = max(len(openActual), len(openPredicted), len(closeActual), len(closePredicted),
                len(highActual), len(highPredicted), len(lowActual), len(lowPredicted),
                len(positions), len(revenueList), len(successess))
    openActual = equalize(openActual, maxSize)
    openPredicted = equalize(openPredicted, maxSize)
    closeActual = equalize(closeActual, maxSize)
    closePredicted = equalize(closePredicted, maxSize)
    highActual = equalize(highActual, maxSize)
    highPredicted = equalize(highPredicted, maxSize)
    lowActual = equalize(lowActual, maxSize)
    lowPredicted = equalize(lowPredicted, maxSize)
    positions = equalize(positions, maxSize)
    revenueList = equalize(revenueList, maxSize)
    accountList = equalize(accountList, maxSize)
    successes = equalize(successess, maxSize)

    # Round elements
    openPredicted = roundArr(openPredicted)
    closePredicted = roundArr(closePredicted)
    highPredicted = roundArr(highPredicted)
    lowPredicted = roundArr(lowPredicted)


     # Create DataFrame
    data = {'Actual Open: ': openActual, 
            'Predicted Open: ': openPredicted,
            'Actual Close: ': closeActual,
            'Predicted Close: ': closePredicted,
            'Actual High: ': highActual,
            'Predicted High: ': highPredicted,
            'Actual Low: ': lowActual,
            'Predicted Low: ': lowPredicted,
            'Position Taken: ': positions,
            'Result: ': successes,
            'Profit/Loss: ': revenueList,
            'Account Value: ': accountList}
    
    df = pd.DataFrame(data)
    df.to_csv ('Scripts/Files/table_data.csv', index = True, sep = '\t')
    print(df)

def equalize(arr, maxSize):
    temp = []
    while len(arr) + len(temp) < maxSize:
        temp.append(None)
    arr = np.concatenate((arr, temp))
    return arr

def roundArr (arr):
    for i in range(len(arr)):
        if arr[i] is not None:
            arr[i] = round(arr[i], 4)
    return arr