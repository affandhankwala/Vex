import requests
import os
import csv

def download_data(pair, granularity, count):
    api_key = "3296284c895481ff108b05e4946e96e3-3258b5cd4be74fdabadead67a4a77f37"
    base_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
    params = {
        "granularity": granularity,  # Hourly timeframe
        "count": count,          # Number of candles to retrieve
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    # Send HTTP GET request to API endpoint
    response = requests.get(base_url, headers=headers, params=params)

    # Check if request was successful (status code 200)
    if response.status_code == 200:
        # Parse JSON response and extract candles data
        candles_data = response.json()
        # Process candles data as needed
        candles = candles_data['candles']
        fileName = f'{pair}_{granularity}_candles.csv'
        directoryPath = f'Files\CandleData'
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