import requests
import os
import csv

api_key = "3296284c895481ff108b05e4946e96e3-3258b5cd4be74fdabadead67a4a77f37"
base_url = "https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles"
granuality = "H1"
pair = "EURUSD"
params = {
    "granularity": granuality,  # Hourly timeframe
    "count": 100,          # Number of candles to retrieve
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
    relativePath = f'Files\CandleData\{granuality}\{pair}_{granuality}_candles.csv'
    fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), relativePath)
    if not os.path.exists(fileName):
        os.makedirs(fileName)
            
    with open(fileName, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['time', 'open', 'high', 'low', 'close', 'volume'])
        for candle in candles:
            writer.writerow([candle['time'], candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c'], candle['volume']])
    
    print(f"Candles data saved to {fileName}")
else:
    # Handle unsuccessful request
    print("Error:", response.status_code, response.text)