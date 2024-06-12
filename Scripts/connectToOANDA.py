import requests
import os
import csv
from position import Position
import time

account_id = "101-001-29192683-001"
base_url = 'https://api-fxpractice.oanda.com/v3/accounts/'
api_key = "3296284c895481ff108b05e4946e96e3-3258b5cd4be74fdabadead67a4a77f37"
eur_usd_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
order_url = f'{base_url}{account_id}/orders'
open_pos_url = f'{base_url}{account_id}/openPositions'

headers = {
    "Authorization": f"Bearer {api_key}",
}


def download_data(pair, granularity, count):
    params = {
        "granularity": granularity,  # Hourly timeframe
        "count": count,          # Number of candles to retrieve
    }

    # Send HTTP GET request to API endpoint
    response = requests.get(eur_usd_url, headers=headers, params=params)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response and extract candles data
        candles_data = response.json()
        # Process candles data as needed
        candles = candles_data['candles']
        fileName = f'{pair}_{granularity}_candles.csv'
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
    else:
        # Handle unsuccessful request
        print("Error:", response.status_code, response.text)



        # update_pos(...):
        #   pos.entryPrice = update
        #   pos.SL = SL +- spread
        #   pos.TP = TP +- spread
        #   update other field
        #   Listen()
        #
        # Listen():
        #   while true:
        #       if trade.finish   
        #           update pos with result
        #           get last 500 wicks and repeat predictions

def get_open_pos():
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
        
def monitor_position():         # TODO: fIX THIS to only show when a new position is closed. ? ??
    prev_pos = get_open_pos()
    while True:
        current_pos = get_open_pos()
        # Compare current positions with previous positions
        closed_positions = [pos for pos in prev_pos if pos not in current_pos]

        if closed_positions:
            for pos in closed_positions:
                instrument = pos['instrument']
                units = pos['long']['units'] if pos['long']['units'] != '0' else pos['short']['units']
                message = f'Position closed for {instrument} with {units} units.'
                print(message)
                

        prev_pos = current_pos

        # Wait for a specified time before checking again
        time.sleep(2)  # Check every 60 seconds



def create_order(position):
    # Create the order based on the values of the position
    # Update position object with real entry/sl/tp positions
    data = {
        "order": {
            "instrument": position.getPair(),
            #"units": #TODO: IDENTIFY HOW MANY UNITS IN LOT ,
            "type": "MARKET",
            "positionFill": "DEFAULT",
            "units": (str)(position.getLot()),
            "takeProfitOnFill": {
                "price": (str)(position.getTPPrice())
            },
            "stopLossOnFill": {
                "price": (str)(position.getSLPrice())
            }
            
        }
    }
    response = requests.post(order_url, headers = headers, json=data)
    if response.status_code == 201:
        print("Trade placed successfully")
        print(response.json())
        # TODO: ALTER POSITION TO REFLECT NEW VALUES
        monitor_position()
        # update_pos(account.tradeconfirmation)

    else:
        print ("Err: {response.status_code}")
        print(response.json())


myP = Position()
myP.enterTrade("EUR_USD", 1.0766, 'BUY', 10000, 0.0020, 1.5)
create_order(myP)