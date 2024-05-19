import numpy as np
import math
import PredictNext
import createTable
import ATR
from position import Position

def takePositions():
    name = 'EURUSD_2023-2024.csv'                                               # File to grab data form csv format


    actual_O, ytrain_O, next1_O, next2_O, next3_O, mse_O = PredictNext.predict_next(name, 'open')
    actual_C, ytrain_C, next1_C, next2_C, next3_C, mse_C = PredictNext.predict_next(name, 'close')
    actual_H, ytrain_H, next1_H, next2_H, next3_H, mse_H = PredictNext.predict_next(name, 'high')
    actual_L, ytrain_L, next1_L, next2_L, next3_L, mse_L = PredictNext.predict_next(name, 'low')

    # List of positions to take
    positions = []

    # Position Object
    myP = Position()

    # All arrays are same size

    # Boolean to hold whether in trade or not
    inTrade = False
    # Iterate through every wick
    for i in range(len(actual_O)):
        # Only enter on uptrend or downtrend for now
        # Uptrend if the next three candles close higher than previous
        if inTrade:
            # Get SL if SL not assigned
            if myP.getSL() < -1:
                myP.setSL(ATR.getATR(actual_L, actual_H, i))         # Set SL to ATR for now

                
                
            return -1 # If in trade, evaluate if SL or TP hit
        
        elif next3_C > next2_C and next2_C > next1_C:
            # Uptrend confirmed
            myP.enterTrade(actual_O[i], 'BUY')
            inTrade = True

        # Downtrend if the next three candles close lower than previous
        elif next3_C < next2_C and next2_C < next1_C:
            # Downtrend confirmed
            myP.enterTrade(actual_O[i], 'SELL')
            inTrade = True
        else:
            # For now, dont enter a trade
            continue
        positions.append(myP.getDirection)

        # Enter at start of current candle
        myP.setEntryPrice(actual_O[i])
        myP.setCurrentPrice(actual_O[i])







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