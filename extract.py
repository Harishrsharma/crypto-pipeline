import requests
import pandas as pd
from datetime import datetime

def fetch_crypto_data(coin_list, currency="usd"):
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": ",".join(coin_list), "vs_currencies": currency}
    
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    
    rows = []
    for coin in coin_list:
        rows.append({
            "coin_name": coin,
            "price": data[coin][currency],
            "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    # Return the result so main.py can catch it
    return pd.DataFrame(rows)