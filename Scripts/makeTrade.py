import PredictNext
import connectToOANDA
import plotRR
import requests
import ATR
from typing import List, Dict, Tuple
import TakePositions

#
# Connect to OANDA
#

# Set the headers within the OANDA connection
def set_broker_headers(api: Dict) -> None:
    connectToOANDA.set_credentials(api["api_key"], api["account_id"])

# Download data on past candles. Returns the name of the new file
def download_candles_csv(trade: Dict, api: Dict) -> str:
    return connectToOANDA.download_data(trade["pair"], trade["granularity"], trade["candle_count"], api["pair_url"])


# Retrieve account value
def get_account_value(api: Dict) -> str:
    return connectToOANDA.get_account_value(api["my_account_url"])
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

# Save best rr to use for the selected granularity and pair
def best_rr (file_name: str, trade: Dict, show_graphs: bool, predictions: Dict) -> float:
    return plotRR.plotRR(file_name, trade["granularity"], trade["pair"],
                         predictions["open"], predictions["close"], predictions["high"],
                         predictions["low"], show_graphs)

# Get the current ATR of the market
def get_current_atr(predictions: Dict, count: int, minimum: int) -> float:
    return ATR.get_atr(predictions["low"][0], predictions["high"][0], count, minimum)
#
# Fetch information from broker
#

# Get the current spread which is the difference between the bid and the ask price
def get_spread(trade: Dict, api: Dict) -> float:
    bid_str, ask_str = connectToOANDA.get_bid_ask(trade["pair"], api["pair_price_url"])
    bid = float(bid_str)
    ask = float(ask_str)
    return bid, ask

def get_open_trades(api: Dict) -> int:
    trades = connectToOANDA.get_trade_ids(api["open_pos_url"])
    if trades:
        return trades[0]
    return None

#
# Place a trade
#

def make_trade(predictions: List, trade: Dict, api: Dict, bid: float, ask: float) -> bool:
    # Determine if safe to enter
    direction = TakePositions.determine_enter(predictions["close"], trade["candle_count"] - 4) 
    if direction != "":
        # We have position to enter trade

        true_sl = TakePositions.get_true_sl(trade["atr"], trade["sl_to_atr_ratio"])
        sl_price, tp_price = TakePositions.get_prices(direction, ask, bid, true_sl, trade["rr"])
        # Calculate the lotsize required
        units = TakePositions.get_units(true_sl * 1000, trade["risk"], trade["account_value"], trade["leverage"])
        buy = 1
        if direction == "SELL": buy = -1 
        # Send off to create order
        position = {
            "sl_price": (str)(round(sl_price, 4)),
            "tp_price": (str)(round(tp_price, 4)),
            "units": (str)(round(units) * buy)
        }

        id = connectToOANDA.create_order(trade, api["order_url"], position)
        
        if id is not None:
            return connectToOANDA.monitor_position(api["open_pos_url"], id)
        
    else: 
        print("Not enterring yet")


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

