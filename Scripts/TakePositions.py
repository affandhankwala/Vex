import numpy as np
import PredictNext
import ATR
from position import Position
import generateWinRate
import generateTable
from typing import List, Tuple

def getInitialAccount():
    return 25000        # Inital account value

def takePositions(name: str, rr: float, pair: str, open: List, close: List, high: List, low: List) -> float:

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
    # Iterate through every wick
    for i in range(len(open[0]) - 3):

        # Calculate the position size
        # Max loss = account * slRisk
        # Movement per pip = SL/max loss
        # Units = Movement * 10,000
        # Lot = Movement / 10
        # SL = 100,000 Units = $10 per pip = 1 Lot
        # miniL = 10,000 Units = $1 per pip = 0.1 Lot
        # microL = 1,000 Units = $0.10 per pip = 0.01 Lot
        SL = ATR.get_atr(low[0], high[0], i, 15)          # Set SL to ATR for now

        lotSize = (totalAccount * slRisk / (SL * 1000)) / 10   

        # Only enter on uptrend or downtrend for now
        # Uptrend if the next three candles close higher than previous
        if inTrade:
            
            # Check if the trade has been stopped out
            if myP.hitSL(low[0][i], high[0][i]):
                myP.invertValue()
                myP.setResult('LOSS')

            elif myP.hitTP(low[0][i], high[0][i], rr):
                myP.profitValue()
                myP.setResult('WIN')
            
            else: 
                # Update the current price
                myP.setCurrentPrice(open[0][i])
                continue            # If not stopped out, keep evaluating position

            # Add the position into the array
            totalAccount += myP.getPosValue()
            positions.append(myP)           
            inTrade = False
            
            # New position object
            myP = Position()
            
        else:
            direction = determine_enter(close, i)
            if direction != "":
                myP.enterTrade(pair, open[0][i], direction, lotSize, SL, rr)
            else: continue
        
    print("Ending Account: " +(str)(round(totalAccount, 2)))

    generateTable.makeTable(name, positions, 
                  generateWinRate.metrics(positions, getInitialAccount()))
    
    return round(totalAccount, 2)

# This method determines what direction to enter
def determine_enter (close: List, location: int) -> str:
    if close[4][location] > close[3][location] and close[3][location] > close[2][location]:
        return "BUY"
    elif close[4][location] < close[3][location] and close[3][location] < close[2][location]:
        return "SELL"
    return ""

# This method returns the sl pip count in 0.000f
def get_true_sl(atr: float, sl_to_atr_ratio: float):
    return atr * sl_to_atr_ratio

# This method returns price of SL given parameters
def get_prices(direction: str, ask_price: float, bid_price: float, true_sl: float, rr: float) -> Tuple:
    if direction == "BUY":
        return ask_price - true_sl, ask_price + (true_sl * rr)
    else: 
        return bid_price + true_sl, bid_price - (true_sl * rr)
    
# This method returns the lotsize and units required for trade
# TODO: MAKE SURE THIS CAN HANDLE CONVERSION RATIOS
def get_units(true_sl: int, risk: float, account_value: float, leverage: float) -> float:
    per_pip = (account_value * risk) / true_sl
    if (per_pip * 100000 )< (leverage * account_value):
        print(f'{per_pip} standard lots')
        return per_pip * 10000
    elif (per_pip * 10000) < (leverage * account_value):
        print(f'{per_pip} mini lots')
        return per_pip * 1000
    elif (per_pip * 1000) < (leverage * account_value):
        print(f'{per_pip} micro lots')
        return per_pip * 100
    else: return 0

def check_JPY (pair: str) -> bool:
    return pair[-3:] == 'JPY'