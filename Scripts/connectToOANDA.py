import requests
import os
import csv
from position import Position
import time as t
from typing import List, Dict, Tuple, Callable
from datetime import datetime, time

headers = {}
account_id = ""
# Set the header dictionary
def set_credentials(api_key: str, a_id: str) -> None:
    headers["Authorization"] = f"Bearer {api_key}"
    account_id = a_id

# Downloads the requested trade pair and granularity data 
# Returns name of file is success or empty if not
def download_data(pair: str, granularity: str, count: int, pair_url: str) -> str:
    params = {
        "granularity": granularity,  
        "count": count
    }
    # Send HTTP GET request to API endpoint
    response = requests.get(pair_url, headers=headers, params=params)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response and extract candles data
        candles_data = response.json()
        # Process candles data as needed
        candles = candles_data['candles']
        fileName = f'{pair}_{granularity}_{count}_candles.csv'
        directoryPath = 'Files\\CandleData'
        filePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), directoryPath, fileName)
        if not os.path.exists(directoryPath):
            os.makedirs(directoryPath)
                
        with open(filePath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['time', 'open', 'high', 'low', 'close', 'volume'])
            for candle in candles:
                writer.writerow([candle['time'], candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c'], candle['volume']])
        
        print(f"Candles data saved to {filePath}")
        return fileName
    else:
        # Handle unsuccessful request
        print("Error:", response.status_code, response.text)
        return ""

def get_account_value(account_url: str) -> float:
    response = requests.get(account_url, headers=headers)
    if response.status_code == 200:
        return float(response.json()['account']['balance'])
    else: 
        print(f"Error fetching account info: {response.status_code} - {response.text}")

def get_bid_ask(pair: str, pair_price_url: str) -> Tuple:
    response = requests.get(pair_price_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices'][0]
        bid_price = prices['bids'][0]['price']
        ask_price = prices['asks'][0]['price']
        print(f"Bid Price: {bid_price}")
        print(f"Ask Price: {ask_price}")
        
    else:
        # Handle error
        print(f"Error: {response.status_code}, {response.text}")
    return bid_price, ask_price

def get_open_pos(open_pos_url: str) -> List:
    # Update prices here
    response = requests.get(open_pos_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        positions = data['positions']
        return positions 
    else:
        print("Failed to retrieve open positions")
        print(response.status_code)
        print(response.json())
        return []
        
def is_trade_open (open_pos_url: str, trade_id: str):
    response = requests.get(open_pos_url, headers=headers)
    if response.status_code == 200:
        open_trades = response.json()['trades']
        for trade in open_trades:
            if trade['id'] == trade_id:
                return True
        return False
    else:
        print(f"Failed to retrieve open trades: {response.status_code}")
        print(response.text)
        return False
    
def monitor_position(open_pos_url: str, trade_id: str) -> bool:         
    while is_trade_open(open_pos_url, trade_id):
        print(f'{trade_id} still open')
        t.sleep(3) # seconds
    print(f'{trade_id} closed')
    return True 




def create_order(trade: Dict, order_url: str, position: Dict) -> FloatingPointError:
    # Create the order based on the values of the position
    # Update position object with real entry/sl/tp positions

    data = {
        "order": {
            "instrument": trade["pair"],
            "type": "MARKET",
            "timeInForce": "FOK",
            "positionFill": "DEFAULT",
            "units": position["units"],
            "takeProfitOnFill": { 
                "price": position["tp_price"],
            },
            "stopLossOnFill": {
                "price": position["sl_price"],
            }
            
        }
    }
    response = requests.post(order_url, headers = headers, json=data)
    if response.status_code == 201:
        print("Trade placed successfully")
        order_response = response.json()
         # Extract the trade ID from the response
        trade_id = None
        
        if 'orderFillTransaction' in order_response:
            # For immediate fills (market orders)
            trade_id = order_response['orderFillTransaction']['id']        
        if trade_id:
            print(f"Trade ID: {trade_id}")
            return trade_id
        else:
            print("Failed to extract trade ID from the response.")
    else:
        print ("Err: {response.status_code}")
        print(response.json())
        return False

def get_trade_ids(open_pos_url: str) -> List:
    response = requests.get(open_pos_url, headers=headers)
    if response.status_code == 200:
        open_trades = response.json()['trades']
        trades = []
        for trade in open_trades:
            trades.append(trade['id'])
        return trades
    else:
        print(f"Failed to retrieve open trades: {response.status_code}")
        print(response.text)
        return None
    
#
# Time related
#

# Return the best pair to trade based on time
def get_best_pair () -> str:
    current_time = datetime.now().time()
    if time(0, 0) <= current_time <= time(2, 0):
        return "EUR_JPY"
    elif time(2, 0) <= current_time <= time(15, 0):
        return "EUR_USD"
    elif time(15, 0) <= current_time <= time(23, 0):
        return "EUR_JPY"