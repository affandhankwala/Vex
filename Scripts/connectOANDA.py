import oandapyV20
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.pricing as pricing
#from oandapyV20.contrib.requests import MarketInstrumentCandlesRequest
import requests
import pandas as pd
import os

def connectToOANDA():
    account_id = '101-001-29192683-001'
    api_key = '97e102a88801338be2e82402e8e8e51c-2cd14eaf72f4ad8deee1a0c849346b9a'
    client = oandapyV20.API(access_token = api_key)

    # Get and print account details
    account_details = get_account_details(account_id, client)
    print("Account Details: ")
    printAccountDetails(account_details, ['id', 'currency', 'balance', 'marginRate', 'openTradeCount', 'pendingOrderCount', 'pl', 'commission']) 
       

    # Get and print pricing information for pair
    pair = "EUR_USD"
    printPairPrice(get_price(account_id, client, pair))

    # Get candle data in CSV
    convertCandleDataToCSV(account_id, client, api_key, pair)
    
# Get account details
def get_account_details(account_id, client):
    r = accounts.AccountDetails(accountID=account_id)
    response = client.request(r)
    return response

# Get pricing information for current pair 
def get_price(account_id, client, pair):
    params = {
        "instruments": pair
    }
    r = pricing.PricingInfo(accountID = account_id, params = params)
    response = client.request(r)
    return response

def printAccountDetails(account, arr):
    result = ""
    for i in arr:
        result += i.capitalize() + ": "
        result += (str)(account['account'][i]) + '\n'
    print(result)

def printPairPrice(response):
    priceInfo = response["prices"][0]
    bid = priceInfo["bids"][0]["price"]
    ask = priceInfo["asks"][0]["price"]
    mid_price = (float(bid) + float(ask)) / 2
    print("Bid: " + bid)
    print("Ask: " + ask)
    print("Mid Price: " + (str)(mid_price))

def convertCandleDataToCSV(account_id, client, api_key, pair):
    granuality = "H1"
    params = {
        "granularity": granuality,             # Time frame of candle
        "count": 500,
    }

    # Get candle Data
    url = "https://api-fxpractice.oanda.com/v3/instruments/{}/candles".format(pair)
    headers = {
        "Authorization": "Bearer {}".format(api_key),
        "Accept-Datetime-Format": "RFC3339",
    }
    response = requests.get(url, headers = headers, params = params)

    # Parse data and save to CSV
    if response.status_code == 200:
        data = response.json()["candles"]
        candles_data = [
            {
                "time": candle["time"],
                "open": candle["mid"]["o"],
                "high": candle["mid"]["h"],
                "low": candle["mid"]["l"],
                "close": candle["mid"]["c"]
            }for candle in data
        ]
        df = pd.DataFrame(candles_data)
        df["time"] = pd.to_datetime(df["time"])
        
        # Generate directory to save File
        relativePath = f'Files/CandleData/{granuality}/{pair}_{granuality}_candles.csv'
        fileName = os.path.join(os.path.dirname(os.path.abspath(__file__)), relativePath)
        if not os.path.exists(fileName):
            os.makedirs(fileName)
            
        df.to_csv(fileName, index = False)
        print("Candle data saved to CSV")
    else:
        print("Failed to fetch candle data.")


# Usage
if __name__ == "__main__":
    connectToOANDA()