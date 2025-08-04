##tum usdt partiler icin çekme kodu
#io icin, ortak kullanima teşvik et
##symbols.py

import requests

def get_all_usdt_symbols():
    try:
        url = "https://api.binance.com/api/v3/exchangeInfo"
        res = requests.get(url)
        data = res.json()
        symbols = [
            s["symbol"]
            for s in data["symbols"]
            if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"
        ]
        return symbols
    except Exception:
        return ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
