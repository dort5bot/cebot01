# ======================================
# ✅ MegaBot Final - utils/binance_api.py
# Binance API işlemleri: fiyat alma, veri çekme
# ======================================
import requests

BASE_URL = "https://api.binance.com/api/v3"

def get_price(symbol):
    response = requests.get(f"{BASE_URL}/ticker/price", params={"symbol": symbol})
    return float(response.json()["price"])

def get_orderbook(symbol, limit=100):
    response = requests.get(f"{BASE_URL}/depth", params={"symbol": symbol, "limit": limit})
    return response.json()

def get_klines(symbol, interval="1h", limit=100):
    response = requests.get(f"{BASE_URL}/klines", params={"symbol": symbol, "interval": interval, "limit": limit})
    return response.json()
