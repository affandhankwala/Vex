import numpy as np
import math
import PredictNext
import createTable

def takePositions():
    name = 'EURUSD_2023-2024.csv'                                               # File to grab data form csv format
    openActual, openPredicted = PredictNext.predict_next(name, 'open')          # Retrieve all open predictions versus actual data
    closeActual, closePredicted = PredictNext.predict_next(name, 'close')       # Retrieve all close predicctions versus actual data
    highActual, highPredicted = PredictNext.predict_next(name, 'high')          # Retreive all high predictions versus actual data
    lowActual, lowPredicted = PredictNext.predict_next(name, 'low')             # Retrieve all low predictions versus actual data
    
    # List of positions to take
    positions = []

    # All arrays are same size

    # Iterate through every wick
    for i in range(len(openPredicted) - 1):
        # Decide on whether to buy or sell based on difference between current close and next prediction high/low
        currentClose = closeActual[i]
        #if (i >= len(openActual) - 1): break
        tomorrowHighPrediction = highPredicted[i + 1]
        tomorrowLowPrediction = lowPredicted[i + 1]
        position = ''
        if(tomorrowHighPrediction - currentClose > currentClose - tomorrowLowPrediction):
            position = 'BUY'
        else: position = 'SELL'
        positions.append(position)
    evaluatePositions(positions, openActual, closeActual, lowActual, highActual,
                      openPredicted, closePredicted, lowPredicted, highPredicted)
    #printPositions(positions)

def evaluatePositions(positions, openActual, closeActual, lowActual, highActual,
                      openPredicted, closePredicted, lowPredicted, highPredicted):
    # Define base values
    account = 25000
    leverage = 100

    # Calculate SL pips (eventually account of coming day's volatility)
    SL = 75

    # Define success storing variables
    totalSuccess = 0
    totalTrades = len(positions)
    successes = []
    revenueList = []
    accountList = [account]

    # Determine if each position yields profit or not
    for i in range(len(positions)):
        # Calculate amount in trade
        tradeAmount = account / leverage

        # Calculate revenue per pip ~$3.34 per 25k on 1:10 with 75p SL
        pipRevenue = tradeAmount / SL

        # Decimal version of SL
        SLp = SL/10000

        # BUY
        if positions[i] == 'BUY':
            # BUY hit SL if we are 75p below entry (current day OPEN) price
            # No real-time implemented yet so use current day's LOW
            if openActual[i] >= lowActual[i] + SLp:
                # Hit BUY SL
                account -= tradeAmount
                revenueList.append(tradeAmount * -1)
                accountList.append(account)
                successes.append('SL')
            else:
                # Did not Hit SL
                # If OPEN < CLOSE then we made profit otherwise loss
                if openActual[i] < closeActual[i]:
                    totalSuccess += 1
                    successes.append('PROFIT')
                else:
                    successes.append('LOSS')
                # Change account balance accordingly
                revenue = (closeActual[i] - openActual[i]) * pipRevenue * 10000
                revenueList.append(revenue)
                account += revenue
                accountList.append(account)

        # SELL
        if positions[i] == 'SELL':
            # SELL hit SL if we are 75p above entry (current day OPEN) price
            # No real-time implemented yet so use current day's HIGH
            if openActual[i] <= highActual[i] - SLp:
                # Hit SELL SL
                account -= tradeAmount
                revenueList.append(tradeAmount * -1)
                accountList.append(account)
                successes.append('SL')
            else:
                # Did not hit SL
                # If OPEN > CLOSE then we made profit otherwise loss
                if openActual[i] > closeActual[i]:
                    totalSuccess += 1
                    successes.append('PROFIT')
                else:
                    successes.append('LOSS')
                # Change account balance accordingly
                revenue = (openActual[i] - closeActual[i]) * pipRevenue * 10000
                revenueList.append(revenue)
                account += revenue
                accountList.append(account)

    print("Win rate: "+ (str) (totalSuccess / totalTrades) + "\n")
    print("Ending account balance: "+ (str) (account)+ "\n")
    generateTable(openActual, openPredicted, closeActual, closePredicted,
                highActual, highPredicted, lowActual, lowPredicted,
                positions, revenueList, accountList, successes, leverage, SL)
                

def generateTable(openActual, openPredicted, closeActual, closePredicted,
                highActual, highPredicted, lowActual, lowPredicted,
                positions, revenueList, accountList, successes, leverage, SL):
    createTable.createTable(openActual, openPredicted, closeActual, closePredicted,
                highActual, highPredicted, lowActual, lowPredicted,
                positions, revenueList, accountList, successes, leverage, SL)
    

def printPositions(positions):
    for pos in positions:
        print(pos+"\n")

takePositions()