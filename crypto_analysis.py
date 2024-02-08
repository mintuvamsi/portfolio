import requests
import datetime
import pandas as pd

def get_historical_data(symbol, limit):
    endpoint = "https://min-api.cryptocompare.com/data/v2/histoday"
    
    # Calculate timestamps for the last 6 months
    end_time = int(datetime.datetime.now().timestamp())
    start_time = int((datetime.datetime.now() - datetime.timedelta(days=180)).timestamp())
    
    params = {
        'fsym': symbol,  # Cryptocurrency symbol (e.g., BTC, ETH)
        'tsym': 'USD',   # Convert to USD, but you can change it to another fiat or crypto
        'limit': limit,  # Number of data points (maximum is 2000 per request)
        'toTs': end_time,
        'aggregate': 1,
        'e': 'CCCAGG',
        'allData': 'true'
    }

    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to fetch data")
        return None

# Example usage: Fetch historical data for Bitcoin (BTC) for the last 6 months
btc_data = get_historical_data('BTC', 180)
if btc_data:
    print(btc_data)  # Process or analyze the data as per your requirements

# print(type(btc_data))
df = pd.DataFrame(btc_data)

print(df)