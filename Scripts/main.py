import makeTrade
import connectToOANDA

# Generate dictionary to house all required trade parameters

trade = {
    "pair": "AUD_USD",
    "granularity": "M5",
    "candle_count": 500,
    "account_value": 0,
    "rr": 1.4,
    "risk": 0.01,
    "conversion_ratio": 0,
    "atr": 0,
    "sl_to_atr_ratio": 1,
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
def update_api():
    # Update dictionary with order and open_pos urls
    api["account_url"] = f'{api["base_url"]}/accounts'
    api["my_account_url"] = f'{api["account_url"]}/{api["account_id"]}'
    api["order_url"] =  f'{api["my_account_url"]}/orders'
    api["open_pos_url"] = f'{api["my_account_url"]}/openTrades'
    api["pair_url"] = f'{api["base_url"]}/instruments/{trade['pair']}/candles'
    api["pair_price_url"] = f'{api["my_account_url"]}/pricing?instruments={trade['pair']}'
    api["open_positions_url"] = f'{api["my_account_url"]}/openPositions'

update_api()

# Set Headers
makeTrade.set_broker_headers(api)

# Find out how to check if any positions are currently open
current_trade = makeTrade.get_open_trades(api)

if current_trade:
    connectToOANDA.monitor_position(api["open_pos_url"], current_trade)

while True:
    # Check time
    trade["pair"] = connectToOANDA.get_best_pair()

    # Update api 
    update_api()

    # Retrieve Candle Data and save to file
    file_name = makeTrade.download_candles_csv(trade, api)

    trade["account_value"] = makeTrade.get_account_value(api)

    # Gather predictions
    predictions = makeTrade.make_predictions(file_name)

    # Predict best rr from data
    trade["rr"] = 1.4
    #trade["rr"] = makeTrade.best_rr(file_name, trade, False, predictions)

    # Get current ATR of the market
    trade["atr"] = makeTrade.get_current_atr(predictions, trade["candle_count"] - 1, 15)

    # Retrieve current bid, ask prices
    bid, ask = makeTrade.get_spread(trade, api)

    new_trade = makeTrade.make_trade(predictions, trade, api, bid, ask)


