import numpy as np
import PredictNext
import ATR
from position import Position
import generateWinRate
import generateTable

def getInitialAccount():
    return 25000        # Inital account value

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
   
    # Account information
    
    totalAccount = getInitialAccount()
    slRisk = 0.01                           # Risk a max of 1% per trade
    rr = 1.3
    # Iterate through every wick
    for i in range(len(actual_O) - 3):

        # Calculate the position size
        # Max loss = account * slRisk
        # Movement per pip = SL/max loss
        # Units = Movement * 10,000
        # Lot = Movement / 10
        # SL = 100,000 Units = $10 per pip = 1 Lot
        # miniL = 10,000 Units = $1 per pip = 0.1 Lot
        # microL = 1,000 Units = $0.10 per pip = 0.01 Lot
        SL = ATR.getATR(actual_L, actual_H, i, 15)          # Set SL to ATR for now

        lotSize = (totalAccount * slRisk / (SL * 1000)) / 10   

        # Only enter on uptrend or downtrend for now
        # Uptrend if the next three candles close higher than previous
        if inTrade:
            
            # Check if the trade has been stopped out
            if myP.hitSL(actual_L[i], actual_H[i]):
                myP.invertValue()
                myP.setResult('LOSS')

            elif myP.hitTP(actual_L[i], actual_H[i], rr):
                myP.setResult('WIN')
            
            else: 
                # Update the current price
                myP.setCurrentPrice(actual_O[i])
                continue            # If not stopped out, keep evaluating position

            # Add the position into the array
            totalAccount += myP.getPosValue()
            positions.append(myP)           
            inTrade = False
            
            # New position object
            myP = Position()
                
        elif next3_C[i] > next2_C[i] and next2_C[i] > next1_C[i]:
            # Uptrend confirmed
            # Set lotSize
            myP.enterTrade(actual_O[i], 'BUY', lotSize, SL, rr)
            inTrade = True

        # Downtrend if the next three candles close lower than previous
        elif next3_C[i] < next2_C[i] and next2_C[i] < next1_C[i]:
            # Downtrend confirmed
            # Set lotSize
            myP.enterTrade(actual_O[i], 'SELL', lotSize, SL, rr)
            inTrade = True
        else:
            # For now, dont enter a trade
            continue
    print("Ending Account: " +(str)(totalAccount))

    generateTable.makeTable(name, positions, 
                  generateWinRate.metrics(positions, getInitialAccount()))
    
    return round(getInitialAccount() - totalAccount, 2)

takePositions()