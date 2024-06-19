import PredictNext
import connectToOANDA
import plotRR
import requests
import ATR
from typing import List, Dict, Tuple
import TakePositions

# Generate dictionary to house all required trade parameters
trade = {
    "pair": "EUR_USD",
    "granularity": "H1",
    "candle_count": 500,
    "account_value": 0,
    "rr": 1.4,
    "risk": 0.01,
    "conversion_ratio": 0,
    "atr": 0,
    "sl_to_atr_ratio": 2,
    "leverage": 50
}

# Generate a dictionary to house all required OANDA API parameters
api = {
    "account_id": "101-001-29192683-001",
    "account_value": 0,
    "base_url": "https://api-fxpractice.oanda.com/v3",
    "account_url": "",
    "my_account_url": "",
    "api_key": "3296284c895481ff108b05e4946e96e3-3258b5cd4be74fdabadead67a4a77f37",
    "pair_url": "",
    "order_url": "",
    "open_pos_url": "",
    "pair_price_url": ""
   
}
# Update dictionary with order and open_pos urls
api["account_url"] = f'{api["base_url"]}/accounts'
api["my_account_url"] = f'{api["account_url"]}/{api["account_id"]}'
api["order_url"] =  f'{api["my_account_url"]}/orders'
api["open_pos_url"] = f'{api["my_account_url"]}/openTrades'

# Create method to update pair_url as needed
def set_pair_url (pair: str) -> None:
    api["pair_url"] = f'{api["base_url"]}/instruments/{pair}/candles'

# Create method to update pair_price_url as needed
def set_pair_price_url(pair: str) -> None:
    api["pair_price_url"] = f'{api["account_url"]}/{api["account_id"]}/pricing?instruments={pair}'

#
# Connect to OANDA
#

# Set the headers within the OANDA connection
def set_broker_headers(api: Dict) -> None:
    connectToOANDA.set_credentials(api["api_key"], api["account_id"])
set_broker_headers(api)

# Download data on past candles. Returns the name of the new file
def download_candles_csv(trade: Dict, api: Dict) -> str:
    set_pair_url(trade["pair"])
    return connectToOANDA.download_data(trade["pair"], trade["granularity"], trade["candle_count"], api["pair_url"])
file_name = download_candles_csv(trade, api)

# Retrieve account value
def get_account_value(api: Dict) -> str:
    return connectToOANDA.get_account_value(api["my_account_url"])
trade["account_value"] = get_account_value(api)
#
# Gather information on predictions
#

# This method calculates and returns the Dict containing the lists of predictions
def make_predictions(file_name: str) -> Dict:
    # Each prediction is in format: 
    # actual, ytrain, next1, next2, next3, mse
    predictions = {}
    predictions["open"] = PredictNext.predict_next(file_name, 'open')
    predictions["close"] = PredictNext.predict_next(file_name, 'close')
    predictions["high"] = PredictNext.predict_next(file_name, 'high')
    predictions["low"] = PredictNext.predict_next(file_name, 'low')
    return predictions

predictions = make_predictions(file_name)
for key in predictions:
    # Print the mse for each range
    print(f"{key}: {predictions[key][5]}")

# Save best rr to use for the selected granularity and pair
def best_rr (file_name: str, trade: Dict, show_graphs: bool) -> float:
    return plotRR.plotRR(file_name, trade["granularity"], trade["pair"],
                         predictions["open"], predictions["close"], predictions["high"],
                         predictions["low"], show_graphs)

# Get the current ATR of the market
def get_current_atr(predictions: Dict, count: int, minimum: int) -> float:
    return ATR.get_atr(predictions["low"][0], predictions["high"][0], count, minimum)
trade["atr"] = get_current_atr(predictions, trade["candle_count"] - 1, 15)
#
# Fetch information from broker
#

# Get the current spread which is the difference between the bid and the ask price
def get_spread(trade: Dict) -> float:
    set_pair_price_url(trade["pair"])
    bid_str, ask_str = connectToOANDA.get_bid_ask(trade["pair"], api["pair_price_url"])
    bid = float(bid_str)
    ask = float(ask_str)
    return bid, ask
print(get_spread(trade))

#
# Place a trade
#

def make_trade(predictions: List, trade: Dict, api: Dict) -> None:
    # Determine if safe to enter
    direction = TakePositions.determine_enter(predictions["close"], trade["candle_count"] - 4) 
    if direction != "":
        # We have position to enter trade
        # Calculate SL = lowest/highest + (atr) * (sL_to_atr_ratio) and tp
        bid, ask = get_spread(trade)
        true_sl = TakePositions.get_true_sl(trade["atr"], trade["sl_to_atr_ratio"])
        sl_price, tp_price = TakePositions.get_prices(direction, ask, bid, true_sl, trade["rr"])
        # Calculate the lotsize required
        units = TakePositions.get_units(true_sl * 1000, trade["risk"], trade["account_value"], trade["leverage"])

        # Send off to create order
        position = {
            "sl_price": (str)(round(sl_price, 4)),
            "tp_price": (str)(round(tp_price, 4)),
            "units": (str)(round(units))
        }

        id = connectToOANDA.create_order(trade, api["order_url"], position)
        
        if id is not None:
            connectToOANDA.monitor_position(api["open_pos_url"], id)
            # Re-enter position
        
        # Monitor open positions
       

        #TODO: HANDLE POSITION CLOSE
    else: 
        print("Not enterring yet")

while(True):
    success = make_trade(predictions, trade, api)
    print(success)
# {
# Grab candle data
# Predict values
# Find conversion ratio between current pair and USD
# Calculate best rr
# } 1
# Determine if conditions to enter are fair
# Calculate used margin
# Calculate useable margin
# Calculate margin call potential
# Calculate SL
# Calculate TP
# Send trade
# Retrieve Trade information
# Monitor Trade
# Re run loop 1
# Upon trade close, update account values. 
# Loop







#trade["rr"] = best_rr(file_name, trade, False)


print("success")

